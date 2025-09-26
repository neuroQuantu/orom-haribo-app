"""HARIBO OROM Quantum Ethique package.

This package provides a runnable reference implementation of the sovereign
HARIBO OROM architecture.  The modules intentionally avoid external
dependencies so the system can be executed on a vanilla Python interpreter.
"""

from .core import HariboQuantumSystem

__all__ = ["HariboQuantumSystem"]
