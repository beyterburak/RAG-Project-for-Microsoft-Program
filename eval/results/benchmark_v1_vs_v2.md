# Benchmark: v1-baseline vs v2-corrective

Aynı 26 soruluk etiketli eval seti ([eval_set.json](../eval_set.json)), aynı bilgi tabanı (6 belge, 43 parça), aynı modeller (`qwen3.5-2b` + `qwen3-embedding-0.6b`). Tek fark: cevaplama hattı.

## Özet Tablo

| Metrik | v1-baseline | v2-corrective | Fark |
|---|---|---|---|
| recall@4 (kaynak düzeyi) | %100 | %100 | — |
| Top-1 kaynak isabeti | %85 | %85 | — |
| Cevap doğruluğu (20 cevaplanabilir) | %80 | **%85** | +5 |
| Ret doğruluğu (6 cevaplanamaz) | %50 | **%66.7** | +16.7 |
| **Genel doğruluk** | %73.1 | **%80.8** | **+7.7** |
| Ortalama LLM süresi | 7.0 sn | 10.3 sn | +%47 |
| Medyan toplam süre | 8.9 sn | 24.7 sn | **2.8×** |

Not: v2'de "retrieval" süresi grader LLM çağrılarını da içerir; saf vektör araması her iki hatta da <1 sn'dir.

## Hatlar

- **v1-baseline:** getir(k=4) → prompt → üret. (etiket: `v1-baseline`)
- **v2-corrective (CRAG deseni):** getir(k=8) → sıkı grader (4'erli parti; "cevabı içermeli, konu benzerliği yetmez") → ilgili yoksa sorgu yeniden yazımı (en çok 1 tekrar) → en iyi ≤4 ilgili parçayla üret → topraklama kontrolü (cevap pasajda açıkça yoksa/yanlış varlığa aitse ret). (etiket: `v2-corrective`)

## Kazanım / Kayıp Analizi (soru bazlı, veriyle doğrulanmış)

**v2'de düzelen 3 soru:**
- **#1 pil ömrü, #2 ağırlık** — v1'de bilgi-yoğun "Teknik Özellikler" parçası top-4'e giremiyor, model komşu parçalardan makul-ama-yanlış cevap üretiyordu ("30 saat", "X9 Pro 104 gram"). v2'nin geniş havuzu (k=8) parçayı yakaladı, partili grader tuttu.
- **#26 PostgreSQL sürümü** — v1'de parametrik sızıntı (uydurma "17.0.0"); v2 grader'ı hiçbir parçayı ilgili bulmayınca üretime gitmeden ret.

**v2'de güvenli hale gelen 2 soru (hâlâ "yanlış" sayılıyor ama davranış düzeldi):**
- **#4 suya dayanıklılık, #5 sıcaklık aralığı** — v1'de kendinden emin yanlış cevap ("suya dayanıklı değildir"); v2'de dürüst ret. Kök neden retrieval: ilgili parça top-8 havuzuna dahi girmiyor (embedding eşleşme sınırı). Çözüm adayı: madde-düzeyi chunking (aşağıda).

**v2'de bozulan 1 soru:**
- **#19 Bachmann/Büyük O** — doğru parça getirildi, doğru cevap üretildi, ancak topraklama kontrolü yanlış-negatif verip cevabı rete çevirdi. Guard'ın bedeli: 3+ halüsinasyonu keserken 1 doğruyu kurban etti.

**Her iki hatta da hatalı 2 sızıntı:**
- **#24 quicksort, #25 Hinton** — parça konuyu içeriyor (karmaşıklık tablosu / araştırmacı listesi) ama sorulan olguyu içermiyor; 2B doğrulayıcı bu ince ayrımı ("tablodaki O(n²) kabarcık sıralamasının, quicksort'un değil") kaçırıyor.

## Sınırlamalar ve Sonraki Adımlar

1. **Judge kapasitesi:** Grader/doğrulayıcı olarak üretici modelin kendisi (2B) kullanılıyor; ince varlık ayrımı hataları (#24, #25) ve yanlış-negatifler (#19) bundan. Daha büyük bir judge modeli (VRAM izin verdiğince) veya NLI tabanlı doğrulayıcı ile iyileşir.
2. **Madde-düzeyi chunking:** #4/#5'in kök nedeni spec listesinin tek parça olması. Liste bölümlerini madde başına parçalamak embedding eşleşmesini doğrudan güçlendirir (v3 adayı — v1/v2 karşılaştırılabilirliğini bozmamak için bu turda dondurulmuş chunking korundu).
3. **Gecikme:** Corrective döngü soru başına 3-4 LLM çağrısı ekliyor (medyan 2.8×). Grader partilerini paralelleştirmek veya yalnız düşük skorlu getirilerde devreye almak (skor eşiği) maliyeti düşürür.
4. **Oturum içi yavaşlama:** Uzun oturumlarda istek süreleri artıyor (2-6 sn → 20-30 sn); Foundry Local servis tarafında araştırılmadı.
