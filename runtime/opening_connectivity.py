"""Evidence-backed opening-to-space connectivity helpers."""
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


def classify_opening_connectivity(openings, spaces, boundary_points, tolerance=1.0):
    """Connect an opening only when its native insertion point lies on two space boundaries."""
    out=[]
    for opening in openings:
        point=opening.get("point")
        if not point: continue
        touching=[]
        for space in spaces:
            pts=boundary_points.get(space["boundary_handle"],[])
            if pts and min(_distance_to_segment(point,a,b) for a,b in _segments(pts))<=tolerance:
                touching.append(space)
        if len(touching)==2:
            a,b=touching
            out.append({"relation_id":f"{a['space_id']}__{b['space_id']}__OPENING-{opening['opening_id']}","from":a["space_id"],"to":b["space_id"],"type":"CONNECTED_BY_OPENING","opening_id":opening["opening_id"],"evidence_ids":a["evidence_ids"]+b["evidence_ids"]+[opening["evidence_id"]],"status":"UNKNOWN"})
        else:
            out.append({"relation_id":f"OPENING-{opening['opening_id']}__UNRESOLVED","from":None,"to":None,"type":"OPENING_CONNECTIVITY_UNKNOWN","opening_id":opening["opening_id"],"evidence_ids":[opening["evidence_id"]],"status":"UNKNOWN"})
    return out
