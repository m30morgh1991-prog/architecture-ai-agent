from runtime.native_dwg_structural_detection import detect_native_dwg_candidates,promote_candidates
def test_native_dwg_needs_independent_evidence():
    c=detect_native_dwg_candidates([{"type":"INSERT","layer":"COLUMNS","block":"COL_01","evidence_ids":("e1",)}])[0]
    assert c.element_type=="COLUMNS" and c.status=="NEEDS_REVIEW"
def test_native_dwg_promotes_with_topology():
    c=detect_native_dwg_candidates([{"type":"INSERT","layer":"COLUMNS","block":"COL_01","closed":True,"topology_neighbor_count":2,"evidence_ids":("e1","e2")}])[0]
    assert c.status=="LOCKED" and c.confidence>=.95
def test_contradiction_blocks():
    c=detect_native_dwg_candidates([{"type":"INSERT","layer":"DOOR","block":"DOOR_01","closed":True,"topology_neighbor_count":1,"evidence_ids":("e1",)}])
    assert promote_candidates(c,("DWG-00000",))[0].status=="BLOCKED"
