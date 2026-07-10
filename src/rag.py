"""Baseline RAG — Hafta 3: uçtan uca answer_query().

Akış: get_top_chunks(soru) → build_qa_messages(bağlam) → yerel LLM → cevap.

Tasarım notları:
- Model bir kez yüklenir (warm-up, Gün 15-16); RagSession yaşadığı sürece
  sorular aynı yüklü model ve web servisi üzerinden cevaplanır.
- Ret tespiti: cevap REFUSAL ile başlıyorsa kuyruk kırpılır (model ret
  cevabına da "(Kaynak: ...)" ekleyebiliyor — Hafta 1 Gün 6 bulgusu).
- Gecikme ölçümü: retrieval ve LLM süreleri ayrı raporlanır (Hafta 4
  latency metriğinin temeli).

Kullanım:
  python main.py ask "soru"   tek soru, ayrıntılı çıktı
  python main.py chat         etkileşimli soru-cevap döngüsü
"""

import time
from dataclasses import dataclass, field

import openai

import config
from src.foundry import get_manager, ensure_model
from src.prompts import REFUSAL, build_qa_messages
from src.retrieval import Chunk, get_top_chunks
from src.similarity import get_embedding_client


@dataclass
class Answer:
    question: str
    answer: str
    chunks: list[Chunk] = field(default_factory=list)
    is_refusal: bool = False
    retrieval_seconds: float = 0.0
    llm_seconds: float = 0.0


class RagSession:
    """Chat modelini bir kez yükleyip art arda soru cevaplayan oturum."""

    def __init__(self):
        self._manager = get_manager()
        # Yükleme sırası önemli (VRAM): önce embedding, sonra chat modeli.
        # Ters sırada phi'nin TensorRT çıkarımı ~2.4 GB isteyip OOM veriyor.
        get_embedding_client()
        self._model = ensure_model(config.CHAT_MODEL_ALIAS)
        self._manager.start_web_service()
        self._client = openai.OpenAI(
            base_url=f"{self._manager.urls[0]}/v1", api_key="none"
        )

    def answer_query(self, question: str, k: int = config.TOP_K) -> Answer:
        t0 = time.perf_counter()
        chunks = get_top_chunks(question, k)
        t1 = time.perf_counter()

        if not chunks:
            return Answer(question, REFUSAL, [], True, t1 - t0, 0.0)

        messages = build_qa_messages(question, [(c.source, c.text) for c in chunks])
        response = self._client.chat.completions.create(
            model=self._model.id, messages=messages,
            temperature=0.2, max_tokens=300,
        )
        t2 = time.perf_counter()

        answer = (response.choices[0].message.content or "").strip()
        is_refusal = answer.startswith(REFUSAL)
        if is_refusal:
            answer = REFUSAL  # ret cevabındaki gereksiz kaynak kuyruğunu kırp

        return Answer(question, answer, chunks, is_refusal, t1 - t0, t2 - t1)

    def close(self):
        self._model.unload()
        self._manager.stop_web_service()


def _print_answer(result: Answer, verbose: bool = True) -> None:
    if verbose:
        print("  Getirilen parçalar:")
        for c in result.chunks:
            print(f"    {c.score:.4f}  [{c.source} / {c.chunk_index}]")
    print(f"\nCevap: {result.answer}")
    print(f"(retrieval {result.retrieval_seconds:.2f} sn, "
          f"LLM {result.llm_seconds:.2f} sn)")


def run_ask(question: str) -> None:
    session = RagSession()
    try:
        result = session.answer_query(question)
        print(f"\nSoru: {question}")
        _print_answer(result)
    finally:
        session.close()


def run_chat() -> None:
    print("Yerel RAG asistanı — çıkmak için 'q' yaz.\n")
    session = RagSession()
    try:
        while True:
            try:
                question = input("Soru> ").strip()
            except EOFError:
                break
            if not question:
                continue
            if question.lower() in ("q", "quit", "exit", "çık"):
                break
            result = session.answer_query(question)
            _print_answer(result, verbose=False)
            sources = ", ".join(sorted({c.source for c in result.chunks}))
            if not result.is_refusal and sources:
                print(f"(bağlam: {sources})")
            print()
    finally:
        session.close()
    print("Görüşürüz!")
