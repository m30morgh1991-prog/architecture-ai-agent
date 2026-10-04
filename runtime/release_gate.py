"""Evidence-backed final release gate.

Release readiness must be based on explicit evidence states, not truthy
caller-provided booleans.
"""
from dataclasses import dataclass


_REQUIRED = (
    "contracts",
    "workflow",
    "final_validation",
    "regression",
    "semantic_corroboration",
    "audit",
    "idempotency",
    "runtime",
)


@dataclass(frozen=True)
class ReleaseGateResult:
    status: str
    checks: dict[str, bool]
    failure_codes: list[str]


def evaluate_release(checks: dict[str, object]) -> ReleaseGateResult:
    normalized = {}
    failures = []
    for name in _REQUIRED:
        value = checks.get(name)
        ok = value is True
        normalized[name] = ok
        if not ok:
            failures.append(f"RELEASE_{name.upper()}_FAILED")
    return ReleaseGateResult(
        "PASS" if not failures else "BLOCKED",
        normalized,
        failures,
    )
