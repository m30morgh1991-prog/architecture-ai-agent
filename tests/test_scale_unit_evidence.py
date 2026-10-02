from runtime.scale_unit_evidence import evaluate_scale_evidence

def test_two_independent_signals_pass():
    r=evaluate_scale_evidence(source_id="dwg1",unit="MM",explicit_unit=True,header_unit=True,dimension_evidence=False,source_metadata=False,evidence_ids=("h","u"))
    assert r.status=="PASS" and r.scale_known

def test_conflicting_units_block():
    r=evaluate_scale_evidence(source_id="dwg1",unit="MM",explicit_unit="MM",header_unit="CM",dimension_evidence=True,source_metadata=True,evidence_ids=("h","u"))
    assert r.status=="BLOCKED"

def test_single_signal_needs_review():
    r=evaluate_scale_evidence(source_id="dwg1",unit="MM",explicit_unit=True,header_unit=False,dimension_evidence=False,source_metadata=False,evidence_ids=("u",))
    assert r.status=="NEEDS_REVIEW"

def test_no_signal_unknown():
    r=evaluate_scale_evidence(source_id="dwg1",unit="UNKNOWN",explicit_unit=False,header_unit=False,dimension_evidence=False,source_metadata=False,evidence_ids=("src",))
    assert r.status=="UNKNOWN"
