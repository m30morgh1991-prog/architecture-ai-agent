import unittest
from pathlib import Path

from runtime.headless_plan_validation import validate_real_plan_result
from runtime.real_visual_runtime import RealVisualRuntime


class HeadlessPlanValidationTests(unittest.TestCase):
    def _run(self, filename, execution_id):
        source = Path(__file__).resolve().parents[1] / "test-assets" / "golden-projects" / filename
        return RealVisualRuntime().run(
            execution_id, str(source), {"change_type": "FURNITURE_ONLY", "targets": ["F01"]}
        )

    def test_bagheri7_headless_fixture_validates_without_approving_semantics(self):
        result = validate_real_plan_result(self._run("bagheri7.dwg", "headless-dwg-01"))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["failures"], ())
        self.assertEqual(result["semantic_approval"], "NOT_GRANTED")

    def test_missing_identity_fails_closed(self):
        result = validate_real_plan_result({"source": {}, "evidence": {}, "detection": {}, "contracts": {}, "constraint_map": {}, "locked_element_detection": {"spaces": [], "space_relations": []}})
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("SOURCE_EVIDENCE_SHA_MISMATCH", result["failures"])
        self.assertEqual(result["semantic_approval"], "NOT_GRANTED")


if __name__ == "__main__":
    unittest.main()
