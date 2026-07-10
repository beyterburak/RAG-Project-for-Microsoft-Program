# Sunum Taslağı — Yerel RAG AI Asistanı (5 dakika)

## 1. Problem (30 sn)

- LLM'ler kendi belgelerinizi bilmez; bilmediklerinde de **uydurur**.
- Canlı kanıt (bu projeden): bağlamsız modele "Zyntrix X9'un pil ömrü?" → kendinden emin **"15-20 saat"** (uydurma ürün, uydurma cevap). Aynı soru RAG ile → **"14 saat (Kaynak: kilavuz)"**.
- Hedef: tamamen **çevrimdışı**, kaynak gösteren, bilmediğinde "bilmiyorum" diyen belge asistanı.

## 2. Mimari (60 sn)

```
Soru → embedding (qwen3-embedding-0.6b) → SQLite'ta kosinüs top-K
     → bağlam + sistem prompt → yerel LLM (qwen3.5-2b, Foundry Local)
     → kaynaklı cevap        [tamamı tek makinede, internetsiz]
```

- **Foundry Local:** model indirme + GPU hızlandırma (TensorRT-RTX) + OpenAI-uyumlu yerel API.
- **SQLite:** embedding'ler float32 blob; idempotent ingestion (`UNIQUE(source, chunk_index)`).
- **Bilgi tabanı:** 6 Türkçe belge (3 kurgusal ürün dokümanı — RAG kanıtlanabilirliği için, 3 ders notu), 43 parça.

## 3. İki varyant + benchmark (90 sn) — projenin iddialı kısmı

- **v1-baseline:** getir(4) → üret.
- **v2-corrective (CRAG):** getir(8) → **grader** ("parça cevabı içeriyor mu?") → gerekirse **sorgu yeniden yazımı** → üret → **topraklama kontrolü** (cevap pasajda yoksa ret).
- 26 soruluk etiketli eval seti; her iki varyant aynı setle ölçüldü:

| | v1 | v2 |
|---|---|---|
| Genel doğruluk | %73.1 | **%80.8** |
| Ret doğruluğu | %50 | %66.7 |
| Medyan süre | 8.9 sn | 24.7 sn |

- Mesaj: **doğruluk parayla değil, gecikmeyle satın alındı** — ödünleşim sayısal.

## 4. Canlı demo (90 sn)

1. `python main.py ask "Zyntrix X9'un pil ömrü standart modda kaç saattir?" --corrective` → doğru, kaynaklı cevap.
2. `python main.py ask "Zyntrix X9'un satış fiyatı ne kadar?" --corrective` → **"Bu bilgi belgelerimde yok."** (sorumlu davranış).
3. (Wi-Fi kapalıyken — çevrimdışılık vurgusu.)

## 5. Çıkarılan dersler (60 sn)

1. **Ölç, tahmin etme:** phi-3.5-mini Türkçe sentezde olguları karıştırdı; kanıta dayalı model değişikliğiyle (qwen3.5-2b) çözüldü. 4B model 8 GB VRAM'e sığmadı — donanım tavanı gerçek bir tasarım kısıtı.
2. **Chunking kaderdir:** dört yanlışın dördü de aynı kök nedene indi — bilgi-yoğun spec listesi parçası top-K'ya girmiyor. Parçaya belge başlığı eklemek retrieval'ı gözle görülür düzeltti.
3. **Guard'lar bedava değil:** topraklama kontrolü 3 halüsinasyonu kesti ama 1 doğru cevabı da kurban etti (yanlış-negatif). 2B judge'ın tavanı belgelendi; gelecek iş: daha büyük judge.
4. Süreç: her adım commit'li, her iddia eval'le doğrulanmış, iki varyant etiketli (`v1-baseline`, `v2-corrective`).
