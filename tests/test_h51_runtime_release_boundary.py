import unittest

from runtime.runtime_release_gate import evaluate_runtime_release


def ready_runtime_result():
    return {
        "status": "READY_FOR_APPROVAL",
        "blockers": [],
        "contracts": {"status": "VALID", "constraint_map_id": "cm-1", "plan_model_id": "model-1"},
        "semantic_corroboration": {"status": "ACCESSIBLE"},
        "constraint_map": {"map_id": "cm-1", "model_id": "model-1", "evidence_ids": ["ev-1"]},
        "evidence": {"evidence_id": "ev-1", "complete": True, "source_sha256": "src-1", "stages": ["SOURCE","DETECTION","PLAN_MODEL","CONSTRAINT_MAP","LOCKED_IDENTIFICATION","SEMANTIC_CORROBORATION","CHANGE_REQUEST","APPROVED_CHANGE_PLAN","CONTROLLED_EDIT","POST_EDIT_DETECTION","POST_EDIT_DIFF","FINAL_VALIDATION"]},
        "source": {"sha256": "src-1"},
    }


class H51RuntimeReleaseBoundaryTests(unittest.TestCase):
    def test_ready_runtime_derives_release_critical_checks(self):
        result = evaluate_runtime_release(
            ready_runtime_result(),
            workflow_ok=True,
            final_validation_ok=True,
            regression_ok=True,
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_blocked_runtime_cannot_become_release_ready(self):
        runtime = ready_runtime_result()
        runtime["status"] = "BLOCKED"
        runtime["semantic_corroboration"] = {"status": "BLOCKED"}
        result = evaluate_runtime_release(
            runtime,
            workflow_ok=True,
            final_validation_ok=True,
            regression_ok=True,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn(
            "RELEASE_SEMANTIC_CORROBORATION_FAILED",
            result.failure_codes,
        )

    def test_invalid_contracts_block_release_even_with_other_checks_green(self):
        runtime = ready_runtime_result()
        runtime["contracts"] = {"status": "BLOCKED"}
        result = evaluate_runtime_release(
            runtime,
            workflow_ok=True,
            final_validation_ok=True,
            regression_ok=True,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_CONTRACTS_FAILED", result.failure_codes)

    def test_external_failed_check_still_blocks_release(self):
        result = evaluate_runtime_release(
            ready_runtime_result(),
            workflow_ok=False,
            final_validation_ok=True,
            regression_ok=True,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_WORKFLOW_FAILED", result.failure_codes)

    def test_manual_override_fields_cannot_bypass_derived_boundary(self):
        runtime = ready_runtime_result()
        runtime["operator_override"] = True
        runtime["semantic_corroboration"] = {"status": "BLOCKED"}
        result = evaluate_runtime_release(
            runtime,
            workflow_ok=True,
            final_validation_ok=True,
            regression_ok=True,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn(
            "RELEASE_SEMANTIC_CORROBORATION_FAILED",
            result.failure_codes,
        )


if __name__ == "__main__":
    unittest.main()
