from typing import List, Dict
from core.retriever import Retriever

class IndexingAgent:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def index_docs(self, docs: List[Dict]):
        if docs:
            self.retriever.add_documents(docs)
        return {"added": len(docs)}
