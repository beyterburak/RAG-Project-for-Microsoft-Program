# Ders Notu: Veritabanları

## Tanım

Veritabanı, yapılandırılmış bilgi ve verilerin depolandığı alandır. Geleneksel dosya-işlem sistemine alternatif olarak geliştirilmiştir ve büyük veri miktarlarının düzenli biçimde yönetilmesini sağlar.

## Veritabanı Yönetim Sistemi (VTYS)

VTYS (İng. DBMS), veritabanını oluşturma, yapılandırma, sorgulama, güvenlik yönetimi ve bakım işlerini üstlenen yazılımdır. Yaygın örnekler: MySQL, PostgreSQL, Oracle, Microsoft SQL Server, IBM DB2, Microsoft Access ve SQLite (sunucusuz, tek dosyalık).

## İlişkisel Model

En yaygın veri modelidir; veriler tablolarda saklanır. Satırlar (row) kayıtları, sütunlar (column) alanları temsil eder. İlişkisel model 1970'lerde **Edgar F. Codd** tarafından geliştirilmiştir. Sorgulama için standart dil **SQL**'dir (Structured Query Language); türevleri arasında PL/SQL ve T-SQL bulunur.

## Normalizasyon

Veri tekrarını ve tutarsızlığı önlemek için şema tasarımında uygulanan kurallardır. Kademeli formlar: 1NF (Birinci Normal Form), 2NF, 3NF ve BCNF (Boyce-Codd Normal Formu). Her form bir öncekinin şartlarını kapsar ve üzerine yeni kısıt ekler.

## NoSQL Sistemleri

İlişkisel olmayan (NoSQL) veritabanları, genellikle anahtar-değer prensibiyle çalışır ve belirli iş yüklerinde ilişkisel modele göre daha hızlıdır. Örnekler: Redis, Couchbase, Amazon DynamoDB. 21. yüzyılda farklı sorgulama yaklaşımlarının yaygınlaşmasıyla popülerlik kazanmışlardır.

## Veritabanı Yöneticisinin Görevleri

Mantıksal veri modelleme, fiziksel veritabanı tasarımı, SQL sorguları yazma, güvenlik ve veri bütünlüğü yönetimi, performans optimizasyonu.

---
*Kaynak: Vikipedi "Veri tabanı" maddesinden derlenmiştir (CC BY-SA).*
