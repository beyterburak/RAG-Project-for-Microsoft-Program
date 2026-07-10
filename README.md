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
python main.py catalog           # kataloğu listele, config.py alias'larını doğrula
python main.py hello             # kurulum testi: yerel modelden ilk çıkarım
python main.py embed-demo        # embedding + kosinüs benzerlik demosu
python main.py db-demo           # SQLite şema + serileştirme testi
python main.py prompt-demo       # prompt şablonu davranış gözlemi
python main.py integration-test  # Hafta 1 uçtan uca zincir testi
```

İlk çalıştırmada SDK, donanıma uygun execution provider'ları ve modeli indirir (birkaç dakika sürebilir).

## Proje Yapısı

```
main.py              # giriş noktası (CLI komutları)
config.py            # model alias'ları + RAG parametreleri
src/
  foundry.py         # Foundry Local SDK ortak yardımcıları
  hello_model.py     # kurulum doğrulama testi
  check_catalog.py   # katalog listeleme + alias doğrulama
  similarity.py      # embedding üretimi + kosinüs benzerliği + find_relevant
  db.py              # SQLite şeması + embedding serileştirme
  prompts.py         # Q&A prompt şablonu (REFUSAL, kaynak gösterimi)
  prompt_demo.py     # bağlamlı/bağlamsız davranış gözlemi
  integration_test.py# Hafta 1 uçtan uca zincir testi
data/                # bilgi tabanı belgeleri (Hafta 2)
eval/                # değerlendirme seti ve sonuçlar (Hafta 4)
notebooks/           # deneyler
```

## Hafta 1 Notları (entegrasyon özeti)

Doğrulanan zincir: `embed → SQLite → retrieval → prompt → LLM` (`integration-test` ile).

- **Modeller (katalog teyitli):** sohbet `phi-3.5-mini` (TensorRT-RTX GPU), embedding `qwen3-embedding-0.6b` — 1024 boyut, normalize vektör.
- **Şema kararı:** embedding float32 BLOB (kayıpsız, DB gidiş-dönüşünde skorlar bit düzeyinde aynı); `UNIQUE(source, chunk_index)` + `INSERT OR REPLACE` → idempotent ingestion.
- **Prompt kararı (deney destekli):** sistem yönergesi İngilizce + "soruyla aynı dilde cevapla" — phi-3.5-mini Türkçe yönergede biçim kurallarına uymuyor. Ret cevabı `REFUSAL` sabiti; modelin ret cevabına da kaynak ekleme huyu Hafta 3'te kırpılacak.
- **Gözlem:** bağlamsız modelin uydurma ürün hakkında kendinden emin halüsinasyonu vs bağlamlı kaynaklı doğru cevap — sunum için hazır karşılaştırma.

## Yol Haritası

| Hafta | Odak | Çıktı |
|-------|------|-------|
| 1 | Kurulum + temeller | Çalışan Foundry Local çıkarımı |
| 2 | Chunking + ingestion + retrieval | Dolu SQLite DB + `get_top_chunks()` |
| 3 | LLM entegrasyonu | Baseline RAG botu (v1) |
| 4 | Değerlendirme çatısı | Eval harness + baseline metrikleri |
| 5 | Corrective/Agentic RAG | v2-corrective varyantı |
| 6 | Benchmark + sunum | v1 vs v2 karşılaştırma raporu |
