import unittest

from runtime.drawing_standards_validation import validate_drawing_standards


class DrawingStandardsValidationTests(unittest.TestCase):
    def test_complete_evidence_can_pass(self):
        result = validate_drawing_standards(
            source_sha256="abc",
            evidence_ids=["ev-1"],
            metadata={
                "scale_units_consistent": True,
                "dimensions_geometry_associated": True,
                "view_section_identity": True,
                "sheet_layout_valid": True,
                "title_block_fields_valid": True,
                "cross_view_consistent": True,
            },
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.unresolved, ())

    def test_missing_evidence_is_unknown_not_pass(self):
        result = validate_drawing_standards(
            source_sha256="abc",
            evidence_ids=["ev-1"],
            metadata={"scale_units_consistent": True},
        )
        self.assertEqual(result.status, "UNKNOWN")
        self.assertIn("DRAW-TITLE-001", result.unresolved)

    def test_explicit_contradiction_blocks(self):
        result = validate_drawing_standards(
            source_sha256="abc",
            evidence_ids=["ev-1", "ev-2"],
            metadata={
                "scale_units_consistent": True,
                "dimensions_geometry_associated": False,
            },
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("DRAW-DIM-001", result.unresolved)


if __name__ == "__main__":
    unittest.main()
