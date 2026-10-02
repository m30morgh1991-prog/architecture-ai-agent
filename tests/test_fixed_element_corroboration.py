from runtime.fixed_element_corroboration import corroborate_fixed_element


def test_geometry_plus_semantics_can_lock_with_three_sources():
    r = corroborate_fixed_element(
        element_id="C01", element_type="COLUMNS",
        geometry_evidence=True, semantic_evidence=True,
        source_metadata_evidence=True, topology_evidence=False,
        evidence_ids=("geo", "sem", "meta"),
    )
    assert r.status == "LOCKED"
    assert r.confidence == 0.95
    r.validate()


def test_two_sources_without_high_confidence_require_review():
    r = corroborate_fixed_element(
        element_id="W01", element_type="WALLS",
        geometry_evidence=True, semantic_evidence=True,
        source_metadata_evidence=False, topology_evidence=False,
        evidence_ids=("geo", "sem"),
    )
    assert r.status == "NEEDS_REVIEW"


def test_geometry_alone_stays_unknown():
    r = corroborate_fixed_element(
        element_id="D01", element_type="DOORS",
        geometry_evidence=True, semantic_evidence=False,
        source_metadata_evidence=False, topology_evidence=False,
        evidence_ids=("geo",),
    )
    assert r.status == "UNKNOWN"


def test_contradiction_blocks():
    r = corroborate_fixed_element(
        element_id="C01", element_type="COLUMNS",
        geometry_evidence=True, semantic_evidence=True,
        source_metadata_evidence=True, topology_evidence=True,
        contradiction=True,
        evidence_ids=("geo", "sem", "meta", "topo"),
    )
    assert r.status == "BLOCKED"
