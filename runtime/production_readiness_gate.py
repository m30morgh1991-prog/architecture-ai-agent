"""Production readiness boundary for the Architecture AI Agent runtime."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionReadinessResult:
    status: str
    checks: dict[str, bool]
    failure_codes: list[str]


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
    checks = {
        "runtime_release": bool(runtime_release_ok),
        "real_runtime_e2e": bool(real_runtime_e2e_ok),
        "fixed_element_detection": bool(fixed_element_detection_ok),
        "complete_visual_evidence": bool(complete_visual_evidence_ok),
    }
    failures = [
        f"PRODUCTION_{name.upper()}_FAILED"
        for name, ok in checks.items()
        if not ok
    ]
    return ProductionReadinessResult(
        status="PASS" if not failures else "BLOCKED",
        checks=checks,
        failure_codes=failures,
    )
