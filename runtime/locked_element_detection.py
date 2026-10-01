"""Conservative fixed-element candidate detection for real architectural artifacts.

This module detects evidence-backed *candidates* but never promotes uncertain
visual candidates to LOCKED. Approval-grade locking remains fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import cv2
import fitz
import numpy as np

try:
    import ezdwg
except ImportError:  # pragma: no cover
    ezdwg = None


_PLAN_TITLE_RE = re.compile(r"\bPLANTA\s+([^\n]+)", re.I)
_FIXED_TYPES = (
    "COLUMNS",
    "OUTER_BOUNDARY",
    "WALLS",
    "DOORS",
    "WINDOWS",
    "OVERALL_PLAN_FORM",
)


@dataclass(frozen=True)
class LockedElementCandidate:
    candidate_id: str
    element_type: str
    bbox: tuple[float, float, float, float]
    confidence: float
    evidence_ids: tuple[str, ...]
    status: str
    rationale: str

    def validate(self) -> None:
        if not self.candidate_id or self.element_type not in _FIXED_TYPES:
            raise ValueError("INVALID_LOCKED_ELEMENT_CANDIDATE")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("INVALID_CANDIDATE_CONFIDENCE")
        if not self.evidence_ids:
            raise ValueError("MISSING_CANDIDATE_EVIDENCE")
        if self.status == "LOCKED" and self.confidence < 0.95:
            raise ValueError("LOCKED_CANDIDATE_CONFIDENCE_TOO_LOW")


class ConservativeLockedElementDetector:
    """Extract plan-level vector evidence and structural candidates without guessing."""

    detector_id = "conservative-vector-fixed-v0.2"

    def detect(self, source_path: str, source_sha256: str) -> dict[str, Any]:
        path = Path(source_path)
        if path.suffix.lower() == ".dwg":
            return self._dwg_detect(path, source_sha256)
        if path.suffix.lower() != ".pdf":
            return self._raster_fallback(source_sha256)

        document = fitz.open(path)
        if document.page_count == 0:
            return {
                "status": "UNKNOWN",
                "reason": "SOURCE_DOCUMENT_EMPTY",
                "plan_panels": [],
                "candidates": [],
            }

        page = document[0]
        blocks = page.get_text("blocks")
        titles = []
        for block_index, block in enumerate(blocks):
            text = block[4].strip()
            matches = list(_PLAN_TITLE_RE.finditer(text))
            for match_index, match in enumerate(matches):
                title = f"PLANTA {match.group(1).strip()}"
                titles.append({
                    "index": len(titles) + 1,
                    "title": title,
                    "bbox": [float(block[0]), float(block[1]), float(block[2]), float(block[3])],
                    "evidence_id": f"pdf-text-block-{block_index}-{match_index}",
                })

        drawings = page.get_drawings()
        vertical_lines = []
        filled_rects = []
        horizontal_lines = []
        for drawing_index, drawing in enumerate(drawings):
            rect = drawing.get("rect")
            fill = drawing.get("fill")
            if rect is not None and fill is not None:
                w, h = float(rect.width), float(rect.height)
                if 20 <= w <= 80 and 20 <= h <= 80:
                    filled_rects.append((drawing_index, rect))

            for item in drawing.get("items", []):
                if not item:
                    continue
                kind = item[0]
                if kind in {"l", "line"}:
                    p1, p2 = item[1], item[2]
                    dx, dy = float(p2.x - p1.x), float(p2.y - p1.y)
                    length = (dx * dx + dy * dy) ** 0.5
                    if length >= 500 and abs(dx) < 2:
                        vertical_lines.append(
                            (float((p1.x + p2.x) / 2), float(min(p1.y, p2.y)),
                             float(max(p1.y, p2.y)), length)
                        )
                    if length >= 500 and abs(dy) < 2:
                        horizontal_lines.append(
                            (float(min(p1.x, p2.x)), float((p1.y + p2.y) / 2),
                             float(max(p1.x, p2.x)), length)
                        )
                elif kind in {"re", "rect", "rectangle"} and len(item) >= 2:
                    item_rect = item[1]
                    w, h = float(item_rect.width), float(item_rect.height)
                    if 20 <= w <= 80 and 20 <= h <= 80:
                        filled_rects.append((drawing_index, item_rect))

        # Build a vector frame even if text extraction does not expose the
        # plan title. This keeps detection evidence-driven and conservative:
        # geometry can establish a candidate panel, but never approval-grade
        # semantics or LOCKED state.
        if not titles and len(vertical_lines) >= 2:
            left = min(vertical_lines, key=lambda line: line[0])
            right = max(vertical_lines, key=lambda line: line[0])
            if left[0] < right[0] and left[1] < 500 and right[1] < 500:
                titles.append({
                    "index": 1,
                    "title": "PLANTA VECTOR PANEL",
                    "bbox": [left[0], left[1], right[0], min(left[2], right[2])],
                    "evidence_id": "pdf-vector-frame-0",
                })

        panels = []
        candidates = []
        for panel in titles:
            cx = (panel["bbox"][0] + panel["bbox"][2]) / 2.0
            # The plan frame in a PDF may start below the title block.
            # Do not assume its top/bottom coordinates relative to the title;
            # use the actual long-vector evidence and let the frame geometry
            # establish the panel bounds.
            left = [
                line for line in vertical_lines
                if line[0] < cx and (line[2] - line[1]) >= 500
            ]
            right = [
                line for line in vertical_lines
                if line[0] > cx and (line[2] - line[1]) >= 500
            ]
            left_line = min(left, key=lambda line: abs(line[0] - cx), default=None)
            right_line = min(right, key=lambda line: abs(line[0] - cx), default=None)
            if left_line and right_line:
                x0 = left_line[0]
                x1 = right_line[0]
                y0 = min(left_line[1], right_line[1])
                y1 = max(left_line[2], right_line[2])
            else:
                x0 = max(0.0, cx - 330.0)
                x1 = min(float(page.rect.width), cx + 330.0)
                y0 = 450.0
                y1 = panel["bbox"][1] - 25.0
            evidence = [panel["evidence_id"], f"vector-frame-{panel['index']}"]
            panel_lines = sum(
                1 for line in vertical_lines
                if x0 <= line[0] <= x1 and line[1] < y1 and line[2] > y0
            )
            panel_bbox = [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)]
            panels.append({
                "panel_id": f"PLAN-{panel['index']:02d}",
                "title": panel["title"],
                "bbox": panel_bbox,
                "evidence_ids": evidence,
                "vertical_frame_evidence_count": panel_lines,
                "horizontal_frame_evidence_count": sum(
                    1 for line in horizontal_lines
                    if x0 <= line[0] and line[2] <= x1 and y0 <= line[1] <= y1
                ),
            })

            # Evidence-backed candidates stay UNKNOWN until approval-grade semantics are proven.
            if panel_lines >= 2:
                candidates.append(LockedElementCandidate(
                    candidate_id=f"{panel['index']:02d}-BOUNDARY-01",
                    element_type="OUTER_BOUNDARY",
                    bbox=tuple(panel_bbox),
                    confidence=0.90,
                    evidence_ids=(panel["evidence_id"], f"vector-frame-{panel['index']}"),
                    status="UNKNOWN",
                    rationale="Plan frame is evidenced by long vector lines, but architectural boundary semantics are not independently verified.",
                ))
                candidates.append(LockedElementCandidate(
                    candidate_id=f"{panel['index']:02d}-FORM-01",
                    element_type="OVERALL_PLAN_FORM",
                    bbox=tuple(panel_bbox),
                    confidence=0.88,
                    evidence_ids=(panel["evidence_id"], f"vector-frame-{panel['index']}"),
                    status="UNKNOWN",
                    rationale="Plan extent is evidenced, but overall architectural form is not independently verified.",
                ))
                candidates.append(LockedElementCandidate(
                    candidate_id=f"{panel['index']:02d}-WALLS-01",
                    element_type="WALLS",
                    bbox=tuple(panel_bbox),
                    confidence=0.72,
                    evidence_ids=(panel["evidence_id"], f"vector-wall-lines-{panel['index']}"),
                    status="UNKNOWN",
                    rationale="Long vector linework is consistent with walls, but wall semantics are not proven.",
                ))

            square_count = 0
            for drawing_index, rect in filled_rects:
                if x0 <= rect.x0 <= x1 and y0 <= rect.y0 <= y1:
                    square_count += 1
                    if square_count <= 12:
                        candidates.append(LockedElementCandidate(
                            candidate_id=f"{panel['index']:02d}-FIXED-{square_count:02d}",
                            element_type="COLUMNS",
                            bbox=(round(rect.x0, 2), round(rect.y0, 2),
                                  round(rect.x1, 2), round(rect.y1, 2)),
                            confidence=0.62,
                            evidence_ids=(panel["evidence_id"], f"pdf-drawing-{drawing_index}"),
                            status="UNKNOWN",
                            rationale="Near-square filled vector mark detected, but its architectural semantics are not proven.",
                        ))

        for candidate in candidates:
            candidate.validate()

        missing = [element_type for element_type in _FIXED_TYPES
                   if not any(c.element_type == element_type and c.status == "LOCKED"
                              for c in candidates)]
        return {
            "detector_id": self.detector_id,
            "status": "UNKNOWN" if missing else "ACCESSIBLE",
            "source_sha256": source_sha256,
            "page_count": document.page_count,
            "plan_panels": panels,
            "candidates": [candidate.__dict__ for candidate in candidates],
            "locked_element_types": [],
            "unresolved_fixed_element_types": missing,
            "reason": (
                "Vector evidence identifies plan panels and fixed-element candidates, "
                "but does not prove approval-grade semantics for columns/walls/doors/windows."
            ) if missing else "All fixed element types identified at approval-grade confidence.",
        }

    def _dwg_detect(self, path: Path, source_sha256: str) -> dict[str, Any]:
        if ezdwg is None:
            return self._dwg_unknown(source_sha256, "DWG_PARSER_UNAVAILABLE")
        try:
            doc = ezdwg.read(str(path))
            msp = doc.modelspace()
            entity_types = "LINE LWPOLYLINE ARC CIRCLE ELLIPSE POINT TEXT MTEXT DIMENSION INSERT MINSERT HATCH SPLINE"
            entities = list(msp.query(entity_types))
            headers = doc.header_variables()
            extmin, extmax = headers.get("extmin"), headers.get("extmax")
            by_type: dict[str, int] = {}
            candidates: list[LockedElementCandidate] = []
            text_labels: list[dict[str, Any]] = []
            line_segments: list[tuple[float,float,float,float,int]] = []
            inserts: list[dict[str, Any]] = []
            for e in entities:
                by_type[e.dxftype] = by_type.get(e.dxftype, 0) + 1
                dxf = e.dxf or {}
                if e.dxftype in {"TEXT", "MTEXT"}:
                    value = str(dxf.get("text", dxf.get("plain_text", ""))).strip()
                    if value:
                        text_labels.append({"handle": e.handle, "text": value, "layer": dxf.get("layer"), "insert": dxf.get("insert", dxf.get("location"))})
                if e.dxftype == "LINE":
                    p1, p2 = dxf.get("start"), dxf.get("end")
                    if p1 and p2:
                        line_segments.append((float(p1[0]),float(p1[1]),float(p2[0]),float(p2[1]),e.handle))
                if e.dxftype in {"INSERT", "MINSERT"}:
                    inserts.append({"handle": e.handle, "block": dxf.get("name", dxf.get("block_name")), "insert": dxf.get("insert")})

            # Native DWG geometry is now interpreted deterministically into
            # bounded architectural candidates. Geometry can strengthen evidence,
            # but it NEVER promotes a candidate to LOCKED by itself.
            lower_text = " ".join(str(x.get("text", "")) for x in text_labels).upper()
            layer_names = {str((e.dxf or {}).get("layer", "")).upper() for e in entities}
            blob = lower_text + " " + " ".join(layer_names)
            def has_any(*terms: str) -> bool:
                return any(term in blob for term in terms)

            def bbox_of_points(points):
                if not points:
                    return (0.0, 0.0, 0.0, 0.0)
                xs = [float(p[0]) for p in points]
                ys = [float(p[1]) for p in points]
                return (min(xs), min(ys), max(xs), max(ys))

            def entity_points(entity):
                try:
                    return [(float(p[0]), float(p[1])) for p in entity.to_points()]
                except Exception:
                    return []

            # Build a normalized geometry inventory. This is the first structured
            # geometry layer: line segments, polylines, arcs/circles and inserts
            # remain traceable to their original DWG handles.
            geometry_inventory = []
            polyline_closed = 0
            arc_count = 0
            circle_count = 0
            closed_shapes = []
            bbox = (0.0, 0.0, 0.0, 0.0)
            for entity in entities:
                dxf = entity.dxf or {}
                if entity.dxftype == "ARC":
                    arc_count += 1
                if entity.dxftype == "CIRCLE":
                    circle_count += 1
                pts = entity_points(entity)
                if pts:
                    geometry_inventory.append({
                        "handle": entity.handle,
                        "type": entity.dxftype,
                        "layer": dxf.get("layer"),
                        "points": pts[:200],
                        "closed": bool(dxf.get("closed", False)),
                    })
                    if entity.dxftype == "LWPOLYLINE" and bool(dxf.get("closed", False)):
                        polyline_closed += 1
                        closed_shapes.append((entity.handle, pts))

            if len(line_segments) >= 4:
                xs = [p for seg in line_segments for p in (seg[0], seg[2])]
                ys = [p for seg in line_segments for p in (seg[1], seg[3])]
                bbox = (min(xs), min(ys), max(xs), max(ys))
                candidates.append(LockedElementCandidate(
                    candidate_id="DWG-BOUNDARY-01", element_type="OUTER_BOUNDARY",
                    bbox=bbox, confidence=0.82, evidence_ids=(f"dwg-geometry-{source_sha256[:8]}",),
                    status="UNKNOWN", rationale="Native line geometry establishes the drawing envelope; closed-boundary semantics are still unverified."
                ))
                candidates.append(LockedElementCandidate(
                    candidate_id="DWG-FORM-01", element_type="OVERALL_PLAN_FORM",
                    bbox=bbox, confidence=0.80, evidence_ids=(f"dwg-geometry-{source_sha256[:8]}",),
                    status="UNKNOWN", rationale="Native geometry establishes a coherent plan-form candidate; architectural form semantics remain unverified."
                ))

            # Wall candidate: require either explicit architectural layer evidence
            # or a geometry pattern of multiple long, approximately parallel lines.
            long_segments = []
            for x0, y0, x1, y1, handle in line_segments:
                length = ((x1-x0)**2 + (y1-y0)**2) ** 0.5
                if length > 0:
                    long_segments.append((x0,y0,x1,y1,handle,length))
            span = max(
                [abs(x1-x0) for x0,y0,x1,y1,_ in line_segments] +
                [abs(y1-y0) for x0,y0,x1,y1,_ in line_segments] + [1.0]
            )
            parallel_pairs = 0
            for i, a in enumerate(long_segments):
                ax, ay, bx, by, _, alen = a
                av=(bx-ax,by-ay)
                for b in long_segments[i+1:]:
                    cx, cy, dx, dy, _, blen = b
                    if min(alen, blen) < span * 0.08:
                        continue
                    bv=(dx-cx,dy-cy)
                    cross=abs(av[0]*bv[1]-av[1]*bv[0])
                    if cross > max(alen*blen*0.02, 1e-9):
                        continue
                    # Distance from one endpoint of b to line a.
                    den=max(alen,1e-9)
                    dist=abs(av[0]*(cy-ay)-av[1]*(cx-ax))/den
                    if span*0.002 <= dist <= span*0.08:
                        parallel_pairs += 1
                        if parallel_pairs >= 4:
                            break
                if parallel_pairs >= 4:
                    break
            wall_geom = parallel_pairs >= 2
            if has_any("WALL", "MURO", "WALLS") or wall_geom:
                evidence = f"dwg-wall-geometry-{source_sha256[:8]}" if wall_geom else f"dwg-layer-{source_sha256[:8]}"
                candidates.append(LockedElementCandidate(
                    candidate_id="DWG-WALLS-01", element_type="WALLS", bbox=bbox if line_segments else (0,0,0,0),
                    confidence=0.86 if wall_geom and has_any("WALL","MURO","WALLS") else 0.78,
                    evidence_ids=(evidence,), status="UNKNOWN",
                    rationale="Wall semantics are supported by native geometry/layer evidence, but the complete wall graph and architectural role are not yet approval-grade."
                ))

            # Columns: closed polylines/circles or block inserts become individual
            # geometry candidates; block/layer semantics only corroborate them.
            column_shapes = []
            for handle, pts in closed_shapes:
                bb=bbox_of_points(pts)
                w,h=bb[2]-bb[0],bb[3]-bb[1]
                if w > 0 and h > 0:
                    ratio=max(w,h)/max(min(w,h),1e-9)
                    if ratio <= 2.5:
                        column_shapes.append((handle,bb))
            if inserts or column_shapes or has_any("COLUMN","COLUM","STRUCT"):
                if column_shapes:
                    for idx,(handle,bb) in enumerate(column_shapes[:24],1):
                        candidates.append(LockedElementCandidate(
                            candidate_id=f"DWG-COLUMN-{idx:02d}", element_type="COLUMNS", bbox=bb,
                            confidence=0.82 if has_any("COLUMN","COLUM","STRUCT") else 0.74,
                            evidence_ids=(f"dwg-closed-shape-{handle}",),
                            status="UNKNOWN",
                            rationale="Closed near-rectangular native geometry is a column candidate; structural semantics remain unverified."
                        ))
                else:
                    candidates.append(LockedElementCandidate(
                        candidate_id="DWG-COLUMNS-01", element_type="COLUMNS", bbox=bbox if line_segments else (0,0,0,0),
                        confidence=0.72, evidence_ids=(f"dwg-entity-{source_sha256[:8]}",), status="UNKNOWN",
                        rationale="Native block/layer evidence yields a column candidate set, but individual structural semantics are not yet approval-grade."
                    ))

            # Derive a conservative room/space graph from closed native polylines.
            # A space is only a candidate when the source itself supplies a closed
            # boundary; we never infer walls merely from labels.
            spaces = []
            for idx, (handle, pts) in enumerate(closed_shapes[:64], 1):
                bb = bbox_of_points(pts)
                if bb[2] <= bb[0] or bb[3] <= bb[1] or len(pts) < 3:
                    continue
                area = 0.0
                for i, a in enumerate(pts):
                    b = pts[(i + 1) % len(pts)]
                    area += a[0] * b[1] - b[0] * a[1]
                area = abs(area) / 2.0
                if area <= 1.0:
                    continue
                cx = sum(p[0] for p in pts) / len(pts)
                cy = sum(p[1] for p in pts) / len(pts)
                label = None
                label_dist = None
                for t in text_labels:
                    # Text positions are not consistently exposed by all ezdwg
                    # versions, so only attach labels when a usable insertion point exists.
                    pos = t.get("insert")
                    if pos:
                        d = ((float(pos[0])-cx)**2 + (float(pos[1])-cy)**2) ** 0.5
                        if label_dist is None or d < label_dist:
                            label_dist, label = d, t.get("text")
                spaces.append({
                    "space_id": f"DWG-SPACE-{idx:02d}",
                    "boundary_handle": handle,
                    "bbox": list(bb),
                    "centroid": [round(cx, 4), round(cy, 4)],
                    "area": round(area, 4),
                    "label": label,
                    "evidence_ids": [f"dwg-space-boundary-{handle}"],
                    "status": "UNKNOWN",
                })

            # Relationships are deliberately topological and evidence-backed:
            # shared boundary handle => SAME_BOUNDARY; centroid containment is
            # recorded only when both geometries are closed.
            space_relations = []
            for i, a in enumerate(spaces):
                for b in spaces[i + 1:]:
                    ax0, ay0, ax1, ay1 = a["bbox"]
                    bx0, by0, bx1, by1 = b["bbox"]
                    overlap_x = max(0.0, min(ax1,bx1)-max(ax0,bx0))
                    overlap_y = max(0.0, min(ay1,by1)-max(ay0,by0))
                    if overlap_x > 0 and overlap_y > 0:
                        space_relations.append({
                            "relation_id": f"{a['space_id']}__{b['space_id']}__OVERLAP",
                            "from": a["space_id"], "to": b["space_id"],
                            "type": "OVERLAP_CANDIDATE",
                            "evidence_ids": a["evidence_ids"] + b["evidence_ids"],
                            "status": "UNKNOWN",
                        })

            # Door/window candidates: arcs and short linework are represented as
            # candidate evidence; explicit layer/text naming is corroborating only.
            door_evidence = arc_count > 0 or has_any("DOOR","PUERTA")
            window_evidence = circle_count > 0 or has_any("WINDOW","VENT","WINDOWS")
            if door_evidence:
                candidates.append(LockedElementCandidate(
                    candidate_id="DWG-DOORS-01", element_type="DOORS", bbox=bbox if line_segments else (0,0,0,0),
                    confidence=0.78 if has_any("DOOR","PUERTA") and arc_count else 0.70,
                    evidence_ids=(f"dwg-door-geometry-{source_sha256[:8]}",), status="UNKNOWN",
                    rationale="Native arc/layer/text evidence supports a door candidate set; individual openings and swing semantics are not yet approval-grade."
                ))
            if window_evidence:
                candidates.append(LockedElementCandidate(
                    candidate_id="DWG-WINDOWS-01", element_type="WINDOWS", bbox=bbox if line_segments else (0,0,0,0),
                    confidence=0.76 if has_any("WINDOW","VENT","WINDOWS") else 0.66,
                    evidence_ids=(f"dwg-window-geometry-{source_sha256[:8]}",), status="UNKNOWN",
                    rationale="Native circle/layer/text evidence supports a window candidate set; wall-host relationships are not yet approval-grade."
                ))
            for candidate in candidates:
                candidate.validate()
            present = {c.element_type for c in candidates}
            missing = [x for x in _FIXED_TYPES if x not in present]
            return {
                "detector_id": self.detector_id + "-dwg",
                "status": "UNKNOWN" if missing or any(c.status != "LOCKED" for c in candidates) else "ACCESSIBLE",
                "source_sha256": source_sha256, "page_count": 1,
                "plan_panels": [{"panel_id":"DWG-MODELSPACE-01","bbox":[extmin,extmax],"evidence_ids":[f"dwg-geometry-{source_sha256[:8]}"]}],
                "candidates": [c.__dict__ for c in candidates],
                "locked_element_types": [], "unresolved_fixed_element_types": missing,
                "dwg_entity_counts": by_type, "dwg_text_labels": text_labels[:200],
                "dwg_insert_count": len(inserts), "dwg_version": doc.version, "dwg_units": doc.units,
                "dwg_geometry": {
                    "inventory_count": len(geometry_inventory),
                    "line_segment_count": len(line_segments),
                    "closed_polyline_count": polyline_closed,
                    "arc_count": arc_count,
                    "circle_count": circle_count,
                    "parallel_wall_pair_evidence": parallel_pairs,
                    "closed_shape_candidates": len(column_shapes),
                    "sample": geometry_inventory[:80],
                },
                "spaces": spaces,
                "space_relations": space_relations,
                "reason": "Native DWG entities are parsed into evidence-backed candidates; approval-grade locking remains fail-closed."
            }
        except Exception as exc:
            return self._dwg_unknown(source_sha256, "DWG_DETECTION_FAILED:" + type(exc).__name__)

    def _dwg_unknown(self, source_sha256: str, reason: str) -> dict[str, Any]:
        return {"detector_id": self.detector_id + "-dwg", "status":"UNKNOWN", "source_sha256":source_sha256,
                "page_count":1, "plan_panels":[], "candidates":[], "locked_element_types":[],
                "unresolved_fixed_element_types":list(_FIXED_TYPES), "reason":reason}

    def _raster_fallback(self, source_sha256: str) -> dict[str, Any]:
        return {
            "detector_id": self.detector_id,
            "status": "UNKNOWN",
            "source_sha256": source_sha256,
            "plan_panels": [],
            "candidates": [],
            "locked_element_types": [],
            "unresolved_fixed_element_types": list(_FIXED_TYPES),
            "reason": "Raster-only input lacks approval-grade semantic evidence for fixed elements.",
        }
