# Eval Sonuçları — v2-corrective

Tarih: 2026-07-10 · Model: qwen3.5-2b · Embedding: qwen3-embedding-0.6b · top-K: 4

## Özet

| Metrik | Değer |
|---|---|
| recall@4 (cevaplanabilir) | 100% |
| top-1 kaynak isabeti | 85% |
| Cevap doğruluğu (cevaplanabilir) | 85% |
| Ret doğruluğu (cevaplanamaz) | 67% |
| Genel doğruluk | 81% |
| Ortalama LLM süresi | 10.28 sn |
| Medyan toplam süre | 24.72 sn |

## Soru bazında

| # | Tip | Soru | Doğru? | Recall | Süre (sn) |
|---|---|---|---|---|---|
| 1 | answer | Zyntrix X9'un pil ömrü standart modda kaç saattir? | ✓ | ✓ | 7.8 |
| 2 | answer | Zyntrix X9 kaç gram ağırlığında? | ✓ | ✓ | 5.1 |
| 3 | answer | Ekranda E-07 hatası görürsem ne yapmalıyım? | ✓ | ✓ | 4.5 |
| 4 | answer | Zyntrix X9 suya dayanıklı mı? | ✗ | ✓ | 4.7 |
| 5 | answer | Zyntrix X9 hangi sıcaklık aralığında çalışır? | ✗ | ✓ | 9.7 |
| 6 | answer | Zyntrix X9'un garanti süresi ne kadar? | ✓ | ✓ | 33.8 |
| 7 | answer | Zyntrix X9 USB-C ile kaç dakikada tam şarj olur? | ✓ | ✓ | 33.2 |
| 8 | answer | X9 ile X9 Pro arasındaki farklar nelerdir? | ✓ | ✓ | 31.9 |
| 9 | answer | Zyntrix Link uygulamasına en fazla kaç cihaz bağlanır? | ✓ | ✓ | 22.5 |
| 10 | answer | CO2 kaç ppm üzerinde havalandırma yapılmalı? | ✓ | ✓ | 23.7 |
| 11 | answer | Zyntrix X9 verilerimi USB ile bilgisayara aktarabilir miyim? | ✓ | ✓ | 27.2 |
| 12 | answer | Firmware 2.1 sürümünde hangi yenilikler geldi? | ✓ | ✓ | 30.4 |
| 13 | answer | Sürüm 2.3 ile Eco modda pil ömrü kaç saate çıktı? | ✓ | ✓ | 32.5 |
| 14 | answer | Firmware güncellemesi için pil en az yüzde kaç dolu olmalı? | ✓ | ✓ | 28.0 |
| 15 | answer | Perceptron modelini kim geliştirdi? | ✓ | ✓ | 24.9 |
| 16 | answer | Backpropagation yönteminde ağırlıklar nasıl güncellenir? | ✓ | ✓ | 26.1 |
| 17 | answer | İlişkisel veri modelini kim, ne zaman geliştirdi? | ✓ | ✓ | 22.2 |
| 18 | answer | NoSQL veritabanlarına hangi örnekler verilebilir? | ✓ | ✓ | 25.6 |
| 19 | answer | Büyük O gösterimini ilk kim, hangi eserde kullandı? | ✗ | ✓ | 20.9 |
| 20 | answer | Birleştirmeli sıralamanın (merge sort) karmaşıklığı nedir? | ✓ | ✓ | 30.8 |
| 21 | unansw | Zyntrix X9'un satış fiyatı ne kadar? | ✓ | - | 20.7 |
| 22 | unansw | Zyntrix X9 hangi renk seçenekleriyle satılıyor? | ✓ | - | 21.7 |
| 23 | unansw | Zyntrix Teknoloji A.Ş. hangi yıl kuruldu? | ✓ | - | 24.6 |
| 24 | unansw | Quicksort algoritmasının en kötü durum karmaşıklığı nedir? | ✗ | - | 25.7 |
| 25 | unansw | Geoffrey Hinton hangi üniversitede çalışıyor? | ✗ | - | 26.5 |
| 26 | unansw | PostgreSQL'in en son sürümü hangisi? | ✓ | - | 19.3 |

## Başarısız vakalar (hata analizi girdisi)

- **#4** Zyntrix X9 suya dayanıklı mı?
  - cevap: Bu bilgi belgelerimde yok.
  - getirilen: zyntrix_x9_kilavuz.md/7, zyntrix_x9_kilavuz.md/0, zyntrix_x9_kilavuz.md/3, zyntrix_sss.md/1
- **#5** Zyntrix X9 hangi sıcaklık aralığında çalışır?
  - cevap: Bu bilgi belgelerimde yok.
  - getirilen: zyntrix_x9_kilavuz.md/3, zyntrix_x9_kilavuz.md/0
- **#19** Büyük O gösterimini ilk kim, hangi eserde kullandı?
  - cevap: Bu bilgi belgelerimde yok.
  - getirilen: ders_algoritma_karmasikligi.md/1, ders_algoritma_karmasikligi.md/3
- **#24** Quicksort algoritmasının en kötü durum karmaşıklığı nedir?
  - cevap: Quicksort algoritmasının en kötü durum karmaşıklığı $O(n^2)$'dir.
(Kaynak: ders_algoritma_karmasikligi.md)
  - getirilen: ders_algoritma_karmasikligi.md/3, ders_algoritma_karmasikligi.md/2
- **#25** Geoffrey Hinton hangi üniversitede çalışıyor?
  - cevap: Geoffrey Hinton, Cambridge Üniversitesi'nde çalışmaktadır.
(Kaynak: ders_aynir_aglari.md)
  - getirilen: ders_yapay_sinir_aglari.md/6, ders_yapay_sinir_aglari.md/3, ders_yapay_sinir_aglari.md/4, ders_yapay_sinir_aglari.md/0