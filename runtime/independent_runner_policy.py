"""Fail-closed policy contract for an unattended AI implementation runner.

This module does not call an AI provider, edit files, create PRs, merge code, or
unlock stages. It is a deterministic authorization boundary for a future runner.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

_REQUIRED_GATES = ("pr_ci", "runtime_tests", "bug_hunt", "required_regression")
_VALID_SHA = re.compile(r"^[0-9a-f]{40}$")


def evaluate_runner_readiness(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Return a conservative decision for whether an AI task may start.

    Every required gate must explicitly equal success. Missing, pending,
    cancelled, skipped, or unknown values fail closed. A configured provider
    must be asserted explicitly; credentials are never inferred from a name.
    An existing agent PR blocks duplicate work.

    Even when ready, this contract never authorizes merge or stage advancement.
    """
    blockers: list[str] = []
    sha = snapshot.get("main_sha")
    stage = snapshot.get("active_stage")

    if not isinstance(sha, str) or not _VALID_SHA.fullmatch(sha):
        blockers.append("MAIN_SHA_MISSING_OR_INVALID")
    if not isinstance(stage, str) or not re.fullmatch(r"H[0-9]{2,3}", stage):
        blockers.append("ACTIVE_STAGE_MISSING_OR_INVALID")

    gates = snapshot.get("gates")
    if not isinstance(gates, Mapping):
        blockers.append("GATE_SNAPSHOT_MISSING")
        gates = {}

    for gate in _REQUIRED_GATES:
        if gates.get(gate) != "success":
            blockers.append(f"GATE_NOT_GREEN:{gate}")

    if snapshot.get("provider_configured") is not True:
        blockers.append("AI_PROVIDER_NOT_CONFIGURED")

    if snapshot.get("agent_pr_open") is True:
        blockers.append("EXISTING_AGENT_PR_REQUIRES_RECONCILIATION")
    elif snapshot.get("agent_pr_open") is not False:
        blockers.append("AGENT_PR_STATE_UNKNOWN")

    ready = not blockers
    return {
        "decision": "READY_FOR_TASK" if ready else "BLOCKED",
        "blockers": blockers,
        "can_inspect": True,
        "can_investigate_failures": True,
        "can_edit_in_isolated_branch": ready,
        "can_open_pull_request": ready,
        "can_merge": False,
        "can_advance_stage": False,
        "requires_human_merge_approval": True,
        "main_sha": sha if isinstance(sha, str) else None,
        "active_stage": stage if isinstance(stage, str) else None,
    }
