"""Conservative space extraction from native architectural linework.

Closed polylines are preferred by the caller. This module handles the common
case where room boundaries are represented by separate orthogonal LINE
entities. It returns geometric face candidates only; it never invents room
names or semantic approval.
"""
from __future__ import annotations
import math


def _near(a, b, tolerance):
    return abs(a[0] - b[0]) <= tolerance and abs(a[1] - b[1]) <= tolerance


def _intersection(a, b, tolerance=1e-6):
    ax, ay, bx, by = a
    cx, cy, dx, dy = b
    ah = abs(ay - by) <= tolerance
    av = abs(ax - bx) <= tolerance
    bh = abs(cy - dy) <= tolerance
    bv = abs(cx - dx) <= tolerance
    if ah == bh or av == bv:
        return None
    if ah and bv:
        p = (cx, ay)
        if min(ax, bx) - tolerance <= p[0] <= max(ax, bx) + tolerance and min(cy, dy) - tolerance <= p[1] <= max(cy, dy) + tolerance:
            return p
    if av and bh:
        p = (ax, cy)
        if min(cx, dx) - tolerance <= p[0] <= max(cx, dx) + tolerance and min(ay, by) - tolerance <= p[1] <= max(ay, by) + tolerance:
            return p
    return None


def _signed_area(points):
    return sum(
        points[i][0] * points[(i + 1) % len(points)][1]
        - points[(i + 1) % len(points)][0] * points[i][1]
        for i in range(len(points))
    ) / 2.0


def polygonize_orthogonal_lines(line_segments, tolerance=1e-6, max_spaces=128):
    """Extract bounded faces from a clean axis-aligned line network."""
    raw = []
    for item in line_segments:
        if len(item) < 4:
            continue
        a = (float(item[0]), float(item[1]))
        b = (float(item[2]), float(item[3]))
        horizontal = abs(a[1] - b[1]) <= tolerance
        vertical = abs(a[0] - b[0]) <= tolerance
        if (horizontal or vertical) and not _near(a, b, tolerance):
            raw.append((a, b, str(item[4]) if len(item) > 4 else ""))

    if not raw:
        return []

    points = [p for a, b, _ in raw for p in (a, b)]
    for i, (a, b, _) in enumerate(raw):
        seg_a = (a[0], a[1], b[0], b[1])
        for c, d, _ in raw[i + 1:]:
            p = _intersection(seg_a, (c[0], c[1], d[0], d[1]), tolerance)
            if p is not None:
                points.append(p)

    unique = []
    for p in points:
        if not any(_near(p, q, tolerance) for q in unique):
            unique.append(p)

    def point_index(p):
        return min(
            range(len(unique)),
            key=lambda i: (unique[i][0] - p[0]) ** 2 + (unique[i][1] - p[1]) ** 2,
        )

    edges = set()
    for a, b, evidence in raw:
        horizontal = abs(a[1] - b[1]) <= tolerance
        on_segment = []
        for p in unique:
            if horizontal:
                ok = abs(p[1] - a[1]) <= tolerance and min(a[0], b[0]) - tolerance <= p[0] <= max(a[0], b[0]) + tolerance
            else:
                ok = abs(p[0] - a[0]) <= tolerance and min(a[1], b[1]) - tolerance <= p[1] <= max(a[1], b[1]) + tolerance
            if ok:
                on_segment.append(p)
        on_segment.sort(key=lambda p: (p[0], p[1]) if horizontal else (p[1], p[0]))
        for u, v in zip(on_segment, on_segment[1:]):
            iu, iv = point_index(u), point_index(v)
            if iu != iv:
                edges.add((iu, iv, evidence))

    adjacency = {i: set() for i in range(len(unique))}
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    directed = {(u, v) for u, v, _ in edges} | {(v, u) for u, v, _ in edges}
    faces = []
    max_steps = max(8, len(directed) + 2)

    while directed:
        start_u, start_v = min(directed)
        directed.remove((start_u, start_v))
        prev, cur = start_u, start_v
        cycle = [prev]

        for _ in range(max_steps):
            cycle.append(cur)
            incoming_angle = math.atan2(unique[prev][1] - unique[cur][1], unique[prev][0] - unique[cur][0])
            candidates = [n for n in adjacency[cur] if (cur, n) in directed or n == start_u]
            if not candidates:
                break

            def clockwise_delta(n):
                outgoing_angle = math.atan2(unique[n][1] - unique[cur][1], unique[n][0] - unique[cur][0])
                return (incoming_angle - outgoing_angle) % (2 * math.pi)

            nxt = min(candidates, key=clockwise_delta)
            if (cur, nxt) in directed:
                directed.remove((cur, nxt))
            prev, cur = cur, nxt
            if cur == start_u:
                break

        if cur != start_u or len(cycle) < 4:
            continue

        pts = [unique[i] for i in cycle[:-1]]
        signed = _signed_area(pts)
        if signed > tolerance:
            faces.append((pts, signed))

    selected = []
    seen = set()
    for pts, area in sorted(faces, key=lambda x: x[1]):
        signature = tuple(sorted((round(x, 6), round(y, 6)) for x, y in pts))
        if signature in seen:
            continue
        seen.add(signature)
        selected.append((pts, area))
        if len(selected) >= max_spaces:
            break
    return selected
