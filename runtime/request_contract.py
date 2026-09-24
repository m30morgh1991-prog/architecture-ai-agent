from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ExecutionRequest:
    execution_id: str
    project_id: str
    input_version_id: str
    plan_id: str
    request: Dict[str, Any]

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
        return cls(*(body[key] for key in required))

    def trace(self) -> Dict[str, str]:
        return {
            "execution_id": self.execution_id,
            "project_id": self.project_id,
            "input_version_id": self.input_version_id,
            "plan_id": self.plan_id,
        }
