from __future__ import annotations
import json, unittest
from pathlib import Path
from runtime.dwg_semantic_evidence import extract_dwg_evidence

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"test-assets/golden-understanding/golden_manifest.json"

class TestGoldenDwgSemanticExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_preserved_golden_dwgs_have_readable_source_evidence(self):
        for case in self.manifest["cases"]:
            source=ROOT/case["source_path"]
            self.assertTrue(source.is_file(), case["case_id"])
            evidence=extract_dwg_evidence(source)
            self.assertEqual(evidence["source_profile"]["sha256"],case["source_sha256"],case["case_id"])
            self.assertEqual(evidence["source_profile"]["source_class"],"ENGINEERING_PLAN")
            self.assertTrue(evidence["authority"]["read_only"])
            self.assertFalse(evidence["authority"]["semantic_authority"])
            self.assertTrue(evidence["entity_counts"],case["case_id"])
            self.assertIn("text",evidence)
            self.assertIn("dimensions",evidence)

if __name__=="__main__":
    unittest.main()
