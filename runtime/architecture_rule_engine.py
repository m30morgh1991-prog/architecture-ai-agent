"""H76 deterministic, evidence-backed architecture rule engine.

The engine is provider-agnostic and never invents regulatory compliance.
Rules carry explicit source provenance and evidence requirements. Unknown,
missing, conflicting, or unsupported evidence fails closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RuleStatus = Literal["PASS", "FAIL", "NEEDS_REVIEW", "UNKNOWN", "BLOCKED", "NOT_APPLICABLE"]
RuleSourceTier = Literal[
    "BINDING_REGULATION",
    "OFFICIAL_STANDARD",
    "TECHNICAL_PUBLICATION",
    "REFERENCE_BOOK",
    "VOCATIONAL_EDUCATION",
    "PROJECT_BASIS",
]
RuleSeverity = Literal["INFO", "WARNING", "BLOCKING"]

_PRIORITY = {
    "BINDING_REGULATION": 1,
    "OFFICIAL_STANDARD": 2,
    "TECHNICAL_PUBLICATION": 3,
    "REFERENCE_BOOK": 4,
    "VOCATIONAL_EDUCATION": 5,
    "PROJECT_BASIS": 6,
}
_STATUSES = {"PASS", "FAIL", "NEEDS_REVIEW", "UNKNOWN", "BLOCKED", "NOT_APPLICABLE"}
_TIERS = set(_PRIORITY)
_SEVERITIES = {"INFO", "WARNING", "BLOCKING"}


@dataclass(frozen=True)
class RuleSource:
    source_id: str
    title: str
    tier: RuleSourceTier
    locator: str
    evidence_required: bool = True

    @property
    def priority(self) -> int:
        return _PRIORITY[self.tier]

    def validate(self) -> None:
        if not self.source_id.strip():
            raise ValueError("RULE_SOURCE_ID_MISSING")
        if not self.title.strip():
            raise ValueError("RULE_SOURCE_TITLE_MISSING")
        if self.tier not in _TIERS:
            raise ValueError("RULE_SOURCE_TIER_INVALID")
        if not self.locator.strip():
            raise ValueError("RULE_SOURCE_LOCATOR_MISSING")


@dataclass(frozen=True)
class Rule:
    rule_id: str
    version: str
    domain: str
    statement: str
    source: RuleSource
    severity: RuleSeverity = "BLOCKING"
    evidence_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("RULE_ID_MISSING")
        if not self.version.strip():
            raise ValueError("RULE_VERSION_MISSING")
        if not self.domain.strip() or not self.statement.strip():
            raise ValueError("RULE_DEFINITION_MISSING")
        self.source.validate()
        if self.severity not in _SEVERITIES:
            raise ValueError("RULE_SEVERITY_INVALID")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("RULE_EVIDENCE_DUPLICATE")
        if self.source.evidence_required and not self.evidence_ids:
            raise ValueError("RULE_EVIDENCE_REQUIRED")


@dataclass(frozen=True)
class RuleEvaluation:
    source_sha256: str
    model_id: str
    rule_id: str
    rule_version: str
    status: RuleStatus
    reason: str
    evidence_ids: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()

    def validate(self) -> None:
        if len(self.source_sha256) != 64:
            raise ValueError("RULE_EVAL_SOURCE_INVALID")
        if not self.model_id.strip() or not self.rule_id.strip() or not self.rule_version.strip():
            raise ValueError("RULE_EVAL_TRACE_INVALID")
        if self.status not in _STATUSES:
            raise ValueError("RULE_EVAL_STATUS_INVALID")
        if not self.reason.strip():
            raise ValueError("RULE_EVAL_REASON_MISSING")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("RULE_EVAL_EVIDENCE_DUPLICATE")
        if self.status == "PASS" and self.blockers:
            raise ValueError("PASS_CANNOT_HAVE_RULE_BLOCKERS")


@dataclass(frozen=True)
class RuleSet:
    ruleset_id: str
    version: str
    rules: tuple[Rule, ...]

    def validate(self) -> None:
        if not self.ruleset_id.strip() or not self.version.strip():
            raise ValueError("RULESET_ID_VERSION_MISSING")
        ids = [rule.rule_id for rule in self.rules]
        if len(ids) != len(set(ids)):
            raise ValueError("RULE_ID_DUPLICATE")
        for rule in self.rules:
            rule.validate()

    def ordered_rules(self) -> tuple[Rule, ...]:
        self.validate()
        return tuple(sorted(self.rules, key=lambda rule: (rule.source.priority, rule.rule_id, rule.version)))


def evaluate_rule(
    rule: Rule,
    *,
    source_sha256: str,
    model_id: str,
    observed_status: RuleStatus | None = None,
    observed_evidence_ids: tuple[str, ...] = (),
) -> RuleEvaluation:
    rule.validate()

    if len(source_sha256) != 64:
        return RuleEvaluation(source_sha256, model_id, rule.rule_id, rule.version,
                              "BLOCKED", "Source identity is invalid.",
                              blockers=("SOURCE_IDENTITY_INVALID",))

    if not model_id.strip():
        return RuleEvaluation(source_sha256, model_id, rule.rule_id, rule.version,
                              "BLOCKED", "Model identity is missing.",
                              blockers=("MODEL_ID_MISSING",))

    evidence = tuple(dict.fromkeys(observed_evidence_ids))
    required = set(rule.evidence_ids)
    if rule.source.evidence_required and not required.issubset(evidence):
        return RuleEvaluation(
            source_sha256, model_id, rule.rule_id, rule.version, "UNKNOWN",
            "Required rule evidence is missing.",
            evidence,
            ("RULE_EVIDENCE_MISSING",),
        )

    if observed_status is None:
        return RuleEvaluation(
            source_sha256, model_id, rule.rule_id, rule.version, "UNKNOWN",
            "No deterministic observation was supplied; compliance is not inferred.",
            evidence,
            ("RULE_OBSERVATION_MISSING",),
        )

    if observed_status not in _STATUSES:
        return RuleEvaluation(
            source_sha256, model_id, rule.rule_id, rule.version, "BLOCKED",
            "Observation status is unsupported.",
            evidence,
            ("RULE_OBSERVATION_INVALID",),
        )

    blockers: tuple[str, ...] = ()
    if observed_status == "FAIL" and rule.severity == "BLOCKING":
        blockers = ("RULE_FAILED",)
    elif observed_status in {"UNKNOWN", "NEEDS_REVIEW"}:
        blockers = ("RULE_REVIEW_REQUIRED",)

    return RuleEvaluation(
        source_sha256, model_id, rule.rule_id, rule.version,
        observed_status, "Observation accepted without changing its meaning.",
        evidence, blockers,
    )
