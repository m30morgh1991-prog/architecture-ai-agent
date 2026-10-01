import unittest
from pathlib import Path
from runtime.drawing_metadata_extractor import extract_drawing_standard_metadata

class DrawingMetadataExtractorTests(unittest.TestCase):
    def test_real_golden_dwgs_expose_native_evidence_shape(self):
        root=Path(__file__).resolve().parents[1]/"test-assets"/"golden-projects"
        for name in ("bagheri7.dwg","afifiiiii.end.edit3.dwg"):
            result=extract_drawing_standard_metadata(str(root/name),"DWG")
            for key in ("scale_units_consistent","dimensions_geometry_associated","view_section_identity","sheet_layout_valid","title_block_fields_valid","cross_view_consistent","evidence_ids","native_drawing_evidence"):
                self.assertIn(key,result)
            self.assertIsInstance(result["evidence_ids"],list)
            self.assertIsInstance(result["native_drawing_evidence"],dict)
            self.assertIn("dimension_evidence",result["native_drawing_evidence"])
            self.assertIn("view_evidence",result["native_drawing_evidence"])
            self.assertIn("title_block_evidence",result["native_drawing_evidence"])

    def test_unknown_is_preserved_for_unsupported_input(self):
        result=extract_drawing_standard_metadata("/tmp/not-a-real-dwg.dwg","OTHER")
        self.assertIsNone(result["scale_units_consistent"])
        self.assertEqual(result["evidence_ids"],[])

if __name__=="__main__":
    unittest.main()
