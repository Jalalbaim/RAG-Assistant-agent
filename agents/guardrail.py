import re
from typing import Tuple

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\b(\+?\d[\d\s().-]{7,}\d)\b")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
SECRET_HINT = re.compile(r"(?i)(api[_-]?key|secret|password|mdp|token|private\s*key)")

def mask(text: str, style: str = "brackets") -> str:
    if style == "stars":
        return "***REDACTED***"
    return "[REDACTED]"

class GuardrailAgent:
    def __init__(self, style: str = "brackets"):
        self.style = style

    def scan_and_mask(self, text: str) -> Tuple[bool, str]:
        blocked = False
        def repl(m):
            nonlocal blocked
            blocked = True
            return mask(m.group(0), self.style)

        text = EMAIL_RE.sub(repl, text)
        text = PHONE_RE.sub(repl, text)
        text = IBAN_RE.sub(repl, text)
        text = SECRET_HINT.sub(repl, text)
        return blocked, text
