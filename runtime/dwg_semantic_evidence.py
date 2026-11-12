"""Read-only DWG evidence extraction for Golden Understanding."""
from __future__ import annotations
import hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any
from runtime.dwg_scale_unit_bridge import observe_dwg_scale_unit

SEMANTIC_TOKENS = {
    "WALLS": ("WALL", "WALLS", "A-WALL"),
    "DOORS": ("DOOR", "DOORS", "A-DOOR"),
    "WINDOWS": ("WINDOW", "WINDOWS", "A-WIND", "A-WINDOW"),
    "COLUMNS": ("COLUMN", "COLUMNS", "COL", "A-COLS", "A-COLUMN", "COULMN"),
}

def _value(entity: Any, key: str, default: Any = None) -> Any:
    dxf = getattr(entity, "dxf", None)
    if dxf is None: return default
    try: return dxf.get(key, default)
    except AttributeError:
        try: return dxf[key]
        except (KeyError, TypeError): return default

def _read_layer_table(doc: Any) -> tuple[dict[str, dict[str, Any]], dict[Any, str]]:
    """Read ezdwg's layer table and build the documented handle -> name map."""
    try:
        table = doc.layers()
    except TypeError:
        table = getattr(doc, "layers", None)
    except Exception:
        table = None

    records: dict[str, dict[str, Any]] = {}
    names_by_handle: dict[Any, str] = {}
    if not hasattr(table, "items"):
        return records, names_by_handle

    for name, raw in table.items():
        if not isinstance(raw, dict):
            continue
        layer_name = str(name)
        records[layer_name] = {
            key: _jsonable(raw.get(key))
            for key in (
                "handle", "color_index", "true_color", "linetype", "off",
                "frozen", "locked", "plot", "lineweight", "lineweight_index",
                "transparency",
            )
            if key in raw
        }
        handle = raw.get("handle")
        if handle is not None:
            names_by_handle[handle] = layer_name
            names_by_handle[str(handle)] = layer_name
    return records, names_by_handle


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)): return value
    if isinstance(value, (list, tuple)): return [_jsonable(v) for v in value]
    if isinstance(value, dict): return {str(k): _jsonable(v) for k, v in value.items()}
    for attrs in (("x","y","z"),("x","y")):
        if all(hasattr(value,a) for a in attrs):
            return {a: float(getattr(value,a)) for a in attrs}
    return str(value)

def _token_hits(name: str) -> set[str]:
    normalized = name.upper().replace("-", "_").replace(" ", "_")
    return {semantic for semantic,tokens in SEMANTIC_TOKENS.items()
            if any(token.replace("-","_") in normalized for token in tokens)}


_LEVEL_NUMBER = r"\d+(?:[.,]\d+)?"
_LEVEL_UNIT = r"(?:mm|cm|m)"
_ELEVATION_CONTEXT_VALUE_RE = re.compile(
    rf"(?:\b(?:RL|EL|FFL|T\.?O\.?\b|کد\s*ارتفاعی|تراز|کف|ارتفاع)"
    rf"\s*(?:[:=]\s*)?(?P<marker>±|[+-])?\s*"
    rf"(?P<value>{_LEVEL_NUMBER})\s*(?P<unit>{_LEVEL_UNIT})?",
    re.IGNORECASE,
)
_SIGNED_LEVEL_VALUE_RE = re.compile(
    rf"(?P<marker>±|[+-])\s*(?P<value>{_LEVEL_NUMBER})\s*(?P<unit>{_LEVEL_UNIT})?",
    re.IGNORECASE,
)
_UNIT_LEVEL_VALUE_RE = re.compile(
    rf"(?P<value>{_LEVEL_NUMBER})\s*(?P<unit>{_LEVEL_UNIT})",
    re.IGNORECASE,
)
_LEVEL_CONTEXT_RE = re.compile(
    r"(?:\b(?:RL|EL|FFL|T\.?O\.?|LEVEL|LVL)\b|کد\s*ارتفاعی|تراز|کف|ارتفاع)",
    re.IGNORECASE,
)

