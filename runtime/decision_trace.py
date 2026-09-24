"""H25 traceable controlled-editing decision record."""
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(frozen=True)
class DecisionTrace:
    decision_id: str
    execution_id: str
    action: str
    outcome: str
    evidence_ids: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.decision_id or not self.execution_id or not self.action:
            raise ValueError("DECISION_TRACEABILITY_MISSING")
        if not self.outcome:
            raise ValueError("DECISION_OUTCOME_MISSING")

    def as_audit_event(self) -> Dict[str, object]:
        self.validate()
        return {"decision_id":self.decision_id,"execution_id":self.execution_id,
                "action":self.action,"outcome":self.outcome,
                "evidence_ids":list(self.evidence_ids),"reasons":list(self.reasons),
                "metadata":dict(self.metadata)}
