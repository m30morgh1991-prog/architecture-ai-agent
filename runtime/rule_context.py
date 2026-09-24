"""H26 provider-neutral regulatory context contract."""
from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class ProjectRuleContext:
    jurisdiction: str
    project_type: str
    authority_scope: List[str] = field(default_factory=list)
    source_ids: List[str] = field(default_factory=list)
    version: str = ""

    def validate(self) -> None:
        if not self.jurisdiction or not self.project_type:
            raise ValueError("RULE_CONTEXT_SCOPE_MISSING")
        if not self.source_ids or not self.version:
            raise ValueError("RULE_CONTEXT_SOURCE_MISSING")

@dataclass(frozen=True)
class ApplicableRule:
    rule_id: str
    source_id: str
    version: str
    applicability: str
    requirement: str

    def validate(self) -> None:
        if not all([self.rule_id,self.source_id,self.version,self.applicability,self.requirement]):
            raise ValueError("RULE_EVIDENCE_INCOMPLETE")
