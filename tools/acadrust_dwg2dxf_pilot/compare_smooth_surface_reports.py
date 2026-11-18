#!/usr/bin/env python3
"""Compare source and independently reopened POLYLINE group-75 records."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _index(
    records: list[dict[str, Any]], value_key: str, owner_key: str, label: str
) -> tuple[dict[str, tuple[int, str]], list[str]]:
    indexed: dict[str, tuple[int, str]] = {}
    errors: list[str] = []
    for record in records:
        handle = str(record.get("handle", "")).upper()
        if not handle:
            errors.append(f"{label}_EMPTY_HANDLE")
            continue
        if handle in indexed:
            errors.append(f"{label}_DUPLICATE_HANDLE handle={handle}")
            continue
        indexed[handle] = (
            int(record.get(value_key, 0)),
            str(record.get(owner_key, "")).upper(),
        )
    return indexed, errors


def compare_report_pair(release: dict[str, Any], upstream: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    stages = (
        (
            "SOURCE",
            release.get("source_polyline_smooth_surfaces", []),
            upstream.get("source_polyline_smooth_surfaces", []),
            "smooth_surface",
            "owner_handle",
        ),
        (
            "OUTPUT",
            release.get("independent_ezdxf", {}).get("polyline_smooth_surfaces", []),
            upstream.get("independent_ezdxf", {}).get("polyline_smooth_surfaces", []),
            "actual_smooth_type",
            "output_owner_handle",
        ),
    )
    for label, left_records, right_records, value_key, owner_key in stages:
        left, left_errors = _index(left_records, value_key, owner_key, f"RELEASE_{label}")
        right, right_errors = _index(right_records, value_key, owner_key, f"UPSTREAM_{label}")
        issues.extend(left_errors)
        issues.extend(right_errors)
        if set(left) != set(right):
            missing_upstream = sorted(set(left) - set(right))
            missing_release = sorted(set(right) - set(left))
            issues.append(
                f"{label}_HANDLE_SET_MISMATCH missing_upstream={missing_upstream} missing_release={missing_release}"
            )
        for handle in sorted(set(left) & set(right)):
            left_value, left_owner = left[handle]
            right_value, right_owner = right[handle]
            if left_value != right_value:
                issues.append(
                    f"{label}_SMOOTH_SURFACE_MISMATCH handle={handle} release={left_value} upstream={right_value}"
                )
            if left_owner != right_owner:
                issues.append(
                    f"{label}_OWNER_HANDLE_MISMATCH handle={handle} release={left_owner} upstream={right_owner}"
                )
    return issues


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "Usage: compare_smooth_surface_reports.py REPORT_DIR FIXTURE [FIXTURE ...]",
            file=sys.stderr,
        )
        return 2

    report_dir = Path(sys.argv[1])
    all_issues: list[str] = []
    for fixture in sys.argv[2:]:
        paths = {
            "release": report_dir / f"{fixture}.release.report.json",
            "upstream-main": report_dir / f"{fixture}.upstream-main.report.json",
        }
        loaded: dict[str, dict[str, Any]] = {}
        for engine, path in paths.items():
            if not path.is_file():
                all_issues.append(f"{fixture} MISSING_REPORT engine={engine} path={path}")
                continue
            try:
                loaded[engine] = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                all_issues.append(f"{fixture} INVALID_REPORT engine={engine} error={exc}")
        if len(loaded) == 2:
            fixture_issues = compare_report_pair(loaded["release"], loaded["upstream-main"])
            all_issues.extend(f"{fixture} {issue}" for issue in fixture_issues)
            if fixture_issues:
                print(f"{fixture}: DISAGREEMENT ({len(fixture_issues)} findings)")
            else:
                print(f"{fixture}: source and independent DXF group-75 records agree")

    if all_issues:
        for issue in all_issues:
            print(issue, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
