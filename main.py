"""Yerel RAG AI Asistanı — giriş noktası.

Komutlar:
  python main.py catalog   Model kataloğunu listele, config alias'larını doğrula
  python main.py hello     'Hello Model' kurulum testi (Hafta 1 kilometre taşı)
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Yerel RAG AI Asistanı (Foundry Local)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("catalog", help="Kataloğu listele ve alias'ları doğrula")
    sub.add_parser("hello", help="Hello Model kurulum testi")
    args = parser.parse_args()

    if args.command == "catalog":
        from src.check_catalog import run
        run()
    elif args.command == "hello":
        from src.hello_model import run
        run()


if __name__ == "__main__":
    main()
