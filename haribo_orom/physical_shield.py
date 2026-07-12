"""Physical shield based on camera face detection."""

from __future__ import annotations

import importlib
import importlib.util
import os
from pathlib import Path
import time
from typing import Any


class PhysicalShield:
    """Monitor a webcam for unknown faces and optionally lock the workstation."""

    def __init__(
        self, reference_image_path: str = "ibrahim_ref.jpg", *, dry_run: bool = True
    ) -> None:
        self.ref_path = Path(reference_image_path)
        self.dry_run = dry_run
        self.ref_face_encodings: Any | None = None
        self.cap: Any | None = None
        self.verrou_actif = False
        self._cv2_available = importlib.util.find_spec("cv2") is not None
        self.face_cascade: Any | None = None
        if self._cv2_available:
            cv2 = importlib.import_module("cv2")
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

    def charger_reference(self) -> None:
        """Load the owner reference face using OpenCV Haar cascades."""
        if (
            not self._cv2_available
            or self.face_cascade is None
            or not self.ref_path.exists()
        ):
            return
        cv2 = importlib.import_module("cv2")
        img = cv2.imread(str(self.ref_path))
        if img is None:
            return
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            self.ref_face_encodings = gray[y : y + h, x : x + w]

    def _lock_screen(self) -> None:
        if self.dry_run:
            print("[Bouclier] Verrouillage simulé (dry-run).")
            return
        if os.name == "posix":
            os.system("loginctl lock-session || gnome-screensaver-command -l")
        elif os.name == "nt":
            ctypes = importlib.import_module("ctypes")
            ctypes.windll.user32.LockWorkStation()

    def demarrer_surveillance(self) -> None:
        """Start continuous webcam surveillance until the camera stream ends."""
        if not self._cv2_available or self.face_cascade is None:
            print("[Bouclier] OpenCV indisponible.")
            return
        cv2 = importlib.import_module("cv2")
        self.cap = cv2.VideoCapture(0)
        self.charger_reference()
        print("[Bouclier] Surveillance physique activée.")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            owner_present = False
            for x, y, w, h in faces:
                if self.ref_face_encodings is None:
                    continue
                face = gray[y : y + h, x : x + w]
                resized = cv2.resize(
                    face,
                    (
                        self.ref_face_encodings.shape[1],
                        self.ref_face_encodings.shape[0],
                    ),
                )
                corr = cv2.matchTemplate(
                    resized, self.ref_face_encodings, cv2.TM_CCOEFF_NORMED
                )[0][0]
                if corr > 0.5:
                    owner_present = True
                    break
            if not owner_present and len(faces) > 0 and not self.verrou_actif:
                print("[Bouclier] Intrusion potentielle détectée.")
                self.verrou_actif = True
                self._lock_screen()
            elif owner_present and self.verrou_actif:
                print("[Bouclier] Propriétaire reconnu.")
                self.verrou_actif = False
            time.sleep(1)
        self.cap.release()
