"""Runtime integration helper for scale/unit evidence.

This adapter keeps scale decisions deterministic and fail-closed. It accepts the
different evidence forms produced by drawing metadata, DWG headers, and dimension
inspection without coupling the Rule Engine to a particular CAD provider.
"""
from __future__ import annotations
from .scale_unit_evidence import ScaleEvidence, evaluate_scale_evidence

def evaluate_runtime_scale(*, source_id: str, declared_unit=None, header_unit=None,
                           dimension_unit=None, metadata_unit=None, evidence_ids=()):
    explicit = declared_unit or dimension_unit
    header = header_unit
    dimension = bool(dimension_unit)
    metadata = bool(metadata_unit)
    resolved_unit = explicit or header or metadata_unit or "UNKNOWN"
    return evaluate_scale_evidence(
        source_id=source_id,
        unit=resolved_unit,
        explicit_unit=explicit,
        header_unit=header,
        dimension_evidence=dimension,
        source_metadata=metadata,
        evidence_ids=tuple(evidence_ids),
    )
