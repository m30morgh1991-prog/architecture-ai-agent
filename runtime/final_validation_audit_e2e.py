"""Final validation and audit gate."""
def evaluate_final_gate(*,approved,post_edit_valid,source_match,model_match,audit_complete):
    return bool(approved and post_edit_valid and source_match and model_match and audit_complete)
