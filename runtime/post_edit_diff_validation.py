"""Post-edit diff and fail-closed validation contract."""
from dataclasses import dataclass
@dataclass(frozen=True)
class PostEditDiff:
    changed_ids: tuple[str,...]
    locked_changes: tuple[str,...]
    source_sha256: str
    model_id: str
    valid: bool
def build_post_edit_diff(*,changed_ids,locked_changes,source_sha256,model_id):
    valid=bool(source_sha256 and model_id) and not tuple(locked_changes)
    return PostEditDiff(tuple(changed_ids),tuple(locked_changes),source_sha256,model_id,valid)
