"""CLI helper to initialize the HARIBO OROM Quantum Ethique system."""
from __future__ import annotations

from pathlib import Path

from haribo_orom import HariboQuantumSystem
from haribo_orom.config import discover_config


def main() -> None:
    config = discover_config([Path(__file__).parent / "configs" / "haribo_config.json"])
    system = HariboQuantumSystem(config)
    state = system.initialize_system()
    print("=== HARIBO OROM Quantum Ethique ===")
    print(f"Propriétaire: {state.owner}")
    print(f"Synthèse des connaissances: {state.knowledge_summary}")
    print("Intégrations synchronisées:")
    for target, detail in state.integrations.items():
        print(f"- {target}: {detail}")

    print("\nLimites éthiques opérationnelles:")
    for key, value in state.ethical_limits.items():
        print(f"- {key}: {value}")

    print("\nDimensions surveillées:")
    for report in state.dimension_reports:
        indicators = ", ".join(
            f"{name}={count}" for name, count in report.indicators.items()
        ) or "aucune donnée"
        print(f"- {report.name} ({report.status}) → {indicators}")

    print("\nSynthèse du codex souverain:")
    for section_name, lines in (
        ("Architecture", state.codex_summary.architecture),
        ("Sécurité", state.codex_summary.securite),
        ("Connaissances", state.codex_summary.connaissances),
        ("Interfaces", state.codex_summary.interfaces),
    ):
        print(f"* {section_name}:")
        for line in lines:
            print(f"  - {line}")

    board = state.oversight.transparency_features
    print("\nSupervision temps réel:")
    print(f"- Synthèse: {board.get('knowledge_summary', 'n/a')}")
    integrations = board.get("integrations", {})
    if integrations:
        print("- Intégrations observées:")
        for target, detail in integrations.items():
            print(f"  - {target}: {detail}")
    dimensions = board.get("dimensions", [])
    if dimensions:
        print("- Dimensions suivies:")
        for dimension in dimensions:
            indicators = ", ".join(
                f"{name}={count}" for name, count in dimension.get("indicators", {}).items()
            )
            print(
                f"  - {dimension.get('name')} ({dimension.get('status')}): {indicators}"
            )
    print("- Protocoles d'intervention:")
    for protocol in state.oversight.intervention_protocols:
        print(f"  - {protocol}")
    print("- Audits récents:")
    if state.oversight.recent_audit_events:
        for event in state.oversight.recent_audit_events:
            print(f"  - {event}")
    else:
        print("  - Aucun événement enregistré")

    print("\nRegistre technologique universel:")
    for categorie, items in state.technology_registry.items():
        print(f"- {categorie}: {len(items)} éléments")

    print("\nPosture de sécurité:")
    for key, value in state.security_posture.items():
        print(f"- {key}: {value}")

    entity = state.sovereign_entity
    print("\nEntité technologique fusionnée:")
    print(
        f"- {entity.nom} · propriétaire={entity.proprietaire} · niveau={entity.niveau_evolution}"
    )
    print(f"- Capacités: {', '.join(entity.capacites)}")

    print("\nRéseau universel:")
    for canal, connexions in state.network_map.items():
        print(f"- {canal}: {', '.join(connexions)}")

    print("\nCommandes souveraines disponibles:")
    for commande in state.commands:
        print(f"- {commande}")

    print("\nRapport avatar:")
    print(system.avatar_report())


if __name__ == "__main__":
    main()
