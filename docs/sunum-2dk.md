# 2 Dakikalık Sunum — Konuşma Metni ve Akış

> Toplam ~300 kelime. Rahat tempoda 2 dakika. Köşeli parantezler ekranda ne olduğunu gösterir.

---

### 0:00 – 0:15 · Problem

*[Ekran: Danışma Masası, boş ekran]*

> "Dil modelleri bizim belgelerimizi bilmez — ama bilmediklerini söylemek yerine **uydururlar.**
> Ben de tamamen çevrimdışı çalışan, cevabını yalnızca kendi belgelerimden veren, kaynağını gösteren ve bilmediğinde bunu dürüstçe söyleyen bir asistan yaptım."

### 0:15 – 0:35 · Sistem

*[Ekran: Arşiv Kataloğu sekmesine geç]*

> "Arşivde 12 Türkçe belge var, 82 parçaya bölünmüş durumda. Soru geldiğinde parçalar anlamsal olarak aranıyor, en ilgili dördü yerel dil modeline bağlam olarak veriliyor.
> Modeli Microsoft Foundry Local çalıştırıyor — **her şey bu bilgisayarda, internet bağlantısı olmadan.**"

### 0:35 – 1:20 · Demo (iki senaryo)

*[Danışma Masası'na dön, birinci hazır fişe tıkla]*

> "Bir soru soralım: Zyntrix X9'un garanti süresi."

*[Cevap akarken sağ paneli göster]*

> "Cevap yazılırken sağda hangi belge parçalarının kullanıldığını, benzerlik skorlarıyla birlikte görüyoruz. Kaynağı da cevabın sonunda belirtiyor.
> Bu ürün **gerçek değil** — kılavuzu ben yazdım. Yani model bu cevabı ezberinden veremez, kesinlikle belgeden okumuş."

*[İkinci fişe tıkla: satış fiyatı]*

> "Şimdi belgelerde bilerek yer vermediğim bir şey soralım: fiyat."

*[Ret mührü basılınca]*

> "Uydurmuyor — 'Bu bilgi belgelerimde yok' diyor. Sorumlu davranış tam olarak bu."

### 1:20 – 1:45 · Ölçüm

*[Teftiş Raporu sekmesine geç]*

> "Sistemi 44 soruluk etiketli bir setle ölçtüm: genel doğruluk **%79.5**, medyan yanıt süresi **8.8 saniye**.
> Üstüne literatürdeki 'corrective RAG' desenini de uyguladım — cevabı üretmeden önce getirilen parçaları denetleyen bir katman. Küçük arşivde **7 puan kazandırmıştı**; arşivi büyütüp birbirine benzeyen belgeler ekleyince **avantajı tersine döndü.**"

### 1:45 – 2:00 · Kapanış

> "Çünkü denetim katmanı, engellediği halüsinasyondan fazlasını doğru cevaplardan kesiyordu.
> Benim için asıl ders bu oldu: **karmaşıklık her zaman iyileştirmez — ölçmeden bilemezsiniz.** Ölçmeseydim iyileştirme yaptığımı sanıyor olacaktım.
> Kod, ölçüm verileri ve rapor GitHub'da. Teşekkürler."

---

## Demo öncesi kontrol listesi

1. `python main.py serve` çalışıyor mu? (model ısınmış olmalı — sunumdan 2 dk önce başlat)
2. `npm --prefix web run dev` açık mı? → http://localhost:3000
3. Bir kez deneme sorusu sor (ilk istek her zaman daha yavaş, o yavaşlık sunuma denk gelmesin).
4. Tema: projeksiyonda **koyu tema** (Gece Nöbeti) genelde daha okunaklı.
5. **Yedek plan:** arayüz açılmazsa `python main.py chat` ile aynı iki soruyu terminalde sor.

## Zaman sıkışırsa ilk kesilecekler

- Arşiv Kataloğu sekmesi (0:15-0:35 kısaltılıp doğrudan demoya geçilebilir)
- Benzerlik skorları açıklaması
- **Kesilmeyecekler:** iki demo senaryosu (doğru cevap + ret) ve ölçüm bulgusu — sunumun omurgası bunlar.
