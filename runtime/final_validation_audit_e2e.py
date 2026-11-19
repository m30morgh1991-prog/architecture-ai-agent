"""Final validation and audit gate."""


def evaluate_final_gate(*, approved, post_edit_valid, source_match, model_match, audit_complete):
    return all(
        value is True
        for value in (
            approved,
            post_edit_valid,
            source_match,
            model_match,
            audit_complete,
        )
    )
