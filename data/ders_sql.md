# Ders Notu: SQL (Yapılandırılmış Sorgu Dili)

## Tanım

SQL (Structured Query Language), ilişkisel veritabanlarındaki verileri tanımlamak, sorgulamak ve yönetmek için kullanılan dildir. Genel amaçlı bir programlama dili değil, veritabanı ortamında çalışan bir alt dildir.

## Tarihçe

Önce SQUARE adlı matematiksel bir sorgulama dili geliştirilmiş, ardından kullanımı kolaylaştırmak amacıyla İngilizceye benzer sözdizimine sahip **SEQUEL** oluşturulmuştur. Dil daha sonra **SQL** adını almış ve ilişkisel veritabanı sistemlerinin standart sorgulama dili hâline gelmiştir.

## Alt Diller

**Veri Tanımlama Dili (DDL)** — veritabanı yapısını tanımlar:
- `CREATE TABLE`: yeni tablo oluşturur
- `ALTER TABLE`: mevcut tabloda yapısal değişiklik yapar
- `DROP TABLE`: tabloyu tümüyle siler
- `TRUNCATE TABLE`: verileri siler, tablo yapısını korur
- `CREATE INDEX` / `DROP INDEX`: indeks işlemleri

**Veri İşleme Dili (DML)** — veriyi kullanır:
- `SELECT`: veri sorgular
- `INSERT`: yeni kayıt ekler
- `UPDATE`: mevcut kayıtları günceller
- `DELETE`: kayıt siler

## Temel Sorgu Yapısı

Bir `SELECT` sorgusu genellikle şu bileşenlerden oluşur: seçilecek sütunlar, `FROM` ile kaynak tablo, `WHERE` ile filtre koşulu, `GROUP BY` ile gruplama, `HAVING` ile grup filtresi ve `ORDER BY` ile sıralama.

## Tabloları Birleştirme (JOIN)

Birden fazla tablodaki veriyi birleştirmek için `JOIN` kullanılır. `INNER JOIN` yalnızca eşleşen satırları, `LEFT JOIN` soldaki tablonun tüm satırlarını, `RIGHT JOIN` sağdaki tablonun tüm satırlarını, `FULL JOIN` ise her iki taraftaki tüm satırları döndürür.

## SQL Destekleyen Sistemler

MySQL, PostgreSQL, Oracle, Microsoft SQL Server, IBM DB2, Sybase, Firebird ve SQLite gibi sistemler SQL dilini destekler. Her sistemin standarda ek olarak kendi lehçesi bulunur (örneğin PL/SQL, T-SQL).

---
*Kaynak: Vikipedi "SQL" maddesinden derlenmiştir (CC BY-SA).*
