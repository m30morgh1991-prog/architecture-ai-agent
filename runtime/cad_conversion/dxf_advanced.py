"""Conservative semantic fingerprints for complex DXF entities."""
from __future__ import annotations

import math
from typing import Any


_IGNORED_DXF_KEYS = {"handle", "owner", "paperspace"}


def _normalise(value: Any, tolerance: float) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("DXF_GEOMETRY_NONFINITE")
        return round(value / tolerance)
    if hasattr(value, "x") and hasattr(value, "y"):
        coords = [value.x, value.y]
        if hasattr(value, "z"):
            coords.append(value.z)
        return tuple(_normalise(float(v), tolerance) for v in coords)
    if isinstance(value, dict):
        return tuple(sorted((str(k), _normalise(v, tolerance)) for k, v in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_normalise(v, tolerance) for v in value)
    if hasattr(value, "dxfattribs"):
        return _normalise(value.dxfattribs(), tolerance)
    if hasattr(value, "__dict__"):
        data = {k: v for k, v in vars(value).items() if not k.startswith("_")}
        if data:
            return _normalise(data, tolerance)
    raise TypeError(f"DXF_COMPLEX_VALUE_UNSUPPORTED:{type(value).__name__}")


def _dxf_payload(entity: Any, tolerance: float) -> Any:
    attrs = entity.dxfattribs()
    return _normalise(
        {key: value for key, value in attrs.items() if key not in _IGNORED_DXF_KEYS},
        tolerance,
    )


def advanced_entity_signature(entity: Any, tolerance: float) -> tuple | None:
    """Return a semantic signature for complex entities, or None if uncertain."""
    kind = entity.dxftype()
    if kind not in {"DIMENSION", "HATCH", "SPLINE", "ATTRIB", "ATTDEF", "LEADER", "MLEADER"}:
        return None
    try:
        payload = _dxf_payload(entity, tolerance)
        extra: Any = None
        if kind == "HATCH":
            paths = []
            for path in entity.paths:
                path_data = {
                    "path_type_flags": getattr(path, "path_type_flags", None),
                    "is_closed": getattr(path, "is_closed", None),
                    "vertices": getattr(path, "vertices", None),
                    "edges": getattr(path, "edges", None),
                }
                paths.append(_normalise(path_data, tolerance))
            extra = (
                tuple(paths),
                getattr(entity.dxf, "pattern_name", None),
                _normalise(getattr(entity.dxf, "pattern_scale", 1.0), tolerance),
                _normalise(getattr(entity.dxf, "pattern_angle", 0.0), tolerance),
                getattr(entity.dxf, "solid_fill", None),
                getattr(entity.dxf, "associative", None),
            )
        elif kind == "DIMENSION":
            geometry = entity.dxf.get("geometry")
            extra = ("geometry_block", str(geometry)) if geometry else ("geometry_block_missing",)
        elif kind == "LEADER":
            extra = _normalise(getattr(entity, "vertices", ()), tolerance)
        elif kind == "MLEADER":
            return None
        return (kind, payload, extra)
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None


def insert_attributes_signature(entity: Any, tolerance: float) -> Any:
    """Fingerprint attached ATTRIB values; unresolved values stay unsupported."""
    try:
        return tuple(
            _normalise(attribute.dxfattribs(), tolerance)
            for attribute in getattr(entity, "attribs", ())
        )
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None


_PRESENTATION_KEYS = (
    "color", "true_color", "color_name", "linetype", "lineweight",
    "transparency", "ltscale", "invisible", "thickness", "extrusion",
    "material", "plotstyle",
)


def presentation_signature(entity: Any, tolerance: float) -> Any:
    """Compare common display and OCS properties for supported entities."""
    try:
        attrs = entity.dxfattribs()
        selected = {key: attrs[key] for key in _PRESENTATION_KEYS if key in attrs}
        return _normalise(selected, tolerance)
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None
