#!/usr/bin/env python3
"""Synthetic regression tests for release/upstream POLYLINE group-75 comparison."""

from __future__ import annotations

import unittest

from compare_smooth_surface_reports import compare_report_pair
from verify_ezdxf import source_polyline_downsave_eligible


def report(source_value: int, output_value: int) -> dict:
    return {
        "source_polyline_smooth_surfaces": [
            {"handle": "A1", "owner_handle": "B1", "smooth_surface": source_value}
        ],
        "independent_ezdxf": {
            "polyline_smooth_surfaces": [
                {"handle": "A1", "source_owner_handle": "B1", "output_owner_handle": "B1", "actual_smooth_type": output_value}
            ]
        },
    }


class SmoothSurfaceReportTests(unittest.TestCase):
    def test_plain_default_2d_polyline_is_eligible_for_documented_downsave(self) -> None:
        self.assertTrue(source_polyline_downsave_eligible({
            "smooth_surface": 0,
            "source_flags": 0x81,
            "source_vertex_flags_default": True,
        }))

    def test_spline_fit_or_mesh_flags_are_not_eligible_for_downsave(self) -> None:
        for flags, smooth, vertex_default in (
            (0x04, 0, True),
            (0x10, 0, True),
            (0, 6, True),
            (0, 0, False),
        ):
            with self.subTest(flags=flags, smooth=smooth, vertex_default=vertex_default):
                self.assertFalse(source_polyline_downsave_eligible({
                    "smooth_surface": smooth,
                    "source_flags": flags,
                    "source_vertex_flags_default": vertex_default,
                }))

    def test_missing_source_flags_fail_closed(self) -> None:
        self.assertFalse(source_polyline_downsave_eligible({"smooth_surface": 0}))

    def test_matching_source_and_output_records_pass(self) -> None:
        self.assertEqual(compare_report_pair(report(6, 6), report(6, 6)), [])

    def test_source_reader_disagreement_is_reported(self) -> None:
        issues = compare_report_pair(report(0, 0), report(6, 6))
        self.assertTrue(any(issue.startswith("SOURCE_SMOOTH_SURFACE_MISMATCH") for issue in issues))

    def test_independent_dxf_output_disagreement_is_reported(self) -> None:
        issues = compare_report_pair(report(6, 6), report(6, 0))
        self.assertTrue(any(issue.startswith("OUTPUT_SMOOTH_SURFACE_MISMATCH") for issue in issues))

    def test_missing_handle_is_reported(self) -> None:
        left = report(6, 6)
        right = report(6, 6)
        right["source_polyline_smooth_surfaces"] = []
        issues = compare_report_pair(left, right)
        self.assertTrue(any(issue.startswith("SOURCE_HANDLE_SET_MISMATCH") for issue in issues))

    def test_source_owner_handle_disagreement_is_reported(self) -> None:
        left = report(6, 6)
        right = report(6, 6)
        right["source_polyline_smooth_surfaces"][0]["owner_handle"] = "C2"
        issues = compare_report_pair(left, right)
        self.assertTrue(any(issue.startswith("SOURCE_OWNER_HANDLE_MISMATCH") for issue in issues))

    def test_independent_output_owner_handle_disagreement_is_reported(self) -> None:
        left = report(6, 6)
        right = report(6, 6)
        right["independent_ezdxf"]["polyline_smooth_surfaces"][0]["output_owner_handle"] = "C2"
        issues = compare_report_pair(left, right)
        self.assertTrue(any(issue.startswith("OUTPUT_OWNER_HANDLE_MISMATCH") for issue in issues))


if __name__ == "__main__":
    unittest.main()
