"""Conservative native DWG evidence extraction for drawing-standard checks."""
from __future__ import annotations
from pathlib import Path
from typing import Any
try:
    import ezdwg
except ImportError:  # pragma: no cover
    ezdwg = None

_CANONICAL_TITLE_TAGS={"TITLE","DRAWING_TITLE","DWG_TITLE","SCALE","SHEET","SHEET_NO","DATE","DRAWN","CHECKED","APPROVED","REV","REVISION"}
_VIEW_WORDS={"PLAN":"PLAN","PLANTA":"PLAN","SECTION":"SECTION","SECT":"SECTION","ELEVATION":"ELEVATION","ELEV":"ELEVATION"}

def _etype(entity: Any) -> str:
    value=getattr(entity,"dxftype","")
    try:
        value=value() if callable(value) else value
    except Exception:
        value=""
    return str(value).upper()

def _xy(value: Any):
    if value is None: return None
    try: return float(value[0]),float(value[1])
    except (TypeError,ValueError,IndexError,KeyError): return None

def _distance_point_segment(point,a,b):
    px,py=point; ax,ay=a; bx,by=b; dx,dy=bx-ax,by-ay; den=dx*dx+dy*dy
    if den<=1e-12: return ((px-ax)**2+(py-ay)**2)**0.5
    t=max(0.0,min(1.0,((px-ax)*dx+(py-ay)*dy)/den)); qx,qy=ax+t*dx,ay+t*dy
    return ((px-qx)**2+(py-qy)**2)**0.5

def _text(entity):
    dxf=getattr(entity,"dxf",{}) or {}
    return str(dxf.get("text",dxf.get("plain_text","")) or "").strip()

def _attr_records(entity):
    records=[]
    try:
        for attrib in (getattr(entity,"attribs",[]) or []):
            dxf=getattr(attrib,"dxf",{}) or {}
            tag=str(dxf.get("tag","")).strip().upper()
            if tag: records.append({"tag":tag,"value":str(dxf.get("text","") or "").strip(),"handle":getattr(attrib,"handle",None)})
    except Exception: return []
    return records

def _extract_geometry(entities):
    lines=[]; evidence=[]
    for entity in entities:
        if _etype(entity)!="LINE": continue
        dxf=getattr(entity,"dxf",{}) or {}; a,b=_xy(dxf.get("start")),_xy(dxf.get("end"))
        if a and b:
            handle=str(getattr(entity,"handle","")); lines.append((a[0],a[1],b[0],b[1],handle)); evidence.append(f"dwg-line-{handle}")
    return lines,evidence

def _dimension_evidence(entities,lines):
    dims=[]; unresolved=[]
    for entity in entities:
        if _etype(entity)!="DIMENSION": continue
        dxf=getattr(entity,"dxf",{}) or {}; handle=str(getattr(entity,"handle","")); points=[]
        for key in ("defpoint","defpoint2","defpoint3","defpoint4","insert"):
            p=_xy(dxf.get(key))
            if p and p not in points: points.append(p)
        measurement=dxf.get("actual_measurement",dxf.get("measurement"))
        try: measurement=float(measurement) if measurement is not None else None
        except (TypeError,ValueError): measurement=None
        matched=[]
        for p in points:
            nearest=min(((_distance_point_segment(p,(x0,y0),(x1,y1)),h) for x0,y0,x1,y1,h in lines),default=None)
            if nearest and nearest[0]<=1.0: matched.append({"point":list(p),"line_handle":nearest[1],"distance":round(nearest[0],6)})
        record={"dimension_id":f"DWG-DIM-{handle}","evidence_id":f"dwg-dimension-{handle}","definition_points":[list(p) for p in points],"measurement":measurement,"matched_geometry":matched,"status":"UNKNOWN"}
        dims.append(record)
        if len(points)<2 or len(matched)<2: unresolved.append(record["dimension_id"])
    return {"count":len(dims),"dimensions":dims,"dimensions_geometry_associated":True if dims and not unresolved else None,"unresolved":unresolved,"evidence_ids":[x["evidence_id"] for x in dims]}

def _view_evidence(entities,document):
    labels=[]
    for entity in entities:
        if _etype(entity) not in {"TEXT","MTEXT"}: continue
        value=_text(entity).upper()
        for token,normalized in _VIEW_WORDS.items():
            if token in value:
                labels.append({"text":_text(entity),"normalized":normalized,"handle":getattr(entity,"handle",None),"evidence_id":f"dwg-view-label-{getattr(entity,'handle','unknown')}"}); break
    layout_names=[]
    # Layout enumeration is optional; parser/version differences must not fail the whole extractor.
    try:
        layouts=document.layouts()
        for layout in layouts:
            name=str(getattr(layout,"name","") or "")
            if name: layout_names.append(name)
    except Exception: pass
    explicit=[name for name in layout_names if name.upper() not in {"MODEL","MODELSPACE"}]
    return {"labels":labels,"layout_names":layout_names,"explicit_layout_evidence":explicit,"view_section_identity":True if labels and explicit else None,"evidence_ids":[x["evidence_id"] for x in labels]}

