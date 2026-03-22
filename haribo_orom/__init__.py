"""HARIBO OROM Quantum Ethique package.

This package provides a runnable reference implementation of the sovereign
HARIBO OROM architecture.  The modules intentionally avoid external
dependencies so the system can be executed on a vanilla Python interpreter.
"""

from .core import HariboQuantumSystem
from .multidimensional_detector import MultidimensionalDetector
from .sovereignty import (
    BaseConnaissanceUniverselle,
    CodexIntegrateurUniversel,
    CommandesMaitres,
    DetecteurMultidimensionnel,
    EthicalPrinciples,
    EthicalGuarantees,
    GestionnaireTechnologiesUniverselles,
    HariboQuantumCoreManifest,
    IntegrateurUniversel,
    MasterOversightSystem,
    NoyauQuantiqueUniversel,
    ReseauUniverselHaribo,
    SecuriteSouveraineAbsolue,
)

__all__ = [
    "HariboQuantumSystem",
    "MultidimensionalDetector",
    "BaseConnaissanceUniverselle",
    "CodexIntegrateurUniversel",
    "CommandesMaitres",
    "DetecteurMultidimensionnel",
    "EthicalPrinciples",
    "EthicalGuarantees",
    "GestionnaireTechnologiesUniverselles",
    "HariboQuantumCoreManifest",
    "IntegrateurUniversel",
    "MasterOversightSystem",
    "NoyauQuantiqueUniversel",
    "ReseauUniverselHaribo",
    "SecuriteSouveraineAbsolue",
]
