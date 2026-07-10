"""Q&A prompt şablonu — Hafta 1, Gün 6.

Tasarım kararları (Gün 6 deneyleriyle doğrulandı):
- Sistem yönergesi İNGİLİZCE: phi-3.5-mini Türkçe yönergede biçim
  kurallarına uymuyordu (kaynak etiketi başta, bozuk cümleler);
  İngilizce yönerge + "soruyla aynı dilde cevapla" kuralı ile
  cevap Türkçe kalıyor ve biçim disiplini belirgin iyileşiyor.
- Halüsinasyon freni: bağlamda yoksa REFUSAL metni döner. Model ret
  cevabına da bazen kaynak ekliyor — Hafta 3'te answer_query() ret
  tespitinde REFUSAL ile başlangıç kontrolü yapıp kuyruğu kırpacak.
- Kaynak gösterimi: parçalar [KAYNAK: dosya] etiketiyle verilir,
  cevap "(Kaynak: dosya)" ile biter.
"""

# Ret cevabı — Hafta 3/4'te programatik tespit için sabit
REFUSAL = "Bu bilgi belgelerimde yok."

SYSTEM_PROMPT = f"""You are a document-grounded question answering assistant.

Rules:
1. Answer ONLY using the information in the CONTEXT below.
2. If the answer is not in the context, do not guess and do not cite any source; reply exactly: "{REFUSAL}"
3. Only when you answered from the context, end your answer with the source in this format: (Kaynak: file_name)
4. Always answer in the same language as the question. Be brief."""

CONTEXT_TEMPLATE = """CONTEXT:
{context}

QUESTION: {question}"""


def format_context(chunks: list[tuple[str, str]]) -> str:
    """chunks: (kaynak, metin) listesi → numaralı, kaynak etiketli bağlam bloğu."""
    return "\n\n".join(
        f"[{i + 1}] [KAYNAK: {source}]\n{text}"
        for i, (source, text) in enumerate(chunks)
    )


def build_qa_messages(question: str, chunks: list[tuple[str, str]]) -> list[dict]:
    """RAG cevap üretimi için OpenAI-biçimli mesaj listesi."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": CONTEXT_TEMPLATE.format(
            context=format_context(chunks), question=question)},
    ]


def build_plain_messages(question: str) -> list[dict]:
    """Karşılaştırma için bağlamsız (RAG'sız) mesaj listesi."""
    return [
        {"role": "system", "content": "You are a helpful assistant. "
                                      "Answer briefly, in the language of the question."},
        {"role": "user", "content": question},
    ]
