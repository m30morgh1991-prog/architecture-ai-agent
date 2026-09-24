import unittest
from runtime.release_gate import evaluate_release


class ReleaseGateTests(unittest.TestCase):
    def test_integrated_green_release_gate(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": True,
            "regression": True,
            "semantic_corroboration": True,
        })
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_any_missing_gate_blocks_release(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": False,
            "regression": True,
            "semantic_corroboration": True,
        })
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_FINAL_VALIDATION_FAILED", result.failure_codes)

    def test_missing_checks_are_not_assumed_green(self):
        result = evaluate_release({})
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(len(result.failure_codes), 5)
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)


if __name__ == "__main__":
    unittest.main()
