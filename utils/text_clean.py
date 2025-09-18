import re

def normalize_ws(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()

def clean_text(s: str) -> str:
    s = s.replace('\x00', ' ')
    s = normalize_ws(s)
    return s
