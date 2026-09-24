"""H24 logical post-edit diff contract."""
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Delta:
    element_id: str
    attribute: str
    before: str
    after: str
    authorized: bool = False


@dataclass(frozen=True)
class PostEditDiff:
    diff_id: str
    source_version_id: str
    post_edit_version_id: str
    deltas: List[Delta] = field(default_factory=list)

    def validate(self) -> None:
        if not self.diff_id or not self.source_version_id or not self.post_edit_version_id:
            raise ValueError("POST_EDIT_DIFF_TRACEABILITY_MISSING")
        for d in self.deltas:
            if not d.element_id or not d.attribute:
                raise ValueError("POST_EDIT_DELTA_INVALID")

    @property
    def unauthorized_deltas(self) -> List[Delta]:
        self.validate()
        return [d for d in self.deltas if not d.authorized]

    @property
    def clean(self) -> bool:
        return not self.unauthorized_deltas
