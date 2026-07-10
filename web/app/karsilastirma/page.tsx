import Link from "next/link";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function TeftisRaporu() {
  return (
    <div className="flex flex-col flex-1 max-w-6xl w-full mx-auto px-6 pb-16">
      <header className="letterhead pt-8 pb-4 flex items-end justify-between gap-6">
        <div>
          <p className="font-mono text-[0.62rem] tracking-[0.3em] text-muted mb-1">
            KAYIT BÜROSU · DENETİM SERVİSİ
          </p>
          <h1 className="h-display text-3xl sm:text-4xl font-bold">Teftiş Raporu</h1>
          <p className="italic text-ink-soft text-sm mt-1">
            Standart usul (v1) ile düzeltmeli usulün (v2) karşılaştırmalı denetimi.
          </p>
        </div>
        <ThemeToggle />
      </header>

      <nav className="flex gap-1.5 mt-6 border-b border-line-strong px-2">
        <Link href="/" className="file-tab">DANIŞMA MASASI</Link>
        <span className="file-tab" data-active="true">TEFTİŞ RAPORU</span>
      </nav>

      <main className="mt-10 text-center text-muted italic">
        <p>Teftiş dosyası hazırlanıyor — bu sekme Faz 4&apos;te doldurulacak.</p>
      </main>
    </div>
  );
}
