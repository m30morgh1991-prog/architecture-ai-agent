from runtime.before_after_detection import DetectionSnapshot, compare_before_after

def snap(elements, status="PASS"):
    return DetectionSnapshot("a"*64, "model-1", tuple(elements), status)

def test_clean_approved_change_passes():
    e={"element_id":"F1","element_type":"FURNITURE","state":"EDITABLE","geometry":{"x":1},"evidence_ids":["e1"]}
    r=compare_before_after(before=snap([e]), after=snap([e]), approved_target_ids=("F1",))
    assert r.valid and r.status == "PASS"

def test_locked_change_blocks():
    b={"element_id":"W1","element_type":"WALL","state":"LOCKED","geometry":{"x":1},"evidence_ids":["e1"]}
    a={"element_id":"W1","element_type":"WALL","state":"LOCKED","geometry":{"x":2},"evidence_ids":["e1"]}
    r=compare_before_after(before=snap([b]), after=snap([a]), approved_target_ids=("W1",))
    assert not r.valid and r.status == "BLOCKED"

def test_unapproved_change_blocks():
    b={"element_id":"F1","element_type":"FURNITURE","state":"EDITABLE","geometry":{"x":1},"evidence_ids":["e1"]}
    a={"element_id":"F1","element_type":"FURNITURE","state":"EDITABLE","geometry":{"x":2},"evidence_ids":["e1"]}
    r=compare_before_after(before=snap([b]), after=snap([a]), approved_target_ids=())
    assert not r.valid and r.status == "BLOCKED"

def test_missing_after_is_not_pass():
    e={"element_id":"F1","element_type":"FURNITURE","state":"EDITABLE","geometry":{"x":1},"evidence_ids":["e1"]}
    r=compare_before_after(before=snap([e]), after=None, approved_target_ids=("F1",))
    assert not r.valid and r.status == "UNKNOWN"
