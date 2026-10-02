from runtime.post_edit_diff_validation import build_post_edit_diff
def test_post_edit_passes_without_locked_changes():
    r=build_post_edit_diff(changed_ids=("F1",),locked_changes=(),source_sha256="abc",model_id="m1")
    assert r.valid
def test_locked_change_blocks():
    r=build_post_edit_diff(changed_ids=("F1","W1"),locked_changes=("W1",),source_sha256="abc",model_id="m1")
    assert not r.valid
