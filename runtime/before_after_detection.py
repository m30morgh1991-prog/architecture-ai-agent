"""Before/after detection contract for real architectural edit verification.

The detector comparison is identity- and evidence-aware. Missing after-state data
never becomes PASS; source/model identity must match before/after.
"""
from dataclasses import dataclass
from typing import Any

_ALLOWED = {"LOCKED", "EDITABLE", "CONDITIONAL", "UNKNOWN"}

@dataclass(frozen=True)
class DetectionSnapshot:
    source_sha256: str
    model_id: str
    elements: tuple[dict[str, Any], ...]
    status: str

    def validate(self) -> None:
        if not self.source_sha256 or not self.model_id:
            raise ValueError("DETECTION_IDENTITY_MISSING")
        if self.status not in {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}:
            raise ValueError("DETECTION_STATUS_INVALID")
        ids = [str(e.get("element_id", "")) for e in self.elements]
        if any(not x for x in ids) or len(ids) != len(set(ids)):
            raise ValueError("DETECTION_ELEMENT_ID_INVALID")
        for e in self.elements:
            if e.get("state", "UNKNOWN") not in _ALLOWED:
                raise ValueError("DETECTION_ELEMENT_STATE_INVALID")

@dataclass(frozen=True)
class BeforeAfterDetection:
    source_sha256: str
    model_id: str
    added_ids: tuple[str, ...]
    removed_ids: tuple[str, ...]
    changed_ids: tuple[str, ...]
    locked_changed_ids: tuple[str, ...]
    unauthorized_changed_ids: tuple[str, ...]
    valid: bool
    status: str
    reason: str

def _fingerprint(e: dict[str, Any]) -> tuple:
    return (
        e.get("element_type"),
        e.get("state", "UNKNOWN"),
        repr(e.get("geometry")),
        tuple(e.get("evidence_ids", ())),
    )

def compare_before_after(*, before: DetectionSnapshot | None,
                         after: DetectionSnapshot | None,
                         approved_target_ids=()) -> BeforeAfterDetection:
    if before is None or after is None:
        return BeforeAfterDetection("", "", (), (), (), (), (), False,
                                    "UNKNOWN", "BEFORE_AFTER_DETECTION_MISSING")
    before.validate()
    after.validate()
    if before.source_sha256 != after.source_sha256 or before.model_id != after.model_id:
        return BeforeAfterDetection(before.source_sha256, before.model_id, (), (), (), (), (), False,
                                    "BLOCKED", "BEFORE_AFTER_IDENTITY_MISMATCH")
    bm = {str(e["element_id"]): e for e in before.elements}
    am = {str(e["element_id"]): e for e in after.elements}
    added = tuple(sorted(set(am) - set(bm)))
    removed = tuple(sorted(set(bm) - set(am)))
    changed = tuple(sorted(k for k in set(bm) & set(am) if _fingerprint(bm[k]) != _fingerprint(am[k])))
    approved = set(map(str, approved_target_ids))
    locked_changed = tuple(sorted(k for k in changed if bm[k].get("state") == "LOCKED" or am[k].get("state") == "LOCKED"))
    unauthorized = tuple(sorted(k for k in changed if k not in approved))
    valid = not added and not removed and not locked_changed and not unauthorized and after.status == "PASS"
    status = "PASS" if valid else ("BLOCKED" if locked_changed or unauthorized or added or removed else "NEEDS_REVIEW")
    reason = "Before/after detection matches approved scope." if valid else (
        "Unauthorized or locked/structural changes detected." if status == "BLOCKED"
        else "After-state detection requires review."
    )
    return BeforeAfterDetection(before.source_sha256, before.model_id, added, removed, changed,
                                locked_changed, unauthorized, valid, status, reason)
