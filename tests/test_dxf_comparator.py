from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import ezdxf

from runtime.cad_conversion import DxfComparator, compare_dxf_files


class TestDxfComparator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.dxf"
        self.candidate = self.root / "candidate.dxf"

    def tearDown(self):
        self.temp.cleanup()

    def _write_dxf(self, path, *, line_end=(10, 5), units=4, include_dimension=False):
        document = ezdxf.new("R2010")
        modelspace = document.modelspace()
        modelspace.add_line((0, 0), line_end)
        modelspace.add_text("Room 101")
        modelspace.add_mtext("سلام")
        if include_dimension:
            modelspace.add_linear_dim(base=(0, 2), p1=(0, 0), p2=(5, 0)).render()
        document.header["$INSUNITS"] = units
        document.header["$MEASUREMENT"] = 1
        block = document.blocks.new("TEST_BLOCK")
        block.add_circle((0, 0), radius=1)
        document.saveas(path)

    def test_identical_supported_files_match_but_fidelity_stays_unknown(self):
        self._write_dxf(self.source)
        self._write_dxf(self.candidate)
        source_bytes = self.source.read_bytes()
        candidate_bytes = self.candidate.read_bytes()
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "MATCHED_SUPPORTED_CONTENT")
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)
        self.assertEqual(self.source.read_bytes(), source_bytes)
        self.assertEqual(self.candidate.read_bytes(), candidate_bytes)
        json.dumps(report.to_dict())

    def test_geometry_difference_is_detected(self):
        self._write_dxf(self.source)
        self._write_dxf(self.candidate, line_end=(10.5, 5))
        report = DxfComparator().compare(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertEqual(report.geometry_comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("supported_geometry_signatures", report.structural_differences)
        self.assertGreater(report.geometry_mismatch_count, 0)

    def test_unit_difference_is_detected(self):
        self._write_dxf(self.source, units=4)
        self._write_dxf(self.candidate, units=5)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("INSUNITS", report.structural_differences)

    def test_tolerance_absorbs_small_coordinate_noise(self):
        self._write_dxf(self.source)
        self._write_dxf(self.candidate, line_end=(10.0000001, 5))
        report = compare_dxf_files(self.source, self.candidate, tolerance=1e-5)
        self.assertEqual(report.comparison_status, "MATCHED_SUPPORTED_CONTENT")

    def test_dimension_is_compared_and_fidelity_stays_unknown(self):
        self._write_dxf(self.source, include_dimension=True)
        self._write_dxf(self.candidate, include_dimension=True)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertNotIn("DIMENSION", report.unsupported_entity_types)
        self.assertEqual(report.fidelity_status, "UNKNOWN")

    def test_malformed_candidate_fails_closed(self):
        self._write_dxf(self.source)
        self.candidate.write_text("not a DXF", encoding="utf-8")
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "COMPARISON_FAILED")
        self.assertEqual(report.error_code, "DXF_PARSE_FAILED")
        self.assertTrue(report.requires_review)

    def test_invalid_tolerance_is_rejected(self):
        with self.assertRaises(ValueError):
            compare_dxf_files(self.source, self.candidate, tolerance=0)


    def test_dimension_semantics_are_compared(self):
        def write(path, measurement=5.0):
            doc = ezdxf.new("R2010")
            doc.modelspace().add_linear_dim(
                base=(0, 2), p1=(0, 0), p2=(measurement, 0),
                dimstyle="Standard"
            ).render()
            doc.saveas(path)
        write(self.source)
        write(self.candidate)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertNotIn("DIMENSION", report.unsupported_entity_types)
        self.assertEqual(report.fidelity_status, "UNKNOWN")

    def test_dimension_geometry_change_is_detected(self):
        def write(path, measurement):
            doc = ezdxf.new("R2010")
            doc.modelspace().add_linear_dim(
                base=(0, 2), p1=(0, 0), p2=(measurement, 0)
            ).render()
            doc.saveas(path)
        write(self.source, 5.0)
        write(self.candidate, 6.0)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")

    def test_hatch_boundary_change_is_detected(self):
        def write(path, x):
            doc = ezdxf.new("R2010")
            hatch = doc.modelspace().add_hatch(color=1)
            hatch.set_solid_fill(color=1)
            hatch.paths.add_polyline_path(
                [(0, 0), (x, 0), (x, 10), (0, 10)],
                is_closed=True
            )
            doc.saveas(path)
        write(self.source, 10.0)
        write(self.candidate, 11.0)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertNotIn("HATCH", report.unsupported_entity_types)

    def test_spline_control_data_change_is_detected(self):
        def write(path, offset):
            doc = ezdxf.new("R2010")
            doc.modelspace().add_spline(
                fit_points=[(0, 0), (3, 4 + offset), (7, 4), (10, 0)],
                degree=3
            )
            doc.saveas(path)
        write(self.source, 0.0)
        write(self.candidate, 1.0)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertNotIn("SPLINE", report.unsupported_entity_types)

    def test_insert_attribute_value_change_is_detected(self):
        def write(path, value):
            doc = ezdxf.new("R2010")
            block = doc.blocks.new("ROOM_TAG")
            block.add_attdef("ROOM", insert=(0, 0), text="A")
            insert = doc.modelspace().add_blockref("ROOM_TAG", (10, 10))
            insert.add_auto_attribs({"ROOM": value})
            doc.saveas(path)
        write(self.source, "101")
        write(self.candidate, "102")
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")

    def test_xref_dependency_is_never_claimed_complete(self):
        def write(path):
            doc = ezdxf.new("R2010")
            doc.blocks.new("SITE_XREF", dxfattribs={"flags": 4, "xref_path": "site.dwg"})
            doc.saveas(path)
        write(self.source)
        write(self.candidate)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "INCOMPLETE")
        self.assertEqual(report.fidelity_status, "UNKNOWN")


    def test_entity_presentation_change_is_detected(self):
        def write(path, color):
            doc = ezdxf.new("R2010")
            doc.modelspace().add_line((0, 0), (10, 0), dxfattribs={"color": color, "lineweight": 25})
            doc.saveas(path)
        write(self.source, 1)
        write(self.candidate, 3)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")


if __name__ == "__main__":
    unittest.main()
