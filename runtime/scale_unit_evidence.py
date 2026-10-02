"""Deterministic scale/unit evidence contract for architectural plan edits."""
from dataclasses import dataclass

_ALLOWED_UNITS={"MM","CM","M","IN","FT","UNKNOWN"}

@dataclass(frozen=True)
class ScaleEvidence:
    source_id:str
    unit:str
    scale_known:bool
    confidence:float
    evidence_ids:tuple[str,...]
    status:str

    def validate(self):
        if not self.source_id or self.unit not in _ALLOWED_UNITS:
            raise ValueError("SCALE_EVIDENCE_INVALID")
        if not 0 <= self.confidence <= 1:
            raise ValueError("SCALE_CONFIDENCE_INVALID")
        if not self.evidence_ids:
            raise ValueError("SCALE_EVIDENCE_MISSING")
        if self.status not in {"PASS","UNKNOWN","BLOCKED","NEEDS_REVIEW"}:
            raise ValueError("SCALE_STATUS_INVALID")
        if self.status=="PASS" and (not self.scale_known or self.confidence<0.95):
            raise ValueError("SCALE_PASS_REQUIRES_VERIFIED_SCALE")

def evaluate_scale_evidence(*,source_id,unit,explicit_unit,header_unit,dimension_evidence,source_metadata,evidence_ids):
    signals=[explicit_unit,header_unit,dimension_evidence,source_metadata]
    present=sum(bool(x) for x in signals)
    if explicit_unit and header_unit and explicit_unit != header_unit:
        r=ScaleEvidence(source_id,"UNKNOWN",False,0.0,evidence_ids,"BLOCKED")
    elif present>=2:
        resolved=explicit_unit or header_unit or unit
        r=ScaleEvidence(source_id,resolved if resolved in _ALLOWED_UNITS else "UNKNOWN",True,0.95,evidence_ids,"PASS")
    elif present==1:
        resolved=explicit_unit or header_unit or unit
        r=ScaleEvidence(source_id,resolved if resolved in _ALLOWED_UNITS else "UNKNOWN",False,0.0,evidence_ids,"NEEDS_REVIEW")
    else:
        r=ScaleEvidence(source_id,"UNKNOWN",False,0.0,evidence_ids,"UNKNOWN")
    r.validate()
    return r
