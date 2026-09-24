import unittest
from runtime.release_gate import evaluate_release


class H46ReleaseGateTests(unittest.TestCase):
    def test_all_required_gates_pass(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": True,
            "regression": True,
            "semantic_corroboration": True,
        })
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_missing_semantic_corroboration_blocks(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": True,
            "regression": True,
        })
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)


if __name__ == "__main__":
    unittest.main()
