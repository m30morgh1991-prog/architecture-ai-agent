import unittest

from runtime.runtime_release_gate import evaluate_runtime_release


REQUIRED_STAGES = [
    "SOURCE",
    "DETECTION",
    "PLAN_MODEL",
    "CONSTRAINT_MAP",
    "LOCKED_IDENTIFICATION",
    "SEMANTIC_CORROBORATION",
    "CHANGE_REQUEST",
    "APPROVED_CHANGE_PLAN",
    "CONTROLLED_EDIT",
    "POST_EDIT_DETECTION",
    "POST_EDIT_DIFF",
    "FINAL_VALIDATION",
]


def ready_runtime_result():
    return {
        "status": "READY_FOR_APPROVAL",
        "blockers": [],
        "contracts": {"status": "VALID", "constraint_map_id": "cm-1", "plan_model_id": "model-1"},
        "semantic_corroboration": {"status": "ACCESSIBLE"},
        "constraint_map": {"map_id": "cm-1", "model_id": "model-1", "evidence_ids": ["ev-1"]},
        "evidence": {
            "evidence_id": "ev-1",
            "complete": True,
            "source_sha256": "src-1",
            "stages": REQUIRED_STAGES,
        },
        "source": {"sha256": "src-1"},
    }


class H58FinalIntegrityGateTests(unittest.TestCase):
    def green(self, runtime=None, **checks):
        return evaluate_runtime_release(
            runtime or ready_runtime_result(),
            workflow_ok=checks.get("workflow_ok", True),
            final_validation_ok=checks.get("final_validation_ok", True),
            regression_ok=checks.get("regression_ok", True),
        )

    def assert_blocks(self, runtime):
        self.assertEqual(self.green(runtime).status, "BLOCKED")

    def test_complete_integrity_chain_passes(self):
        result = self.green()
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_plan_model_identity_must_match_constraint_map(self):
        x = ready_runtime_result()
        x["constraint_map"]["model_id"] = "model-2"
        self.assert_blocks(x)

    def test_contract_plan_model_identity_is_required(self):
        x = ready_runtime_result()
        del x["contracts"]["plan_model_id"]
        self.assert_blocks(x)

    def test_evidence_stages_must_be_complete_and_exact(self):
        x = ready_runtime_result()
        x["evidence"]["stages"] = REQUIRED_STAGES[:-1]
        self.assert_blocks(x)

    def test_complete_flag_cannot_override_invalid_stage_chain(self):
        x = ready_runtime_result()
        x["evidence"]["complete"] = True
        x["evidence"]["stages"] = ["SOURCE"]
        self.assert_blocks(x)

    def test_each_external_release_check_remains_required(self):
        for key in ("workflow_ok", "final_validation_ok", "regression_ok"):
            checks = {key: False}
            self.assert_blocks(ready_runtime_result()) if False else None
            result = self.green(ready_runtime_result(), **checks)
            self.assertEqual(result.status, "BLOCKED")

    def test_hidden_blocker_blocks_even_when_everything_else_is_green(self):
        x = ready_runtime_result()
        x["blockers"] = ["LOCKED_ELEMENT_UNCERTAIN"]
        self.assert_blocks(x)


if __name__ == "__main__":
    unittest.main()
