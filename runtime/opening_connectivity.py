"""Evidence-backed opening-to-space connectivity helpers.

The module stays fail-closed: insertion-point proximity is only a candidate
signal. Approval-grade connectivity requires a native opening span, a host
wall verified against the supplied wall inventory, and source evidence IDs.
"""
from __future__ import annotations

from math import hypot


def _segments(points):
    pts = [(float(p[0]), float(p[1])) for p in points]
    return list(zip(pts, pts[1:] + pts[:1])) if len(pts) >= 3 else []


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
    if not span or len(span) < 2 or not points:
        return False
    a, b = span[0], span[1]
    # Endpoint proximity is deliberately conservative and avoids treating a
    # nearby insertion point as an architectural opening by itself.
    return (
        min(_distance_to_segment(a, c, d) for c, d in _segments(points)) <= tolerance
        and min(_distance_to_segment(b, c, d) for c, d in _segments(points)) <= tolerance
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
    verified_host_wall_ids = {
        value for value in (host_wall_ids or ()) if _valid_evidence_id(value)
    }
    out = []
    for index, opening in enumerate(openings):
        opening_id = opening.get("opening_id")
        stable_opening_id = opening_id if _valid_evidence_id(opening_id) else f"UNKNOWN-{index}"
        point = opening.get("point")
        span = opening.get("span")
        touched = []
        for space in spaces:
            pts = boundary_points.get(space["boundary_handle"], [])
            if not pts:
                continue
            if span and _span_touches_boundary(span, pts, tolerance):
                touched.append(space)
            elif not span and point and min(
                _distance_to_segment(point, a, b) for a, b in _segments(pts)
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
