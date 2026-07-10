"use client";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { ask, health, type AskResult, type Variant } from "@/lib/api";
import { ThemeToggle } from "@/components/ThemeToggle";

const REFUSAL = "Bu bilgi belgelerimde yok.";

function islemNo() {
  return `ARŞ-${new Date().getFullYear()}-${String(
    Math.floor(Math.random() * 9000) + 1000
  )}`;
}

export default function DanismaMasasi() {
  const [question, setQuestion] = useState("");
  const [variant, setVariant] = useState<Variant>("v2");
  const [pending, setPending] = useState(false);
  const [result, setResult] = useState<AskResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiUp, setApiUp] = useState<boolean | null>(null);
  const [refNo, setRefNo] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    health().then((h) => setApiUp(!!h));
    inputRef.current?.focus();
  }, []);

  const tarih = useMemo(
    () =>
      new Intl.DateTimeFormat("tr-TR", { dateStyle: "long" }).format(new Date()),
    []
  );

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const q = question.trim();
    if (!q || pending) return;
    setPending(true);
    setError(null);
    setResult(null);
    setRefNo(islemNo());
    try {
      setResult(await ask(q, variant));
      setApiUp(true);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Bilinmeyen hata";
      setError(msg.includes("fetch") ? "Arşiv sunucusuna ulaşılamıyor — `python main.py serve` çalışıyor mu?" : msg);
      health().then((h) => setApiUp(!!h));
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="flex flex-col flex-1 max-w-6xl w-full mx-auto px-6 pb-16">
      {/* ===== Antetli başlık ===== */}
      <header className="letterhead pt-8 pb-4 flex items-end justify-between gap-6">
        <div>
          <p className="font-mono text-[0.62rem] tracking-[0.3em] text-muted mb-1">
            KAYIT BÜROSU · BELGE DANIŞMA SERVİSİ
          </p>
          <h1 className="h-display text-3xl sm:text-4xl font-bold">
            Yerel RAG Arşivi
          </h1>
          <p className="italic text-ink-soft text-sm mt-1">
            Cevaplar yalnız arşivdeki belgelere dayanır; her tutanak kaynağıyla mühürlenir.
          </p>
        </div>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <div className="yuvarlak-muhur" title="İnternet bağlantısı gerekmez">
            <span>
              ÇEVRİM<br />DIŞI<br />ARŞİV
            </span>
          </div>
        </div>
      </header>

      {/* ===== Dosya sekmeleri ===== */}
      <nav className="flex gap-1.5 mt-6 border-b border-line-strong px-2">
        <span className="file-tab" data-active="true">DANIŞMA MASASI</span>
        <Link href="/karsilastirma" className="file-tab">TEFTİŞ RAPORU</Link>
        <span className="ml-auto self-center font-mono text-[0.62rem] tracking-widest pb-1"
          style={{ color: apiUp === false ? "var(--stamp)" : "var(--muted)" }}>
          {apiUp === null ? "SERVİS: ?" : apiUp ? "SERVİS: AÇIK" : "SERVİS: KAPALI"}
        </span>
      </nav>

      <main className="grid grid-cols-1 lg:grid-cols-[7fr_5fr] gap-8 mt-8 items-start">
        {/* ===== Sol: talep formu + tutanak ===== */}
        <section>
          <form onSubmit={onSubmit} className="tutanak p-6 belge-gelis">
            <div className="flex justify-between items-baseline mb-5">
              <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold">
                TALEP FORMU
              </h2>
              <span className="font-mono text-[0.62rem] text-muted">{tarih}</span>
            </div>

            <label className="block mb-6">
              <span className="font-mono text-[0.62rem] tracking-[0.2em] text-muted block mb-1.5">
                TALEP KONUSU
              </span>
              <input
                ref={inputRef}
                className="form-input"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Arşive sormak istediğiniz soruyu yazınız…"
                maxLength={500}
                disabled={pending}
              />
            </label>

            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex gap-2" role="radiogroup" aria-label="İşlem usulü">
                <button type="button" className="usul-radio" data-checked={variant === "v1"}
                  onClick={() => setVariant("v1")}>
                  <span className="kutu" /> STANDART USUL (v1)
                </button>
                <button type="button" className="usul-radio" data-checked={variant === "v2"}
                  onClick={() => setVariant("v2")}>
                  <span className="kutu" /> DÜZELTMELİ USUL (v2)
                </button>
              </div>
              <button className="stamp-btn" disabled={pending || !question.trim()}>
                {pending ? "İŞLENİYOR…" : "İŞLEME AL"}
              </button>
            </div>
          </form>

          {/* --- Tutanak / cevap --- */}
          {pending && (
            <div className="tutanak tutanak-ruled p-6 mt-6 belge-gelis">
              <p className="font-mono text-[0.68rem] tracking-[0.2em] text-ink-soft daktilo-bekleme">
                TALEP İŞLEME ALINDI — ARŞİV TARANIYOR
              </p>
              <p className="text-sm text-muted italic mt-3">
                {variant === "v2"
                  ? "Düzeltmeli usulde fişler tek tek incelenir; işlem birkaç saniye uzun sürebilir."
                  : "Standart usul: en yakın fişler doğrudan kâtibe iletilir."}
              </p>
            </div>
          )}

          {error && (
            <div className="tutanak p-6 mt-6 belge-gelis border-stamp!">
              <p className="font-mono text-[0.68rem] tracking-[0.2em] text-stamp font-semibold mb-2">
                İŞLEM HATASI
              </p>
              <p className="text-sm text-ink-soft">{error}</p>
            </div>
          )}

          {result && (
            <article className="tutanak p-6 mt-6 belge-gelis relative overflow-hidden">
              <div className="flex justify-between items-baseline border-b border-line pb-3 mb-4">
                <h3 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold">
                  CEVAP TUTANAĞI
                </h3>
                <span className="font-mono text-[0.62rem] text-muted">
                  İşlem No: {refNo} · {result.variant === "v2" ? "Düzeltmeli" : "Standart"} Usul
                </span>
              </div>

              <p className="font-mono text-[0.65rem] text-muted mb-3">
                Talep: <span className="italic">{result.question}</span>
              </p>

              {result.is_refusal ? (
                <div className="py-10 grid place-items-center">
                  <span className="buyuk-muhur">BU BİLGİ BELGELERDE YOK</span>
                  {result.corrective?.rewritten_query && (
                    <p className="font-mono text-[0.62rem] text-muted mt-6">
                      Düzeltme kaydı: arama &ldquo;{result.corrective.rewritten_query}&rdquo; olarak
                      yinelendi, uygun evrak bulunamadı.
                    </p>
                  )}
                </div>
              ) : (
                <p className="text-[1.08rem] leading-[1.85rem]">{result.answer}</p>
              )}

              <div className="border-t border-line mt-5 pt-3 flex flex-wrap gap-x-6 gap-y-1">
                <span className="font-mono text-[0.62rem] text-muted">
                  İşlem süresi: tarama {result.retrieval_seconds} sn · yazım {result.llm_seconds} sn
                </span>
                {result.corrective && result.corrective.graded_out > 0 && (
                  <span className="font-mono text-[0.62rem] text-muted">
                    {result.corrective.graded_out} fiş incelemede elendi
                  </span>
                )}
              </div>
            </article>
          )}

          {!result && !pending && !error && (
            <div className="mt-10 text-center text-muted italic text-sm">
              <p>Arşiv hazır. Talebinizi yazıp <span className="font-mono not-italic text-[0.7rem]">İŞLEME AL</span> mührüne basınız.</p>
            </div>
          )}
        </section>

        {/* ===== Sağ: işlem tutanağı ===== */}
        <aside className="lg:sticky lg:top-6">
          <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold mb-3">
            İŞLEM TUTANAĞI
          </h2>

          {!result && (
            <p className="text-sm text-muted italic border-l-2 border-line pl-3">
              İşlem yapıldığında taranan fişler ve aşama kayıtları burada dosyalanır.
            </p>
          )}

          {result && (
            <div className="space-y-1.5 mb-5 belge-gelis">
              <div className="islem-satiri">
                <span>Arşiv tarandı</span><span className="dolgu" />
                <span>{result.retrieval_seconds} sn</span>
              </div>
              {result.corrective && (
                <div className="islem-satiri">
                  <span>Fiş incelemesi ({result.corrective.graded_out} elendi)</span>
                  <span className="dolgu" /><span>usul gereği</span>
                </div>
              )}
              {result.corrective?.rewritten_query && (
                <div className="islem-satiri">
                  <span>Düzeltme kaydı düşüldü</span><span className="dolgu" />
                  <span>{result.corrective.attempts}. deneme</span>
                </div>
              )}
              <div className="islem-satiri">
                <span>{result.is_refusal ? "Ret mührü basıldı" : "Tutanak yazıldı"}</span>
                <span className="dolgu" /><span>{result.llm_seconds} sn</span>
              </div>
            </div>
          )}

          {result && result.chunks.length > 0 && (
            <div className="space-y-4">
              {result.chunks.map((c, i) => (
                <div key={`${c.source}-${c.chunk_index}`} className="fis p-4 pt-5 belge-gelis"
                  style={{ animationDelay: `${i * 90}ms` }}>
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <span className="font-mono text-[0.62rem] font-semibold text-ink-soft break-all">
                      {c.source} <span className="text-muted">/ fiş {c.chunk_index}</span>
                    </span>
                    {result.variant === "v2" && (
                      <span className="stamp-mark stamp-kabul">KABUL</span>
                    )}
                  </div>
                  <p className="text-[0.78rem] leading-relaxed text-ink-soft line-clamp-3">
                    {c.text}
                  </p>
                  <p className="font-mono text-[0.6rem] text-muted mt-2">
                    Benzerlik: {c.score.toFixed(4)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </aside>
      </main>

      <footer className="mt-auto pt-12 text-center font-mono text-[0.6rem] tracking-[0.2em] text-muted">
        FOUNDRY LOCAL · QWEN3.5-2B + QWEN3-EMBEDDING-0.6B · SQLITE · TÜM İŞLEMLER BU CİHAZDA
      </footer>
    </div>
  );
}
