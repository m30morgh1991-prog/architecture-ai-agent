"""Deterministic review report contract.

Aggregates the results of the existing validators (rule engine, drawing
standards, conflict/validation, revision diff, input completeness) into one
traceable list of findings that a human reviewer can acknowledge or override.

Design rules (fail-closed):
* A finding without evidence is invalid; no uncertainty is promoted to PASS.
* ``overall_status`` depends only on finding statuses. A human disposition never
  changes a status, so an overridden UNKNOWN finding is still UNKNOWN.
* BLOCKED / BLOCKING findings cannot be overridden; they need new evidence and a
  new run.
* ``human_review_complete`` is not PASS and does not authorize editing. Editing
  still requires an ApprovedChangePlan.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Iterable

FINDING_STATUSES = ("PASS", "NEEDS_REVIEW", "BLOCKED", "UNKNOWN", "SOURCE_REQUIRED")
SEVERITIES = ("INFO", "WARNING", "BLOCKING")
CATEGORIES = (
    "COMPLETENESS",
    "DRAWING_STANDARDS",
    "CONFLICT",
    "RULE",
    "REVISION_DIFF",
)
DISPOSITIONS = ("PENDING", "ACKNOWLEDGED", "OVERRIDDEN")

# Worst first. PASS is only reachable when no other status is present.
_STATUS_PRECEDENCE = ("BLOCKED", "SOURCE_REQUIRED", "NEEDS_REVIEW", "UNKNOWN")


@dataclass(frozen=True)
class Finding:
    finding_id: str
    category: str
    check_id: str
    status: str
    severity: str
    message: str
    evidence_ids: tuple[str, ...]
    element_ids: tuple[str, ...] = ()
    disposition: str = "PENDING"
    reviewer_id: str = ""
    disposition_reason: str = ""

    def validate(self) -> None:
        if not self.finding_id or not self.check_id:
            raise ValueError("FINDING_TRACEABILITY_MISSING")
        if self.category not in CATEGORIES:
            raise ValueError("FINDING_CATEGORY_INVALID")
        if self.status not in FINDING_STATUSES:
            raise ValueError("FINDING_STATUS_INVALID")
        if self.severity not in SEVERITIES:
            raise ValueError("FINDING_SEVERITY_INVALID")
        if not self.message.strip():
            raise ValueError("FINDING_MESSAGE_MISSING")
        if not self.evidence_ids or not all(self.evidence_ids):
            raise ValueError("FINDING_EVIDENCE_MISSING")
        if self.status == "PASS" and self.severity != "INFO":
            raise ValueError("PASS_FINDING_SEVERITY_INVALID")
        if self.status == "BLOCKED" and self.severity != "BLOCKING":
            raise ValueError("BLOCKED_FINDING_SEVERITY_INVALID")
        if self.disposition not in DISPOSITIONS:
            raise ValueError("FINDING_DISPOSITION_INVALID")
        if self.disposition != "PENDING":
            if self.status == "PASS":
                raise ValueError("PASS_FINDING_NEEDS_NO_DISPOSITION")
            if not self.reviewer_id.strip():
                raise ValueError("DISPOSITION_REVIEWER_MISSING")
            if not self.disposition_reason.strip():
                raise ValueError("DISPOSITION_REASON_MISSING")
        if self.disposition == "OVERRIDDEN" and (
            self.status == "BLOCKED" or self.severity == "BLOCKING"
        ):
            raise ValueError("OVERRIDE_NOT_ALLOWED_FOR_BLOCKING")

    @property
    def resolved(self) -> bool:
        """PASS, or explicitly overridden by a named reviewer with a reason."""
        return self.status == "PASS" or self.disposition == "OVERRIDDEN"

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "category": self.category,
            "check_id": self.check_id,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "evidence_ids": list(self.evidence_ids),
            "element_ids": list(self.element_ids),
            "disposition": self.disposition,
            "reviewer_id": self.reviewer_id,
            "disposition_reason": self.disposition_reason,
        }


@dataclass(frozen=True)
class ReviewReport:
    report_id: str
    model_id: str
    source_sha256: str
    findings: tuple[Finding, ...]

    def validate(self) -> None:
        if not self.report_id or not self.model_id:
            raise ValueError("REVIEW_REPORT_TRACEABILITY_MISSING")
        if len(self.source_sha256) != 64:
            raise ValueError("REVIEW_REPORT_SOURCE_INVALID")
        ids = [finding.finding_id for finding in self.findings]
        if len(ids) != len(set(ids)):
            raise ValueError("FINDING_ID_DUPLICATE")
        for finding in self.findings:
            finding.validate()

    @property
    def overall_status(self) -> str:
        """Worst finding status; an empty report is UNKNOWN, never PASS."""
        self.validate()
        statuses = {finding.status for finding in self.findings}
        for status in _STATUS_PRECEDENCE:
            if status in statuses:
                return status
        return "PASS" if statuses else "UNKNOWN"

    @property
    def unresolved_findings(self) -> tuple[Finding, ...]:
        self.validate()
        return tuple(finding for finding in self.findings if not finding.resolved)

    @property
    def human_review_complete(self) -> bool:
        """True only when findings exist and every one is PASS or overridden.

        This is not PASS and not an edit authorization.
        """
        self.validate()
        return bool(self.findings) and not self.unresolved_findings

    def summary(self) -> dict[str, int]:
        self.validate()
        counts = {status: 0 for status in FINDING_STATUSES}
        for finding in self.findings:
            counts[finding.status] += 1
        return counts

    def with_disposition(
        self,
        finding_id: str,
        disposition: str,
        *,
        reviewer_id: str,
        reason: str,
    ) -> "ReviewReport":
        """Return a new report; the original is never mutated."""
        self.validate()
        if finding_id not in {finding.finding_id for finding in self.findings}:
            raise ValueError("FINDING_NOT_FOUND")
        updated = []
        for finding in self.findings:
            if finding.finding_id == finding_id:
                finding = replace(
                    finding,
                    disposition=disposition,
                    reviewer_id=reviewer_id,
                    disposition_reason=reason,
                )
                finding.validate()
            updated.append(finding)
        report = replace(self, findings=tuple(updated))
        report.validate()
        return report

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "model_id": self.model_id,
            "source_sha256": self.source_sha256,
            "overall_status": self.overall_status,
            "human_review_complete": self.human_review_complete,
            "summary": self.summary(),
            "findings": [finding.to_dict() for finding in self.findings],
        }


def build_report(
    report_id: str,
    model_id: str,
    source_sha256: str,
    *finding_groups: Iterable[Finding],
) -> ReviewReport:
    findings: list[Finding] = []
    for group in finding_groups:
        findings.extend(group)
    report = ReviewReport(report_id, model_id, source_sha256, tuple(findings))
    report.validate()
    return report


# ---------------------------------------------------------------------------
# Adapters from existing contracts (duck-typed on purpose: no import coupling).
# ---------------------------------------------------------------------------

_RULE_STATUS = {
    "PASS": ("PASS", "INFO"),
    "NEEDS_REVIEW": ("NEEDS_REVIEW", "WARNING"),
    "BLOCKED": ("BLOCKED", "BLOCKING"),
    "UNKNOWN": ("UNKNOWN", "WARNING"),
}


def findings_from_rule_evaluation(evaluation: Any) -> tuple[Finding, ...]:
    """Convert a rule_engine.RuleEvaluation into findings."""
    evaluation.validate()
    findings: list[Finding] = []
    for decision in evaluation.decisions:
        status, severity = _RULE_STATUS[decision.status]
        findings.append(
            Finding(
                finding_id=f"RULE:{decision.rule_id}",
                category="RULE",
                check_id=decision.rule_id,
                status=status,
                severity=severity,
                message=(
                    f"{decision.reason} [source {decision.source_id} "
                    f"v{decision.version}, {decision.authority_level}]"
                ),
                evidence_ids=tuple(decision.evidence_ids),
            )
        )
    for index, blocker in enumerate(evaluation.blockers):
        findings.append(
            Finding(
                finding_id=f"RULE-BLOCKER:{index}:{blocker}",
                category="RULE",
                check_id=str(blocker),
                status="BLOCKED",
                severity="BLOCKING",
                message=f"Rule evaluation blocker: {blocker}",
                evidence_ids=(f"source:{evaluation.source_sha256}",),
            )
        )
    return tuple(findings)


def findings_from_drawing_standards(validation: Any) -> tuple[Finding, ...]:
    """Convert DrawingStandardsValidation. Missing evidence is SOURCE_REQUIRED."""
    validation.validate()
    findings: list[Finding] = []
    for check_id, result in sorted(validation.checks.items()):
        if result == "PASS":
            status, severity, text = "PASS", "INFO", "Check passed on supplied evidence."
        elif result == "BLOCKED":
            status, severity, text = "BLOCKED", "BLOCKING", "Evidence shows the check is violated."
        else:
            status, severity, text = (
                "SOURCE_REQUIRED",
                "WARNING",
                "Evidence not supplied; the value is not inferred.",
            )
        findings.append(
            Finding(
                finding_id=f"DS:{check_id}",
                category="DRAWING_STANDARDS",
                check_id=check_id,
                status=status,
                severity=severity,
                message=text,
                evidence_ids=tuple(validation.evidence_ids),
            )
        )
    return tuple(findings)


_VALIDATION_STATE = {
    "PASS": ("PASS", "INFO"),
    "NEEDS_REVISION": ("NEEDS_REVIEW", "WARNING"),
    "REJECT": ("BLOCKED", "BLOCKING"),
    "BLOCKED": ("BLOCKED", "BLOCKING"),
    "UNKNOWN": ("UNKNOWN", "WARNING"),
}
_CONFLICT_SEVERITY = {
    "INFO": ("PASS", "INFO"),
    "WARNING": ("NEEDS_REVIEW", "WARNING"),
    "BLOCKING": ("BLOCKED", "BLOCKING"),
}


def findings_from_validation_result(result: Any) -> tuple[Finding, ...]:
    """Convert conflict_validation_contract.ValidationResult into findings.

    An INFO conflict is informational (PASS/INFO). The overall validation state
    is always reported as its own finding so it cannot be hidden by conflicts.
    """
    result.validate()
    evidence = tuple(result.evidence_ids) or (f"validation:{result.validation_id}",)
    state_status, state_severity = _VALIDATION_STATE[result.state]
    findings = [
        Finding(
            finding_id=f"VAL:{result.validation_id}:STATE",
            category="CONFLICT",
            check_id="VALIDATION-STATE",
            status=state_status,
            severity=state_severity,
            message=f"Validation state is {result.state}.",
            evidence_ids=evidence,
        )
    ]
    for conflict in result.conflicts:
        status, severity = _CONFLICT_SEVERITY[conflict.severity]
        findings.append(
            Finding(
                finding_id=f"VAL:{result.validation_id}:{conflict.conflict_id}",
                category="CONFLICT",
                check_id=conflict.code,
                status=status,
                severity=severity,
                message=f"Conflict {conflict.code} ({conflict.severity}).",
                evidence_ids=evidence,
                element_ids=tuple(conflict.affected_elements),
            )
        )
    return tuple(findings)
