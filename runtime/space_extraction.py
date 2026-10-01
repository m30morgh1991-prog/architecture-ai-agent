"""Conservative space extraction from native architectural linework.

Closed polylines are preferred. When rooms are represented by separate wall
LINE entities, this module polygonizes only a clean orthogonal line network.
It never labels a polygon as a named room without explicit text evidence.
"""
from __future__ import annotations
from typing import Any

def _near(a,b,t): return abs(a[0]-b[0])<=t and abs(a[1]-b[1])<=t

def _intersections(a,b,tol=1e-6):
    ax,ay,bx,by=a; cx,cy,dx,dy=b
    out=[]
    if abs(ay-by)<=tol and abs(cy-dy)<=tol: return out
    if abs(ax-bx)<=tol and abs(cx-dx)<=tol: return out
    if abs(ay-by)<=tol and abs(cx-dx)<=tol:
        x=cx; y=ay
        if min(ax,bx)-tol<=x<=max(ax,bx)+tol and min(cy,dy)-tol<=y<=max(cy,dy)+tol: out.append((x,y))
    elif abs(ax-bx)<=tol and abs(cy-dy)<=tol:
        x=ax; y=cy
        if min(cx,dx)-tol<=x<=max(cx,dx)+tol and min(ay,by)-tol<=y<=max(ay,by)+tol: out.append((x,y))
    return out

def polygonize_orthogonal_lines(line_segments,tolerance=1e-6,max_spaces=128):
    """Return bounded face candidates from a clean axis-aligned line network."""
    raw=[]
    for item in line_segments:
        if len(item)<4: continue
        a=(float(item[0]),float(item[1])); b=(float(item[2]),float(item[3]))
        if abs(a[0]-b[0])<=tolerance or abs(a[1]-b[1])<=tolerance:
            if not _near(a,b,tolerance): raw.append((a,b,str(item[4]) if len(item)>4 else ""))
    if not raw: return []
    points=[]
    for a,b,h in raw:
        points.extend([a,b])
    for i,(a,b,_) in enumerate(raw):
        for c,d,_ in raw[i+1:]: points.extend(_intersections((a[0],a[1],b[0],b[1]),(c[0],c[1],d[0],d[1]),tolerance))
    uniq=[]
    for p in points:
        if not any(_near(p,q,tolerance) for q in uniq): uniq.append(p)
    def key(p): return min(range(len(uniq)),key=lambda i:((uniq[i][0]-p[0])**2+(uniq[i][1]-p[1])**2))
    edges=set()
    for a,b,h in raw:
        pts=[p for p in uniq if ((abs(a[0]-b[0])<=tolerance and abs(p[0]-a[0])<=tolerance and min(a[1],b[1])-tolerance<=p[1]<=max(a[1],b[1])+tolerance) or
                                 (abs(a[1]-b[1])<=tolerance and abs(p[1]-a[1])<=tolerance and min(a[0],b[0])-tolerance<=p[0]<=max(a[0],b[0])+tolerance))]
        pts.sort(key=lambda p:(p[0],p[1]))
        if abs(a[0]-b[0])<=tolerance: pts.sort(key=lambda p:p[1])
        else: pts.sort(key=lambda p:p[0])
        for u,v in zip(pts,pts[1:]):
            ku,kv=key(u),key(v)
            if ku!=kv: edges.add((ku,kv,h))
    adj={i:set() for i in range(len(uniq))}
    for u,v,_ in edges: adj[u].add(v); adj[v].add(u)
    # Trace directed faces by taking the smallest clockwise turn at each node.
    directed=set((u,v) for u,v,_ in edges)|set((v,u) for u,v,_ in edges)
    faces=[]
    while directed:
        start=min(directed); directed.remove(start)
        u,v=start; cycle=[u]; prev=u; cur=v
        for _ in range(len(uniq)+2):
            cycle.append(cur)
            candidates=[n for n in adj[cur] if (cur,n) in directed or n==start]
            if cur==start: break
            incoming=(uniq[prev][0]-uniq[cur][0],uniq[prev][1]-uniq[cur][1])
            def angle(n):
                vec=(uniq[n][0]-uniq[cur][0],uniq[n][1]-uniq[cur][1])
                import math
                return (math.atan2(incoming[1],incoming[0])-math.atan2(vec[1],vec[0]))%(2*math.pi)
            nxt=min(candidates,key=angle,default=None)
            if nxt is None: break
            if (cur,nxt) in directed: directed.remove((cur,nxt))
            prev,cur=cur,nxt
            if cur==start: break
        if len(cycle)>=4 and cycle[-1]==start:
            pts=[uniq[i] for i in cycle[:-1]]
            area=abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))/2)
            if area>tolerance:
                faces.append((pts,area))
    # Each bounded face is duplicated against the exterior orientation in many
    # planar traces; retain only faces whose centroid is not the global exterior.
    if not faces: return []
    max_area=max(a for _,a in faces)
    selected=[]
    seen=set()
    for pts,area in sorted(faces,key=lambda x:x[1]):
        sig=tuple(sorted((round(x,6),round(y,6)) for x,y in pts))
        if sig in seen or area>=max_area and len(faces)>1: continue
        seen.add(sig); selected.append((pts,area))
        if len(selected)>=max_spaces: break
    return selected
