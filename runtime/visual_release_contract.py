"""H37 visual release contract.

The final release decision must consume semantic corroboration explicitly.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisualReleaseDecision:
    status: str
    failure_codes: tuple[str, ...]

    def validate(self) -> None:
        if self.status not in {"PASS", "BLOCKED"}:
            raise ValueError("INVALID_VISUAL_RELEASE_STATUS")


def evaluate_visual_release(
    *,
    contracts: bool,
    workflow: bool,
    final_validation: bool,
    regression: bool,
    semantic_corroboration: str,
) -> VisualReleaseDecision:
    failures: list[str] = []
    for name, ok in (
        ("contracts", contracts),
        ("workflow", workflow),
        ("final_validation", final_validation),
        ("regression", regression),
    ):
        if not ok:
            failures.append(f"RELEASE_{name.upper()}_FAILED")

    if semantic_corroboration != "ACCESSIBLE":
        failures.append("RELEASE_SEMANTIC_CORROBORATION_FAILED")

    result = VisualReleaseDecision(
        "PASS" if not failures else "BLOCKED",
        tuple(failures),
    )
    result.validate()
    return result
