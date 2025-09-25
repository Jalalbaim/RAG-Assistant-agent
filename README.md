# Assistant documentaire multi-agents (RAG)

**Objectif** : Répondre aux questions à partir des documents internes (PDF, pages exportées, emails .eml), avec **citations garanties** et **garde-fous** pour PII/secrets.

## Stack

- Python, FastAPI
- Embeddings: sentence-transformers
- Vector store: ChromaDB (local, persistant)
- BM25: rank-bm25 (hybride)
- OCR: Tesseract (optionnel si PDF scannés)
- LLM: OpenAI _ou_ Ollama (local).

## Lancer

```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env  # puis éditer
uvicorn app.main:app --reload --port 8000
```
