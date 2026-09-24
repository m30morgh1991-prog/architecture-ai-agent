import tempfile
import unittest
from pathlib import Path

import fitz

from runtime.locked_element_detection import ConservativeLockedElementDetector


class LockedElementDetectionTests(unittest.TestCase):
    def test_pdf_vector_evidence_finds_plan_titles_but_stays_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.pdf"
            document = fitz.open()
            page = document.new_page(width=1200, height=1800)
            for i, title in enumerate(
                ("PLANTA PRIMER NIVEL", "PLANTA SEGUNDO NIVEL",
                 "PLANTA TERCER NIVEL", "PLANTA AZOTEA")
            ):
                x = 120 + i * 260
                page.draw_rect(fitz.Rect(x, 300, x + 200, 1500))
                page.insert_text((x + 10, 1540), title)
            document.save(path)

            result = ConservativeLockedElementDetector().detect(
                str(path), "abc123"
            )

            self.assertEqual(result["status"], "UNKNOWN")
            self.assertEqual(len(result["plan_panels"]), 4)
            self.assertEqual(result["locked_element_types"], [])
            self.assertIn("COLUMNS", result["unresolved_fixed_element_types"])
            self.assertIn("WALLS", result["unresolved_fixed_element_types"])

    def test_locked_candidate_cannot_pass_with_low_confidence(self):
        # Regression is covered through the candidate contract itself.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.pdf"
            document = fitz.open()
            page = document.new_page(width=600, height=600)
            page.draw_rect(fitz.Rect(50, 50, 550, 550))
            page.insert_text((80, 540), "PLANTA PRIMER NIVEL")
            document.save(path)
            result = ConservativeLockedElementDetector().detect(
                str(path), "def456"
            )
            for candidate in result["candidates"]:
                self.assertEqual(candidate["status"], "UNKNOWN")
                self.assertLess(candidate["confidence"], 0.95)


if __name__ == "__main__":
    unittest.main()
