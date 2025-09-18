from typing import List, Dict
from core.llm import LLMClient

SYSTEM_PROMPT = """
Tu es un assistant qui répond STRICTEMENT à partir des extraits fournis.
- Si une information n'est pas dans le contexte, dis: "Je ne trouve pas cette information dans les documents." 
- Réponds en phrases courtes et claires.
- Chaque phrase clé DOIT finir par une référence de la forme [#N] (N = index de l'extrait).
- Ne fais AUCUNE hallucination.
Contexte fourni ci-dessous.
"""

def build_context(passages: List[Dict]) -> str:
    lines = []
    for i, p in enumerate(passages, start=1):
        meta = p.get("metadata", {})
        src = meta.get("source_path", meta.get("doc_id", "source"))
        lines.append(f"[{i}] ({src})\n{p['text']}\n")
    return "\n".join(lines)

class ResponseAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def answer(self, question: str, passages: List[Dict]) -> str:
        context = build_context(passages)
        user = f"Question: {question}\n\nExtraits:\n{context}\n\nRéponse (rappelle-toi: chaque phrase clé finit par [#N]):"
        return self.llm.chat(SYSTEM_PROMPT, user)
