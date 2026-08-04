# Ders Notu: İşletim Sistemleri

## Tanım

İşletim sistemi (Operating System, OS), bir bilgisayarın donanım kaynaklarını yöneten ve uygulama yazılımlarına hizmet sağlayan yazılımlar bütünüdür. Kullanıcı ile donanım arasında bir soyutlama katmanı oluşturur.

## Temel Görevleri

- **Süreç yönetimi:** Çalışan programların başlatılması, durdurulması ve işlemciye paylaştırılması.
- **Bellek yönetimi:** RAM ve depolama alanının verimli kullanılması, süreçler arasında paylaştırılması.
- **Dosya sistemi:** Verilerin düzenlenmesi, adlandırılması ve erişim denetimi.
- **Aygıt yönetimi:** Yazıcı, ekran, disk gibi donanım birimlerinin sürücüler aracılığıyla denetimi.

## Çekirdek (Kernel) Türleri

1. **Monolitik çekirdek:** Tüm çekirdek hizmetleri tek adres alanında çalışır. Unix, Linux ve Windows bu yaklaşımı kullanır.
2. **Mikro çekirdek:** Yalnızca en temel hizmetler çekirdekte tutulur, diğerleri kullanıcı alanında çalışır. QNX, BeOS ve Windows NT örnektir.
3. **Ekzo çekirdek:** Donanımı doğrudan uygulamalara açan deneysel yaklaşım; hâlâ araştırma aşamasındadır.

## Çok Görevlilik (Multitasking)

Sistemin aynı anda birden fazla görevi yürütebilmesidir. İki türü vardır: **önleyici (preemptive)** çok görevlilikte işletim sistemi süreçten denetimi zorla alabilir (Linux, Unix-Solaris); **kooperatif** çok görevlilikte süreç denetimi kendi isteğiyle bırakır (Windows 95).

## Yaygın İşletim Sistemleri

| Sistem | Başlangıç | Özellik |
|--------|-----------|---------|
| Windows | 1985 | Kişisel bilgisayarlarda yaygın |
| GNU/Linux | 1991 | Açık kaynak, ücretsiz |
| macOS | 2001 | Unix tabanlı, Apple donanımı için |
| Android / iOS | 2008 | Mobil cihazlar için |

## Tarihsel Gelişim

1940–50'lerde ilk "yönetim programları" ortaya çıktı. 1960'larda IBM OS/360 ile çoklu işlem yaygınlaştı. 1970'lerde Unix geliştirildi. 1980'lerde DOS ve Macintosh System 1 kişisel bilgisayarlara yayıldı. 1990'larda Windows 95/98 ile grafik arayüz standart hâline geldi. 2000'lerde Windows XP/7 ve Linux büyüdü; 2010'lardan itibaren mobil işletim sistemleri baskın konuma geçti.

---
*Kaynak: Vikipedi "İşletim sistemi" maddesinden derlenmiştir (CC BY-SA).*
