from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from unittest.mock import patch
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
        self.assertEqual(report.source_sha256, hashlib.sha256(source_bytes).hexdigest())
        self.assertEqual(report.candidate_sha256, hashlib.sha256(candidate_bytes).hexdigest())
        self.assertTrue(report.ezdxf_version)
        self.assertEqual(report.comparator_version, "0.8.0")
        self.assertEqual(self.source.read_bytes(), source_bytes)
        self.assertEqual(self.candidate.read_bytes(), candidate_bytes)
        json.dumps(report.to_dict())

    def test_layer_table_property_changes_are_detected(self):
        def write(path, *, color, lineweight, plot):
            document = ezdxf.new("R2010")
            document.layers.new(
                "A-WALL",
                dxfattribs={
                    "color": color,
                    "lineweight": lineweight,
                    "linetype": "CONTINUOUS",
                    "plot": plot,
                },
            )
            document.modelspace().add_line(
                (0, 0), (10, 0), dxfattribs={"layer": "A-WALL"}
            )
            document.saveas(path)

        write(self.source, color=1, lineweight=25, plot=1)
        write(self.candidate, color=3, lineweight=50, plot=0)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("layer_properties", report.structural_differences)
        self.assertEqual(report.source_layer_properties["A-WALL"]["color"], 1)
        self.assertEqual(report.candidate_layer_properties["A-WALL"]["color"], 3)
        self.assertEqual(report.source_layer_properties["A-WALL"]["lineweight"], 25)
        self.assertEqual(report.candidate_layer_properties["A-WALL"]["lineweight"], 50)
        self.assertTrue(report.source_layer_properties["A-WALL"]["plot"])
        self.assertFalse(report.candidate_layer_properties["A-WALL"]["plot"])
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)

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


    def test_minsert_array_spacing_change_is_detected(self):
        def write(path, spacing):
            doc = ezdxf.new("R2010")
            doc.blocks.new("COLUMN")
            doc.modelspace().add_blockref(
                "COLUMN", (0, 0),
                dxfattribs={"row_count": 2, "column_count": 3, "row_spacing": spacing, "column_spacing": 4}
            )
            doc.saveas(path)
        write(self.source, 2.0)
        write(self.candidate, 3.0)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")


    def test_insert_extrusion_change_is_detected(self):
        def write(path, extrusion):
            doc = ezdxf.new("R2010")
            doc.blocks.new("SYMBOL").add_circle((0, 0), radius=1)
            doc.modelspace().add_blockref(
                "SYMBOL", (5, 5), dxfattribs={"extrusion": extrusion}
            )
            doc.saveas(path)

        write(self.source, (0, 0, 1))
        write(self.candidate, (0, 1, 0))
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("supported_geometry_signatures", report.structural_differences)
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)

    def test_nested_block_definition_geometry_change_is_detected(self):
        def write(path, endpoint):
            doc = ezdxf.new("R2010")
            inner = doc.blocks.new("INNER_SYMBOL")
            inner.add_line((0, 0), endpoint)
            outer = doc.blocks.new("OUTER_SYMBOL")
            outer.add_blockref("INNER_SYMBOL", (2, 3))
            doc.modelspace().add_blockref("OUTER_SYMBOL", (10, 10))
            doc.saveas(path)

        write(self.source, (10, 0))
        write(self.candidate, (12, 0))
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("block_definition_geometry", report.structural_differences)
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)

    def test_nested_insert_transform_change_is_detected(self):
        def write(path, rotation):
            doc = ezdxf.new("R2010")
            doc.blocks.new("INNER_SYMBOL").add_circle((0, 0), radius=1)
            outer = doc.blocks.new("OUTER_SYMBOL")
            outer.add_blockref("INNER_SYMBOL", (2, 3), dxfattribs={"rotation": rotation})
            doc.modelspace().add_blockref("OUTER_SYMBOL", (10, 10))
            doc.saveas(path)

        write(self.source, 0)
        write(self.candidate, 45)
        report = compare_dxf_files(self.source, self.candidate)
        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("block_definition_geometry", report.structural_differences)
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)



    def test_missing_shx_and_reversed_persian_text_do_not_block_geometry(self):
        def write(path):
            document = ezdxf.new("R2010")
            document.styles.new("PERSIAN_MISSING", dxfattribs={"font": "not-installed.shx"})
            modelspace = document.modelspace()
            modelspace.add_line((0, 0), (20, 10))
            modelspace.add_text("ﻡﻼﺳ", dxfattribs={"style": "PERSIAN_MISSING"})
            modelspace.add_mtext("ﻥﺎﺘﺳﺭﺎﮐ", dxfattribs={"style": "PERSIAN_MISSING"})
            document.saveas(path)

        write(self.source)
        write(self.candidate)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "MATCHED_SUPPORTED_CONTENT")
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.source_entity_counts["LINE"], 1)
        self.assertEqual(report.source_entity_counts["TEXT"], 1)
        self.assertEqual(report.source_entity_counts["MTEXT"], 1)
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)

    def test_text_signature_exception_does_not_block_geometry_comparison(self):
        def write(path):
            document = ezdxf.new("R2010")
            modelspace = document.modelspace()
            modelspace.add_line((0, 0), (20, 10))
            modelspace.add_text("سلام")
            document.saveas(path)

        write(self.source)
        write(self.candidate)
        original_signature = DxfComparator._signature

        def fail_only_text(entity, tolerance):
            if entity.dxftype() == "TEXT":
                raise UnicodeError("simulated legacy text decode failure")
            return original_signature(entity, tolerance)

        with patch.object(DxfComparator, "_signature", side_effect=fail_only_text):
            report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "INCOMPLETE")
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertIn("TEXT_READ_UNAVAILABLE", report.unsupported_entity_types)
        self.assertEqual(report.source_entity_counts["LINE"], 1)
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)

    def test_one_sided_text_read_failure_is_not_reported_as_geometry_change(self):
        def write(path):
            document = ezdxf.new("R2010")
            modelspace = document.modelspace()
            modelspace.add_line((0, 0), (20, 10))
            modelspace.add_text("سلام")
            document.saveas(path)

        write(self.source)
        write(self.candidate)
        original_signature = DxfComparator._signature
        text_calls = 0

        def fail_first_text_only(entity, tolerance):
            nonlocal text_calls
            if entity.dxftype() == "TEXT":
                text_calls += 1
                if text_calls == 1:
                    raise UnicodeError("simulated one-sided legacy text decode failure")
            return original_signature(entity, tolerance)

        with patch.object(DxfComparator, "_signature", side_effect=fail_first_text_only):
            report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.geometry_mismatch_count, 0)
        self.assertGreater(report.text_mismatch_count, 0)
        self.assertIn("text_content", report.structural_differences)
        self.assertIn("TEXT_READ_UNAVAILABLE", report.unsupported_entity_types)
        self.assertEqual(report.fidelity_status, "UNKNOWN")

    def test_lossily_decoded_text_is_incomplete_but_geometry_stays_comparable(self):
        def write(path):
            document = ezdxf.new("R2010")
            modelspace = document.modelspace()
            modelspace.add_line((0, 0), (20, 10))
            modelspace.add_text("سلام")
            document.saveas(path)
            raw = path.read_bytes()
            raw = raw.replace("سلام".encode("utf-8"), b"\xff\xfe\xfd\xfc", 1)
            path.write_bytes(raw)

        write(self.source)
        write(self.candidate)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "INCOMPLETE")
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertIn("TEXT_READ_UNAVAILABLE", report.unsupported_entity_types)
        self.assertEqual(report.source_entity_counts["LINE"], 1)
        self.assertEqual(report.geometry_mismatch_count, 0)
        self.assertEqual(report.fidelity_status, "UNKNOWN")
        self.assertTrue(report.requires_review)

    def test_layout_metadata_change_is_detected(self):
        def write(path, taborder):
            document = ezdxf.new("R2010")
            layout = document.layouts.new("SHEET_A")
            layout.dxf_layout.dxf.taborder = taborder
            layout.dxf_layout.dxf.limmax = (420, 297, 0)
            document.modelspace().add_line((0, 0), (10, 0))
            document.saveas(path)

        write(self.source, 3)
        write(self.candidate, 4)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("layout_properties", report.structural_differences)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.fidelity_status, "UNKNOWN")

    def test_viewport_camera_change_is_detected_without_geometry_mismatch(self):
        def write(path, view_height):
            document = ezdxf.new("R2010")
            layout = document.layouts.new("SHEET_A")
            layout.add_viewport(
                center=(100, 100),
                size=(200, 150),
                view_center_point=(0, 0),
                view_height=view_height,
            )
            document.modelspace().add_line((0, 0), (10, 0))
            document.saveas(path)

        write(self.source, 100)
        write(self.candidate, 125)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("viewports", report.structural_differences)
        self.assertGreater(report.viewport_mismatch_count, 0)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertNotIn("VIEWPORT", report.unsupported_entity_types)

    def test_ucs_table_change_is_detected(self):
        def write(path, origin):
            document = ezdxf.new("R2010")
            document.ucs.new(
                "SITE_UCS",
                dxfattribs={
                    "origin": origin,
                    "xaxis": (1, 0, 0),
                    "yaxis": (0, 1, 0),
                },
            )
            document.modelspace().add_line((0, 0), (10, 0))
            document.saveas(path)

        write(self.source, (0, 0, 0))
        write(self.candidate, (10, 0, 0))
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("ucs_properties", report.structural_differences)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")

    def test_computed_layout_extents_change_is_reported(self):
        def write(path, max_x):
            document = ezdxf.new("R2010")
            document.modelspace().add_line((0, 0), (max_x, 100))
            document.saveas(path)

        write(self.source, 100)
        write(self.candidate, 120)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("extents", report.structural_differences)
        self.assertNotEqual(report.source_extents, report.candidate_extents)
        self.assertEqual(report.geometry_comparison_status, "DIFFERENCES_FOUND")

    def test_coordinate_system_header_change_is_detected(self):
        def write(path, ucs_origin):
            document = ezdxf.new("R2010")
            document.header["$UCSORG"] = ucs_origin
            document.header["$INSBASE"] = (5, 5, 0)
            document.modelspace().add_line((0, 0), (10, 0))
            document.saveas(path)

        write(self.source, (0, 0, 0))
        write(self.candidate, (5, 0, 0))
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("coordinate_metadata", report.structural_differences)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")

    def test_text_style_shx_reference_change_is_detected_without_loading_font(self):
        def write(path, font_name):
            document = ezdxf.new("R2010")
            document.styles.new(
                "PERSIAN",
                dxfattribs={"font": font_name, "bigfont": "missing_bigfont.shx"},
            )
            modelspace = document.modelspace()
            modelspace.add_line((0, 0), (10, 0))
            modelspace.add_text("سلام", dxfattribs={"style": "PERSIAN"})
            document.saveas(path)

        write(self.source, "missing_primary.shx")
        write(self.candidate, "alternate_missing.shx")
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("text_styles", report.structural_differences)
        self.assertIn("PERSIAN", report.source_text_styles)
        self.assertIn("missing_primary.shx", repr(report.source_text_styles["PERSIAN"]))
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.fidelity_status, "UNKNOWN")

    def test_dimension_style_property_change_is_detected(self):
        def write(path, text_height):
            document = ezdxf.new("R2010")
            document.dimstyles.new(
                "ARCH",
                dxfattribs={"dimtxt": text_height, "dimasz": 1.5},
            )
            document.modelspace().add_line((0, 0), (10, 0))
            document.saveas(path)

        write(self.source, 2.5)
        write(self.candidate, 3.0)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("dimension_styles", report.structural_differences)
        self.assertIn("ARCH", report.source_dimension_styles)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.fidelity_status, "UNKNOWN")

    def test_xdata_change_is_detected_without_geometry_mismatch(self):
        def write(path, label):
            document = ezdxf.new("R2010")
            document.appids.new("ARCH_APP")
            line = document.modelspace().add_line((0, 0), (10, 0))
            line.set_xdata("ARCH_APP", [(1000, label), (1040, 1.5), (1070, 2)])
            document.saveas(path)

        write(self.source, "source metadata")
        write(self.candidate, "candidate metadata")
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("entity_metadata", report.structural_differences)
        self.assertGreater(report.entity_metadata_mismatch_count, 0)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.geometry_mismatch_count, 0)
        self.assertEqual(report.fidelity_status, "UNKNOWN")

    def test_extension_dictionary_xrecord_change_is_detected(self):
        def write(path, label):
            document = ezdxf.new("R2010")
            line = document.modelspace().add_line((0, 0), (10, 0))
            extension = line.new_extension_dict()
            record = extension.add_xrecord("ARCH_RECORD")
            record.reset([(1, label), (40, 1.25), (1070, 7)])
            document.saveas(path)

        write(self.source, "source record")
        write(self.candidate, "candidate record")
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "DIFFERENCES_FOUND")
        self.assertIn("entity_metadata", report.structural_differences)
        self.assertGreater(report.entity_metadata_mismatch_count, 0)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.geometry_mismatch_count, 0)

    def test_unresolved_xdata_handle_reference_fails_closed(self):
        def write(path):
            document = ezdxf.new("R2010")
            document.appids.new("ARCH_APP")
            line = document.modelspace().add_line((0, 0), (10, 0))
            line.set_xdata("ARCH_APP", [(1005, "ABCD")])
            document.saveas(path)

        write(self.source)
        write(self.candidate)
        report = compare_dxf_files(self.source, self.candidate)

        self.assertEqual(report.comparison_status, "INCOMPLETE")
        self.assertIn("ENTITY_METADATA_UNSUPPORTED", report.unsupported_entity_types)
        self.assertEqual(report.geometry_comparison_status, "MATCHED")
        self.assertEqual(report.fidelity_status, "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
