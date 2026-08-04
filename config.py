"""Merkezi yapılandırma: model alias'ları ve RAG parametreleri.

Model alias'larını degistirmeden önce `python main.py catalog` ile
güncel katalogda var olduklarini teyit et.
"""

from pathlib import Path

# --- Foundry Local ---
APP_NAME = "rag-microsoft"

# Sohbet (generation) modeli — Hafta 3 karşılaştırmasıyla seçildi:
# phi-3.5-mini Türkçe çok-parçalı sentezde olguları karıştırıyor;
# qwen3.5-4b 8GB VRAM'e (RTX 3060 Ti) embedding modeliyle birlikte sığmıyor;
# qwen3.5-2b düzgün Türkçe + doğru kaynak gösterimi + kabul edilebilir hız.
CHAT_MODEL_ALIAS = "qwen3.5-2b"
CHAT_MODEL_FALLBACK = "qwen2.5-0.5b"

# Embedding modeli — Foundry Local 1.1+ kataloğunda resmi alias.
EMBEDDING_MODEL_ALIAS = "qwen3-embedding-0.6b"

# --- Yollar ---
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = PROJECT_ROOT / "rag.db"
EVAL_DIR = PROJECT_ROOT / "eval"

# --- RAG parametreleri ---
CHUNK_SIZE = 800        # karakter cinsinden hedef parça boyutu (~1-3 paragraf)
CHUNK_OVERLAP = 150     # ardışık parçalar arası örtüşme (karakter)
TOP_K = 4               # geri getirilecek parça sayısı
EMBED_BATCH_SIZE = 16   # tek istekte embed edilecek parça sayısı

# --- Corrective RAG (v2, Hafta 5) ---
MAX_CORRECTIVE_RETRIES = 1  # sorgu yeniden yazma üst sınırı (sonsuz döngü freni)
WIDE_K = 8                  # corrective ilk getirme havuzu (grader süzer)
MAX_CONTEXT_CHUNKS = 4      # üretime giden en fazla ilgili parça

# Yüksek güven eşiği: top-1 benzerlik bunun üstündeyse grader ve topraklama
# denetimi atlanır (soru v1 hızıyla cevaplanır). Eşik ölçümle seçildi:
# 44 soruluk sette cevaplanamaz soruların en yüksek top-1 skoru 0.6896 —
# 0.70 üstünde yalnız cevaplanabilir sorular var, sızıntı riski yok.
HIGH_CONFIDENCE_SCORE = 0.70
