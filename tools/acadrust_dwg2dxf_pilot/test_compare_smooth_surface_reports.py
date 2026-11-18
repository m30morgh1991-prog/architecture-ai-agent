#!/usr/bin/env python3
"""Synthetic regression tests for release/upstream POLYLINE group-75 comparison."""

from __future__ import annotations

import unittest

from compare_smooth_surface_reports import compare_report_pair


def report(source_value: int, output_value: int) -> dict:
    return {
        "source_polyline_smooth_surfaces": [
            {"handle": "A1", "owner_handle": "B1", "smooth_surface": source_value}
        ],
        "independent_ezdxf": {
            "polyline_smooth_surfaces": [
                {"handle": "A1", "actual_smooth_type": output_value}
            ]
        },
    }


class SmoothSurfaceReportTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
