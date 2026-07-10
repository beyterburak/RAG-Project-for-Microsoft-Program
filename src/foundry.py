"""Foundry Local SDK için ortak yardımcılar.

Tüm komutlar manager'ı buradan alır; böylece EP (execution provider)
kaydı ve tekil (singleton) başlatma tek yerde yönetilir.
"""

import sys

from foundry_local_sdk import Configuration, FoundryLocalManager

import config

_initialized = False


def get_manager() -> FoundryLocalManager:
    """SDK'yı bir kez başlatır ve manager örneğini döndürür."""
    global _initialized
    if not _initialized:
        cfg = Configuration(app_name=config.APP_NAME)
        FoundryLocalManager.initialize(cfg)
        _register_execution_providers(FoundryLocalManager.instance)
        _initialized = True
    return FoundryLocalManager.instance


def _register_execution_providers(manager) -> None:
    """Windows'ta donanım hızlandırma için EP'leri indirir ve kaydeder.

    Cross-platform pakette bu metot bulunmayabilir; o durumda atlanır.
    """
    if not hasattr(manager, "download_and_register_eps"):
        return

    state = {"current": ""}

    def _progress(ep_name: str, percent: float) -> None:
        if ep_name != state["current"]:
            if state["current"]:
                print()
            state["current"] = ep_name
        print(f"\r  EP {ep_name:<30} {percent:5.1f}%", end="", flush=True)

    manager.download_and_register_eps(progress_callback=_progress)
    if state["current"]:
        print()


def ensure_model(alias: str):
    """Modeli katalogdan alır, gerekiyorsa indirir ve yükler."""
    manager = get_manager()
    model = manager.catalog.get_model(alias)
    if model is None:
        print(f"HATA: '{alias}' katalogda bulunamadı. "
              f"Güncel alias'lar için: python main.py catalog")
        sys.exit(1)

    if not model.is_cached:
        print(f"'{alias}' indiriliyor (ilk seferde birkaç dakika sürebilir)...")
        model.download(
            lambda p: print(f"\r  {p:.1f}%", end="", flush=True)
        )
        print()

    if not model.is_loaded:
        print(f"'{alias}' yükleniyor...")
        model.load()

    return model
