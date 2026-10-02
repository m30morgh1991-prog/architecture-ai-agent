from runtime.architectural_relations import ArchitecturalRelationSet, ArchitecturalRelation
from runtime.geometry_topology_validation import (
    GeometryValidation, TopologyValidation, validate_geometry,
    validate_plan_geometry, validate_relation_topology,
)
from runtime.plan_model_contract import PlanElement, PlanModel


def _model(geometry):
    return PlanModel(
        model_id="pm-h73",
        source_sha256="a" * 64,
        drawing_count=1,
        elements=(PlanElement("W1", "WALL", "LOCKED", geometry, ("e1",), 0.99),),
    )


def _relations(status="SUPPORTED"):
    return ArchitecturalRelationSet(
        set_id="rs1",
        source_sha256="a" * 64,
        relations=(
            ArchitecturalRelation(
                "r1", "a" * 64, "ELEMENT_ADJACENCY", "W1", "W2", ("e1",), status, 1.0 if status=="SUPPORTED" else 0.0
            ),
        ),
    )


def test_polygon_geometry_passes():
    validate_geometry({"kind": "polygon", "points": [(0,0), (10,0), (10,5), (0,5)]})


def test_self_intersecting_polygon_is_rejected():
    try:
        validate_geometry({"kind": "polygon", "points": [(0,0), (10,10), (0,10), (10,0)]})
    except ValueError as exc:
        assert str(exc) == "POLYGON_SELF_INTERSECTION"
    else:
        raise AssertionError("expected rejection")


def test_plan_geometry_is_fail_closed():
    result = validate_plan_geometry(_model({"kind": "bbox", "bbox": [0, 0, 0, 5]}))
    assert result[0].status == "BLOCKED"
    assert result[0].issues == ("GEOMETRY_BBOX_NON_POSITIVE",)


def test_pass_validation_cannot_contain_issues():
    try:
        GeometryValidation("W1", "PASS", ("unexpected",)).validate()
    except ValueError as exc:
        assert str(exc) == "PASS_CANNOT_HAVE_GEOMETRY_ISSUES"
    else:
        raise AssertionError("expected rejection")


def test_topology_source_mismatch_is_blocked():
    class FakeRelations:
        source_sha256 = "b" * 64
        relations = ()
        def validate(self): pass
    result = validate_relation_topology(_model({"kind":"bbox","bbox":[0,0,1,1]}), FakeRelations())
    assert result.status == "BLOCKED"
    assert result.issues == ("ARCH_RELATION_SOURCE_MISMATCH",)


def test_unsupported_relation_is_never_pass():
    result = validate_relation_topology(_model({"kind":"bbox","bbox":[0,0,1,1]}), _relations("UNKNOWN"))
    assert result.status == "NEEDS_REVIEW"


def test_mixed_space_element_relations_use_correct_endpoint_domains():
    from runtime.space_model_contract import SpaceModel, SpaceRecord
    space = SpaceRecord(
        "S1", "b1", (0, 0, 10, 10), (5, 5), 100, "Living", ("e1",), "ACCESSIBLE"
    )
    model = PlanModel(
        model_id="pm-h73-mixed",
        source_sha256="a" * 64,
        drawing_count=1,
        elements=(PlanElement("W1", "WALL", "LOCKED", {"kind":"bbox","bbox":[0,0,1,1]}, ("e1",), 0.99),),
        space_model=SpaceModel("sm1", "a" * 64, (space,), ()),
    )
    relation = ArchitecturalRelation(
        "r-mixed", "a" * 64, "SPACE_BOUNDARY_ELEMENT",
        "S1", "W1", ("e1",), "SUPPORTED", 1.0
    )
    relations = ArchitecturalRelationSet("rs-mixed", "a" * 64, (relation,))
    result = validate_relation_topology(model, relations)
    assert result.status == "PASS"
    assert result.issues == ()
