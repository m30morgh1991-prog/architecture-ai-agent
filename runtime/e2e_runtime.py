"""H42-H46 fail-closed end-to-end runtime boundary."""
from dataclasses import dataclass
from typing import Any

from .visual_orchestration import VisualExecutionBoundary
from .final_validation import validate_post_edit
from .release_gate import evaluate_release


@dataclass(frozen=True)
class E2ERuntimeResult:
    visual: Any
    execution: dict[str, Any]
    final_validation: Any
    release: Any


class E2ERuntimeBoundary:
    def __init__(self, visual_boundary: VisualExecutionBoundary, execute_fn):
        self.visual_boundary = visual_boundary
        self.execute_fn = execute_fn

    def run(
        self,
        execution_id: str,
        request: dict[str, Any],
        document: Any,
        approved_change_plan: dict[str, Any],
        plan: dict[str, Any],
    ) -> E2ERuntimeResult:
        if approved_change_plan.get("status") != "APPROVED":
            return E2ERuntimeResult(
                visual=None,
                execution={"status": "REJECT", "failure_codes": ["APPROVED_CHANGE_PLAN_REQUIRED"]},
                final_validation=None,
                release=evaluate_release({
                    "contracts": False,
                    "workflow": False,
                    "final_validation": False,
                    "regression": False,
                    "semantic_corroboration": False,
                }),
            )

        visual = self.visual_boundary.render(
            execution_id, request, document, approved_change_plan
        )
        execution = self.execute_fn(plan, request)

        diff_payload = execution.get("post_edit_diff", {}) if isinstance(execution, dict) else {}
        diff_payload = dict(diff_payload)
        if "locked_delta_ids" not in diff_payload and "unauthorized_delta_ids" not in diff_payload:
            diff_payload = {"locked_delta_ids": [], "unauthorized_delta_ids": []}
        final_validation = validate_post_edit(diff_payload)

        execution_data = execution if isinstance(execution, dict) else {}
        release = evaluate_release({
            "contracts": execution_data.get("contracts_ok", False),
            "workflow": execution_data.get("workflow_ok", False),
            "final_validation": final_validation.status == "PASS",
            "regression": execution_data.get("regression_ok", False),
            "semantic_corroboration": execution_data.get("semantic_corroboration_ok", False),
        })
        if final_validation.status != "PASS":
            execution = {
                **execution_data,
                "status": "REJECT",
                "failure_codes": final_validation.failure_codes,
            }
        return E2ERuntimeResult(
            visual=visual,
            execution=execution,
            final_validation=final_validation,
            release=release,
        )
