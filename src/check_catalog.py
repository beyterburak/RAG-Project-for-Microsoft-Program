"""Model kataloğunu listeler ve config.py'daki alias'ları doğrular.

Kullanım: python main.py catalog
"""

import config
from src.foundry import get_manager


def run() -> None:
    manager = get_manager()
    models = manager.catalog.list_models()

    print(f"\nKatalogda {len(models)} model var:\n")
    for m in models:
        alias = getattr(m, "alias", "?")
        model_id = getattr(m, "id", "?")
        print(f"  {alias:<40} {model_id}")

    cached = manager.catalog.get_cached_models()
    if cached:
        print(f"\nYerel önbellekte {len(cached)} model:")
        for m in cached:
            print(f"  {getattr(m, 'alias', getattr(m, 'id', '?'))}")

    print("\n--- config.py alias doğrulaması ---")
    aliases = {getattr(m, "alias", None) for m in models}
    for label, alias in [
        ("Sohbet modeli", config.CHAT_MODEL_ALIAS),
        ("Sohbet yedeği", config.CHAT_MODEL_FALLBACK),
        ("Embedding modeli", config.EMBEDDING_MODEL_ALIAS),
    ]:
        status = "BULUNDU" if alias in aliases else "YOK — config.py'yi güncelle"
        print(f"  {label:<18} {alias:<28} {status}")
