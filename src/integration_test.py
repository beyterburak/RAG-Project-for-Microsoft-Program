"""Hafta 1 entegrasyon testi — tüm yapı taşları uçtan uca.

Akış (Hafta 2-3'ün minyatürü):
  cümleleri embed et → SQLite'a yaz → sorguyu embed et →
  kosinüs benzerliğiyle top-K getir → prompt şablonuna koy → LLM cevabı

Kullanım: python main.py integration-test
"""

import numpy as np
import openai

import config
from src import db
from src.foundry import get_manager, ensure_model
from src.prompts import REFUSAL, build_qa_messages
from src.similarity import DEMO_SENTENCES, embed_texts, cosine_similarity

QUERY = "Hücreler enerjiyi nasıl üretir?"
EXPECTED_KEYWORD = "itokondri"  # büyük/küçük harf farkına takılmasın


def run() -> None:
    failures = []

    # 1) Ingestion minyatürü: embed + SQLite'a yaz
    print("1) Cümleler embed edilip SQLite'a yazılıyor...")
    vectors = embed_texts(DEMO_SENTENCES)
    conn = db.connect(":memory:")
    db.insert_chunks(conn, [
        ("demo.md", i, text, vectors[i]) for i, text in enumerate(DEMO_SENTENCES)
    ])
    count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    print(f"   DB kayıt sayısı: {count}")
    if count != len(DEMO_SENTENCES):
        failures.append("DB kayıt sayısı beklenenle eşleşmiyor")

    # 2) Retrieval minyatürü: DB'den oku + kosinüs top-K
    print("2) Sorgu embed edilip DB üzerinden top-3 getiriliyor...")
    query_vec = embed_texts([QUERY])[0]
    _, texts, matrix = db.load_all(conn)
    scores = cosine_similarity(query_vec, matrix)
    top_idx = np.argsort(scores)[::-1][:3]
    top_chunks = [("demo.md", texts[i]) for i in top_idx]
    print(f"   En iyi eşleşme ({scores[top_idx[0]]:.4f}): {texts[top_idx[0]][:60]}...")
    if EXPECTED_KEYWORD not in texts[top_idx[0]]:
        failures.append("Retrieval beklenen parçayı birinci sıraya koymadı")
    conn.close()

    # 3) Generation minyatürü: prompt şablonu + LLM
    print("3) Getirilen bağlamla LLM cevabı üretiliyor...")
    manager = get_manager()
    model = ensure_model(config.CHAT_MODEL_ALIAS)
    manager.start_web_service()
    try:
        client = openai.OpenAI(base_url=f"{manager.urls[0]}/v1", api_key="none")
        response = client.chat.completions.create(
            model=model.id,
            messages=build_qa_messages(QUERY, top_chunks),
            temperature=0.2, max_tokens=150,
        )
        answer = response.choices[0].message.content.strip()
    finally:
        model.unload()
        manager.stop_web_service()

    print(f"   Cevap: {answer}")
    if not answer:
        failures.append("LLM boş cevap döndürdü")
    if answer.startswith(REFUSAL):
        failures.append("Cevap bağlamda olduğu halde model ret döndürdü")

    print()
    if failures:
        print("ENTEGRASYON TESTİ BAŞARISIZ:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print("ENTEGRASYON TESTİ BAŞARILI — embed → SQLite → retrieval → prompt → LLM zinciri çalışıyor.")
