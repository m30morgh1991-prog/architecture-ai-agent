"""H52 hardening for runtime release readiness.

A release decision must not be derived from component checks alone: the
runtime's top-level state must explicitly be READY_FOR_APPROVAL.
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
    if not isinstance(runtime_result, dict):
        return evaluate_release({
            "contracts": False, "workflow": workflow_ok,
            "final_validation": final_validation_ok, "regression": regression_ok,
            "semantic_corroboration": False,
        })

    runtime_ready = runtime_result.get("status") == "READY_FOR_APPROVAL"
    contracts = runtime_result.get("contracts") or {}
    semantics = runtime_result.get("semantic_corroboration") or {}

    return evaluate_release({
        "contracts": runtime_ready and contracts.get("status") == "VALID",
        "workflow": workflow_ok,
        "final_validation": final_validation_ok,
        "regression": regression_ok,
        "semantic_corroboration": runtime_ready and semantics.get("status") == "ACCESSIBLE",
    })
