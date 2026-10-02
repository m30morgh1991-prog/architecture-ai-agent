from runtime.bim_ready_contract import BIMElementIdentity, BIMElementRelation
from runtime.plan_model_contract import PlanElement, PlanModel


SOURCE = "a" * 64


def test_bim_identity_is_optional_for_mvp():
    element = PlanElement(
        "F01", "FURNITURE", "EDITABLE",
        {"kind": "bbox", "bbox": [0, 0, 1, 1]},
        ("ev-f01",), 0.95,
    )
    element.validate()


def test_bim_identity_preserves_semantics_and_properties():
    identity = BIMElementIdentity(
        category="Furniture",
        ifc_class="IfcFurniture",
        name="Sofa",
        level_id="L01",
        parent_id="R01",
        properties=(("material", "fabric"), ("manufacturer", "unknown")),
        external_refs=(("source", "dwg:F01"),),
    )
    element = PlanElement(
        "F01", "FURNITURE", "EDITABLE",
        {"kind": "bbox", "bbox": [0, 0, 1, 1]},
        ("ev-f01",), 0.95, identity,
    )
    element.validate()


def test_plan_model_accepts_bim_relationship_graph():
    elements = (
        PlanElement("R01", "SPACE", "EDITABLE", {"kind": "polygon"}, ("ev-r01",), 0.95),
        PlanElement("D01", "DOOR", "EDITABLE", {"kind": "bbox"}, ("ev-d01",), 0.95),
    )
    model = PlanModel(
        model_id="pm-bim",
        source_sha256=SOURCE,
        drawing_count=1,
        elements=elements,
        bim_relations=(BIMElementRelation("CONNECTS", "R01", "D01"),),
    )
    model.validate()


def test_unknown_bim_relation_endpoint_fails_closed():
    model = PlanModel(
        model_id="pm-bim",
        source_sha256=SOURCE,
        drawing_count=1,
        elements=(
            PlanElement("R01", "SPACE", "EDITABLE", {"kind": "polygon"}, ("ev-r01",), 0.95),
        ),
        bim_relations=(BIMElementRelation("CONNECTS", "R01", "D99"),),
    )
    try:
        model.validate()
    except ValueError as exc:
        assert str(exc) == "BIM_RELATION_ENDPOINT_UNKNOWN"
    else:
        raise AssertionError("Expected fail-closed BIM relation validation")


def test_duplicate_bim_property_keys_are_rejected():
    identity = BIMElementIdentity(
        category="Wall",
        properties=(("fire_rating", "60"), ("fire_rating", "90")),
    )
    try:
        identity.validate()
    except ValueError as exc:
        assert str(exc) == "BIM_PROPERTY_KEY_DUPLICATE"
    else:
        raise AssertionError("Expected duplicate property rejection")
