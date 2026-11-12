"""Revision diff between two PlanModels.

``post_edit_diff`` records deltas after an edit we performed. This module
compares two arbitrary PlanModel versions (for example two revisions of the same
plan) and checks that protected elements were not touched.

Limits (stated, not hidden):
* Element identity is the ``element_id`` only. A renamed or renumbered element is
  reported as REMOVED + ADDED; the module never guesses a match.
* Geometry is compared as given. The caller must provide traceable coordinate
  evidence proving the same frame and recognized units for both models; otherwise
  the comparison is refused instead of producing a misleading result.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Iterable

from runtime.plan_model_contract import PlanElement, PlanModel
from runtime.post_edit_diff import Delta, PostEditDiff
from runtime.review_report_contract import Finding

CHANGE_TYPES = ("ADDED", "REMOVED", "STATE_CHANGED", "TYPE_CHANGED", "GEOMETRY_CHANGED")


_UNIT_CANONICAL = {
    "mm": "mm", "millimeter": "mm", "millimeters": "mm", "millimetre": "mm", "millimetres": "mm",
    "cm": "cm", "centimeter": "cm", "centimeters": "cm", "centimetre": "cm", "centimetres": "cm",
    "m": "m", "meter": "m", "meters": "m", "metre": "m", "metres": "m",
    "in": "in", "inch": "in", "inches": "in",
    "ft": "ft", "foot": "ft", "feet": "ft",
}


@dataclass(frozen=True)
class CoordinateSystemEvidence:
    base_frame_id: str
    revised_frame_id: str
    base_units: str
    revised_units: str
    evidence_ids: tuple[str, ...]

    def validate(self) -> tuple[str, str]:
        if not all((self.base_frame_id, self.revised_frame_id, self.base_units, self.revised_units)):
            raise ValueError("COORDINATE_SYSTEM_EVIDENCE_MISSING")
        if not self.evidence_ids or not all(self.evidence_ids):
            raise ValueError("COORDINATE_SYSTEM_PROVENANCE_MISSING")
        if self.base_frame_id != self.revised_frame_id:
            raise ValueError("COORDINATE_FRAME_NOT_ESTABLISHED")
        base_unit = _UNIT_CANONICAL.get(self.base_units.strip().lower())
        revised_unit = _UNIT_CANONICAL.get(self.revised_units.strip().lower())
        if not base_unit or not revised_unit:
            raise ValueError("COORDINATE_UNITS_NOT_ESTABLISHED")
        if base_unit != revised_unit:
            raise ValueError("UNIT_MISMATCH_NOT_ESTABLISHED")
        return self.base_frame_id, base_unit


@dataclass(frozen=True)
class ElementChange:
    element_id: str
    change_type: str
    before: str
    after: str
    base_state: str | None
    revised_state: str | None
    protected: bool = False

    @property
    def violates_protection(self) -> bool:
        """A protected/LOCKED base element was removed or modified."""
        return self.protected and self.change_type != "ADDED"


@dataclass(frozen=True)
class RevisionDiff:
    diff_id: str
    base_model_id: str
    revised_model_id: str
    base_sha256: str
    revised_sha256: str
    coordinate_frame_id: str
    units: str
    coordinate_evidence_ids: tuple[str, ...]
    changes: tuple[ElementChange, ...]

    def validate(self) -> None:
        if not self.diff_id or not self.base_model_id or not self.revised_model_id:
            raise ValueError("REVISION_DIFF_TRACEABILITY_MISSING")
        if not self.coordinate_frame_id or not self.units or not self.coordinate_evidence_ids:
            raise ValueError("REVISION_DIFF_COORDINATE_PROVENANCE_MISSING")
        for change in self.changes:
            if not change.element_id or change.change_type not in CHANGE_TYPES:
                raise ValueError("REVISION_CHANGE_INVALID")

    @property
    def protection_violations(self) -> tuple[ElementChange, ...]:
        self.validate()
        return tuple(c for c in self.changes if c.violates_protection)

    @property
    def clean(self) -> bool:
        return not self.protection_violations


def _num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _geometry_equal(a: Any, b: Any, tolerance: float) -> bool:
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_geometry_equal(a[k], b[k], tolerance) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_geometry_equal(x, y, tolerance) for x, y in zip(a, b))
    if _num(a) and _num(b):
        return abs(a - b) <= tolerance  # NaN never compares equal: fail closed
    return a == b


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def compute_revision_diff(
    base: PlanModel,
    revised: PlanModel,
    *,
    coordinate_system_evidence: CoordinateSystemEvidence,
    protected_element_ids: Iterable[str] = (),
    tolerance: float = 0.0,
    diff_id: str | None = None,
) -> RevisionDiff:
    if not isinstance(coordinate_system_evidence, CoordinateSystemEvidence):
        raise ValueError("COORDINATE_SYSTEM_EVIDENCE_MISSING")
    coordinate_frame_id, units = coordinate_system_evidence.validate()
    if (
        isinstance(tolerance, bool)
        or not isinstance(tolerance, (int, float))
        or not math.isfinite(tolerance)
        or tolerance < 0
    ):
        raise ValueError("TOLERANCE_INVALID")
    base.validate()
    revised.validate()

    base_by_id: dict[str, PlanElement] = {e.element_id: e for e in base.elements}
    revised_by_id: dict[str, PlanElement] = {e.element_id: e for e in revised.elements}
    protected = set(protected_element_ids)
    changes: list[ElementChange] = []

    for element_id in sorted(base_by_id.keys() | revised_by_id.keys()):
        old = base_by_id.get(element_id)
        new = revised_by_id.get(element_id)
        is_protected = old is not None and (old.state == "LOCKED" or element_id in protected)
        if old is None and new is not None:
            changes.append(ElementChange(element_id, "ADDED", "", new.element_type, None, new.state))
            continue
        if new is None and old is not None:
            changes.append(
                ElementChange(element_id, "REMOVED", old.element_type, "", old.state, None, is_protected)
            )
            continue
        assert old is not None and new is not None
        if old.element_type != new.element_type:
            changes.append(ElementChange(element_id, "TYPE_CHANGED", old.element_type,
                                         new.element_type, old.state, new.state, is_protected))
        if old.state != new.state:
            changes.append(ElementChange(element_id, "STATE_CHANGED", old.state, new.state,
                                         old.state, new.state, is_protected))
        if not _geometry_equal(old.geometry, new.geometry, tolerance):
            changes.append(ElementChange(element_id, "GEOMETRY_CHANGED", _dump(old.geometry),
                                         _dump(new.geometry), old.state, new.state, is_protected))

    diff = RevisionDiff(
        diff_id or f"REV:{base.model_id}->{revised.model_id}",
        base.model_id,
        revised.model_id,
        base.source_sha256,
        revised.source_sha256,
        coordinate_frame_id,
        units,
        tuple(coordinate_system_evidence.evidence_ids),
        tuple(changes),
    )
    diff.validate()
    return diff


def revision_findings(diff: RevisionDiff) -> tuple[Finding, ...]:
    diff.validate()
    evidence = (f"diff:{diff.diff_id}",)
    if not diff.changes:
        return (
            Finding(
                finding_id=f"{diff.diff_id}:NOCHANGE",
                category="REVISION_DIFF",
                check_id="REV-NOCHANGE-001",
                status="PASS",
                severity="INFO",
                message="No element differences between the two models.",
                evidence_ids=evidence,
            ),
        )
    findings: list[Finding] = []
    for change in diff.changes:
        if change.violates_protection:
            check, status, severity = "REV-LOCKED-001", "BLOCKED", "BLOCKING"
            text = f"Protected element changed ({change.change_type}); revision rejected."
        elif change.change_type == "ADDED":
            if change.revised_state == "LOCKED":
                check, status, severity = "REV-ADDED-LOCKED-001", "NEEDS_REVIEW", "WARNING"
                text = "A new LOCKED element appeared; confirm it is a real structural element."
            else:
                check, status, severity = "REV-ADDED-001", "PASS", "INFO"
                text = "Element added (informational)."
        elif change.base_state == "EDITABLE":
            check, status, severity = "REV-EDITABLE-001", "PASS", "INFO"
            text = f"Editable element changed ({change.change_type}); informational."
        else:
            check, status, severity = "REV-UNCERTAIN-001", "NEEDS_REVIEW", "WARNING"
            text = (f"Element in state {change.base_state} changed "
                    f"({change.change_type}); human review required.")
        findings.append(
            Finding(
                finding_id=f"{diff.diff_id}:{change.element_id}:{change.change_type}",
                category="REVISION_DIFF",
                check_id=check,
                status=status,
                severity=severity,
                message=text,
                evidence_ids=evidence,
                element_ids=(change.element_id,),
            )
        )
    return tuple(findings)


def to_post_edit_diff(
    diff: RevisionDiff,
    *,
    authorized_element_ids: Iterable[str] = (),
) -> PostEditDiff:
    """Express a revision diff with the existing PostEditDiff contract.

    A change to a protected element is never authorized, even if listed.
    """
    diff.validate()
    authorized = set(authorized_element_ids)
    attribute = {
        "ADDED": "presence",
        "REMOVED": "presence",
        "STATE_CHANGED": "state",
        "TYPE_CHANGED": "element_type",
        "GEOMETRY_CHANGED": "geometry",
    }
    deltas = [
        Delta(
            c.element_id,
            attribute[c.change_type],
            c.before,
            c.after,
            c.element_id in authorized and not c.violates_protection,
        )
        for c in diff.changes
    ]
    result = PostEditDiff(diff.diff_id, diff.base_model_id, diff.revised_model_id, deltas)
    result.validate()
    return result
