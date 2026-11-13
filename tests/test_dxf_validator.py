from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import ezdxf

from runtime.cad_conversion import DxfValidator, validate_dxf


class TestDxfValidator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "sample.dxf"

    def tearDown(self):
        self.temp.cleanup()

    def _write_valid_dxf(self):
        document = ezdxf.new("R2010")
        modelspace = document.modelspace()
        modelspace.add_line((0, 0), (10, 5))
        modelspace.add_text("Room 101")
        modelspace.add_mtext("سلام")
        document.header["$INSUNITS"] = 4
        document.header["$MEASUREMENT"] = 1
        block = document.blocks.new("TEST_BLOCK")
        block.add_circle((0, 0), radius=1)
        document.saveas(self.source)

    def test_valid_dxf_reports_structure_units_and_persian_text(self):
        self._write_valid_dxf()
        original_bytes = self.source.read_bytes()

        report = validate_dxf(self.source)

        self.assertEqual(report.parse_status, "PASS")
        self.assertEqual(report.audit_status, "CLEAN")
        self.assertEqual(report.validation_status, "PARSE_PASS")
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)
        self.assertGreaterEqual(report.entity_count, 3)
        self.assertEqual(report.entity_types["LINE"], 1)
        self.assertEqual(report.text_entity_count, 2)
        self.assertEqual(report.persian_text_entity_count, 1)
        self.assertEqual(report.insunits_code, 4)
        self.assertEqual(report.insunits_name, "millimeters")
        self.assertEqual(report.measurement_code, 1)
        self.assertIn("TEST_BLOCK", report.blocks)
        self.assertGreaterEqual(report.block_definition_entity_count, 1)
        self.assertEqual(self.source.read_bytes(), original_bytes)

    def test_missing_file_fails_closed(self):
        report = DxfValidator().validate(self.source)
        self.assertEqual(report.parse_status, "FAIL")
        self.assertEqual(report.error_code, "SOURCE_REQUIRED")
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)

    def test_empty_file_fails_closed(self):
        self.source.write_bytes(b"")
        report = validate_dxf(self.source)
        self.assertEqual(report.error_code, "DXF_EMPTY")
        self.assertEqual(report.parse_status, "FAIL")

    def test_wrong_extension_fails_closed(self):
        wrong = self.root / "drawing.dwg"
        wrong.write_bytes(b"not-a-dxf")
        report = validate_dxf(wrong)
        self.assertEqual(report.error_code, "DXF_INPUT_REQUIRED")
        self.assertEqual(report.parse_status, "FAIL")

    def test_malformed_dxf_fails_closed(self):
        self.source.write_text("this is not a DXF file", encoding="utf-8")
        report = validate_dxf(self.source)
        self.assertEqual(report.parse_status, "FAIL")
        self.assertEqual(report.validation_status, "PARSE_FAILED")
        self.assertEqual(report.error_code, "DXF_PARSE_FAILED")

    def test_report_is_json_serializable(self):
        self._write_valid_dxf()
        payload = validate_dxf(self.source).to_dict()
        self.assertEqual(payload["fidelity_status"], "UNKNOWN")
        self.assertTrue(payload["requires_review"])
        self.assertIsInstance(payload["entity_types"], dict)


if __name__ == "__main__":
    unittest.main()
