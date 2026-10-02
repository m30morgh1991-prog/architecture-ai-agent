from runtime.golden_dwg_regression import validate_golden_dwg
def test_golden_dwg_requires_all_invariants():
    assert validate_golden_dwg(source_sha256="abc",entity_count=10,candidate_count=4,plan_model_valid=True,evidence_valid=True,bim_graph_valid=True,fail_closed=True)
def test_golden_dwg_fails_on_invalid_model():
    assert not validate_golden_dwg(source_sha256="abc",entity_count=10,candidate_count=4,plan_model_valid=False,evidence_valid=True,bim_graph_valid=True,fail_closed=True)
