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
    """Extract bounded planar faces from clean axis-aligned native linework.

    The implementation keeps the same evidence semantics as the original
    polygonizer, but avoids the quadratic all-segment intersection scan and
    the repeated global point-on-segment scan. Intersections are only possible
    between horizontal and vertical segments, and split points are retained
    per source segment as they are discovered.
    """
    raw = []
    for item in line_segments:
        if len(item) < 4:
            continue
        a = (float(item[0]), float(item[1]))
        b = (float(item[2]), float(item[3]))
        if _near(a, b, tolerance):
            continue
        horizontal = abs(a[1] - b[1]) <= tolerance
        vertical = abs(a[0] - b[0]) <= tolerance
        if not (horizontal or vertical):
            continue
        raw.append((a, b, str(item[4]) if len(item) > 4 else ""))

    if not raw:
        return []

    horizontals = []
    verticals = []
    split_points = [[raw[i][0], raw[i][1]] for i in range(len(raw))]

    for index, (a, b, _) in enumerate(raw):
        if abs(a[1] - b[1]) <= tolerance:
            x0, x1 = sorted((a[0], b[0]))
            horizontals.append((index, x0, x1, (a[1] + b[1]) / 2.0))
        else:
            y0, y1 = sorted((a[1], b[1]))
            verticals.append((index, y0, y1, (a[0] + b[0]) / 2.0))

    # Orthogonal intersections are the only intersections relevant here.
    # Keep them attached to both source segments so later edge construction
    # does not need to scan every global point against every segment.
    for hi, hx0, hx1, hy in horizontals:
        for vi, vy0, vy1, vx in verticals:
            if hx0 - tolerance <= vx <= hx1 + tolerance and vy0 - tolerance <= hy <= vy1 + tolerance:
                p = (vx, hy)
                split_points[hi].append(p)
                split_points[vi].append(p)

    # Deduplicate split points locally. This preserves the previous geometric
    # tolerance while making the cost proportional to each segment's crossings.
    def unique_points(points):
        ordered = sorted(
            points,
            key=lambda p: (round(p[0] / max(tolerance, 1e-12)),
                           round(p[1] / max(tolerance, 1e-12)))
        )
        unique = []
        for point in ordered:
            if not unique or not _near(point, unique[-1], tolerance):
                unique.append(point)
        return unique

    unique = []
    point_ids = {}

    def point_id(point):
        key = (
            round(point[0] / max(tolerance, 1e-12)),
            round(point[1] / max(tolerance, 1e-12)),
        )
        existing = point_ids.get(key)
        if existing is not None:
            candidate = unique[existing]
            if _near(point, candidate, tolerance):
                return existing
        index = len(unique)
        unique.append(point)
        point_ids[key] = index
        return index

    edges = set()
    for index, (a, b, _) in enumerate(raw):
        points = unique_points(split_points[index])
        horizontal = abs(a[1] - b[1]) <= tolerance
        points.sort(
            key=lambda p: (p[0], p[1]) if horizontal else (p[1], p[0])
        )
        for p, q in zip(points, points[1:]):
            u, v = point_id(p), point_id(q)
            if u != v:
                edges.add((min(u, v), max(u, v)))

    outgoing = {i: [] for i in range(len(unique))}
    for u, v in edges:
        outgoing[u].append(v)
        outgoing[v].append(u)
    for u in outgoing:
        outgoing[u].sort(
            key=lambda v: math.atan2(
                unique[v][1] - unique[u][1],
                unique[v][0] - unique[u][0],
            )
        )

    next_edge = {}
    for edge in edges:
        for u, v in (edge, (edge[1], edge[0])):
            nbrs = outgoing[v]
            if not nbrs:
                continue
            try:
                pos = nbrs.index(u)
            except ValueError:
                continue
            w = nbrs[(pos - 1) % len(nbrs)]
            next_edge[(u, v)] = (v, w)

    visited = set()
    faces = []
    for start in sorted(next_edge):
        if start in visited:
            continue
        cycle = []
        cur = start
        local = set()
        for _ in range(len(next_edge) + 1):
            if cur in local or cur not in next_edge:
                break
            local.add(cur)
            visited.add(cur)
            cycle.append(cur[0])
            cur = next_edge[cur]
            if cur == start:
                pts = [unique[i] for i in cycle]
                if len(pts) >= 3:
                    area = _signed_area(pts)
                    if area > tolerance:
                        faces.append((pts, area))
                break

    selected = []
    seen = set()
    for pts, area in sorted(faces, key=lambda x: x[1]):
        sig = tuple(sorted((round(x, 6), round(y, 6)) for x, y in pts))
        if sig in seen:
            continue
        seen.add(sig)
        selected.append((pts, area))
        if len(selected) >= max_spaces:
            break
    return selected
def merge_space_boundaries(explicit_shapes, line_faces, tolerance=1e-6, max_spaces=128):
    """Merge explicit closed boundaries with derived line faces without duplicate rooms.

    Explicit native closed polylines are preferred when they describe the same
    boundary as a derived face. Line-derived faces are still retained when they
    represent additional enclosed regions. No semantic status is inferred.
    """
    merged = []
    signatures = set()

    def signature(points):
        return tuple(sorted((round(float(x), 6), round(float(y), 6)) for x, y in points))

    for handle, points in list(explicit_shapes)[:max_spaces]:
        if len(points) < 3:
            continue
        area = abs(_signed_area(points))
        if area <= 1.0:
            continue
        sig = signature(points)
        if sig in signatures:
            continue
        signatures.add(sig)
        merged.append((handle, points, "EXPLICIT_CLOSED_BOUNDARY"))

    for index, item in enumerate(list(line_faces)[:max_spaces], 1):
        points, area = item
        if len(points) < 3 or area <= 1.0:
            continue
        sig = signature(points)
        if sig in signatures:
            continue
        # Guard against a line-derived face that is merely the same room with
        # tiny coordinate noise: compare centroid and area ratio.
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
        duplicate = False
        for _, existing, _ in merged:
            ex_area = abs(_signed_area(existing))
            ex_cx = sum(p[0] for p in existing) / len(existing)
            ex_cy = sum(p[1] for p in existing) / len(existing)
            area_ratio = min(area, ex_area) / max(area, ex_area)
            if area_ratio >= 0.995 and ((cx-ex_cx)**2 + (cy-ex_cy)**2) ** 0.5 <= tolerance * 10:
                duplicate = True
                break
        if not duplicate:
            merged.append((f"line-face-{index:03d}", points, "DERIVED_LINE_FACE"))
    return merged
