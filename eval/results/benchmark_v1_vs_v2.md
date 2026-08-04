# Benchmark Raporu — v1 / v2 / v3

**Sonuç:** Basit hat (v1) kazandı. Corrective katmanı küçük korpusta kazandırdı, gerçekçi korpusta kaybettirdi.

---

## 1. Özet Tablo (44 soru, 12 belge, 82 parça)

| Metrik | **v1-baseline** | v2-corrective | v3-optimize |
|---|---|---|---|
| **Genel doğruluk** | **%79.5** | %77.3 | %75.0 |
| Cevap doğruluğu (35 cevaplanabilir) | **%82.9** | %80.0 | %80.0 |
| Ret doğruluğu (9 cevaplanamaz) | **%66.7** | **%66.7** | %55.6 |
| Belge isabeti (recall@4) | **%97.1** | %94.3 | %94.3 |
| Top-1 kaynak isabeti | %82.9 | %82.9 | %82.9 |
| Ortalama LLM süresi | **11.1 sn** | 12.4 sn | 13.1 sn |
| Medyan toplam süre | **8.8 sn** | 26.6 sn | 23.6 sn |

Hatlar:
- **v1-baseline:** getir(k=4) → üret.
- **v2-corrective:** getir(k=8) → sıkı grader → gerekirse sorgu yeniden yazımı → üret → topraklama denetimi.
- **v3-optimize:** v2 + gevşetilmiş guard + koşullu denetim (top-1 benzerlik ≥ 0.70 ise grader ve topraklama atlanır).

---

## 2. Ana Bulgu: Korpus Ölçeği Sonucu Tersine Çevirdi

Aynı hatlar iki farklı korpusta ölçüldü:

| Korpus | v1 genel | v2 genel | Fark |
|---|---|---|---|
| 6 belge / 43 parça / 26 soru | %73.1 | **%80.8** | v2 **+7.7** |
| 12 belge / 82 parça / 44 soru | **%79.5** | %77.3 | v2 **−2.2** |

Küçük korpusta corrective katmanı net kazandırıyordu. Korpus iki katına çıkıp **çeldirici belge** (X9 Pro kılavuzu: standart X9 ile aynı bölüm başlıkları, farklı sayılar) eklenince avantaj tersine döndü.

**Neden:** Belgeler birbirine benzedikçe grader daha temkinli davranıyor, doğru parçaları da eliyor. Guard'ın engellediği halüsinasyon sayısı, kestiği doğru cevap sayısının altında kaldı.

Bu, sentetik küçük veri kümesinde ölçülen iyileşmelerin gerçek ölçekte doğrulanmadan kabul edilmemesi gerektiğinin somut bir örneğidir.

---

## 3. Guard Ödünleşimi (v2 → v3)

v3'te topraklama denetimi "şüphede evet" moduna alındı ve grader gevşetildi. Sonuç:

- **Kazanç (1 soru):** #19 (Bachmann/Büyük O) — doğru cevap üretiliyordu, sıkı guard iptal ediyordu; artık geçiyor.
- **Kayıp (2 soru):** #22 (renk seçenekleri) — model *"belirli bir renk paletiyle mevcuttur"* diye uydurdu, sıkı guard bunu kesiyordu; #2 (ağırlık) — X9 Pro değeri verildi.
- **Değişmeyen:** #24 (quicksort), #25 (Hinton), #26 (PostgreSQL) sızıntıları her üç varyantta da hatalı. Guard'ın ne sıkı ne gevşek hâli bunları yakalayabiliyor.

Guard sıkılığı bir ayar düğmesi: sıkarsanız halüsinasyonla birlikte doğru cevapları da kesiyor, gevşetirseniz ikisini birden geçiriyor. 2B doğrulayıcı bu ayrımı yapacak kapasitede değil.

---

## 4. Koşullu Denetim ve Eşik Seçimi

v3'te denetim yalnız düşük güvenli getirmelerde çalışır. Eşik tahminle değil ölçümle seçildi:

