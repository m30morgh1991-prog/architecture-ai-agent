from runtime.controlled_editing_e2e_gate import (
    ControlledEditingE2EGate,
    evaluate_controlled_editing_e2e,
)

SOURCE = "a" * 64


def test_all_gates_required():
    result = evaluate_controlled_editing_e2e(
        source_sha256=SOURCE, model_id="m1", target_ids=("F1",),
        impact_status="PASS", approval_status="APPROVED",
        visual_status="READY_FOR_APPROVAL",
    )
    assert result.executable


def test_visual_block_blocks_execution():
    result = evaluate_controlled_editing_e2e(
        source_sha256=SOURCE, model_id="m1", target_ids=("F1",),
        impact_status="PASS", approval_status="APPROVED",
        visual_status="BLOCKED",
    )
    assert not result.executable


def test_unknown_impact_blocks():
    result = evaluate_controlled_editing_e2e(
        source_sha256=SOURCE, model_id="m1", target_ids=("F1",),
        impact_status="UNKNOWN", approval_status="APPROVED",
        visual_status="READY_FOR_APPROVAL",
    )
    assert not result.executable


def test_truthy_string_executable_cannot_pass_direct_construction():
    result = ControlledEditingE2EGate(
        source_sha256=SOURCE, model_id="m1", target_ids=("F1",),
        impact_status="PASS", approval_status="APPROVED",
        visual_status="READY_FOR_APPROVAL", executable="false",
        reason="forged false string",
    )
    try:
        result.validate()
    except ValueError as exc:
        assert "E2E_EXECUTABLE_INVALID" in str(exc)
    else:
        raise AssertionError("non-boolean executable must be rejected")


def test_invalid_source_hash_is_rejected():
    result = ControlledEditingE2EGate(
        source_sha256="abc", model_id="m1", target_ids=("F1",),
        impact_status="PASS", approval_status="APPROVED",
        visual_status="READY_FOR_APPROVAL", executable=True,
        reason="invalid identity",
    )
    try:
        result.validate()
    except ValueError as exc:
        assert "E2E_SOURCE_INVALID" in str(exc)
    else:
        raise AssertionError("invalid source identity must be rejected")
