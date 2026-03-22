"""Simulation-oriented multidimensional detector primitives."""
from __future__ import annotations

from datetime import datetime, timezone
import random
from typing import Dict, List, Mapping


class MultidimensionalDetector:
    """Deterministic-friendly detector that can be replaced by real sensors later."""

    def __init__(self, owner: str, dimensions: List[str] | None = None, *, seed: int = 42) -> None:
        self.owner = owner
        self.active_dimensions = dimensions or ["physique", "quantique", "conscience"]
        self.last_scan: Dict[str, Dict[str, object]] | None = None
        self._random = random.Random(seed)

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()

    def scan_physical_realm(self) -> Dict[str, object]:
        return {
            "status": "stable",
            "anomalies": [],
            "timestamp": self._timestamp(),
            "devices_detected": ["ordinateur", "smartphone", "réseau local"],
        }

    def scan_quantum_realm(self) -> Dict[str, object]:
        return {
            "status": "coherent",
            "superposition_states": self._random.randint(10, 100),
            "entanglement_pairs": self._random.randint(5, 50),
            "timestamp": self._timestamp(),
        }

    def scan_energy_realm(self) -> Dict[str, object]:
        return {
            "status": "normal",
            "background_level": "0.23 µT",
            "spikes": [],
            "timestamp": self._timestamp(),
        }

    def scan_consciousness_realm(self) -> Dict[str, object]:
        return {
            "status": "active",
            "presence": f"{self.owner} détecté",
            "coherence": 0.92,
            "timestamp": self._timestamp(),
        }

    def scan_dimensions(self) -> Dict[str, Dict[str, object]]:
        scan = {
            "physique": self.scan_physical_realm(),
            "quantique": self.scan_quantum_realm(),
            "energetique": self.scan_energy_realm(),
            "conscience": self.scan_consciousness_realm(),
        }
        self.last_scan = scan
        return scan

    def detect_threats(self) -> List[str]:
        if self.last_scan is None:
            self.scan_dimensions()
        assert self.last_scan is not None
        threats: List[str] = []
        if self.last_scan["physique"].get("anomalies"):
            threats.append("Anomalie physique détectée")
        if self.last_scan["energetique"].get("spikes"):
            threats.append("Pic énergétique inhabituel")
        return threats

    def get_active_dimensions(self) -> List[str]:
        return list(self.active_dimensions)

    def to_presence_matrix(self, scan: Mapping[str, Mapping[str, object]]) -> Dict[str, Dict[str, int]]:
        return {
            dimension: {
                "signals": sum(
                    1
                    for value in payload.values()
                    if value not in (None, "", [], {}, 0)
                )
            }
            for dimension, payload in scan.items()
        }
