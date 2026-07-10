import type { Metadata } from "next";
import { Zilla_Slab, Spectral, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const zilla = Zilla_Slab({
  weight: ["500", "600", "700"],
  subsets: ["latin", "latin-ext"],
  variable: "--font-display",
});

const spectral = Spectral({
  weight: ["400", "500", "600"],
  style: ["normal", "italic"],
  subsets: ["latin", "latin-ext"],
  variable: "--font-body",
});

const plexMono = IBM_Plex_Mono({
  weight: ["400", "500", "600"],
  subsets: ["latin", "latin-ext"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Yerel RAG Arşivi — Danışma Masası",
  description:
    "Tamamen çevrimdışı, kaynak gösteren belge soru-cevap asistanı (Foundry Local + SQLite).",
};

const themeInit = `
try {
  const saved = localStorage.getItem("arsiv-tema");
  const theme = saved ?? (matchMedia("(prefers-color-scheme: dark)").matches ? "gece" : "gunduz");
  document.documentElement.dataset.theme = theme;
} catch {}
`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="tr"
      suppressHydrationWarning
      className={`${zilla.variable} ${spectral.variable} ${plexMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
        {children}
      </body>
    </html>
  );
}
