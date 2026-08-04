# Proje Raporu — Yerel RAG AI Asistanı

**Microsoft Türkiye CSU Yaz Programı 2026** · Foundry Local ile çevrimdışı belge soru-cevap sistemi

---

## 1. Özet

Bu proje, kullanıcının kendi belgelerinden soru cevaplayan, **internet bağlantısı olmadan tek bir bilgisayarda çalışan** bir yapay zekâ asistanıdır. Sistem cevaplarını yalnızca yerel belge arşivine dayandırır, kullandığı kaynağı belirtir ve cevap arşivde yoksa uydurmak yerine "Bu bilgi belgelerimde yok" der.

Çalışan sistemin yanında, projenin ikinci yarısı bir **deneye** ayrılmıştır: literatürde bilinen "corrective RAG" deseni uygulanmış, kendi ölçüm çatımızla değerlendirilmiş ve **bu koşullarda fayda getirmediği ölçülerek gösterilmiştir**. Raporun en özgün katkısı bu negatif sonucun nedeniyle birlikte belgelenmesidir.

**Sayılarla sistem:** 12 belge · 82 parça · 44 soruluk etiketli değerlendirme seti · %79.5 genel doğruluk · 8.8 saniye medyan yanıt süresi · sıfır ağ trafiği.

---

## 2. Problem ve Hedef

Büyük dil modelleri kendi eğitim verilerinde olmayan bilgileri bilmez; ancak bilmediklerini söylemek yerine **inandırıcı biçimde uydururlar**. Bu, kurum içi dokümanlar, ders notları veya ürün kılavuzları üzerinde çalışan bir asistan için kabul edilemez.

Projede bu sorunu üç şartla çözmek hedeflendi:

1. **Kaynağa bağlılık:** Cevap yalnızca verilen belgelerden üretilecek, kaynak dosya adı belirtilecek.
2. **Dürüstlük:** Bilgi belgelerde yoksa cevap uydurulmayacak.
3. **Çevrimdışılık:** Tüm işlem tek cihazda, ağ bağlantısı olmadan gerçekleşecek (veri gizliliği ve bağımsızlık).

Çözüm yaklaşımı **RAG (Retrieval-Augmented Generation)**: soruyu doğrudan modele sormak yerine, önce belge arşivinden ilgili bölümleri bul, sonra bu bölümleri modele bağlam olarak ver, cevabı bu bağlamdan üret.

---

## 3. Sistem Nasıl Çalışır

### 3.1 Hazırlık aşaması (bir kez çalıştırılır)

```
data/*.md → parçalama → embedding üretimi → SQLite (rag.db)
```

