from runtime.scale_unit_runtime_gate import evaluate_runtime_scale

def test_runtime_scale_uses_two_independent_signals():
    result = evaluate_runtime_scale(source_id="dwg-1", declared_unit="MM",
                                    header_unit="MM", evidence_ids=("declared","header"))
    assert result.status == "PASS"
    assert result.unit == "MM"

def test_runtime_scale_conflict_blocks():
    result = evaluate_runtime_scale(source_id="dwg-1", declared_unit="MM",
                                    header_unit="CM", evidence_ids=("declared","header"))
    assert result.status == "BLOCKED"

def test_runtime_scale_single_signal_needs_review():
    result = evaluate_runtime_scale(source_id="dwg-1", header_unit="MM",
                                    evidence_ids=("header",))
    assert result.status == "NEEDS_REVIEW"
