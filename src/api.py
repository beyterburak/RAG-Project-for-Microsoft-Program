"""FastAPI katmanı — web arayüzünün (web/) yerel backend'i.

Tasarım kararları:
- Tek CorrectiveSession açılır ve SICAK tutulur: model bir kez yüklenir,
  v1 istekleri aynı oturum üzerinden RagSession.answer_query ile (miras
  alınan baseline davranış), v2 istekleri override edilmiş corrective
  akışla cevaplanır. Etiketli v1/v2 davranışına dokunulmaz.
- Tamamen yerel: yalnız 127.0.0.1'e bağlanır, CORS yalnız localhost:3000.

Kullanım: python main.py serve  →  http://127.0.0.1:8000/docs
"""

import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

import config
from src.corrective import CorrectiveAnswer, CorrectiveSession
from src.rag import Answer, RagSession
from src.streaming import stream_events

_state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Modeller yükleniyor (ilk istekten önce ısınma)...")
    _state["session"] = CorrectiveSession()
    print("Hazır: http://127.0.0.1:8000")
    yield
    _state["session"].close()


app = FastAPI(title="Yerel RAG Arşivi", version="0.1", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    variant: str = Field(default="v1", pattern="^(v1|v2)$")


def _serialize(result: Answer, variant: str) -> dict:
    payload = {
        "variant": variant,
        "question": result.question,
        "answer": result.answer,
        "is_refusal": result.is_refusal,
        "chunks": [
            {"source": c.source, "chunk_index": c.chunk_index,
             "score": round(c.score, 4), "text": c.text}
            for c in result.chunks
        ],
        "retrieval_seconds": round(result.retrieval_seconds, 2),
        "llm_seconds": round(result.llm_seconds, 2),
    }
    if isinstance(result, CorrectiveAnswer):
        payload["corrective"] = {
            "attempts": result.attempts,
            "graded_out": result.graded_out,
            "rewritten_query": result.rewritten_query,
            "forced_refusal": result.forced_refusal,
        }
    return payload


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "chat_model": config.CHAT_MODEL_ALIAS,
        "embedding_model": config.EMBEDDING_MODEL_ALIAS,
        "warm": "session" in _state,
    }


@app.post("/api/ask")
def ask(req: AskRequest) -> dict:
    session: CorrectiveSession = _state["session"]
    question = req.question.strip()
    try:
        if req.variant == "v2":
            result = session.answer_query(question)
        else:
            result = RagSession.answer_query(session, question)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return _serialize(result, req.variant)


@app.post("/api/ask/stream")
def ask_stream(req: AskRequest) -> StreamingResponse:
    session: CorrectiveSession = _state["session"]
    question = req.question.strip()

    def gen():
        try:
            for event in stream_events(session, question, req.variant):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        except ValueError as e:
            yield f"data: {json.dumps({'type': 'error', 'detail': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )


@app.get("/api/corpus")
def corpus() -> dict:
    """Arşivdeki belgeler ve parça sayıları (Arşiv Kataloğu sayfası için)."""
    from src import db

    conn = db.connect()
    try:
        rows = conn.execute(
            "SELECT source, COUNT(*), SUM(LENGTH(chunk_text)), "
            "  (SELECT chunk_text FROM documents i "
            "   WHERE i.source = d.source ORDER BY chunk_index LIMIT 1) "
            "FROM documents d GROUP BY source ORDER BY source"
        ).fetchall()
    finally:
        conn.close()

    belgeler = []
    for source, n, karakter, ilk_parca in rows:
        # Parçaların ilk satırı "Belge Başlığı — Bölüm" biçiminde (chunking.py);
        # dosya adı ASCII olduğu için gerçek başlık buradan alınır.
        ilk_satir = (ilk_parca or "").splitlines()[0] if ilk_parca else source
        baslik = ilk_satir.split(" — ")[0].strip() or source
        belgeler.append({
            "source": source,
            "title": baslik,
            "chunks": n,
            "characters": karakter,
        })
    return {
        "documents": belgeler,
        "total_documents": len(belgeler),
        "total_chunks": sum(b["chunks"] for b in belgeler),
    }


@app.get("/api/results")
def results() -> dict:
    out = {}
    for variant in ("v1-baseline", "v2-corrective", "v3-optimize"):
        path = config.EVAL_DIR / "results" / f"{variant}.json"
        if path.exists():
            out[variant] = json.loads(path.read_text(encoding="utf-8"))
    if not out:
        raise HTTPException(status_code=404, detail="Eval sonucu bulunamadı.")
    return out
