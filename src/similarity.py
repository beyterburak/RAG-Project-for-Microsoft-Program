"""Embedding üretimi ve kosinüs benzerliği — Hafta 1, Gün 3-4.

Bellek-içi benzerlik prototipi: küçük bir cümle listesini embed eder,
sorguya en yakın top-K cümleyi döndürür. find_relevant() Hafta 2'de
SQLite tabanlı get_top_chunks()'ın çekirdeği olacak.

Kullanım: python main.py embed-demo
"""

import numpy as np

import config
from src.foundry import ensure_model

_client = None


def get_embedding_client():
    """Embedding modelini yükler ve istemciyi döndürür (tekil)."""
    global _client
    if _client is None:
        model = ensure_model(config.EMBEDDING_MODEL_ALIAS)
        _client = model.get_embedding_client()
    return _client


def embed_texts(texts: list[str]) -> np.ndarray:
    """Metin listesini (n, d) boyutlu embedding matrisine çevirir."""
    client = get_embedding_client()
    response = client.generate_embeddings(texts)
    return np.array([item.embedding for item in response.data], dtype=np.float32)


def cosine_similarity(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Sorgu vektörü ile matristeki her satır arasındaki kosinüs benzerliği."""
    query_norm = query_vec / np.linalg.norm(query_vec)
    matrix_norms = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix_norms @ query_norm


def find_relevant(query: str, texts: list[str], k: int = config.TOP_K) -> list[tuple[float, str]]:
    """Sorguya en benzer k metni (skor, metin) listesi olarak döndürür."""
    query_vec = embed_texts([query])[0]
    matrix = embed_texts(texts)
    scores = cosine_similarity(query_vec, matrix)
    top_idx = np.argsort(scores)[::-1][:k]
    return [(float(scores[i]), texts[i]) for i in top_idx]


DEMO_SENTENCES = [
    "Fotosentez, bitkilerin güneş ışığını kimyasal enerjiye dönüştürdüğü süreçtir.",
    "Python, okunabilirliği ön planda tutan yüksek seviyeli bir programlama dilidir.",
    "İstanbul Boğazı, Asya ile Avrupa kıtalarını birbirinden ayırır.",
    "Mitokondri, hücrenin enerji santrali olarak görev yapar.",
    "SQLite, sunucu gerektirmeyen tek dosyalık bir veritabanı motorudur.",
    "Osmanlı İmparatorluğu 1453'te İstanbul'u fethetti.",
    "Derin öğrenme modelleri, çok katmanlı yapay sinir ağlarına dayanır.",
    "Kosinüs benzerliği, iki vektör arasındaki açının kosinüsünü ölçer.",
]

DEMO_QUERY = "Hücreler enerjiyi nasıl üretir?"


def run() -> None:
    print(f"Embedding modeli: {config.EMBEDDING_MODEL_ALIAS}\n")

    # Boyut ve normalizasyon kontrolü (plan, Gün 3-4)
    sample = embed_texts([DEMO_SENTENCES[0]])
    dim = sample.shape[1]
    norm = float(np.linalg.norm(sample[0]))
    print(f"Embedding boyutu : {dim}")
    print(f"Vektör normu     : {norm:.4f} "
          f"({'normalize geliyor' if abs(norm - 1.0) < 0.01 else 'normalize DEĞİL — kosinüste normalize ediyoruz'})")

    print(f"\nSorgu: {DEMO_QUERY}\n")
    results = find_relevant(DEMO_QUERY, DEMO_SENTENCES, k=3)
    print("Top-3 sonuç:")
    for score, text in results:
        print(f"  {score:.4f}  {text}")

    best = results[0][1]
    expected = DEMO_SENTENCES[3]  # mitokondri cümlesi
    verdict = "BAŞARILI" if best == expected else "BEKLENENDEN FARKLI"
    print(f"\nBeklenen en yakın cümle: 'Mitokondri...' → {verdict}")
