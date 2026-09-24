import unittest
from runtime.visual_release_contract import evaluate_visual_release

class VisualReleaseContractTests(unittest.TestCase):
    def test_unknown_semantics_blocks_release(self):
        result = evaluate_visual_release(
            contracts=True, workflow=True, final_validation=True,
            regression=True, semantic_corroboration="UNKNOWN")
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)

    def test_accessible_semantics_allows_release(self):
        result = evaluate_visual_release(
            contracts=True, workflow=True, final_validation=True,
            regression=True, semantic_corroboration="ACCESSIBLE")
        self.assertEqual(result.status, "PASS")

    def test_any_other_gate_failure_still_blocks(self):
        result = evaluate_visual_release(
            contracts=True, workflow=False, final_validation=True,
            regression=True, semantic_corroboration="ACCESSIBLE")
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_WORKFLOW_FAILED", result.failure_codes)

if __name__ == "__main__":
    unittest.main()
