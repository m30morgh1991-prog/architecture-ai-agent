"""H28 real visual runtime readiness gate.

Readiness is not a visual PASS. Missing evidence produces BLOCKED.
"""
from dataclasses import dataclass, field
from typing import List

VISUAL_BLOCKERS={
    "VISUAL_ADAPTER_UNSELECTED","SOURCE_DOCUMENT_MISSING","DETECTION_UNCERTAIN",
    "SCALE_UNKNOWN","LOCKED_ELEMENT_UNCERTAIN","EDITOR_GUARD_UNVERIFIED",
    "POST_EDIT_DETECTION_MISSING"
}

@dataclass(frozen=True)
class VisualRuntimeReadiness:
    input_type:str
    evidence_ids:List[str]=field(default_factory=list)
    blockers:List[str]=field(default_factory=list)

    def validate(self)->None:
        if self.input_type not in {"JPG","PNG","WEBP","PDF"}:
            raise ValueError("UNSUPPORTED_VISUAL_INPUT")
        invalid=set(self.blockers)-VISUAL_BLOCKERS
        if invalid:
            raise ValueError("UNKNOWN_VISUAL_BLOCKER")

    @property
    def ready(self)->bool:
        self.validate()
        return bool(self.evidence_ids) and not self.blockers
