"""Offline-first Architecture Intelligence Engine primitives.

The initial AIE facade is read-only and delegates canonical data ownership to
existing runtime contracts.
"""

from runtime.aie.core_facade import (
    AIEFinding,
    AIEInspectionResult,
    inspect_plan,
)

__all__ = ["AIEFinding", "AIEInspectionResult", "inspect_plan"]
