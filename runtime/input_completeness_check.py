"""Input completeness / drawing-health check.

Runs before any understanding or editing. It reads only metadata that an
upstream extractor already produced (for example the dict returned by
``drawing_metadata_extractor.extract_drawing_standard_metadata``) and never
infers a missing value:

* value missing            -> SOURCE_REQUIRED
* value explicitly False   -> BLOCKED
* raster-grade geometry    -> NEEDS_REVIEW (raster is not reliable geometry)
* drawing authored in inch -> NEEDS_REVIEW (confirm the plotting-scale conversion)
"""
from __future__ import annotations

from typing import Any, Mapping

from runtime.input_source_contract import SourceProfile
from runtime.review_report_contract import Finding

# (check_id, metadata_key, kind, label)
_REQUIRED = (
    ("INPUT-SCALE-001", "scale", "text", "Drawing scale"),
    ("INPUT-UNITS-001", "units", "text", "Drawing units"),
    ("INPUT-DIM-001", "dimensions_geometry_associated", "flag", "Dimensions associated with geometry"),
    ("INPUT-VIEW-001", "view_section_identity", "flag", "View/section identity"),
    ("INPUT-SHEET-001", "sheet_layout_valid", "flag", "Sheet layout"),
    ("INPUT-TITLE-001", "title_block_fields_valid", "flag", "Title block fields"),
)
_INCH_UNITS = {"in", "inch", "inches"}


def check_input_completeness(
    *,
    source_sha256: str,
    source_profile: SourceProfile,
    metadata: Mapping[str, Any] | None = None,
    evidence_ids: tuple[str, ...] | list[str] = (),
) -> tuple[Finding, ...]:
    if len(source_sha256) != 64:
        raise ValueError("INPUT_COMPLETENESS_SOURCE_INVALID")
    metadata = metadata or {}
    evidence = tuple(str(e) for e in evidence_ids if e) or (f"source:{source_sha256}",)
    findings: list[Finding] = []

    for check_id, key, kind, label in _REQUIRED:
        value = metadata.get(key)
        if kind == "text":
            present = isinstance(value, str) and bool(value.strip())
            if present:
                status, severity, text = "PASS", "INFO", f"{label} supplied: {value.strip()}."
            else:
                status, severity, text = (
                    "SOURCE_REQUIRED", "WARNING", f"{label} not supplied; it is not inferred.",
                )
        else:
            if value is True:
                status, severity, text = "PASS", "INFO", f"{label} confirmed by evidence."
            elif value is False:
                status, severity, text = "BLOCKED", "BLOCKING", f"{label} contradicted by evidence."
            else:
                status, severity, text = (
                    "SOURCE_REQUIRED", "WARNING", f"{label} not supplied; it is not inferred.",
                )
        findings.append(
            Finding(
                finding_id=f"IN:{check_id}",
                category="COMPLETENESS",
                check_id=check_id,
                status=status,
                severity=severity,
                message=text,
                evidence_ids=evidence,
            )
        )

    rank = source_profile.geometry_trust_rank
    if rank >= 3:
        status, severity, text = "PASS", "INFO", "Source has vector geometry (trust rank %d)." % rank
    elif rank > 0:
        status, severity, text = (
            "NEEDS_REVIEW", "WARNING",
            "Raster source (trust rank %d): geometry is not reliable on its own." % rank,
        )
    else:
        status, severity, text = (
            "SOURCE_REQUIRED", "WARNING",
            "Source representation unknown; inspection evidence is required.",
        )
    findings.append(
        Finding(
            finding_id="IN:INPUT-TRUST-001",
            category="COMPLETENESS",
            check_id="INPUT-TRUST-001",
            status=status,
            severity=severity,
            message=text,
            evidence_ids=evidence,
        )
    )

    units = metadata.get("units")
    if isinstance(units, str) and units.strip().lower() in _INCH_UNITS:
        findings.append(
            Finding(
                finding_id="IN:INPUT-INCH-001",
                category="COMPLETENESS",
                check_id="INPUT-INCH-001",
                status="NEEDS_REVIEW",
                severity="WARNING",
                message="Drawing units are inches; confirm the scale used for centimetre plotting.",
                evidence_ids=evidence,
            )
        )
    return tuple(findings)
