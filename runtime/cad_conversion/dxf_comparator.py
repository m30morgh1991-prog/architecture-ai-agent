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


COMPARATOR_VERSION = "0.5.0"


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
    source_insunits: int | None = None
    candidate_insunits: int | None = None
    source_measurement: int | None = None
    candidate_measurement: int | None = None
    geometry_mismatch_count: int = 0
    text_mismatch_count: int = 0
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

        source_entities, source_blocks, source_block_inventory, source_unsupported = self._collect(source_doc, tolerance)
        candidate_entities, candidate_blocks, candidate_block_inventory, candidate_unsupported = self._collect(candidate_doc, tolerance)
        if source_recovered:
            source_unsupported.add("DXF_RECOVERY_USED")
        if candidate_recovered:
            candidate_unsupported.add("DXF_RECOVERY_USED")
        geometry_mismatches = self._counter_delta(source_entities, candidate_entities, text_only=False)
        block_mismatches = self._counter_delta(source_blocks, candidate_blocks, text_only=False)
        block_inventory_mismatches = self._counter_delta(source_block_inventory, candidate_block_inventory, text_only=False)
        text_mismatches = (
            self._counter_delta(source_entities, candidate_entities, text_only=True)
            + self._counter_delta(source_blocks, candidate_blocks, text_only=True)
        )

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
        if block_mismatches:
            differences.append("block_definition_geometry")
        if block_inventory_mismatches and "block_entity_counts" not in differences:
            differences.append("block_entity_counts")

        unsupported = sorted(source_unsupported | candidate_unsupported)
        geometry_unsupported = set(unsupported) - {"TEXT_READ_UNAVAILABLE"}
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
            source_insunits=source_insunits,
            candidate_insunits=candidate_insunits,
            source_measurement=source_measurement,
            candidate_measurement=candidate_measurement,
            source_block_entity_counts=self._serialize_block_inventory(source_block_inventory),
            candidate_block_entity_counts=self._serialize_block_inventory(candidate_block_inventory),
            geometry_mismatch_count=geometry_mismatches + block_mismatches + block_inventory_mismatches,
            text_mismatch_count=text_mismatches,
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
    def _collect(cls, document: Any, tolerance: float) -> tuple[Counter, Counter, Counter, set[str]]:
        layout_signatures: Counter = Counter()
        block_signatures: Counter = Counter()
        block_inventory: Counter = Counter()
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
        return layout_signatures, block_signatures, block_inventory, unsupported

    @classmethod
    def _signature(cls, entity: Any, tolerance: float) -> tuple | None:
        kind = entity.dxftype()
        dxf = entity.dxf
        layer = dxf.get("layer", "0")
        if kind in {"TEXT", "MTEXT", "ATTRIB", "ATTDEF"}:
            text_value = entity.text if kind == "MTEXT" else dxf.get("text", "")
            if "\\ufffd" in str(text_value):
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
    def _counter_delta(left: Counter, right: Counter, *, text_only: bool | None = None) -> int:
        text_types = {"TEXT", "MTEXT", "ATTRIB", "ATTDEF"}

        def selected(counter: Counter) -> Counter:
            if text_only is None:
                return counter
            return Counter({
                key: count for key, count in counter.items()
                if ((isinstance(key, tuple) and len(key) > 1 and key[1] in text_types) is text_only)
            })

        selected_left = selected(left)
        selected_right = selected(right)
        return sum((selected_left - selected_right).values()) + sum((selected_right - selected_left).values())

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
