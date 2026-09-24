import tempfile
import unittest
from pathlib import Path

import cv2
import fitz
import numpy as np

from runtime.real_visual_runtime import RealVisualRuntime


class H59RealRuntimeE2EGateTests(unittest.TestCase):
    def _pdf(self, directory: str) -> str:
        path = Path(directory) / "real-plan.pdf"
        document = fitz.open()
        page = document.new_page(width=800, height=1100)
        page.insert_text((80, 100), "PLANTA ARQUITECTONICA")
        page.draw_rect(fitz.Rect(100, 180, 650, 850), color=(0, 0, 0))
        page.draw_line((220, 180), (220, 850), color=(0, 0, 0))
        page.draw_line((500, 180), (500, 850), color=(0, 0, 0))
        document.save(path)
        document.close()
        return str(path)

    def test_real_pdf_path_reaches_structured_runtime_and_fails_closed_on_uncertain_fixed_elements(self):
        runtime = RealVisualRuntime()
        with tempfile.TemporaryDirectory() as tmp:
            source = self._pdf(tmp)
            result = runtime.run(
                "exec-h59-real-pdf",
                source,
                {"change_type": "FURNITURE_ONLY", "targets": ["F01"]},
            )

        self.assertEqual(result["source"]["sha256"], result["evidence"]["source_sha256"])
        self.assertEqual(result["contracts"]["status"], "VALID")
        self.assertEqual(result["constraint_map"]["map_id"], result["contracts"]["constraint_map_id"])
        self.assertEqual(result["constraint_map"]["model_id"], result["contracts"]["plan_model_id"])
        self.assertIn(result["evidence"]["evidence_id"], result["constraint_map"]["evidence_ids"])
        self.assertEqual(
            result["evidence"]["stages"],
            [
                "SOURCE", "DETECTION", "PLAN_MODEL", "CONSTRAINT_MAP",
                "LOCKED_IDENTIFICATION", "SEMANTIC_CORROBORATION", "CHANGE_REQUEST",
            ],
        )
        self.assertFalse(result["evidence"]["complete"])
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["blockers"])
        self.assertIsNone(result["next_stage"])

    def test_real_raster_path_is_never_approved_without_fixed_element_semantics(self):
        runtime = RealVisualRuntime()
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "real-plan.png"
            image = np.full((800, 600, 3), 255, dtype=np.uint8)
            cv2.rectangle(image, (80, 80), (520, 720), (0, 0, 0), 4)
            cv2.imwrite(str(source), image)
            result = runtime.run(
                "exec-h59-real-raster",
                str(source),
                {"change_type": "FURNITURE_ONLY", "targets": ["F01"]},
            )

        self.assertEqual(result["source"]["sha256"], result["evidence"]["source_sha256"])
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["blockers"])
        self.assertEqual(result["locked_element_detection"]["status"], "UNKNOWN")
        self.assertEqual(
            result["locked_element_detection"]["unresolved_fixed_element_types"],
            ["COLUMNS", "OUTER_BOUNDARY", "WALLS", "DOORS", "WINDOWS", "OVERALL_PLAN_FORM"],
        )
        self.assertIsNone(result["next_stage"])


if __name__ == "__main__":
    unittest.main()
