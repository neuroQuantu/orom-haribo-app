"""Configuration loading utilities for HARIBO OROM."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
import json


@dataclass(frozen=True)
class KnowledgeSource:
    """Represents a structured knowledge source on disk."""

    name: str
    path: Path

    def load_entries(self) -> List[str]:
        """Return sanitized entries from the knowledge source."""
        entries: List[str] = []
        if not self.path.exists():
            return entries
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            entries.append(line.lstrip("- "))
        return entries


@dataclass(frozen=True)
class SystemConfig:
    owner: str
    creation_date: str
    sovereignty_level: str


@dataclass(frozen=True)
class SecurityConfig:
    allowed_channels: List[str]
    audit_retention_days: int
    alert_emails: List[str]


@dataclass(frozen=True)
class HariboConfig:
    system: SystemConfig
    security: SecurityConfig
    knowledge_sources: List[KnowledgeSource]
    integration_targets: List[str]
    dimensions: List[str]

    @classmethod
    def from_dict(cls, payload: dict, base_path: Path | None = None) -> "HariboConfig":
        base_path = base_path or Path.cwd()
        system = payload["system"]
        security = payload["security"]
        knowledge_sources = [
            KnowledgeSource(name=source["name"], path=(base_path / source["path"]).resolve())
            for source in payload.get("knowledge_sources", [])
        ]
        return cls(
            system=SystemConfig(**system),
            security=SecurityConfig(**security),
            knowledge_sources=knowledge_sources,
            integration_targets=list(payload.get("integration_targets", [])),
            dimensions=list(payload.get("dimensions", [])),
        )


def load_config(config_path: Path) -> HariboConfig:
    """Load configuration from a JSON file."""
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return HariboConfig.from_dict(payload, base_path=config_path.parent.parent)


def discover_config(paths: Iterable[Path]) -> HariboConfig:
    """Return the first configuration found in *paths*."""
    for candidate in paths:
        if candidate.exists():
            return load_config(candidate)
    raise FileNotFoundError("No HARIBO configuration file found")
