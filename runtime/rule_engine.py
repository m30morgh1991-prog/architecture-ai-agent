"""H76 deterministic Architecture Rule Engine.

Rules consume structured PlanModel/ConstraintMap/ImpactAnalysis context and
explicit rule evidence. They never infer missing regulatory context. Missing or
contradictory evidence is fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

from runtime.impact_analysis import ImpactAnalysis
from runtime.plan_model_contract import ConstraintMap, PlanModel
from runtime.rule_context import ProjectRuleContext

RuleStatus = Literal["PASS", "NEEDS_REVIEW", "BLOCKED", "UNKNOWN"]
AuthorityLevel = Literal["BINDING", "OFFICIAL_STANDARD", "TECHNICAL", "REFERENCE", "EDUCATIONAL"]

_AUTHORITY_RANK = {
    "BINDING": 5,
    "OFFICIAL_STANDARD": 4,
    "TECHNICAL": 3,
    "REFERENCE": 2,
    "EDUCATIONAL": 1,
}


@dataclass(frozen=True)
class ArchitectureRule:
    rule_id: str
    source_id: str
    version: str
    authority_level: AuthorityLevel
    applicability: str
    requirement: str
    evidence_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        if not all((self.rule_id, self.source_id, self.version,
                    self.applicability, self.requirement)):
            raise ValueError("RULE_DEFINITION_INCOMPLETE")
        if self.authority_level not in _AUTHORITY_RANK:
            raise ValueError("RULE_AUTHORITY_INVALID")
        if not self.evidence_ids:
            raise ValueError("RULE_EVIDENCE_MISSING")


@dataclass(frozen=True)
class RuleDecision:
    rule_id: str
    status: RuleStatus
    source_id: str
    version: str
    authority_level: AuthorityLevel
    reason: str
    evidence_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.rule_id or not self.source_id or not self.version:
            raise ValueError("RULE_DECISION_TRACE_INVALID")
        if self.status not in {"PASS", "NEEDS_REVIEW", "BLOCKED", "UNKNOWN"}:
            raise ValueError("RULE_DECISION_STATUS_INVALID")
        if not self.reason.strip():
            raise ValueError("RULE_DECISION_REASON_MISSING")
        if not self.evidence_ids:
            raise ValueError("RULE_DECISION_EVIDENCE_MISSING")


@dataclass(frozen=True)
class RuleEvaluation:
    model_id: str
    source_sha256: str
    status: RuleStatus
    decisions: tuple[RuleDecision, ...]
    blockers: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.model_id or len(self.source_sha256) != 64:
            raise ValueError("RULE_EVALUATION_TRACE_INVALID")
        if self.status not in {"PASS", "NEEDS_REVIEW", "BLOCKED", "UNKNOWN"}:
            raise ValueError("RULE_EVALUATION_STATUS_INVALID")
        for decision in self.decisions:
            decision.validate()
        if self.status == "PASS" and self.blockers:
            raise ValueError("PASS_CANNOT_HAVE_RULE_BLOCKERS")


def _applicable(rule: ArchitectureRule, context: ProjectRuleContext) -> bool | None:
    """Return False only for explicit non-applicability; None means unknown."""
    scope = rule.applicability.strip().lower()
    if not scope or scope == "all":
        return True
    accepted = {part.strip().lower() for part in scope.split("|") if part.strip()}
    if context.project_type.lower() in accepted or context.jurisdiction.lower() in accepted:
        return True
    if any("*" == part for part in accepted):
        return True
    # A non-matching explicit scope is deterministic non-applicability.
    return False


def evaluate_rules(
    plan_model: PlanModel,
    constraint_map: ConstraintMap,
    impact: ImpactAnalysis,
    context: ProjectRuleContext,
    rules: Sequence[ArchitectureRule],
) -> RuleEvaluation:
    plan_model.validate()
    constraint_map.validate()
    impact.validate()
    context.validate()

    if impact.model_id != plan_model.model_id or impact.source_sha256 != plan_model.source_sha256:
        return RuleEvaluation(
            plan_model.model_id, plan_model.source_sha256, "BLOCKED", (),
            ("RULE_INPUT_MODEL_MISMATCH",),
        )

    if not rules:
        return RuleEvaluation(
            plan_model.model_id, plan_model.source_sha256, "UNKNOWN", (),
            ("RULE_SET_MISSING",),
        )

    for rule in rules:
        rule.validate()

    ordered = sorted(rules, key=lambda r: (-_AUTHORITY_RANK[r.authority_level], r.rule_id))
    decisions: list[RuleDecision] = []
    blockers: list[str] = []

    # Impact is an upstream gate: a blocked/unknown impact cannot become a rule PASS.
    if impact.status in {"BLOCKED", "UNKNOWN"}:
        return RuleEvaluation(
            plan_model.model_id, plan_model.source_sha256,
            "BLOCKED" if impact.status == "BLOCKED" else "UNKNOWN",
            (), ("IMPACT_NOT_APPROVABLE",),
        )

    for rule in ordered:
        applicable = _applicable(rule, context)
        if applicable is False:
            continue
        if applicable is None:
            decisions.append(RuleDecision(
                rule.rule_id, "UNKNOWN", rule.source_id, rule.version,
                rule.authority_level, "Rule applicability cannot be established.",
                rule.evidence_ids,
            ))
            blockers.append(f"RULE_APPLICABILITY_UNKNOWN:{rule.rule_id}")
            continue

        # H76 deliberately evaluates only explicit evidence supplied by the caller.
        # A rule is not considered satisfied merely because its requirement exists.
        evidence_ids = tuple(dict.fromkeys((*context.source_ids, *rule.evidence_ids)))
        if not evidence_ids:
            decisions.append(RuleDecision(
                rule.rule_id, "UNKNOWN", rule.source_id, rule.version,
                rule.authority_level, "Required rule evidence is missing.",
                rule.evidence_ids,
            ))
            blockers.append(f"RULE_EVIDENCE_MISSING:{rule.rule_id}")
            continue

        # No implicit PASS: callers must provide an explicit rule outcome in a later
        # adapter. H76 therefore marks unresolved applicability/evidence as review.
        decisions.append(RuleDecision(
            rule.rule_id, "NEEDS_REVIEW", rule.source_id, rule.version,
            rule.authority_level,
            "Rule is applicable and evidenced; requirement outcome requires explicit deterministic check.",
            evidence_ids,
        ))
        blockers.append(f"RULE_CHECK_REQUIRED:{rule.rule_id}")

    if any(d.status == "BLOCKED" for d in decisions):
        status: RuleStatus = "BLOCKED"
    elif any(d.status == "UNKNOWN" for d in decisions):
        status = "UNKNOWN"
    elif blockers:
        status = "NEEDS_REVIEW"
    else:
        status = "PASS"

    result = RuleEvaluation(
        plan_model.model_id, plan_model.source_sha256, status,
        tuple(decisions), tuple(dict.fromkeys(blockers)),
    )
    result.validate()
    return result
