import json, os
from typing import List, Dict
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import wordpunct_tokenize
nltk.download('punkt', quiet=True)  # ensure tokenizer is available

class BM25Store:
    def __init__(self, path: str):
        self.path = path
        self.records: List[Dict] = []
        self.index = None

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
            except Exception:
                self.records = []

        if self.records:
            self._build_index()

    def _build_index(self):
        corpus = [wordpunct_tokenize(r["text"].lower()) for r in self.records]
        self.index = BM25Okapi(corpus)

    def add_many(self, items: List[Dict]):
        # items: [{id, text, metadata}]
        self.records.extend(items)
        self._persist()
        self._build_index()

    def _persist(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def query(self, q: str, top_k: int = 8):
        if not self.index or not self.records:
            return []
        toks = wordpunct_tokenize(q.lower())
        scores = self.index.get_scores(toks)
        ranked = sorted(zip(range(len(scores)), scores), key=lambda x: x[1], reverse=True)[:top_k]
        out = []
        for idx, score in ranked:
            rec = self.records[idx]
            out.append({"id": rec["id"], "text": rec["text"], "metadata": rec.get("metadata", {}), "score": float(score)})
        return out
