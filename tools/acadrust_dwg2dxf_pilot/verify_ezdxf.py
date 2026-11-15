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
    }

    try:
        document = ezdxf.readfile(candidate)
        modelspace_count = len(document.modelspace())
        layer_count = len(document.layers)
        linetype_count = len(document.linetypes)
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
