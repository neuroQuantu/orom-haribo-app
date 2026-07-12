"""Magnetic-field scanner for serial QMC5883L-style sensor frames."""

from __future__ import annotations

from datetime import datetime
import importlib
import importlib.util
from typing import Any


class EnergyScanner:
    """Read simple ``X,Y,Z`` microtesla frames from a serial device."""

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200) -> None:
        self.port = port
        self.baudrate = baudrate
        self.ser: Any | None = None
        self._serial_available = importlib.util.find_spec("serial") is not None

    def connect(self) -> bool:
        if not self._serial_available:
            return False
        serial = importlib.import_module("serial")
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"[Énergie] Connecté au capteur sur {self.port}")
        except Exception as exc:  # serial hardware may be absent
            print(f"[Énergie] Erreur connexion : {exc}")
            self.ser = None
        return self.ser is not None

    def read_sensor(self) -> dict[str, Any] | None:
        """Read one ``X,Y,Z`` line and compute the vector magnitude."""
        if not self.ser:
            return None
        self.ser.write(b"R")
        line = self.ser.readline().decode(errors="ignore").strip()
        parts = line.split(",")
        if len(parts) != 3:
            return None
        x, y, z = map(float, parts)
        magnitude = (x**2 + y**2 + z**2) ** 0.5
        return {
            "x_uT": x,
            "y_uT": y,
            "z_uT": z,
            "magnitude_uT": magnitude,
            "timestamp": datetime.now().isoformat(),
        }

    def scan(self) -> dict[str, Any]:
        """Standard scanner interface used by the multidimensional detector."""
        if not self.ser:
            self.connect()
        if self.ser:
            data = self.read_sensor()
            if data:
                spikes = [data] if data["magnitude_uT"] > 100 else []
                return {
                    "status": "normal" if not spikes else "perturbé",
                    "background_level": f"{data['magnitude_uT']:.2f} µT",
                    "spikes": spikes,
                    "timestamp": data["timestamp"],
                }
        return {
            "status": "indisponible",
            "background_level": "0 µT",
            "spikes": [],
            "timestamp": datetime.now().isoformat(),
        }
