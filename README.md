# Yerel RAG AI Asistanı

Microsoft Foundry Local ile tamamen çevrimdışı çalışan belge tabanlı soru-cevap (RAG) sistemi.

**Program:** Microsoft Türkiye CSU Yaz Programı 2026 · **Süre:** 6 hafta (13 Temmuz – 23 Ağustos 2026)

## Mimari

Kullanıcı sorusu → SQLite vektör veritabanında benzerlik araması → getirilen parçalar + soru → Foundry Local LLM → kaynağa dayalı cevap. Tüm akış internetsiz, tek cihazda.

- **Sohbet modeli:** `phi-3.5-mini` (bkz. `config.py`)
- **Embedding modeli:** `qwen3-embedding-0.6b`
- **Vektör deposu:** SQLite (brute-force kosinüs benzerliği)

## Kurulum

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# macOS / Linux
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Kullanım

```bash
python main.py catalog   # kataloğu listele, config.py alias'larını doğrula
python main.py hello     # kurulum testi: yerel modelden ilk çıkarım
```

İlk çalıştırmada SDK, donanıma uygun execution provider'ları ve modeli indirir (birkaç dakika sürebilir).

## Proje Yapısı

```
main.py            # giriş noktası (CLI komutları)
config.py          # model alias'ları + RAG parametreleri
src/
  foundry.py       # Foundry Local SDK ortak yardımcıları
  hello_model.py   # Hafta 1: kurulum doğrulama testi
  check_catalog.py # katalog listeleme + alias doğrulama
data/              # bilgi tabanı belgeleri (Hafta 2)
eval/              # değerlendirme seti ve sonuçlar (Hafta 4)
notebooks/         # deneyler
```

## Yol Haritası

| Hafta | Odak | Çıktı |
|-------|------|-------|
| 1 | Kurulum + temeller | Çalışan Foundry Local çıkarımı |
| 2 | Chunking + ingestion + retrieval | Dolu SQLite DB + `get_top_chunks()` |
| 3 | LLM entegrasyonu | Baseline RAG botu (v1) |
| 4 | Değerlendirme çatısı | Eval harness + baseline metrikleri |
| 5 | Corrective/Agentic RAG | v2-corrective varyantı |
| 6 | Benchmark + sunum | v1 vs v2 karşılaştırma raporu |
