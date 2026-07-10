"""Belge parçalama (chunking) — Hafta 2, Gün 8-9.

Strateji: markdown başlık/paragraf sınırlarına saygılı, parametrik parçalama.
- Paragraflar asla ortadan bölünmez (tek paragraf chunk_size'ı aşmadıkça).
- Her parçanın başına "Belge Başlığı — Bölüm" bağlam satırı eklenir; belge
  başlığı olmadan bölüm parçaları konudan (örn. ürün adından) kopuyordu.
- Ardışık parçalar arasında örtüşme: önceki parçanın son paragrafı,
  overlap sınırına sığıyorsa yeni parçanın başında tekrarlanır.

Kullanım: python main.py chunk-demo
"""

from pathlib import Path

import config


def _split_blocks(text: str) -> list[str]:
    """Metni boş satırlardan bloklara ayırır (başlıklar ayrı blok olur)."""
    blocks, current = [], []
    for line in text.splitlines():
        if line.strip():
            current.append(line.rstrip())
        elif current:
            blocks.append("\n".join(current))
            current = []
    if current:
        blocks.append("\n".join(current))
    return blocks


def _hard_split(paragraph: str, chunk_size: int, overlap: int) -> list[str]:
    """chunk_size'dan uzun tek paragrafı karakter bazında böler."""
    pieces, start = [], 0
    step = max(1, chunk_size - overlap)  # overlap >= chunk_size'da sonsuz döngü koruması
    while start < len(paragraph):
        pieces.append(paragraph[start:start + chunk_size])
        start += step
    return pieces


def chunk_document(text: str, source: str,
                   chunk_size: int = config.CHUNK_SIZE,
                   overlap: int = config.CHUNK_OVERLAP) -> list[tuple[str, int, str]]:
    """Bir belgeyi (source, chunk_index, chunk_text) listesine parçalar."""
    doc_title = ""
    heading = ""
    chunks: list[str] = []
    buffer: list[str] = []          # mevcut parçanın paragrafları
    buffer_heading = ""

    def emit():
        nonlocal buffer
        if buffer:
            body = "\n\n".join(buffer)
            chunks.append(f"{buffer_heading}\n\n{body}" if buffer_heading else body)
            buffer = []

    for block in _split_blocks(text):
        if block.lstrip().startswith("#"):
            emit()
            section = block.strip("# ").strip()
            if not doc_title:
                doc_title = section
                heading = doc_title
            else:
                heading = f"{doc_title} — {section}"
            buffer_heading = heading
            continue

        paragraphs = ([block] if len(block) <= chunk_size
                      else _hard_split(block, chunk_size, overlap))
        for para in paragraphs:
            current_len = sum(len(p) for p in buffer)
            if buffer and current_len + len(para) > chunk_size:
                last = buffer[-1]
                emit()
                buffer_heading = heading
                # örtüşme: önceki parçanın son paragrafı sığıyorsa taşı
                if len(last) <= overlap:
                    buffer.append(last)
            elif not buffer:
                buffer_heading = heading
            buffer.append(para)

    emit()
    return [(source, i, chunk) for i, chunk in enumerate(chunks)]


def chunk_directory(data_dir: Path = config.DATA_DIR,
                    chunk_size: int = config.CHUNK_SIZE,
                    overlap: int = config.CHUNK_OVERLAP) -> list[tuple[str, int, str]]:
    """data/ altındaki tüm .md/.txt belgeleri parçalar."""
    all_chunks = []
    for path in sorted(data_dir.glob("*")):
        if path.suffix.lower() not in (".md", ".txt"):
            continue
        text = path.read_text(encoding="utf-8")
        all_chunks.extend(chunk_document(text, path.name, chunk_size, overlap))
    return all_chunks


def run() -> None:
    """Parametre deneyi + varsayılan ayarla belge bazında istatistik."""
    print("Parametre deneyi (toplam parça sayısı / ortalama uzunluk):\n")
    print(f"  {'chunk_size':>10} {'overlap':>8} {'parça':>6} {'ort. uzunluk':>13}")
    for size, ov in [(400, 80), (800, 150), (1200, 200)]:
        chunks = chunk_directory(chunk_size=size, overlap=ov)
        avg = sum(len(c) for _, _, c in chunks) / len(chunks)
        print(f"  {size:>10} {ov:>8} {len(chunks):>6} {avg:>12.0f}c")

    print(f"\nVarsayılan ayar (size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP}) "
          f"ile belge bazında:\n")
    chunks = chunk_directory()
    by_source: dict[str, list[str]] = {}
    for source, _, text in chunks:
        by_source.setdefault(source, []).append(text)
    for source, texts in by_source.items():
        lens = [len(t) for t in texts]
        print(f"  {source:<36} {len(texts):>3} parça  "
              f"(min {min(lens)}, ort {sum(lens)//len(lens)}, max {max(lens)})")

    print(f"\nToplam: {len(chunks)} parça")
    print("\n--- Örnek parça (ilk belge, 2. parça) ---")
    sample = [c for c in chunks if c[0] == chunks[0][0]]
    source, idx, text = sample[min(1, len(sample) - 1)]
    print(f"[{source} / parça {idx}]\n{text}")
