"""Evidence-backed opening-to-space connectivity helpers.

The module stays fail-closed: insertion-point proximity is only a candidate
signal. Approval-grade connectivity requires a native opening span and host
wall evidence that touches two space boundaries.
"""
from __future__ import annotations
from math import hypot


def _segments(points):
    pts=[(float(p[0]),float(p[1])) for p in points]
    return list(zip(pts,pts[1:]+pts[:1])) if len(pts)>=3 else []


def _distance_to_segment(p,a,b):
    vx,vy=b[0]-a[0],b[1]-a[1]
    wx,wy=p[0]-a[0],p[1]-a[1]
    den=vx*vx+vy*vy
    if den==0: return hypot(p[0]-a[0],p[1]-a[1])
    t=max(0,min(1,(wx*vx+wy*vy)/den))
    q=(a[0]+t*vx,a[1]+t*vy)
    return hypot(p[0]-q[0],p[1]-q[1])


def _span_touches_boundary(span, points, tolerance):
    if not span or len(span) < 2 or not points:
        return False
    a,b=span[0],span[1]
    # Endpoint proximity is deliberately conservative and avoids treating a
    # nearby insertion point as an architectural opening by itself.
    return (
        min(_distance_to_segment(a,c,d) for c,d in _segments(points)) <= tolerance
        and min(_distance_to_segment(b,c,d) for c,d in _segments(points)) <= tolerance
    )


def classify_opening_connectivity(
    openings, spaces, boundary_points, tolerance=1.0, host_wall_ids=None
):
    """Classify opening connectivity using native span + two-boundary evidence.

    Returns CONNECTED_BY_OPENING only when the opening span has evidence touching
    exactly two space boundaries. All results remain UNKNOWN until downstream
    validation approves the semantics.
    """
    host_wall_ids = set(host_wall_ids or ())
    out=[]
    for opening in openings:
        point=opening.get("point")
        span=opening.get("span")
        touched=[]
        for space in spaces:
            pts=boundary_points.get(space["boundary_handle"],[])
            if not pts:
                continue
            if span and _span_touches_boundary(span, pts, tolerance):
                touched.append(space)
            elif not span and point and min(
                _distance_to_segment(point,a,b) for a,b in _segments(pts)
            ) <= tolerance:
                touched.append(space)

        # A host wall reference is useful corroboration, but never creates a
        # connection by itself. Unknown/missing host evidence remains unresolved.
        host_wall_evidenced = bool(opening.get("host_wall_id") and (
            not host_wall_ids or opening.get("host_wall_id") in host_wall_ids
        ))

        if len(touched)==2 and span and host_wall_evidenced:
            a,b=touched
            out.append({
                "relation_id":f"{a['space_id']}__{b['space_id']}__OPENING-{opening['opening_id']}",
                "from":a["space_id"],"to":b["space_id"],"type":"CONNECTED_BY_OPENING",
                "opening_id":opening["opening_id"],
                "evidence_ids":a["evidence_ids"]+b["evidence_ids"]+
                    [opening["evidence_id"], opening["span_evidence_id"], opening["host_wall_evidence_id"]],
                "status":"UNKNOWN",
            })
        else:
            out.append({
                "relation_id":f"OPENING-{opening['opening_id']}__UNRESOLVED",
                "from":None,"to":None,"type":"OPENING_CONNECTIVITY_UNKNOWN",
                "opening_id":opening["opening_id"],
                "evidence_ids":[opening["evidence_id"]] +
                    ([opening["span_evidence_id"]] if opening.get("span_evidence_id") else []) +
                    ([opening["host_wall_evidence_id"]] if opening.get("host_wall_evidence_id") else []),
                "status":"UNKNOWN",
                "touched_space_count":len(touched),
                "host_wall_evidenced":host_wall_evidenced,
            })
    return out
