"""H62 evidence-backed space model contract.

Space extraction is not approval-grade semantics by itself. This contract
keeps room geometry, labels, room numbers, schedule mappings, and spatial
relations traceable and fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SpaceStatus = Literal["UNKNOWN", "ACCESSIBLE", "BLOCKED"]
SpaceIdentityStatus = Literal["EXPLICIT", "SCHEDULE_MAPPED", "INFERRED", "CONFLICT", "UNKNOWN"]
RelationType = Literal[
    "SHARED_BOUNDARY", "CONTAINS", "OVERLAPS", "DISCONNECTED",
    "CONNECTED_BY_OPENING", "OPENING_CONNECTIVITY_UNKNOWN",
]


@dataclass(frozen=True)
class SpaceRecord:
    space_id: str
    boundary_handle: str
    bbox: tuple[float, float, float, float]
    centroid: tuple[float, float]
    area: float
    label: str | None
    evidence_ids: tuple[str, ...]
    status: SpaceStatus = "UNKNOWN"
    name: str | None = None
    number: str | None = None
    schedule_name: str | None = None
    schedule_number: str | None = None
    identity_status: SpaceIdentityStatus = "UNKNOWN"

    @property
    def resolved_name(self) -> str | None:
        """Use explicit plan/schedule identity; do not replace it with a guess."""
        if self.identity_status == "CONFLICT":
            return None
        return self.name or self.schedule_name or self.label

    @property
    def resolved_number(self) -> str | None:
        if self.identity_status == "CONFLICT":
            return None
        return self.number or self.schedule_number

    def validate(self) -> None:
        if not self.space_id or not self.boundary_handle:
            raise ValueError("SPACE_ID_OR_BOUNDARY_MISSING")
        if len(self.bbox) != 4 or len(self.centroid) != 2:
            raise ValueError("SPACE_GEOMETRY_INVALID")
        x0, y0, x1, y1 = self.bbox
        if x1 <= x0 or y1 <= y0:
            raise ValueError("SPACE_BBOX_INVALID")
        if self.area <= 0:
            raise ValueError("SPACE_AREA_INVALID")
        if not self.evidence_ids:
            raise ValueError("SPACE_EVIDENCE_MISSING")
        if self.status not in {"UNKNOWN", "ACCESSIBLE", "BLOCKED"}:
            raise ValueError("SPACE_STATUS_INVALID")
        if self.identity_status not in {
            "EXPLICIT", "SCHEDULE_MAPPED", "INFERRED", "CONFLICT", "UNKNOWN"
        }:
            raise ValueError("SPACE_IDENTITY_STATUS_INVALID")


@dataclass(frozen=True)
class SpaceRelation:
    relation_id: str
    relation_type: RelationType
    from_space_id: str | None
    to_space_id: str | None
    evidence_ids: tuple[str, ...]
    status: SpaceStatus = "UNKNOWN"

    def validate(self) -> None:
        if not self.relation_id:
            raise ValueError("SPACE_RELATION_ID_MISSING")
        if self.relation_type not in {
            "SHARED_BOUNDARY", "CONTAINS", "OVERLAPS", "DISCONNECTED",
            "CONNECTED_BY_OPENING", "OPENING_CONNECTIVITY_UNKNOWN",
        }:
            raise ValueError("SPACE_RELATION_TYPE_INVALID")
        if self.relation_type == "OPENING_CONNECTIVITY_UNKNOWN":
            if self.from_space_id is not None or self.to_space_id is not None:
                raise ValueError("UNRESOLVED_OPENING_ENDPOINTS_MUST_BE_NULL")
        elif not self.from_space_id or not self.to_space_id:
            raise ValueError("SPACE_RELATION_ENDPOINT_MISSING")
        if not self.evidence_ids:
            raise ValueError("SPACE_RELATION_EVIDENCE_MISSING")
        if self.status not in {"UNKNOWN", "ACCESSIBLE", "BLOCKED"}:
            raise ValueError("SPACE_STATUS_INVALID")


@dataclass(frozen=True)
class SpaceModel:
    model_id: str
    source_sha256: str
    spaces: tuple[SpaceRecord, ...]
    relations: tuple[SpaceRelation, ...]
    unresolved: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.model_id or not self.source_sha256:
            raise ValueError("SPACE_MODEL_ID_OR_SOURCE_MISSING")
        ids = {space.space_id for space in self.spaces}
        if len(ids) != len(self.spaces):
            raise ValueError("SPACE_ID_DUPLICATE")
        for space in self.spaces:
            space.validate()
        relation_ids = {relation.relation_id for relation in self.relations}
        if len(relation_ids) != len(self.relations):
            raise ValueError("SPACE_RELATION_ID_DUPLICATE")
        for relation in self.relations:
            relation.validate()
            if relation.from_space_id and relation.from_space_id not in ids:
                raise ValueError("SPACE_RELATION_SOURCE_UNKNOWN")
            if relation.to_space_id and relation.to_space_id not in ids:
                raise ValueError("SPACE_RELATION_TARGET_UNKNOWN")


def build_space_model(
    *,
    model_id: str,
    source_sha256: str,
    spaces: list[dict],
    relations: list[dict],
) -> SpaceModel:
    records = tuple(
        SpaceRecord(
            space_id=str(item["space_id"]),
            boundary_handle=str(item["boundary_handle"]),
            bbox=tuple(float(x) for x in item["bbox"]),
            centroid=tuple(float(x) for x in item["centroid"]),
            area=float(item["area"]),
            label=item.get("label"),
            evidence_ids=tuple(str(x) for x in item.get("evidence_ids", [])),
            status=str(item.get("status", "UNKNOWN")),
            name=item.get("name"),
            number=str(item["number"]) if item.get("number") is not None else None,
            schedule_name=item.get("schedule_name"),
            schedule_number=(
                str(item["schedule_number"])
                if item.get("schedule_number") is not None else None
            ),
            identity_status=str(item.get("identity_status", "UNKNOWN")),
        )
        for item in spaces
    )
    relation_records = tuple(
        SpaceRelation(
            relation_id=str(item["relation_id"]),
            relation_type=str(item["type"]),
            from_space_id=item.get("from"),
            to_space_id=item.get("to"),
            evidence_ids=tuple(str(x) for x in item.get("evidence_ids", [])),
            status=str(item.get("status", "UNKNOWN")),
        )
        for item in relations
    )
    model = SpaceModel(
        model_id=model_id,
        source_sha256=source_sha256,
        spaces=records,
        relations=relation_records,
        unresolved=tuple(
            r.relation_id for r in relation_records
            if r.status != "ACCESSIBLE"
        ),
    )
    model.validate()
    return model
