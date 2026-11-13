"""Read-only structural validation for generated DXF artifacts.

A clean parse/audit is not proof of DWG-to-DXF fidelity or architectural
correctness. This module never saves or modifies the input drawing.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    import ezdxf
    from ezdxf import DXFError
except ImportError:  # pragma: no cover - exercised in dependency-missing installs
    ezdxf = None
    DXFError = Exception


_PERSIAN_RANGES = (
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
)
_UNIT_NAMES = {
    0: "unitless",
    1: "inches",
    2: "feet",
    3: "miles",
    4: "millimeters",
    5: "centimeters",
    6: "meters",
    7: "kilometers",
    8: "microinches",
    9: "mils",
    10: "yards",
    11: "angstroms",
    12: "nanometers",
    13: "microns",
    14: "decimeters",
    15: "decameters",
    16: "hectometers",
    17: "gigameters",
    18: "astronomical units",
    19: "light years",
    20: "parsecs",
}


@dataclass(frozen=True)
class DxfValidationReport:
    source_path: str
    validation_status: str
    parse_status: str
    audit_status: str
    fidelity_status: str
    requires_review: bool
    file_size_bytes: int
    dxf_version: str | None = None
    entity_count: int = 0
    entity_types: dict[str, int] = field(default_factory=dict)
    layers: list[str] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)
    layouts: list[str] = field(default_factory=list)
    dimension_count: int = 0
    text_entity_count: int = 0
    non_ascii_text_entity_count: int = 0
    persian_text_entity_count: int = 0
    block_definition_entity_count: int = 0
    block_entity_types: dict[str, int] = field(default_factory=dict)
    insunits_code: int | None = None
    insunits_name: str | None = None
    measurement_code: int | None = None
    audit_error_count: int = 0
    audit_fix_count: int = 0
    audit_messages: list[str] = field(default_factory=list)
    error_code: str | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of this report."""
        return asdict(self)


class DxfValidator:
    """Validate DXF readability and structure without changing the source."""

    def validate(self, source_path: str | Path) -> DxfValidationReport:
        source = Path(source_path).expanduser().resolve()
        if source.suffix.lower() != ".dxf":
            return self._failure(source, "DXF_INPUT_REQUIRED", "Input must have a .dxf extension.")
        if not source.is_file():
            return self._failure(source, "SOURCE_REQUIRED", "DXF source file does not exist.")
        try:
            size = source.stat().st_size
        except OSError:
            return self._failure(source, "SOURCE_UNREADABLE", "DXF source metadata could not be read.")
        if size == 0:
            return self._failure(source, "DXF_EMPTY", "DXF source file is empty.")
        if ezdxf is None:
            return self._failure(
                source,
                "EZDXF_UNAVAILABLE",
                "The ezdxf dependency is not installed; independent DXF validation is unavailable.",
                file_size_bytes=size,
            )

        try:
            document = ezdxf.readfile(source)
        except (OSError, DXFError, UnicodeError, ValueError) as exc:
            return self._failure(
                source,
                "DXF_PARSE_FAILED",
                f"DXF could not be parsed ({type(exc).__name__}).",
                file_size_bytes=size,
            )

        layout_counts: Counter[str] = Counter()
        block_counts: Counter[str] = Counter()
        text_entities = 0
        non_ascii_text_entities = 0
        persian_text_entities = 0
        dimension_count = 0

        for layout in document.layouts:
            for entity in layout:
                kind = entity.dxftype()
                layout_counts[kind] += 1
                if kind in {"TEXT", "MTEXT", "ATTRIB", "ATTDEF"}:
                    text_entities += 1
                    value = self._text_value(entity)
                    if any(ord(char) > 127 for char in value):
                        non_ascii_text_entities += 1
                    if any(self._is_persian(char) for char in value):
                        persian_text_entities += 1
                if kind == "DIMENSION":
                    dimension_count += 1

        user_blocks = [block for block in document.blocks if not getattr(block, "is_any_layout", False)]
        for block in user_blocks:
            for entity in block:
                block_counts[entity.dxftype()] += 1

        auditor = document.audit()
        audit_errors = list(getattr(auditor, "errors", ()))
        audit_fixes = list(getattr(auditor, "fixes", ()))
        audit_messages = [
            str(item)[:500]
            for item in (audit_errors + audit_fixes)[:50]
        ]
        insunits = self._header_int(document, "$INSUNITS")
        measurement = self._header_int(document, "$MEASUREMENT")
        audit_status = "CLEAN" if not audit_errors and not audit_fixes else "HAS_FINDINGS"

        return DxfValidationReport(
            source_path=str(source),
            validation_status="PARSE_PASS" if audit_status == "CLEAN" else "PARSE_PASS_WITH_AUDIT_FINDINGS",
            parse_status="PASS",
            audit_status=audit_status,
            fidelity_status="UNKNOWN",
            requires_review=True,
            file_size_bytes=size,
            dxf_version=getattr(document, "dxfversion", None),
            entity_count=sum(layout_counts.values()),
            entity_types=dict(sorted(layout_counts.items())),
            layers=sorted(layer.dxf.name for layer in document.layers),
            blocks=sorted(block.name for block in user_blocks),
            layouts=sorted(layout.name for layout in document.layouts),
            dimension_count=dimension_count,
            text_entity_count=text_entities,
            non_ascii_text_entity_count=non_ascii_text_entities,
            persian_text_entity_count=persian_text_entities,
            block_definition_entity_count=sum(block_counts.values()),
            block_entity_types=dict(sorted(block_counts.items())),
            insunits_code=insunits,
            insunits_name=_UNIT_NAMES.get(insunits) if insunits is not None else None,
            measurement_code=measurement,
            audit_error_count=len(audit_errors),
            audit_fix_count=len(audit_fixes),
            audit_messages=audit_messages,
        )

    @staticmethod
    def _text_value(entity: Any) -> str:
        try:
            if entity.dxftype() == "MTEXT":
                return entity.text
            return str(entity.dxf.get("text", ""))
        except (AttributeError, TypeError):
            return ""

    @staticmethod
    def _is_persian(char: str) -> bool:
        codepoint = ord(char)
        return any(start <= codepoint <= end for start, end in _PERSIAN_RANGES)

    @staticmethod
    def _header_int(document: Any, key: str) -> int | None:
        try:
            value = document.header.get(key)
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _failure(
        source: Path,
        code: str,
        message: str,
        *,
        file_size_bytes: int = 0,
    ) -> DxfValidationReport:
        return DxfValidationReport(
            source_path=str(source),
            validation_status="PARSE_FAILED",
            parse_status="FAIL",
            audit_status="NOT_RUN",
            fidelity_status="UNKNOWN",
            requires_review=True,
            file_size_bytes=file_size_bytes,
            error_code=code,
            error_message=message,
        )


def validate_dxf(source_path: str | Path) -> DxfValidationReport:
    """Convenience entry point for read-only DXF validation."""
    return DxfValidator().validate(source_path)
