# Sunum Taslağı — Yerel RAG AI Asistanı (5 dakika)

> Ana mesaj: **"Karmaşıklık her zaman iyileştirmez — ölçmeden bilemezsiniz."**
> Proje hem çalışan bir sistem hem de bu sistemi dürüstçe ölçen bir deney.

---

## 1. Problem (30 sn)

- Dil modelleri sizin belgelerinizi bilmez; bilmediklerinde de **uydurur**.
- **Canlı kanıt (bu projeden):** Bağlamsız modele "Zyntrix X9'un pil ömrü?" diye sorduğumuzda kendinden emin biçimde **"15-20 saat"** dedi. Zyntrix diye bir ürün yok — belgeleri biz yazdık. Aynı soru RAG ile: **"14 saat (Kaynak: kılavuz)"**.
- Hedef: tamamen **çevrimdışı**, kaynak gösteren, bilmediğinde "bilmiyorum" diyen belge asistanı.

## 2. Mimari (45 sn)

```
Soru → embedding (qwen3-embedding-0.6b) → SQLite'ta kosinüs benzerliği → top-K parça
     → bağlam + sistem promptu → yerel LLM (qwen3.5-2b, Foundry Local)
     → kaynaklı cevap            [tamamı tek makinede, internetsiz]
```

- **Foundry Local:** model yönetimi + GPU hızlandırma (TensorRT-RTX) + OpenAI-uyumlu yerel API.
- **SQLite:** embedding'ler float32 blob; `UNIQUE(source, chunk_index)` ile idempotent ingestion.
- **Bilgi tabanı:** 12 Türkçe belge / 82 parça — 6'sı kurgusal ürün dokümanı (RAG'ın kanıtlanabilirliği için), 6'sı ders notu.
- **Arayüz:** CLI + web ("Yerel Arşiv" teması, Next.js + FastAPI).

## 3. Deney: üç varyant, aynı ölçüm (90 sn) — projenin kalbi

44 soruluk etiketli set (35 cevaplanabilir + 9 bilerek cevaplanamaz), her varyant aynı setle ölçüldü:

| | v1 (basit) | v2 (corrective) | v3 (optimize) |
|---|---|---|---|
| Genel doğruluk | **%79.5** | %77.3 | %75.0 |
| Ret doğruluğu | **%66.7** | %66.7 | %55.6 |
| Medyan süre | **8.8 sn** | 26.6 sn | 23.6 sn |

**Asıl hikâye burada:** Corrective katmanı (getir → denetle → yeniden ara → üret → kaynak kontrolü) ilk ölçümde, **43 parçalık küçük korpusta +7.7 puan kazandırmıştı.** Korpusu 82 parçaya çıkarıp bilinçli bir **çeldirici belge** (X9 Pro kılavuzu — standart modelle aynı başlıklar, farklı sayılar) ekleyince sonuç tersine döndü.

Sebep: belgeler birbirine benzedikçe denetleyici katman daha temkinli davranıyor ve **engellediği halüsinasyondan fazlasını doğru cevaplardan kesiyor.**

## 4. Canlı demo (90 sn)

Web arayüzünde (http://localhost:3000):

1. **Doğru cevap + kaynak:** "Zyntrix X9'un pil ömrü standart modda kaç saattir?" → cevap daktilo gibi akar, sağda taranan belge parçaları fiş fiş düşer.
2. **Sorumlu ret:** "Zyntrix X9'un satış fiyatı ne kadar?" → tutanağa kırmızı **"BU BİLGİ BELGELERDE YOK"** mührü basılır.
3. **Teftiş Raporu sekmesi:** üç varyantın karşılaştırma tablosu, soru bazlı denetim listesi.
4. (Wi-Fi kapalıyken çalıştır — çevrimdışılık vurgusu.)

*Yedek plan: arayüz açılmazsa `python main.py chat` ile aynı iki senaryo terminalde gösterilir.*

## 5. Çıkarılan dersler (75 sn)

1. **Ölç, varsayma.** Corrective RAG literatürde iyi bilinen bir desen ve küçük korpusta bende de kazandırdı — ama gerçekçi korpusta kaybettirdi. Ölçmeseydim "iyileştirme yaptım" diye raporlayacaktım.
2. **Test verisi kolay olursa sonuç yanıltır.** Çeldirici belgeyi bilerek eklemek, sistemin gerçek zayıflıklarını ortaya çıkardı (recall %100 → %97.1).
3. **Guard'lar bedava değil.** Halüsinasyonu kesen doğrulayıcı, doğru cevapları da kesiyor. Sıkı/gevşek ayarının ikisini de denedim; 2B model bu ayrımı yapacak kapasitede değil.
4. **Donanım gerçek bir tasarım kısıtı.** 8 GB VRAM tavanı yüzünden 4B model kullanılamadı; model seçimi bu kısıt altında ölçümle yapıldı (phi-3.5-mini Türkçe sentezde olguları karıştırıyordu).
5. **Hataların çoğu retrieval değil okuma-anlama kaynaklı** — sistemin bir sonraki adımı daha iyi bir model ya da madde-düzeyi chunking.

---

## Olası jüri soruları

- *"Corrective işe yaramadıysa neden repoda?"* → Ölçüm sonucu korpusa bağlı; hat `--corrective` bayrağıyla duruyor, farklı korpus/judge ile yeniden değerlendirilebilir. Negatif sonuç da sonuçtur.
- *"Neden bu kadar yavaş?"* → v1 medyanı 8.8 sn, basit sorularda 2-3 sn. Corrective 3-4 LLM çağrısı ekliyor. Ölçüm sırasında ara sıra 30 sn'lik sıçramalar da gözlendi (servis/GPU kaynaklı, raporda açık).
- *"Kaç belgeye kadar ölçeklenir?"* → Brute-force kosinüs; birkaç bin parçaya kadar sorunsuz, ötesinde vektör indeksi (FAISS/sqlite-vec) gerekir — raporda "gelecek işler"de.
