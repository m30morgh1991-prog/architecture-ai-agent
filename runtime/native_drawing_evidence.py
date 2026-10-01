"""Conservative native DWG evidence extraction for drawing-standard checks.

This module extracts evidence only. It never promotes uncertain geometry or
labels into architectural compliance.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import ezdwg
except ImportError:  # pragma: no cover
    ezdwg = None


_CANONICAL_TITLE_TAGS = {
    "TITLE", "DRAWING_TITLE", "DWG_TITLE", "SCALE", "SHEET", "SHEET_NO",
    "DATE", "DRAWN", "CHECKED", "APPROVED", "REV", "REVISION"
}
_VIEW_WORDS = {
    "PLAN": "PLAN",
    "PLANTA": "PLAN",
    "SECTION": "SECTION",
    "SECT": "SECTION",
    "ELEVATION": "ELEVATION",
    "ELEV": "ELEVATION",
}


def _xy(value: Any) -> tuple[float, float] | None:
    if value is None:
        return None
    try:
        return float(value[0]), float(value[1])
    except (TypeError, ValueError, IndexError, KeyError):
        return None


def _distance_point_segment(point: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    px, py = point
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    den = dx * dx + dy * dy
    if den <= 1e-12:
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / den))
    qx, qy = ax + t * dx, ay + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5


def _text(entity: Any) -> str:
    dxf = getattr(entity, "dxf", {}) or {}
    return str(dxf.get("text", dxf.get("plain_text", "")) or "").strip()


def _attr_records(entity: Any) -> list[dict[str, Any]]:
    records = []
    try:
        attribs = getattr(entity, "attribs", []) or []
        for attrib in attribs:
            dxf = getattr(attrib, "dxf", {}) or {}
            tag = str(dxf.get("tag", "")).strip().upper()
            value = str(dxf.get("text", "") or "").strip()
            if tag:
                records.append({"tag": tag, "value": value, "handle": getattr(attrib, "handle", None)})
    except Exception:
        return []
    return records


def _extract_geometry(entities: list[Any]) -> tuple[list[tuple[float, float, float, float, str]], list[str]]:
    lines = []
    evidence = []
    for entity in entities:
        if getattr(entity, "dxftype", "") != "LINE":
            continue
        dxf = getattr(entity, "dxf", {}) or {}
        a, b = _xy(dxf.get("start")), _xy(dxf.get("end"))
        if a and b:
            handle = str(getattr(entity, "handle", ""))
            lines.append((a[0], a[1], b[0], b[1], handle))
            evidence.append(f"dwg-line-{handle}")
    return lines, evidence


def _dimension_evidence(entities: list[Any], lines: list[tuple[float, float, float, float, str]]) -> dict[str, Any]:
    dims = []
    unresolved = []
    for entity in entities:
        if getattr(entity, "dxftype", "") != "DIMENSION":
            continue
        dxf = getattr(entity, "dxf", {}) or {}
        handle = str(getattr(entity, "handle", ""))
        points = []
        for key in ("defpoint", "defpoint2", "defpoint3", "defpoint4", "insert"):
            p = _xy(dxf.get(key))
            if p and p not in points:
                points.append(p)
        measurement = dxf.get("actual_measurement", dxf.get("measurement"))
        try:
            measurement = float(measurement) if measurement is not None else None
        except (TypeError, ValueError):
            measurement = None
        matched = []
        for p in points:
            nearest = min(
                (
                    (_distance_point_segment(p, (x0, y0), (x1, y1)), handle_line)
                    for x0, y0, x1, y1, handle_line in lines
                ),
                default=None,
            )
            if nearest and nearest[0] <= 1.0:
                matched.append({"point": list(p), "line_handle": nearest[1], "distance": round(nearest[0], 6)})
        record = {
            "dimension_id": f"DWG-DIM-{handle}",
            "evidence_id": f"dwg-dimension-{handle}",
            "definition_points": [list(p) for p in points],
            "measurement": measurement,
            "matched_geometry": matched,
            "status": "UNKNOWN",
        }
        dims.append(record)
        if len(points) < 2 or len(matched) < 2:
            unresolved.append(record["dimension_id"])
    associated = bool(dims) and not unresolved
    return {
        "count": len(dims),
        "dimensions": dims,
        "dimensions_geometry_associated": associated if dims else None,
        "unresolved": unresolved,
        "evidence_ids": [x["evidence_id"] for x in dims],
    }


def _view_evidence(entities: list[Any], document: Any) -> dict[str, Any]:
    labels = []
    for entity in entities:
        if getattr(entity, "dxftype", "") not in {"TEXT", "MTEXT"}:
            continue
        value = _text(entity).upper()
        for token, normalized in _VIEW_WORDS.items():
            if token in value:
                labels.append({
                    "text": _text(entity),
                    "normalized": normalized,
                    "handle": getattr(entity, "handle", None),
                    "evidence_id": f"dwg-view-label-{getattr(entity, 'handle', 'unknown')}",
                })
                break

    layout_names = []
    try:
        layouts = document.layouts()
        for layout in layouts:
            name = str(getattr(layout, "name", "") or "")
            if name:
                layout_names.append(name)
    except Exception:
        pass

    # Text labels alone are insufficient to establish view identity.
    explicit_layout_evidence = [name for name in layout_names if name.upper() not in {"MODEL", "MODELSPACE"}]
    identity = True if labels and explicit_layout_evidence else None
    return {
        "labels": labels,
        "layout_names": layout_names,
        "explicit_layout_evidence": explicit_layout_evidence,
        "view_section_identity": identity,
        "evidence_ids": [x["evidence_id"] for x in labels],
    }


def _title_block_evidence(entities: list[Any]) -> dict[str, Any]:
    blocks = []
    for entity in entities:
        if getattr(entity, "dxftype", "") not in {"INSERT", "MINSERT"}:
            continue
        dxf = getattr(entity, "dxf", {}) or {}
        name = str(dxf.get("name", dxf.get("block_name", "")) or "")
        attrs = _attr_records(entity)
        if not attrs and not any(token in name.upper() for token in ("TITLE", "TBLOCK", "TITLEBLOCK", "FRAME")):
            continue
        tags = {a["tag"] for a in attrs}
        matched = sorted(tags & _CANONICAL_TITLE_TAGS)
        blocks.append({
            "block": name,
            "handle": getattr(entity, "handle", None),
            "attributes": attrs,
            "recognized_tags": matched,
            "evidence_id": f"dwg-title-block-{getattr(entity, 'handle', 'unknown')}",
        })
    # A title block is not considered valid merely because a block exists.
    valid = True if blocks and any(len(x["recognized_tags"]) >= 3 for x in blocks) else None
    return {
        "blocks": blocks,
        "title_block_fields_valid": valid,
        "evidence_ids": [x["evidence_id"] for x in blocks],
    }


def cross_view_consistency(views: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare only explicitly identified views; absence of correspondence stays UNKNOWN."""
    explicit = [v for v in views if v.get("identity") in {"PLAN", "SECTION", "ELEVATION"} and v.get("fingerprint")]
    if len(explicit) < 2:
        return {"cross_view_consistent": None, "unresolved": ["INSUFFICIENT_VIEW_CORRESPONDENCE"], "evidence_ids": []}
    fingerprints = {str(v["fingerprint"]) for v in explicit}
    consistent = len(fingerprints) == len(explicit) or all(v.get("correspondence_verified") is True for v in explicit)
    return {
        "cross_view_consistent": True if consistent else False,
        "unresolved": [] if consistent else ["VIEW_CORRESPONDENCE_CONTRADICTION"],
        "evidence_ids": [str(v["evidence_id"]) for v in explicit],
    }


