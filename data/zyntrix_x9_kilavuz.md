# Zyntrix X9 Taşınabilir Hava Kalitesi Sensörü — Kullanım Kılavuzu

## Genel Bakış

Zyntrix X9, iç ve dış ortamlarda hava kalitesini ölçen taşınabilir bir sensör cihazıdır. Cihaz PM2.5 (ince partikül madde) ve CO2 (karbondioksit) ölçümü yapar. Ölçümler 30 saniyede bir otomatik olarak alınır ve cihazın yerel hafızasında 6 ay boyunca saklanır.

Zyntrix X9, Zyntrix Teknoloji A.Ş. tarafından 2024 yılında piyasaya sürülmüştür ve X serisinin üçüncü ürünüdür (öncekiler: X5 ve X7).

## Teknik Özellikler

- **Ölçülen değerler:** PM2.5 (0–500 µg/m³) ve CO2 (400–5000 ppm)
- **Ölçüm aralığı:** 30 saniye (Eco modunda 120 saniye)
- **Pil ömrü:** Tek şarjla 14 saat (Eco modunda 26 saat)
- **Şarj süresi:** USB-C ile 90 dakikada tam şarj
- **Ekran:** 1.9 inç renkli OLED
- **Ağırlık:** 86 gram
- **Suya dayanıklılık:** IP54 (sıçramaya dayanıklı, suya daldırılamaz)
- **Bağlantı:** Bluetooth 5.2, Zyntrix Link mobil uygulaması ile eşleşir

## Şarj ve Pil

Cihaz kutudan çıktığında pil yaklaşık %60 doludur. İlk kullanımdan önce tam şarj önerilir. Şarj için yalnızca kutudaki 15W USB-C adaptörü veya eşdeğeri kullanılmalıdır; 30W üzeri hızlı şarj adaptörleri pil ömrünü kısaltabilir.

Pil seviyesi %15'in altına düştüğünde ekranın sağ üst köşesindeki pil simgesi turuncu renkte yanıp söner. %5'in altında cihaz otomatik olarak Eco moduna geçer ve ölçüm aralığını 120 saniyeye düşürür.

## Ölçüm Modları

Zyntrix X9'da üç ölçüm modu vardır:

1. **Standart mod:** 30 saniyede bir ölçüm. Günlük kullanım için önerilir.
2. **Eco mod:** 120 saniyede bir ölçüm; pil ömrünü 26 saate uzatır.
3. **Anlık mod:** Yan tuşa çift basınca tetiklenir, 5 saniye içinde tek ölçüm alır. Havalandırma sonrası hızlı kontrol için idealdir.

Mod değiştirmek için ana ekranda yan tuşu 2 saniye basılı tutun.

## Veri Aktarımı

Ölçüm geçmişi, Zyntrix Link uygulaması üzerinden CSV formatında dışa aktarılabilir. Cihaz hafızası dolduğunda (yaklaşık 6 aylık veri) en eski kayıtlar otomatik silinir. Kalıcı arşiv için ayda bir dışa aktarma önerilir.

## Bakım ve Temizlik

Sensör ızgarasını ayda bir kez kuru ve yumuşak bir fırçayla temizleyin. Islak bez, alkol veya çözücü kullanmayın; bu maddeler PM2.5 sensörünün optik lensine kalıcı hasar verir. Cihaz -10°C ile +45°C arasında çalışacak şekilde tasarlanmıştır; bu aralık dışında ölçüm doğruluğu garanti edilmez.

## Sorun Giderme

- **Ekranda "E-03" hatası:** CO2 sensörü kalibrasyon gerektiriyor. Cihazı temiz havada 10 dakika bekletin; kalibrasyon otomatik tamamlanır.
- **Ekranda "E-07" hatası:** Sensör ızgarası tıkalı. Bakım bölümündeki temizlik adımlarını uygulayın.
- **Bluetooth eşleşmiyor:** Yan tuşa 10 saniye basılı tutarak cihazı yeniden başlatın; sorun sürerse Zyntrix Link uygulamasında "Cihazı Unut" deyip yeniden eşleştirin.
- **Pil hızlı bitiyor:** Standart mod yerine Eco modunu deneyin ve ekran parlaklığını uygulamadan %50'ye düşürün.

## Garanti

Zyntrix X9, satın alma tarihinden itibaren 2 yıl garanti kapsamındadır. Pil, 500 tam şarj döngüsüne kadar garanti kapsamındadır. Garanti işlemleri için destek@zyntrix.example adresine seri numarası ile başvurulur.
