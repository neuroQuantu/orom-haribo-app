"""Knowledge aggregation utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .config import KnowledgeSource


@dataclass
class KnowledgeSnapshot:
    """Immutable representation of the knowledge state."""

    catalogue: Dict[str, List[str]]

    def summarize(self) -> str:
        """Return a human-readable summary."""
        segments = []
        for name, entries in self.catalogue.items():
            segments.append(f"{name}: {len(entries)} éléments indexés")
        return " | ".join(segments) if segments else "Aucune connaissance disponible"


class KnowledgeOrchestrator:
    """Loads and normalizes all configured knowledge sources."""

    def __init__(self, sources: Iterable[KnowledgeSource]):
        self.sources = list(sources)

    def load_snapshot(self) -> KnowledgeSnapshot:
        catalogue: Dict[str, List[str]] = {}
        for source in self.sources:
            catalogue[source.name] = source.load_entries()
        return KnowledgeSnapshot(catalogue)

    def search(self, keyword: str) -> Dict[str, List[str]]:
        keyword_lower = keyword.lower()
        matches: Dict[str, List[str]] = {}
        for source in self.sources:
            entries = [
                entry
                for entry in source.load_entries()
                if keyword_lower in entry.lower()
            ]
            if entries:
                matches[source.name] = entries
        return matches
