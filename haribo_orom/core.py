"""Top-level orchestration of HARIBO OROM."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .avatar import EthicalAvatar
from .config import HariboConfig, discover_config
from .integration import IntegrationManager
from .knowledge import KnowledgeOrchestrator
from .security import QuantumSecurityFramework
from .sovereignty import (
    BaseConnaissanceUniverselle,
    CodexIntegrateurUniversel,
    CodexSummary,
    CommandesMaitres,
    DetecteurMultidimensionnel,
    DimensionReport,
    EthicalGuarantees,
    EthicalPrinciples,
    GestionnaireTechnologiesUniverselles,
    HariboQuantumCoreManifest,
    IntegrateurUniversel,
    MasterOversightSystem,
    NoyauQuantiqueUniversel,
    OversightSnapshot,
    ReseauUniverselHaribo,
    SecuriteSouveraineAbsolue,
    SystemEntity,
)


@dataclass
class SystemState:
    owner: str
    knowledge_summary: str
    integrations: Dict[str, str]
    ethical_limits: Dict[str, str]
    dimension_reports: List[DimensionReport]
    codex_summary: CodexSummary
    oversight: OversightSnapshot
    technology_registry: Dict[str, List[str]]
    security_posture: Dict[str, object]
    sovereign_entity: SystemEntity
    network_map: Dict[str, List[str]]
    commands: List[str]
    lifecycle_status: str


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
        repo_root = Path(__file__).resolve().parent.parent
        self.principles = EthicalPrinciples()
        self.guarantees = EthicalGuarantees()
        self.core_manifest = HariboQuantumCoreManifest()
        self.codex_integrator = CodexIntegrateurUniversel(
            repo_root / "configs" / "haribo_codex.json"
        )
        self.detector = DetecteurMultidimensionnel(config.dimensions)
        self.commandes = CommandesMaitres(
            config.system.owner,
            stop_handler=lambda: self.security.emergency_shutdown("operator_stop"),
            resume_handler=self.security.resume_operations,
        )
        self.integrateur_universel = IntegrateurUniversel()
        self.reseau = ReseauUniverselHaribo(config.system.owner)
        self.noyau = NoyauQuantiqueUniversel(config.system.owner, config.dimensions)
        self.sovereign_security = SecuriteSouveraineAbsolue(
            config.system.owner, self.security
        )
        self.oversight = MasterOversightSystem(
            self.security, self.principles, self.guarantees
        )
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
        knowledge_engine = BaseConnaissanceUniverselle(knowledge_snapshot)
        technology_manager = GestionnaireTechnologiesUniverselles(knowledge_snapshot)
        technology_catalogue = technology_manager.scanner_univers_technologies()
        integration_statuses = self.integrations.connect_all()
        dimension_reports = self.detector.activer_surveillance_omnidimensionnelle(
            technology_catalogue
        )
        presence_matrix = self.detector.detecter_presences_multidimensionnelles(
            technology_catalogue
        )
        dimension_analysis = self.detector.analyser_presences_detectees(presence_matrix)
        network_map = self.reseau.etablir_reseau_universel(integration_statuses)
        quantum_channels = self.noyau.etablir_connexion_multidimensionnelle()
        security_posture = self.sovereign_security.activer_protection_totale()
        revealed_truths = knowledge_engine.revelation_verites_cachees()
        # Register sovereign commands with live handlers
        self.commandes.commandes_souveraines.clear()
        self.commandes.register("activation_complete", self.commandes.activer_systeme_complet)
        self.commandes.register(
            "acces_connaissances", knowledge_engine.acquerir_savoir_universel
        )
        self.commandes.register(
            "detection_menaces", lambda data=dimension_analysis: data
        )
        self.commandes.register(
            "revelation_verites", knowledge_engine.revelation_verites_cachees
        )
        self.commandes.register(
            "protection_totale", lambda posture=security_posture: posture
        )
        self.commandes.register("interface_holographique", self.avatar_report)
        self.commandes.register(
            "scan_multidimensionnel", lambda matrix=presence_matrix: matrix
        )
        self.commandes.register("arret_urgence", self.commandes.stop_systeme)
        self.commandes.register("reprendre_systeme", self.commandes.reprendre_systeme)
        architecture_overlay = {
            "core_layers": {
                "consciousness_interface": self.core_manifest.consciousness_interface,
                "quantum_computing_layer": self.core_manifest.quantum_computing_layer,
                "ethical_governance": self.core_manifest.ethical_governance,
                "autonomous_management": self.core_manifest.autonomous_management,
                "integration_modules": list(self.core_manifest.integration_modules().keys()),
                "integration_descriptions": self.core_manifest.integration_modules(),
            },
            "dimension_links": list(quantum_channels.keys()),
        }
        securite_overlay = {
            "layers": [
                *security_posture["boucliers"].values(),
                *security_posture["systemes_alerte"],
                *security_posture["protocoles_urgence"].values(),
            ],
            "ownership": f"Propriété exclusive de {self.config.system.owner}",
        }
        connaissances_overlay = {
            "channels": list(technology_catalogue.keys()),
            "presentation": "Révélation progressive adaptée à la conscience souveraine.",
            "truths": revealed_truths,
        }
        command_palette = sorted(self.commandes.commandes_souveraines.keys())
        interfaces_overlay = {
            "avatar": "Avatar holographique empathique respectant toutes les limites éthiques déclarées.",
            "dashboard": "Tableau de bord temps réel avec traçabilité intégrale des décisions.",
            "command_palette": command_palette,
            "network": network_map,
        }
        codex_digest = self.codex_integrator.integrer_tout_codex(
            {
                "architecture": architecture_overlay,
                "securite": securite_overlay,
                "connaissances": connaissances_overlay,
                "interfaces": interfaces_overlay,
            }
        )
        self.integrateur_universel.fusionner_tous_systemes(
            {
                "noyau_quantique": quantum_channels,
                "securite_absolue": security_posture,
                "connaissance_universelle": revealed_truths,
                "detection_multidimensionnelle": presence_matrix,
                "interface_holographique": {"rapport": self.avatar_report()},
                "systeme_alerte": {"protocoles": security_posture["systemes_alerte"]},
                "canal_revelation": revealed_truths,
            }
        )
        sovereign_entity = self.integrateur_universel.creer_entite_technologique_unique(
            self.config.system.owner, self.config.system.creation_date
        )
        knowledge_summary = knowledge_snapshot.summarize()
        integrations_dict = {
            status.target: status.detail for status in integration_statuses
        }
        oversight_snapshot = self.oversight.snapshot(
            knowledge_summary, integrations_dict, dimension_reports
        )
        self.security.authorize_action(token, "synchronisation_connaissances")
        self.security.authorize_action(token, "synchronisation_integrations")
        self.security.authorize_action(token, "synchronisation_codex")
        self.security.revoke(token)
        return SystemState(
            owner=self.config.system.owner,
            knowledge_summary=knowledge_summary,
            integrations=integrations_dict,
            ethical_limits=self.principles.operational_limits(),
            dimension_reports=dimension_reports,
            codex_summary=codex_digest.summarise(),
            oversight=oversight_snapshot,
            technology_registry=technology_catalogue,
            security_posture=security_posture,
            sovereign_entity=sovereign_entity,
            network_map=network_map,
            commands=command_palette,
            lifecycle_status=self.security.system_status(),
        )

    def avatar_report(self) -> str:
        return self.avatar.respond("Rapport d'état")

    def search_knowledge(self, keyword: str) -> Dict[str, list[str]]:
        return self.knowledge.search(keyword)
