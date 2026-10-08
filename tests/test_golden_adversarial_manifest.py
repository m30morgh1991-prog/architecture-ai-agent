import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "test-assets" / "golden-understanding" / "adversarial_manifest.json"
ALLOWED = {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}
REQUIRED_CATEGORIES = {
    "SOURCE_REQUIRED", "SOURCE_IDENTITY", "DETECTION_UNCERTAIN", "CONTRADICTION",
    "MISSING_EVIDENCE", "LOCKED_ELEMENT_UNCERTAIN", "SCALE_UNKNOWN",
    "EDITOR_GUARD_UNVERIFIED", "POST_EDIT_DETECTION_MISSING", "UNSUPPORTED_CAPABILITY",
}

class GoldenAdversarialManifestTests(unittest.TestCase):
    def test_every_fail_closed_category_has_a_case(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        categories = {case["category"] for case in data["cases"]}
        self.assertEqual(categories, REQUIRED_CATEGORIES)
        for case in data["cases"]:
            self.assertIn(case["expected_decision"], ALLOWED)
            self.assertNotEqual(case["expected_decision"], "PASS")

    def test_duplicate_case_ids_are_rejected(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        ids = [case["case_id"] for case in data["cases"]]
        self.assertEqual(len(ids), len(set(ids)))

if __name__ == "__main__":
    unittest.main()
