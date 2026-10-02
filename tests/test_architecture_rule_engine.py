from runtime.architecture_rule_engine import (
    Rule,
    RuleEvaluation,
    RuleSet,
    RuleSource,
    evaluate_rule,
)

SOURCE = "a" * 64


def _rule(**kwargs):
    source = RuleSource(
        "nbr-door", "Project door rule basis", "PROJECT_BASIS",
        "door-clear-opening", True
    )
    data = {
        "rule_id": "door-clear-opening",
        "version": "1.0.0",
        "domain": "accessibility",
        "statement": "Evaluate effective clear opening, not nominal width.",
        "source": source,
        "severity": "BLOCKING",
        "evidence_ids": ("ev-door",),
    }
    data.update(kwargs)
    return Rule(**data)


def test_rule_requires_explicit_provenance_and_evidence():
    rule = _rule()
    rule.validate()
    assert rule.source.tier == "PROJECT_BASIS"
    assert rule.source.evidence_required is True


def test_missing_evidence_fails_closed():
    result = evaluate_rule(
        _rule(), source_sha256=SOURCE, model_id="pm-76",
        observed_status="PASS", observed_evidence_ids=()
    )
    assert result.status == "UNKNOWN"
    assert result.blockers == ("RULE_EVIDENCE_MISSING",)
    result.validate()


def test_no_observation_never_becomes_pass():
    result = evaluate_rule(
        _rule(), source_sha256=SOURCE, model_id="pm-76",
        observed_evidence_ids=("ev-door",)
    )
    assert result.status == "UNKNOWN"
    assert "RULE_OBSERVATION_MISSING" in result.blockers


def test_observed_pass_is_traceable():
    result = evaluate_rule(
        _rule(), source_sha256=SOURCE, model_id="pm-76",
        observed_status="PASS", observed_evidence_ids=("ev-door",)
    )
    assert result.status == "PASS"
    assert result.evidence_ids == ("ev-door",)
    assert result.blockers == ()
    result.validate()


def test_blocking_failure_is_blocked():
    result = evaluate_rule(
        _rule(), source_sha256=SOURCE, model_id="pm-76",
        observed_status="FAIL", observed_evidence_ids=("ev-door",)
    )
    assert result.status == "FAIL"
    assert result.blockers == ("RULE_FAILED",)


def test_ruleset_rejects_duplicate_rule_ids():
    rule = _rule()
    ruleset = RuleSet("iran-architecture", "1.0.0", (rule, rule))
    try:
        ruleset.validate()
    except ValueError as exc:
        assert str(exc) == "RULE_ID_DUPLICATE"
    else:
        raise AssertionError("duplicate rule ids must fail")


def test_invalid_source_identity_blocks():
    result = evaluate_rule(
        _rule(), source_sha256="bad", model_id="pm-76",
        observed_status="PASS", observed_evidence_ids=("ev-door",)
    )
    assert result.status == "BLOCKED"
    assert result.blockers == ("SOURCE_IDENTITY_INVALID",)


def test_project_basis_is_lower_priority_than_binding_regulation():
    binding = RuleSource("reg", "Binding regulation", "BINDING_REGULATION", "section-x")
    project = RuleSource("project", "Project basis", "PROJECT_BASIS", "note-x")
    assert binding.priority < project.priority
    ruleset = RuleSet("ordered", "1.0.0", (_rule(),))
    assert ruleset.ordered_rules()[0].source.priority == 6
