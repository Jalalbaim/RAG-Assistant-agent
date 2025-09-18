from typing import List, Dict
import re

def split_into_chunks(text: str, chunk_size: int = 800, overlap: int = 120) -> List[Dict]:
    # simple word-based splitter
    words = re.findall(r"\S+|\n", text)
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        piece = " ".join(words[start:end])
        chunks.append({"text": piece})
        if end == len(words):
            break
        start = max(end - overlap, 0)
    return chunks
