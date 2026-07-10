"""Merkezi yapılandırma: model alias'ları ve RAG parametreleri.

Model alias'larını degistirmeden önce `python main.py catalog` ile
güncel katalogda var olduklarini teyit et.
"""

from pathlib import Path

# --- Foundry Local ---
APP_NAME = "rag-microsoft"

# Sohbet (generation) modeli — küçük ve hızlı; Hafta 3'te gerekirse büyütülür.
CHAT_MODEL_ALIAS = "phi-3.5-mini"
# Katalogda phi-3.5-mini yoksa catalog komutunun önerdigi alias ile degistir.
CHAT_MODEL_FALLBACK = "qwen2.5-0.5b"

# Embedding modeli — Foundry Local 1.1+ kataloğunda resmi alias.
EMBEDDING_MODEL_ALIAS = "qwen3-embedding-0.6b"

# --- Yollar ---
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = PROJECT_ROOT / "rag.db"
EVAL_DIR = PROJECT_ROOT / "eval"

# --- RAG parametreleri (Hafta 2'de deneylerle ayarlanacak) ---
CHUNK_SIZE = 800        # karakter cinsinden hedef parça boyutu (~1-3 paragraf)
CHUNK_OVERLAP = 150     # ardışık parçalar arası örtüşme (karakter)
TOP_K = 4               # geri getirilecek parça sayısı
