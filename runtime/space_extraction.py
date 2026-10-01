"""Conservative space extraction from native architectural linework."""
from __future__ import annotations
import math


def _near(a, b, tolerance):
    return abs(a[0]-b[0]) <= tolerance and abs(a[1]-b[1]) <= tolerance


def _intersection(a, b, tolerance=1e-6):
    ax, ay, bx, by = a; cx, cy, dx, dy = b
    ah = abs(ay-by) <= tolerance; av = abs(ax-bx) <= tolerance
    bh = abs(cy-dy) <= tolerance; bv = abs(cx-dx) <= tolerance
    if ah == bh or av == bv: return None
    if ah and bv:
        p=(cx,ay)
        if min(ax,bx)-tolerance <= p[0] <= max(ax,bx)+tolerance and min(cy,dy)-tolerance <= p[1] <= max(cy,dy)+tolerance: return p
    if av and bh:
        p=(ax,cy)
        if min(cx,dx)-tolerance <= p[0] <= max(cx,dx)+tolerance and min(ay,by)-tolerance <= p[1] <= max(ay,by)+tolerance: return p
    return None


def _signed_area(points):
    return sum(points[i][0]*points[(i+1)%len(points)][1]-points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points)))/2.0


def polygonize_orthogonal_lines(line_segments, tolerance=1e-6, max_spaces=128):
    """Extract bounded planar faces from clean axis-aligned native linework."""
    raw=[]
    for item in line_segments:
        if len(item)<4: continue
        a=(float(item[0]),float(item[1])); b=(float(item[2]),float(item[3]))
        if not _near(a,b,tolerance) and (abs(a[1]-b[1])<=tolerance or abs(a[0]-b[0])<=tolerance):
            raw.append((a,b,str(item[4]) if len(item)>4 else ""))
    if not raw: return []

    points=[p for a,b,_ in raw for p in (a,b)]
    for i,(a,b,_) in enumerate(raw):
        for c,d,_ in raw[i+1:]:
            p=_intersection((a[0],a[1],b[0],b[1]),(c[0],c[1],d[0],d[1]),tolerance)
            if p is not None: points.append(p)
    unique=[]
    for p in points:
        if not any(_near(p,q,tolerance) for q in unique): unique.append(p)
    def idx(p):
        return min(range(len(unique)), key=lambda i:(unique[i][0]-p[0])**2+(unique[i][1]-p[1])**2)

    edges=set()
    for a,b,_ in raw:
        horizontal=abs(a[1]-b[1])<=tolerance
        pts=[]
        for p in unique:
            on=(abs(p[1]-a[1])<=tolerance and min(a[0],b[0])-tolerance<=p[0]<=max(a[0],b[0])+tolerance) if horizontal else (abs(p[0]-a[0])<=tolerance and min(a[1],b[1])-tolerance<=p[1]<=max(a[1],b[1])+tolerance)
            if on: pts.append(p)
        pts.sort(key=lambda p:(p[0],p[1]) if horizontal else (p[1],p[0]))
        for p,q in zip(pts,pts[1:]):
            u,v=idx(p),idx(q)
            if u!=v: edges.add((min(u,v),max(u,v)))

    outgoing={i:[] for i in range(len(unique))}
    for u,v in edges:
        outgoing[u].append(v); outgoing[v].append(u)
    for u in outgoing:
        outgoing[u].sort(key=lambda v:math.atan2(unique[v][1]-unique[u][1],unique[v][0]-unique[u][0]))

    # Traverse each directed half-edge with the face on its left.
    next_edge={}
    for u,v in ((u,v) for e in edges for u,v in (e,(e[1],e[0]))):
        nbrs=outgoing[v]
        if not nbrs: continue
        try: pos=nbrs.index(u)
        except ValueError: continue
        w=nbrs[(pos-1)%len(nbrs)]  # predecessor in CCW order => left-face walk
        next_edge[(u,v)]=(v,w)

    visited=set(); faces=[]
    for start in sorted(next_edge):
        if start in visited: continue
        cycle=[]; cur=start; local=set()
        for _ in range(len(next_edge)+1):
            if cur in local: break
            if cur not in next_edge: break
            local.add(cur); visited.add(cur); cycle.append(cur[0]); cur=next_edge[cur]
            if cur==start:
                pts=[unique[i] for i in cycle]
                if len(pts)>=3:
                    area=_signed_area(pts)
                    if area>tolerance: faces.append((pts,area))
                break

    selected=[]; seen=set()
    for pts,area in sorted(faces,key=lambda x:x[1]):
        sig=tuple(sorted((round(x,6),round(y,6)) for x,y in pts))
        if sig in seen: continue
        seen.add(sig); selected.append((pts,area))
        if len(selected)>=max_spaces: break
    return selected