def _level_candidate(text: str, handle: int, source_sha256: str, source_units: Any) -> dict[str, Any] | None:
    """Extract elevation only when the numeric value is tied to elevation evidence."""
    raw = " ".join(str(text).split())
    if not raw:
        return None

    matches = list(_ELEVATION_CONTEXT_VALUE_RE.finditer(raw))
    if not matches:
        matches = list(_SIGNED_LEVEL_VALUE_RE.finditer(raw))
    if not matches:
        matches = list(_UNIT_LEVEL_VALUE_RE.finditer(raw))
    if not matches:
        # A floor index such as LEVEL 2 is not an elevation.
        return None

    context = bool(_LEVEL_CONTEXT_RE.search(raw))
    ambiguous = len(matches) != 1
    match = matches[0]
    marker = match.groupdict().get("marker") or ""
    unit = match.groupdict().get("unit")
    value = None if ambiguous else float(match.group("value").replace(",", "."))
    if not ambiguous and not unit:
        unit = str(source_units or "")
    status = "SUPPORTED" if (not ambiguous and unit) else "UNKNOWN"
    return {
        "handle": handle,
        "raw_text": raw,
        "marker": marker,
        "elevation": (value * (-1.0 if marker == "-" else 1.0)) if value is not None else None,
        "unit": unit or "",
        "context_explicit": context,
        "provenance": "DIRECT",
        "status": status,
        "reason": "AMBIGUOUS_ELEVATION_VALUES" if ambiguous else ("UNIT_UNKNOWN" if not unit else ""),
        "source_sha256": source_sha256,
    }

_SECTION_CONTEXT_RE = re.compile(
    r"(?:\b(?:SECTION|SECT\.?|CUT[\s_-]*PLANE|ELEVATION|ELEV\.?|DETAIL)\b|مقطع|برش|جزئیات)",
    re.IGNORECASE,
)
_SECTION_LABEL_RE = re.compile(
    r"(?P<label>(?:[A-Z]{1,2}|\d{1,2})\s*[-–—/]\s*(?:[A-Z]{1,2}|\d{1,2}))",
    re.IGNORECASE,
)
_SECTION_BLOCK_RE = re.compile(r"(?:SECTION|SECT|CUT[\s_-]*PLANE|ELEVATION|DETAIL)", re.IGNORECASE)

def _section_marker_candidate(
    text: str, handle: int, source_sha256: str, evidence_kind: str = "TEXT"
) -> dict[str, Any] | None:
    """Record explicit marker evidence only; never infer direction or cut-plane geometry."""
    raw = " ".join(str(text).split())
    if not raw:
        return None
    label_match = _SECTION_LABEL_RE.search(raw)
    context = bool(_SECTION_CONTEXT_RE.search(raw))
    block_context = evidence_kind == "BLOCK" and bool(_SECTION_BLOCK_RE.search(raw))
    if not ((context and label_match) or block_context):
        return None
    if re.search(r"(?:CUT[\s_-]*PLANE|برش)", raw, re.IGNORECASE):
        marker_type = "CUT_PLANE_MARKER"
    elif re.search(r"(?:ELEVATION|ELEV\.?)", raw, re.IGNORECASE):
        marker_type = "ELEVATION_MARKER"
    elif re.search(r"(?:DETAIL|جزئیات)", raw, re.IGNORECASE):
        marker_type = "DETAIL_MARKER"
    else:
        marker_type = "SECTION_MARKER"
    return {
        "handle": handle,
        "raw_text": raw,
        "marker_type": marker_type,
        "label": re.sub(r"\s+", "", label_match.group("label")).upper() if label_match else "",
        "evidence_kind": evidence_kind,
        "direction_status": "UNKNOWN",
        "cut_plane_status": "UNKNOWN",
        "provenance": "DIRECT",
        "status": "SUPPORTED",
        "source_sha256": source_sha256,
    }

