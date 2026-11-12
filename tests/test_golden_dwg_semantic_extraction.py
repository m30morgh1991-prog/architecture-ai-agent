from __future__ import annotations
import json, unittest
from pathlib import Path
from runtime.dwg_semantic_evidence import extract_dwg_evidence, _level_candidate

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"test-assets/golden-understanding/golden_manifest.json"

class TestGoldenDwgSemanticExtraction(unittest.TestCase):
    def test_level_parser_prefers_elevation_value_not_floor_index(self):
        cases = [
            ("LEVEL 2 FFL +3.20 m", "m", 3.20),
            ("طبقه دوم تراز +3.20", "m", 3.20),
            ("FFL +3.20 m", "m", 3.20),
        ]
        for raw, units, expected in cases:
            with self.subTest(raw=raw):
                evidence = _level_candidate(raw, 17, "fixture-sha", units)
                self.assertIsNotNone(evidence)
                self.assertEqual(evidence["status"], "SUPPORTED")
                self.assertAlmostEqual(evidence["elevation"], expected)
                self.assertEqual(evidence["unit"], "m")

    def test_floor_index_alone_is_not_elevation(self):
        self.assertIsNone(_level_candidate("LEVEL 2", 18, "fixture-sha", "m"))

    def test_multiple_elevation_values_fail_closed(self):
        evidence = _level_candidate("FFL +3.20 m / RL +4.10 m", 19, "fixture-sha", "m")
        self.assertIsNotNone(evidence)
        self.assertEqual(evidence["status"], "UNKNOWN")
        self.assertIsNone(evidence["elevation"])
        self.assertEqual(evidence["reason"], "AMBIGUOUS_ELEVATION_VALUES")

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
            self.assertTrue(evidence["layer_table"],case["case_id"])
            self.assertTrue(evidence["layer_counts"],case["case_id"])
            self.assertEqual(evidence["layer_table_status"],"SUPPORTED",case["case_id"])
            self.assertEqual(evidence["semantic_candidates"]["WALLS"]["status"],"SUPPORTED",case["case_id"])
            self.assertEqual(evidence["semantic_candidates"]["COLUMNS"]["status"],"SUPPORTED",case["case_id"])
            self.assertEqual(evidence["semantic_candidates"]["DOORS"]["status"],"UNKNOWN",case["case_id"])
            self.assertEqual(evidence["semantic_candidates"]["WINDOWS"]["status"],"UNKNOWN",case["case_id"])
            self.assertEqual(evidence["scale_unit_evidence"]["status"],"NEEDS_REVIEW",case["case_id"])
            self.assertFalse(evidence["scale_unit_evidence"]["scale_known"],case["case_id"])
            self.assertIn("text",evidence)
            self.assertIn("dimensions",evidence)

if __name__=="__main__":
    unittest.main()
