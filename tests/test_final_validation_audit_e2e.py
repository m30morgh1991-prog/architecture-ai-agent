from runtime.final_validation_audit_e2e import evaluate_final_gate
def test_final_gate_requires_every_invariant():
    assert evaluate_final_gate(approved=True,post_edit_valid=True,source_match=True,model_match=True,audit_complete=True)
def test_final_gate_blocks_missing_audit():
    assert not evaluate_final_gate(approved=True,post_edit_valid=True,source_match=True,model_match=True,audit_complete=False)
