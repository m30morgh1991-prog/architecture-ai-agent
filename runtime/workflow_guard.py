from dataclasses import dataclass
from typing import Any, Dict

from .audit import AuditTrail
from .error_policy import classify
from .idempotency import IdempotencyGuard


@dataclass(frozen=True)
class WorkflowDecision:
    status: str
    state: str
    failure_code: str | None = None


class WorkflowGuard:
    """Provider-neutral workflow gate for execution lifecycle consistency."""

    def __init__(self, audit: AuditTrail | None = None, idempotency: IdempotencyGuard | None = None):
        self.audit = audit or AuditTrail()
        self.idempotency = idempotency or IdempotencyGuard()

    def begin(self, execution_id: str, key: str) -> WorkflowDecision:
        cached = self.idempotency.check(key)
        if cached is not None:
            return cached
        self.audit.record(execution_id, "WORKFLOW", "STARTED", {"idempotency_key": key})
        decision = WorkflowDecision("PASS", "RUNNING")
        self.idempotency.store(key, decision)
        return decision

    def finish(self, execution_id: str, key: str, failure_code: str | None = None) -> WorkflowDecision:
        if failure_code:
            state = "BLOCKED" if classify(failure_code) == "BLOCKING" else "FAILED"
            decision = WorkflowDecision("REJECT" if state == "BLOCKED" else "NEEDS_REVISION", state, failure_code)
        else:
            decision = WorkflowDecision("PASS", "SUCCEEDED")
        # WorkflowDecision statuses are API-level outcomes. AuditTrail uses
        # evidence states, so map non-terminal API labels to their explicit
        # fail-closed audit equivalents rather than recording unsupported values.
        audit_status = {
            "PASS": "PASS",
            "REJECT": "BLOCKED",
            "NEEDS_REVISION": "NEEDS_REVIEW",
        }[decision.status]
        self.audit.record(
            execution_id,
            "WORKFLOW",
            audit_status,
            {"state": decision.state, "failure_code": failure_code},
        )

        self.idempotency.store(key, decision)
        return decision

    def trace(self, execution_id: str) -> list[Any]:
        return self.audit.events(execution_id)
