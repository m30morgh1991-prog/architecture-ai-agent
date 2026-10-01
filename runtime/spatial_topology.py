"""Conservative spatial topology utilities for native architectural plan geometry."""
from __future__ import annotations

from math import hypot


def _segments(points):
    pts=[(float(p[0]),float(p[1])) for p in points]
    return list(zip(pts, pts[1:]+pts[:1])) if len(pts)>=3 else []


def _cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def _point_on_segment(p,a,b,tol):
    if abs(_cross(a,b,p))>tol: return False
    return min(a[0],b[0])-tol<=p[0]<=max(a[0],b[0])+tol and min(a[1],b[1])-tol<=p[1]<=max(a[1],b[1])+tol


def _shared_boundary_length(pa,pb,tol):
    total=0.0
    for a,b in _segments(pa):
        for c,d in _segments(pb):
            if abs(_cross(a,b,c))<=tol and abs(_cross(a,b,d))<=tol:
                ux,uy=b[0]-a[0],b[1]-a[1]
                den=hypot(ux,uy)
                if den<=tol: continue
                proj=lambda p: ((p[0]-a[0])*ux+(p[1]-a[1])*uy)/den
                lo=max(min(proj(a),proj(b)),min(proj(c),proj(d)))
                hi=min(max(proj(a),proj(b)),max(proj(c),proj(d)))
                if hi-lo>tol: total+=hi-lo
    return total


def _bbox(space): return tuple(space["bbox"])


def _bbox_overlap(a,b,tol):
    ax0,ay0,ax1,ay1=_bbox(a); bx0,by0,bx1,by1=_bbox(b)
    return min(ax1,bx1)-max(ax0,bx0)>tol and min(ay1,by1)-max(ay0,by0)>tol


def _point_in_polygon(p,points):
    inside=False
    for a,b in _segments(points):
        if _point_on_segment(p,a,b,1e-8): return True
        if (a[1]>p[1]) != (b[1]>p[1]):
            x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if x>p[0]: inside=not inside
    return inside


def classify_space_relations(spaces, boundary_points, tolerance=1e-6):
    """Return evidence-backed relations; never infer adjacency from bbox overlap alone."""
    out=[]
    for i,a in enumerate(spaces):
        for b in spaces[i+1:]:
            pa=boundary_points.get(a["boundary_handle"],[]); pb=boundary_points.get(b["boundary_handle"],[])
            if not pa or not pb: continue
            shared=_shared_boundary_length(pa,pb,tolerance)
            if shared>tolerance:
                relation="SHARED_BOUNDARY"
            elif _point_in_polygon(tuple(a["centroid"]),pb):
                relation="CONTAINS"
            elif _point_in_polygon(tuple(b["centroid"]),pa):
                relation="CONTAINS"
            elif _bbox_overlap(a,b,tolerance):
                relation="OVERLAPS"
            else:
                relation="DISCONNECTED"
            out.append({
                "relation_id":f"{a['space_id']}__{b['space_id']}__{relation}",
                "from":a["space_id"],"to":b["space_id"],"type":relation,
                "evidence_ids":a["evidence_ids"]+b["evidence_ids"],
                "geometry_reference":{"from_boundary":a["boundary_handle"],"to_boundary":b["boundary_handle"],"shared_boundary_length":round(shared,6)},
                "status":"UNKNOWN",
            })
    return out
