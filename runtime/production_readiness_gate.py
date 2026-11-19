"""Production readiness boundary for the Architecture AI Agent runtime."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionReadinessResult:
    status: str
    checks: dict[str, bool]
    failure_codes: list[str]

    def validate(self) -> None:
        if self.status not in {"PASS", "BLOCKED"}:
            raise ValueError("PRODUCTION_READINESS_STATUS_INVALID")
        if set(self.checks) != set(REQUIRED_CHECKS):
            raise ValueError("PRODUCTION_READINESS_CHECKS_INCOMPLETE")
        if any(type(value) is not bool for value in self.checks.values()):
            raise ValueError("PRODUCTION_READINESS_CHECK_TYPE_INVALID")
        if self.status == "PASS" and (
            any(value is not True for value in self.checks.values()) or self.failure_codes
        ):
            raise ValueError("PRODUCTION_READINESS_FALSE_PASS")
        if self.status == "BLOCKED" and not self.failure_codes:
            raise ValueError("PRODUCTION_READINESS_BLOCKER_MISSING")


REQUIRED_CHECKS = (
    "runtime_release",
    "real_runtime_e2e",
    "fixed_element_detection",
    "complete_visual_evidence",
)


def evaluate_production_readiness(
    *,
    runtime_release_ok: bool,
    real_runtime_e2e_ok: bool,
    fixed_element_detection_ok: bool,
    complete_visual_evidence_ok: bool,
) -> ProductionReadinessResult:
    raw_checks = {
        "runtime_release": runtime_release_ok,
        "real_runtime_e2e": real_runtime_e2e_ok,
        "fixed_element_detection": fixed_element_detection_ok,
        "complete_visual_evidence": complete_visual_evidence_ok,
    }
    checks = {name: value is True for name, value in raw_checks.items()}
    failures = [
        f"PRODUCTION_{name.upper()}_FAILED"
        for name, ok in checks.items()
        if not ok
    ]
    result = ProductionReadinessResult(
        status="PASS" if not failures else "BLOCKED",
        checks=checks,
        failure_codes=failures,
    )
    result.validate()
    return result
