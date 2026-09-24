from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ReleaseGateResult:
    status: str
    checks: dict[str, bool]
    failure_codes: list[str]


def evaluate_release(checks: dict[str, bool]) -> ReleaseGateResult:
    required = ("contracts", "workflow", "final_validation", "regression")
    normalized = {name: bool(checks.get(name, False)) for name in required}
    failures = [f"RELEASE_{name.upper()}_FAILED" for name, ok in normalized.items() if not ok]
    return ReleaseGateResult("PASS" if not failures else "BLOCKED", normalized, failures)
