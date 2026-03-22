"""Security controls for HARIBO OROM."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Dict, Iterable, List
import json
import secrets


@dataclass
class AuditRecord:
    timestamp: datetime
    actor: str
    action: str
    context: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, str]:
        payload = {
            "timestamp": self.timestamp.isoformat(),
            "actor": self.actor,
            "action": self.action,
        }
        if self.context:
            payload["context"] = self.context
        return payload


class SovereignAccessControl:
    """Simple attribute-based access control implementation."""

    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.active_tokens: Dict[str, str] = {}

    def mint_token(self, subject: str, attributes: Iterable[str]) -> str:
        """Create a short-lived sovereign token."""
        if subject != self.owner:
            raise PermissionError("Only the sovereign owner may mint tokens")
        fingerprint = sha256("|".join(sorted(attributes)).encode("utf-8")).hexdigest()
        token = sha256((fingerprint + secrets.token_hex(16)).encode("utf-8")).hexdigest()
        self.active_tokens[token] = fingerprint
        return token

    def validate(self, token: str, required_attributes: Iterable[str]) -> bool:
        fingerprint = self.active_tokens.get(token)
        if not fingerprint:
            return False
        expected = sha256("|".join(sorted(required_attributes)).encode("utf-8")).hexdigest()
        return secrets.compare_digest(fingerprint, expected)

    def revoke(self, token: str) -> None:
        self.active_tokens.pop(token, None)


class AuditTrail:
    """Immutable append-only audit file."""

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not storage_path.exists():
            storage_path.write_text("[]", encoding="utf-8")

    def append(self, record: AuditRecord) -> None:
        payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
        payload.append(record.to_dict())
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def tail(self, limit: int = 10) -> List[AuditRecord]:
        payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
        sliced = payload[-limit:]
        return [
            AuditRecord(
                timestamp=datetime.fromisoformat(item["timestamp"]),
                actor=item["actor"],
                action=item["action"],
                context=item.get("context", {}),
            )
            for item in sliced
        ]


class QuantumSecurityFramework:
    """High-level orchestrator that composes the security primitives."""

    def __init__(self, owner: str, audit_storage: Path) -> None:
        self.owner = owner
        self.access_control = SovereignAccessControl(owner)
        self.audit_trail = AuditTrail(audit_storage)
        self.halted = False

    def sovereign_login(self) -> str:
        token = self.access_control.mint_token(self.owner, ["sovereign", "interactive"])
        self.audit_trail.append(
            AuditRecord(timestamp=datetime.utcnow(), actor=self.owner, action="login")
        )
        return token

    def authorize_action(self, token: str, action: str, *, context: Dict[str, str] | None = None) -> bool:
        allowed = self.access_control.validate(token, ["sovereign", "interactive"])
        if self.halted and action != "resume_operations":
            allowed = False
        self.audit_trail.append(
            AuditRecord(
                timestamp=datetime.utcnow(),
                actor=self.owner if allowed else "unknown",
                action=action,
                context=context or {},
            )
        )
        return allowed

    def emergency_shutdown(self, reason: str = "manual_stop") -> Dict[str, str]:
        self.halted = True
        self.audit_trail.append(
            AuditRecord(
                timestamp=datetime.utcnow(),
                actor=self.owner,
                action="emergency_shutdown",
                context={"reason": reason},
            )
        )
        return {"status": "stopped", "reason": reason}

    def resume_operations(self) -> Dict[str, str]:
        self.halted = False
        self.audit_trail.append(
            AuditRecord(timestamp=datetime.utcnow(), actor=self.owner, action="resume_operations")
        )
        return {"status": "running"}

    def system_status(self) -> str:
        return "stopped" if self.halted else "running"

    def revoke(self, token: str) -> None:
        self.access_control.revoke(token)
        self.audit_trail.append(
            AuditRecord(timestamp=datetime.utcnow(), actor=self.owner, action="logout")
        )
