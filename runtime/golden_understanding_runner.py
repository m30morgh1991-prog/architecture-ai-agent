from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from runtime.golden_understanding_regression import REQUIRED_DOMAINS, GoldenCase, load_manifest
from runtime.plan_understanding_core import PlanUnderstandingCore


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _domain_observation(result, source_sha256: str) -> dict[str, Any]:
    detection = result.detection
    model = result.plan_model
    elements = [element.element_type for element in model.elements]

    return {
        "source_profile": {
            "sha256": source_sha256,
            "detector_id": detection.get("detector_id"),
            "status": detection.get("status"),
        },
        "elements": elements,
        "geometry": detection.get("dwg_geometry", {}),
        "topology": {
            "spaces": detection.get("spaces", ()),
            "space_relations": detection.get("space_relations", ()),
        },
        "relations": detection.get("space_relations", ()),
        "drawing_evidence": (
            tuple(evidence.evidence_id for evidence in model.drawing_evidence.evidences)
            if model.drawing_evidence is not None
            else ()
        ),
        "text": detection.get("dwg_text_labels", ()),
        "dimensions": "UNKNOWN",
        "levels": "UNKNOWN",
        "view_markers": "UNKNOWN",
        "vertical_circulation": "UNKNOWN",
        "bim_mapping": {
            "elements_with_bim_identity": sum(
                element.bim_identity is not None for element in model.elements
            ),
            "relations": model.bim_relations,
        },
        "provenance": {
            "source_sha256": source_sha256,
            "element_evidence_bound": model.element_evidence is not None,
        },
        "uncertainties": tuple(model.unresolved),
        "contradictions": (),
        "missing_evidence": tuple(model.unresolved),
        "fail_closed_decision": result.status,
    }


def run_golden_case(case: GoldenCase, core: PlanUnderstandingCore | None = None) -> dict[str, Any]:
    path = Path(case.source_path)
    if not path.is_file():
        return {
            "case_id": case.case_id,
            "source_sha256": None,
            "source_exists": False,
            "observed": {
                domain: "UNKNOWN" for domain in REQUIRED_DOMAINS
            },
            "decision": "NEEDS_REVIEW",
            "failures": ["SOURCE_FILE_MISSING"],
        }

    source_sha256 = sha256_file(path)
    if case.source_sha256 is not None and source_sha256 != case.source_sha256:
        return {
            "case_id": case.case_id,
            "source_sha256": source_sha256,
            "source_exists": True,
            "observed": {domain: "UNKNOWN" for domain in REQUIRED_DOMAINS},
            "decision": "BLOCKED",
            "failures": ["SOURCE_SHA256_MISMATCH"],
        }

    understanding = (core or PlanUnderstandingCore()).understand(
        source_path=str(path),
        source_sha256=source_sha256,
        model_id=f"golden:{case.case_id}",
    )
    observed = _domain_observation(understanding, source_sha256)
    return {
        "case_id": case.case_id,
        "source_sha256": source_sha256,
        "source_exists": True,
        "observed": observed,
        "decision": understanding.status,
        "failures": [],
    }


def run_manifest_to_report(
    manifest_path: str | Path,
    *,
    core: PlanUnderstandingCore | None = None,
) -> dict[str, Any]:
    cases = load_manifest(manifest_path)
    reports = [run_golden_case(case, core=core) for case in cases]
    return {
        "schema": "golden-understanding-report-v1",
        "manifest": str(manifest_path),
        "cases": reports,
    }


def write_report(
    manifest_path: str | Path,
    output_path: str | Path,
    *,
    core: PlanUnderstandingCore | None = None,
) -> None:
    report = run_manifest_to_report(manifest_path, core=core)
    Path(output_path).write_text(
        json.dumps(report, indent=2, default=str, sort_keys=True),
        encoding="utf-8",
    )
