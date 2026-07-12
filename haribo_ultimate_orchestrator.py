"""Ultimate CLI orchestrator for optional HARIBO sensors and interfaces."""

from __future__ import annotations

import argparse
import hashlib
import threading
from datetime import datetime
from typing import Any

from haribo_orom import HariboQuantumSystem
from haribo_orom.eeg_consciousness import EEGConsciousnessScanner
from haribo_orom.energy_scanner import EnergyScanner
from haribo_orom.generate_codex_pdf import CodexPDFGenerator
from haribo_orom.local_llm import LLMLocal
from haribo_orom.physical_shield import PhysicalShield


class MultidimensionalDetector:
    """Aggregate optional physical and consciousness scanners."""

    def __init__(self, *, eeg: bool = False, energy: bool = False) -> None:
        self.eeg = EEGConsciousnessScanner() if eeg else None
        self.energy = EnergyScanner() if energy else None

    def scan_dimensions(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "system": {"status": "active", "timestamp": datetime.now().isoformat()}
        }
        if self.eeg:
            payload["consciousness"] = self.eeg.scan()
        if self.energy:
            payload["energy"] = self.energy.scan()
        return payload


class CodexIntegrateurUniversel:
    """Compose the core HARIBO system with optional sensor, LLM and PDF features."""

    def __init__(self, config: dict[str, bool]) -> None:
        self.system = HariboQuantumSystem()
        self.detector = MultidimensionalDetector(
            eeg=config.get("eeg", False), energy=config.get("energy", False)
        )
        self.shield = PhysicalShield() if config.get("shield", False) else None
        self.llm = LLMLocal() if config.get("llm", False) else None
        self.imza = hashlib.sha256(
            self.system.config.system.owner.encode("utf-8")
        ).hexdigest()
        self.pdfgen = CodexPDFGenerator(self.system.config.system.owner, self.imza)

    def isle(self, metin: str) -> str:
        """Handle high-level French/Turkish operator commands."""
        if "génère codex" in metin.lower() or "genere codex" in metin.lower():
            scan_data = self.detector.scan_dimensions()
            path = self.pdfgen.creer_pdf(scan_data)
            return f"Codex souverain généré : {path}"
        if self.llm:
            return self.llm.dialogue(metin)
        return self.system.avatar_report()

    def start_background_services(self, *, hologram: bool = False) -> None:
        if self.shield:
            threading.Thread(
                target=self.shield.demarrer_surveillance, daemon=True
            ).start()
        if hologram:
            from haribo_orom.holographic_interface import lancer_serveur

            threading.Thread(
                target=lancer_serveur, args=(self.detector, 5000), daemon=True
            ).start()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HARIBO OROM ultimate orchestrator")
    parser.add_argument(
        "--eeg", action="store_true", help="Enable BrainFlow EEG scanning"
    )
    parser.add_argument(
        "--energy", action="store_true", help="Enable serial magnetic energy scanning"
    )
    parser.add_argument(
        "--shield",
        action="store_true",
        help="Enable physical camera shield in dry-run mode",
    )
    parser.add_argument(
        "--llm", action="store_true", help="Enable local Ollama dialogue"
    )
    parser.add_argument(
        "--hologram",
        action="store_true",
        help="Enable Flask-SocketIO holographic dashboard",
    )
    parser.add_argument(
        "--command", default="rapport", help="Command to execute once at startup"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    integrateur = CodexIntegrateurUniversel(vars(args))
    integrateur.start_background_services(hologram=args.hologram)
    print(integrateur.isle(args.command))


if __name__ == "__main__":
    main()
