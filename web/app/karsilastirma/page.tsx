"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { results, type EvalResults, type EvalRow, type EvalSummary } from "@/lib/api";
import { ThemeToggle } from "@/components/ThemeToggle";

const pct = (x: number) => `%${Math.round(x * 1000) / 10}`;

function Verdict({ ok }: { ok: boolean }) {
  return (
    <span className={`stamp-mark ${ok ? "stamp-kabul" : "stamp-ret"}`}>
      {ok ? "DOĞRU" : "HATALI"}
    </span>
  );
}

function MetricRow({
  label, v1, v2, better,
}: { label: string; v1: string; v2: string; better?: "v2" | "eşit" | "maliyet" }) {
  return (
    <tr className="border-b border-line">
      <td className="py-2.5 pr-4 text-sm">{label}</td>
      <td className="py-2.5 px-4 font-mono text-sm text-center">{v1}</td>
      <td className="py-2.5 px-4 font-mono text-sm text-center font-semibold">{v2}</td>
      <td className="py-2.5 pl-4 text-center">
        {better === "v2" && <span className="stamp-mark stamp-kabul">İYİLEŞME</span>}
        {better === "eşit" && <span className="font-mono text-[0.62rem] text-muted">—</span>}
        {better === "maliyet" && <span className="stamp-mark stamp-ret">BEDEL</span>}
      </td>
    </tr>
  );
}

