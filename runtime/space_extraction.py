"""Conservative space extraction from native architectural linework."""
from __future__ import annotations
import math


def _near(a, b, tolerance):
    return abs(a[0] - b[0]) <= tolerance and abs(a[1] - b[1]) <= tolerance


def _intersection(a, b, tolerance=1e-6):
    ax, ay, bx, by = a
    cx, cy, dx, dy = b
    ah, av = abs(ay-by) <= tolerance, abs(ax-bx) <= tolerance
    bh, bv = abs(cy-dy) <= tolerance, abs(cx-dx) <= tolerance
    if ah == bh or av == bv:
        return None
    if ah and bv:
        p=(cx,ay)
        if min(ax,bx)-tolerance <= p[0] <= max(ax,bx)+tolerance and min(cy,dy)-tolerance <= p[1] <= max(cy,dy)+tolerance: return p
    if av and bh:
        p=(ax,cy)
        if min(cx,dx)-tolerance <= p[0] <= max(cx,dx)+tolerance and min(ay,by)-tolerance <= p[1] <= max(ay,by)+tolerance: return p
    return None


def _signed_area(points):
    return sum(points[i][0]*points[(i+1)%len(points)][1] - points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points)))/2.0


def polygonize_orthogonal_lines(line_segments, tolerance=1e-6, max_spaces=128):
    """Extract bounded faces from a clean axis-aligned line network."""
    raw=[]
    for item in line_segments:
        if len(item)<4: continue
        a=(float(item[0]),float(item[1])); b=(float(item[2]),float(item[3]))
        if ((abs(a[1]-b[1])<=tolerance) or (abs(a[0]-b[0])<=tolerance)) and not _near(a,b,tolerance):
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
        return min(range(len(unique)),key=lambda i:(unique[i][0]-p[0])**2+(unique[i][1]-p[1])**2)
    edge_pairs=set()
    for a,b,_ in raw:
        horizontal=abs(a[1]-b[1])<=tolerance
        pts=[]
        for p in unique:
            if horizontal:
                ok=abs(p[1]-a[1])<=tolerance and min(a[0],b[0])-tolerance<=p[0]<=max(a[0],b[0])+tolerance
            else:
                ok=abs(p[0]-a[0])<=tolerance and min(a[1],b[1])-tolerance<=p[1]<=max(a[1],b[1])+tolerance
            if ok: pts.append(p)
        pts.sort(key=lambda p:(p[0],p[1]) if horizontal else (p[1],p[0]))
        for u,v in zip(pts,pts[1:]):
            iu,iv=idx(u),idx(v)
            if iu!=iv: edge_pairs.add(tuple(sorted((iu,iv))))
    adjacency={i:set() for i in range(len(unique))}
    for u,v in edge_pairs: adjacency[u].add(v); adjacency[v].add(u)

    directed={(u,v) for u,v in edge_pairs for u,v in ((u,v),(v,u))}
    faces=[]
    max_steps=max(8,len(directed)+2)
    while directed:
        start=min(directed); u,v=start; cycle=[]
        for _ in range(max_steps):
            if (u,v) not in directed: break
            directed.remove((u,v)); cycle.append(u)
            rev=math.atan2(unique[u][1]-unique[v][1],unique[u][0]-unique[v][0])
            options=[]
            for n in adjacency[v]:
                candidate=(v,n)
                if candidate in directed or candidate == start:
                    ang=math.atan2(unique[n][1]-unique[v][1],unique[n][0]-unique[v][0])
                    options.append(((rev-ang)%(2*math.pi),n,candidate==start))
            if not options: break
            _,nxt,is_start=min(options)
            if is_start:
                pts=[unique[i] for i in cycle]
                if len(pts)>=3:
                    area=_signed_area(pts)
                    if area>tolerance: faces.append((pts,area))
                break
            u,v=v,nxt
    selected=[]; seen=set()
    for pts,area in sorted(faces,key=lambda x:x[1]):
        sig=tuple(sorted((round(x,6),round(y,6)) for x,y in pts))
        if sig in seen: continue
        seen.add(sig); selected.append((pts,area))
        if len(selected)>=max_spaces: break
    return selected
