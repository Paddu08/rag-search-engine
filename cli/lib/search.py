# search.py

import os
import pickle
import string
from typing import Iterable


def remove_punctuation(val: str) -> str:
    return val.lower().translate(str.maketrans("", "", string.punctuation))


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def _add_document(self, doc_id: int, text: str) -> None:
        tokens = remove_punctuation(text).split()
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def build(self, movies: Iterable[dict]) -> None:
        for m in movies:
            doc_id = m["id"]
            text = f"{m['description']} {m["title"]}"
            self._add_document(doc_id, text)
            self.docmap[doc_id] = m

    def get_documents(self, term: str) -> set[int]:
        term = remove_punctuation(term)
        return self.index.get(term, set())

    def save(self, cache_dir: str = "cache") -> None:
        os.makedirs(cache_dir, exist_ok=True)
        with open(f"{cache_dir}/index.pkl", "wb") as f:
            pickle.dump(self.index, f)
        with open(f"{cache_dir}/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self, cache_dir: str = "cache") -> None:
        index_path = f"{cache_dir}/index.pkl"
        docmap_path = f"{cache_dir}/docmap.pkl"

        if not os.path.exists(index_path) or not os.path.exists(docmap_path):
            raise FileNotFoundError("Index not built. Run `build` first.")

        with open(index_path, "rb") as f:
            self.index = pickle.load(f)
        with open(docmap_path, "rb") as f:
            self.docmap = pickle.load(f)