export default function TeftisRaporu() {
  const [data, setData] = useState<EvalResults | null | undefined>(undefined);

  useEffect(() => {
    results().then(setData);
  }, []);

  const v1 = data?.["v1-baseline"];
  const v2 = data?.["v2-corrective"];

  return (
    <div className="flex flex-col flex-1 max-w-6xl w-full mx-auto px-6 pb-16">
      <header className="letterhead pt-8 pb-4 flex items-end justify-between gap-6">
        <div>
          <p className="font-mono text-[0.62rem] tracking-[0.3em] text-muted mb-1">
            YEREL BELGE ARŞİVİ · KARŞILAŞTIRMA
          </p>
          <h1 className="h-display text-3xl sm:text-4xl font-bold">Teftiş Raporu</h1>
          <p className="italic text-ink-soft text-sm mt-1">
            Standart (v1) ve düzeltmeli (v2) modların aynı 26 soruluk setle ölçülmüş karşılaştırması.
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

      {v1 && v2 && (
        <main className="mt-8 space-y-10">
          {/* ===== Özet karnesi ===== */}
          <section className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {[
              { ad: "STANDART (v1)", s: v1.summary, not: "getir → üret" },
              { ad: "DÜZELTMELİ (v2)", s: v2.summary, not: "getir → denetle → gerekirse yeniden ara → üret → kaynak kontrolü" },
            ].map(({ ad, s, not }) => (
              <div key={ad} className="tutanak p-6">
                <p className="font-mono text-[0.65rem] tracking-[0.2em] text-ink-soft font-semibold mb-1">{ad}</p>
                <p className="font-mono text-[0.6rem] text-muted mb-4">{not}</p>
                <p className="h-display text-5xl font-bold">{pct(s.overall_accuracy)}</p>
                <p className="font-mono text-[0.62rem] text-muted mt-1 mb-4">genel doğruluk · {s.questions} soru</p>
                <div className="space-y-1">
                  <div className="islem-satiri">
                    <span>Cevaplanabilir</span><span className="dolgu" /><span>{pct(s.answerable_accuracy)}</span>
                  </div>
                  <div className="islem-satiri">
                    <span>Cevaplanamaz (ret)</span><span className="dolgu" /><span>{pct(s.refusal_accuracy)}</span>
                  </div>
                  <div className="islem-satiri">
                    <span>Medyan süre</span><span className="dolgu" /><span>{s.median_total_seconds} sn</span>
                  </div>
                </div>
              </div>
            ))}
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
                  <th className="pb-2 px-4">v1</th>
                  <th className="pb-2 px-4">v2</th>
                  <th className="pb-2 pl-4">HÜKÜM</th>
                </tr>
              </thead>
              <tbody>
                <MetricRow label={`Belge isabeti (recall@${v1.summary.top_k})`}
                  v1={pct(v1.summary.recall_at_k)} v2={pct(v2.summary.recall_at_k)} better="eşit" />
                <MetricRow label="Cevap doğruluğu (cevaplanabilir)"
                  v1={pct(v1.summary.answerable_accuracy)} v2={pct(v2.summary.answerable_accuracy)} better="v2" />
                <MetricRow label="Ret doğruluğu (cevaplanamaz)"
                  v1={pct(v1.summary.refusal_accuracy)} v2={pct(v2.summary.refusal_accuracy)} better="v2" />
                <MetricRow label="Genel doğruluk"
                  v1={pct(v1.summary.overall_accuracy)} v2={pct(v2.summary.overall_accuracy)} better="v2" />
                <MetricRow label="Ortalama cevap süresi"
                  v1={`${v1.summary.avg_llm_seconds} sn`} v2={`${v2.summary.avg_llm_seconds} sn`} better="maliyet" />
                <MetricRow label="Medyan toplam süre"
                  v1={`${v1.summary.median_total_seconds} sn`} v2={`${v2.summary.median_total_seconds} sn`} better="maliyet" />
              </tbody>
            </table>
            <p className="font-mono text-[0.62rem] text-muted mt-4">
              Hüküm: düzeltmeli mod doğruluğu artırır; bedeli cevap süresidir. Denetim maliyeti bilinçli bir ödünleşimdir.
            </p>
          </section>

          {/* ===== Soru bazlı denetim listesi ===== */}
          <section className="tutanak p-6 overflow-x-auto">
            <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold mb-1">
              SORU BAZLI DENETİM
            </h2>
            <p className="font-mono text-[0.62rem] text-muted mb-4">
              Aynı sorular iki modda da soruldu; değişen sonuçlar vurgulanmıştır.
            </p>
            <table className="w-full min-w-[560px]">
              <thead>
                <tr className="border-b-2 border-line-strong font-mono text-[0.62rem] tracking-[0.15em] text-muted">
                  <th className="text-left pb-2 pr-3">#</th>
                  <th className="text-left pb-2 pr-4">SORU</th>
                  <th className="pb-2 px-3">TÜR</th>
                  <th className="pb-2 px-3">v1</th>
                  <th className="pb-2 pl-3">v2</th>
                </tr>
              </thead>
              <tbody>
                {v1.rows.map((r1: EvalRow) => {
                  const r2 = v2.rows.find((r) => r.id === r1.id);
                  if (!r2) return null;
                  const changed = r1.correct !== r2.correct;
                  return (
                    <tr key={r1.id}
                      className={`border-b border-line ${changed ? "bg-[var(--stamp-soft)]" : ""}`}>
                      <td className="py-2 pr-3 font-mono text-[0.7rem] text-muted">{r1.id}</td>
                      <td className="py-2 pr-4 text-sm">{r1.question}</td>
                      <td className="py-2 px-3 text-center font-mono text-[0.6rem] text-muted">
                        {r1.type === "answerable" ? "CEVAPLI" : "CEVAPSIZ"}
                      </td>
                      <td className="py-2 px-3 text-center"><Verdict ok={r1.correct} /></td>
                      <td className="py-2 pl-3 text-center"><Verdict ok={r2.correct} /></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </section>
        </main>
      )}

      <footer className="mt-auto pt-12 text-center font-mono text-[0.6rem] tracking-[0.2em] text-muted">
        ÖLÇÜM: eval/eval_set.json · 26 SORU · AYNI BİLGİ TABANI VE MODELLER
      </footer>
    </div>
  );
}
