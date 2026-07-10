"""Yerel RAG AI Asistanı — giriş noktası.

Komutlar:
  python main.py catalog     Model kataloğunu listele, config alias'larını doğrula
  python main.py hello       'Hello Model' kurulum testi (Hafta 1 kilometre taşı)
  python main.py embed-demo  Embedding benzerlik demosu (Hafta 1, Gün 3-4)
  python main.py db-demo     SQLite şema + serileştirme testi (Hafta 1, Gün 5)
  python main.py prompt-demo Prompt şablonu davranış gözlemi (Hafta 1, Gün 6)
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Yerel RAG AI Asistanı (Foundry Local)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("catalog", help="Kataloğu listele ve alias'ları doğrula")
    sub.add_parser("hello", help="Hello Model kurulum testi")
    sub.add_parser("embed-demo", help="Embedding benzerlik demosu")
    sub.add_parser("db-demo", help="SQLite şema + serileştirme testi")
    sub.add_parser("prompt-demo", help="Prompt şablonu davranış gözlemi")
    args = parser.parse_args()

    if args.command == "catalog":
        from src.check_catalog import run
        run()
    elif args.command == "hello":
        from src.hello_model import run
        run()
    elif args.command == "embed-demo":
        from src.similarity import run
        run()
    elif args.command == "db-demo":
        from src.db import run
        run()
    elif args.command == "prompt-demo":
        from src.prompt_demo import run
        run()


if __name__ == "__main__":
    main()
