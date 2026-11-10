"""Validate source-bound JSON evidence exported by the AutoCAD .NET adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from runtime.cad_adapter_contract import CADInspectionEvidence

SCHEMA = "autodesk-autocad-readonly-evidence-v1"
ADAPTER_ID = "autodesk-autocad-dotnet-readonly-v1"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_autodesk_export(export_path: str | Path, source_path: str | Path) -> CADInspectionEvidence:
    """Validate export identity/invariants; never promote CAD data to semantics."""
    export_file, source_file = Path(export_path), Path(source_path)
    if not export_file.is_file() or not source_file.is_file():
        return CADInspectionEvidence(ADAPTER_ID, "", {"error": "SOURCE_OR_EXPORT_MISSING"}, "BLOCKED")
    try:
        data: dict[str, Any] = json.loads(export_file.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        return CADInspectionEvidence(ADAPTER_ID, "", {"error": "AUTODESK_EXPORT_INVALID_JSON"}, "BLOCKED")
    if data.get("schema") != SCHEMA:
        return CADInspectionEvidence(ADAPTER_ID, "", {"error": "AUTODESK_EXPORT_SCHEMA_UNSUPPORTED"}, "BLOCKED")

    profile, integrity = data.get("source_profile"), data.get("source_integrity")
    authority, scope = data.get("authority"), data.get("scope")
    entities, layers = data.get("entities"), data.get("layers")
    if not all(isinstance(x, dict) for x in (profile, integrity, authority, scope)):
        return CADInspectionEvidence(ADAPTER_ID, "", {"error": "AUTODESK_EXPORT_ENVELOPE_INCOMPLETE"}, "BLOCKED")
    if not isinstance(entities, list) or not isinstance(layers, list):
        return CADInspectionEvidence(ADAPTER_ID, "", {"error": "AUTODESK_EXPORT_COLLECTION_INVALID"}, "BLOCKED")
    if not all(isinstance(x, dict) and x.get("handle") and x.get("type") and x.get("layer") is not None for x in entities):
        return CADInspectionEvidence(ADAPTER_ID, "", {"error": "AUTODESK_ENTITY_RECORD_INVALID"}, "BLOCKED")

    before, after, source_sha = integrity.get("sha256_before"), integrity.get("sha256_after"), profile.get("sha256")
    if not all(isinstance(x, str) and len(x) == 64 for x in (before, after, source_sha)):
        return CADInspectionEvidence(ADAPTER_ID, "", {"error": "AUTODESK_SOURCE_HASH_MISSING"}, "BLOCKED")
    actual = _sha256(source_file)
    if before != after or before != source_sha or actual != source_sha:
        return CADInspectionEvidence(ADAPTER_ID, actual, {"error": "AUTODESK_SOURCE_SHA_MISMATCH", "expected_sha256": source_sha, "sha256_before": before, "sha256_after": after, "actual_sha256": actual}, "BLOCKED")
    if integrity.get("source_mutated") is not False or authority.get("read_only") is not True:
        return CADInspectionEvidence(ADAPTER_ID, actual, {"error": "AUTODESK_READ_ONLY_INVARIANT_FAILED"}, "BLOCKED")
    if authority.get("semantic_authority") is not False or authority.get("compliance_assessed") is not False:
        return CADInspectionEvidence(ADAPTER_ID, actual, {"error": "AUTODESK_AUTHORITY_BOUNDARY_VIOLATION"}, "BLOCKED")

    payload = {"schema": SCHEMA, "source_profile": profile, "source_integrity": integrity, "scope": scope, "layers": layers, "entities": entities, "authority": authority, "semantic_promotion": "NOT_PERMITTED"}
    status = "NEEDS_REVIEW" if integrity.get("snapshot_binding_status") != "VERIFIED" or str(profile.get("insunits", "")).upper() in {"", "UNITLESS", "UNKNOWN"} else "READY"
    result = CADInspectionEvidence(ADAPTER_ID, actual, payload, status)
    result.validate(actual)
    return result
