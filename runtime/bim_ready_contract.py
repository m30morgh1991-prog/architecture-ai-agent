"""BIM-ready semantic contracts for the architectural PlanModel core.

This is intentionally not a full IFC/BIM implementation. It preserves the
minimum semantic identity, attributes, hierarchy and relationships needed to
evolve PlanModel into a richer building-information model without making BIM
a dependency of the MVP.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BIMElementIdentity:
    """Stable semantic identity for a plan element."""

    category: str
    ifc_class: str | None = None
    name: str | None = None
    level_id: str | None = None
    parent_id: str | None = None
    properties: tuple[tuple[str, Any], ...] = ()
    external_refs: tuple[tuple[str, str], ...] = ()

    def validate(self) -> None:
        if not self.category.strip():
            raise ValueError("BIM_CATEGORY_MISSING")
        if self.ifc_class is not None and not self.ifc_class.strip():
            raise ValueError("BIM_IFC_CLASS_INVALID")
        if self.level_id is not None and not self.level_id.strip():
            raise ValueError("BIM_LEVEL_ID_INVALID")
        if self.parent_id is not None and not self.parent_id.strip():
            raise ValueError("BIM_PARENT_ID_INVALID")
        keys = [key for key, _ in self.properties]
        if any(not key.strip() for key in keys):
            raise ValueError("BIM_PROPERTY_KEY_INVALID")
        if len(keys) != len(set(keys)):
            raise ValueError("BIM_PROPERTY_KEY_DUPLICATE")
        refs = [key for key, _ in self.external_refs]
        if any(not key.strip() or not value.strip() for key, value in self.external_refs):
            raise ValueError("BIM_EXTERNAL_REF_INVALID")
        if len(refs) != len(set(refs)):
            raise ValueError("BIM_EXTERNAL_REF_KEY_DUPLICATE")


@dataclass(frozen=True)
class BIMElementRelation:
    """Evidence-free graph edge; evidence remains owned by PlanModel elements."""

    relation_type: str
    source_id: str
    target_id: str

    def validate(self) -> None:
        if not self.relation_type.strip():
            raise ValueError("BIM_RELATION_TYPE_MISSING")
        if not self.source_id or not self.target_id:
            raise ValueError("BIM_RELATION_ENDPOINT_MISSING")
        if self.source_id == self.target_id:
            raise ValueError("BIM_SELF_RELATION")


def validate_bim_graph(
    element_ids: set[str],
    relations: tuple[BIMElementRelation, ...],
) -> None:
    seen: set[tuple[str, str, str]] = set()
    for relation in relations:
        relation.validate()
        if relation.source_id not in element_ids or relation.target_id not in element_ids:
            raise ValueError("BIM_RELATION_ENDPOINT_UNKNOWN")
        key = (relation.relation_type, relation.source_id, relation.target_id)
        if key in seen:
            raise ValueError("BIM_RELATION_DUPLICATE")
        seen.add(key)
