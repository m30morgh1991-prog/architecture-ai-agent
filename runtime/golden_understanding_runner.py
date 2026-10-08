from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from runtime.golden_understanding_regression import (
    REQUIRED_DOMAINS,
    GoldenCase,
    evaluate_golden_case,
    load_manifest,
    summarize_domain_metrics,
)
from runtime.plan_understanding_core import PlanUnderstandingCore
from runtime.input_source_contract import classify_source


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _domain_observation(result, source_sha256: str, source_path: str) -> dict[str, Any]:
    detection = result.detection
    model = result.plan_model
    elements = [element.element_type for element in model.elements]

    source_profile = classify_source(source_path)
    return {
        "source_profile": {
            "sha256": source_sha256,
            "source_class": source_profile.source_class.value,
            "input_mode": source_profile.input_mode.value,
            "geometry_trust_rank": source_profile.geometry_trust_rank,
            "requires_pdf_inspection": source_profile.requires_pdf_inspection,
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


def _blocked_observation(reason: str) -> dict[str, Any]:
    return {
        domain: "UNKNOWN" for domain in REQUIRED_DOMAINS
    } | {
        "uncertainties": (reason,),
        "missing_evidence": (reason,),
        "contradictions": (),
        "fail_closed_decision": "BLOCKED",
        "elements": (),
    }


def run_golden_case(case: GoldenCase, core: PlanUnderstandingCore | None = None) -> dict[str, Any]:
    path = Path(case.source_path)
    if not path.is_file():
        observed = _blocked_observation("SOURCE_FILE_MISSING")
        regression = evaluate_golden_case(case, observed)
        return {
            "case_id": case.case_id,
            "source_sha256": None,
            "source_exists": False,
            "observed": observed,
            "decision": regression.decision,
            "unsafe_acceptance": regression.unsafe_acceptance,
            "failures": ("SOURCE_FILE_MISSING",) + regression.failures,
        }

    source_sha256 = sha256_file(path)
    if case.source_sha256 is not None and source_sha256 != case.source_sha256:
        observed = _blocked_observation("SOURCE_SHA256_MISMATCH")
        regression = evaluate_golden_case(case, observed)
        return {
            "case_id": case.case_id,
            "source_sha256": source_sha256,
            "source_exists": True,
            "observed": observed,
            "decision": "BLOCKED",
            "unsafe_acceptance": regression.unsafe_acceptance,
            "failures": ("SOURCE_SHA256_MISMATCH",) + regression.failures,
        }

    understanding = (core or PlanUnderstandingCore()).understand(
        source_path=str(path),
        source_sha256=source_sha256,
        model_id=f"golden:{case.case_id}",
    )
    observed = _domain_observation(understanding, source_sha256, str(path))
    regression = evaluate_golden_case(case, observed)
    return {
        "case_id": case.case_id,
        "source_sha256": source_sha256,
        "source_exists": True,
        "observed": observed,
        "decision": regression.decision,
        "unsafe_acceptance": regression.unsafe_acceptance,
        "failures": regression.failures,
        "domain_results": dict(regression.domain_results),
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
        "summary": {
            "case_count": len(reports),
            "pass_count": sum(report["decision"] == "PASS" for report in reports),
            "blocked_count": sum(report["decision"] == "BLOCKED" for report in reports),
            "needs_review_count": sum(
                report["decision"] == "NEEDS_REVIEW" for report in reports
            ),
            "unsafe_acceptance_count": sum(
                report["unsafe_acceptance"] for report in reports
            ),
            "domain_metrics": summarize_domain_metrics(
                tuple(
                    evaluate_golden_case(
                        case,
                        report["observed"],
                    )
                    for case, report in zip(cases, reports)
                )
            ),
        },
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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Golden Understanding regression manifest.")
    parser.add_argument("--manifest", required=True, help="Path to golden-understanding manifest JSON")
    parser.add_argument("--output", required=True, help="Path for the machine-checkable JSON report")
    args = parser.parse_args()
    write_report(args.manifest, args.output)
