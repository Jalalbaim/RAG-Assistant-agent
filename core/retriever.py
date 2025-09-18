from typing import List, Dict
from app.config import Settings
from core.embeddings import Embeddings
from core.vectorstore import VectorStore
from core.bm25_store import BM25Store

class Retriever:
    def __init__(self, cfg: Settings):
        self.cfg = cfg
        self.emb = Embeddings(cfg.EMBEDDING_MODEL)
        self.vs = VectorStore(cfg.CHROMA_DIR)
        self.bm25 = BM25Store(cfg.BM25_PATH)

    def add_documents(self, docs: List[Dict]):
        # docs items: {id, text, metadata}
        ids = [d["id"] for d in docs]
        texts = [d["text"] for d in docs]
        metas = [d.get("metadata", {}) for d in docs]
        embs = self.emb.encode(texts)
        self.vs.add(ids=ids, embeddings=embs, metadatas=metas, documents=texts)
        self.bm25.add_many(docs)

    def hybrid_search(self, query: str, top_k: int) -> List[Dict]:
        q_emb = self.emb.encode([query])
        vec_hits = self.vs.query(q_emb, top_k=top_k*2)  # wider then cut
        bm25_hits = self.bm25.query(query, top_k=top_k*2)

        # Normalize scores to [0,1], smaller distance -> higher score for vectors
        def norm_vec_score(d):
            # cosine distance in Chroma is 1 - cosine_sim; we invert
            return 1.0 - float(d.get("distance", 1.0))

        max_b = max([h["score"] for h in bm25_hits], default=1.0)
        def norm_bm25_score(s): return (s / max_b) if max_b > 0 else 0.0

        alpha = float(self.cfg.HYBRID_ALPHA)
        merged = {}

        for h in vec_hits:
            sid = h["id"]
            merged.setdefault(sid, {"text": h["doc"], "metadata": h["metadata"], "vec": 0.0, "bm25": 0.0})
            merged[sid]["vec"] = max(merged[sid]["vec"], norm_vec_score(h))

        for h in bm25_hits:
            sid = h["id"]
            merged.setdefault(sid, {"text": h["text"], "metadata": h["metadata"], "vec": 0.0, "bm25": 0.0})
            merged[sid]["bm25"] = max(merged[sid]["bm25"], norm_bm25_score(h["score"]))

        scored = []
        for sid, v in merged.items():
            score = alpha * v["vec"] + (1 - alpha) * v["bm25"]
            scored.append({"id": sid, "text": v["text"], "metadata": v["metadata"], "score": float(score)})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
