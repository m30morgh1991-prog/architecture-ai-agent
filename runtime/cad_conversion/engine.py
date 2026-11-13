"""Explicit provider registry and fail-closed CAD conversion facade."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from .oda_file_converter import ConversionError, ConversionResult, sha256_file
from .provider import CadConversionProvider


_PROVIDER_ID = re.compile(r"^[a-z][a-z0-9_]{1,63}$")


class ProviderRegistry:
    """Registry with explicit registration and selection; no auto-fallback."""

    def __init__(self, providers: Iterable[CadConversionProvider] = ()):
        self._providers: dict[str, CadConversionProvider] = {}
        for provider in providers:
            self.register(provider)

    def register(self, provider: CadConversionProvider) -> None:
        if not isinstance(provider, CadConversionProvider):
            raise TypeError("CAD_PROVIDER_CONTRACT_INVALID")
        provider_id = provider.provider_id
        if not isinstance(provider_id, str) or not _PROVIDER_ID.fullmatch(provider_id):
            raise ValueError("CAD_PROVIDER_ID_INVALID")
        if provider_id in self._providers:
            raise ValueError("CAD_PROVIDER_DUPLICATE")
        self._providers[provider_id] = provider

    def get(self, provider_id: str) -> CadConversionProvider:
        provider = self._providers.get(provider_id)
        if provider is None:
            raise ConversionError(
                "PROVIDER_UNAVAILABLE",
                f"Requested CAD conversion provider is not registered: {provider_id}",
            )
        return provider

    def available_providers(self) -> tuple[str, ...]:
        return tuple(sorted(self._providers))


class CadConversionEngine:
    """Run only the provider explicitly selected by the caller.

    The facade validates the provider result and preserves the v0.1 rule that
    execution completion never implies conversion fidelity.
    """

    def __init__(self, providers: Iterable[CadConversionProvider] = ()):
        self.registry = ProviderRegistry(providers)

    def available_providers(self) -> tuple[str, ...]:
        return self.registry.available_providers()

    def convert_dwg_to_dxf(
        self,
        provider_id: str,
        source_path: str | Path,
        output_path: str | Path,
    ) -> ConversionResult:
        source = Path(source_path).expanduser().resolve()
        destination = Path(output_path).expanduser().resolve()

        if not provider_id:
            raise ConversionError("PROVIDER_REQUIRED", "A provider must be selected explicitly.")
        if not source.is_file() or source.suffix.lower() != ".dwg":
            raise ConversionError("SOURCE_REQUIRED", "A readable DWG source is required.")
        if destination.suffix.lower() != ".dxf":
            raise ConversionError("OUTPUT_FORMAT_INVALID", "Output path must use the .dxf extension.")
        if source == destination:
            raise ConversionError("SOURCE_OUTPUT_COLLISION", "Source and output paths must be different.")
        if destination.exists():
            raise ConversionError("OUTPUT_ALREADY_EXISTS", "Output exists; refusing to overwrite it.")

        provider = self.registry.get(provider_id)
        source_hash_before = sha256_file(source)
        result = provider.convert_dwg_to_dxf(source, destination)
        source_hash_after = sha256_file(source)

        if source_hash_before != source_hash_after or not result.source_unchanged:
            raise ConversionError("SOURCE_MUTATED", "Provider changed the source DWG; result is rejected.")
        if result.source_path.resolve() != source or result.output_path.resolve() != destination:
            raise ConversionError("PROVIDER_PATH_MISMATCH", "Provider result paths do not match the requested files.")
        if not destination.is_file() or destination.stat().st_size == 0:
            raise ConversionError("PROVIDER_OUTPUT_INVALID", "Provider did not produce one non-empty DXF.")
        if sha256_file(destination) != result.output_sha256:
            raise ConversionError("PROVIDER_OUTPUT_HASH_MISMATCH", "Provider output hash does not match the artifact.")
        if result.execution_status != "COMPLETED":
            raise ConversionError("PROVIDER_EXECUTION_INCOMPLETE", "Provider did not report completed execution.")
        if result.fidelity_status != "UNKNOWN" or result.requires_review is not True:
            raise ConversionError(
                "PROVIDER_FIDELITY_CONTRACT_VIOLATION",
                "v0.1 providers must keep fidelity UNKNOWN and require human review.",
            )
        return result
