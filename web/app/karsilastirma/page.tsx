"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  results,
  type EvalResults,
  type EvalRow,
  type VariantResult,
} from "@/lib/api";
import { ThemeToggle } from "@/components/ThemeToggle";

const pct = (x: number) => `%${Math.round(x * 1000) / 10}`;

type Sutun = { anahtar: keyof EvalResults; ad: string; not: string; data: VariantResult };

function Verdict({ ok }: { ok: boolean }) {
  return (
    <span className={`stamp-mark ${ok ? "stamp-kabul" : "stamp-ret"}`}>
      {ok ? "DOĞRU" : "HATALI"}
    </span>
  );
}

export default function TeftisRaporu() {
  const [data, setData] = useState<EvalResults | null | undefined>(undefined);

  useEffect(() => {
    results().then(setData);
  }, []);

  const tanim: { anahtar: keyof EvalResults; ad: string; not: string }[] = [
    { anahtar: "v1-baseline", ad: "STANDART (v1)", not: "getir → üret" },
    { anahtar: "v2-corrective", ad: "DÜZELTMELİ (v2)", not: "getir → denetle → gerekirse yeniden ara → üret → kaynak kontrolü" },
    { anahtar: "v3-optimize", ad: "OPTİMİZE (v3)", not: "güçlü eşleşmede denetimi atla, yalnız şüpheli getirmede denetle" },
  ];

  const sutunlar: Sutun[] = data
    ? tanim.flatMap((t) => (data[t.anahtar] ? [{ ...t, data: data[t.anahtar]! }] : []))
    : [];

  const enIyi = sutunlar.length
    ? Math.max(...sutunlar.map((s) => s.data.summary.overall_accuracy))
    : 0;

  const olcutler: { ad: string; al: (s: VariantResult) => string; buyukIyi: boolean }[] = [
    { ad: "Belge isabeti (recall@4)", al: (s) => pct(s.summary.recall_at_k), buyukIyi: true },
    { ad: "Cevap doğruluğu (cevaplanabilir)", al: (s) => pct(s.summary.answerable_accuracy), buyukIyi: true },
    { ad: "Ret doğruluğu (cevaplanamaz)", al: (s) => pct(s.summary.refusal_accuracy), buyukIyi: true },
    { ad: "Genel doğruluk", al: (s) => pct(s.summary.overall_accuracy), buyukIyi: true },
    { ad: "Ortalama cevap süresi", al: (s) => `${s.summary.avg_llm_seconds} sn`, buyukIyi: false },
    { ad: "Medyan toplam süre", al: (s) => `${s.summary.median_total_seconds} sn`, buyukIyi: false },
  ];

  return (
    <div className="flex flex-col flex-1 max-w-6xl w-full mx-auto px-6 pb-16">
      <header className="letterhead pt-8 pb-4 flex items-end justify-between gap-6">
        <div>
          <p className="font-mono text-[0.62rem] tracking-[0.3em] text-muted mb-1">
            YEREL BELGE ARŞİVİ · KARŞILAŞTIRMA
          </p>
          <h1 className="h-display text-3xl sm:text-4xl font-bold">Teftiş Raporu</h1>
          <p className="italic text-ink-soft text-sm mt-1">
            Cevaplama modlarının aynı 44 soruluk etiketli setle ölçülmüş karşılaştırması.
          </p>
        </div>
        <ThemeToggle />
      </header>

      <nav className="flex gap-1.5 mt-6 border-b border-line-strong px-2">
        <Link href="/" className="file-tab">DANIŞMA MASASI</Link>
        <span className="file-tab" data-active="true">TEFTİŞ RAPORU</span>
      </nav>

      {data === undefined && (
        <p className="mt-10 text-center text-muted italic daktilo-bekleme">
          Teftiş dosyası açılıyor
        </p>
      )}

      {data === null && (
        <div className="tutanak p-6 mt-10 max-w-xl mx-auto">
          <p className="font-mono text-[0.68rem] tracking-[0.2em] text-stamp font-semibold mb-2">
            DOSYAYA ULAŞILAMADI
          </p>
          <p className="text-sm text-ink-soft">
            Arşiv sunucusu kapalı görünüyor — <code className="font-mono text-[0.8rem]">python main.py serve</code>{" "}
            çalıştırıp sayfayı yenileyin.
          </p>
        </div>
      )}

      {sutunlar.length > 0 && (
        <main className="mt-8 space-y-10">
          {/* ===== Özet karneler ===== */}
          <section className={`grid grid-cols-1 gap-6 ${sutunlar.length > 2 ? "lg:grid-cols-3 sm:grid-cols-2" : "sm:grid-cols-2"}`}>
            {sutunlar.map(({ ad, not, data: d }) => {
              const kazanan = d.summary.overall_accuracy === enIyi;
              return (
                <div key={ad} className="tutanak p-6 relative">
                  {kazanan && (
                    <span className="stamp-mark stamp-kabul absolute top-4 right-4">EN İYİ</span>
                  )}
                  <p className="font-mono text-[0.65rem] tracking-[0.2em] text-ink-soft font-semibold mb-1">{ad}</p>
                  <p className="font-mono text-[0.6rem] text-muted mb-4 leading-relaxed">{not}</p>
                  <p className="h-display text-5xl font-bold">{pct(d.summary.overall_accuracy)}</p>
                  <p className="font-mono text-[0.62rem] text-muted mt-1 mb-4">
                    genel doğruluk · {d.summary.questions} soru
                  </p>
                  <div className="space-y-1">
                    <div className="islem-satiri">
                      <span>Cevaplanabilir</span><span className="dolgu" />
                      <span>{pct(d.summary.answerable_accuracy)}</span>
                    </div>
                    <div className="islem-satiri">
                      <span>Cevaplanamaz (ret)</span><span className="dolgu" />
                      <span>{pct(d.summary.refusal_accuracy)}</span>
                    </div>
                    <div className="islem-satiri">
                      <span>Medyan süre</span><span className="dolgu" />
                      <span>{d.summary.median_total_seconds} sn</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </section>

          {/* ===== Metrik cetveli ===== */}
          <section className="tutanak p-6 overflow-x-auto">
            <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold mb-4">
              METRİK CETVELİ
            </h2>
            <table className="w-full min-w-[540px]">
              <thead>
                <tr className="border-b-2 border-line-strong font-mono text-[0.62rem] tracking-[0.15em] text-muted">
                  <th className="text-left pb-2 pr-4">ÖLÇÜT</th>
                  {sutunlar.map((s) => (
                    <th key={s.ad} className="pb-2 px-4">{s.anahtar.split("-")[0].toUpperCase()}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {olcutler.map((o) => {
                  const degerler = sutunlar.map((s) => o.al(s.data));
                  const sayilar = sutunlar.map((s) => parseFloat(o.al(s.data).replace("%", "").replace(" sn", "")));
                  const enIyiDeger = o.buyukIyi ? Math.max(...sayilar) : Math.min(...sayilar);
                  return (
                    <tr key={o.ad} className="border-b border-line">
                      <td className="py-2.5 pr-4 text-sm">{o.ad}</td>
                      {degerler.map((d, i) => (
                        <td key={i}
                          className={`py-2.5 px-4 font-mono text-sm text-center ${sayilar[i] === enIyiDeger ? "font-semibold text-stamp" : ""}`}>
                          {d}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <p className="font-mono text-[0.62rem] text-muted mt-4">
              Her satırda en iyi değer vurgulanmıştır. Süre ölçütlerinde küçük olan iyidir.
            </p>
          </section>

          {/* ===== Soru bazlı denetim ===== */}
          <section className="tutanak p-6 overflow-x-auto">
            <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold mb-1">
              SORU BAZLI DENETİM
            </h2>
            <p className="font-mono text-[0.62rem] text-muted mb-4">
              Aynı sorular her modda soruldu; modlar arasında sonucu değişen satırlar vurgulanmıştır.
            </p>
            <table className="w-full min-w-[600px]">
              <thead>
                <tr className="border-b-2 border-line-strong font-mono text-[0.62rem] tracking-[0.15em] text-muted">
                  <th className="text-left pb-2 pr-3">#</th>
                  <th className="text-left pb-2 pr-4">SORU</th>
                  <th className="pb-2 px-3">TÜR</th>
                  {sutunlar.map((s) => (
                    <th key={s.ad} className="pb-2 px-3">{s.anahtar.split("-")[0].toUpperCase()}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sutunlar[0].data.rows.map((ilk: EvalRow) => {
                  const satirlar = sutunlar.map((s) => s.data.rows.find((r) => r.id === ilk.id));
                  const sonuclar = satirlar.map((r) => r?.correct);
                  const degisti = new Set(sonuclar).size > 1;
                  return (
                    <tr key={ilk.id}
                      className={`border-b border-line ${degisti ? "bg-[var(--stamp-soft)]" : ""}`}>
                      <td className="py-2 pr-3 font-mono text-[0.7rem] text-muted">{ilk.id}</td>
                      <td className="py-2 pr-4 text-sm">{ilk.question}</td>
                      <td className="py-2 px-3 text-center font-mono text-[0.6rem] text-muted">
                        {ilk.type === "answerable" ? "CEVAPLI" : "CEVAPSIZ"}
                      </td>
                      {satirlar.map((r, i) => (
                        <td key={i} className="py-2 px-3 text-center">
                          {r ? <Verdict ok={r.correct} /> : <span className="text-muted">—</span>}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </section>
        </main>
      )}

      <footer className="mt-auto pt-12 text-center font-mono text-[0.6rem] tracking-[0.2em] text-muted">
        ÖLÇÜM: eval/eval_set.json · 12 BELGE · 82 PARÇA · AYNI MODELLER
      </footer>
    </div>
  );
}