1. **Parçalama (chunking):** Belgeler başlık ve paragraf sınırlarına saygılı biçimde ~800 karakterlik parçalara bölünür. Her parçanın başına ait olduğu **"Belge Başlığı — Bölüm"** satırı eklenir; bu olmadan bölüm parçaları hangi ürüne ait olduklarını kaybediyordu.
2. **Embedding:** Her parça `qwen3-embedding-0.6b` ile 1024 boyutlu bir vektöre çevrilir (16'lık partiler hâlinde).
3. **Depolama:** Parça metni, kaynak dosya adı, sıra numarası ve vektör SQLite'a yazılır.

### 3.2 Soru-cevap aşaması

```
Soru → embedding → 82 vektörle kosinüs benzerliği → en yakın 4 parça
     → sistem promptu + bağlam → LLM (qwen3.5-2b) → kaynaklı cevap
```

Sistem promptu modele üç kural verir: yalnız verilen bağlamı kullan, bağlamda yoksa tam olarak "Bu bilgi belgelerimde yok" de, cevabın sonunda kaynak dosya adını belirt.

**Maliyet:** soru başına 1 embedding + 1 LLM çağrısı.

### 3.3 Arayüzler

- **CLI:** `python main.py chat` — resmi program planının önerdiği (Option A) yol.
- **Web:** Next.js + FastAPI. Model sunucuda bir kez yüklenip sıcak tutulur (CLI'daki 30-60 saniyelik model yükleme beklemesi ortadan kalkar). Cevap kelime kelime akar; sağ panelde hangi belge parçalarının kullanıldığı benzerlik skorlarıyla görünür.

---

## 4. Bilgi Tabanı

12 Türkçe belge, iki kasıtlı gruba ayrılmıştır:

**Kurgusal ürün dokümanları (6 belge)** — "Zyntrix X9" adlı var olmayan bir hava kalitesi sensörünün kılavuzu, SSS'i, sürüm notları, X9 Pro kılavuzu, garanti şartnamesi ve kurulum kılavuzu.

*Neden kurgusal?* Model bu ürünü ön eğitiminden **bilemez**. Dolayısıyla doğru cevap verdiğinde bunu kesinlikle belgelerden almıştır — RAG'ın çalıştığının kanıtı. Gerçek bir konuda (örneğin Python) doğru cevap, modelin ezberinden de gelebilirdi.

**Ders notları (6 belge)** — yapay sinir ağları, veritabanları, algoritma karmaşıklığı, makine öğrenmesi, SQL, işletim sistemleri (Vikipedi'den derlenmiş, CC BY-SA atıflı).

**Bilinçli tuzak:** X9 Pro kılavuzu, standart X9 kılavuzuyla **aynı bölüm başlıklarına ama farklı sayılara** sahiptir (21 saat pil / 104 gram / IP67, standart modelde 14 saat / 86 gram / IP54). Bu, sistemin birbirine çok benzeyen iki belgeyi ayırt edip edemediğini test eder. Bölüm 7'de görüleceği gibi en öğretici hatalar buradan çıkmıştır.

Ayrıca hiçbir belgeye **fiyat, renk seçeneği veya şirket kuruluş yılı** bilgisi konmamıştır; bunlar değerlendirme setindeki "cevaplanamaz" soruların dayanağıdır.

---

## 5. Tasarım Kararları

Her karar deneyle veya ölçümle alınmıştır.

| Karar | Gerekçe |
|---|---|
| **Sohbet modeli: `qwen3.5-2b`** | İlk tercih `phi-3.5-mini` idi; Türkçe çok parçalı sentezde olguları karıştırdığı gözlendi ("pil ömrü %60 doludur" gibi). `qwen3.5-4b` denendi ancak **8 GB VRAM'e (RTX 3060 Ti) embedding modeliyle birlikte sığmadı** ve zaman aşımına düştü. 2B model doğru Türkçe üretti ve VRAM'e sığdı. |
| **Prompt dili: İngilizce yönerge, Türkçe cevap** | Türkçe sistem promptunda model biçim kurallarına (kaynak etiketi, ret kalıbı) uymuyordu. İngilizce yönerge + *"soruyla aynı dilde cevapla"* kuralı hem biçim disiplinini hem Türkçe cevabı sağladı. |
| **Model yükleme sırası: önce embedding, sonra sohbet** | Ters sırada TensorRT çıkarım anında ~2.4 GB istiyor ve GPU bellek taşması veriyordu. |
| **Embedding depolama: float32 blob** | JSON'a göre ~3 kat küçük ve kayıpsız; test, veritabanı gidiş-dönüşünde benzerlik skorlarının bit düzeyinde aynı kaldığını doğruladı. |
| **`UNIQUE(source, chunk_index)` + kaynak bazlı silme** | Aynı belge yeniden işlendiğinde kopya oluşmaz, belge küçüldüğünde bayat parça kalmaz — ingestion tekrar çalıştırılabilir. |
| **Parça başına belge başlığı** | Denetimde fark edildi: bölüm parçaları ürün adını içermiyordu, "Zyntrix'in pili" sorgusunda eşleşme zayıflıyordu. Başlık eklendikten sonra kılavuzun 8 parçasının 8'i de ürün adını taşıyor. |
| **Arayüz: CLI + web** | Resmi plan CLI'yı öneriyor (Option A), web arayüzünü ileri hedef olarak işaretliyor (Option C). İkisi de yapıldı; CLI sunum için yedek yoldur. |

---

## 6. Değerlendirme Yöntemi

### 6.1 Test seti

44 soru elle etiketlendi:

- **35 cevaplanabilir soru** — her biri için beklenen kaynak belge ve cevapta geçmesi gereken anahtar kelimeler tanımlandı (örn. #1 → `zyntrix_x9_kilavuz.md`, "14").
- **9 cevaplanamaz soru** — cevabı hiçbir belgede bulunmayan sorular (fiyat, renk, kuruluş yılı, PostgreSQL sürümü…). Doğru davranış bunlarda **ret** vermektir.

Set, 12 belgenin tamamını kapsar ve X9/X9 Pro karıştırma tuzaklarını içerir.

### 6.2 Ölçülen metrikler

| Metrik | Tanımı |
|---|---|
| **recall@4** | Beklenen kaynak belge, getirilen 4 parça arasında mı? |
| **Top-1 isabeti** | En yüksek skorlu parça doğru belgeden mi? |
| **Cevap doğruluğu** | Cevaplanabilir sorularda: ret verilmemiş **ve** anahtar kelime cevapta geçiyor. |
| **Ret doğruluğu** | Cevaplanamaz sorularda: sistem gerçekten reddetmiş. |
| **Gecikme** | Arama ve üretim süreleri ayrı; medyan ve ortalama. |

### 6.3 Ölçüm kriterinde yapılan düzeltme

İlk ölçümde ret tespiti yalnızca birebir *"Bu bilgi belgelerimde yok."* kalıbını arıyordu. Ancak model bazen *"Bu bilgi belgelerinde belirtilmemiş"* gibi eşanlamlı ifadeler kullanıyordu ve bunlar **haksız yere hatalı** sayılıyordu.

Kriter, cevapta **"belge" kökü + olumsuzluk** aranacak şekilde genişletildi. Yalnız olumsuzluk aramak yanlış olurdu: *"sıcaklık sensörü bulunmamaktadır"* gibi **hatalı** bir cevap da ret sayılırdı. Düzeltmeden sonra v1'in ret doğruluğu %44.4'ten gerçek değeri olan %66.7'ye çıktı.

---

## 7. Sonuçlar

### 7.1 Üç varyantın karşılaştırması (44 soru, 82 parça)

| Metrik | **v1 (üretim)** | v2 (corrective) | v3 (optimize) |
|---|---|---|---|
| Genel doğruluk | **%79.5** | %77.3 | %75.0 |
| Cevap doğruluğu | **%82.9** | %80.0 | %80.0 |
| Ret doğruluğu | **%66.7** | **%66.7** | %55.6 |
| recall@4 | **%97.1** | %94.3 | %94.3 |
| Medyan süre | **8.8 sn** | 26.6 sn | 23.6 sn |

**v2 (corrective)** her soruda ek denetimler yapar: 8 parça getirir, her parçayı modele "bu cevabı içeriyor mu?" diye sorar (grader), hiçbiri geçmezse soruyu yeniden yazıp tekrar arar, cevabı ürettikten sonra "bu cevap gerçekten pasajlarda var mı?" diye bir kez daha denetler. Maliyeti soru başına 4-7 LLM çağrısıdır.

**v3**, v2'nin hızlandırılmış hâlidir: arama sonucu yeterince güçlüyse (benzerlik ≥ 0.70) tüm denetimler atlanır.

### 7.2 Ana bulgu: korpus ölçeği sonucu tersine çevirdi

Aynı hatlar iki farklı büyüklükte arşivde ölçüldü:

| Arşiv | v1 | v2 | Sonuç |
|---|---|---|---|
| 6 belge / 43 parça / 26 soru | %73.1 | **%80.8** | v2 **+7.7 puan** |
| 12 belge / 82 parça / 44 soru | **%79.5** | %77.3 | v2 **−2.2 puan** |

Küçük arşivde corrective katmanı açık ara kazandırıyordu. Arşiv büyüyüp **çeldirici belge** eklenince avantaj tersine döndü.

**Neden:** Belgeler birbirine benzedikçe grader daha temkinli davranıyor ve doğru parçaları da eliyor. Teşhis çalışmasında "aşırı ret" vakalarının **dörtte üçünde** grader doğru parçayı geçirmiş, model doğru cevabı üretmiş, ancak son topraklama denetimi cevabı iptal etmişti. Denetim katmanının engellediği halüsinasyon sayısı, kestiği doğru cevap sayısının altında kaldı.

### 7.3 v3'te denenen iyileştirmeler

Guard'lar gevşetildi ve denetim koşullu hâle getirildi. Eşik tahminle değil ölçümle seçildi: 44 sorunun benzerlik skorları çıkarıldığında cevaplanamaz soruların en yükseği **0.6896** çıktı; 0.70 üstünde 13 cevaplanabilir soru var ve **hiç cevaplanamaz soru yok**, yani o bölgede denetimi atlamak yapısal olarak risksiz.

Mekanizma çalıştı (13 soru denetimsiz geçti) ama sonuç net kazanç vermedi: gevşeyen guard bir doğru cevabı kurtarırken (#19) iki halüsinasyonu serbest bıraktı (#22, #2), medyan süre yalnız %11 düştü.

---

## 8. Hata Analizi

v1'in 9 hatası dört kategoriye ayrılıyor:

| Kategori | Sorular | Örnek |
|---|---|---|
| **Model/mod karıştırması** | #1, #2, #7 | "X9'un pil ömrü?" → *26 saat* (bu X9'un **Eco modu** değeri); "X9 kaç gram?" → *X9 Pro 104 gram* |
| **Parametrik sızıntı** | #23, #24, #44 | "Zyntrix ne zaman kuruldu?" → kılavuzdaki "2024'te piyasaya sürüldü" ifadesini kuruluş yılı sandı |
| **Retrieval kaçağı** | #4, #5 | Teknik özellik parçası ilk 4'e giremedi (IP54, çalışma sıcaklığı) |
| **Ters okuma** | #36 | Belgede "ölçüm geçmişi **silinmez**" yazıyor, model "silinir" dedi |

**Kritik gözlem:** Hataların çoğu (#1, #2, #7, #36) **arama hatası değil, okuma-anlama hatasıdır** — doğru parça getirilmiş, model yanlış yorumlamıştır. Bu, corrective katmanının neden yardımcı olamadığını da açıklar: sorun getirilen bağlamda değil, o bağlamın yorumlanmasındadır. Çözüm daha iyi arama değil, daha yetenekli bir modeldir.

---

## 9. Sınırlamalar

1. **Model kapasitesi (temel kısıt).** 2B parametreli model, birbirine benzeyen iki ürünü ayırt etmekte ve olumsuz cümleleri doğru okumakta zorlanıyor. 8 GB VRAM tavanı daha büyük modele geçişi engelliyor.
2. **Judge kapasitesi.** Grader ve doğrulayıcı, üretici modelin kendisiyle çalışıyor. Ayrı ve daha yetenekli bir judge, corrective sonuçlarını değiştirebilir.
3. **Ölçek.** Brute-force kosinüs araması birkaç bin parçaya kadar uygundur; ötesinde vektör indeksi (FAISS, sqlite-vec) gerekir.
4. **Gecikme sıçramaları.** Ölçüm sırasında ara sıra 30 saniyeyi aşan istekler gözlendi (aynı girdi, aynı çıktı uzunluğu; 8 istekten 7'si 1.5-4 sn, biri 32 sn). Kod kaynaklı değil; Foundry Local servisi veya GPU zamanlaması ile ilgili, araştırılmadı.
5. **Tek dil.** Sistem Türkçe belge ve sorular için ayarlandı; çok dilli kullanım test edilmedi.
6. **Tek platform.** Windows üzerinde geliştirildi ve test edildi; kod cross-platform hazırdır ancak macOS'ta çalıştırılmadı.

---

## 10. Öğrenilenler

1. **Ölçmeden iyileştirme iddiasında bulunulamaz.** Corrective RAG'ı küçük veriyle test etseydim "+7.7 puan iyileştirme yaptım" diye raporlayacaktım. Gerçekçi veride sonuç tersine döndü.
2. **Kolay test verisi yanıltır.** İlk arşivde recall %100'dü — sistem mükemmel görünüyordu. Çeldirici belge eklenince gerçek zayıflıklar ortaya çıktı.
3. **Guard'lar bedava değildir.** Halüsinasyonu engelleyen her denetim, doğru cevapları da kesme riski taşır. Bu bir ayar düğmesidir ve model kapasitesi yetmiyorsa iki uçta da kaybedersiniz.
4. **Donanım bir tasarım kısıtıdır.** VRAM sınırı, model seçiminden mimariye kadar her kararı etkiledi.
5. **Kurgusal test verisi güçlü bir doğrulama aracıdır.** Var olmayan bir ürün hakkında doğru cevap, sistemin gerçekten belgeleri okuduğunun tartışmasız kanıtıdır.

---

## 11. Gelecek İşler

1. **Daha yetenekli judge modeli** (en yüksek etkili) — corrective ödünleşimini kökten değiştirebilir; VRAM için sıralı yükleme gerekir.
2. **Madde-düzeyi parçalama** — teknik özellik listelerini madde başına bölmek, #4/#5 tipi retrieval kaçaklarını doğrudan azaltır.
3. **Ürün metadatası ile filtreleme** — parçalara ürün modeli etiketi ekleyip sorgu zamanında filtrelemek X9/X9 Pro karışmasını çözebilir.
4. **Vektör indeksi** — arşiv birkaç bin parçayı aştığında.
5. **Gecikme sıçramalarının teşhisi** — Foundry Local servis tarafında.

---

## 12. Çalıştırma Talimatları

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py ingest      # belgeleri işle (bir kez)
python main.py chat        # soru-cevap
```

Web arayüzü için: `python main.py serve` (API) + `npm --prefix web run dev` (arayüz) → http://localhost:3000

Ölçümü tekrarlamak için: `python main.py eval` — sonuçlar `eval/results/` altına yazılır.

---

*Ayrıntılı ölçüm verileri ve soru bazlı analiz: [eval/results/benchmark_v1_vs_v2.md](../eval/results/benchmark_v1_vs_v2.md)*
