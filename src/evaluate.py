"""Değerlendirme çatısı (eval harness) — Hafta 4.

eval/eval_set.json'daki etiketli soruları RAG hattında koşturur ve ölçer:
- Geri getirme: recall@K (beklenen kaynak top-K'da mı) ve top-1 isabeti
  (kaynak düzeyinde — chunk_index chunking parametresiyle kayabildiği
  için parça değil belge referans alınır)
- Cevap: cevaplanabilirde anahtar kelime isabeti + ret olmaması;
  cevaplanamazda birebir ret (REFUSAL)
- Gecikme: retrieval ve LLM süreleri (ortalama + medyan)

Sonuçlar eval/results/<variant>.json ve .md olarak yazılır.

Kullanım: python main.py eval [--variant v1-baseline]
"""

import json
import statistics
from datetime import date
from pathlib import Path

import config
from src.corrective import CorrectiveSession
from src.rag import RagSession

EVAL_SET_PATH = config.EVAL_DIR / "eval_set.json"
RESULTS_DIR = config.EVAL_DIR / "results"


def _match_keywords(answer: str, keywords: list[str]) -> bool:
    a = answer.casefold()
    return any(k.casefold() in a for k in keywords)


def evaluate_question(session: RagSession, q: dict) -> dict:
    result = session.answer_query(q["question"])
    retrieved_sources = [c.source for c in result.chunks]

    row = {
        "id": q["id"],
        "type": q["type"],
        "question": q["question"],
        "answer": result.answer,
        "retrieved": [f"{c.source}/{c.chunk_index}" for c in result.chunks],
        "is_refusal": result.is_refusal,
        "retrieval_seconds": round(result.retrieval_seconds, 3),
        "llm_seconds": round(result.llm_seconds, 3),
    }

    if q["type"] == "answerable":
        row["recall_hit"] = any(s in retrieved_sources for s in q["expected_sources"])
        row["top1_hit"] = bool(retrieved_sources) and retrieved_sources[0] in q["expected_sources"]
        row["correct"] = (not result.is_refusal) and _match_keywords(result.answer, q["keywords"])
    else:
        row["recall_hit"] = None
        row["top1_hit"] = None
        row["correct"] = result.is_refusal
    return row


def summarize(rows: list[dict]) -> dict:
    answerable = [r for r in rows if r["type"] == "answerable"]
    unanswerable = [r for r in rows if r["type"] == "unanswerable"]
    llm_times = [r["llm_seconds"] for r in rows]
    total_times = [r["llm_seconds"] + r["retrieval_seconds"] for r in rows]
    return {
        "questions": len(rows),
        "recall_at_k": round(sum(r["recall_hit"] for r in answerable) / len(answerable), 3),
        "top1_rate": round(sum(r["top1_hit"] for r in answerable) / len(answerable), 3),
        "answerable_accuracy": round(sum(r["correct"] for r in answerable) / len(answerable), 3),
        "refusal_accuracy": round(sum(r["correct"] for r in unanswerable) / len(unanswerable), 3),
        "overall_accuracy": round(sum(r["correct"] for r in rows) / len(rows), 3),
        "avg_llm_seconds": round(statistics.mean(llm_times), 2),
        "median_total_seconds": round(statistics.median(total_times), 2),
        "top_k": config.TOP_K,
    }


def _write_markdown(path: Path, variant: str, summary: dict, rows: list[dict]) -> None:
    lines = [
        f"# Eval Sonuçları — {variant}",
        f"\nTarih: {date.today().isoformat()} · Model: {config.CHAT_MODEL_ALIAS} · "
        f"Embedding: {config.EMBEDDING_MODEL_ALIAS} · top-K: {summary['top_k']}",
        "\n## Özet\n",
        "| Metrik | Değer |", "|---|---|",
        f"| recall@{summary['top_k']} (cevaplanabilir) | {summary['recall_at_k']:.0%} |",
        f"| top-1 kaynak isabeti | {summary['top1_rate']:.0%} |",
        f"| Cevap doğruluğu (cevaplanabilir) | {summary['answerable_accuracy']:.0%} |",
        f"| Ret doğruluğu (cevaplanamaz) | {summary['refusal_accuracy']:.0%} |",
        f"| Genel doğruluk | {summary['overall_accuracy']:.0%} |",
        f"| Ortalama LLM süresi | {summary['avg_llm_seconds']} sn |",
        f"| Medyan toplam süre | {summary['median_total_seconds']} sn |",
        "\n## Soru bazında\n",
        "| # | Tip | Soru | Doğru? | Recall | Süre (sn) |", "|---|---|---|---|---|---|",
    ]
    for r in rows:
        recall = "-" if r["recall_hit"] is None else ("✓" if r["recall_hit"] else "✗")
        ok = "✓" if r["correct"] else "✗"
        t = r["retrieval_seconds"] + r["llm_seconds"]
        lines.append(f"| {r['id']} | {r['type'][:6]} | {r['question']} | {ok} | {recall} | {t:.1f} |")

    failed = [r for r in rows if not r["correct"]]
    if failed:
        lines.append("\n## Başarısız vakalar (hata analizi girdisi)\n")
        for r in failed:
            lines.append(f"- **#{r['id']}** {r['question']}")
            lines.append(f"  - cevap: {r['answer'][:200]}")
            lines.append(f"  - getirilen: {', '.join(r['retrieved'])}")
    path.write_text("\n".join(lines), encoding="utf-8")


def run(variant: str = "v1-baseline", corrective: bool = False) -> None:
    questions = json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))["questions"]
    RESULTS_DIR.mkdir(exist_ok=True)

    pipeline = "corrective (v2)" if corrective else "baseline (v1)"
    print(f"Eval başlıyor: {len(questions)} soru, varyant: {variant}, hat: {pipeline}\n")
    session = CorrectiveSession() if corrective else RagSession()
    rows = []
    try:
        for q in questions:
            row = evaluate_question(session, q)
            rows.append(row)
            mark = "OK" if row["correct"] else "XX"
            print(f"  {mark} #{row['id']:>2} [{q['type'][:6]}] {q['question'][:60]}")
    finally:
        session.close()

    summary = summarize(rows)
    json_path = RESULTS_DIR / f"{variant}.json"
    json_path.write_text(
        json.dumps({"variant": variant, "summary": summary, "rows": rows},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    md_path = RESULTS_DIR / f"{variant}.md"
    _write_markdown(md_path, variant, summary, rows)

    print("\n--- ÖZET ---")
    for k, v in summary.items():
        print(f"  {k:<24} {v}")
    print(f"\nSonuçlar: {md_path}")
