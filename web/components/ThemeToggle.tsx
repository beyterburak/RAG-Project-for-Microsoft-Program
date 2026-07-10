"use client";

import { useEffect, useState } from "react";

export function ThemeToggle() {
  const [theme, setTheme] = useState<string | null>(null);

  useEffect(() => {
    setTheme(document.documentElement.dataset.theme ?? "gunduz");
  }, []);

  function toggle() {
    const next = theme === "gece" ? "gunduz" : "gece";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("arsiv-tema", next);
    setTheme(next);
  }

  return (
    <button
      onClick={toggle}
      className="font-mono text-[0.65rem] tracking-[0.15em] border border-line px-3 py-1.5 text-ink-soft hover:text-ink hover:border-line-strong cursor-pointer transition-colors"
      title="Tema değiştir"
    >
      {theme === "gece" ? "☾ GECE NÖBETİ" : "☀ GÜNDÜZ ARŞİVİ"}
    </button>
  );
}
