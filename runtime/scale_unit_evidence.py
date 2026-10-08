"""Deterministic scale/unit evidence contract for architectural plan edits."""
from dataclasses import dataclass

_ALLOWED_UNITS={"MM","CM","M","IN","FT","UNKNOWN"}
_VERIFIED_UNITS=_ALLOWED_UNITS-{"UNKNOWN"}

def _normalize_unit(value):
    if not isinstance(value,str):
        return None
    normalized=value.strip().upper()
    return normalized if normalized in _VERIFIED_UNITS else None

def _signal_present(value):
    if isinstance(value,str) and value.strip().upper()=="UNKNOWN":
        return False
    return bool(value)

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
        if self.status=="PASS" and (
            not self.scale_known or self.confidence<0.95 or self.unit=="UNKNOWN"
        ):
            raise ValueError("SCALE_PASS_REQUIRES_VERIFIED_SCALE_AND_UNIT")

def evaluate_scale_evidence(*,source_id,unit,explicit_unit,header_unit,dimension_evidence,source_metadata,evidence_ids):
    signals=[explicit_unit,header_unit,dimension_evidence,source_metadata]
    present=sum(_signal_present(x) for x in signals)
    explicit_value=_normalize_unit(explicit_unit)
    header_value=_normalize_unit(header_unit)
    base_value=_normalize_unit(unit)

    if explicit_value and header_value and explicit_value != header_value:
        result=ScaleEvidence(source_id,"UNKNOWN",False,0.0,evidence_ids,"BLOCKED")
    else:
        resolved=explicit_value or header_value or base_value or "UNKNOWN"
        if present>=2 and resolved!="UNKNOWN":
            result=ScaleEvidence(source_id,resolved,True,0.95,evidence_ids,"PASS")
        elif present>=1:
            result=ScaleEvidence(source_id,resolved,False,0.0,evidence_ids,"NEEDS_REVIEW")
        else:
            result=ScaleEvidence(source_id,"UNKNOWN",False,0.0,evidence_ids,"UNKNOWN")
    result.validate()
    return result
