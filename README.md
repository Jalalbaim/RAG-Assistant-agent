# Assistant documentaire multi-agents (RAG)

**Objectif** : Répondre aux questions à partir des documents internes (PDF, pages exportées, emails .eml), avec **citations garanties** et **garde-fous** pour PII/secrets.

## Setup
- Python, FastAPI
- Embeddings: sentence-transformers (par défaut)
- Vector store: ChromaDB (local, persistant)
- BM25: rank-bm25 (hybride)
- OCR: Tesseract (optionnel si PDF scannés)
- LLM: OpenAI *ou* Ollama (local).

## To launch
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env  # puis éditer
uvicorn app.main:app --reload --port 8000
```

## Endpoints
- `POST /ingest` : ingère un fichier ou un dossier (chemin local).  
  Body JSON: `{ "path": "data/docs" }`
- `POST /ask` : poser une question.  
  Body JSON: `{ "question": "..." }`
- `POST /search` : debug retrieval (retours top-k).
- `GET /health` : ping.

