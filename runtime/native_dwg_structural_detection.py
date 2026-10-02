"""Native DWG structural candidate extraction with fail-closed promotion."""
from __future__ import annotations
from dataclasses import dataclass

_FIXED={"COLUMNS","WALLS","DOORS","WINDOWS","OUTER_BOUNDARY","OVERALL_PLAN_FORM"}

@dataclass(frozen=True)
class DWGCandidate:
    candidate_id:str
    element_type:str
    evidence_ids:tuple[str,...]
    signals:tuple[str,...]
    confidence:float
    status:str
    geometry:dict

def _norm(v): return str(v or "").strip().upper().replace(" ","_").replace("-","_")

def classify_dwg_entity(entity, index:int):
    """Classify from independent native-DWG signals without assuming semantics."""
    dtype = _norm(entity.get("type"))
    layer = _norm(entity.get("layer"))
    block = _norm(entity.get("block"))
    signals=[]
    kind=None
    text=f"{layer} {block}"
    if any(x in text for x in ("COLUMN","COL_","STRUCT","PILLAR")):
        kind="COLUMNS"; signals.append("layer_or_block_semantics")
    elif "WALL" in text:
        kind="WALLS"; signals.append("layer_semantics")
    elif "DOOR" in text:
        kind="DOORS"; signals.append("layer_or_block_semantics")
    elif "WINDOW" in text or "WIN_" in text:
        kind="WINDOWS"; signals.append("layer_or_block_semantics")
    if dtype in {"INSERT","BLOCK_REFERENCE"} and block:
        signals.append("native_block_identity")
    if entity.get("closed") or entity.get("geometry_closed"):
        signals.append("closed_geometry")
    if entity.get("topology_neighbor_count",0):
        signals.append("topology")
    if not kind:
        return None
    independent=len(set(signals))
    status="LOCKED" if independent>=3 else ("NEEDS_REVIEW" if independent>=2 else "UNKNOWN")
    confidence={1:.70,2:.90,3:.95}.get(min(independent,3),.95)
    return DWGCandidate(f"DWG-{index:05d}",kind,tuple(entity.get("evidence_ids",())),tuple(signals),confidence,status,dict(entity.get("geometry") or {}))

def detect_native_dwg_candidates(entities):
    out=[]
    for i,e in enumerate(entities):
        c=classify_dwg_entity(e,i)
        if c: out.append(c)
    return tuple(out)

def promote_candidates(candidates, contradiction_ids=()):
    if contradiction_ids:
        return tuple(DWGCandidate(c.candidate_id,c.element_type,c.evidence_ids,c.signals,c.confidence,"BLOCKED",c.geometry) for c in candidates)
    return tuple(candidates)
