from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IngestRequest(BaseModel):
    path: str = Field(..., description="Fichier ou dossier à ingérer")

class AskRequest(BaseModel):
    question: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 8

class Passage(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    score: float
    metadata: Dict[str, Any] = {}

class AskResponse(BaseModel):
    answer: str
    sources: List[Passage]
    blocked: bool = False
    reason: Optional[str] = None
