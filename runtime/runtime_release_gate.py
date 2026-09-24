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
    blockers_clear = not bool(runtime_result.get("blockers") or [])
    contracts = runtime_result.get("contracts") or {}
    semantics = runtime_result.get("semantic_corroboration") or {}
    evidence = runtime_result.get("evidence") or {}
    constraint_map = runtime_result.get("constraint_map") or {}
    source = runtime_result.get("source") or {}\n    evidence_source_bound = bool(evidence.get("source_sha256")) and bool(source.get("sha256")) and evidence.get("source_sha256") == source.get("sha256")\n    evidence_complete = evidence.get("complete") is True and bool(evidence.get("evidence_id")) and evidence_source_bound
    constraint_map_id = constraint_map.get("map_id")
    contract_constraint_map_id = contracts.get("constraint_map_id")
    constraint_map_bound = bool(constraint_map_id) and bool(contract_constraint_map_id) and constraint_map_id == contract_constraint_map_id

    return evaluate_release({
        "contracts": runtime_ready and blockers_clear and contracts.get("status") == "VALID" and constraint_map_bound,
        "workflow": workflow_ok,
        "final_validation": final_validation_ok,
        "regression": regression_ok,
        "semantic_corroboration": runtime_ready and blockers_clear and semantics.get("status") == "ACCESSIBLE" and evidence_complete,
    })
