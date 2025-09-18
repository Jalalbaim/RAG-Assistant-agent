import os, glob
from typing import List, Dict
from utils.pdf_utils import extract_text_from_pdf
from utils.text_clean import clean_text
from utils.splitter import split_into_chunks
from utils.id_utils import new_id

SUPPORTED = {".pdf", ".txt", ".md", ".eml"}

def read_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext in {".txt", ".md"}:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext == ".eml":
        # very basic .eml extraction
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        return ""

class IngestionAgent:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def ingest_path(self, path: str) -> List[Dict]:
        files = []
        if os.path.isdir(path):
            for ext in SUPPORTED:
                files.extend(glob.glob(os.path.join(path, f"**/*{ext}"), recursive=True))
        else:
            files = [path]

        docs = []
        for fp in files:
            raw = read_file(fp)
            raw = clean_text(raw)
            if not raw:
                continue
            chunks = split_into_chunks(raw, chunk_size=800, overlap=120)
            for i, ch in enumerate(chunks):
                doc_id = os.path.basename(fp)
                chunk_id = new_id("chunk")
                docs.append({
                    "id": f"{doc_id}::{chunk_id}",
                    "text": ch["text"],
                    "metadata": {"source_path": fp, "doc_id": doc_id, "chunk_id": chunk_id, "chunk_index": i}
                })
        return docs
