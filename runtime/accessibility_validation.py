"""H27 accessibility validation gate contract."""
from dataclasses import dataclass

ACCESSIBILITY_STATES={"ACCESSIBLE","PARTIALLY_ACCESSIBLE","BLOCKED","UNKNOWN","NOT_APPLICABLE"}

@dataclass(frozen=True)
class AccessibilityResult:
    check_id:str
    state:str
    critical:bool=True
    evidence_id:str=""

    def validate(self)->None:
        if not self.check_id:
            raise ValueError("ACCESSIBILITY_TRACEABILITY_MISSING")
        if self.state not in ACCESSIBILITY_STATES:
            raise ValueError("ACCESSIBILITY_STATE_INVALID")
        if self.state!="NOT_APPLICABLE" and not self.evidence_id:
            raise ValueError("ACCESSIBILITY_EVIDENCE_MISSING")

    @property
    def passes_gate(self)->bool:
        self.validate()
        return self.state in {"ACCESSIBLE","NOT_APPLICABLE"}
