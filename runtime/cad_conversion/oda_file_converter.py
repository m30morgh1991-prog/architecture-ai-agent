"""Safe isolated adapter for the ODA File Converter command-line interface.

This adapter orchestrates an installed external codec. It does not claim
conversion is lossless or that output is architecturally valid.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


class ConversionError(RuntimeError):
    """Fail-closed conversion error with a stable machine-readable code."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class ODAFileConverterConfig:
    executable: str = "ODAFileConverter"
    output_version: str = "ACAD2018"
    timeout_seconds: int = 300
    audit: bool = False

    def __post_init__(self) -> None:
        supported = {"ACAD9", "ACAD10", "ACAD12", "ACAD14", "ACAD2000", "ACAD2004", "ACAD2007", "ACAD2010", "ACAD2013", "ACAD2018"}
        if self.output_version not in supported:
            raise ValueError("ODA_OUTPUT_VERSION_UNSUPPORTED")
        if not 1 <= self.timeout_seconds <= 3600:
            raise ValueError("ODA_TIMEOUT_OUT_OF_RANGE")


@dataclass(frozen=True)
class ConversionResult:
    source_path: Path
    output_path: Path
    engine: str
    output_version: str
    source_sha256: str
    output_sha256: str
    source_unchanged: bool
    execution_status: str
    fidelity_status: str
    requires_review: bool


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class ODAFileConverter:
    """DWG-to-DXF adapter using an externally installed ODA executable.

    Exactly one source is staged privately. The original source directory is
    never passed to the converter, recursion is disabled, and outputs are
    never overwritten.
    """

    def __init__(self, config: ODAFileConverterConfig | None = None):
        self.config = config or ODAFileConverterConfig()

    def _resolve_executable(self) -> str:
        candidate = self.config.executable
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
        path = Path(candidate).expanduser()
        if path.is_file():
            return str(path.resolve())
        raise ConversionError("CONVERTER_NOT_FOUND", "ODA File Converter executable was not found.")

    def convert_dwg_to_dxf(self, source_path: str | Path, output_path: str | Path) -> ConversionResult:
        source = Path(source_path).expanduser().resolve()
        destination = Path(output_path).expanduser().resolve()

        if not source.is_file():
            raise ConversionError("SOURCE_REQUIRED", "Source DWG file does not exist.")
        if source.suffix.lower() != ".dwg":
            raise ConversionError("SOURCE_FORMAT_UNSUPPORTED", "This adapter currently accepts DWG input only.")
        if destination.suffix.lower() != ".dxf":
            raise ConversionError("OUTPUT_FORMAT_INVALID", "Output path must use the .dxf extension.")
        if source == destination:
            raise ConversionError("SOURCE_OUTPUT_COLLISION", "Source and output paths must be different.")
        if destination.exists():
            raise ConversionError("OUTPUT_ALREADY_EXISTS", "Output exists; refusing to overwrite it.")

        executable = self._resolve_executable()
        source_hash_before = sha256_file(source)
        destination.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix="architecture-ai-cad-") as temp_root:
            root = Path(temp_root)
            staged_input, staged_output = root / "input", root / "output"
            staged_input.mkdir()
            staged_output.mkdir()
            staged_source = staged_input / f"source{source.suffix.lower()}"
            shutil.copy2(source, staged_source)

            command = [
                executable, str(staged_input), str(staged_output),
                self.config.output_version, "DXF", "0",
                "1" if self.config.audit else "0", "*.dwg",
            ]
            try:
                completed = subprocess.run(
                    command, capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=self.config.timeout_seconds, check=False,
                )
            except subprocess.TimeoutExpired as exc:
                raise ConversionError("CONVERSION_TIMEOUT", "ODA conversion exceeded its configured timeout.") from exc
            except OSError as exc:
                raise ConversionError("CONVERTER_EXECUTION_FAILED", "ODA executable could not be started.") from exc

            if completed.returncode != 0:
                raise ConversionError("CONVERTER_NONZERO_EXIT", f"ODA File Converter exited with code {completed.returncode}.")

            candidates = [
                item for item in staged_output.iterdir()
                if item.is_file() and item.suffix.lower() == ".dxf" and item.stem.lower() == "source"
            ]
            if len(candidates) != 1 or candidates[0].stat().st_size == 0:
                raise ConversionError("OUTPUT_MISSING_OR_AMBIGUOUS", "ODA did not produce exactly one non-empty DXF output.")

            source_hash_after = sha256_file(source)
            if source_hash_before != source_hash_after:
                raise ConversionError("SOURCE_MUTATED", "Source DWG changed during conversion; output is rejected.")

            try:
                with destination.open("xb") as target, candidates[0].open("rb") as generated:
                    shutil.copyfileobj(generated, target)
            except FileExistsError as exc:
                raise ConversionError("OUTPUT_ALREADY_EXISTS", "Output appeared during conversion; refusing to overwrite it.") from exc
            except OSError as exc:
                destination.unlink(missing_ok=True)
                raise ConversionError("OUTPUT_WRITE_FAILED", "Converted DXF could not be safely written.") from exc

        if destination.stat().st_size == 0:
            destination.unlink(missing_ok=True)
            raise ConversionError("OUTPUT_EMPTY", "Converted DXF is empty.")

        return ConversionResult(
            source_path=source, output_path=destination,
            engine="ODA File Converter", output_version=self.config.output_version,
            source_sha256=source_hash_before, output_sha256=sha256_file(destination),
            source_unchanged=True, execution_status="COMPLETED",
            fidelity_status="UNKNOWN", requires_review=True,
        )
