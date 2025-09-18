from typing import List, Dict
from app.config import Settings
from app.schemas import AskResponse, Passage
from core.retriever import Retriever
from core.llm import LLMClient
from agents.ingestion import IngestionAgent
from agents.indexing import IndexingAgent
from agents.search import SearchAgent
from agents.response import ResponseAgent
from agents.citations_verifier import CitationsVerifierAgent
from agents.guardrail import GuardrailAgent

class Orchestrator:
    def __init__(self, cfg: Settings):
        self.cfg = cfg
        self.retriever = Retriever(cfg)
        self.ing = IngestionAgent(cfg.DATA_DIR)
        self.indexer = IndexingAgent(self.retriever)
        self.search_agent = SearchAgent(self.retriever)
        self.llm = LLMClient(cfg)
        self.responder = ResponseAgent(self.llm)
        self.verifier = CitationsVerifierAgent()
        self.guard = GuardrailAgent(cfg.MASKING_STRATEGY)

    # --- Public API ---
    def run_ingestion(self, path: str) -> Dict:
        docs = self.ing.ingest_path(path)
        stat = self.indexer.index_docs(docs)
        return stat

    def search_only(self, query: str, top_k: int = 8) -> List[Passage]:
        hits = self.search_agent.search(query, top_k=top_k)
        return [Passage(doc_id=h['metadata'].get('doc_id','?'),
                        chunk_id=h['metadata'].get('chunk_id','?'),
                        text=h['text'], score=h['score'], metadata=h['metadata']) for h in hits]

    def handle_question(self, question: str) -> AskResponse:
        # 1) Recherche
        hits = self.search_agent.search(question, top_k=self.cfg.TOP_K)

        passages = hits

        if not passages:
            return AskResponse(answer="Aucun contexte trouvé pour répondre.", sources=[], blocked=False)

        # 2) Réponse conditionnée au contexte
        answer = self.responder.answer(question, passages)

        # 3) Vérif citations
        ok = self.verifier.verify(answer, passages)
        if not ok:
            answer = "Je ne peux pas répondre de façon fiable avec citations à partir des documents fournis."

        # 4) Garde-fous (PII/secrets)
        blocked, masked = (False, answer)
        if self.cfg.ENABLE_GUARDRAILS:
            blocked, masked = self.guard.scan_and_mask(answer)

        # 5) Restitution
        srcs = [Passage(doc_id=p['metadata'].get('doc_id','?'),
                        chunk_id=p['metadata'].get('chunk_id','?'),
                        text=p['text'], score=p['score'], metadata=p['metadata']) for p in passages[:self.cfg.TOP_K]]

        return AskResponse(answer=masked, sources=srcs, blocked=blocked, reason="masquage PII" if blocked else None)
