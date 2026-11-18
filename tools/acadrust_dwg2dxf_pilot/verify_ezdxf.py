#!/usr/bin/env python3
"""Independent ezdxf reopen/inventory check for an acadrust pilot candidate."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import ezdxf


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()



def verify_polyline_smooth_surfaces(document, report: dict[str, object]) -> dict[str, object]:
    """Compare source non-default POLYLINE group 75 values with ezdxf output."""
    expected_records = report.get("source_polyline_smooth_surfaces", [])
    observed: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []

    for expected in expected_records:
        handle = str(expected.get("handle", "")).upper()
        expected_value = int(expected.get("smooth_surface", 0))
        entity = document.entitydb.get(handle) if handle else None
        if entity is None:
            mismatches.append({"handle": handle, "reason": "MISSING_ENTITY"})
            continue
        if entity.dxftype() != "POLYLINE":
            mismatches.append(
                {"handle": handle, "reason": "ENTITY_TYPE_CHANGED", "actual_type": entity.dxftype()}
            )
            continue

        raw_smooth_type = entity.dxf.get("smooth_type", 0)
        actual_value = 0 if raw_smooth_type is None else int(raw_smooth_type)
        actual_owner = str(entity.dxf.get("owner", "")).upper()
        record = {
            "handle": handle,
            "source_owner_handle": str(expected.get("owner_handle", "")).upper(),
            "output_owner_handle": actual_owner,
            "expected_smooth_surface": expected_value,
            "actual_smooth_type": actual_value,
        }
        observed.append(record)
        if actual_value != expected_value:
            mismatches.append(
                {
                    **record,
                    "reason": "GROUP_75_VALUE_MISMATCH",
                }
            )
        if not record["source_owner_handle"] or not actual_owner:
            mismatches.append(
                {
                    **record,
                    "reason": "OWNER_HANDLE_MISSING",
                }
            )
        elif actual_owner != record["source_owner_handle"]:
            mismatches.append(
                {
                    **record,
                    "reason": "OWNER_HANDLE_MISMATCH",
                }
            )

    return {
        "polyline_smooth_surfaces": observed,
        "polyline_smooth_surface_mismatches": mismatches,
        "matches_source_polyline_smooth_surfaces": (
            len(mismatches) == 0 and len(observed) == len(expected_records)
        ),
        "matches_source_polyline_owners": not any(
            item.get("reason") in ("OWNER_HANDLE_MISMATCH", "OWNER_HANDLE_MISSING") for item in mismatches
        ),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: verify_ezdxf.py CANDIDATE.dxf REPORT.json", file=sys.stderr)
        return 2

    candidate = Path(sys.argv[1])
    report_path = Path(sys.argv[2])
    report = json.loads(report_path.read_text(encoding="utf-8"))
    checks: dict[str, object] = {
        "parser": "ezdxf",
        "ezdxf_version": ezdxf.__version__,
        "candidate_sha256": sha256(candidate),
        "candidate_hash_matches_rust_report": False,
        "reopened": False,
        "modelspace_entities": None,
        "layers": None,
        "line_types": None,
        "matches_source_modelspace_entities": False,
        "matches_source_layer_count": False,
        "matches_source_linetype_count": False,
        "polyline_smooth_surfaces": [],
        "polyline_smooth_surface_mismatches": [],
        "matches_source_polyline_smooth_surfaces": False,
        "matches_source_polyline_owners": False,
    }

    try:
        document = ezdxf.readfile(candidate)
        modelspace_count = len(document.modelspace())
        layer_count = len(document.layers)
        linetype_count = len(document.linetypes)
        smooth_surface_check = verify_polyline_smooth_surfaces(document, report)
        checks.update(
            {
                "reopened": True,
                "modelspace_entities": modelspace_count,
                "layers": layer_count,
                "line_types": linetype_count,
                "matches_source_modelspace_entities": (
                    modelspace_count == report["source_modelspace_entity_count"]
                ),
                "matches_source_layer_count": (
                    layer_count == report["source_tables"]["layers"]
                ),
                "matches_source_linetype_count": (
                    linetype_count == report["source_tables"]["line_types"]
                ),
                **smooth_surface_check,
            }
        )
    except Exception as exc:  # record parser failures as evidence, do not hide them
        checks["error"] = f"{type(exc).__name__}: {exc}"

    checks["candidate_hash_matches_rust_report"] = (
        checks["candidate_sha256"] == report["candidate_sha256"]
    )
    passed = all(
        checks[key]
        for key in (
            "candidate_hash_matches_rust_report",
            "reopened",
            "matches_source_modelspace_entities",
            "matches_source_layer_count",
            "matches_source_linetype_count",
            "matches_source_polyline_smooth_surfaces",
            "matches_source_polyline_owners",
        )
    )
    report["independent_ezdxf"] = checks
    report["decision"] = "NEEDS_REVIEW" if passed and report["structural_checks_pass"] else "BLOCKED"
    report.setdefault("reasons", []).append(
        "INDEPENDENT_EZDXF_REOPENED_CANDIDATE; FULL_ENTITY_PROPERTY_AND_CAD_HOST_REVIEW_STILL_REQUIRED"
    )
    temporary = report_path.with_name(report_path.name + f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, report_path)
    print(
        f"decision={report['decision']} ezdxf={ezdxf.__version__} "
        f"modelspace={checks['modelspace_entities']} "
        f"layers={checks['layers']} linetypes={checks['line_types']}"
    )
    return 0 if passed and report["structural_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
