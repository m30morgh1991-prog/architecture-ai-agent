"""Read-only DWG evidence extraction for Golden Understanding."""
from __future__ import annotations
import hashlib, json
from collections import Counter
from pathlib import Path
from typing import Any

SEMANTIC_TOKENS = {
    "WALLS": ("WALL", "WALLS", "A-WALL"),
    "DOORS": ("DOOR", "DOORS", "A-DOOR"),
    "WINDOWS": ("WINDOW", "WINDOWS", "A-WIND", "A-WINDOW"),
    "COLUMNS": ("COLUMN", "COLUMNS", "COL", "A-COLS", "A-COLUMN"),
}

def _value(entity: Any, key: str, default: Any = None) -> Any:
    dxf = getattr(entity, "dxf", None)
    if dxf is None: return default
    try: return dxf.get(key, default)
    except AttributeError:
        try: return dxf[key]
        except (KeyError, TypeError): return default

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

def extract_dwg_evidence(path: str | Path) -> dict[str, Any]:
    import ezdwg
    source = Path(path)
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    doc = ezdwg.read(str(source))
    entities = list(doc.modelspace().query())
    type_counts, layer_counts, block_counts = Counter(), Counter(), Counter()
    geometry_counts = Counter()
    text_evidence, dimension_evidence = [], []
    candidates = {k: [] for k in SEMANTIC_TOKENS}

    for entity in entities:
        dxftype = str(getattr(entity, "dxftype", "UNKNOWN"))
        type_counts[dxftype] += 1
        layer = _value(entity, "layer")
        if layer:
            layer_name = str(layer); layer_counts[layer_name] += 1
            for semantic in _token_hits(layer_name):
                candidates[semantic].append({"kind":"LAYER_NAME","value":layer_name,
                    "handle":int(getattr(entity,"handle",0)),"provenance":"DIRECT"})
        if dxftype in {"INSERT","MINSERT"}:
            name = _value(entity, "name")
            if name:
                block_name = str(name); block_counts[block_name] += 1
                for semantic in _token_hits(block_name):
                    candidates[semantic].append({"kind":"BLOCK_NAME","value":block_name,
                        "handle":int(getattr(entity,"handle",0)),"provenance":"DIRECT"})
        if dxftype in {"LINE","LWPOLYLINE","ARC","CIRCLE","ELLIPSE","SPLINE","HATCH"}:
            geometry_counts[dxftype] += 1
        if dxftype in {"TEXT","MTEXT","ATTRIB","ATTDEF"}:
            text_evidence.append({"handle":int(getattr(entity,"handle",0)),"type":dxftype,
                "text":str(getattr(entity,"text",None) or _value(entity,"text","")),
                "insert":_jsonable(_value(entity,"insert")),
                "rotation":_jsonable(_value(entity,"rotation")),"provenance":"DIRECT"})
        if dxftype == "DIMENSION":
            dimension_evidence.append({"handle":int(getattr(entity,"handle",0)),"type":dxftype,
                "text":str(_value(entity,"text","")),
                "actual_measurement":_jsonable(_value(entity,"actual_measurement")),
                "defpoint":_jsonable(_value(entity,"defpoint")),
                "defpoint2":_jsonable(_value(entity,"defpoint2")),
                "defpoint3":_jsonable(_value(entity,"defpoint3")),"provenance":"DIRECT"})

    semantic_support = {semantic:{
        "status":"SUPPORTED" if rows else "UNKNOWN",
        "provenance":"DIRECT" if rows else "UNKNOWN",
        "evidence":rows} for semantic,rows in candidates.items()}
    try:
        hv = doc.header_variables()
        header = {"extmin":_jsonable(hv.get("extmin")),"extmax":_jsonable(hv.get("extmax"))}
    except Exception:
        header = {}
    return {
        "schema":"dwg-semantic-evidence-v1",
        "source_profile":{"source_class":"ENGINEERING_PLAN","path":str(source),
            "sha256":source_sha256,"version":str(getattr(doc,"version","UNKNOWN")),
            "decode_version":str(getattr(doc,"decode_version","UNKNOWN")),
            "units":getattr(doc,"units",None),"provenance":"DIRECT"},
        "entity_counts":dict(sorted(type_counts.items())),
        "layer_counts":dict(sorted(layer_counts.items())),
        "block_counts":dict(sorted(block_counts.items())),
        "geometry_counts":dict(sorted(geometry_counts.items())),
        "text":text_evidence,"dimensions":dimension_evidence,
        "semantic_candidates":semantic_support,"header":header,
        "authority":{"read_only":True,"semantic_authority":False,
            "generic_linework_is_not_architectural_truth":True},
    }

def write_evidence(path: str | Path, output: str | Path) -> None:
    Path(output).write_text(json.dumps(extract_dwg_evidence(path),ensure_ascii=False,
        indent=2,sort_keys=True),encoding="utf-8")
