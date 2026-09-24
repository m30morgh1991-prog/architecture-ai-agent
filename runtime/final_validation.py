from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class FinalValidationResult:
    status: str
    failure_codes: list[str]
    checks: dict[str, Any]

def validate_post_edit(post_edit_diff: dict[str, Any]) -> FinalValidationResult:
    locked = post_edit_diff.get("locked_delta_ids", [])
    unauthorized = post_edit_diff.get("unauthorized_delta_ids", [])
    if locked:
        return FinalValidationResult("REJECT", ["POST_EDIT_REJECTED"], {
            "locked_delta_clear": False, "unauthorized_delta_clear": not unauthorized
        })
    if unauthorized:
        return FinalValidationResult("REJECT", ["POST_EDIT_UNAUTHORIZED_DELTA"], {
            "locked_delta_clear": True, "unauthorized_delta_clear": False
        })
    return FinalValidationResult("PASS", [], {
        "locked_delta_clear": True, "unauthorized_delta_clear": True
    })
