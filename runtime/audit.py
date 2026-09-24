from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class AuditEvent:
    execution_id: str
    stage: str
    status: str
    details: dict[str, Any]

class AuditTrail:
    def __init__(self): self._events=[]
    def record(self, execution_id, stage, status, details=None):
        self._events.append(AuditEvent(execution_id,stage,status,details or {})); return self._events[-1]
    def events(self, execution_id): return [e for e in self._events if e.execution_id==execution_id]
