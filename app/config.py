import os
from dotenv import load_dotenv

load_dotenv()

def getenv_bool(key: str, default: bool) -> bool:
    v = os.getenv(key)
    if v is None:
        return default
    return v.strip().lower() in {"1","true","yes","y","on"}

class Settings:
    DATA_DIR = os.getenv("DATA_DIR", "./data")
    CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma")
    BM25_PATH = os.getenv("BM25_PATH", "./data/bm25_corpus.json")

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    TOP_K = int(os.getenv("TOP_K", "8"))
    HYBRID_ALPHA = float(os.getenv("HYBRID_ALPHA", "0.5"))

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai") # openai|ollama
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")

    ENABLE_GUARDRAILS = getenv_bool("ENABLE_GUARDRAILS", True)
    MASKING_STRATEGY = os.getenv("MASKING_STRATEGY", "brackets")  # brackets|stars

    # derive
    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.CHROMA_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(cls.BM25_PATH), exist_ok=True)

Settings.ensure_dirs()
