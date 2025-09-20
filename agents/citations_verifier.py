
import re
from typing import List, Dict

class CitationsVerifierAgent:
    REF_RE = re.compile(r"\[#(\d+)\]")

    def verify(self, answer: str, passages: List[Dict]) -> bool:
        sentences = [s.strip() for s in re.split(r'[\.!?]\s+', answer) if s.strip()]
        if not sentences:
            return False
        valid = set(range(1, len(passages)+1))
        any_ref = False
        for s in sentences:
            refs = set(int(m.group(1)) for m in self.REF_RE.finditer(s))
            if refs:
                any_ref = True
                if not refs.issubset(valid):
                    return False
        return any_ref  # au moins une référence valide dans la réponse
