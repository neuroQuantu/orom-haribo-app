"""Integration orchestration for connected ecosystems."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class IntegrationStatus:
    target: str
    connected: bool
    detail: str


class IntegrationManager:
    """Simulate connection to heterogeneous integration targets."""

    def __init__(self, targets: List[str]):
        self.targets = targets
        self.status: Dict[str, IntegrationStatus] = {}

    def connect_all(self) -> List[IntegrationStatus]:
        results: List[IntegrationStatus] = []
        for target in self.targets:
            status = IntegrationStatus(
                target=target,
                connected=True,
                detail=f"Canal {target} synchronisé sous clé souveraine",
            )
            self.status[target] = status
            results.append(status)
        return results

    def get_status_report(self) -> List[IntegrationStatus]:
        if not self.status:
            return [
                IntegrationStatus(target=target, connected=False, detail="non initialisé")
                for target in self.targets
            ]
        return list(self.status.values())
