"""Read-only structural and supported-geometry comparison for two DXF files.

This comparator is deliberately conservative. It does not establish DWG-to-DXF
fidelity, and unsupported entity types keep the result incomplete.
"""
from __future__ import annotations

import hashlib
import math
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import ezdxf
from ezdxf import DXFError

from .dxf_advanced import advanced_entity_signature, insert_attributes_signature, presentation_signature


COMPARATOR_VERSION = "0.9.0"


@dataclass(frozen=True)
class DxfComparisonReport:
    source_path: str
    candidate_path: str
    comparison_status: str
    geometry_comparison_status: str
    fidelity_status: str
    requires_review: bool
    source_sha256: str | None = None
    candidate_sha256: str | None = None
    ezdxf_version: str | None = None
    comparator_version: str = COMPARATOR_VERSION
    source_entity_counts: dict[str, int] = field(default_factory=dict)
    candidate_entity_counts: dict[str, int] = field(default_factory=dict)
    source_layers: list[str] = field(default_factory=list)
    candidate_layers: list[str] = field(default_factory=list)
    source_layer_properties: dict[str, dict[str, Any]] = field(default_factory=dict)
    candidate_layer_properties: dict[str, dict[str, Any]] = field(default_factory=dict)
    source_blocks: list[str] = field(default_factory=list)
    candidate_blocks: list[str] = field(default_factory=list)
    source_block_entity_counts: dict[str, int] = field(default_factory=dict)
    candidate_block_entity_counts: dict[str, int] = field(default_factory=dict)
    source_layouts: list[str] = field(default_factory=list)
    candidate_layouts: list[str] = field(default_factory=list)
    source_text_styles: dict[str, Any] = field(default_factory=dict)
    candidate_text_styles: dict[str, Any] = field(default_factory=dict)
    source_dimension_styles: dict[str, Any] = field(default_factory=dict)
    candidate_dimension_styles: dict[str, Any] = field(default_factory=dict)
    source_layout_properties: dict[str, Any] = field(default_factory=dict)
    candidate_layout_properties: dict[str, Any] = field(default_factory=dict)
    source_viewport_properties: dict[str, Any] = field(default_factory=dict)
    candidate_viewport_properties: dict[str, Any] = field(default_factory=dict)
    source_ucs_properties: dict[str, Any] = field(default_factory=dict)
    candidate_ucs_properties: dict[str, Any] = field(default_factory=dict)
    source_extents: dict[str, Any] = field(default_factory=dict)
    candidate_extents: dict[str, Any] = field(default_factory=dict)
    source_coordinate_metadata: dict[str, Any] = field(default_factory=dict)
    candidate_coordinate_metadata: dict[str, Any] = field(default_factory=dict)
    source_insunits: int | None = None
    candidate_insunits: int | None = None
    source_measurement: int | None = None
    candidate_measurement: int | None = None
    geometry_mismatch_count: int = 0
    text_mismatch_count: int = 0
    viewport_mismatch_count: int = 0
    entity_metadata_mismatch_count: int = 0
    source_proxy_graphics: list[dict[str, Any]] = field(default_factory=list)
    candidate_proxy_graphics: list[dict[str, Any]] = field(default_factory=list)
    proxy_graphic_mismatch_count: int = 0
    source_proxy_object_count: int = 0
    candidate_proxy_object_count: int = 0
    unsupported_entity_types: list[str] = field(default_factory=list)
    structural_differences: list[str] = field(default_factory=list)
    error_code: str | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DxfComparator:
    """Compare two DXF artifacts without modifying either file."""

    def compare(
        self,
        source_path: str | Path,
        candidate_path: str | Path,
        *,
        tolerance: float = 1e-6,
    ) -> DxfComparisonReport:
        source = Path(source_path).expanduser().resolve()
        candidate = Path(candidate_path).expanduser().resolve()
        if not math.isfinite(tolerance) or tolerance <= 0:
            raise ValueError("DXF_COMPARISON_TOLERANCE_INVALID")
        if source == candidate:
            return self._failure(source, candidate, "INPUT_PATH_COLLISION", "Source and candidate must be different files.")
        for path in (source, candidate):
            if path.suffix.lower() != ".dxf":
                return self._failure(source, candidate, "DXF_INPUT_REQUIRED", "Both inputs must have .dxf extensions.")
            if not path.is_file():
                return self._failure(source, candidate, "SOURCE_REQUIRED", "Both DXF input files must exist.")
            try:
                if path.stat().st_size == 0:
                    return self._failure(source, candidate, "DXF_EMPTY", "An input DXF file is empty.")
            except OSError:
                return self._failure(source, candidate, "SOURCE_UNREADABLE", "An input DXF file cannot be inspected.")

        try:
            source_sha256 = cls_sha256_file(source)
            candidate_sha256 = cls_sha256_file(candidate)
            ezdxf_version = getattr(ezdxf, "__version__", None)
            source_doc, source_recovered = self._read_document(source)
            candidate_doc, candidate_recovered = self._read_document(candidate)
        except Exception as exc:
            return self._failure(
                source,
                candidate,
                "DXF_PARSE_FAILED",
                f"At least one DXF could not be parsed or recovered ({type(exc).__name__}).",
            )

        source_entities, source_blocks, source_block_inventory, source_metadata, source_unsupported = self._collect(source_doc, tolerance)
        candidate_entities, candidate_blocks, candidate_block_inventory, candidate_metadata, candidate_unsupported = self._collect(candidate_doc, tolerance)
        if source_recovered:
            source_unsupported.add("DXF_RECOVERY_USED")
        if candidate_recovered:
            candidate_unsupported.add("DXF_RECOVERY_USED")
        geometry_exclusions = {"TEXT", "MTEXT", "ATTRIB", "ATTDEF", "VIEWPORT"}
        geometry_mismatches = self._counter_delta(source_entities, candidate_entities, exclude_types=geometry_exclusions)
        block_mismatches = self._counter_delta(source_blocks, candidate_blocks, exclude_types=geometry_exclusions)
        block_inventory_mismatches = self._counter_delta(source_block_inventory, candidate_block_inventory, exclude_types=geometry_exclusions)
        text_types = {"TEXT", "MTEXT", "ATTRIB", "ATTDEF"}
        text_mismatches = (
            self._counter_delta(source_entities, candidate_entities, include_types=text_types)
            + self._counter_delta(source_blocks, candidate_blocks, include_types=text_types)
        )
        viewport_mismatches = self._counter_delta(source_entities, candidate_entities, include_types={"VIEWPORT"})
        entity_metadata_mismatches = self._counter_delta(source_metadata, candidate_metadata)
        source_proxy_counter, source_proxy_graphics = self._proxy_graphic_inventory(source_doc)
        candidate_proxy_counter, candidate_proxy_graphics = self._proxy_graphic_inventory(candidate_doc)
        proxy_graphic_mismatches = self._counter_delta(source_proxy_counter, candidate_proxy_counter)
        source_proxy_object_count = self._proxy_object_count(source_doc)
        candidate_proxy_object_count = self._proxy_object_count(candidate_doc)
        if source_proxy_object_count:
            source_unsupported.add("ACAD_PROXY_OBJECT")
        if candidate_proxy_object_count:
            candidate_unsupported.add("ACAD_PROXY_OBJECT")

        source_counts = self._layout_counts(source_doc)
        candidate_counts = self._layout_counts(candidate_doc)
        source_layers = sorted(layer.dxf.name for layer in source_doc.layers)
        candidate_layers = sorted(layer.dxf.name for layer in candidate_doc.layers)
        source_layer_properties = self._layer_properties(source_doc)
        candidate_layer_properties = self._layer_properties(candidate_doc)
        source_block_names = self._user_block_names(source_doc)
        candidate_block_names = self._user_block_names(candidate_doc)
        source_layouts = sorted(layout.name for layout in source_doc.layouts)
        candidate_layouts = sorted(layout.name for layout in candidate_doc.layouts)
        source_text_styles = self._table_properties(source_doc.styles, tolerance)
        candidate_text_styles = self._table_properties(candidate_doc.styles, tolerance)
        source_dimension_styles = self._table_properties(source_doc.dimstyles, tolerance)
        candidate_dimension_styles = self._table_properties(candidate_doc.dimstyles, tolerance)
        source_layout_properties = self._layout_properties(source_doc, tolerance)
        candidate_layout_properties = self._layout_properties(candidate_doc, tolerance)
        source_viewport_properties = self._viewport_properties(source_doc, tolerance)
        candidate_viewport_properties = self._viewport_properties(candidate_doc, tolerance)
        source_ucs_properties = self._ucs_properties(source_doc, tolerance)
        candidate_ucs_properties = self._ucs_properties(candidate_doc, tolerance)
        source_extents = self._computed_extents(source_doc, tolerance)
        candidate_extents = self._computed_extents(candidate_doc, tolerance)
        coordinate_keys = ("$INSBASE", "$UCSORG", "$UCSXDIR", "$UCSYDIR", "$UCSNAME", "$UCSORTHOREF", "$UCSORTHOVIEW", "$UCSBASE", "$PUCSORG", "$PUCSXDIR", "$PUCSYDIR", "$PUCSNAME", "$PUCSORTHOREF", "$PUCSORTHOVIEW", "$TILEMODE", "$WORLDVIEW", "$CVPORT")
        source_coordinate_metadata = self._header_properties(source_doc, coordinate_keys, tolerance)
        candidate_coordinate_metadata = self._header_properties(candidate_doc, coordinate_keys, tolerance)
        source_insunits = self._header_int(source_doc, "$INSUNITS")
        candidate_insunits = self._header_int(candidate_doc, "$INSUNITS")
        source_measurement = self._header_int(source_doc, "$MEASUREMENT")
        candidate_measurement = self._header_int(candidate_doc, "$MEASUREMENT")

        differences: list[str] = []
        comparisons = (
            ("entity_counts", source_counts, candidate_counts),
            ("layers", source_layers, candidate_layers),
            ("layer_properties", source_layer_properties, candidate_layer_properties),
            ("blocks", source_block_names, candidate_block_names),
            ("block_entity_counts", self._serialize_block_inventory(source_block_inventory), self._serialize_block_inventory(candidate_block_inventory)),
            ("layouts", source_layouts, candidate_layouts),
            ("text_styles", source_text_styles, candidate_text_styles),
            ("dimension_styles", source_dimension_styles, candidate_dimension_styles),
            ("layout_properties", source_layout_properties, candidate_layout_properties),
            ("viewports", source_viewport_properties, candidate_viewport_properties),
            ("ucs_properties", source_ucs_properties, candidate_ucs_properties),
            ("extents", source_extents, candidate_extents),
            ("coordinate_metadata", source_coordinate_metadata, candidate_coordinate_metadata),
            ("INSUNITS", source_insunits, candidate_insunits),
            ("MEASUREMENT", source_measurement, candidate_measurement),
        )
        for label, left, right in comparisons:
            if left != right:
                differences.append(label)
        if geometry_mismatches:
            differences.append("supported_geometry_signatures")
        if text_mismatches:
            differences.append("text_content")
        if viewport_mismatches and "viewports" not in differences:
            differences.append("viewports")
        if entity_metadata_mismatches:
            differences.append("entity_metadata")
        if proxy_graphic_mismatches:
            differences.append("proxy_graphics")
        if source_proxy_object_count != candidate_proxy_object_count:
            differences.append("proxy_objects")
        if block_mismatches:
            differences.append("block_definition_geometry")
        if block_inventory_mismatches and "block_entity_counts" not in differences:
            differences.append("block_entity_counts")

        unsupported = sorted(source_unsupported | candidate_unsupported)
        geometry_unsupported = set(unsupported) - {"TEXT_READ_UNAVAILABLE", "ENTITY_METADATA_UNSUPPORTED"}
        if differences:
            status = "DIFFERENCES_FOUND"
            geometry_status = "DIFFERENCES_FOUND" if geometry_mismatches or block_mismatches or block_inventory_mismatches else (
                "INCOMPLETE" if geometry_unsupported else "MATCHED"
            )
        elif unsupported:
            status = "INCOMPLETE"
            geometry_status = "INCOMPLETE" if geometry_unsupported else "MATCHED"
        else:
            status = "MATCHED_SUPPORTED_CONTENT"
            geometry_status = "MATCHED"

        return DxfComparisonReport(
            source_path=str(source),
            candidate_path=str(candidate),
            source_sha256=source_sha256,
            candidate_sha256=candidate_sha256,
            ezdxf_version=ezdxf_version,
            comparison_status=status,
            geometry_comparison_status=geometry_status,
            fidelity_status="UNKNOWN",
            requires_review=True,
            source_entity_counts=source_counts,
            candidate_entity_counts=candidate_counts,
            source_layers=source_layers,
            candidate_layers=candidate_layers,
            source_layer_properties=source_layer_properties,
            candidate_layer_properties=candidate_layer_properties,
            source_blocks=source_block_names,
            candidate_blocks=candidate_block_names,
            source_layouts=source_layouts,
            candidate_layouts=candidate_layouts,
            source_text_styles=source_text_styles,
            candidate_text_styles=candidate_text_styles,
            source_dimension_styles=source_dimension_styles,
            candidate_dimension_styles=candidate_dimension_styles,
            source_layout_properties=source_layout_properties,
            candidate_layout_properties=candidate_layout_properties,
            source_viewport_properties=source_viewport_properties,
            candidate_viewport_properties=candidate_viewport_properties,
            source_ucs_properties=source_ucs_properties,
            candidate_ucs_properties=candidate_ucs_properties,
            source_extents=source_extents,
            candidate_extents=candidate_extents,
            source_coordinate_metadata=source_coordinate_metadata,
            candidate_coordinate_metadata=candidate_coordinate_metadata,
            source_insunits=source_insunits,
            candidate_insunits=candidate_insunits,
            source_measurement=source_measurement,
            candidate_measurement=candidate_measurement,
            source_block_entity_counts=self._serialize_block_inventory(source_block_inventory),
            candidate_block_entity_counts=self._serialize_block_inventory(candidate_block_inventory),
            geometry_mismatch_count=geometry_mismatches + block_mismatches + block_inventory_mismatches,
            text_mismatch_count=text_mismatches,
            viewport_mismatch_count=viewport_mismatches,
            entity_metadata_mismatch_count=entity_metadata_mismatches,
            source_proxy_graphics=source_proxy_graphics,
            candidate_proxy_graphics=candidate_proxy_graphics,
            proxy_graphic_mismatch_count=proxy_graphic_mismatches,
            source_proxy_object_count=source_proxy_object_count,
            candidate_proxy_object_count=candidate_proxy_object_count,
            unsupported_entity_types=unsupported,
            structural_differences=differences,
        )

    @staticmethod
    def _read_document(path: Path) -> tuple[Any, bool]:
        """Read strictly first, then recover damaged records without hiding uncertainty."""
        try:
            return ezdxf.readfile(path), False
        except Exception as strict_error:
            try:
                from ezdxf import recover
                document, _auditor = recover.readfile(path)
                return document, True
            except Exception:
                raise strict_error

    @classmethod
    def _collect(cls, document: Any, tolerance: float) -> tuple[Counter, Counter, Counter, Counter, set[str]]:
        layout_signatures: Counter = Counter()
        block_signatures: Counter = Counter()
        block_inventory: Counter = Counter()
        metadata_signatures: Counter = Counter()
        unsupported: set[str] = set()
        text_kinds = {"TEXT", "MTEXT", "ATTRIB", "ATTDEF"}

        for layout in document.layouts:
            container = ("layout", layout.name)
            for entity in layout:
                kind = None
                try:
                    kind = entity.dxftype()
                    signature = cls._signature(entity, tolerance)
                    presentation = presentation_signature(entity, tolerance)
                except Exception:
                    unsupported.add("TEXT_READ_UNAVAILABLE" if kind in text_kinds else "UNKNOWN_ENTITY")
                    continue
                if signature is None or presentation is None:
                    unsupported.add("TEXT_READ_UNAVAILABLE" if kind in text_kinds else kind)
                else:
                    layout_signatures[(container, kind, (signature, presentation))] += 1
                try:
                    metadata = cls._entity_metadata_signature(entity, tolerance)
                    if metadata is not None:
                        metadata_signatures[(container, kind, metadata)] += 1
                except Exception:
                    unsupported.add("ENTITY_METADATA_UNSUPPORTED")

        for block in document.blocks:
            if getattr(block, "is_any_layout", False):
                continue
            container = ("block", block.name)
            block_record = getattr(block, "block", None)
            block_dxf = getattr(block_record, "dxf", None)
            if block_dxf is not None:
                xref_path = block_dxf.get("xref_path")
                flags = int(block_dxf.get("flags", 0) or 0)
                if xref_path or flags & (4 | 8):
                    block_inventory[(block.name, f"XREF:{xref_path or 'UNRESOLVED'}")] += 1
                    unsupported.add("XREF_DEPENDENCY")
            for entity in block:
                kind = None
                try:
                    kind = entity.dxftype()
                    block_inventory[(block.name, kind)] += 1
                    signature = cls._signature(entity, tolerance)
                    presentation = presentation_signature(entity, tolerance)
                except Exception:
                    unsupported.add("TEXT_READ_UNAVAILABLE" if kind in text_kinds else "UNKNOWN_ENTITY")
                    continue
                if signature is None or presentation is None:
                    unsupported.add("TEXT_READ_UNAVAILABLE" if kind in text_kinds else kind)
                else:
                    block_signatures[(container, kind, (signature, presentation))] += 1
                try:
                    metadata = cls._entity_metadata_signature(entity, tolerance)
                    if metadata is not None:
                        metadata_signatures[(container, kind, metadata)] += 1
                except Exception:
                    unsupported.add("ENTITY_METADATA_UNSUPPORTED")
        return layout_signatures, block_signatures, block_inventory, metadata_signatures, unsupported

    @classmethod
    def _signature(cls, entity: Any, tolerance: float) -> tuple | None:
        kind = entity.dxftype()
        dxf = entity.dxf
        layer = dxf.get("layer", "0")
        if kind in {"TEXT", "MTEXT", "ATTRIB", "ATTDEF"}:
            text_value = entity.text if kind == "MTEXT" else dxf.get("text", "")
            if any(char == "\ufffd" or 0xDC80 <= ord(char) <= 0xDCFF for char in str(text_value)):
                # Invalid source bytes decoded as U+FFFD are not trusted text.
                return None
        if kind == "LINE":
            points = [cls._vector(dxf.start, tolerance), cls._vector(dxf.end, tolerance)]
            return (layer, tuple(sorted(points)))
        if kind == "CIRCLE":
            return (layer, cls._vector(dxf.center, tolerance), cls._quantize(dxf.radius, tolerance))
        if kind == "ARC":
            return (
                layer, cls._vector(dxf.center, tolerance),
                cls._quantize(dxf.radius, tolerance),
                cls._quantize(dxf.start_angle, tolerance),
                cls._quantize(dxf.end_angle, tolerance),
            )
        if kind == "POINT":
            return (layer, cls._vector(dxf.location, tolerance))
        if kind == "LWPOLYLINE":
            points = tuple(
                tuple(cls._quantize(value, tolerance) for value in point)
                for point in entity.get_points("xyseb")
            )
            return (layer, bool(entity.closed), points)
        if kind == "TEXT":
            return (
                layer, dxf.text, cls._vector(dxf.insert, tolerance),
                cls._quantize(dxf.height, tolerance),
                cls._quantize(dxf.rotation, tolerance),
                dxf.get("style", "Standard"),
                int(dxf.get("halign", 0)), int(dxf.get("valign", 0)),
                cls._vector(dxf.get("align_point", dxf.insert), tolerance),
            )
        if kind == "MTEXT":
            return (
                layer, entity.text, cls._vector(dxf.insert, tolerance),
                cls._quantize(dxf.char_height, tolerance),
                cls._quantize(dxf.get("width", 0), tolerance),
                cls._quantize(dxf.get("rotation", 0), tolerance),
                dxf.get("style", "Standard"),
                int(dxf.get("attachment_point", 1)),
            )
        if kind == "INSERT":
            attributes = insert_attributes_signature(entity, tolerance)
            if attributes is None:
                return None
            return (
                layer, dxf.name, cls._vector(dxf.insert, tolerance),
                # INSERT coordinates are OCS-based; extrusion changes the
                # orientation of the block reference and must be compared.
                cls._vector(dxf.get("extrusion", (0, 0, 1)), tolerance),
                cls._quantize(dxf.get("xscale", 1), tolerance),
                cls._quantize(dxf.get("yscale", 1), tolerance),
                cls._quantize(dxf.get("zscale", 1), tolerance),
                cls._quantize(dxf.get("rotation", 0), tolerance),
                int(dxf.get("row_count", 1)),
                int(dxf.get("column_count", 1)),
                cls._quantize(dxf.get("row_spacing", 0), tolerance),
                cls._quantize(dxf.get("column_spacing", 0), tolerance),
                attributes,
            )
        if kind == "VIEWPORT":
            return ("VIEWPORT", cls._stable_attributes(entity.dxfattribs(), tolerance, {"handle", "owner", "paperspace"}))
        if kind == "ELLIPSE":
            return (
                layer, cls._vector(dxf.center, tolerance),
                cls._vector(dxf.major_axis, tolerance),
                cls._quantize(dxf.ratio, tolerance),
                cls._quantize(dxf.start_param, tolerance),
                cls._quantize(dxf.end_param, tolerance),
            )
        return advanced_entity_signature(entity, tolerance)

    @staticmethod
    def _vector(value: Any, tolerance: float) -> tuple[int, ...]:
        return tuple(DxfComparator._quantize(component, tolerance) for component in value)

    @staticmethod
    def _quantize(value: Any, tolerance: float) -> int:
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("DXF_GEOMETRY_NONFINITE")
        return round(number / tolerance)

    @staticmethod
    def _serialize_block_inventory(inventory: Counter) -> dict[str, int]:
        return {f"{block_name}::{entity_type}": count for (block_name, entity_type), count in sorted(inventory.items())}

    @staticmethod
    def _counter_delta(
        left: Counter,
        right: Counter,
        *,
        include_types: set[str] | None = None,
        exclude_types: set[str] | None = None,
    ) -> int:
        def selected(counter: Counter) -> Counter:
            result = Counter()
            for key, count in counter.items():
                kind = key[1] if isinstance(key, tuple) and len(key) > 1 else None
                if include_types is not None and kind not in include_types:
                    continue
                if exclude_types is not None and kind in exclude_types:
                    continue
                result[key] = count
            return result

        selected_left = selected(left)
        selected_right = selected(right)
        return sum((selected_left - selected_right).values()) + sum((selected_right - selected_left).values())

    @classmethod
    def _stable_value(cls, value: Any, tolerance: float) -> Any:
        if value is None or isinstance(value, (str, bool, int)):
            return value
        if isinstance(value, float):
            return cls._quantize(value, tolerance)
        if hasattr(value, "x") and hasattr(value, "y"):
            components = [value.x, value.y]
            if hasattr(value, "z"):
                components.append(value.z)
            return tuple(cls._quantize(component, tolerance) for component in components)
        if isinstance(value, dict):
            return tuple(sorted((str(key), cls._stable_value(item, tolerance)) for key, item in value.items()))
        if isinstance(value, (tuple, list)):
            return tuple(cls._stable_value(item, tolerance) for item in value)
        raise TypeError(f"DXF_METADATA_VALUE_UNSUPPORTED:{type(value).__name__}")

    @classmethod
    def _stable_attributes(cls, attributes: dict[str, Any], tolerance: float, excluded: set[str]) -> tuple:
        return tuple(sorted(
            (str(key), cls._stable_value(value, tolerance))
            for key, value in attributes.items()
            if key not in excluded
        ))

    @classmethod
    def _tag_payload(cls, tags: Any, tolerance: float, *, max_tags: int = 4096) -> tuple:
        values = []
        for index, tag in enumerate(tags):
            if index >= max_tags:
                raise ValueError("DXF_METADATA_TAG_LIMIT")
            code = int(tag.code)
            if code == 1005:
                # Handle references are not stable across independent DXF files.
                raise ValueError("DXF_METADATA_HANDLE_REFERENCE_UNRESOLVED")
            value = tag.value
            if isinstance(value, (bytes, bytearray)):
                value = ("SHA256", hashlib.sha256(bytes(value)).hexdigest())
            else:
                value = cls._stable_value(value, tolerance)
            values.append((code, value))
        return tuple(values)

    @classmethod
    def _extension_dictionary_payload(
        cls,
        dictionary: Any,
        tolerance: float,
        *,
        depth: int = 0,
        seen: set[str] | None = None,
        budget: list[int] | None = None,
    ) -> tuple:
        if depth > 8:
            raise ValueError("DXF_EXTENSION_DICTIONARY_DEPTH_LIMIT")
        if seen is None:
            seen = set()
        if budget is None:
            budget = [0]
        handle = getattr(getattr(dictionary, "dxf", None), "handle", None)
        if handle and handle in seen:
            raise ValueError("DXF_EXTENSION_DICTIONARY_CYCLE")
        if handle:
            seen.add(handle)
        items = list(dictionary.items())
        budget[0] += len(items)
        if budget[0] > 256:
            raise ValueError("DXF_EXTENSION_DICTIONARY_ENTRY_LIMIT")
        result = []
        for key, value in sorted(items, key=lambda item: str(item[0])):
            kind = value.dxftype()
            if kind == "XRECORD":
                payload = ("XRECORD", cls._tag_payload(value.tags, tolerance))
            elif kind == "DICTIONARY":
                payload = ("DICTIONARY", cls._extension_dictionary_payload(
                    value, tolerance, depth=depth + 1, seen=seen, budget=budget
                ))
            else:
                raise TypeError(f"DXF_EXTENSION_OBJECT_UNSUPPORTED:{kind}")
            result.append((str(key), payload))
        return tuple(result)

    @classmethod
    def _proxy_graphic_inventory(cls, document: Any) -> tuple[Counter, list[dict[str, Any]]]:
        """Hash opaque proxy graphics for inventory only; never interpret them as geometry."""
        inventory: Counter = Counter()
        entries: list[dict[str, Any]] = []
        for layout in document.layouts:
            for entity in layout:
                try:
                    if entity.dxftype() != "ACAD_PROXY_ENTITY":
                        continue
                    graphic = getattr(entity, "proxy_graphic", b"") or b""
                    tags = getattr(entity, "acdb_proxy_entity", None) or ()
                    class_id = next((tag.value for tag in tags if tag.code == 91), None)
                    drawing_format = next((tag.value for tag in tags if tag.code == 95), None)
                    digest = hashlib.sha256(graphic).hexdigest() if graphic else None
                    item = {
                        "layout": layout.name,
                        "byte_count": len(graphic),
                        "sha256": digest,
                        "class_id": class_id,
                        "drawing_format": drawing_format,
                    }
                    entries.append(item)
                    inventory[(layout.name, len(graphic), digest, class_id, drawing_format)] += 1
                except Exception:
                    inventory[(layout.name, "UNKNOWN_PROXY_GRAPHIC")] += 1
                    entries.append({
                        "layout": layout.name,
                        "byte_count": None,
                        "sha256": None,
                        "class_id": None,
                        "drawing_format": None,
                        "status": "UNKNOWN",
                    })
        entries.sort(key=lambda item: repr(sorted(item.items())))
        return inventory, entries

    @staticmethod
    def _proxy_object_count(document: Any) -> int:
        count = 0
        for obj in document.objects:
            try:
                if obj.dxftype() == "ACAD_PROXY_OBJECT":
                    count += 1
            except Exception:
                continue
        return count

    @classmethod
    def _entity_metadata_signature(cls, entity: Any, tolerance: float) -> tuple | None:
        xdata_payload = ()
        xdata = getattr(entity, "xdata", None)
        data = getattr(xdata, "data", {}) if xdata is not None else {}
        if data:
            app_payloads = []
            for appid, tags in sorted(data.items(), key=lambda item: str(item[0])):
                app_payloads.append((str(appid), cls._tag_payload(tags, tolerance)))
            xdata_payload = tuple(app_payloads)

        extension_payload = ()
        if getattr(entity, "has_extension_dict", False):
            extension_payload = cls._extension_dictionary_payload(
                entity.get_extension_dict(), tolerance
            )
        if not xdata_payload and not extension_payload:
            return None
        return ("XDATA", xdata_payload, "EXTENSION_DICTIONARY", extension_payload)

    @classmethod
    def _table_properties(cls, table: Any, tolerance: float) -> dict[str, Any]:
        """Compare style-table records while excluding volatile handles and owners."""
        properties = {}
        for record in table:
            try:
                name = str(record.dxf.name)
                properties[name] = cls._stable_attributes(
                    record.dxfattribs(), tolerance, {"handle", "owner"}
                )
            except Exception:
                # Keep the table entry visible but never invent a normalized value.
                name = str(getattr(getattr(record, "dxf", None), "name", "UNKNOWN"))
                properties[name] = "UNKNOWN"
        return dict(sorted(properties.items()))

    @classmethod
    def _layout_properties(cls, document: Any, tolerance: float) -> dict[str, Any]:
        properties = {}
        for layout in document.layouts:
            record = getattr(layout, "dxf_layout", None)
            if record is None:
                continue
            properties[layout.name] = cls._stable_attributes(
                record.dxfattribs(), tolerance, {"handle", "owner", "block_record_handle"}
            )
        return dict(sorted(properties.items()))

    @classmethod
    def _viewport_properties(cls, document: Any, tolerance: float) -> dict[str, Any]:
        properties = {}
        for layout in document.layouts:
            viewports = []
            for entity in layout:
                if entity.dxftype() == "VIEWPORT":
                    viewports.append(cls._stable_attributes(
                        entity.dxfattribs(), tolerance, {"handle", "owner", "paperspace"}
                    ))
            properties[layout.name] = tuple(sorted(viewports, key=repr))
        return dict(sorted(properties.items()))

    @classmethod
    def _ucs_properties(cls, document: Any, tolerance: float) -> dict[str, Any]:
        properties = {}
        for record in document.ucs:
            properties[str(record.dxf.name)] = cls._stable_attributes(
                record.dxfattribs(), tolerance, {"handle", "owner"}
            )
        return dict(sorted(properties.items()))

    @classmethod
    def _computed_extents(cls, document: Any, tolerance: float) -> dict[str, Any]:
        """Compute conservative per-layout extents without depending on stale header extents."""
        from ezdxf import bbox

        properties = {}
        ignored_types = {"TEXT", "MTEXT", "ATTRIB", "ATTDEF", "VIEWPORT", "ACAD_PROXY_ENTITY"}
        for layout in document.layouts:
            entities = []
            for entity in layout:
                try:
                    if entity.dxftype() not in ignored_types:
                        entities.append(entity)
                except Exception:
                    continue
            try:
                bounds = bbox.extents(entities, fast=True)
                if bounds.has_data:
                    properties[layout.name] = {
                        "min": cls._stable_value(bounds.extmin, tolerance),
                        "max": cls._stable_value(bounds.extmax, tolerance),
                    }
                else:
                    properties[layout.name] = None
            except Exception:
                # Extents are supplementary metadata; a failure must not erase
                # the independently collected entity signatures.
                properties[layout.name] = "UNKNOWN"
        return dict(sorted(properties.items()))

    @classmethod
    def _header_properties(cls, document: Any, keys: tuple[str, ...], tolerance: float) -> dict[str, Any]:
        properties = {}
        for key in keys:
            try:
                value = document.header.get(key)
                if value is not None:
                    properties[key] = cls._stable_value(value, tolerance)
            except (AttributeError, TypeError, ValueError, OverflowError):
                properties[key] = "UNKNOWN"
        return properties

    @staticmethod
    def _layout_counts(document: Any) -> dict[str, int]:
        counts: Counter = Counter()
        for layout in document.layouts:
            for entity in layout:
                try:
                    counts[entity.dxftype()] += 1
                except Exception:
                    counts["UNKNOWN_ENTITY"] += 1
        return dict(sorted(counts.items()))

    @staticmethod
    def _layer_properties(document: Any) -> dict[str, dict[str, Any]]:
        """Return stable, JSON-safe layer table properties relevant to plotting."""
        properties: dict[str, dict[str, Any]] = {}
        for layer in document.layers:
            dxf = layer.dxf
            name = str(dxf.name)
            properties[name] = {
                "flags": int(dxf.get("flags", 0) or 0),
                "linetype": str(dxf.get("linetype", "CONTINUOUS") or "CONTINUOUS"),
                "color": int(dxf.get("color", 7) or 0),
                "lineweight": int(dxf.get("lineweight", -1) if dxf.get("lineweight", -1) is not None else -1),
                "plot": bool(dxf.get("plot", 1)),
                "plotstyle_handle": dxf.get("plotstyle_handle"),
            }
        return dict(sorted(properties.items()))

    @staticmethod
    def _user_block_names(document: Any) -> list[str]:
        return sorted(block.name for block in document.blocks if not getattr(block, "is_any_layout", False))

    @staticmethod
    def _header_int(document: Any, key: str) -> int | None:
        try:
            value = document.header.get(key)
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _failure(source: Path, candidate: Path, code: str, message: str) -> DxfComparisonReport:
        return DxfComparisonReport(
            source_path=str(source),
            candidate_path=str(candidate),
            comparison_status="COMPARISON_FAILED",
            geometry_comparison_status="NOT_RUN",
            fidelity_status="UNKNOWN",
            requires_review=True,
            error_code=code,
            error_message=message,
        )


def cls_sha256_file(path: Path) -> str:
    """Hash a DXF in bounded chunks so comparison reports identify exact inputs."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compare_dxf_files(
    source_path: str | Path,
    candidate_path: str | Path,
    *,
    tolerance: float = 1e-6,
) -> DxfComparisonReport:
    """Convenience entry point for conservative read-only DXF comparison."""
    return DxfComparator().compare(source_path, candidate_path, tolerance=tolerance)
