import pytest
from runtime.scale_unit_evidence import ScaleEvidence, evaluate_scale_evidence

def test_two_independent_signals_pass_with_known_unit():
    r=evaluate_scale_evidence(source_id="dwg1",unit="MM",explicit_unit=True,header_unit=True,dimension_evidence=False,source_metadata=False,evidence_ids=("h","u"))
    assert r.status=="PASS" and r.scale_known and r.unit=="MM"

def test_conflicting_units_block():
    r=evaluate_scale_evidence(source_id="dwg1",unit="MM",explicit_unit="MM",header_unit="CM",dimension_evidence=True,source_metadata=True,evidence_ids=("h","u"))
    assert r.status=="BLOCKED" and r.unit=="UNKNOWN"

def test_single_signal_needs_review():
    r=evaluate_scale_evidence(source_id="dwg1",unit="MM",explicit_unit=True,header_unit=False,dimension_evidence=False,source_metadata=False,evidence_ids=("u",))
    assert r.status=="NEEDS_REVIEW"

def test_no_signal_unknown():
    r=evaluate_scale_evidence(source_id="dwg1",unit="UNKNOWN",explicit_unit=False,header_unit=False,dimension_evidence=False,source_metadata=False,evidence_ids=("src",))
    assert r.status=="UNKNOWN"

def test_multiple_signals_without_resolvable_unit_cannot_pass():
    r=evaluate_scale_evidence(source_id="dwg1",unit="UNKNOWN",explicit_unit=True,header_unit=True,dimension_evidence=False,source_metadata=False,evidence_ids=("explicit","header"))
    assert r.status=="NEEDS_REVIEW"
    assert r.unit=="UNKNOWN"
    assert not r.scale_known

def test_unknown_string_is_not_counted_as_unit_evidence():
    r=evaluate_scale_evidence(source_id="dwg1",unit="UNKNOWN",explicit_unit="UNKNOWN",header_unit="UNKNOWN",dimension_evidence=False,source_metadata=False,evidence_ids=("src",))
    assert r.status=="UNKNOWN"

def test_pass_with_unknown_unit_is_rejected_by_contract():
    evidence=ScaleEvidence("dwg1","UNKNOWN",True,0.99,("e1","e2"),"PASS")
    with pytest.raises(ValueError,match="SCALE_PASS_REQUIRES_VERIFIED_SCALE_AND_UNIT"):
        evidence.validate()

def test_units_are_normalized_before_pass():
    r=evaluate_scale_evidence(source_id="dwg1",unit="mm",explicit_unit="mm",header_unit="MM",dimension_evidence=False,source_metadata=False,evidence_ids=("text","header"))
    assert r.status=="PASS" and r.unit=="MM"

def test_unsupported_unit_label_cannot_become_pass():
    r=evaluate_scale_evidence(source_id="dwg1",unit="MM",explicit_unit="MILLIMETERS",header_unit=True,dimension_evidence=False,source_metadata=False,evidence_ids=("text","header"))
    assert r.status=="NEEDS_REVIEW"
    assert not r.scale_known
