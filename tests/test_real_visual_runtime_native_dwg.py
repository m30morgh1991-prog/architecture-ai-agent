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


class _DxftypePropertyEntity:
    dxftype = "INSERT"
    dxf = {"layer": "COLUMNS", "name": "COL_02"}
    closed = True


class _FakeModelspace:
    def query(self):
        return [_DxftypePropertyEntity()]


class _FakeDocument:
    def modelspace(self):
        return _FakeModelspace()

    def header_variables(self):
        return {"extmin": (0, 0), "extmax": (100, 100)}


def test_real_visual_runtime_accepts_dxftype_property(tmp_path, monkeypatch):
    import runtime.real_visual_runtime as module

    source = tmp_path / "sample.dwg"
    source.write_bytes(b"fake-dwg")
    monkeypatch.setattr(module.ezdwg, "read", lambda _path: _FakeDocument())

    artifact = RealVisualArtifactAdapter().ingest(str(source))
    assert artifact.image["entities"][0]["type"] == "INSERT"


class _FakeDocumentWithoutHeader:
    def modelspace(self):
        return _FakeModelspace()


def test_real_visual_runtime_allows_missing_optional_header_metadata(tmp_path, monkeypatch):
    import runtime.real_visual_runtime as module

    source = tmp_path / "sample-no-header.dwg"
    source.write_bytes(b"fake-dwg")
    monkeypatch.setattr(module.ezdwg, "read", lambda _path: _FakeDocumentWithoutHeader())

    artifact = RealVisualArtifactAdapter().ingest(str(source))
    assert artifact.image["extmin"] is None
    assert artifact.image["extmax"] is None
    assert artifact.image["entity_count"] == 1
