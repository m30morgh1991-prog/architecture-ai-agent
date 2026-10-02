from runtime.controlled_editing_e2e_gate import evaluate_controlled_editing_e2e

def test_all_gates_required():
    r=evaluate_controlled_editing_e2e(source_sha256="abc",model_id="m1",target_ids=("F1",),impact_status="PASS",approval_status="APPROVED",visual_status="READY_FOR_APPROVAL")
    assert r.executable

def test_visual_block_blocks_execution():
    r=evaluate_controlled_editing_e2e(source_sha256="abc",model_id="m1",target_ids=("F1",),impact_status="PASS",approval_status="APPROVED",visual_status="BLOCKED")
    assert not r.executable

def test_unknown_impact_blocks():
    r=evaluate_controlled_editing_e2e(source_sha256="abc",model_id="m1",target_ids=("F1",),impact_status="UNKNOWN",approval_status="APPROVED",visual_status="READY_FOR_APPROVAL")
    assert not r.executable
