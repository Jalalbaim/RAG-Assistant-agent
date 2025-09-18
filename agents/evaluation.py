import json
from typing import List, Dict
from agents.search import SearchAgent

class EvaluationAgent:
    def __init__(self, search: SearchAgent):
        self.search = search

    def evaluate(self, qa_pairs: List[Dict], top_k: int = 5) -> Dict:
        # Toy metric: proportion where at least one retrieved chunk contains any gold_answer token
        ok = 0
        for item in qa_pairs:
            q = item["question"]
            gold = item["answer"].lower()
            hits = self.search.search(q, top_k=top_k)
            if any(gold[:20] in h["text"].lower() for h in hits):  # crude heuristic
                ok += 1
        return {"n": len(qa_pairs), "hit_rate": ok / max(1, len(qa_pairs))}
