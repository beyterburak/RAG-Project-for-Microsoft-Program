"""SQLite şeması ve embedding serileştirme — Hafta 1, Gün 5.

Şema kararları:
- documents(id, source, chunk_index, chunk_text, embedding)
- embedding: float32 ham baytlar (BLOB) — JSON'a göre ~3x küçük ve kayıpsız
- UNIQUE(source, chunk_index) + INSERT OR REPLACE → ingestion idempotent
  (Hafta 2'de aynı belge yeniden yutulursa kopya oluşmaz)

Kullanım: python main.py db-demo
"""

import sqlite3
from pathlib import Path

import numpy as np

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    id          INTEGER PRIMARY KEY,
    source      TEXT    NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_text  TEXT    NOT NULL,
    embedding   BLOB    NOT NULL,
    UNIQUE (source, chunk_index)
);
"""


def connect(db_path: str | Path = config.DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    return conn


def serialize(vec: np.ndarray) -> bytes:
    return np.asarray(vec, dtype=np.float32).tobytes()


def deserialize(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32)


def insert_chunks(conn: sqlite3.Connection,
                  rows: list[tuple[str, int, str, np.ndarray]]) -> None:
    """rows: (source, chunk_index, chunk_text, embedding) listesi."""
    conn.executemany(
        "INSERT OR REPLACE INTO documents (source, chunk_index, chunk_text, embedding) "
        "VALUES (?, ?, ?, ?)",
        [(s, i, t, serialize(e)) for s, i, t, e in rows],
    )
    conn.commit()


def load_all(conn: sqlite3.Connection) -> tuple[list[int], list[str], np.ndarray]:
    """Tüm parçaları döndürür: (id listesi, metin listesi, (n, d) embedding matrisi)."""
    cur = conn.execute("SELECT id, chunk_text, embedding FROM documents ORDER BY id")
    ids, texts, vecs = [], [], []
    for row_id, text, blob in cur:
        ids.append(row_id)
        texts.append(text)
        vecs.append(deserialize(blob))
    matrix = np.stack(vecs) if vecs else np.empty((0, 0), dtype=np.float32)
    return ids, texts, matrix


def run() -> None:
    """Şema testi: geçici DB'de insert/select + serileştirme gidiş-dönüşü."""
    rng = np.random.default_rng(42)
    demo_rows = [
        ("notlar.md", 0, "Birinci parça metni.", rng.standard_normal(1024).astype(np.float32)),
        ("notlar.md", 1, "İkinci parça metni.", rng.standard_normal(1024).astype(np.float32)),
        ("sss.md", 0, "SSS ilk parçası.", rng.standard_normal(1024).astype(np.float32)),
    ]

    conn = connect(":memory:")

    insert_chunks(conn, demo_rows)
    count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    print(f"Eklenen kayıt: {count} (beklenen 3)")

    # Serileştirme gidiş-dönüşü bit düzeyinde kayıpsız mı?
    _, texts, matrix = load_all(conn)
    original = np.stack([e for _, _, _, e in demo_rows])
    exact = bool(np.array_equal(matrix, original))
    print(f"Embedding gidiş-dönüşü kayıpsız: {exact}")
    print(f"Matris boyutu: {matrix.shape}, dtype: {matrix.dtype}")

    # Idempotenlik: aynı satırlar tekrar yazılınca kopya oluşmamalı
    insert_chunks(conn, demo_rows)
    count2 = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    print(f"Aynı veri tekrar yutulunca kayıt: {count2} (beklenen 3 — idempotent)")

    ok = count == 3 and exact and count2 == 3 and texts[0] == "Birinci parça metni."
    print(f"\nSQLite şema testi: {'BAŞARILI' if ok else 'BAŞARISIZ'}")
    conn.close()
