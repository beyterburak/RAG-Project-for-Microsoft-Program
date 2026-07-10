# Ders Notu: Yapay Sinir Ağları

## Tanım

Yapay sinir ağları (YSA), insan beyninin bilgi işleme tekniğinden esinlenerek geliştirilmiş bir bilgi işlem teknolojisidir. Biyolojik sinir sisteminin çalışması taklit edilir: sinir hücreleri (nöronlar) ve aralarındaki sinaptik bağlar dijital olarak modellenir. YSA'lar, birbiriyle bağlantılı işlem birimlerinden oluşan matematiksel ağlardır.

## Temel Bileşenler

- **Nöron (işlem birimi):** Diğer nöronlardan gelen sinyalleri alır, ağırlıklarla çarpıp toplar ve aktivasyon fonksiyonundan geçirerek çıktı üretir.
- **Ağırlıklar:** Nöronlar arası bağlantıların gücünü temsil eden, öğrenme sırasında güncellenen parametrelerdir.
- **Aktivasyon fonksiyonu:** Nöronun toplam girdisini çıktıya dönüştüren matematiksel işlemdir; yaygın örnekler sigmoid ve ReLU'dur.

## Ağ Mimarisi

Tipik bir YSA üç tür katmandan oluşur: veriyi alan **giriş katmanı**, asıl işlemi yapan bir veya daha fazla **gizli katman** ve sonucu üreten **çıktı katmanı**.

## Öğrenme: Geri Yayılım (Backpropagation)

Öğrenme, bağlantı ağırlıklarının eğitim algoritmasıyla tekrar tekrar ayarlanmasıyla gerçekleşir. Geri yayılım yönteminde ağın çıktısındaki hata hesaplanır ve bu hata ağ boyunca geriye doğru yayılarak ağırlıklar güncellenir.

## Geleneksel Bilgisayarlardan Farkı

Geleneksel işlemciler komutları sırayla işler; YSA'lar ise problemin küçük parçalarıyla ilgilenen çok sayıda bağımsız birimin paralel çalışması gibi davranır.

## Üstünlükler ve Sınırlamalar

Üstünlükleri: paralel işleme, örnek verilerden öğrenebilme, gürültülü ve eksik verilerle çalışabilme. Sınırlamaları: ağın içinde ne olduğunun anlaşılamayabilmesi (kara kutu problemi), bazı ağlar için kararlılık analizinin yapılamaması ve bir probleme kurulan ağın başka sisteme taşınmasının zorluğu.

## Önemli Araştırmacılar

- **Frank Rosenblatt:** Perceptron modeli
- **Geoffrey Hinton:** Derin öğrenme
- **Yann LeCun:** Evrişimli sinir ağları (CNN)
- **Yoshua Bengio:** Makine öğrenmesi
- **Jürgen Schmidhuber:** LSTM

## Uygulama Alanları

Görüntü tanıma, doğal dil işleme, otonom sistemler, tıbbi teşhis ve finansal tahminleme. Ayrıca YSA teknolojisine dayanan özel donanımlar (nörobilgisayarlar) geliştirilmiştir; örneğin Siemens'in Synapse 1 makinesi saniyede 3,2 milyar çarpma-toplama işlemi yapabilir.

---
*Kaynak: Vikipedi "Yapay sinir ağı" maddesinden derlenmiştir (CC BY-SA).*
