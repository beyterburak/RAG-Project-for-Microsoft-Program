"""Geri getirme (retrieval) — Hafta 2, Gün 12-13.

get_top_chunks(query, k): sorguyu embed et → rag.db'deki tüm vektörleri
oku → kosinüs benzerliği → en ilgili k parçayı döndür. Küçük N için
brute-force yeterli; koleksiyon büyürse (10k+ parça) vektör indeksine
(FAISS/sqlite-vec) geçiş gerekir — bilinçli sınırlama.

Kullanım:
  python main.py retrieve "soru"   tek sorgu için top-K parçayı göster
  python main.py retrieve          bilinen cevaplı doğrulama setini koştur
"""

from dataclasses import dataclass

import numpy as np

import config
from src import db
from src.similarity import embed_texts, cosine_similarity


@dataclass
class Chunk:
    score: float
    source: str
    chunk_index: int
    text: str


def get_top_chunks(query: str, k: int = config.TOP_K) -> list[Chunk]:
    """Sorguya en benzer k parçayı skorla birlikte döndürür."""
    if not query or not query.strip():
        raise ValueError("Sorgu boş olamaz.")

    conn = db.connect()
    try:
        rows, matrix = db.load_all(conn)
    finally:
        conn.close()
    if not rows:
        return []

    query_vec = embed_texts([query.strip()])[0]
    scores = cosine_similarity(query_vec, matrix)
    top_idx = np.argsort(scores)[::-1][:k]
    return [
        Chunk(float(scores[i]), rows[i][1], rows[i][2], rows[i][3])
        for i in top_idx
    ]


# Bilinen cevaplı doğrulama sorguları (plan, Gün 12-13: manuel doğrulama)
VERIFICATION_QUERIES = [
    ("Zyntrix X9'un pil ömrü ne kadar?", "zyntrix_x9_kilavuz.md"),
    ("E-03 hatası ne anlama geliyor?", "zyntrix_x9_kilavuz.md"),
    ("X9 ile X9 Pro arasındaki fark nedir?", "zyntrix_sss.md"),
    ("Firmware 2.1 sürümünde ne değişti?", "zyntrix_surum_notlari.md"),
    ("İlişkisel veri modelini kim geliştirdi?", "ders_veritabanlari.md"),
    ("Büyük O gösterimini ilk kim kullandı?", "ders_algoritma_karmasikligi.md"),
    ("Backpropagation nasıl çalışır?", "ders_yapay_sinir_aglari.md"),
]


def run(query: str | None = None) -> None:
    if query:
        print(f"Sorgu: {query}\n")
        for c in get_top_chunks(query):
            print(f"  {c.score:.4f}  [{c.source} / parça {c.chunk_index}]")
            print(f"          {c.text.splitlines()[0][:80]}\n")
        return

    print(f"Doğrulama seti ({len(VERIFICATION_QUERIES)} sorgu, beklenen belge top-1'de mi?):\n")
    hits = 0
    for question, expected_source in VERIFICATION_QUERIES:
        top = get_top_chunks(question, k=1)[0]
        ok = top.source == expected_source
        hits += ok
        mark = "OK " if ok else "XX "
        print(f"  {mark} {top.score:.4f}  {question}")
        if not ok:
            print(f"       beklenen: {expected_source}, gelen: {top.source}/{top.chunk_index}")
    print(f"\nSonuç: {hits}/{len(VERIFICATION_QUERIES)} sorguda beklenen belge birinci sırada.")
    if hits < len(VERIFICATION_QUERIES):
        raise SystemExit(1)
