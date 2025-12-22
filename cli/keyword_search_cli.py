#!/usr/bin/env python3

import argparse
import json
from lib.search import InvertedIndex, remove_punctuation


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command")

    search_parser = subparsers.add_parser("search", help="Search movies")
    search_parser.add_argument("query", type=str)

    subparsers.add_parser("build", help="Build inverted index")

    args = parser.parse_args()

    if args.command == "build":
        with open("./data/movies.json", "r", encoding="utf-8") as f:
            movies = json.load(f)["movies"]

        index = InvertedIndex()
        index.build(movies)
        index.save()
        print("Index built successfully.")
        return

    if args.command == "search":
        index = InvertedIndex()
        try:
            index.load()
        except FileNotFoundError as e:
            print(e)
            return

        result_docs = None
        terms = remove_punctuation(args.query).split()

        for term in terms:
            docs = index.get_documents(term)
            if result_docs is None:
                result_docs = set(docs)
            else:
                result_docs |= docs

            if result_docs and len(result_docs) >= 5:
                break

        if not result_docs:
            print("No match")
            return

        for doc_id in sorted(result_docs)[:5]:
            movie = index.docmap[doc_id]
            print(f"{movie['title']} {movie['id']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
