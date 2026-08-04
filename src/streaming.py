"""SSE olay üretici — Faz 3: canlı işlem kaydı + daktilo akışı.

answer_query'nin olay yayınlayan eşleniği. Dondurulmuş v1/v2 sınıflarına
dokunmaz; CorrectiveSession'ın grade_chunks / rewrite_query /
verify_grounded metotlarını yeniden kullanır.

Olay sırası:
  v1: chunks → token* → done
  v2: graded (deneme başına) → [rewritten] → chunks → token* →
      [verifying → [revoked]] → done

'revoked': üretilen cevap topraklama kontrolünden geçemedi; arayüz yazılmış
metnin üstüne ret mührü basar (denetimde iptal edilen tutanak).
"""

import time
from typing import Iterator

import config
from src.corrective import CorrectiveSession
from src.prompts import REFUSAL, build_qa_messages
from src.retrieval import Chunk, get_top_chunks


def _chunk_dict(c: Chunk) -> dict:
    return {"source": c.source, "chunk_index": c.chunk_index,
            "score": round(c.score, 4), "text": c.text}


def stream_events(session: CorrectiveSession, question: str,
                  variant: str) -> Iterator[dict]:
    t0 = time.perf_counter()
    rewritten: str | None = None

    high_confidence = False
    if variant == "v2":
        query, attempts = question, 0
        chunks: list[Chunk] = []
        while True:
            attempts += 1
            pool = get_top_chunks(query, config.WIDE_K)

            # yüksek benzerlikte denetim atlanır (v1 hızı, ölçülmüş eşik)
            if pool and pool[0].score >= config.HIGH_CONFIDENCE_SCORE:
                chunks = pool[:config.MAX_CONTEXT_CHUNKS]
                high_confidence = True
                yield {"type": "high_confidence", "score": round(pool[0].score, 3)}
                break

            flags = session.grade_chunks(question, pool) if pool else []
            chunks = [c for c, ok in zip(pool, flags) if ok][:config.MAX_CONTEXT_CHUNKS]
            yield {"type": "graded", "attempt": attempts,
                   "kept": len(chunks), "out": len(pool) - len(chunks)}
            if chunks or attempts > config.MAX_CORRECTIVE_RETRIES:
                break
            query = rewritten = session.rewrite_query(question)
            yield {"type": "rewritten", "query": rewritten}
    else:
        chunks = get_top_chunks(question, config.TOP_K)

    t1 = time.perf_counter()
    yield {"type": "chunks", "chunks": [_chunk_dict(c) for c in chunks],
           "seconds": round(t1 - t0, 2)}

    if not chunks:
        yield {"type": "done", "answer": REFUSAL, "is_refusal": True,
               "revoked": False, "rewritten_query": rewritten,
               "retrieval_seconds": round(t1 - t0, 2), "llm_seconds": 0.0}
        return

    messages = build_qa_messages(question, [(c.source, c.text) for c in chunks])
    stream = session._client.chat.completions.create(
        model=session._model.id, messages=messages,
        temperature=0.2, max_tokens=300, stream=True,
    )
    parts: list[str] = []
    for piece in stream:
        if piece.choices and piece.choices[0].delta.content:
            parts.append(piece.choices[0].delta.content)
            yield {"type": "token", "text": piece.choices[0].delta.content}

    answer = "".join(parts).strip()
    is_refusal = REFUSAL in answer
    if is_refusal:
        answer = REFUSAL

    revoked = False
    if variant == "v2" and not is_refusal and not high_confidence:
        yield {"type": "verifying"}
        if not session.verify_grounded(question, answer, chunks):
            revoked, is_refusal, answer = True, True, REFUSAL
            yield {"type": "revoked"}

    t2 = time.perf_counter()
    yield {"type": "done", "answer": answer, "is_refusal": is_refusal,
           "revoked": revoked, "rewritten_query": rewritten,
           "retrieval_seconds": round(t1 - t0, 2),
           "llm_seconds": round(t2 - t1, 2)}
