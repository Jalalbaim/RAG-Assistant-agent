# Assistant documentaire multi-agents (RAG)

**Objectif** : Répondre aux questions à partir des documents internes (PDF, pages exportées, emails .eml), avec **citations garanties** et **garde-fous** pour PII/secrets.

## Stack
- Python, FastAPI
- Embeddings: sentence-transformers (par défaut)
- Vector store: ChromaDB (local, persistant)
- BM25: rank-bm25 (hybride)
- OCR: Tesseract (optionnel si PDF scannés)
- LLM: OpenAI *ou* Ollama (local).

## Lancer
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

## Notes
- Si OCR nécessaire, installez Tesseract en système et (optionnel) Poppler pour `pdf2image`.
- Pour Ollama : installez `ollama`, puis `ollama pull llama3.1:8b-instruct` (ou autre).
- Les réponses incluent des références de type `[#3]` — validées par l’agent de vérification.
