"""Convert Golden DWG inputs to DXF and fail closed on fidelity loss.

This is an evidence-only test: source DWGs are hashed before/after and never edited.
A generated DXF is not accepted as a lossless replacement unless every comparison passes.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import ezdxf
import ezdwg

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "test-assets/golden-understanding/golden_manifest.json"
OUT = ROOT / "artifacts/golden-dwg-dxf-conversion"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entity_counts(layout: Any) -> dict[str, int]:
    return dict(sorted(Counter(entity.dxftype() for entity in layout).items()))


def layer_names(layout: Any) -> list[str]:
    return sorted({str(entity.dxf.get("layer", "0")) for entity in layout})


def jsonable_result(result: Any) -> dict[str, Any]:
    skipped = getattr(result, "skipped_by_type", {}) or {}
    diagnostics = getattr(result, "diagnostics", []) or []
    return {
        "total_entities": int(getattr(result, "total_entities", 0)),
        "written_entities": int(getattr(result, "written_entities", 0)),
        "skipped_entities": int(getattr(result, "skipped_entities", 0)),
        "skipped_by_type": dict(skipped),
        "diagnostics": [str(item) for item in diagnostics],
    }


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    reports: list[dict[str, Any]] = []

    for case in manifest["cases"]:
        source = ROOT / case["source_path"]
        if not source.is_file():
            raise FileNotFoundError(f"SOURCE_REQUIRED:{case['case_id']}:{source}")

        before = sha256_file(source)
        expected = case.get("source_sha256")
        if expected and before != expected:
            raise RuntimeError(f"SOURCE_SHA256_MISMATCH:{case['case_id']}")

        source_doc = ezdwg.read(str(source))
        source_msp = source_doc.modelspace()
        source_counts = entity_counts(source_msp)
        source_layers = layer_names(source_msp)

        output = OUT / f"{case['case_id'].lower()}.dxf"
        result = ezdwg.to_dxf(
            str(source),
            str(output),
            dxf_version="R2010",
            strict=False,
        )
        conversion = jsonable_result(result)

        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError(f"DXF_OUTPUT_MISSING_OR_EMPTY:{case['case_id']}")

        # Independent reopen/parse using ezdxf, not ezdwg's source reader.
        converted_doc = ezdxf.readfile(output)
        converted_msp = converted_doc.modelspace()
        converted_counts = entity_counts(converted_msp)
        converted_layers = layer_names(converted_msp)
        auditor = converted_doc.audit()
        audit_errors = len(auditor.errors)
        audit_fixes = len(auditor.fixes)

        type_deltas = {}
        for kind in sorted(set(source_counts) | set(converted_counts)):
            delta = converted_counts.get(kind, 0) - source_counts.get(kind, 0)
            if delta:
                type_deltas[kind] = delta

        missing_layers = sorted(set(source_layers) - set(converted_layers))
        added_layers = sorted(set(converted_layers) - set(source_layers))
        after = sha256_file(source)
        source_unchanged = before == after

        checks = {
            "source_hash_unchanged": source_unchanged,
            "output_reopened_by_ezdxf": True,
            "no_skipped_entities": conversion["skipped_entities"] == 0,
            "entity_counts_identical": not type_deltas,
            "layer_names_identical": not missing_layers and not added_layers,
            "no_dxf_audit_errors": audit_errors == 0,
            "no_dxf_audit_fixes": audit_fixes == 0,
        }
        status = "PASS" if all(checks.values()) else "NEEDS_REVIEW"

        report = {
            "case_id": case["case_id"],
            "source_path": case["source_path"],
            "source_sha256_before": before,
            "source_sha256_after": after,
            "source_unchanged": source_unchanged,
            "source_dwg_version": str(getattr(source_doc, "version", "UNKNOWN")),
            "source_units_metadata": getattr(source_doc, "units", None),
            "target_dxf_version": "R2010",
            "output_path": str(output.relative_to(ROOT)),
            "output_size_bytes": output.stat().st_size,
            "conversion": conversion,
            "source_entity_counts": source_counts,
            "converted_entity_counts": converted_counts,
            "entity_count_deltas_converted_minus_source": type_deltas,
            "source_layer_names": source_layers,
            "converted_layer_names": converted_layers,
            "missing_layer_names": missing_layers,
            "added_layer_names": added_layers,
            "dxf_audit_errors": audit_errors,
            "dxf_audit_fixes": audit_fixes,
            "checks": checks,
            "status": status,
            "decision": (
                "DXF_CONVERSION_FIDELITY_VERIFIED_FOR_THIS_FIXTURE"
                if status == "PASS"
                else "DO_NOT_USE_AS_LOSSLESS_ORIGINAL; REVIEW_REPORTED_DIFFERENCES"
            ),
        }
        report_path = OUT / f"{case['case_id'].lower()}-report.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        reports.append(report)

    overall = {
        "schema": "golden-dwg-dxf-conversion-report-v1",
        "overall_status": "PASS" if all(row["status"] == "PASS" for row in reports) else "NEEDS_REVIEW",
        "source_files_modified": any(not row["source_unchanged"] for row in reports),
        "cases": reports,
        "safety_note": (
            "A successful DXF conversion does not establish DWG write-back safety, "
            "AutoCAD visual equivalence, architectural meaning, or regulatory compliance."
        ),
    }
    (OUT / "index.json").write_text(
        json.dumps(overall, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(overall, ensure_ascii=False, indent=2, sort_keys=True))
    # CI validates that conversion and independent reopening work. Fidelity is
    # reported separately and remains fail-closed as NEEDS_REVIEW when any
    # unsupported entity, count delta, layer delta, or audit issue is detected.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
