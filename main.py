"""Yerel RAG AI Asistanı — giriş noktası.

Komutlar:
  python main.py catalog     Model kataloğunu listele, config alias'larını doğrula
  python main.py hello       'Hello Model' kurulum testi (Hafta 1 kilometre taşı)
  python main.py embed-demo  Embedding benzerlik demosu (Hafta 1, Gün 3-4)
  python main.py db-demo     SQLite şema + serileştirme testi (Hafta 1, Gün 5)
  python main.py prompt-demo Prompt şablonu davranış gözlemi (Hafta 1, Gün 6)
  python main.py integration-test  Hafta 1 uçtan uca entegrasyon testi (Gün 7)
  python main.py chunk-demo  Belge parçalama istatistikleri (Hafta 2, Gün 8-9)
  python main.py ingest      Belgeleri embed edip rag.db'ye yaz (Gün 10-11)
  python main.py retrieve [soru]  Top-K parça getir / doğrulama seti (Gün 12-13)
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
    sub.add_parser("integration-test", help="Hafta 1 uçtan uca entegrasyon testi")
    sub.add_parser("chunk-demo", help="Belge parçalama istatistikleri")
    sub.add_parser("ingest", help="Belgeleri embed edip rag.db'ye yaz")
    p_retrieve = sub.add_parser("retrieve", help="Top-K parça getir / doğrulama seti")
    p_retrieve.add_argument("query", nargs="?", default=None, help="Sorgu (boşsa doğrulama seti koşulur)")
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
    elif args.command == "integration-test":
        from src.integration_test import run
        run()
    elif args.command == "chunk-demo":
        from src.chunking import run
        run()
    elif args.command == "ingest":
        from src.ingest import run
        run()
    elif args.command == "retrieve":
        from src.retrieval import run
        run(args.query)


if __name__ == "__main__":
    main()
