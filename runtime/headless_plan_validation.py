"""Provider-neutral headless validation for real plan runtime results."""

REQUIRED_SPACE_KEYS = {
    "space_id", "boundary_handle", "bbox", "centroid", "area", "evidence_ids", "status"
}


def validate_real_plan_result(result):
    """Validate structural invariants without rendering or approving semantics."""
    failures = []

    source_sha = result.get("source", {}).get("sha256")
    evidence = result.get("evidence", {})
    detection = result.get("detection", {})
    contracts = result.get("contracts", {})
    constraint_map = result.get("constraint_map", {})
    locked = result.get("locked_element_detection", {})

    if not source_sha or evidence.get("source_sha256") != source_sha:
        failures.append("SOURCE_EVIDENCE_SHA_MISMATCH")
    if detection.get("artifact_sha256") != source_sha:
        failures.append("SOURCE_DETECTION_SHA_MISMATCH")
    if detection.get("dwg_entity_count", 0) <= 0:
        failures.append("DWG_ENTITY_EVIDENCE_MISSING")
    if not contracts.get("plan_model_id") or constraint_map.get("model_id") != contracts.get("plan_model_id"):
        failures.append("PLAN_MODEL_ID_MISMATCH")
    if not contracts.get("constraint_map_id") or constraint_map.get("map_id") != contracts.get("constraint_map_id"):
        failures.append("CONSTRAINT_MAP_ID_MISMATCH")

    spaces = locked.get("spaces")
    relations = locked.get("space_relations")
    if not isinstance(spaces, list):
        failures.append("SPACES_NOT_LIST")
    else:
        for space in spaces:
            missing = REQUIRED_SPACE_KEYS - set(space)
            if missing:
                failures.append("SPACE_SCHEMA_INCOMPLETE")
                break
            if space.get("status") != "UNKNOWN":
                failures.append("SPACE_SEMANTICS_NOT_FAIL_CLOSED")
                break

    if not isinstance(relations, list):
        failures.append("SPACE_RELATIONS_NOT_LIST")
    else:
        for relation in relations:
            if relation.get("type") == "OVERLAP_CANDIDATE" and relation.get("status") != "UNKNOWN":
                failures.append("OVERLAP_CANDIDATE_NOT_UNKNOWN")
                break

    # This validator never upgrades a blocked/unknown runtime to PASS.
    return {
        "status": "PASS" if not failures else "BLOCKED",
        "failures": tuple(failures),
        "semantic_approval": "NOT_GRANTED",
    }
