import unittest
from pathlib import Path

from runtime.real_visual_runtime import RealVisualRuntime


class RealPlanTestBaseline(unittest.TestCase):
    """Real DWG golden-project gate: source identity must be preserved and uncertainty must block."""

    def _run(self, filename: str, execution_id: str):
        source = Path(__file__).resolve().parents[1] / "test-assets" / "golden-projects" / filename
        self.assertTrue(source.is_file())
        return RealVisualRuntime().run(
            execution_id,
            str(source),
            {"change_type": "FURNITURE_ONLY", "targets": ["F01"]},
        )

    def test_bagheri7_dwg_preserves_identity_and_blocks_uncertain_structure(self):
        result = self._run("bagheri7.dwg", "real-plan-dwg-01")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["blockers"])
        self.assertEqual(result["source"]["sha256"], result["evidence"]["source_sha256"])
        self.assertEqual(result["source"]["sha256"], result["detection"]["artifact_sha256"])
        self.assertGreater(result["detection"]["dwg_entity_count"], 0)
        self.assertGreater(result["contracts"]["element_count"], 0)
        self.assertGreater(len(result["locked_element_detection"]["candidates"]), 0)
        self.assertIn("OUTER_BOUNDARY", {x["element_type"] for x in result["locked_element_detection"]["candidates"]})
        self.assertEqual(result["constraint_map"]["map_id"], result["contracts"]["constraint_map_id"])
        self.assertEqual(result["constraint_map"]["model_id"], result["contracts"]["plan_model_id"])
        self.assertIn(result["evidence"]["evidence_id"], result["constraint_map"]["evidence_ids"])
        self.assertIn("dwg_geometry", result["locked_element_detection"])
        self.assertIn("spaces", result["locked_element_detection"])
        self.assertIn("space_relations", result["locked_element_detection"])
        self.assertGreaterEqual(result["locked_element_detection"]["dwg_geometry"]["inventory_count"], 0)
        self.assertIsInstance(result["locked_element_detection"]["spaces"], list)
        self.assertIsInstance(result["locked_element_detection"]["space_relations"], list)
        self.assertTrue(all(x["type"] in {"SHARED_BOUNDARY", "CONTAINS", "OVERLAPS", "DISCONNECTED"} for x in result["locked_element_detection"]["space_relations"]))
        self.assertTrue(all(x["status"] == "UNKNOWN" for x in result["locked_element_detection"]["space_relations"]))
        self.assertIn("dwg_geometry", result["locked_element_detection"])
        self.assertIn("spaces", result["locked_element_detection"])
        self.assertIn("space_relations", result["locked_element_detection"])
        self.assertIsInstance(result["locked_element_detection"]["spaces"], list)
        self.assertIsInstance(result["locked_element_detection"]["space_relations"], list)
        self.assertEqual(result["drawing_standards"]["status"], "UNKNOWN")
        self.assertIsNone(result["next_stage"])

    def test_afifiiiii_dwg_also_fails_closed(self):
        result = self._run("afifiiiii.end.edit3.dwg", "real-plan-dwg-02")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["blockers"])
        self.assertEqual(result["evidence"]["input_type"], "DWG")
        self.assertGreater(result["detection"]["dwg_entity_count"], 0)
        self.assertGreater(result["contracts"]["element_count"], 0)
        self.assertGreater(len(result["locked_element_detection"]["candidates"]), 0)
        self.assertIsNone(result["next_stage"])


if __name__ == "__main__":
    unittest.main()
