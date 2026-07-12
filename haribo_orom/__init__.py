"""HARIBO OROM Quantum Ethique package.

This package provides a runnable reference implementation of the sovereign
HARIBO OROM architecture.  The modules intentionally avoid external
dependencies so the system can be executed on a vanilla Python interpreter.
"""

from .core import HariboQuantumSystem
from .eeg_consciousness import EEGConsciousnessScanner
from .energy_scanner import EnergyScanner
from .generate_codex_pdf import CodexPDFGenerator
from .local_llm import LLMLocal
from .physical_shield import PhysicalShield

__all__ = [
    "HariboQuantumSystem",
    "EEGConsciousnessScanner",
    "EnergyScanner",
    "CodexPDFGenerator",
    "LLMLocal",
    "PhysicalShield",
]
