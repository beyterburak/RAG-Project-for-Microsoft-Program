"""Veri yutma hattı — Hafta 2, Gün 10-11.

data/ altındaki belgeleri parçalar, toplu (batch) embed eder ve rag.db'ye
yazar. Idempotent: her belge yazılmadan önce eski parçaları silinir; böylece
belge küçüldüğünde bayat parça kalmaz, aynı belge tekrar yutulunca kopya
oluşmaz.

Kullanım: python main.py ingest
"""

import numpy as np

import config
from src import db
from src.chunking import chunk_directory
from src.similarity import embed_texts


def embed_in_batches(texts: list[str],
                     batch_size: int = config.EMBED_BATCH_SIZE) -> np.ndarray:
    """Uzun listeyi parti parti embed eder (tek dev istek yerine)."""
    parts = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        parts.append(embed_texts(batch))
        done = min(start + batch_size, len(texts))
        print(f"\r  embed: {done}/{len(texts)}", end="", flush=True)
    print()
    return np.vstack(parts)


def run() -> None:
    chunks = chunk_directory()
    if not chunks:
        raise SystemExit(f"HATA: {config.DATA_DIR} altında belge bulunamadı.")

    sources = sorted({source for source, _, _ in chunks})
    print(f"{len(sources)} belge → {len(chunks)} parça. Embedding üretiliyor...")

    vectors = embed_in_batches([text for _, _, text in chunks])

    conn = db.connect()
    try:
        # idempotenlik: yutulan belgelerin eski parçalarını temizle
        for source in sources:
            conn.execute("DELETE FROM documents WHERE source = ?", (source,))
        db.insert_chunks(conn, [
            (source, idx, text, vectors[i])
            for i, (source, idx, text) in enumerate(chunks)
        ])

        # doğrulama: DB'deki kayıt sayısı beklenenle eşleşiyor mu? (plan, Gün 10-11)
        count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        print(f"\nDB doğrulaması: {count} kayıt (beklenen {len(chunks)})", end=" — ")
        if count != len(chunks):
            print("EŞLEŞMİYOR")
            raise SystemExit(1)
        print("EŞLEŞTİ")

        per_source = conn.execute(
            "SELECT source, COUNT(*) FROM documents GROUP BY source ORDER BY source"
        ).fetchall()
        for source, n in per_source:
            print(f"  {source:<36} {n:>3} parça")
        print(f"\nIngestion tamamlandı → {config.DB_PATH}")
    finally:
        conn.close()
