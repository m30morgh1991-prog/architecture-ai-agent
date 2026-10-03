"""Before/after detection contract for real architectural edit verification."""
from dataclasses import dataclass
from typing import Any

_ALLOWED={"LOCKED","EDITABLE","CONDITIONAL","UNKNOWN"}
_STATUSES={"PASS","UNKNOWN","NEEDS_REVIEW","BLOCKED"}

@dataclass(frozen=True)
class DetectionSnapshot:
    source_sha256:str
    model_id:str
    elements:tuple[dict[str,Any],...]
    status:str
    def validate(self)->None:
        if not self.source_sha256 or not self.model_id: raise ValueError("DETECTION_IDENTITY_MISSING")
        if self.status not in _STATUSES: raise ValueError("DETECTION_STATUS_INVALID")
        ids=[str(e.get("element_id","")) for e in self.elements]
        if any(not x for x in ids) or len(ids)!=len(set(ids)): raise ValueError("DETECTION_ELEMENT_ID_INVALID")
        for e in self.elements:
            if e.get("state","UNKNOWN") not in _ALLOWED: raise ValueError("DETECTION_ELEMENT_STATE_INVALID")

@dataclass(frozen=True)
class BeforeAfterDetection:
    source_sha256:str
    model_id:str
    added_ids:tuple[str,...]
    removed_ids:tuple[str,...]
    changed_ids:tuple[str,...]
    locked_changed_ids:tuple[str,...]
    unauthorized_changed_ids:tuple[str,...]
    valid:bool
    status:str
    reason:str
    def validate(self)->None:
        if self.status not in _STATUSES: raise ValueError("BEFORE_AFTER_STATUS_INVALID")
        if self.status!="UNKNOWN" and (not self.source_sha256 or not self.model_id): raise ValueError("BEFORE_AFTER_IDENTITY_MISSING")
        if self.valid and self.status!="PASS": raise ValueError("BEFORE_AFTER_PASS_STATUS_MISMATCH")
        if self.status=="PASS" and (self.added_ids or self.removed_ids or self.locked_changed_ids or self.unauthorized_changed_ids): raise ValueError("BEFORE_AFTER_PASS_HAS_BLOCKING_DELTA")
        for name,values in (("changed",self.changed_ids),("added",self.added_ids),("removed",self.removed_ids)):
            if len(set(values))!=len(values): raise ValueError(f"BEFORE_AFTER_{name.upper()}_ID_DUPLICATE")

def _fingerprint(e:dict[str,Any])->tuple:
    return (e.get("element_type"),e.get("state","UNKNOWN"),repr(e.get("geometry")),tuple(e.get("evidence_ids",())))

def compare_before_after(*,before:DetectionSnapshot|None,after:DetectionSnapshot|None,approved_target_ids=())->BeforeAfterDetection:
    if before is None or after is None:
        return BeforeAfterDetection("","",(),(),(),(),(),False,"UNKNOWN","BEFORE_AFTER_DETECTION_MISSING")
    before.validate(); after.validate()
    if before.source_sha256!=after.source_sha256 or before.model_id!=after.model_id:
        return BeforeAfterDetection(before.source_sha256,before.model_id,(),(),(),(),(),False,"BLOCKED","BEFORE_AFTER_IDENTITY_MISMATCH")
    bm={str(e["element_id"]):e for e in before.elements}; am={str(e["element_id"]):e for e in after.elements}
    added=tuple(sorted(set(am)-set(bm))); removed=tuple(sorted(set(bm)-set(am)))
    changed=tuple(sorted(k for k in set(bm)&set(am) if _fingerprint(bm[k])!=_fingerprint(am[k])))
    approved=set(map(str,approved_target_ids))
    locked=tuple(sorted(k for k in changed if bm[k].get("state")=="LOCKED" or am[k].get("state")=="LOCKED"))
    unauthorized=tuple(sorted(k for k in changed if k not in approved))
    valid=not added and not removed and not locked and not unauthorized and after.status=="PASS"
    status="PASS" if valid else ("BLOCKED" if locked or unauthorized or added or removed else "NEEDS_REVIEW")
    reason="Before/after detection matches approved scope." if valid else ("Unauthorized or locked/structural changes detected." if status=="BLOCKED" else "After-state detection requires review.")
    return BeforeAfterDetection(before.source_sha256,before.model_id,added,removed,changed,locked,unauthorized,valid,status,reason)
