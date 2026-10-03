"""Mandatory PR Bug Hunting evidence gate.

This gate intentionally fails closed: missing or incomplete evidence is a merge blocker.
It is deterministic and dependency-free so CI can run it in a clean environment.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import re
import sys

REQUIRED_SECTIONS = (
    "## Scope", "## Bug Hunt", "## Findings", "## Regression",
    "## CI Verification", "## Final Decision",
)
REQUIRED_TOKENS = (
    "reproduction", "root cause", "regression", "UNKNOWN",
    "NEEDS_REVIEW", "BLOCKED", "PASS",
)

def evidence_path(pr_number: str, root: Path | None = None) -> Path:
    base = root or Path(__file__).resolve().parents[1]
    if not re.fullmatch(r"\d+", str(pr_number)):
        raise ValueError("PR_NUMBER_INVALID")
    return base / "docs" / "bug-hunting" / f"PR-{pr_number}.md"

def validate_evidence(text: str) -> list[str]:
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"MISSING_SECTION:{section}")
    lower = text.lower()
    for token in REQUIRED_TOKENS:
        if token.lower() not in lower:
            errors.append(f"MISSING_TOKEN:{token}")
    if "unresolved" not in lower:
        errors.append("MISSING_UNRESOLVED_STATE")
    return errors

def run(pr_number: str, root: Path | None = None) -> int:
    path = evidence_path(pr_number, root)
    if not path.exists():
        print(f"BUG_HUNT_BLOCKED: missing {path}")
        return 1
    errors = validate_evidence(path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"BUG_HUNT_BLOCKED: {error}")
        return 1
    print(f"BUG_HUNT_PASS: {path}")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-number", required=True)
    args = parser.parse_args()
    sys.exit(run(args.pr_number))
