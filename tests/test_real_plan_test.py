import tempfile
import unittest
from pathlib import Path

import cv2
import fitz
import numpy as np

from runtime.real_visual_runtime import RealVisualRuntime


class RealPlanTestBaseline(unittest.TestCase):
    """Baseline real-plan gate: ingestion must be deterministic and fail closed."""

    def _pdf(self, directory: str) -> str:
        path = Path(directory) / "real-plan-baseline.pdf"
        doc = fitz.open()
        page = doc.new_page(width=800, height=1100)
        page.insert_text((80, 100), "PLANTA ARQUITECTONICA")
        page.draw_rect(fitz.Rect(100, 180, 650, 850), color=(0, 0, 0))
        page.draw_rect(fitz.Rect(200, 300, 240, 340), color=(0, 0, 0), fill=(0, 0, 0))
        page.draw_line((220, 180), (220, 850), color=(0, 0, 0))
        page.draw_line((500, 180), (500, 850), color=(0, 0, 0))
        doc.save(path)
        doc.close()
        return str(path)

    def test_real_plan_baseline_preserves_source_identity_and_blocks_uncertain_structure(self):
        runtime = RealVisualRuntime()
        with tempfile.TemporaryDirectory() as tmp:
            source = self._pdf(tmp)
            result = runtime.run(
                "real-plan-baseline-01",
                source,
                {"change_type": "FURNITURE_ONLY", "targets": ["F01"]},
            )

        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["blockers"])
        self.assertEqual(result["source"]["sha256"], result["evidence"]["source_sha256"])
        self.assertEqual(result["source"]["sha256"], result["detection"]["artifact_sha256"])
        self.assertEqual(result["constraint_map"]["map_id"], result["contracts"]["constraint_map_id"])
        self.assertEqual(result["constraint_map"]["model_id"], result["contracts"]["plan_model_id"])
        self.assertIn(result["evidence"]["evidence_id"], result["constraint_map"]["evidence_ids"])
        self.assertIsNone(result["next_stage"])

    def test_raster_plan_baseline_remains_fail_closed(self):
        runtime = RealVisualRuntime()
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "real-plan-baseline.png"
            image = np.full((800, 600, 3), 255, dtype=np.uint8)
            cv2.rectangle(image, (80, 80), (520, 720), (0, 0, 0), 4)
            cv2.imwrite(str(source), image)
            result = runtime.run(
                "real-plan-baseline-02",
                str(source),
                {"change_type": "FURNITURE_ONLY", "targets": ["F01"]},
            )

        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["blockers"])
        self.assertEqual(result["locked_element_detection"]["status"], "UNKNOWN")
        self.assertIsNone(result["next_stage"])


if __name__ == "__main__":
    unittest.main()