def extract_dwg_evidence(path: str | Path) -> dict[str, Any]:
    import ezdwg
    source = Path(path)
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    doc = ezdwg.read(str(source))
    scale_unit_evidence = observe_dwg_scale_unit({"dwg_units": getattr(doc, "insunits", None)}, source_sha256)
    entities = list(doc.modelspace().query())
    layer_table, layer_names_by_handle = _read_layer_table(doc)
    type_counts, layer_counts, block_counts = Counter(), Counter(), Counter()
    geometry_counts = Counter()
    text_evidence, dimension_evidence, level_evidence, section_marker_evidence = [], [], [], []
    candidates = {k: [] for k in SEMANTIC_TOKENS}

    for entity in entities:
        dxftype = str(getattr(entity, "dxftype", "UNKNOWN"))
        type_counts[dxftype] += 1
        handle = int(getattr(entity, "handle", 0))
        layer_handle = _value(entity, "layer_handle")
        layer = layer_names_by_handle.get(layer_handle)
        if layer is None and layer_handle is not None:
            layer = layer_names_by_handle.get(str(layer_handle))
        if layer is None:
            layer = _value(entity, "layer")
        if layer is not None:
            layer_name = str(layer)
            layer_counts[layer_name] += 1
            for semantic in _token_hits(layer_name):
                candidates[semantic].append({
                    "kind": "LAYER_NAME", "value": layer_name,
                    "layer_handle": _jsonable(layer_handle), "handle": handle,
                    "provenance": "DIRECT", "source_sha256": source_sha256,
                })
        if dxftype in {"INSERT","MINSERT"}:
            name = _value(entity, "name")
            if name:
                block_name = str(name); block_counts[block_name] += 1
                for semantic in _token_hits(block_name):
                    candidates[semantic].append({"kind":"BLOCK_NAME","value":block_name,
                        "handle":handle,"provenance":"DIRECT"})
                section_marker = _section_marker_candidate(block_name, handle, source_sha256, "BLOCK")
                if section_marker:
                    section_marker_evidence.append(section_marker)
        if dxftype in {"LINE","LWPOLYLINE","ARC","CIRCLE","ELLIPSE","SPLINE","HATCH"}:
            geometry_counts[dxftype] += 1
        if dxftype in {"TEXT","MTEXT","ATTRIB","ATTDEF"}:
            text = str(getattr(entity, "text", None) or _value(entity, "text", ""))
            text_evidence.append({"handle":handle,"type":dxftype,
                "layer":str(layer) if layer is not None else None,
                "layer_handle":_jsonable(layer_handle),
                "text":text,
                "insert":_jsonable(_value(entity, "insert")),
                "rotation":_jsonable(_value(entity, "rotation")),"provenance":"DIRECT"})
            level = _level_candidate(text, handle, source_sha256, getattr(doc, "units", None))
            if level:
                level_evidence.append(level)
            section_marker = _section_marker_candidate(text, handle, source_sha256)
            if section_marker:
                section_marker_evidence.append(section_marker)
        if dxftype == "DIMENSION":
            dimension_evidence.append({"handle":handle,"type":dxftype,
                "layer":str(layer) if layer is not None else None,
                "layer_handle":_jsonable(layer_handle),
                "text":str(_value(entity, "text", "")),
                "actual_measurement":_jsonable(_value(entity, "actual_measurement")),
                "defpoint":_jsonable(_value(entity, "defpoint")),
                "defpoint2":_jsonable(_value(entity, "defpoint2")),
                "defpoint3":_jsonable(_value(entity, "defpoint3")),"provenance":"DIRECT"})

    semantic_support = {semantic:{
        "status":"SUPPORTED" if rows else "UNKNOWN",
        "provenance":"DIRECT" if rows else "UNKNOWN",
        "evidence":rows} for semantic,rows in candidates.items()}
    try:
        hv = doc.header_variables()
        header = {"extmin":_jsonable(hv.get("extmin")),"extmax":_jsonable(hv.get("extmax")),
                  "insunits":_jsonable(hv.get("insunits")),"lunits":_jsonable(hv.get("lunits"))}
    except Exception:
        header = {}
    return {
        "schema":"dwg-semantic-evidence-v1",
        "source_profile":{"source_class":"ENGINEERING_PLAN","path":str(source),
            "sha256":source_sha256,"version":str(getattr(doc,"version","UNKNOWN")),
            "decode_version":str(getattr(doc,"decode_version","UNKNOWN")),
            "units":getattr(doc,"units",None),"insunits":getattr(doc,"insunits",None),
            "provenance":"DIRECT"},
        "entity_counts":dict(sorted(type_counts.items())),
        "layer_counts":dict(sorted(layer_counts.items())),
        "layer_table":layer_table,
        "layer_table_status":"SUPPORTED" if layer_table else "UNKNOWN",
        "block_counts":dict(sorted(block_counts.items())),
        "geometry_counts":dict(sorted(geometry_counts.items())),
        "text":text_evidence,"dimensions":dimension_evidence,"levels":level_evidence,
        "section_markers":section_marker_evidence,
        "semantic_candidates":semantic_support,"header":header,
        "scale_unit_evidence":scale_unit_evidence,
        "authority":{"read_only":True,"semantic_authority":False,
            "generic_linework_is_not_architectural_truth":True},
    }

def write_evidence(path: str | Path, output: str | Path) -> None:
    Path(output).write_text(json.dumps(extract_dwg_evidence(path),ensure_ascii=False,
        indent=2,sort_keys=True),encoding="utf-8")
