# Eval Sonuçları — v1-baseline

Tarih: 2026-07-10 · Model: qwen3.5-2b · Embedding: qwen3-embedding-0.6b · top-K: 4

## Özet

| Metrik | Değer |
|---|---|
| recall@4 (cevaplanabilir) | 100% |
| top-1 kaynak isabeti | 85% |
| Cevap doğruluğu (cevaplanabilir) | 80% |
| Ret doğruluğu (cevaplanamaz) | 50% |
| Genel doğruluk | 73% |
| Ortalama LLM süresi | 7.02 sn |
| Medyan toplam süre | 8.92 sn |

## Soru bazında

| # | Tip | Soru | Doğru? | Recall | Süre (sn) |
|---|---|---|---|---|---|
| 1 | answer | Zyntrix X9'un pil ömrü standart modda kaç saattir? | ✗ | ✓ | 5.4 |
| 2 | answer | Zyntrix X9 kaç gram ağırlığında? | ✗ | ✓ | 1.8 |
| 3 | answer | Ekranda E-07 hatası görürsem ne yapmalıyım? | ✓ | ✓ | 2.4 |
| 4 | answer | Zyntrix X9 suya dayanıklı mı? | ✗ | ✓ | 1.6 |
| 5 | answer | Zyntrix X9 hangi sıcaklık aralığında çalışır? | ✗ | ✓ | 2.2 |
| 6 | answer | Zyntrix X9'un garanti süresi ne kadar? | ✓ | ✓ | 1.8 |
| 7 | answer | Zyntrix X9 USB-C ile kaç dakikada tam şarj olur? | ✓ | ✓ | 4.7 |
| 8 | answer | X9 ile X9 Pro arasındaki farklar nelerdir? | ✓ | ✓ | 2.3 |
| 9 | answer | Zyntrix Link uygulamasına en fazla kaç cihaz bağlanır? | ✓ | ✓ | 1.5 |
| 10 | answer | CO2 kaç ppm üzerinde havalandırma yapılmalı? | ✓ | ✓ | 1.7 |
| 11 | answer | Zyntrix X9 verilerimi USB ile bilgisayara aktarabilir miyim? | ✓ | ✓ | 2.1 |
| 12 | answer | Firmware 2.1 sürümünde hangi yenilikler geldi? | ✓ | ✓ | 5.4 |
| 13 | answer | Sürüm 2.3 ile Eco modda pil ömrü kaç saate çıktı? | ✓ | ✓ | 10.8 |
| 14 | answer | Firmware güncellemesi için pil en az yüzde kaç dolu olmalı? | ✓ | ✓ | 9.1 |
| 15 | answer | Perceptron modelini kim geliştirdi? | ✓ | ✓ | 9.5 |
| 16 | answer | Backpropagation yönteminde ağırlıklar nasıl güncellenir? | ✓ | ✓ | 9.1 |
| 17 | answer | İlişkisel veri modelini kim, ne zaman geliştirdi? | ✓ | ✓ | 8.7 |
| 18 | answer | NoSQL veritabanlarına hangi örnekler verilebilir? | ✓ | ✓ | 9.8 |
| 19 | answer | Büyük O gösterimini ilk kim, hangi eserde kullandı? | ✓ | ✓ | 10.7 |
| 20 | answer | Birleştirmeli sıralamanın (merge sort) karmaşıklığı nedir? | ✓ | ✓ | 12.1 |
| 21 | unansw | Zyntrix X9'un satış fiyatı ne kadar? | ✓ | - | 9.8 |
| 22 | unansw | Zyntrix X9 hangi renk seçenekleriyle satılıyor? | ✓ | - | 10.2 |
| 23 | unansw | Zyntrix Teknoloji A.Ş. hangi yıl kuruldu? | ✓ | - | 13.5 |
| 24 | unansw | Quicksort algoritmasının en kötü durum karmaşıklığı nedir? | ✗ | - | 14.6 |
| 25 | unansw | Geoffrey Hinton hangi üniversitede çalışıyor? | ✗ | - | 10.9 |
| 26 | unansw | PostgreSQL'in en son sürümü hangisi? | ✗ | - | 11.5 |

## Başarısız vakalar (hata analizi girdisi)

- **#1** Zyntrix X9'un pil ömrü standart modda kaç saattir?
  - cevap: Standart modda pil ömrü 30 saattir.
(Kaynak: dosya.md)
  - getirilen: zyntrix_x9_kilavuz.md/3, zyntrix_x9_kilavuz.md/7, zyntrix_sss.md/4, zyntrix_surum_notlari.md/3
- **#2** Zyntrix X9 kaç gram ağırlığında?
  - cevap: X9 Pro'nun ağırlığı 104 gramdır.
(Kaynak: dosya.md)
  - getirilen: zyntrix_sss.md/1, zyntrix_sss.md/0, zyntrix_x9_kilavuz.md/0, zyntrix_x9_kilavuz.md/7
- **#4** Zyntrix X9 suya dayanıklı mı?
  - cevap: Zyntrix X9 cihazı suya dayanıklı değildir.
  - getirilen: zyntrix_x9_kilavuz.md/7, zyntrix_sss.md/2, zyntrix_surum_notlari.md/3, zyntrix_surum_notlari.md/4
- **#5** Zyntrix X9 hangi sıcaklık aralığında çalışır?
  - cevap: Zyntrix X9 cihazında sıcaklık sensörü bulunmamaktadır; bu nedenle cihaz sıcaklık değerlerini ölçmez. Sıcaklık ölçümü cihazın üst model olan X9 Pro'da bulunan sensör sayesinde yapılır.
(Kaynak: zyntrix
  - getirilen: zyntrix_x9_kilavuz.md/3, zyntrix_sss.md/0, zyntrix_sss.md/2, zyntrix_x9_kilavuz.md/7
- **#24** Quicksort algoritmasının en kötü durum karmaşıklığı nedir?
  - cevap: Quicksort algoritmasının en kötü durum karmaşıklığı O(n²)'dir.
(Kaynak: ders_algoritma_karmasikligi.md)
  - getirilen: ders_algoritma_karmasikligi.md/3, ders_algoritma_karmasikligi.md/4, ders_algoritma_karmasikligi.md/0, ders_algoritma_karmasikligi.md/5
- **#25** Geoffrey Hinton hangi üniversitede çalışıyor?
  - cevap: Geoffrey Hinton, Cambridge Üniversitesi'nde çalışmaktadır.
(Kaynak: ders_aynir_aglari.md)
  - getirilen: ders_yapay_sinir_aglari.md/6, ders_yapay_sinir_aglari.md/3, ders_yapay_sinir_aglari.md/4, ders_yapay_sinir_aglari.md/0
- **#26** PostgreSQL'in en son sürümü hangisi?
  - cevap: PostgreSQL'in en son sürümü 17.0.0'dir.
  - getirilen: zyntrix_surum_notlari.md/0, ders_veritabanlari.md/4, ders_veritabanlari.md/2, ders_veritabanlari.md/1