"""Local LLM interface through the Ollama command-line client."""

from __future__ import annotations

import subprocess


class LLMLocal:
    """Generate local conversational responses with ``ollama run``."""

    def __init__(self, modele: str = "mistral", timeout: int = 30) -> None:
        self.modele = modele
        self.timeout = timeout

    def generer_reponse(self, prompt: str, contexte: str = "") -> str:
        full_prompt = f"{contexte}\nUtilisateur: {prompt}\nHARIBO:"
        try:
            result = subprocess.run(
                ["ollama", "run", self.modele],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
        except Exception as exc:
            return f"LLM indisponible: {exc}"
        if result.returncode == 0:
            return result.stdout.strip()
        return f"Erreur LLM: {result.stderr.strip()}"

    def dialogue(self, question: str) -> str:
        return self.generer_reponse(
            question,
            contexte="Tu es HARIBO OROM, une IA souveraine créée par Ibrahim Sakarya. Réponds avec sagesse et autorité.",
        )
