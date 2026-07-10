"""Corrective / Agentic RAG (v2) — Hafta 5.

CRAG ruhu: getir → derecelendir → (gerekiyorsa) yeniden yaz & getir → üret.

Baseline'ın ölçülmüş iki hata kategorisine nişan alır (eval v1, Gün 28):
A) Spec-listesi parçası top-K'ya girmiyor → sorgu yeniden yazma +
   genişletilmiş K ile ikinci getirme şansı.
B) Cevaplanamaz soruda parametrik bilgi sızıntısı → grader hiçbir parçayı
   ilgili bulmazsa LLM'e hiç gitmeden güvenli ret.

Döngü freni: en fazla MAX_CORRECTIVE_RETRIES yeniden yazma (config).

Kullanım: python main.py ask "soru" --corrective
"""

import re
from dataclasses import dataclass, field

import config
from src.prompts import REFUSAL, build_qa_messages
from src.rag import Answer, RagSession
from src.retrieval import Chunk, get_top_chunks

GRADER_SYSTEM = """You are a strict relevance grader for a retrieval system.
You will see a QUESTION and numbered PASSAGES.
For each passage decide: does it CONTAIN the specific fact needed to answer the
question (the exact number, name, date or statement being asked for)?
Topical similarity is NOT enough — if the passage discusses the subject but does
not state the requested fact, the verdict is no.
Reply with ONLY one line, one verdict per passage, comma-separated, format: 1:yes, 2:no, 3:yes, 4:no
No explanations."""

VERIFY_SYSTEM = """You are a groundedness checker for a question answering system.
You will see a QUESTION, PASSAGES, and a proposed ANSWER.
Reply "yes" ONLY if the answer's claim is explicitly stated in the passages AND
it answers the question about the exact entity being asked (not a similar one).
If the answer uses knowledge not in the passages, or answers about a different
entity/product, reply "no". Reply with ONLY yes or no."""

REWRITE_SYSTEM = """You rewrite search queries for a document retrieval system.
The original query failed to retrieve relevant passages.
Rewrite it as a short, keyword-rich query in the SAME language, expanding it with
likely synonyms or the document terminology (e.g. technical spec terms).
Reply with ONLY the rewritten query, nothing else."""


@dataclass
class CorrectiveAnswer(Answer):
    """Answer + corrective döngü meta bilgisi."""
    rewritten_query: str | None = None
    attempts: int = 1
    graded_out: int = 0          # elenen parça sayısı (toplam denemelerde)
    forced_refusal: bool = False  # grader kararıyla üretime gitmeden ret


class CorrectiveSession(RagSession):
    """Retrieval grader + query rewrite + düzeltici döngü ile RagSession."""

    def _llm(self, system: str, user: str, max_tokens: int = 100) -> str:
        response = self._client.chat.completions.create(
            model=self._model.id,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=0.0, max_tokens=max_tokens,
        )
        return (response.choices[0].message.content or "").strip()

    GRADE_BATCH = 4      # tek çağrıda değerlendirilen pasaj sayısı (dikkat seyrelmesi freni)
    GRADE_TEXT_CAP = 600  # grader'a giden pasaj uzunluğu sınırı (gecikme freni)

    def grade_chunks(self, question: str, chunks: list[Chunk]) -> list[bool]:
        """Her parça için 'cevabı içeriyor mu' kararı (4'erli partilerle)."""
        flags: list[bool] = []
        for start in range(0, len(chunks), self.GRADE_BATCH):
            batch = chunks[start:start + self.GRADE_BATCH]
            passages = "\n\n".join(
                f"PASSAGE {i + 1}:\n{c.text[:self.GRADE_TEXT_CAP]}"
                for i, c in enumerate(batch)
            )
            raw = self._llm(GRADER_SYSTEM, f"QUESTION: {question}\n\n{passages}")
            verdicts = dict(re.findall(r"(\d+)\s*:\s*(yes|no)", raw.lower()))
            # parse edilemeyen pasaj güvenli tarafta 'ilgili' sayılır (bilgi kaybetme)
            flags.extend(
                verdicts.get(str(i + 1), "yes") == "yes" for i in range(len(batch))
            )
        return flags

    def verify_grounded(self, question: str, answer: str, chunks: list[Chunk]) -> bool:
        """Üretilen cevap pasajlara dayanıyor mu (parametrik sızıntı freni)?"""
        passages = "\n\n".join(c.text[:self.GRADE_TEXT_CAP] for c in chunks)
        raw = self._llm(
            VERIFY_SYSTEM,
            f"QUESTION: {question}\n\nPASSAGES:\n{passages}\n\nANSWER: {answer}",
            max_tokens=5,
        )
        return "yes" in raw.lower()

    def rewrite_query(self, question: str) -> str:
        rewritten = self._llm(REWRITE_SYSTEM, question, max_tokens=60)
        return rewritten.splitlines()[0].strip() or question

    def answer_query(self, question: str, k: int = config.TOP_K) -> CorrectiveAnswer:
        import time
        t0 = time.perf_counter()

        query, attempts, graded_out, rewritten = question, 0, 0, None
        relevant: list[Chunk] = []
        while True:
            attempts += 1
            # geniş havuz getir, sıkı grader süzsün (spec parçası 5-8. sırada
            # kalabiliyor — v1 hata kategorisi A'nın kök nedeni)
            chunks = get_top_chunks(query, config.WIDE_K)
            flags = self.grade_chunks(question, chunks) if chunks else []
            relevant = [c for c, ok in zip(chunks, flags) if ok][:config.MAX_CONTEXT_CHUNKS]
            graded_out += len(chunks) - len(relevant)
            if relevant or attempts > config.MAX_CORRECTIVE_RETRIES:
                break
            query = rewritten = self.rewrite_query(question)

        t1 = time.perf_counter()

        if not relevant:
            # grader hiçbir denemede ilgili parça bulamadı → güvenli ret
            return CorrectiveAnswer(
                question=question, answer=REFUSAL, chunks=[], is_refusal=True,
                retrieval_seconds=t1 - t0, llm_seconds=0.0,
                rewritten_query=rewritten, attempts=attempts,
                graded_out=graded_out, forced_refusal=True,
            )

        messages = build_qa_messages(question, [(c.source, c.text) for c in relevant])
        response = self._client.chat.completions.create(
            model=self._model.id, messages=messages,
            temperature=0.2, max_tokens=300,
        )
        t2 = time.perf_counter()

        answer = (response.choices[0].message.content or "").strip()
        is_refusal = REFUSAL in answer
        if is_refusal:
            answer = REFUSAL

        forced = False
        if not is_refusal and not self.verify_grounded(question, answer, relevant):
            # cevap bağlamda açıkça yok (parametrik sızıntı / yanlış varlık) → ret
            answer, is_refusal, forced = REFUSAL, True, True
        t3 = time.perf_counter()

        return CorrectiveAnswer(
            question=question, answer=answer, chunks=relevant,
            is_refusal=is_refusal, retrieval_seconds=t1 - t0,
            llm_seconds=t3 - t1, rewritten_query=rewritten,
            attempts=attempts, graded_out=graded_out, forced_refusal=forced,
        )
