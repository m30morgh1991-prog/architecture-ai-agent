"""H30 production readiness gate."""
from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class ProductionReadiness:
    required_checks: List[str]
    passed_checks: List[str]=field(default_factory=list)
    blockers: List[str]=field(default_factory=list)

    def validate(self)->None:
        if not self.required_checks:
            raise ValueError("RELEASE_CHECKS_MISSING")
        if not set(self.passed_checks).issubset(set(self.required_checks)):
            raise ValueError("RELEASE_CHECK_NOT_DECLARED")

    @property
    def ready(self)->bool:
        self.validate()
        return len(self.passed_checks)==len(set(self.required_checks)) and not self.blockers
