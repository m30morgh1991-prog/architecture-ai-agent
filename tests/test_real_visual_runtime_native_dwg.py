from runtime.real_visual_runtime import RealVisualArtifactAdapter, VisualArtifact


def test_real_visual_runtime_exposes_native_dwg_candidates():
    artifact = VisualArtifact(
        source_path="sample.dwg",
        input_type="DWG",
        sha256="a" * 64,
        width=0,
        height=0,
        page_count=1,
        image={
            "entity_count": 1,
            "extmin": (0, 0),
            "extmax": (100, 100),
            "entities": [{
                "type": "INSERT",
                "layer": "COLUMNS",
                "block": "COL_01",
                "closed": True,
                "topology_neighbor_count": 2,
                "evidence_ids": ("dwg-e1", "dwg-e2"),
            }],
        },
    )

    result = RealVisualArtifactAdapter().detect(artifact)

    assert result["fixed_element_identification"]["status"] == "LOCKED"
    assert len(result["native_dwg_candidates"]) == 1
    assert result["native_dwg_candidates"][0]["candidate_id"] == "DWG-00000"
    assert result["native_dwg_candidates"][0]["evidence_ids"] == ["dwg-e1", "dwg-e2"]
