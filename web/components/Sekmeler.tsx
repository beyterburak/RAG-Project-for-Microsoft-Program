import Link from "next/link";

const SEKMELER = [
  { href: "/", ad: "DANIŞMA MASASI" },
  { href: "/arsiv", ad: "ARŞİV KATALOĞU" },
  { href: "/karsilastirma", ad: "TEFTİŞ RAPORU" },
];

export function Sekmeler({ aktif, sag }: { aktif: string; sag?: React.ReactNode }) {
  return (
    <nav className="flex gap-1.5 mt-6 border-b border-line-strong px-2">
      {SEKMELER.map((s) =>
        s.href === aktif ? (
          <span key={s.href} className="file-tab" data-active="true">
            {s.ad}
          </span>
        ) : (
          <Link key={s.href} href={s.href} className="file-tab">
            {s.ad}
          </Link>
        )
      )}
      {sag && <span className="ml-auto self-center pb-1">{sag}</span>}
    </nav>
  );
}
