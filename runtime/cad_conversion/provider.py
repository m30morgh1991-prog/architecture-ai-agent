"""Provider contract for explicitly selected local CAD conversion engines."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from .oda_file_converter import ConversionResult


@runtime_checkable
class CadConversionProvider(Protocol):
    """Structural contract implemented by a local DWG-to-DXF provider."""

    @property
    def provider_id(self) -> str:
        """Stable provider identifier; never selected implicitly."""
        ...

    def convert_dwg_to_dxf(
        self, source_path: str | Path, output_path: str | Path
    ) -> ConversionResult:
        """Convert one DWG to one DXF without mutating the source."""
        ...
