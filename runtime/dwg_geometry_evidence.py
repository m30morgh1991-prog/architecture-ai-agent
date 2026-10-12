"""Read-only, defensive geometry evidence helpers for DWG entities."""
from __future__ import annotations
from typing import Any
import math

def _dxf(entity: Any, key: str, default: Any = None) -> Any:
    data = getattr(entity, "dxf", None)
    if data is None:
        return default
    try:
        return data.get(key, default)
    except (AttributeError, TypeError):
        try:
            return data[key]
        except (KeyError, TypeError):
            return default

def _point(value: Any) -> dict[str, float] | None:
    if value is None:
        return None
    if isinstance(value, (tuple, list)) and len(value) >= 2:
        try:
            result = {"x": float(value[0]), "y": float(value[1])}
            if len(value) >= 3:
                result["z"] = float(value[2])
            return result if all(math.isfinite(v) for v in result.values()) else None
        except (TypeError, ValueError):
            return None
    if all(hasattr(value, k) for k in ("x", "y")):
        try:
            result = {"x": float(value.x), "y": float(value.y)}
            if hasattr(value, "z"):
                result["z"] = float(value.z)
            return result if all(math.isfinite(v) for v in result.values()) else None
        except (TypeError, ValueError):
            return None
    return None

def _safe_float(value: Any) -> float | None:
    try:
        number = float(value) if value is not None else None
        return number if number is not None and math.isfinite(number) else None
    except (TypeError, ValueError):
        return None

def extract_entity_geometry(entity: Any, entity_type: str, handle: int) -> dict[str, Any] | None:
    """Extract direct coordinates only; never infer architectural meaning."""
    row: dict[str, Any] = {
        "handle": handle,
        "type": entity_type,
        "layer": _dxf(entity, "layer"),
        "provenance": "DIRECT",
        "semantic_authority": False,
    }
    if entity_type == "LINE":
        row.update(start=_point(_dxf(entity, "start")), end=_point(_dxf(entity, "end")))
    elif entity_type == "LWPOLYLINE":
        points = None
        getter = getattr(entity, "get_points", None)
        if callable(getter):
            for format_code in ("xy", "xyseb"):
                try:
                    points = getter(format_code)
                    if points is not None:
                        break
                except (TypeError, ValueError, AttributeError, NotImplementedError):
                    continue
        if points is None:
            points = _dxf(entity, "points")
        normalized = []
        vertices_valid = points is not None
        if points is not None:
            try:
                for p in points:
                    point = _point(p)
                    if point is None or "x" not in point or "y" not in point:
                        vertices_valid = False
                        normalized = []
                        break
                    # LWPOLYLINE vertices are planar; retain XY only.
                    normalized.append({"x": point["x"], "y": point["y"]})
            except (TypeError, ValueError):
                vertices_valid = False
                normalized = []
        row["vertices"] = normalized if vertices_valid else []

        row["closed"] = _dxf(entity, "closed")
        row["elevation"] = _safe_float(_dxf(entity, "elevation"))
    elif entity_type in {"ARC", "CIRCLE"}:
        row.update(center=_point(_dxf(entity, "center")), radius=_safe_float(_dxf(entity, "radius")))
        if entity_type == "ARC":
            row.update(start_angle=_safe_float(_dxf(entity, "start_angle")),
                       end_angle=_safe_float(_dxf(entity, "end_angle")))
    elif entity_type == "ELLIPSE":
        row.update(center=_point(_dxf(entity, "center")),
                   major_axis=_point(_dxf(entity, "major_axis")),
                   ratio=_safe_float(_dxf(entity, "ratio")),
                   start_param=_safe_float(_dxf(entity, "start_param")),
                   end_param=_safe_float(_dxf(entity, "end_param")))
    elif entity_type == "SPLINE":
        controls = _dxf(entity, "control_points")
        normalized = []
        if controls is not None:
            try:
                normalized = [p for p in (_point(v) for v in controls) if p is not None]
            except TypeError:
                normalized = []
        row["control_points"] = normalized
        row["degree"] = _dxf(entity, "degree")
        row["closed"] = _dxf(entity, "closed")
    else:
        return None
    # A single present field is not enough to claim usable coordinates.
    # Require the complete direct-coordinate field set for each entity type.
    required_fields = {
        "LINE": ("start", "end"),
        "LWPOLYLINE": ("vertices",),
        "ARC": ("center", "radius", "start_angle", "end_angle"),
        "CIRCLE": ("center", "radius"),
        "ELLIPSE": ("center", "major_axis", "ratio", "start_param", "end_param"),
        "SPLINE": ("control_points", "degree"),
    }
    required = required_fields.get(entity_type, ())
    complete = bool(required) and all(row.get(key) is not None for key in required)
    if entity_type in {"LWPOLYLINE", "SPLINE"}:
        collection_key = "vertices" if entity_type == "LWPOLYLINE" else "control_points"
        complete = complete and bool(row.get(collection_key))
    if entity_type == "LINE":
        complete = complete and all(isinstance(row.get(key), dict) and
                                     "x" in row[key] and "y" in row[key]
                                     for key in ("start", "end"))
    elif entity_type in {"ARC", "CIRCLE", "ELLIPSE"}:
        point_keys = ("center", "major_axis") if entity_type == "ELLIPSE" else ("center",)
        complete = complete and all(isinstance(row.get(key), dict) and
                                     "x" in row[key] and "y" in row[key]
                                     for key in point_keys)
    row["coordinate_status"] = "SUPPORTED" if complete else "UNKNOWN"
    return row
