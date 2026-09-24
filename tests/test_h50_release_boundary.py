import unittest

from runtime.release_gate import evaluate_release


class H50ReleaseBoundaryTests(unittest.TestCase):
    def test_all_required_release_checks_must_pass(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": True,
            "regression": True,
            "semantic_corroboration": True,
        })
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])
        self.assertTrue(all(result.checks.values()))

    def test_missing_required_check_blocks_release(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": True,
            "regression": True,
        })
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)

    def test_false_required_check_blocks_release(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": True,
            "regression": True,
            "semantic_corroboration": False,
        })
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(
            result.failure_codes,
            ["RELEASE_SEMANTIC_CORROBORATION_FAILED"],
        )

    def test_extra_non_required_check_cannot_bypass_required_boundary(self):
        result = evaluate_release({
            "contracts": True,
            "workflow": True,
            "final_validation": True,
            "regression": True,
            "semantic_corroboration": False,
            "operator_override": True,
        })
        self.assertEqual(result.status, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
