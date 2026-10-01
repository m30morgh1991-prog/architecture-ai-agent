import unittest
from pathlib import Path

from runtime.real_visual_runtime import RealVisualRuntime


class RealVisualRuntimeTests(unittest.TestCase):
    def test_real_dwg_artifact_is_ingested_and_fail_closed(self):
        source = Path(__file__).resolve().parents[1] / "test-assets" / "golden-projects" / "bagheri7.dwg"
        self.assertTrue(source.is_file())

        result = RealVisualRuntime().run(
            "real-dwg-01",
            str(source),
            {"change_type": "FURNITURE", "instruction": "rearrange furniture only"},
        )

        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["blockers"], ["LOCKED_ELEMENT_UNCERTAIN"])
        self.assertEqual(result["evidence"]["input_type"], "DWG")
        self.assertGreater(result["detection"]["dwg_entity_count"], 0)
        self.assertEqual(result["source"]["page_count"], 1)
        self.assertEqual(result["source"]["sha256"], result["evidence"]["source_sha256"])
        self.assertFalse(result["evidence"]["complete"])
        self.assertIsNone(result["next_stage"])


if __name__ == "__main__":
    unittest.main()
