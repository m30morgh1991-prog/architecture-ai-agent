"""Golden DWG regression invariants."""
def validate_golden_dwg(*,source_sha256,entity_count,candidate_count,plan_model_valid,evidence_valid,bim_graph_valid,fail_closed):
    if not source_sha256: return False
    if entity_count < 0 or candidate_count < 0: return False
    return all((plan_model_valid,evidence_valid,bim_graph_valid,fail_closed))
