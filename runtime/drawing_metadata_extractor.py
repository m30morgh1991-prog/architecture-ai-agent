"""Conservative extraction of drawing-standard evidence from real artifacts.

This module extracts evidence only; it does not infer compliance where the
artifact does not contain enough information.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import fitz

from .native_drawing_evidence import extract_native_drawing_evidence

try:
    import ezdwg
except ImportError:  # pragma: no cover
    ezdwg = None

_SCALE_RE = re.compile(r"(?i)\b(?:SCALE|ESCALA)\s*[:=]?\s*(1\s*[:/]\s*\d+)\b")
_UNIT_RE = re.compile(r"(?i)\b(mm|cm|m|in|ft|inch|feet|meter|metre|centimeter|millimeter)\b")
_DWG_UNITS = {1:"in",2:"ft",3:"mi",4:"mm",5:"cm",6:"m",7:"km",8:"microinch",9:"mil",10:"yd",11:"angstrom",12:"nm",13:"micron",14:"dm",15:"dam",16:"hm",17:"gm",18:"au",19:"pc",20:"ly",21:"us_survey_ft"}

def _parse_text(text: str) -> dict[str, Any]:
    scale_match = _SCALE_RE.search(text or "")
    unit_matches = sorted(set(m.group(1).lower() for m in _UNIT_RE.finditer(text or "")))
    return {"scale": scale_match.group(1).replace(" ","") if scale_match else None,
            "text_units": unit_matches,
            "scale_units_consistent": bool(scale_match and unit_matches),
            "scale_evidence": "text-scale" if scale_match else None,
            "unit_evidence": "text-units" if unit_matches else None}

def extract_drawing_standard_metadata(source_path: str, input_type: str, *, artifact_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    path = Path(source_path)
    evidence_ids: list[str] = []
    result: dict[str, Any] = {"scale":None,"units":None,"scale_units_consistent":None,
        "dimensions_geometry_associated":None,"view_section_identity":None,
        "sheet_layout_valid":None,"title_block_fields_valid":None,"cross_view_consistent":None,
        "evidence_ids":evidence_ids,"notes":[]}
    if input_type == "PDF":
        document = fitz.open(path)
        parsed = _parse_text("\n".join(page.get_text() for page in document))
        result.update(parsed)
        if parsed["scale_evidence"]: evidence_ids.append(parsed["scale_evidence"])
        if parsed["unit_evidence"]: evidence_ids.append(parsed["unit_evidence"])
        if document.page_count:
            page=document[0]
            result["sheet_size_points"]=[float(page.rect.width),float(page.rect.height)]
            result["notes"].append("Page size is extracted, but ISO 5457 sheet-layout compliance is not inferred.")
        return result
    if input_type != "DWG":
        result["notes"].append("No native metadata extractor for this input type.")
        return result
    if ezdwg is None:
        result["notes"].append("DWG parser unavailable; native metadata remains UNKNOWN.")
        return result
    try:
        document=ezdwg.read(str(path))
        header=document.header_variables()
        raw_units=header.get("insunits",header.get("$INSUNITS",0))
        try: raw_units=int(raw_units)
        except (TypeError,ValueError): raw_units=0
        result["units"]=_DWG_UNITS.get(raw_units)
        if result["units"]: evidence_ids.append("dwg-$INSUNITS")
        elif raw_units==0: result["notes"].append("DWG $INSUNITS is unitless/unspecified; no unit is inferred.")
        payload=artifact_payload or {}
        result["extents"]=[payload.get("extmin"),payload.get("extmax")]
        texts=[]; dimension_count=0; insert_count=0
        for entity in document.modelspace().query():
            dxftype=str(getattr(entity,"dxftype",lambda:"")()).upper()
            if dxftype in {"TEXT","MTEXT"}: texts.append(str(getattr(entity,"text","") or ""))
            elif dxftype=="DIMENSION": dimension_count+=1
            elif dxftype=="INSERT": insert_count+=1
        parsed=_parse_text("\n".join(texts))
        result["scale"]=parsed["scale"]; result["scale_evidence"]=parsed["scale_evidence"]; result["text_units"]=parsed["text_units"]
        if parsed["scale_evidence"]: evidence_ids.append("dwg-text-scale")
        if parsed["unit_evidence"]: evidence_ids.append("dwg-text-units")
        result["scale_units_consistent"]=True if result["scale"] and result["units"] else None
        result["dimension_entity_count"]=dimension_count; result["insert_entity_count"]=insert_count
        if dimension_count: result["notes"].append("DIMENSION entities detected; geometric association is delegated to native evidence.")
        if insert_count: result["notes"].append("INSERT entities detected; title-block validity is delegated to native evidence.")
        native=extract_native_drawing_evidence(str(path),input_type)
        for key in ("dimensions_geometry_associated","view_section_identity","title_block_fields_valid","cross_view_consistent"):
            result[key]=native.get(key)
        result["native_drawing_evidence"]=native
        evidence_ids.extend(native.get("evidence_ids",[]))
        result["notes"].extend(f"Native evidence unresolved: {item}." for item in native.get("unresolved",[]))
        return result
    except Exception as exc:
        result["notes"].append(f"Native metadata extraction failed closed: {type(exc).__name__}.")
        return result
