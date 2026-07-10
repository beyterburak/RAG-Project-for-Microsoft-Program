"""Prompt davranış gözlemi — Hafta 1, Gün 6.

Üç senaryoyu karşılaştırır (plan: "bağlamlı/bağlamsız aynı sorunun
cevap farkını gözlemleme"):
  A) Bağlam VAR, cevap bağlamda VAR   → bağlamdan, kaynaklı cevap beklenir
  B) Bağlam YOK, aynı soru            → modelin baş başa davranışı (kıyas)
  C) Bağlam VAR, cevap bağlamda YOK   → "Bu bilgi belgelerimde yok." beklenir

Bağlam bilerek uydurma bir ürün hakkında: model ön eğitiminden bilemez,
dolayısıyla A'daki doğru cevap ancak bağlamdan gelebilir.

Kullanım: python main.py prompt-demo
"""

import openai

import config
from src.foundry import get_manager, ensure_model
from src.prompts import build_qa_messages, build_plain_messages

# Uydurma bilgi tabanı — ön eğitimde bulunamaz
DEMO_CHUNKS = [
    ("zyntrix_kilavuz.md",
     "Zyntrix X9 taşınabilir hava sensörünün pil ömrü tek şarjla 14 saattir. "
     "Cihaz USB-C ile 90 dakikada tam şarj olur."),
    ("zyntrix_kilavuz.md",
     "Zyntrix X9, PM2.5 ve CO2 ölçümü yapar. Ölçüm aralığı 30 saniyedir ve "
     "veriler yerel hafızada 6 ay saklanır."),
]

QUESTION_IN_CONTEXT = "Zyntrix X9'un pil ömrü ne kadar?"
QUESTION_NOT_IN_CONTEXT = "Zyntrix X9'un satış fiyatı nedir?"


def _ask(client, model_id: str, messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=model_id, messages=messages, temperature=0.2, max_tokens=150,
    )
    return response.choices[0].message.content.strip()


def run() -> None:
    manager = get_manager()
    model = ensure_model(config.CHAT_MODEL_ALIAS)
    manager.start_web_service()
    try:
        client = openai.OpenAI(base_url=f"{manager.urls[0]}/v1", api_key="none")

        print("A) Bağlam VAR, cevap bağlamda VAR")
        print(f"   Soru : {QUESTION_IN_CONTEXT}")
        answer = _ask(client, model.id, build_qa_messages(QUESTION_IN_CONTEXT, DEMO_CHUNKS))
        print(f"   Cevap: {answer}\n")

        print("B) Bağlam YOK (kıyas)")
        print(f"   Soru : {QUESTION_IN_CONTEXT}")
        answer = _ask(client, model.id, build_plain_messages(QUESTION_IN_CONTEXT))
        print(f"   Cevap: {answer}\n")

        print("C) Bağlam VAR, cevap bağlamda YOK")
        print(f"   Soru : {QUESTION_NOT_IN_CONTEXT}")
        answer = _ask(client, model.id, build_qa_messages(QUESTION_NOT_IN_CONTEXT, DEMO_CHUNKS))
        print(f"   Cevap: {answer}")
    finally:
        model.unload()
        manager.stop_web_service()
