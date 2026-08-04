# Yerel RAG AI Asistanı

Microsoft Foundry Local ile **tamamen çevrimdışı** çalışan, kaynak gösteren belge soru-cevap (RAG) sistemi. Cevaplar yalnızca yerel belge arşivine dayanır; bilgi arşivde yoksa sistem "bilmiyorum" der.

**Program:** Microsoft Türkiye CSU Yaz Programı 2026

📄 [Proje Raporu](docs/proje-raporu.md) · 📊 [Ölçüm Raporu](eval/results/benchmark_v1_vs_v2.md) · 🎤 [Sunum](docs/sunum-2dk.md)

---

## Mimari

```
Soru → embedding → SQLite'ta kosinüs benzerliği → en ilgili 4 parça
     → bağlam + sistem promptu → yerel LLM → kaynaklı cevap
                    [tamamı tek cihazda, internet yok]
```

| Bileşen | Seçim |
|---|---|
| Sohbet modeli | `qwen3.5-2b` (Foundry Local, TensorRT-RTX hızlandırma) |
| Embedding modeli | `qwen3-embedding-0.6b` (1024 boyut) |
| Vektör deposu | SQLite — float32 blob, brute-force kosinüs |
| Bilgi tabanı | 12 Türkçe belge / 82 parça |
| Arayüz | CLI + web (Next.js + FastAPI) |

Model ve parametre seçimlerinin gerekçeleri için [proje raporuna](docs/proje-raporu.md) bakınız.

## Kurulum

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py ingest
```

macOS/Linux için `python3 -m venv .venv && source .venv/bin/activate`. İlk çalıştırmada SDK, donanıma uygun execution provider'ları ve modelleri indirir (birkaç dakika).

## Kullanım

```bash
python main.py chat            # etkileşimli soru-cevap (önerilen)
python main.py ask "soru"      # tek soru
python main.py serve           # web arayüzü API'si (127.0.0.1:8000)
```

Web arayüzü için ikinci bir terminalde:

```bash
npm --prefix web run dev       # http://localhost:3000
```

<details>
<summary>Değerlendirme ve tanılama komutları</summary>

```bash
python main.py eval                    # 44 soruluk eval seti → v1 metrikleri
python main.py eval --variant v2-corrective --corrective   # denetimli varyant
python main.py ask "soru" --corrective # tek soru, denetimli hat
python main.py retrieve "soru"         # yalnız arama sonuçlarını göster
python main.py catalog                 # model kataloğu + alias doğrulama
python main.py chunk-demo              # parçalama istatistikleri
python main.py integration-test        # uçtan uca zincir testi
```
</details>

## Sonuçlar

44 soruluk etiketli set (35 cevaplanabilir + 9 bilerek cevaplanamaz), 82 parçalık bilgi tabanı:

| Metrik | **v1 (üretim)** | v2 (deneysel) | v3 (deneysel) |
|---|---|---|---|
| Genel doğruluk | **%79.5** | %77.3 | %75.0 |
| Cevap doğruluğu | **%82.9** | %80.0 | %80.0 |
| Ret doğruluğu | **%66.7** | **%66.7** | %55.6 |
| Medyan süre | **8.8 sn** | 26.6 sn | 23.6 sn |

**Üretim varyantı v1.** v2/v3, cevap üretmeden önce getirilen parçaları ve üretilen cevabı ayrıca denetleyen "corrective" hatlardır. Küçük korpusta (43 parça) v2 **+7.7 puan** kazandırıyordu; korpus 82 parçaya çıkıp benzer içerikli çeldirici belge eklenince avantaj tersine döndü — denetim katmanı, engellediği halüsinasyondan fazlasını doğru cevaplardan kesti. Ayrıntılı analiz: [ölçüm raporu](eval/results/benchmark_v1_vs_v2.md).

## Proje Yapısı

```
main.py               # CLI giriş noktası
config.py             # model alias'ları + RAG parametreleri
src/
  foundry.py          # Foundry Local SDK yardımcıları (EP kaydı, model yükleme)
  chunking.py         # başlık/paragraf saygılı belge parçalama
  similarity.py       # embedding üretimi + kosinüs benzerliği
  db.py               # SQLite şeması + float32 blob serileştirme
  ingest.py           # belge → parça → embedding → rag.db
  retrieval.py        # get_top_chunks: arama katmanı
  prompts.py          # Q&A prompt şablonu (ret kalıbı, kaynak gösterimi)
  rag.py              # v1 üretim hattı (RagSession, answer_query)
  corrective.py       # v2/v3 deneysel hat (grader, rewrite, topraklama)
  evaluate.py         # ölçüm çatısı → eval/results/
  api.py              # FastAPI: /api/ask, /api/ask/stream, /api/results
  streaming.py        # SSE olay üretici (web arayüzü canlı akışı)
web/                  # Next.js arayüzü ("Yerel Arşiv" teması)
data/                 # 12 belge: 6 kurgusal ürün dokümanı + 6 ders notu
eval/                 # eval_set.json + results/ (ölçümler, karşılaştırma raporu)
docs/                 # proje raporu + sunum taslağı
```

## Lisans ve Kaynaklar

Ders notları Vikipedi'den derlenmiştir (CC BY-SA, her dosyada atıflı). Zyntrix ürün dokümanları tamamen kurgusaldır — RAG'ın gerçekten belgelerden cevap ürettiğini kanıtlamak için yazılmıştır.
