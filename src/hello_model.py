"""'Hello Model' — Hafta 1 kilometre taşı: yerel çıkarım doğrulaması.

Sohbet modelini indirir, yükler, OpenAI-uyumlu yerel REST servisi
üzerinden tek bir soru sorar ve yanıtı akış halinde yazdırır.

Kullanım: python main.py hello
"""

import time

import openai

import config
from src.foundry import get_manager, ensure_model


def run() -> None:
    manager = get_manager()
    model = ensure_model(config.CHAT_MODEL_ALIAS)

    print("Yerel web servisi başlatılıyor...")
    manager.start_web_service()
    base_url = f"{manager.urls[0]}/v1"
    print(f"  Endpoint: {base_url}  (model id: {model.id})")

    try:
        client = openai.OpenAI(base_url=base_url, api_key="none")

        question = "Tek cümleyle: RAG (Retrieval-Augmented Generation) nedir?"
        print(f"\nSoru: {question}\nCevap: ", end="", flush=True)

        start = time.perf_counter()
        stream = client.chat.completions.create(
            model=model.id,
            messages=[
                {"role": "system", "content": "Kısa ve net cevap veren bir asistansın."},
                {"role": "user", "content": question},
            ],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
        elapsed = time.perf_counter() - start

        print(f"\n\nToplam süre: {elapsed:.1f} sn")
        print("Hello Model testi BAŞARILI — Foundry Local çıkarımı çalışıyor.")
    finally:
        model.unload()
        manager.stop_web_service()
