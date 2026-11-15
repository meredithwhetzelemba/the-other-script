"""Simple audit trail — same idea as homework harness logs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
AUDIT_PATH = ROOT / "output" / "audit_trail.json"


class AuditLogger:
    def __init__(self, path: Path = AUDIT_PATH) -> None:
        self.path = path
        self.events: list[dict[str, Any]] = []
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, kind: str, payload: dict[str, Any] | None = None) -> None:
        self.events.append(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "kind": kind,
                "payload": payload or {},
            }
        )

    def flush(self) -> Path:
        self.path.write_text(
            json.dumps({"events": self.events}, indent=2),
            encoding="utf-8",
        )
        return self.path
