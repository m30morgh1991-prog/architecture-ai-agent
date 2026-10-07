from runtime.space_model_contract import build_space_model


SOURCE = "a" * 64


def test_explicit_room_name_and_number_are_preserved():
    model = build_space_model(
        model_id="m1",
        source_sha256=SOURCE,
        spaces=[{
            "space_id": "s1",
            "boundary_handle": "b1",
            "bbox": [0, 0, 10, 10],
            "centroid": [5, 5],
            "area": 100,
            "label": "01",
            "name": "Kitchen",
            "number": "01",
            "evidence_ids": ["e1"],
            "identity_status": "EXPLICIT",
        }],
        relations=[],
    )
    space = model.spaces[0]
    assert space.resolved_name == "Kitchen"
    assert space.resolved_number == "01"


def test_schedule_mapping_resolves_space_identity():
    model = build_space_model(
        model_id="m1",
        source_sha256=SOURCE,
        spaces=[{
            "space_id": "s1",
            "boundary_handle": "b1",
            "bbox": [0, 0, 10, 10],
            "centroid": [5, 5],
            "area": 100,
            "label": "03",
            "schedule_name": "Bedroom",
            "schedule_number": "03",
            "evidence_ids": ["e1", "schedule-row-03"],
            "identity_status": "SCHEDULE_MAPPED",
        }],
        relations=[],
    )
    space = model.spaces[0]
    assert space.resolved_name == "Bedroom"
    assert space.resolved_number == "03"


def test_identity_conflict_never_resolves_to_a_guess():
    model = build_space_model(
        model_id="m1",
        source_sha256=SOURCE,
        spaces=[{
            "space_id": "s1",
            "boundary_handle": "b1",
            "bbox": [0, 0, 10, 10],
            "centroid": [5, 5],
            "area": 100,
            "label": "03",
            "name": "Kitchen",
            "number": "03",
            "schedule_name": "Bedroom",
            "schedule_number": "03",
            "evidence_ids": ["e1", "schedule-row-03"],
            "identity_status": "CONFLICT",
        }],
        relations=[],
    )
    space = model.spaces[0]
    assert space.resolved_name is None
    assert space.resolved_number is None
