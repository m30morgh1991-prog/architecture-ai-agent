"""Evidence-backed space extraction result normalization (H64).

Keeps native geometry extraction deterministic and fail-closed. The result
records both explicit closed boundaries and line-derived faces when available;
it never assigns architectural room semantics from geometry alone.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.space_model_contract import build_space_model


@dataclass(frozen=True)
class SpaceExtractionResult:
    detector_id: str
    source_sha256: str
    spaces: tuple[dict[str, Any], ...]
    relations: tuple[dict[str, Any], ...]
    unresolved: tuple[str, ...]

    def validate(self) -> None:
        if not self.detector_id or not self.source_sha256:
            raise ValueError("SPACE_EXTRACTION_ID_OR_SOURCE_MISSING")
        if any(not item.get("space_id") for item in self.spaces):
            raise ValueError("SPACE_EXTRACTION_SPACE_ID_MISSING")
        if any(not item.get("evidence_ids") for item in self.spaces):
            raise ValueError("SPACE_EXTRACTION_SPACE_EVIDENCE_MISSING")
        if any(not item.get("relation_id") for item in self.relations):
            raise ValueError("SPACE_EXTRACTION_RELATION_ID_MISSING")
        expected = tuple(
            str(item["relation_id"])
            for item in self.relations
            if str(item.get("status", "UNKNOWN")) != "ACCESSIBLE"
        )
        if tuple(self.unresolved) != expected:
            raise ValueError("SPACE_EXTRACTION_UNRESOLVED_MISMATCH")

    def to_space_model(self):
        self.validate()
        return build_space_model(
            model_id=f"{self.detector_id}:{self.source_sha256[:12]}",
            source_sha256=self.source_sha256,
            spaces=list(self.spaces),
            relations=list(self.relations),
        )


def build_space_extraction_result(
    *,
    detector_id: str,
    source_sha256: str,
    spaces: list[dict[str, Any]],
    relations: list[dict[str, Any]],
) -> SpaceExtractionResult:
    result = SpaceExtractionResult(
        detector_id=detector_id,
        source_sha256=source_sha256,
        spaces=tuple(spaces),
        relations=tuple(relations),
        unresolved=tuple(
            str(item["relation_id"])
            for item in relations
            if str(item.get("status", "UNKNOWN")) != "ACCESSIBLE"
        ),
    )
    result.validate()
    # Force the typed contract validation before returning raw evidence.
    result.to_space_model()
    return result
