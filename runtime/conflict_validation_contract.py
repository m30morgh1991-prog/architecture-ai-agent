"""H23 deterministic conflict and validation result contract."""
from dataclasses import dataclass, field
from typing import List


CONFLICT_SEVERITIES = {"INFO", "WARNING", "BLOCKING"}
VALIDATION_STATES = {"PASS", "NEEDS_REVISION", "REJECT", "BLOCKED", "UNKNOWN"}


@dataclass(frozen=True)
class Conflict:
    conflict_id: str
    code: str
    severity: str
    affected_elements: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.conflict_id or not self.code:
            raise ValueError("CONFLICT_TRACEABILITY_MISSING")
        if self.severity not in CONFLICT_SEVERITIES:
            raise ValueError("CONFLICT_SEVERITY_INVALID")


@dataclass(frozen=True)
class ValidationResult:
    validation_id: str
    state: str
    conflicts: List[Conflict] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.validation_id:
            raise ValueError("VALIDATION_TRACEABILITY_MISSING")
        if self.state not in VALIDATION_STATES:
            raise ValueError("VALIDATION_STATE_INVALID")
        for conflict in self.conflicts:
            conflict.validate()

    @property
    def executable(self) -> bool:
        self.validate()
        return self.state == "PASS" and not any(
            c.severity == "BLOCKING" for c in self.conflicts
        )
