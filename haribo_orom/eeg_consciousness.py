"""EEG consciousness scanner integration for BrainFlow-compatible devices."""

from __future__ import annotations

from datetime import datetime
import importlib
import importlib.util
import time
from typing import Any


class EEGConsciousnessScanner:
    """Read a short alpha-band coherence sample from BrainFlow.

    The scanner degrades gracefully when BrainFlow or NumPy are not installed so
    the rest of the HARIBO system remains runnable in lightweight environments.
    """

    def __init__(
        self, serial_port: str | None = None, board_id: Any | None = None
    ) -> None:
        self.serial_port = serial_port
        self.board_id = board_id
        self.params: Any | None = None
        self.board: Any | None = None
        self.sampling_rate: int | None = None
        self.connected = False
        self._brainflow_available = importlib.util.find_spec("brainflow") is not None

    def _default_board_id(self) -> Any:
        board_shim = importlib.import_module("brainflow.board_shim")
        return board_shim.BoardIds.SYNTHETIC_BOARD

    def connecter(self) -> bool:
        """Connect to the EEG board and start streaming."""
        if not self._brainflow_available:
            self.connected = False
            return False
        board_shim = importlib.import_module("brainflow.board_shim")
        BoardShim = board_shim.BoardShim
        BrainFlowInputParams = board_shim.BrainFlowInputParams
        self.board_id = (
            self.board_id if self.board_id is not None else self._default_board_id()
        )
        self.params = BrainFlowInputParams()
        if self.serial_port:
            self.params.serial_port = self.serial_port
        try:
            self.board = BoardShim(self.board_id, self.params)
            self.board.prepare_session()
            self.board.start_stream()
            self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
            self.connected = True
        except (
            Exception
        ) as exc:  # hardware connection errors are expected in dev environments
            print(f"[EEG] Impossible de se connecter : {exc}")
            self.connected = False
        return self.connected

    def lire_ondes(self, duree_secondes: float = 2.0) -> dict[str, Any] | None:
        """Read EEG data and return a simple alpha-band coherence score."""
        if not self.connected or self.board is None or self.sampling_rate is None:
            return None
        time.sleep(duree_secondes)
        board_shim = importlib.import_module("brainflow.board_shim")
        data_filter = importlib.import_module("brainflow.data_filter")
        np = importlib.import_module("numpy")
        BoardShim = board_shim.BoardShim
        DataFilter = data_filter.DataFilter
        FilterTypes = data_filter.FilterTypes
        DetrendOperations = data_filter.DetrendOperations
        data = self.board.get_current_board_data(
            int(self.sampling_rate * duree_secondes)
        )
        self.board.stop_stream()
        self.board.release_session()
        self.connected = False
        eeg_channels = BoardShim.get_eeg_channels(self.board_id)
        if not eeg_channels:
            return {"erreur": "Aucun canal EEG", "coherence": 0.0}
        signal = data[eeg_channels[0]]
        DataFilter.detrend(signal, DetrendOperations.CONSTANT.value)
        DataFilter.perform_bandpass(
            signal,
            self.sampling_rate,
            8.0,
            12.0,
            2,
            FilterTypes.BUTTERWORTH.value,
            0,
        )
        alpha_power = float(np.mean(np.abs(signal)))
        return {
            "alpha_power": alpha_power,
            "coherence": min(0.99, alpha_power / 100.0),
            "timestamp": datetime.now().isoformat(),
        }

    def scan(self) -> dict[str, Any]:
        """Standard scanner interface used by the multidimensional detector."""
        if not self.connected:
            self.connecter()
        if self.connected:
            data = self.lire_ondes()
            return data or {
                "status": "lecture vide",
                "coherence": 0.0,
                "timestamp": datetime.now().isoformat(),
            }
        return {
            "status": "non connecté",
            "coherence": 0.0,
            "timestamp": datetime.now().isoformat(),
        }


def scan_consciousness_realm() -> dict[str, Any]:
    """Return a consciousness-realm status derived from the EEG scanner."""
    data = EEGConsciousnessScanner().scan()
    coherence = float(data.get("coherence", 0.0))
    return {
        "status": "active" if coherence > 0.7 else "faible",
        "presence": (
            "Ibrahim Sakarya détecté" if coherence > 0.7 else "présence non confirmée"
        ),
        "coherence": coherence,
        "timestamp": data.get("timestamp", datetime.now().isoformat()),
    }
