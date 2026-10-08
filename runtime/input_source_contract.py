"""H100 source classification boundary for engineering vs image inputs.

Source classification is evidence-driven. File extension alone is insufficient
for PDF: a PDF must be inspected as vector or raster before choosing its path.
The ranking is a trust ordering for geometry reconstruction, not a claim that
every file of a class is correct.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePath

class SourceClass(str, Enum):
    ENGINEERING_VECTOR = "ENGINEERING_VECTOR"
    DOCUMENT_VECTOR = "DOCUMENT_VECTOR"
    DOCUMENT_RASTER = "DOCUMENT_RASTER"
    IMAGE_RASTER = "IMAGE_RASTER"
    UNKNOWN = "UNKNOWN"

class InputMode(str, Enum):
    ENGINEERING_PLAN = "ENGINEERING_PLAN"
    IMAGE = "IMAGE"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class SourceProfile:
    source_class: SourceClass
    input_mode: InputMode
    geometry_trust_rank: int
    requires_pdf_inspection: bool = False

    @property
    def is_engineering_input(self) -> bool:
        return self.input_mode is InputMode.ENGINEERING_PLAN

    @property
    def is_image_input(self) -> bool:
        return self.input_mode is InputMode.IMAGE

_GEOMETRY_TRUST = {
    SourceClass.ENGINEERING_VECTOR: 4,
    SourceClass.DOCUMENT_VECTOR: 3,
    SourceClass.DOCUMENT_RASTER: 2,
    SourceClass.IMAGE_RASTER: 1,
    SourceClass.UNKNOWN: 0,
}

def classify_source(filename: str, *, pdf_representation: str | None = None) -> SourceProfile:
    """Classify an input without pretending that PDF representation is known.

    pdf_representation must be "vector" or "raster" when supplied.
    Otherwise PDF remains UNKNOWN until inspection provides evidence.
    """
    suffix = PurePath(filename).suffix.lower()

    if suffix in {".dwg", ".dxf"}:
        source_class = SourceClass.ENGINEERING_VECTOR
        return SourceProfile(source_class, InputMode.ENGINEERING_PLAN, _GEOMETRY_TRUST[source_class])

    if suffix == ".pdf":
        if pdf_representation == "vector":
            source_class = SourceClass.DOCUMENT_VECTOR
            return SourceProfile(source_class, InputMode.ENGINEERING_PLAN, _GEOMETRY_TRUST[source_class])
        if pdf_representation == "raster":
            source_class = SourceClass.DOCUMENT_RASTER
            return SourceProfile(source_class, InputMode.IMAGE, _GEOMETRY_TRUST[source_class])
        if pdf_representation not in {None, "vector", "raster"}:
            raise ValueError("PDF_REPRESENTATION_INVALID")
        return SourceProfile(SourceClass.UNKNOWN, InputMode.UNKNOWN, 0, requires_pdf_inspection=True)

    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        source_class = SourceClass.IMAGE_RASTER
        return SourceProfile(source_class, InputMode.IMAGE, _GEOMETRY_TRUST[source_class])

    return SourceProfile(SourceClass.UNKNOWN, InputMode.UNKNOWN, 0)