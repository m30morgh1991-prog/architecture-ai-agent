from dataclasses import dataclass
from typing import Any

_ALLOWED_STATUSES = {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}

@dataclass(frozen=True)
class AuditEvent:
    execution_id: str
    stage: str
    status: str
    details: dict[str, Any]

class AuditTrail:
    def __init__(self):
        self._events = []

    def record(self, execution_id, stage, status, details=None):
        if not execution_id:
            raise ValueError("AUDIT_EXECUTION_ID_MISSING")
        if not stage:
            raise ValueError("AUDIT_STAGE_MISSING")
        if status not in _ALLOWED_STATUSES:
            raise ValueError("AUDIT_STATUS_INVALID")
        event = AuditEvent(execution_id, stage, status, details or {})
        self._events.append(event)
        return event

    def events(self, execution_id):
        return [e for e in self._events if e.execution_id == execution_id]

    def is_complete(self, execution_id, required_stages):
        if not execution_id or not required_stages:
            return False
        events = self.events(execution_id)
        seen = {event.stage: event for event in events}
        return all(stage in seen and seen[stage].status == "PASS" for stage in required_stages)
