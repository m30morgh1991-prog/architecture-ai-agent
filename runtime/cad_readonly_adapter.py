"""Dependency-free, read-only CAD inspection adapter.

This adapter is deliberately limited to source identity and filesystem-level
inspection. It never edits a CAD source and never claims semantic understanding.
A real AutoCAD-MCP implementation can replace this behind the same boundary.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from runtime.cad_adapter_contract import CADCapability, CADInspectionEvidence


class ReadOnlyCADInspectionAdapter:
    adapter_id = "filesystem-cad-readonly-v1"

    def capabilities(self) -> tuple[CADCapability, ...]:
        return (CADCapability("inspect_source_identity", True, True),)

    def inspect(self, source: Any, source_sha256: str) -> CADInspectionEvidence:
        path = Path(source)
        if not path.is_file():
            return CADInspectionEvidence(
                self.adapter_id, source_sha256, {"error": "SOURCE_MISSING"}, "BLOCKED"
            )
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != source_sha256:
            return CADInspectionEvidence(
                self.adapter_id,
                actual,
                {"error": "CAD_SOURCE_SHA_MISMATCH", "expected_sha256": source_sha256},
                "BLOCKED",
            )
        return CADInspectionEvidence(
            self.adapter_id,
            actual,
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "suffix": path.suffix.lower(),
                "read_only": True,
                "semantic_authority": False,
            },
            "READY",
        )
