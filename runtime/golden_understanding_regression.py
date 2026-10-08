from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ALLOWED_DECISIONS = {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}
REQUIRED_DOMAINS = (
    "source_profile", "elements", "geometry", "topology", "relations",
    "drawing_evidence", "text", "dimensions", "levels", "view_markers",
    "vertical_circulation", "bim_mapping", "provenance", "uncertainties",
    "contradictions", "missing_evidence", "fail_closed_decision",
)


@dataclass(frozen=True)
class GoldenCase:
    case_id: str
    source_path: str
    source_sha256: str | None
    expected_elements: tuple[str, ...]
    expected_domains: tuple[str, ...]
    expected_status: str
    adversarial: bool = False

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id is required")
        if not self.source_path.strip():
            raise ValueError("source_path is required")
        if self.source_sha256 is not None and (
            len(self.source_sha256) != 64
            or any(c not in "0123456789abcdef" for c in self.source_sha256.lower())
        ):
            raise ValueError("source_sha256 must be a 64-character hex digest")
        if self.expected_status not in ALLOWED_DECISIONS:
            raise ValueError("invalid expected_status")
        if not self.expected_domains:
            raise ValueError("expected_domains must not be empty")
        unknown = set(self.expected_domains) - set(REQUIRED_DOMAINS)
        if unknown:
            raise ValueError(f"unknown expected domains: {sorted(unknown)}")


@dataclass(frozen=True)
class GoldenRegressionReport:
    case_id: str
    domain_results: Mapping[str, bool]
    unsafe_acceptance: bool
    decision: str
    failures: tuple[str, ...]
    unknown_domains: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.decision not in ALLOWED_DECISIONS:
            raise ValueError("invalid decision")
        if self.decision == "PASS" and (self.failures or self.unsafe_acceptance):
            raise ValueError("PASS cannot contain failures or unsafe acceptance")


def load_manifest(path: str | Path) -> tuple[GoldenCase, ...]:
    import json

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema") != "golden-understanding-v1":
        raise ValueError("unsupported golden manifest schema")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("manifest cases must be a non-empty list")

    result: list[GoldenCase] = []
    seen: set[str] = set()
    for raw in cases:
        case = GoldenCase(
            case_id=str(raw["case_id"]),
            source_path=str(raw["source_path"]),
            source_sha256=raw.get("source_sha256"),
            expected_elements=tuple(raw.get("expected_elements", ())),
            expected_domains=tuple(raw["expected_domains"]),
            expected_status=str(raw["expected_status"]),
            adversarial=bool(raw.get("adversarial", False)),
        )
        if case.case_id in seen:
            raise ValueError(f"duplicate case_id: {case.case_id}")
        seen.add(case.case_id)
        result.append(case)
    return tuple(result)


def evaluate_golden_case(
    case: GoldenCase, observed: Mapping[str, Any]
) -> GoldenRegressionReport:
    failures: list[str] = []
    domain_results: dict[str, bool] = {}

    for domain in case.expected_domains:
        value = observed.get(domain)
        # A domain is covered only when it is populated or explicitly UNKNOWN.
        # Empty containers are not evidence of understanding.
        explicit_unknown = value == "UNKNOWN" or (
            isinstance(value, Mapping) and value.get("status") == "UNKNOWN"
        )
        populated = value is not None and value != () and value != [] and value != {}
        ok = explicit_unknown or populated
        domain_results[domain] = ok
        if not ok:
            failures.append(f"MISSING_DOMAIN:{domain}")

    observed_elements = set(observed.get("elements", ()))
    for element in case.expected_elements:
        if element not in observed_elements:
            failures.append(f"MISSING_ELEMENT:{element}")

    observed_decision = observed.get("fail_closed_decision")
    if observed_decision not in ALLOWED_DECISIONS:
        failures.append("INVALID_DECISION")
    elif observed_decision != case.expected_status:
        failures.append(
            f"DECISION_MISMATCH:{observed_decision}!={case.expected_status}"
        )

    unresolved = bool(
        observed.get("uncertainties")
        or observed.get("contradictions")
        or observed.get("missing_evidence")
    )
    unsafe_acceptance = unresolved and observed_decision == "PASS"
    if unsafe_acceptance:
        failures.append("UNSAFE_ACCEPTANCE:UNRESOLVED_TO_PASS")

    if unsafe_acceptance:
        decision = "BLOCKED"
    elif failures:
        decision = "NEEDS_REVIEW"
    else:
        decision = "PASS"

    unknown_domains = tuple(
        domain for domain in case.expected_domains
        if observed.get(domain) == "UNKNOWN"
        or (
            isinstance(observed.get(domain), Mapping)
            and observed[domain].get("status") == "UNKNOWN"
        )
    )
    return GoldenRegressionReport(
        case_id=case.case_id,
        domain_results=domain_results,
        unsafe_acceptance=unsafe_acceptance,
        decision=decision,
        failures=tuple(failures),
        unknown_domains=unknown_domains,
    )


def run_manifest(
    manifest_path: str | Path, observations: Mapping[str, Mapping[str, Any]]
) -> tuple[GoldenRegressionReport, ...]:
    cases = load_manifest(manifest_path)
    return tuple(
        evaluate_golden_case(case, observations.get(case.case_id, {}))
        for case in cases
    )


def summarize_domain_metrics(
    reports: tuple[GoldenRegressionReport, ...] | list[GoldenRegressionReport],
) -> dict[str, Any]:
    """Return coverage metrics without treating UNKNOWN as successful understanding."""
    domain_names = sorted(
        {domain for report in reports for domain in report.domain_results}
    )
    metrics: dict[str, Any] = {}
    for domain in domain_names:
        total = len(reports)
        covered = sum(report.domain_results.get(domain, False) for report in reports)
        unknown = sum(domain in report.unknown_domains for report in reports)
        metrics[domain] = {
            "cases": total,
            "covered": covered,
            "unknown": unknown,
            "understood": covered - unknown,
            "coverage": covered / total if total else 0.0,
            "understood_rate": (covered - unknown) / total if total else 0.0,
        }
    return metrics