def _title_block_evidence(entities):
    blocks=[]
    for entity in entities:
        if _etype(entity) not in {"INSERT","MINSERT"}: continue
        dxf=getattr(entity,"dxf",{}) or {}; name=str(dxf.get("name",dxf.get("block_name","")) or "")
        attrs=_attr_records(entity)
        if not attrs and not any(t in name.upper() for t in ("TITLE","TBLOCK","TITLEBLOCK","FRAME")): continue
        tags={a["tag"] for a in attrs}; matched=sorted(tags & _CANONICAL_TITLE_TAGS)
        blocks.append({"block":name,"handle":getattr(entity,"handle",None),"attributes":attrs,"recognized_tags":matched,"evidence_id":f"dwg-title-block-{getattr(entity,'handle','unknown')}"})
    return {"blocks":blocks,"title_block_fields_valid":True if blocks and any(len(x["recognized_tags"])>=3 for x in blocks) else None,"evidence_ids":[x["evidence_id"] for x in blocks]}

def cross_view_consistency(views):
    explicit=[v for v in views if v.get("identity") in {"PLAN","SECTION","ELEVATION"} and v.get("fingerprint")]
    if len(explicit)<2: return {"cross_view_consistent":None,"unresolved":["INSUFFICIENT_VIEW_CORRESPONDENCE"],"evidence_ids":[]}
    if any(v.get("correspondence_verified") is False for v in explicit):
        return {"cross_view_consistent":False,"unresolved":["VIEW_CORRESPONDENCE_CONTRADICTION"],"evidence_ids":[str(v["evidence_id"]) for v in explicit]}
    by_identity={}
    for v in explicit: by_identity.setdefault(v["identity"],set()).add(str(v["fingerprint"]))
    if any(len(fps)>1 for fps in by_identity.values()):
        return {"cross_view_consistent":False,"unresolved":["VIEW_CORRESPONDENCE_CONTRADICTION"],"evidence_ids":[str(v["evidence_id"]) for v in explicit]}
    if all(v.get("correspondence_verified") is True for v in explicit):
        return {"cross_view_consistent":True,"unresolved":[],"evidence_ids":[str(v["evidence_id"]) for v in explicit]}
    return {"cross_view_consistent":None,"unresolved":["INSUFFICIENT_VERIFIED_CORRESPONDENCE"],"evidence_ids":[str(v["evidence_id"]) for v in explicit]}

def _empty(reason):
    return {"dimensions_geometry_associated":None,"view_section_identity":None,"title_block_fields_valid":None,"cross_view_consistent":None,"dimension_evidence":{},"view_evidence":{},"title_block_evidence":{},"evidence_ids":[],"unresolved":[reason]}

def extract_native_drawing_evidence(source_path,input_type):
    if input_type!="DWG": return _empty("NATIVE_DWG_EVIDENCE_UNAVAILABLE")
    if ezdwg is None: return _empty("DWG_PARSER_UNAVAILABLE")
    try:
        document=ezdwg.read(str(Path(source_path))); entities=list(document.modelspace().query("LINE LWPOLYLINE ARC CIRCLE ELLIPSE POINT TEXT MTEXT DIMENSION INSERT MINSERT HATCH SPLINE"))
    except Exception as exc: return _empty(f"NATIVE_EVIDENCE_FAILED_CLOSED:{type(exc).__name__}")
    lines,line_evidence=_extract_geometry(entities)
    try: dimensions=_dimension_evidence(entities,lines)
    except Exception as exc: dimensions={"count":0,"dimensions":[],"dimensions_geometry_associated":None,"unresolved":[f"DIMENSION_EVIDENCE_FAILED:{type(exc).__name__}"],"evidence_ids":[]}
    try: views=_view_evidence(entities,document)
    except Exception as exc: views={"labels":[],"layout_names":[],"explicit_layout_evidence":[],"view_section_identity":None,"evidence_ids":[],"error":f"VIEW_EVIDENCE_FAILED:{type(exc).__name__}"}
    try: title=_title_block_evidence(entities)
    except Exception as exc: title={"blocks":[],"title_block_fields_valid":None,"evidence_ids":[],"error":f"TITLE_BLOCK_EVIDENCE_FAILED:{type(exc).__name__}"}
    unresolved=list(dimensions.get("unresolved",[]))
    if views.get("view_section_identity") is None: unresolved.append("VIEW_IDENTITY_UNCERTAIN")
    if title.get("title_block_fields_valid") is None: unresolved.append("TITLE_BLOCK_EVIDENCE_INCOMPLETE")
    return {"dimensions_geometry_associated":dimensions.get("dimensions_geometry_associated"),"view_section_identity":views.get("view_section_identity"),"title_block_fields_valid":title.get("title_block_fields_valid"),"cross_view_consistent":None,"dimension_evidence":dimensions,"view_evidence":views,"title_block_evidence":title,"evidence_ids":sorted(set(line_evidence+dimensions.get("evidence_ids",[])+views.get("evidence_ids",[])+title.get("evidence_ids",[]))),"unresolved":sorted(set(unresolved))}
