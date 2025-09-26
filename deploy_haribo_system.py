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
    print("Intégrations:")
    for target, detail in state.integrations.items():
        print(f"- {target}: {detail}")
    print("\nRapport avatar:")
    print(system.avatar_report())


if __name__ == "__main__":
    main()
