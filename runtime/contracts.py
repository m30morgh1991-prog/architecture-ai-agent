from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Element:
    element_id: str
    element_type: str
    state: str
    geometry: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlanModel:
    plan_id: str
    elements: List[Element]

@dataclass
class ChangeRequest:
    change_type: str
    target_ids: List[str]
    instruction: str

@dataclass
class ValidationResult:
    status: str
    failure_codes: List[str] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)

@dataclass
class ApprovedChangePlan:
    request: ChangeRequest
    approved_target_ids: List[str]
    status: str

@dataclass
class PostEditDiff:
    changed_ids: List[str]
    unauthorized_delta_ids: List[str]
    locked_delta_ids: List[str]
