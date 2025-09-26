"""Top-level orchestration of HARIBO OROM."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from .avatar import EthicalAvatar
from .config import HariboConfig, discover_config
from .integration import IntegrationManager
from .knowledge import KnowledgeOrchestrator
from .security import QuantumSecurityFramework


@dataclass
class SystemState:
    owner: str
    knowledge_summary: str
    integrations: Dict[str, str]


class HariboQuantumSystem:
    """Executable wrapper around the HARIBO reference architecture."""

    def __init__(self, config: HariboConfig | None = None) -> None:
        if config is None:
            repo_root = Path(__file__).resolve().parent.parent
            config = discover_config([repo_root / "configs" / "haribo_config.json"])
        self.config = config
        self.security = QuantumSecurityFramework(
            owner=config.system.owner,
            audit_storage=Path(".haribo_audit.json").resolve(),
        )
        self.knowledge = KnowledgeOrchestrator(config.knowledge_sources)
        self.integrations = IntegrationManager(config.integration_targets)
        self.avatar = EthicalAvatar()
        self._initialize_avatar()

    def _initialize_avatar(self) -> None:
        self.avatar.set_disclosure(
            "connaissances",
            "Synthèse multi-sources historisées, présentes et classifiées sous supervision souveraine.",
        )
        self.avatar.set_disclosure(
            "sécurité",
            "Journalisation immuable et contrôle d'accès quantifié pour Ibrahim uniquement.",
        )
        self.avatar.set_disclosure(
            "intégrations",
            "Connecteurs harmonisés couvrant mobile, desktop, wearables, smart_home et quantum_cloud.",
        )

    def initialize_system(self) -> SystemState:
        token = self.security.sovereign_login()
        knowledge_snapshot = self.knowledge.load_snapshot()
        integration_statuses = self.integrations.connect_all()
        self.security.authorize_action(token, "synchronisation_connaissances")
        self.security.authorize_action(token, "synchronisation_integrations")
        self.security.revoke(token)
        return SystemState(
            owner=self.config.system.owner,
            knowledge_summary=knowledge_snapshot.summarize(),
            integrations={status.target: status.detail for status in integration_statuses},
        )

    def avatar_report(self) -> str:
        return self.avatar.respond("Rapport d'état")

    def search_knowledge(self, keyword: str) -> Dict[str, list[str]]:
        return self.knowledge.search(keyword)
