import io, os
from typing import List
from pypdf import PdfReader
import pdfplumber
from PIL import Image
import pytesseract

def extract_text_from_pdf(path: str) -> str:
    try:
        # try text first
        text = []
        reader = PdfReader(path)
        for page in reader.pages:
            t = page.extract_text() or ""
            text.append(t)
        joined = "\n".join(text).strip()
        if joined:
            return joined
    except Exception:
        pass

    # fallback to OCR per page
    txt = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            try:
                img = page.to_image(resolution=200)
                pil = Image.open(io.BytesIO(img.original))
                ocr = pytesseract.image_to_string(pil, lang="eng+fra")
                txt.append(ocr)
            except Exception:
                continue
    return "\n".join(txt)
