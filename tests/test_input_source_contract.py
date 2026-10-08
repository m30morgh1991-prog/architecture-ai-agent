import unittest

from runtime.input_source_contract import InputMode, SourceClass, classify_source

class InputSourceContractTests(unittest.TestCase):
    def test_geometry_trust_hierarchy(self):
        ranks = [
            classify_source("plan.dwg").geometry_trust_rank,
            classify_source("plan.pdf", pdf_representation="vector").geometry_trust_rank,
            classify_source("scan.pdf", pdf_representation="raster").geometry_trust_rank,
            classify_source("plan.jpg").geometry_trust_rank,
        ]
        self.assertEqual(ranks, [4, 3, 2, 1])

    def test_engineering_vector_is_separate_from_image_input(self):
        profile = classify_source("office-plan.dxf")
        self.assertEqual(profile.source_class, SourceClass.ENGINEERING_VECTOR)
        self.assertEqual(profile.input_mode, InputMode.ENGINEERING_PLAN)
        self.assertTrue(profile.is_engineering_input)
        self.assertFalse(profile.is_image_input)

    def test_vector_pdf_is_engineering_input(self):
        profile = classify_source("phase2.pdf", pdf_representation="vector")
        self.assertEqual(profile.source_class, SourceClass.DOCUMENT_VECTOR)
        self.assertEqual(profile.input_mode, InputMode.ENGINEERING_PLAN)

    def test_raster_pdf_uses_image_path(self):
        profile = classify_source("scan.pdf", pdf_representation="raster")
        self.assertEqual(profile.source_class, SourceClass.DOCUMENT_RASTER)
        self.assertEqual(profile.input_mode, InputMode.IMAGE)

    def test_pdf_requires_representation_evidence(self):
        profile = classify_source("unknown.pdf")
        self.assertEqual(profile.source_class, SourceClass.UNKNOWN)
        self.assertEqual(profile.input_mode, InputMode.UNKNOWN)
        self.assertTrue(profile.requires_pdf_inspection)

    def test_invalid_pdf_representation_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "PDF_REPRESENTATION_INVALID"):
            classify_source("plan.pdf", pdf_representation="guessed")