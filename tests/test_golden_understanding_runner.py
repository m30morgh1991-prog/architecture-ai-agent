import hashlib
import json

from runtime.golden_understanding_runner import run_manifest_to_report, sha256_file


def test_sha256_is_stable(tmp_path):
    source = tmp_path / "sample.dwg"
    source.write_bytes(b"golden-source")
    assert sha256_file(source) == hashlib.sha256(b"golden-source").hexdigest()


def test_runner_emits_machine_checkable_report(tmp_path):
    source = tmp_path / "sample.dwg"
    source.write_bytes(b"not-a-real-dwg")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "schema": "golden-understanding-v1",
        "version": "2026-10-08",
        "truth_policy": "DIRECT_AND_VALIDATED_DERIVED_ONLY",
        "cases": [{
            "case_id": "CASE-RUNNER",
            "source_path": str(source),
            "source_sha256": digest,
            "expected_elements": [],
            "expected_domains": [
                "source_profile", "elements", "geometry", "topology",
                "relations", "drawing_evidence", "provenance",
                "fail_closed_decision"
            ],
            "expected_status": "UNKNOWN"
        }]
    }), encoding="utf-8")
    report = run_manifest_to_report(manifest)
    case = report["cases"][0]
    assert report["schema"] == "golden-understanding-report-v1"
    assert case["source_exists"] is True
    assert len(case["source_sha256"]) == 64
    assert case["observed"]["source_profile"]["sha256"] == case["source_sha256"]
    assert case["observed"]["source_profile"]["source_class"] == "ENGINEERING_VECTOR"
    assert case["observed"]["source_profile"]["input_mode"] == "ENGINEERING_PLAN"
    assert case["decision"] in {"UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}
