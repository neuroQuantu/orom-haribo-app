"""Ethical avatar implementation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class EthicalConstraints:
    no_persuasion: bool = True
    truth_only: bool = True
    transparency_required: bool = True


class EthicalAvatar:
    """A deterministic avatar that enforces the ethical charter."""

    def __init__(self, constraints: EthicalConstraints | None = None) -> None:
        self.constraints = constraints or EthicalConstraints()
        self._disclosures: Dict[str, str] = {}

    def set_disclosure(self, capability: str, description: str) -> None:
        self._disclosures[capability] = description

    def respond(self, prompt: str) -> str:
        """Respond to *prompt* without violating constraints."""
        if not prompt.strip():
            return "Aucune instruction détectée."
        acknowledgement = "Instruction enregistrée."
        disclosures = self._format_disclosures()
        return f"{acknowledgement}\nContraintes actives: {self._constraint_summary()}\n{disclosures}"

    def _format_disclosures(self) -> str:
        if not self._disclosures:
            return "Aucune capacité déclarée."
        lines = ["Capacités déclarées:"]
        for capability, description in self._disclosures.items():
            lines.append(f"- {capability}: {description}")
        return "\n".join(lines)

    def _constraint_summary(self) -> str:
        flags: list[str] = []
        if self.constraints.no_persuasion:
            flags.append("pas de persuasion")
        if self.constraints.truth_only:
            flags.append("vérité obligatoire")
        if self.constraints.transparency_required:
            flags.append("transparence")
        return ", ".join(flags)
