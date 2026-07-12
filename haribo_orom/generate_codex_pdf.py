"""Generate a signed PDF containing the HARIBO manifest and detector state."""

from __future__ import annotations

from datetime import datetime
import hashlib
import importlib
import json
from typing import Any


class CodexPDFGenerator:
    """Create the sovereign HARIBO PDF codex with a SHA-256 fingerprint."""

    def __init__(self, proprietaire: str, imza: str) -> None:
        self.proprietaire = proprietaire
        self.imza = imza

    def creer_pdf(
        self, detector_data: dict[str, Any], chemin: str = "CODEX_SOUVERAIN_HARIBO.pdf"
    ) -> str:
        fpdf = importlib.import_module("fpdf")
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "CODEX SOUVERAIN HARIBO OROM", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Propriétaire: {self.proprietaire}", ln=True)
        pdf.cell(0, 10, f"Date: {datetime.now().isoformat()}", ln=True)
        pdf.cell(0, 10, f"Signature: {self.imza[:32]}...", ln=True)
        pdf.ln(5)
        pdf.cell(0, 10, "État des dimensions:", ln=True)
        for dim, data in detector_data.items():
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, dim.capitalize(), ln=True)
            pdf.set_font("Arial", "", 10)
            for key, val in data.items():
                pdf.cell(0, 6, f"  {key}: {val}", ln=True)
        pdf.ln(10)
        content = json.dumps(detector_data, sort_keys=True, default=str)
        fingerprint = hashlib.sha256(content.encode("utf-8")).hexdigest()
        pdf.cell(0, 10, f"Empreinte SHA-256: {fingerprint}", ln=True)
        pdf.output(chemin)
        print(f"[Codex PDF] Document généré: {chemin}")
        return chemin
