# Ders Notu: Makine Öğrenmesi

## Tanım

Makine öğrenmesi, veriden öğrenebilen ve daha önce görmediği verilere genelleştirebilen istatistiksel algoritmaların geliştirilmesiyle ilgilenen yapay zekâ dalıdır. Sistem, açıkça programlanmış komutlar yerine veri içindeki örüntüleri keşfeder ve bu örüntüleri yeni durumlara uygular.

## Tarihçe

Terimi 1959 yılında **Arthur Samuel** ortaya atmıştır; Samuel bilgisayar oyunları ve yapay zekâ alanında öncü çalışmalar yapmıştır. 1960'larda Nilsson'un *Öğrenme Makineleri* kitabı örüntü sınıflandırmasına odaklandı; 1973'te Duda ve Hart model tanıma araştırmalarını yürüttü. 1981'de sinir ağlarının 40 karakteri tanımayı öğrendiği çalışma yayımlandı. 1980'ler ve 1990'larda alan pratik problemlere yönelerek istatistik ve olasılık teorisini benimsedi.

## Öğrenme Yaklaşımları

- **Gözetimli öğrenme:** Etiketlenmiş örneklerden öğrenir; girdileri çıktılara eşler. Sınıflandırma ve regresyon bu başlık altındadır.
- **Gözetimsiz öğrenme:** Etiketsiz veriden örüntü ve ilişki keşfeder; kümeleme tipik örnektir.
- **Pekiştirmeli öğrenme:** Çevreyle etkileşerek deneme-yanılma yoluyla en iyi davranışı öğrenir.
- **Yarı gözetimli öğrenme:** Az sayıda etiketli örneği çok sayıda etiketsiz örnekle birlikte kullanır.

## Yaygın Algoritmalar

Gözetimli: karar ağaçları, Naive Bayes, destek vektör makineleri (SVM), yapay sinir ağları. Gözetimsiz: k-ortalamalar (k-means) kümeleme, hiyerarşik kümeleme, beklenti maksimizasyonu. Boyut indirgeme: PCA, LDA, t-SNE.

## Aşırı Öğrenme (Overfitting)

Model gereğinden karmaşıksa eğitim verisine aşırı uyum sağlar; eğitimde çok başarılı görünürken yeni verilerde başarısız olur. İdeal model karmaşıklığı, verinin altında yatan gerçek fonksiyonun karmaşıklığıyla eşleşmelidir.

## Eğitim ve Test Ayrımı

Modelin görmediği örneklerdeki başarısını ölçebilmek için veri, eğitim (model geliştirme) ve test (değerlendirme) kümelerine ayrılır. Test kümesi model geliştirme sırasında kullanılmaz.

## Uygulama Alanları

Bilgisayarlı görme ve nesne tanıma, doğal dil işleme, konuşma ve el yazısı tanıma, tıbbi tanı, kredi kartı dolandırıcılığı tespiti, arama motorları ve tavsiye sistemleri, DNA dizi sınıflandırması.

---
*Kaynak: Vikipedi "Makine öğrenimi" maddesinden derlenmiştir (CC BY-SA).*
