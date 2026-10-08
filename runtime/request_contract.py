from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class ExecutionRequest:
    execution_id: str
    project_id: str
    input_version_id: str
    plan_id: str
    request: Dict[str, Any]
    edit_permissions: List[Dict[str, Any]] = field(default_factory=list)
    uncertainty: List[Dict[str, Any]] = field(default_factory=list)
    impact_dependencies: List[Dict[str, Any]] = field(default_factory=list)
    source_profile: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, body: Dict[str, Any]):
        required = ("execution_id", "project_id", "input_version_id", "plan_id", "request")
        missing = [key for key in required if key not in body]
        if missing:
            raise ValueError("REQUEST_FIELD_MISSING:" + ",".join(missing))
        if not all(isinstance(body[key], str) and body[key] for key in required[:-1]):
            raise ValueError("REQUEST_ID_INVALID")
        if not isinstance(body["request"], dict):
            raise ValueError("REQUEST_OBJECT_INVALID")

        edit_permissions = body.get("edit_permissions", [])
        uncertainty = body.get("uncertainty", [])
        impact_dependencies = body.get("impact_dependencies", [])
        source_profile = body.get("source_profile", {})

        if not isinstance(edit_permissions, list):
            raise ValueError("EDIT_PERMISSIONS_INVALID")
        if not isinstance(uncertainty, list):
            raise ValueError("UNCERTAINTY_INVALID")
        if not isinstance(impact_dependencies, list):
            raise ValueError("IMPACT_DEPENDENCIES_INVALID")
        if not isinstance(source_profile, dict):
            raise ValueError("SOURCE_PROFILE_INVALID")

        return cls(
            *(body[key] for key in required),
            edit_permissions=edit_permissions,
            uncertainty=uncertainty,
            impact_dependencies=impact_dependencies,
            source_profile=source_profile,
        )

    def trace(self) -> Dict[str, str]:
        return {
            "execution_id": self.execution_id,
            "project_id": self.project_id,
            "input_version_id": self.input_version_id,
            "plan_id": self.plan_id,
        }

    def controlled_editing_context(self) -> Dict[str, Any]:
        return {
            "edit_permissions": self.edit_permissions,
            "uncertainty": self.uncertainty,
            "impact_dependencies": self.impact_dependencies,
            "source_profile": self.source_profile,
        }