"""H35 visual-semantic corroboration gate.

Converts raw visual evidence into approval-grade structural semantics only when
independent evidence sources corroborate the same interpretation. No signal is
allowed to self-label a marker as a column.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CorroborationResult:
    status: str
    semantics: str
    supporting_evidence: tuple[str, ...]
    contradictions: tuple[str, ...]
    reason: str

    def validate(self) -> None:
        if self.status not in {"ACCESSIBLE", "UNKNOWN", "BLOCKED"}:
            raise ValueError("INVALID_CORROBORATION_STATUS")
        if self.semantics not in {"COLUMNS", "STRUCTURAL_FIXED_ELEMENTS", "UNKNOWN"}:
            raise ValueError("INVALID_CORROBORATION_SEMANTICS")
        if self.status == "ACCESSIBLE" and self.semantics == "UNKNOWN":
            raise ValueError("ACCESSIBLE_UNKNOWN_SEMANTICS")


class VisualSemanticCorroborationGate:
    """Fail-closed semantic gate for structural fixed-element identification."""

    gate_id = "visual-semantic-corroboration-v0.1"

    def evaluate(
        self,
        *,
        marker_evidence: bool,
        wall_geometry_evidence: bool,
        vector_or_grid_evidence: bool,
        structural_geometry_evidence: bool,
        contradiction_evidence: bool = False,
    ) -> CorroborationResult:
        evidence = {
            "marker": marker_evidence,
            "wall_geometry": wall_geometry_evidence,
            "vector_or_grid": vector_or_grid_evidence,
            "structural_geometry": structural_geometry_evidence,
        }
        supporting = tuple(name for name, present in evidence.items() if present)

        if contradiction_evidence:
            result = CorroborationResult(
                "BLOCKED",
                "UNKNOWN",
                supporting,
                ("contradictory_evidence",),
                "Conflicting visual evidence prevents approval-grade structural semantics.",
            )
        elif len(supporting) >= 2:
            result = CorroborationResult(
                "ACCESSIBLE",
                "COLUMNS" if marker_evidence and structural_geometry_evidence else "STRUCTURAL_FIXED_ELEMENTS",
                supporting,
                (),
                "Independent visual evidence sources corroborate the fixed-element interpretation.",
            )
        else:
            result = CorroborationResult(
                "UNKNOWN",
                "UNKNOWN",
                supporting,
                (),
                "Insufficient independent evidence for approval-grade structural semantics.",
            )

        result.validate()
        return result
