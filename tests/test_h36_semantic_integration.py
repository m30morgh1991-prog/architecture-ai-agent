import tempfile
import unittest
from pathlib import Path
import fitz

from runtime.real_visual_runtime import RealVisualRuntime

class H36SemanticIntegrationTests(unittest.TestCase):
    def test_runtime_exposes_corroboration_and_fail_closes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.pdf"
            document = fitz.open()
            page = document.new_page(width=600, height=400)
            page.draw_rect(fitz.Rect(40, 40, 560, 360))
            page.insert_text((70, 90), "PLANTA PRIMER NIVEL")
            document.save(path)
            result = RealVisualRuntime().run(
                "H36-01", str(path), {"change_type":"FURNITURE","instruction":"rearrange furniture only"}
            )
            self.assertIn("semantic_corroboration", result)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["semantic_corroboration"]["status"], "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
