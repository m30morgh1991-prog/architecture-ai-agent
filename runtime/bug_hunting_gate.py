"""Mandatory PR Bug Hunting evidence gate.

This gate intentionally fails closed: missing or incomplete evidence is a merge blocker.
It is deterministic and dependency-free so CI can run in a clean environment.
"""

from __future__ import annotations
from pathlib import Path
import argparse
import re
import sys

REQUIRED_SECTIONS = (
    "## Scope",
    "## Bug Hunt",
    "## Findings",
    "## Reproduction",
    "## Root Cause",
    "## Regression",
    "## Required fail-closed states",
    "## CI Verification",
    "## Affected Contracts",
    "## Risk Classification",
    "## Negative Tests",
    "## Unresolved Findings",
    "## Final Decision",
)
REQUIRED_TOKENS = (
    "reproduction",
    "root cause",
    "regression",
    "UNKNOWN",
    "NEEDS_REVIEW",
    "BLOCKED",
    "PASS",
    "exact-head",
    "false pass",
    "affected contract",
    "risk",
    "negative test",
    "unresolved findings",
)

def evidence_path(pr_number: str, root: Path | None = None) -> Path:
    base = root or Path(__file__).resolve().parents[1]
    if not re.fullmatch(r"\d+", str(pr_number)):
        raise ValueError("PR_NUMBER_INVALID")
    return base / "docs" / "bug-hunting" / f"PR-{pr_number}.md"

def _outside_fenced_code_lines(text: str) -> list[str]:
    """Return Markdown lines outside fenced code blocks (backticks or tildes)."""
    visible: list[str] = []
    fence_char: str | None = None
    fence_length = 0

    for line in text.splitlines():
        opener = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char is None:
            if opener:
                marker, info = opener.groups()
                # CommonMark disallows backticks in the info string of a backtick fence.
                if marker[0] == "`" and "`" in info:
                    visible.append(line)
                    continue
                fence_char = marker[0]
                fence_length = len(marker)
                continue
            visible.append(line)
            continue

        closing = re.match(r"^ {0,3}(" + re.escape(fence_char) + r"{" + str(fence_length) + r",})[ \t]*$", line)
        if closing:
            fence_char = None
            fence_length = 0
        # All lines inside a fence are intentionally excluded, including the closing fence.
    return visible

def validate_evidence(text: str) -> list[str]:
    errors: list[str] = []
    visible_lines = _outside_fenced_code_lines(text)
    visible_text = "\n".join(visible_lines)
    for section in REQUIRED_SECTIONS:
        found = any(
            line.strip() == section
            and len(line) - len(line.lstrip(" ")) <= 3
            and not line.startswith("\t")
            for line in visible_lines
        )
        if not found:
            errors.append(f"MISSING_SECTION:{section}")
    lower = visible_text.lower()
    for token in REQUIRED_TOKENS:
        if token.lower() not in lower:
            errors.append(f"MISSING_TOKEN:{token}")
    if "unresolved" not in lower:
        errors.append("MISSING_UNRESOLVED_STATE")
    if "exact-head" not in lower:
        errors.append("MISSING_EXACT_HEAD_EVIDENCE")
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
