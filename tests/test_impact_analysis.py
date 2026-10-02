from runtime.change_request_contract import ChangeRequest
from runtime.impact_analysis import ImpactStatus, analyze_impact
from runtime.plan_model_contract import ConstraintMap, PlanElement, PlanModel


SOURCE = "a" * 64


def _plan():
    return PlanModel(
        model_id="pm-75",
        source_sha256=SOURCE,
        drawing_count=1,
        elements=(
            PlanElement("F01", "FURNITURE", "EDITABLE",
                        {"kind": "bbox", "bbox": [0, 0, 1, 1]}, ("ev-f01",), 0.95),
            PlanElement("W01", "WALL", "LOCKED",
                        {"kind": "line", "points": [[0, 0], [10, 0]]}, ("ev-w01",), 0.99),
        ),
    )


def _map():
    return ConstraintMap(
        map_id="cm-75",
        model_id="pm-75",
        protected_element_ids=("W01",),
        editable_element_ids=("F01",),
        conditional_element_ids=(),
        unknown_element_ids=(),
        evidence_ids=("ev-f01", "ev-w01"),
    )


def _request(**overrides):
    data = {
        "request_id": "cr-75",
        "source_sha256": SOURCE,
        "model_id": "pm-75",
        "change_type": "FURNITURE_LAYOUT_CHANGE",
        "instruction": "Move the sofa.",
        "target_ids": ("F01",),
        "evidence_ids": ("ev-f01",),
    }
    data.update(overrides)
    return ChangeRequest(**data)


def test_editable_target_passes():
    result = analyze_impact(_plan(), _map(), _request())
    assert result.status == "PASS"
    assert result.impacted_element_ids == ("F01",)
    result.validate()


def test_missing_targets_are_review():
    result = analyze_impact(_plan(), _map(), _request(target_ids=()))
    assert result.status == "NEEDS_REVIEW"
    assert "TARGETS_REQUIRED_FOR_DETERMINISTIC_IMPACT" in result.blockers


def test_unknown_target_fails_closed():
    result = analyze_impact(_plan(), _map(), _request(target_ids=("MISSING",)))
    assert result.status == "UNKNOWN"
    assert "TARGET_ELEMENT_MISSING" in result.blockers


def test_protected_target_is_blocked():
    result = analyze_impact(
        _plan(), _map(),
        _request(target_ids=("W01",), change_type="FURNITURE"),
    )
    assert result.status == "BLOCKED"
    assert "PROTECTED_TARGET" in result.blockers


def test_source_mismatch_is_blocked():
    result = analyze_impact(
        _plan(), _map(),
        _request(source_sha256="b" * 64),
    )
    assert result.status == "BLOCKED"
    assert result.blockers == ("CHANGE_REQUEST_SOURCE_MISMATCH",)


def test_overall_layout_never_auto_passes():
    result = analyze_impact(
        _plan(), _map(),
        _request(
            change_type="OVERALL_ARCHITECTURAL_LAYOUT_CHANGE",
            target_ids=("F01",),
        ),
    )
    assert result.status == "BLOCKED"
    assert "OVERALL_LAYOUT_REQUIRES_PROTECTED_IMPACT_REVIEW" in result.blockers
