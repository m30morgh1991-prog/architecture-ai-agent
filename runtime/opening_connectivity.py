"""Evidence-backed opening-to-space connectivity helpers.

The module stays fail-closed: insertion-point proximity is only a candidate
signal. Approval-grade connectivity requires a native opening span, a host
wall verified against the supplied wall inventory, and source evidence IDs.
"""
from __future__ import annotations

from math import hypot, isfinite
from numbers import Real


def _finite_point(value):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        return None
    point = []
    for coordinate in value:
        if isinstance(coordinate, bool) or not isinstance(coordinate, Real):
            return None
        try:
            number = float(coordinate)
        except (TypeError, ValueError, OverflowError):
            return None
        if not isfinite(number):
            return None
        point.append(number)
    return tuple(point)


def _segments(points):
    if not isinstance(points, (list, tuple)) or len(points) < 3:
        return []
    pts = [_finite_point(point) for point in points]
    if any(point is None for point in pts):
        return []
    return list(zip(pts, pts[1:] + pts[:1]))


def _distance_to_segment(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    wx, wy = p[0] - a[0], p[1] - a[1]
    den = vx * vx + vy * vy
    if den == 0:
        return hypot(p[0] - a[0], p[1] - a[1])
    t = max(0, min(1, (wx * vx + wy * vy) / den))
    q = (a[0] + t * vx, a[1] + t * vy)
    return hypot(p[0] - q[0], p[1] - q[1])


def _span_touches_boundary(span, points, tolerance):
    if not isinstance(span, (list, tuple)) or len(span) != 2:
        return False
    a, b = _finite_point(span[0]), _finite_point(span[1])
    if a is None or b is None:
        return False
    segments = _segments(points)
    if not segments:
        return False
    # Endpoint proximity is deliberately conservative and avoids treating a
    # nearby insertion point as an architectural opening by itself.
    return (
        min(_distance_to_segment(a, c, d) for c, d in segments) <= tolerance
        and min(_distance_to_segment(b, c, d) for c, d in segments) <= tolerance
    )


def _valid_evidence_id(value):
    return isinstance(value, str) and bool(value.strip())


def classify_opening_connectivity(
    openings, spaces, boundary_points, tolerance=1.0, host_wall_ids=None
):
    """Classify opening connectivity using native span + two-boundary evidence.

    CONNECTED_BY_OPENING is emitted only when the opening span touches exactly
    two distinct space boundaries, the host wall is present in the explicitly
    supplied wall inventory, and all three opening evidence references exist.
    Even then, the relation status remains UNKNOWN pending downstream review.
    """
    if isinstance(tolerance, bool) or not isinstance(tolerance, Real):
        raise ValueError("OPENING_CONNECTIVITY_TOLERANCE_INVALID")
    try:
        tolerance = float(tolerance)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("OPENING_CONNECTIVITY_TOLERANCE_INVALID") from None
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError("OPENING_CONNECTIVITY_TOLERANCE_INVALID")
    if not isinstance(openings, (list, tuple)):
        raise ValueError("OPENING_CONNECTIVITY_OPENINGS_INVALID")
    if not isinstance(spaces, (list, tuple)):
        raise ValueError("OPENING_CONNECTIVITY_SPACES_INVALID")
    if not isinstance(boundary_points, dict):
        raise ValueError("OPENING_CONNECTIVITY_BOUNDARIES_INVALID")

    if isinstance(host_wall_ids, (list, tuple, set, frozenset)):
        verified_host_wall_ids = {
            value for value in host_wall_ids if _valid_evidence_id(value)
        }
    else:
        # A string is not an inventory: iterating it would turn characters
        # into apparently verified wall IDs.
        verified_host_wall_ids = set()

    out = []
    for index, opening in enumerate(openings):
        if not isinstance(opening, dict):
            opening = {}
        opening_id = opening.get("opening_id")
        stable_opening_id = opening_id if _valid_evidence_id(opening_id) else f"UNKNOWN-{index}"
        point = _finite_point(opening.get("point"))
        span = opening.get("span")
        touched = []
        for space in spaces:
            if not isinstance(space, dict):
                continue
            boundary_handle = space.get("boundary_handle")
            if not _valid_evidence_id(boundary_handle):
                continue
            pts = boundary_points.get(boundary_handle, [])
            segments = _segments(pts)
            if not segments:
                continue
            if span and _span_touches_boundary(span, pts, tolerance):
                touched.append(space)
            elif not span and point is not None and min(
                _distance_to_segment(point, a, b) for a, b in segments
            ) <= tolerance:
                touched.append(space)

        host_wall_id = opening.get("host_wall_id")
        host_wall_evidence_id = opening.get("host_wall_evidence_id")
        host_wall_evidenced = bool(
            _valid_evidence_id(host_wall_id)
            and host_wall_id in verified_host_wall_ids
            and _valid_evidence_id(host_wall_evidence_id)
        )
        required_opening_evidence = (
            opening.get("evidence_id"),
            opening.get("span_evidence_id"),
            host_wall_evidence_id,
        )
        opening_evidence_complete = all(
            _valid_evidence_id(value) for value in required_opening_evidence
        )
        space_evidence_complete = all(
            isinstance(space.get("evidence_ids"), (list, tuple))
            and bool(space.get("evidence_ids"))
            and all(_valid_evidence_id(value) for value in space["evidence_ids"])
            for space in touched
        )
        distinct_spaces = (
            len(touched) == 2
            and touched[0].get("space_id") != touched[1].get("space_id")
            and _valid_evidence_id(touched[0].get("space_id"))
            and _valid_evidence_id(touched[1].get("space_id"))
        )

        if (
            distinct_spaces
            and _valid_evidence_id(opening_id)
            and span
            and host_wall_evidenced
            and opening_evidence_complete
            and space_evidence_complete
        ):
            a, b = touched
            out.append({
                "relation_id": f"{a['space_id']}__{b['space_id']}__OPENING-{stable_opening_id}",
                "from": a["space_id"],
                "to": b["space_id"],
                "type": "CONNECTED_BY_OPENING",
                "opening_id": stable_opening_id,
                "evidence_ids": (
                    list(a["evidence_ids"])
                    + list(b["evidence_ids"])
                    + list(required_opening_evidence)
                ),
                "status": "UNKNOWN",
            })
        else:
            evidence_ids = [
                value for value in (
                    opening.get("evidence_id"),
                    opening.get("span_evidence_id"),
                    host_wall_evidence_id,
                ) if _valid_evidence_id(value)
            ]
            out.append({
                "relation_id": f"OPENING-{stable_opening_id}__UNRESOLVED",
                "from": None,
                "to": None,
                "type": "OPENING_CONNECTIVITY_UNKNOWN",
                "opening_id": stable_opening_id,
                "evidence_ids": evidence_ids,
                "status": "UNKNOWN",
                "touched_space_count": len(touched),
                "host_wall_evidenced": host_wall_evidenced,
                "opening_evidence_complete": opening_evidence_complete,
                "space_evidence_complete": space_evidence_complete,
            })
    return out
