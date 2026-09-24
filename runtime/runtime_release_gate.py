"""H51 runtime-to-release gate adapter.

Derives release-critical checks from the runtime result instead of allowing
callers to manually assert semantic/contract readiness.
"""
from __future__ import annotations

from typing import Any

from .release_gate import ReleaseGateResult, evaluate_release


def evaluate_runtime_release(
    runtime_result: dict[str, Any],
    *,
    workflow_ok: bool,
    final_validation_ok: bool,
    regression_ok: bool,
) -> ReleaseGateResult:
    """Evaluate the frozen release boundary from an actual runtime result.

    Contracts and semantic corroboration are derived from runtime evidence.
    Workflow, final validation, and regression remain explicit CI/system
    checks because they are external to a single visual-runtime result.
    """
    if not isinstance(runtime_result, dict):
        return evaluate_release({
            "contracts": False,
            "workflow": workflow_ok,
            "final_validation": final_validation_ok,
            "regression": regression_ok,
            "semantic_corroboration": False,
        })

    contracts = runtime_result.get("contracts") or {}
    semantics = runtime_result.get("semantic_corroboration") or {}

    return evaluate_release({
        "contracts": contracts.get("status") == "VALID",
        "workflow": workflow_ok,
        "final_validation": final_validation_ok,
        "regression": regression_ok,
        "semantic_corroboration": semantics.get("status") == "ACCESSIBLE",
    })
