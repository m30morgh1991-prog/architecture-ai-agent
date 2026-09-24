"""H29 evidence harness for real visual runtime.

It validates presence and ordering of evidence; it never fabricates source artifacts.
"""
from dataclasses import dataclass
from typing import List

REQUIRED_STAGES=[
    "SOURCE","DETECTION","PLAN_MODEL","CONSTRAINT_MAP","LOCKED_IDENTIFICATION",
    "CHANGE_REQUEST","APPROVED_CHANGE_PLAN","CONTROLLED_EDIT",
    "POST_EDIT_DETECTION","POST_EDIT_DIFF","FINAL_VALIDATION"
]

@dataclass(frozen=True)
class VisualEvidence:
    evidence_id:str
    input_type:str
    stages:List[str]

    def validate(self)->None:
        if not self.evidence_id:
            raise ValueError("VISUAL_EVIDENCE_ID_MISSING")
        if self.input_type not in {"JPG","PNG","WEBP","PDF"}:
            raise ValueError("UNSUPPORTED_VISUAL_INPUT")
        if self.stages != [s for s in REQUIRED_STAGES if s in self.stages]:
            raise ValueError("VISUAL_STAGE_ORDER_INVALID")

    @property
    def complete(self)->bool:
        self.validate()
        return self.stages == REQUIRED_STAGES
