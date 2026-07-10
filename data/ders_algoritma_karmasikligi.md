# Ders Notu: Algoritma Karmaşıklığı ve Büyük O Gösterimi

## Tanım

Büyük O gösterimi, bir fonksiyonun asimptotik davranışını daha basit bir fonksiyon cinsinden üst sınır olarak ifade eden matematiksel gösterimdir. Bilgisayar bilimlerinde algoritmaların, girdi boyutu (n) büyüdükçe zaman veya bellek gereksiniminin nasıl arttığını sınıflandırmak için kullanılır.

## Tarihçe

Gösterimi ilk kez Alman sayı kuramcısı **Paul Bachmann**, 1892 tarihli *Analytische Zahlentheorie* adlı eserinde kullanmıştır. Matematikçi **Edmund Landau** gösterimi yaygınlaştırmıştır; bu nedenle "Landau sembolü" olarak da bilinir.

## Biçimsel Tanım

f(x) ∈ O(g(x)) (x → ∞) olması için, |f(x)| ≤ M·|g(x)| eşitsizliğini tüm x > x₀ değerlerinde sağlayan M ve x₀ sabitlerinin var olması gerekir ve yeterlidir.

## Yaygın Karmaşıklık Sınıfları

| Gösterim | Adı | Tipik örnek |
|----------|-----|-------------|
| O(1) | Sabit | Dizinin bir elemanına indisle erişim |
| O(log n) | Logaritmik | İkili arama (binary search) |
| O(n) | Doğrusal | Sıralanmamış dizide tarama |
| O(n log n) | Doğrusal-logaritmik | Birleştirmeli sıralama (merge sort) |
| O(n²) | Karesel | Kabarcık sıralaması (bubble sort) |
| O(2ⁿ) | Üstel | Tüm alt kümeleri üretme |
| O(n!) | Faktöriyel | Tüm permütasyonları deneme |

## İlgili Gösterimler

- **Ω (Omega):** Asimptotik alt sınır — algoritma en iyi durumda bile bundan hızlı olamaz.
- **Θ (Theta):** Sıkı sınır — üst ve alt sınırın çakıştığı durum.
- **o (küçük o):** Asimptotik olarak ihmal edilebilir büyüme.
- **Õ (Soft-O):** Logaritmik çarpanları yok sayan gösterim.

## Pratik Not

Büyük O, sabit çarpanları ve düşük dereceli terimleri yok sayar: 3n² + 5n + 20 fonksiyonu O(n²) sınıfındadır. İki algoritma aynı O sınıfında olsa bile gerçek performansları sabitler nedeniyle farklı olabilir.

---
*Kaynak: Vikipedi "Büyük O gösterimi" maddesinden derlenmiştir (CC BY-SA).*
