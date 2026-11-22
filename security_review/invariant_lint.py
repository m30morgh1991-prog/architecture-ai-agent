#!/usr/bin/env python3
"""Offline, stdlib-only heuristic linter for Architecture AI Agent.

Read-only. Findings are NEEDS_REVIEW signals, not proof. A clean run is NOT
a security pass. Exit: 0 no new findings, 1 findings, 2 internal error.
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path


def finding(rule, path, line, message):
    return {"rule": rule, "file": str(path), "line": line, "message": message}


def lint_py(path, rel):
    out = []
    src = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return [finding("INV-000", rel, exc.lineno or 0, "file does not parse")]
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg == "authorized" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    out.append(finding("INV-001", rel, node.lineno, "authorized=True may lift LOCKED guard; requires bound approval evidence"))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            seg = ast.get_source_segment(src, node) or ""
            if "float(" in seg and re.search(r"\bmax\(\s*0(\.0)?\s*,\s*min\(\s*1(\.0)?\s*,\s*float\(", seg) and not re.search(r"isfinite|isnan|math\.isinf", seg):
                out.append(finding("INV-002", rel, node.lineno, f"{node.name}(): float() clamped via max/min without finite-number check"))
            if isinstance(node, ast.FunctionDef) and node.name == "classify" and "NON_BLOCKING" in seg and "BLOCKING" in seg and "in BLOCKING" in seg:
                out.append(finding("INV-003", rel, node.lineno, "classify() may default unknown codes to NON_BLOCKING; prefer explicit allow-list"))
            if isinstance(node, ast.FunctionDef) and node.name.startswith("has_completed") and node.body and isinstance(node.body[-1], ast.Return) and isinstance(node.body[-1].value, ast.Constant) and node.body[-1].value.value is True:
                out.append(finding("INV-004", rel, node.body[-1].lineno, f"{node.name}() ends in unconditional return True"))
    for match in re.finditer(r'["\']0\.0\.0\.0["\']', src):
        out.append(finding("INV-005", rel, src[:match.start()].count("\n") + 1, "binds all interfaces"))
    if re.search(r"\bHTTPServer\(", src) and not re.search(r"ThreadingHTTPServer|settimeout|\.timeout\s*=", src):
        out.append(finding("INV-006", rel, 1, "single-threaded HTTPServer without visible timeout/threading protection"))
    if rel.startswith("runtime/") and rel not in ("runtime/app.py", "runtime/cad_conversion/oda_file_converter.py"):
        pattern = r"^\s*(import|from)\s+(subprocess|requests|urllib|httpx|socket)\b|shell\s*=\s*True|\beval\(|\bexec\(|pickle\.loads?"
        for match in re.finditer(pattern, src, re.M):
            out.append(finding("INV-007", rel, src[:match.start()].count("\n") + 1, f"sensitive API pattern: {match.group(0).strip()}"))
    return out


def lint_workflow(path, rel):
    out = []
    text = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"^permissions:", text, re.M):
        out.append(finding("INV-101", rel, 1, "no top-level permissions block; token permissions depend on repository defaults"))
    for line_no, line in enumerate(text.splitlines(), 1):
        match = re.search(r"uses:\s*([^\s#]+)", line)
        if match and not match.group(1).startswith("./") and not re.search(r"@[0-9a-f]{40}$", match.group(1)):
            out.append(finding("INV-102", rel, line_no, f"action not pinned to a full commit SHA: {match.group(1)}"))
        if re.search(r"\$\{\{\s*github\.(event\.(pull_request\.(title|body|head\.ref)|issue\.(title|body)|comment\.body)|head_ref)", line) and "run:" in text:
            out.append(finding("INV-103", rel, line_no, "untrusted event data interpolated into workflow run script"))
        if re.search(r"continue-on-error:\s*true", line):
            out.append(finding("INV-104", rel, line_no, "continue-on-error: true can mask scan failure"))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--baseline")
    parser.add_argument("--write-baseline")
    parser.add_argument("--json")
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    findings = []
    runtime = root / "runtime"
    workflows = root / ".github/workflows"
    if runtime.exists():
        for path in sorted(runtime.rglob("*.py")):
            findings.extend(lint_py(path, path.relative_to(root).as_posix()))
    if workflows.exists():
        for path in sorted(workflows.glob("*.y*ml")):
            findings.extend(lint_workflow(path, path.relative_to(root).as_posix()))
    key = lambda item: f"{item['rule']}|{item['file']}|{item['message']}"
    if args.write_baseline:
        Path(args.write_baseline).write_text(json.dumps(sorted({key(item) for item in findings}), indent=1), encoding="utf-8")
    baseline = set(json.loads(Path(args.baseline).read_text(encoding="utf-8"))) if args.baseline else set()
    new_findings = [item for item in findings if key(item) not in baseline]
    for item in findings:
        print(f"{'NEW' if item in new_findings else 'baseline'} {item['rule']} {item['file']}:{item['line']} {item['message']}")
    print(f"\ntotal={len(findings)} new={len(new_findings)} baseline={len(findings)-len(new_findings)} (heuristic only; clean is not a security pass)")
    if args.json:
        Path(args.json).write_text(json.dumps({"total": len(findings), "new": len(new_findings), "findings": findings}, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.exit(1 if new_findings else 0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print("INTERNAL ERROR:", exc, file=sys.stderr)
        sys.exit(2)
