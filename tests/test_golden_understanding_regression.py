import json

import pytest

from runtime.golden_understanding_regression import (
    evaluate_golden_case,
    load_manifest,
)


def _case(tmp_path):
    manifest = {
        "schema": "golden-understanding-v1",
        "version": "2026-10-08",
        "truth_policy": "DIRECT_AND_VALIDATED_DERIVED_ONLY",
        "cases": [{
            "case_id": "CASE-1",
            "source_path": "test-assets/golden-projects/example.dwg",
            "source_sha256": None,
            "expected_elements": ["WALL", "DOOR"],
            "expected_domains": [
                "source_profile", "elements", "geometry",
                "topology", "relations", "drawing_evidence",
                "provenance", "fail_closed_decision"
            ],
            "expected_status": "UNKNOWN",
            "adversarial": False,
        }],
    }
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps(manifest), encoding="utf-8")
    return load_manifest(p)[0]


def test_manifest_schema_and_case_load(tmp_path):
    case = _case(tmp_path)
    assert case.case_id == "CASE-1"
    assert case.expected_status == "UNKNOWN"


def test_complete_observation_passes(tmp_path):
    case = _case(tmp_path)
    observed = {
        domain: {} for domain in case.expected_domains
    }
    observed["elements"] = ["WALL", "DOOR"]
    observed["fail_closed_decision"] = "UNKNOWN"
    report = evaluate_golden_case(case, observed)
    assert report.decision == "PASS"
    assert not report.failures


def test_empty_domain_requires_review(tmp_path):
    case = _case(tmp_path)
    observed = {domain: {} for domain in case.expected_domains}
    observed["elements"] = ["WALL", "DOOR"]
    observed["fail_closed_decision"] = "UNKNOWN"
    report = evaluate_golden_case(case, observed)
    assert report.decision == "NEEDS_REVIEW"
    assert "MISSING_DOMAIN:source_profile" in report.failures


def test_explicit_unknown_domain_is_covered(tmp_path):
    case = _case(tmp_path)
    observed = {domain: "UNKNOWN" for domain in case.expected_domains}
    observed["elements"] = ["WALL", "DOOR"]
    observed["fail_closed_decision"] = "UNKNOWN"
    report = evaluate_golden_case(case, observed)
    assert report.decision == "PASS"
    assert not report.failures


def test_missing_domain_requires_review(tmp_path):
    case = _case(tmp_path)
    observed = {
        domain: {} for domain in case.expected_domains
        if domain != "topology"
    }
    observed["elements"] = ["WALL", "DOOR"]
    observed["fail_closed_decision"] = "UNKNOWN"
    report = evaluate_golden_case(case, observed)
    assert report.decision == "NEEDS_REVIEW"
    assert "MISSING_DOMAIN:topology" in report.failures


def test_unresolved_evidence_cannot_pass(tmp_path):
    case = _case(tmp_path)
    observed = {domain: {} for domain in case.expected_domains}
    observed["elements"] = ["WALL", "DOOR"]
    observed["uncertainties"] = ["LOW_RESOLUTION"]
    observed["fail_closed_decision"] = "PASS"
    report = evaluate_golden_case(case, observed)
    assert report.decision == "BLOCKED"
    assert report.unsafe_acceptance is True
    assert "UNSAFE_ACCEPTANCE:UNRESOLVED_TO_PASS" in report.failures


def test_invalid_expected_status_is_rejected(tmp_path):
    payload = {
        "schema": "golden-understanding-v1",
        "cases": [{
            "case_id": "BAD",
            "source_path": "x.dwg",
            "expected_domains": ["elements"],
            "expected_status": "NOT_A_DECISION",
        }],
    }
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        load_manifest(p)
