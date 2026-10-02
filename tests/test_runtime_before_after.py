from runtime.runtime_before_after import compare_runtime_detections, snapshot_from_detection


def _detection(candidate_id="DWG-00000", evidence=("e1",), state="LOCKED"):
    return {
        "native_dwg_candidates": [{
            "candidate_id": candidate_id,
            "element_type": "COLUMN",
            "status": state,
            "evidence_ids": list(evidence),
            "geometry": {"bbox": [0, 0, 10, 10]},
        }]
    }


def test_runtime_detection_snapshot_is_identity_and_evidence_aware():
    snapshot = snapshot_from_detection(
        source_sha256="a" * 64,
        model_id="plan-1",
        detection=_detection(),
        status="PASS",
    )
    assert snapshot.elements[0]["element_id"] == "DWG-00000"
    assert snapshot.elements[0]["state"] == "LOCKED"
    assert snapshot.elements[0]["evidence_ids"] == ("e1",)


def test_runtime_before_after_clean_approved_change_passes():
    before = _detection("F-01", ("e1",), "EDITABLE")
    after = _detection("F-01", ("e1", "e2"), "EDITABLE")
    before["native_dwg_candidates"][0]["element_type"] = "FURNITURE"
    after["native_dwg_candidates"][0]["element_type"] = "FURNITURE"
    before["native_dwg_candidates"][0]["geometry"] = {"bbox": [0, 0, 10, 10]}
    after["native_dwg_candidates"][0]["geometry"] = {"bbox": [20, 0, 10, 10]}

    result = compare_runtime_detections(
        before_detection=before,
        after_detection=after,
        source_sha256="a" * 64,
        model_id="plan-1",
        before_status="PASS",
        after_status="PASS",
        approved_target_ids=("F-01",),
    )
    assert result.status == "PASS"
    assert result.changed_ids == ("F-01",)


def test_runtime_before_after_locked_change_blocks():
    result = compare_runtime_detections(
        before_detection=_detection(),
        after_detection=_detection(evidence=("e1", "e2")),
        source_sha256="a" * 64,
        model_id="plan-1",
        before_status="PASS",
        after_status="PASS",
        approved_target_ids=(),
    )
    assert result.status == "BLOCKED"
    assert result.locked_changed_ids == ("DWG-00000",)


def test_runtime_before_after_missing_after_never_passes():
    result = compare_runtime_detections(
        before_detection=_detection(),
        after_detection=None,
        source_sha256="a" * 64,
        model_id="plan-1",
        before_status="PASS",
        after_status=None,
    )
    assert result.status == "UNKNOWN"
    assert result.valid is False
