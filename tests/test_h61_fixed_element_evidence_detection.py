import tempfile
import unittest
from pathlib import Path

import fitz

from runtime.locked_element_detection import ConservativeLockedElementDetector


class FixedElementEvidenceDetectionH61(unittest.TestCase):
    def test_pdf_vector_evidence_yields_conservative_structural_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "architectural-plan.pdf"
            doc = fitz.open()
            page = doc.new_page(width=800, height=1100)
            page.insert_text((80, 100), "PLANTA ARQUITECTONICA")
            page.draw_line((120, 450), (120, 1000), color=(0, 0, 0))
            page.draw_line((680, 450), (680, 1000), color=(0, 0, 0))
            page.draw_line((120, 450), (680, 450), color=(0, 0, 0))
            page.draw_line((120, 1000), (680, 1000), color=(0, 0, 0))
            page.draw_line((300, 450), (300, 1000), color=(0, 0, 0))
            page.draw_line((500, 450), (500, 1000), color=(0, 0, 0))
            page.draw_rect(fitz.Rect(285, 600, 315, 630), color=(0, 0, 0), fill=(0, 0, 0))
            doc.save(path)
            doc.close()

            result = ConservativeLockedElementDetector().detect(str(path), "sha-h61")

        self.assertEqual(result["status"], "UNKNOWN")
        types = {candidate["element_type"] for candidate in result["candidates"]}
        self.assertIn("COLUMNS", types)
        self.assertIn("OUTER_BOUNDARY", types)
        self.assertIn("OVERALL_PLAN_FORM", types)
        self.assertIn("WALLS", types)
        self.assertNotIn("LOCKED", {candidate["status"] for candidate in result["candidates"]})
        self.assertIn("DOORS", result["unresolved_fixed_element_types"])
        self.assertIn("WINDOWS", result["unresolved_fixed_element_types"])


if __name__ == "__main__":
    unittest.main()
