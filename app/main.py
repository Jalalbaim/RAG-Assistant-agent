from fastapi import FastAPI, HTTPException
from app.schemas import IngestRequest, AskRequest, SearchRequest, AskResponse, Passage
from app.config import Settings
from agents.orchestrator import Orchestrator

app = FastAPI(title="RAG Multi-Agents", version="0.1.0")
orchestrator = Orchestrator(Settings())

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(req: IngestRequest):
    try:
        stats = orchestrator.run_ingestion(req.path)
        return {"ingested": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
def search(req: SearchRequest):
    try:
        results = orchestrator.search_only(req.query, req.top_k)
        return {"results": [r.__dict__ for r in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        result = orchestrator.handle_question(req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
