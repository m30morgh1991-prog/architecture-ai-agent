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


class H54ConstraintMapBindingTests(unittest.TestCase):
    def green(self, runtime=None):
        return evaluate_runtime_release(runtime or ready_runtime_result(), workflow_ok=True, final_validation_ok=True, regression_ok=True)

    def test_matching_constraint_map_identity_passes(self):
        self.assertEqual(self.green().status, "PASS")

    def test_mismatched_constraint_map_identity_blocks(self):
        runtime = ready_runtime_result()
        runtime["constraint_map"]["map_id"] = "cm-2"
        result = self.green(runtime)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_CONTRACTS_FAILED", result.failure_codes)

    def test_contract_map_identity_cannot_replace_missing_runtime_map(self):
        runtime = ready_runtime_result()
        runtime["constraint_map"] = {}
        result = self.green(runtime)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_CONTRACTS_FAILED", result.failure_codes)

    def test_runtime_map_identity_cannot_replace_missing_contract_binding(self):
        runtime = ready_runtime_result()
        runtime["contracts"] = {"status": "VALID"}
        result = self.green(runtime)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_CONTRACTS_FAILED", result.failure_codes)


if __name__ == "__main__":
    unittest.main()
