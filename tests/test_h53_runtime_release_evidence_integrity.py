import unittest

from runtime.runtime_release_gate import evaluate_runtime_release


def ready_runtime_result():
    return {
        "status": "READY_FOR_APPROVAL",
        "blockers": [],
        "contracts": {"status": "VALID", "constraint_map_id": "cm-1"},
        "semantic_corroboration": {"status": "ACCESSIBLE"},
        "constraint_map": {"map_id": "cm-1"},
        "evidence": {"evidence_id": "ev-1", "complete": True},
    }


class H53RuntimeReleaseEvidenceIntegrityTests(unittest.TestCase):
    def green(self, runtime=None):
        return evaluate_runtime_release(
            runtime or ready_runtime_result(),
            workflow_ok=True,
            final_validation_ok=True,
            regression_ok=True,
        )

    def test_complete_ready_runtime_passes(self):
        result = self.green()
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_hidden_blockers_cannot_be_ignored(self):
        runtime = ready_runtime_result()
        runtime["blockers"] = ["LOCKED_ELEMENT_UNCERTAIN"]
        result = self.green(runtime)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_CONTRACTS_FAILED", result.failure_codes)
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)

    def test_incomplete_evidence_blocks_release(self):
        runtime = ready_runtime_result()
        runtime["evidence"] = {"evidence_id": "ev-1", "complete": False}
        result = self.green(runtime)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)

    def test_missing_constraint_map_blocks_release(self):
        runtime = ready_runtime_result()
        runtime["constraint_map"] = {}
        runtime["contracts"] = {"status": "VALID"}
        result = self.green(runtime)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_CONTRACTS_FAILED", result.failure_codes)

    def test_missing_evidence_id_blocks_release(self):
        runtime = ready_runtime_result()
        runtime["evidence"] = {"complete": True}
        result = self.green(runtime)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)


if __name__ == "__main__":
    unittest.main()
