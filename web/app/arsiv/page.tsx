"use client";

import { useEffect, useState } from "react";
import { corpus, type Corpus } from "@/lib/api";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Sekmeler } from "@/components/Sekmeler";

const belgeTuru = (source: string) =>
  source.startsWith("ders_") ? "DERS NOTU" : "ÜRÜN DOKÜMANI";

export default function ArsivKatalogu() {
  const [data, setData] = useState<Corpus | null | undefined>(undefined);

  useEffect(() => {
    corpus().then(setData);
  }, []);

  const enBuyuk = data ? Math.max(...data.documents.map((d) => d.chunks)) : 1;

  return (
    <div className="flex flex-col flex-1 max-w-6xl w-full mx-auto px-6 pb-16">
      <header className="letterhead pt-8 pb-4 flex items-end justify-between gap-6">
        <div>
          <p className="font-mono text-[0.62rem] tracking-[0.3em] text-muted mb-1">
            YEREL BELGE ARŞİVİ · KATALOG
          </p>
          <h1 className="h-display text-3xl sm:text-4xl font-bold">Arşiv Kataloğu</h1>
          <p className="italic text-ink-soft text-sm mt-1">
            Asistanın cevap verirken kullanabildiği belgelerin tamamı — bu listede olmayan hiçbir bilgi cevaplara giremez.
          </p>
        </div>
        <ThemeToggle />
      </header>

      <Sekmeler aktif="/arsiv" />

      {data === undefined && (
        <p className="mt-10 text-center text-muted italic daktilo-bekleme">Katalog açılıyor</p>
      )}

      {data === null && (
        <div className="tutanak p-6 mt-10 max-w-xl mx-auto">
          <p className="font-mono text-[0.68rem] tracking-[0.2em] text-stamp font-semibold mb-2">
            KATALOĞA ULAŞILAMADI
          </p>
          <p className="text-sm text-ink-soft">
            Arşiv sunucusu kapalı görünüyor — <code className="font-mono text-[0.8rem]">python main.py serve</code>{" "}
            çalıştırıp sayfayı yenileyin.
          </p>
        </div>
      )}

      {data && (
        <main className="mt-8 space-y-8">
          {/* künye */}
          <section className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { etiket: "BELGE", deger: String(data.total_documents) },
              { etiket: "PARÇA", deger: String(data.total_chunks) },
              { etiket: "VEKTÖR BOYUTU", deger: "1024" },
              { etiket: "AĞ TRAFİĞİ", deger: "YOK" },
            ].map((k) => (
              <div key={k.etiket} className="tutanak p-4 text-center">
                <p className="h-display text-3xl font-bold">{k.deger}</p>
                <p className="font-mono text-[0.58rem] tracking-[0.15em] text-muted mt-1">
                  {k.etiket}
                </p>
              </div>
            ))}
          </section>

          {/* raf listesi */}
          <section className="tutanak p-6">
            <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold mb-1">
              RAF LİSTESİ
            </h2>
            <p className="font-mono text-[0.62rem] text-muted mb-5">
              Her belge, aranabilir parçalara bölünerek saklanır. Çubuklar parça sayısını gösterir.
            </p>

            <div className="space-y-3">
              {data.documents.map((d, i) => {
                return (
                  <div key={d.source} className="belge-gelis"
                    style={{ animationDelay: `${i * 40}ms` }}>
                    <div className="flex items-baseline justify-between gap-3 mb-1">
                      <span className="text-sm">
                        {d.title}{" "}
                        <span className="font-mono text-[0.55rem] tracking-wider text-muted ml-1 whitespace-nowrap">
                          {belgeTuru(d.source)}
                        </span>
                      </span>
                      <span className="font-mono text-[0.62rem] text-muted whitespace-nowrap">
                        {d.chunks} parça · {(d.characters / 1000).toFixed(1)}k karakter
                      </span>
                    </div>
                    <div className="h-2 border border-line-strong bg-[var(--card-aged)]">
                      <div
                        className="h-full bg-[var(--tab)]"
                        style={{ width: `${(d.chunks / enBuyuk) * 100}%` }}
                      />
                    </div>
                    <p className="font-mono text-[0.55rem] text-muted mt-1">{d.source}</p>
                  </div>
                );
              })}
            </div>
          </section>

          <section className="tutanak p-6">
            <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold mb-3">
              ARŞİV NASIL DERLENDİ?
            </h2>
            <div className="space-y-3 text-sm leading-relaxed text-ink-soft">
              <p>
                <strong className="text-ink">Ürün dokümanları kurgusaldır.</strong> &ldquo;Zyntrix&rdquo; diye bir
                ürün yoktur; kılavuz, SSS, sürüm notları ve garanti şartnamesi bu proje için yazılmıştır.
                Model bu ürünü ön eğitiminden bilemeyeceği için, doğru cevap verdiğinde bilgiyi kesinlikle
                arşivden almış olur — sistemin gerçekten belge okuduğunun kanıtı budur.
              </p>
              <p>
                <strong className="text-ink">X9 Pro kılavuzu bilinçli bir çeldiricidir.</strong> Standart X9 ile
                aynı bölüm başlıklarına ama farklı sayılara sahiptir (21 saat pil / 104 gram / IP67). Birbirine
                çok benzeyen iki belge arasında ayrım yapabilme sınavıdır.
              </p>
              <p>
                <strong className="text-ink">Ders notları Vikipedi&apos;den derlenmiştir</strong> (CC BY-SA,
                her dosyada atıflı) ve gerçek içerikle çalışıldığını gösterir.
              </p>
            </div>
          </section>
        </main>
      )}

      <footer className="mt-auto pt-12 text-center font-mono text-[0.6rem] tracking-[0.2em] text-muted">
        BELGELER data/ KLASÖRÜNDE · PARÇALAR rag.db İÇİNDE · HER İKİSİ DE BU CİHAZDA
      </footer>
    </div>
  );
}
