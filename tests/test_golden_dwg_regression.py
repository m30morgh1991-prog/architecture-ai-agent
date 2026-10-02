from runtime.golden_dwg_regression import validate_golden_dwg

def test_golden_dwg_requires_all_invariants():
    assert validate_golden_dwg(source_sha256="a"*64, entity_count=10, candidate_count=2,
                               candidate_ids=("C01","W01"), plan_model_valid=True,
                               evidence_valid=True, bim_graph_valid=True, fail_closed=True)

def test_golden_dwg_rejects_candidate_count_mismatch():
    try:
        validate_golden_dwg(source_sha256="a"*64, entity_count=10, candidate_count=2,
                            candidate_ids=("C01",), plan_model_valid=True,
                            evidence_valid=True, bim_graph_valid=True, fail_closed=True)
    except ValueError as exc:
        assert str(exc) == "GOLDEN_CANDIDATE_COUNT_MISMATCH"
    else:
        raise AssertionError("expected mismatch to fail closed")

def test_golden_dwg_rejects_invalid_source_identity():
    try:
        validate_golden_dwg(source_sha256="abc", entity_count=10, candidate_count=0,
                            candidate_ids=(), plan_model_valid=True,
                            evidence_valid=True, bim_graph_valid=True, fail_closed=True)
    except ValueError as exc:
        assert str(exc) == "GOLDEN_SOURCE_SHA256_INVALID"
    else:
        raise AssertionError("expected source identity to fail closed")
