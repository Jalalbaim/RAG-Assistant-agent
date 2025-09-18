from typing import List, Dict
from core.retriever import Retriever

class SearchAgent:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def search(self, query: str, top_k: int = 8) -> List[Dict]:
        return self.retriever.hybrid_search(query, top_k=top_k)
