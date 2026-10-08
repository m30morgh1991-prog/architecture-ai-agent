"""Normalize read-only DWG evidence into the canonical DrawingEvidence contract.

This bridge creates source-bound evidence records only. It never promotes a
candidate directly into PlanModel truth; reconciliation remains the authority.
"""
from __future__ import annotations

import hashlib
from typing import Any

from runtime.drawing_semantic_evidence import DrawingEvidenceSet, build_drawing_evidence_set


def _evidence_id(source_sha256: str, kind: str, subject: str, ordinal: int) -> str:
    payload = f"{source_sha256}:{kind}:{subject}:{ordinal}".encode("utf-8")
    return "dwg:" + hashlib.sha256(payload).hexdigest()[:24]


def normalize_dwg_evidence(raw: dict[str, Any]) -> DrawingEvidenceSet:
    source = raw.get("source_profile") or {}
    source_sha256 = str(source.get("sha256", ""))
    if len(source_sha256) != 64:
        raise ValueError("DWG_EVIDENCE_SOURCE_SHA_MISSING")

    records: list[dict[str, Any]] = []
    ordinal = 0

    for semantic, payload in sorted((raw.get("semantic_candidates") or {}).items()):
        for candidate in payload.get("evidence") or ():
            ordinal += 1
            subject = str(candidate.get("handle", "UNKNOWN"))
            records.append({
                "evidence_id": _evidence_id(source_sha256, "semantic", semantic, ordinal),
                "source_sha256": source_sha256,
                "domain": "STRUCTURE" if semantic == "COLUMNS" else "SYMBOL",
                "subject_id": f"{semantic}:{subject}",
                "predicate": "architectural_element_candidate",
                "value": semantic,
                "status": "SUPPORTED",
                "confidence": 1.0,
                "source_ref": f"dwg:{source_sha256}:entity:{subject}",
                "notes": f"direct CAD {candidate.get('kind', 'evidence')}",
            })

    for item in raw.get("text") or ():
        ordinal += 1
        handle = str(item.get("handle", "UNKNOWN"))
        value = str(item.get("text", ""))
        records.append({
            "evidence_id": _evidence_id(source_sha256, "text", handle, ordinal),
            "source_sha256": source_sha256,
            "domain": "TEXT",
            "subject_id": f"TEXT:{handle}",
            "predicate": "text_content",
            "value": value,
            "status": "SUPPORTED" if value else "UNKNOWN",
            "confidence": 1.0 if value else 0.0,
            "source_ref": f"dwg:{source_sha256}:entity:{handle}",
            "notes": "direct CAD text evidence",
        })

    for item in raw.get("dimensions") or ():
        ordinal += 1
        handle = str(item.get("handle", "UNKNOWN"))
        measurement = item.get("actual_measurement")
        value = str(measurement if measurement is not None else item.get("text", ""))
        records.append({
            "evidence_id": _evidence_id(source_sha256, "dimension", handle, ordinal),
            "source_sha256": source_sha256,
            "domain": "DIMENSION",
            "subject_id": f"DIMENSION:{handle}",
            "predicate": "dimension_value",
            "value": value or "UNKNOWN",
            "status": "SUPPORTED" if measurement is not None else "UNKNOWN",
            "confidence": 1.0 if measurement is not None else 0.0,
            "source_ref": f"dwg:{source_sha256}:entity:{handle}",
            "notes": "direct CAD dimension evidence",
        })

    return build_drawing_evidence_set(
        set_id=f"dwg:{source_sha256}",
        source_sha256=source_sha256,
        records=records,
    )
