import re
from typing import List, Dict

class CitationsVerifierAgent:
    REF_RE = re.compile(r"\[#(\d+)\]")  # matches [#N]

    def verify(self, answer: str, passages: List[Dict]) -> bool:
        # Check that each sentence has at least one [#N] and N is valid
        sentences = [s.strip() for s in re.split(r'[\.!?]\s+', answer) if s.strip()]
        if not sentences:
            return False

        valid_indices = set(range(1, len(passages)+1))

        for s in sentences:
            refs = set(int(m.group(1)) for m in self.REF_RE.finditer(s))
            if not refs:
                return False
            if not refs.issubset(valid_indices):
                return False
        return True

    def strip_trailing(self, answer: str) -> str:
        # ensure references remain; no action now but kept for future edits
        return answer
