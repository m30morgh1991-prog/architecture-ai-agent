"""H73 deterministic geometry and topology validation contract.

Geometry is validated independently from semantic approval. Invalid, incomplete,
non-finite, or contradictory geometry is fail-closed and cannot become PASS.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Literal

ValidationStatus = Literal["PASS", "UNKNOWN", "BLOCKED", "NEEDS_REVIEW"]

_ALLOWED_GEOMETRY = {"point", "line", "polyline", "polygon", "bbox"}


def _number(value: Any) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise ValueError("GEOMETRY_NUMBER_INVALID") from None
    if not isfinite(result):
        raise ValueError("GEOMETRY_NUMBER_NONFINITE")
    return result


def _point(value: Any) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("GEOMETRY_POINT_INVALID")
    return (_number(value[0]), _number(value[1]))


def _points(values: Any, *, minimum: int) -> tuple[tuple[float, float], ...]:
    if not isinstance(values, (list, tuple)) or len(values) < minimum:
        raise ValueError("GEOMETRY_POINTS_INSUFFICIENT")
    return tuple(_point(item) for item in values)


def _bbox(values: Any) -> tuple[float, float, float, float]:
    if not isinstance(values, (list, tuple)) or len(values) != 4:
        raise ValueError("GEOMETRY_BBOX_INVALID")
    x0, y0, x1, y1 = (_number(item) for item in values)
    if x1 <= x0 or y1 <= y0:
        raise ValueError("GEOMETRY_BBOX_NON_POSITIVE")
    return x0, y0, x1, y1


def polygon_area(points: tuple[tuple[float, float], ...]) -> float:
    if len(points) < 3:
        raise ValueError("POLYGON_POINTS_INSUFFICIENT")
    ring = points if points[0] == points[-1] else points + (points[0],)
    return abs(
        sum(
            ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1]
            for i in range(len(ring) - 1)
        )
    ) / 2.0


def _orientation(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _segments_intersect(
    a: tuple[float, float], b: tuple[float, float],
    c: tuple[float, float], d: tuple[float, float],
) -> bool:
    def on_segment(p, q, r):
        return (
            min(p[0], r[0]) <= q[0] <= max(p[0], r[0])
            and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])
        )

    o1, o2 = _orientation(a, b, c), _orientation(a, b, d)
    o3, o4 = _orientation(c, d, a), _orientation(c, d, b)
    eps = 1e-9
    if abs(o1) < eps and on_segment(a, c, b):
        return True
    if abs(o2) < eps and on_segment(a, d, b):
        return True
    if abs(o3) < eps and on_segment(c, a, d):
        return True
    if abs(o4) < eps and on_segment(c, b, d):
        return True
    return ((o1 > 0) != (o2 > 0)) and ((o3 > 0) != (o4 > 0))


def validate_geometry(geometry: dict[str, Any]) -> None:
    if not isinstance(geometry, dict):
        raise ValueError("GEOMETRY_CONTAINER_INVALID")
    kind = geometry.get("kind")
    if kind not in _ALLOWED_GEOMETRY:
        raise ValueError("GEOMETRY_KIND_INVALID")
    if kind == "point":
        _point(geometry.get("point"))
    elif kind == "line":
        _points(geometry.get("points"), minimum=2)
    elif kind == "polyline":
        points = _points(geometry.get("points"), minimum=2)
        if len(set(points)) < 2:
            raise ValueError("POLYLINE_DEGENERATE")
    elif kind == "polygon":
        points = _points(geometry.get("points"), minimum=3)
        if polygon_area(points) <= 0:
            raise ValueError("POLYGON_AREA_ZERO")
        ring = points if points[0] == points[-1] else points + (points[0],)
        for i in range(len(ring) - 1):
            for j in range(i + 1, len(ring) - 1):
                if j in {i - 1, i + 1}:
                    continue
                if i == 0 and j == len(ring) - 2:
                    continue
                if _segments_intersect(ring[i], ring[i + 1], ring[j], ring[j + 1]):
                    raise ValueError("POLYGON_SELF_INTERSECTION")
    elif kind == "bbox":
        _bbox(geometry.get("bbox"))


@dataclass(frozen=True)
class GeometryValidation:
    element_id: str
    status: ValidationStatus
    issues: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.element_id:
            raise ValueError("GEOMETRY_VALIDATION_ELEMENT_ID_MISSING")
        if self.status not in {"PASS", "UNKNOWN", "BLOCKED", "NEEDS_REVIEW"}:
            raise ValueError("GEOMETRY_VALIDATION_STATUS_INVALID")
        if self.status == "PASS" and self.issues:
            raise ValueError("PASS_CANNOT_HAVE_GEOMETRY_ISSUES")


@dataclass(frozen=True)
class TopologyValidation:
    source_sha256: str
    status: ValidationStatus
    issues: tuple[str, ...] = ()
    checked_element_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        if len(self.source_sha256) != 64:
            raise ValueError("TOPOLOGY_SOURCE_INVALID")
        if self.status not in {"PASS", "UNKNOWN", "BLOCKED", "NEEDS_REVIEW"}:
            raise ValueError("TOPOLOGY_STATUS_INVALID")
        if len(set(self.checked_element_ids)) != len(self.checked_element_ids):
            raise ValueError("TOPOLOGY_ELEMENT_ID_DUPLICATE")
        if self.status == "PASS" and self.issues:
            raise ValueError("PASS_CANNOT_HAVE_TOPOLOGY_ISSUES")


def validate_plan_geometry(plan_model) -> tuple[GeometryValidation, ...]:
    plan_model.validate()
    results = []
    for element in plan_model.elements:
        try:
            validate_geometry(element.geometry)
        except ValueError as exc:
            results.append(GeometryValidation(element.element_id, "BLOCKED", (str(exc),)))
        else:
            results.append(GeometryValidation(element.element_id, "PASS"))
    return tuple(results)


def validate_relation_topology(plan_model, relation_set) -> TopologyValidation:
    plan_model.validate()
    relation_set.validate()
    if relation_set.source_sha256 != plan_model.source_sha256:
        return TopologyValidation(
            plan_model.source_sha256, "BLOCKED",
            ("ARCH_RELATION_SOURCE_MISMATCH",),
        )
    element_ids = {element.element_id for element in plan_model.elements}
    space_ids = {space.space_id for space in plan_model.spaces}
    checked = []
    issues = []
    for relation in relation_set.relations:
        checked.extend((relation.from_id, relation.to_id))
        if relation.relation_kind == "SPACE_ADJACENCY":
            if relation.from_id not in space_ids or relation.to_id not in space_ids:
                issues.append("SPACE_RELATION_ENDPOINT_INVALID")
        elif relation.relation_kind in {"SPACE_BOUNDARY_ELEMENT", "SPACE_OPENING_ELEMENT"}:
            if relation.from_id not in space_ids or relation.to_id not in element_ids:
                issues.append("SPACE_ELEMENT_RELATION_ENDPOINT_INVALID")
        elif relation.relation_kind in {
            "ELEMENT_ADJACENCY", "ELEMENT_CONTAINS", "ELEMENT_INTERSECTS"
        }:
            if relation.from_id not in element_ids or relation.to_id not in element_ids:
                issues.append("ELEMENT_RELATION_ENDPOINT_INVALID")
        if relation.status != "SUPPORTED":
            issues.append(f"RELATION_{relation.status}")
    if issues:
        return TopologyValidation(
            plan_model.source_sha256,
            "NEEDS_REVIEW" if any(i.startswith("RELATION_") for i in issues) else "BLOCKED",
            tuple(sorted(set(issues))),
            tuple(dict.fromkeys(checked)),
        )
    return TopologyValidation(
        plan_model.source_sha256, "PASS", (), tuple(dict.fromkeys(checked))
    )
