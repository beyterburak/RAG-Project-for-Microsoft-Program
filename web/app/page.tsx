"use client";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { askStream, health, type Chunk, type Variant } from "@/lib/api";
import { ThemeToggle } from "@/components/ThemeToggle";

type Stage = { label: string; detail: string };
type DoneMeta = {
  answer: string;
  is_refusal: boolean;
  revoked: boolean;
  rewritten_query: string | null;
  retrieval_seconds: number;
  llm_seconds: number;
};

function islemNo() {
  return `ARŞ-${new Date().getFullYear()}-${String(
    Math.floor(Math.random() * 9000) + 1000
  )}`;
}

export default function DanismaMasasi() {
  const [question, setQuestion] = useState("");
  const [variant, setVariant] = useState<Variant>("v2");
  const [pending, setPending] = useState(false);
  const [askedQuestion, setAskedQuestion] = useState("");
  const [askedVariant, setAskedVariant] = useState<Variant>("v2");
  const [stages, setStages] = useState<Stage[]>([]);
  const [chunks, setChunks] = useState<Chunk[]>([]);
  const [text, setText] = useState("");
  const [meta, setMeta] = useState<DoneMeta | null>(null);
  const [revoked, setRevoked] = useState(false);
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
    const v = variant;
    setPending(true);
    setError(null);
    setStages([]);
    setChunks([]);
    setText("");
    setMeta(null);
    setRevoked(false);
    setAskedQuestion(q);
    setAskedVariant(v);
    setRefNo(islemNo());

    try {
      await askStream(q, v, (ev) => {
        switch (ev.type) {
          case "graded":
            setStages((s) => [...s, {
              label: ev.attempt > 1 ? `Parça denetimi (${ev.attempt}. deneme)` : "Parça denetimi",
              detail: `${ev.kept} kabul · ${ev.out} elendi`,
            }]);
            break;
          case "rewritten":
            setStages((s) => [...s, { label: "Soru yeniden yazıldı", detail: "yeni arama" }]);
            break;
          case "chunks":
            setChunks(ev.chunks);
            setStages((s) => [...s, { label: "Arşiv tarandı", detail: `${ev.seconds} sn` }]);
            break;
          case "token":
            setText((t) => t + ev.text);
            break;
          case "verifying":
            setStages((s) => [...s, { label: "Cevap kaynak denetiminde", detail: "kontrol" }]);
            break;
          case "revoked":
            setRevoked(true);
            setStages((s) => [...s, { label: "Cevap denetimde reddedildi", detail: "ret" }]);
            break;
          case "done":
            setMeta(ev);
            setStages((s) => [...s, {
              label: ev.is_refusal ? (ev.revoked ? "Ret mührü basıldı" : "Cevap bulunamadı — ret") : "Cevap yazıldı",
              detail: `${ev.llm_seconds} sn`,
            }]);
            setApiUp(true);
            break;
          case "error":
            setError(ev.detail);
            break;
        }
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Bilinmeyen hata";
      setError(
        msg.includes("fetch")
          ? "Arşiv sunucusuna ulaşılamıyor — `python main.py serve` çalışıyor mu?"
          : msg
      );
      health().then((h) => setApiUp(!!h));
    } finally {
      setPending(false);
    }
  }

  const showTutanak = pending || text || meta || revoked;

  return (
    <div className="flex flex-col flex-1 max-w-6xl w-full mx-auto px-6 pb-16">
      {/* ===== Antetli başlık ===== */}
      <header className="letterhead pt-8 pb-4 flex items-end justify-between gap-6">
        <div>
          <p className="font-mono text-[0.62rem] tracking-[0.3em] text-muted mb-1">
            YEREL BELGE ARŞİVİ · SORU-CEVAP
          </p>
          <h1 className="h-display text-3xl sm:text-4xl font-bold">
            Yerel RAG Arşivi
          </h1>
          <p className="italic text-ink-soft text-sm mt-1">
            Sorularınızı yalnızca arşivdeki belgelere dayanarak, kaynak göstererek yanıtlar — internet olmadan.
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
        {/* ===== Sol: soru formu + tutanak ===== */}
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
                SORUNUZ
              </span>
              <input
                ref={inputRef}
                className="form-input"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Belgelere ne sormak istersiniz?"
                maxLength={500}
                disabled={pending}
              />
            </label>

            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex gap-2" role="radiogroup" aria-label="Cevaplama modu">
                <button type="button" className="usul-radio" data-checked={variant === "v1"}
                  onClick={() => setVariant("v1")}>
                  <span className="kutu" /> STANDART (v1)
                </button>
                <button type="button" className="usul-radio" data-checked={variant === "v2"}
                  onClick={() => setVariant("v2")}>
                  <span className="kutu" /> DÜZELTMELİ (v2)
                </button>
              </div>
              <button className="stamp-btn" disabled={pending || !question.trim()}>
                {pending ? "ARANIYOR…" : "ARŞİVE SOR"}
              </button>
            </div>
          </form>

          {error && (
            <div className="tutanak p-6 mt-6 belge-gelis">
              <p className="font-mono text-[0.68rem] tracking-[0.2em] text-stamp font-semibold mb-2">
                İŞLEM HATASI
              </p>
              <p className="text-sm text-ink-soft">{error}</p>
            </div>
          )}

          {showTutanak && !error && (
            <article className="tutanak p-6 mt-6 belge-gelis relative overflow-hidden">
              <div className="flex justify-between items-baseline border-b border-line pb-3 mb-4">
                <h3 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold">
                  CEVAP TUTANAĞI
                </h3>
                <span className="font-mono text-[0.62rem] text-muted">
                  İşlem No: {refNo} · {askedVariant === "v2" ? "Düzeltmeli" : "Standart"}
                </span>
              </div>

              <p className="font-mono text-[0.65rem] text-muted mb-3">
                Soru: <span className="italic">{askedQuestion}</span>
              </p>

              {/* akan / biten cevap */}
              {meta?.is_refusal ? (
                <div className="py-6 grid place-items-center gap-4">
                  {revoked && text && (
                    <p className="text-[0.95rem] leading-relaxed opacity-35 line-through decoration-[var(--stamp)] decoration-2 max-w-prose">
                      {text}
                    </p>
                  )}
                  <span className="buyuk-muhur">BU BİLGİ BELGELERDE YOK</span>
                  {revoked && (
                    <p className="font-mono text-[0.62rem] text-muted">
                      Yazılan cevap kaynak denetiminden geçemediği için iptal edildi.
                    </p>
                  )}
                  {meta.rewritten_query && (
                    <p className="font-mono text-[0.62rem] text-muted">
                      Soru &ldquo;{meta.rewritten_query}&rdquo; olarak yeniden aranıp denendi;
                      yine de uygun bir kayıt bulunamadı.
                    </p>
                  )}
                </div>
              ) : text ? (
                <p className={`text-[1.08rem] leading-[1.85rem] ${pending ? "daktilo-bekleme" : ""}`}>
                  {text}
                </p>
              ) : (
                <p className="font-mono text-[0.68rem] tracking-[0.2em] text-ink-soft daktilo-bekleme">
                  {askedVariant === "v2" ? "PARÇALAR DENETLENİYOR" : "ARŞİV TARANIYOR"}
                </p>
              )}

              {meta && (
                <div className="border-t border-line mt-5 pt-3 flex flex-wrap gap-x-6 gap-y-1">
                  <span className="font-mono text-[0.62rem] text-muted">
                    Süre: arama {meta.retrieval_seconds} sn · cevap {meta.llm_seconds} sn
                  </span>
                </div>
              )}
            </article>
          )}

          {!showTutanak && !error && (
            <div className="mt-10 text-center text-muted italic text-sm">
              <p>Arşiv hazır — sorunuzu yazın, gerisini raflar halleder.</p>
            </div>
          )}
        </section>

        {/* ===== Sağ: işlem kaydı ===== */}
        <aside className="lg:sticky lg:top-6">
          <h2 className="font-mono text-[0.68rem] tracking-[0.25em] text-ink-soft font-semibold mb-3">
            İŞLEM KAYDI
          </h2>

          {stages.length === 0 && (
            <p className="text-sm text-muted italic border-l-2 border-line pl-3">
              Bir soru sorduğunuzda, taranan belge parçaları ve işlem adımları burada görünür.
            </p>
          )}

          {stages.length > 0 && (
            <div className="space-y-1.5 mb-5">
              {stages.map((s, i) => (
                <div key={i} className="islem-satiri belge-gelis">
                  <span>{s.label}</span>
                  <span className="dolgu" />
                  <span>{s.detail}</span>
                </div>
              ))}
              {pending && (
                <div className="islem-satiri opacity-60">
                  <span className="daktilo-bekleme">işlem sürüyor</span>
                </div>
              )}
            </div>
          )}

          {chunks.length > 0 && (
            <div className="space-y-4">
              {chunks.map((c, i) => (
                <div key={`${c.source}-${c.chunk_index}`} className="fis p-4 pt-5 belge-gelis"
                  style={{ animationDelay: `${i * 90}ms` }}>
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <span className="font-mono text-[0.62rem] font-semibold text-ink-soft break-all">
                      {c.source} <span className="text-muted">/ parça {c.chunk_index}</span>
                    </span>
                    {askedVariant === "v2" && (
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
