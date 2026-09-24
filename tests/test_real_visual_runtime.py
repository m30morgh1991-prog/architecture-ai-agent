import tempfile
import unittest
from pathlib import Path

import fitz

from runtime.real_visual_runtime import RealVisualRuntime


class RealVisualRuntimeTests(unittest.TestCase):
    def test_real_pdf_artifact_is_ingested_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.pdf"
            document = fitz.open()
            page = document.new_page(width=600, height=400)
            page.draw_rect(fitz.Rect(40, 40, 560, 360))
            page.insert_text((70, 90), "PLANTA PRIMER NIVEL")
            page.insert_text((70, 130), "COCINA")
            document.save(path)
            result = RealVisualRuntime().run(
                "real-test-01",
                str(path),
                {"change_type":"FURNITURE","instruction":"rearrange furniture only"},
            )
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["blockers"], ["LOCKED_ELEMENT_UNCERTAIN"])
            self.assertEqual(result["source"]["page_count"], 1)
            self.assertEqual(result["evidence"]["input_type"], "PDF")
            self.assertEqual(
                result["evidence"]["stages"],
                ["SOURCE","DETECTION","PLAN_MODEL","CONSTRAINT_MAP",
                 "LOCKED_IDENTIFICATION","SEMANTIC_CORROBORATION","CHANGE_REQUEST"],
            )
            self.assertFalse(result["evidence"]["complete"])


if __name__ == "__main__":
    unittest.main()