- 44 sorunun top-1 benzerlik skorları hesaplandı.
- Cevaplanamaz soruların en yüksek skoru: **0.6896**.
- 0.70 üstünde 13 cevaplanabilir soru var, **cevaplanamaz soru yok** → bu bölgede denetimi atlamak yapısal olarak sızıntı riski taşımıyor.

**Sonuç:** Mekanizma doğru çalıştı (13 soru denetimsiz geçti) ama medyan süre yalnız %11 düştü (26.6 → 23.6 sn). Denetimsiz geçen sorular zaten hızlı olanlardı; medyanı belirleyen orta zorluktaki sorular hâlâ 3-4 LLM çağrısından geçiyor.

---

## 5. Hata Analizi (v1 üzerinden, 9 hata)

| Kategori | Sorular | Açıklama |
|---|---|---|
| **Model/mod karıştırması** | #1, #2, #7 | Doğru parça getirildi ama X9/X9 Pro veya Standart/Eco modu karıştırıldı |
| **Parametrik sızıntı / halüsinasyon** | #23, #24, #44 | Cevap belgede yok; model ön eğitiminden verdi ya da belgedeki ifadeyi çarpıttı (#23: "2024'te piyasaya sürüldü" → "2024'te kuruldu") |
| **Retrieval kaçağı** | #4, #5 | İlgili teknik özellik parçası top-4'e giremedi |
| **Ters okuma** | #36 | Belgede "silinmez" yazıyor, model "silinir" dedi |

Hataların çoğu (#1, #2, #7, #36) **retrieval değil okuma-anlama** kaynaklı. Bu, corrective katmanının neden yardımcı olamadığını da açıklıyor: sorun getirilen bağlamda değil, o bağlamın yorumlanmasında.

---

## 6. Sonuç ve Öneri

**Üretim varyantı: v1-baseline.** Bu korpus ve bu model (qwen3.5-2b) için en doğru ve en hızlı hat. Corrective varyantlar depoda korunuyor (`--corrective` bayrağı) — farklı korpus veya daha yetenekli bir judge modeliyle yeniden değerlendirilebilir.

## 7. Sınırlamalar ve Gelecek İşler

1. **Judge kapasitesi (en yüksek etkili):** Grader ve doğrulayıcı, üretici modelin kendisiyle (2B) çalışıyor. Ayrı ve daha yetenekli bir judge modeli guard ödünleşimini kökten değiştirebilir — ancak 8 GB VRAM (RTX 3060 Ti) tavanı iki modelin aynı anda yüklü kalmasına izin vermiyor.
2. **Madde-düzeyi chunking:** #4/#5/#34'ün kök nedeni spec listelerinin tek parçada toplanması. Liste maddelerini ayrı parçalara bölmek retrieval kaçağını doğrudan azaltır.
3. **Varlık ayrımı:** X9/X9 Pro karışması için parça metadatasına ürün modeli eklenip sorgu-zamanı filtreleme yapılabilir.
4. **Gecikme sıçramaları:** Ölçüm sırasında ara sıra 30+ saniyelik istekler gözlendi (aynı girdi, aynı token sayısı; 8 istekten 7'si 1.5-4 sn, biri 32 sn). Kod kaynaklı değil; Foundry Local servisi veya GPU zamanlaması ile ilgili, araştırılmadı.
5. **Ölçüm kriteri:** Ret tespiti, modelin birebir kalıp yerine eşanlamlı ifadeler kullanabilmesi nedeniyle genişletildi ("belge" kökü + olumsuzluk). Bu düzeltme öncesi v1'in ret doğruluğu %44.4 görünüyordu, gerçekte %66.7'ydi.

---

## Ek: Önceki Korpus (6 belge / 43 parça / 26 soru)

Arşiv: [`korpus-43/`](korpus-43/). O ölçümde v1 %73.1, v2 %80.8 idi; ayrıntılı kazanç/kayıp analizi ilgili dosyalardadır. Bu tarihsel sonuç, Bölüm 2'deki ölçek bulgusunun karşılaştırma tabanıdır.
