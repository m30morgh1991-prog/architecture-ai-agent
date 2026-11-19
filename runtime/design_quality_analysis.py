"""Advisory space-program fit diagnostics (v0.1).

This module checks an architect-supplied room program against an existing,
source-bound SpaceModel. It does not generate geometry, approve a design, or
apply legal/code rules. Findings are explainable prompts for architect review.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import Literal

from runtime.space_model_contract import SpaceModel

FindingSeverity = Literal["INFO", "WARNING", "REVIEW"]
AnalysisStatus = Literal["ANALYSIS_COMPLETE", "NEEDS_REVIEW"]


def _positive_number(value: object, code: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(code)
    number = float(value)
    if not isfinite(number) or number <= 0:
        raise ValueError(code)
    return number


@dataclass(frozen=True)
class SpaceProgramRequirement:
    """A requirement explicitly authored by the architect/client.

    Relations use stable SpaceRecord IDs, never inferred room-name matching.
    Area values use the same drawing-unit-squared convention as SpaceModel.
    """

    space_id: str
    min_area: float | None = None
    target_area: float | None = None
    max_area: float | None = None
    required_adjacent_to: tuple[str, ...] = ()
    avoid_adjacent_to: tuple[str, ...] = ()
    require_accessible_path_to: tuple[str, ...] = ()

    def validate(self) -> None:
        if not isinstance(self.space_id, str) or not self.space_id.strip():
            raise ValueError("PROGRAM_SPACE_ID_MISSING")
        minimum = _positive_number(self.min_area, "PROGRAM_MIN_AREA_INVALID") if self.min_area is not None else None
        target = _positive_number(self.target_area, "PROGRAM_TARGET_AREA_INVALID") if self.target_area is not None else None
        maximum = _positive_number(self.max_area, "PROGRAM_MAX_AREA_INVALID") if self.max_area is not None else None
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("PROGRAM_AREA_RANGE_INVALID")
        if target is not None and minimum is not None and target < minimum:
            raise ValueError("PROGRAM_TARGET_OUTSIDE_RANGE")
        if target is not None and maximum is not None and target > maximum:
            raise ValueError("PROGRAM_TARGET_OUTSIDE_RANGE")
        for values in (self.required_adjacent_to, self.avoid_adjacent_to, self.require_accessible_path_to):
            if any(not isinstance(item, str) or not item.strip() for item in values):
                raise ValueError("PROGRAM_RELATION_TARGET_INVALID")
            if len(values) != len(set(values)):
                raise ValueError("PROGRAM_RELATION_TARGET_DUPLICATE")
        if self.space_id in self.required_adjacent_to or self.space_id in self.avoid_adjacent_to or self.space_id in self.require_accessible_path_to:
            raise ValueError("PROGRAM_SELF_RELATION_INVALID")


@dataclass(frozen=True)
class DesignFinding:
    code: str
    severity: FindingSeverity
    space_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    message: str
    suggestion: str

    def validate(self) -> None:
        if not self.code or not self.message.strip() or not self.suggestion.strip():
            raise ValueError("DESIGN_FINDING_INCOMPLETE")
        if self.severity not in {"INFO", "WARNING", "REVIEW"}:
            raise ValueError("DESIGN_FINDING_SEVERITY_INVALID")
        if not self.space_ids:
            raise ValueError("DESIGN_FINDING_SPACES_MISSING")
        if not self.evidence_ids:
            raise ValueError("DESIGN_FINDING_EVIDENCE_MISSING")


@dataclass(frozen=True)
class SpaceProgramFitAnalysis:
    model_id: str
    source_sha256: str
    status: AnalysisStatus
    findings: tuple[DesignFinding, ...]
    checked_requirement_count: int

    def validate(self) -> None:
        if not self.model_id or len(self.source_sha256) != 64:
            raise ValueError("DESIGN_ANALYSIS_SOURCE_INVALID")
        if self.status not in {"ANALYSIS_COMPLETE", "NEEDS_REVIEW"}:
            raise ValueError("DESIGN_ANALYSIS_STATUS_INVALID")
        if self.checked_requirement_count < 0:
            raise ValueError("DESIGN_ANALYSIS_COUNT_INVALID")
        for finding in self.findings:
            finding.validate()
        expected = "NEEDS_REVIEW" if self.findings else "ANALYSIS_COMPLETE"
        if self.status != expected:
            raise ValueError("DESIGN_ANALYSIS_STATUS_INCONSISTENT")


def analyze_space_program_fit(
    space_model: SpaceModel,
    requirements: tuple[SpaceProgramRequirement, ...] | list[SpaceProgramRequirement],
) -> SpaceProgramFitAnalysis:
    """Compare explicit room-program requirements with source-bound spaces.

    A clean result means only that the supplied checks found no discrepancy.
    It is not architectural approval, regulatory compliance, or proof that
    unprovided requirements have been satisfied.
    """
    space_model.validate()
    if not isinstance(requirements, (tuple, list)):
        raise ValueError("PROGRAM_REQUIREMENTS_INVALID")
    for requirement in requirements:
        if not isinstance(requirement, SpaceProgramRequirement):
            raise ValueError("PROGRAM_REQUIREMENT_TYPE_INVALID")
        requirement.validate()

    spaces = {space.space_id: space for space in space_model.spaces}
    relations: dict[frozenset[str], list] = {}
    for relation in space_model.relations:
        if relation.from_space_id and relation.to_space_id:
            key = frozenset((relation.from_space_id, relation.to_space_id))
            relations.setdefault(key, []).append(relation)

    findings: list[DesignFinding] = []

    def evidence_for(ids: tuple[str, ...], relation_items=()) -> tuple[str, ...]:
        evidence = []
        for space_id in ids:
            space = spaces.get(space_id)
            if space is not None:
                evidence.extend(space.evidence_ids)
        for relation in relation_items:
            evidence.extend(relation.evidence_ids)
        return tuple(dict.fromkeys(evidence))

    for requirement in requirements:
        space = spaces.get(requirement.space_id)
        if space is None:
            # There is no source-bound evidence to support a fabricated finding.
            # The missing mapping is represented as an unresolved model-level item
            # only when at least one space supplies traceable evidence.
            available_evidence = tuple(dict.fromkeys(
                evidence_id for item in space_model.spaces for evidence_id in item.evidence_ids
            ))
            if available_evidence:
                finding = DesignFinding(
                    "PROGRAM_SPACE_NOT_MAPPED", "REVIEW", (requirement.space_id,),
                    available_evidence[:8],
                    f"Program space '{requirement.space_id}' is not mapped to a detected SpaceModel record.",
                    "Map the program requirement to the correct space or complete space detection before evaluating it.",
                )
                findings.append(finding)
            continue

        if requirement.min_area is not None and space.area < requirement.min_area:
            findings.append(DesignFinding(
                "SPACE_AREA_BELOW_PROGRAM_MINIMUM", "WARNING", (space.space_id,),
                evidence_for((space.space_id,)),
                f"Detected area {space.area:g} is below the supplied minimum {requirement.min_area:g}.",
                "Review the room boundary, drawing units and program requirement; consider reallocating area from adjacent spaces.",
            ))
        if requirement.max_area is not None and space.area > requirement.max_area:
            findings.append(DesignFinding(
                "SPACE_AREA_ABOVE_PROGRAM_MAXIMUM", "INFO", (space.space_id,),
                evidence_for((space.space_id,)),
                f"Detected area {space.area:g} exceeds the supplied maximum {requirement.max_area:g}.",
                "Check whether the additional area improves function or could be reassigned to another space.",
            ))
        if requirement.target_area is not None and space.area != requirement.target_area:
            findings.append(DesignFinding(
                "SPACE_AREA_DIFFERS_FROM_TARGET", "INFO", (space.space_id,),
                evidence_for((space.space_id,)),
                f"Detected area {space.area:g} differs from the requested target {requirement.target_area:g}.",
                "Review the deviation with the architect; the target is a design preference, not an automatic failure.",
            ))

        for other_id in requirement.required_adjacent_to:
            pair = (space.space_id, other_id)
            pair_relations = relations.get(frozenset(pair), [])
            positive = [r for r in pair_relations if r.relation_type in {"SHARED_BOUNDARY", "CONNECTED_BY_OPENING"}]
            disconnected = [r for r in pair_relations if r.relation_type == "DISCONNECTED"]
            if positive:
                continue
            if disconnected:
                findings.append(DesignFinding(
                    "REQUIRED_ADJACENCY_NOT_MET", "WARNING", pair,
                    evidence_for(pair, disconnected),
                    f"The required neighboring spaces {space.space_id} and {other_id} are explicitly classified as disconnected.",
                    "Review whether a direct connection is functionally necessary and whether the layout can be rearranged.",
                ))
            else:
                findings.append(DesignFinding(
                    "REQUIRED_ADJACENCY_UNRESOLVED", "REVIEW", pair,
                    evidence_for(pair, pair_relations),
                    f"Adjacency between {space.space_id} and {other_id} is not established by current topology evidence.",
                    "Inspect the shared boundary and openings; do not assume proximity or bounding-box overlap proves adjacency.",
                ))

        for other_id in requirement.avoid_adjacent_to:
            pair = (space.space_id, other_id)
            pair_relations = relations.get(frozenset(pair), [])
            adjacent = [r for r in pair_relations if r.relation_type in {"SHARED_BOUNDARY", "CONNECTED_BY_OPENING"}]
            if adjacent:
                findings.append(DesignFinding(
                    "UNWANTED_ADJACENCY_PRESENT", "WARNING", pair,
                    evidence_for(pair, adjacent),
                    f"The supplied program asks to separate {space.space_id} and {other_id}, but the model records a shared boundary or opening.",
                    "Review privacy, acoustic and functional zoning; consider a buffer or a different room arrangement.",
                ))

        for target_id in requirement.require_accessible_path_to:
            if target_id not in spaces:
                findings.append(DesignFinding(
                    "ACCESS_PATH_TARGET_UNMAPPED", "REVIEW", (space.space_id, target_id),
                    evidence_for((space.space_id,)),
                    f"No SpaceModel record exists for requested path destination {target_id}.",
                    "Complete room mapping and opening-connectivity evidence before assessing circulation.",
                ))
                continue
            # Only explicitly accessible door/opening relations count as a path.
            adjacency: dict[str, set[str]] = {key: set() for key in spaces}
            for relation in space_model.relations:
                if relation.relation_type == "CONNECTED_BY_OPENING" and relation.status == "ACCESSIBLE":
                    adjacency[relation.from_space_id].add(relation.to_space_id)
                    adjacency[relation.to_space_id].add(relation.from_space_id)
            visited = {space.space_id}
            frontier = [space.space_id]
            while frontier:
                current = frontier.pop()
                for neighbor in adjacency[current] - visited:
                    visited.add(neighbor)
                    frontier.append(neighbor)
            if target_id not in visited:
                relevant = [
                    r for r in space_model.relations
                    if r.relation_type in {"CONNECTED_BY_OPENING", "OPENING_CONNECTIVITY_UNKNOWN"}
                    and (r.from_space_id in visited or r.to_space_id in visited)
                ]
                findings.append(DesignFinding(
                    "ACCESSIBLE_PATH_NOT_ESTABLISHED", "REVIEW", (space.space_id, target_id),
                    evidence_for((space.space_id, target_id), relevant) or evidence_for((space.space_id,)),
                    f"An accessible opening path from {space.space_id} to {target_id} is not established by current evidence.",
                    "Inspect doors, opening directions and connectivity; missing path evidence is not proof that no path exists.",
                ))

    result = SpaceProgramFitAnalysis(
        model_id=space_model.model_id,
        source_sha256=space_model.source_sha256,
        status="NEEDS_REVIEW" if findings else "ANALYSIS_COMPLETE",
        findings=tuple(findings),
        checked_requirement_count=len(requirements),
    )
    result.validate()
    return result
