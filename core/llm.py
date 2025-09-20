from typing import List, Dict
from app.config import Settings

class LLMClient:
    def __init__(self, cfg: Settings):
        self.cfg = cfg
        self.provider = cfg.LLM_PROVIDER.lower()

        if self.provider == "openai":
            from openai import OpenAI
            self._client = OpenAI(api_key=cfg.OPENAI_API_KEY)
        elif self.provider == "ollama":
            import ollama
            self._client = ollama
        else:
            raise RuntimeError("Unsupported LLM_PROVIDER. Use 'openai' or 'ollama'.")

    def chat(self, system: str, user: str) -> str:
        if self.provider == "openai":
            resp = self._client.chat.completions.create(
                model=self.cfg.OPENAI_MODEL,
                messages=[{"role":"system","content":system},{"role":"user","content":user}],
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()

        # ---- OLLAMA (Gemma-friendly) ----
        try:
            # Utilise la vraie API "chat" -> laisse le template du modèle faire le bon formatage
            resp = self._client.chat(
                model=self.cfg.OLLAMA_MODEL,
                messages=[{"role":"system","content":system},{"role":"user","content":user}],
                options={"temperature": 0.2},
            )
            return resp["message"]["content"].strip()
        except Exception:
            # Fallback robuste si jamais l’API chat n’est pas dispo
            prompt = f"SYSTEM:\n{system}\n\nUSER:\n{user}\n\nASSISTANT:"
            r = self._client.generate(
                model=self.cfg.OLLAMA_MODEL,
                prompt=prompt,
                options={"temperature": 0.2},
            )
            return r["response"].strip()