def extract_native_drawing_evidence(source_path: str, input_type: str) -> dict[str, Any]:
    if input_type != "DWG":
        return {
            "dimensions_geometry_associated": None,
            "view_section_identity": None,
            "title_block_fields_valid": None,
            "cross_view_consistent": None,
            "dimension_evidence": {},
            "view_evidence": {},
            "title_block_evidence": {},
            "evidence_ids": [],
            "unresolved": ["NATIVE_DWG_EVIDENCE_UNAVAILABLE"],
        }
    if ezdwg is None:
        return {
            "dimensions_geometry_associated": None,
            "view_section_identity": None,
            "title_block_fields_valid": None,
            "cross_view_consistent": None,
            "dimension_evidence": {},
            "view_evidence": {},
            "title_block_evidence": {},
            "evidence_ids": [],
            "unresolved": ["DWG_PARSER_UNAVAILABLE"],
        }
    try:
        document = ezdwg.read(str(Path(source_path)))
        modelspace = document.modelspace()
        entity_types = "LINE LWPOLYLINE ARC CIRCLE ELLIPSE POINT TEXT MTEXT DIMENSION INSERT MINSERT HATCH SPLINE"
        entities = list(modelspace.query(entity_types))
        lines, line_evidence = _extract_geometry(entities)
        dimensions = _dimension_evidence(entities, lines)
        views = _view_evidence(entities, document)
        title = _title_block_evidence(entities)
        evidence_ids = sorted(set(line_evidence + dimensions["evidence_ids"] + views["evidence_ids"] + title["evidence_ids"]))
        unresolved = sorted(set(dimensions["unresolved"]))
        if views["view_section_identity"] is None:
            unresolved.append("VIEW_IDENTITY_UNCERTAIN")
        if title["title_block_fields_valid"] is None:
            unresolved.append("TITLE_BLOCK_EVIDENCE_INCOMPLETE")
        return {
            "dimensions_geometry_associated": dimensions["dimensions_geometry_associated"],
            "view_section_identity": views["view_section_identity"],
            "title_block_fields_valid": title["title_block_fields_valid"],
            "cross_view_consistent": None,
            "dimension_evidence": dimensions,
            "view_evidence": views,
            "title_block_evidence": title,
            "evidence_ids": evidence_ids,
            "unresolved": sorted(set(unresolved)),
        }
    except Exception as exc:
        return {
            "dimensions_geometry_associated": None,
            "view_section_identity": None,
            "title_block_fields_valid": None,
            "cross_view_consistent": None,
            "dimension_evidence": {},
            "view_evidence": {},
            "title_block_evidence": {},
            "evidence_ids": [],
            "unresolved": [f"NATIVE_EVIDENCE_FAILED_CLOSED:{type(exc).__name__}"],
        }
