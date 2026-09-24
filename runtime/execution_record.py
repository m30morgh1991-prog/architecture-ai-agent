from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class ExecutionRecord:
    execution_id: str
    project_id: str
    input_version_id: str
    state: str
    result_reference: Optional[str] = None
    error: Optional[Dict[str, Any]] = None


class ExecutionRecordStore:
    """Provider-neutral execution record boundary.

    In-memory persistence for MVP; a database adapter can replace this store
    without changing API/runtime contracts.
    """

    def __init__(self):
        self._records: Dict[str, ExecutionRecord] = {}

    def create(self, execution_id: str, project_id: str,
               input_version_id: str) -> ExecutionRecord:
        if execution_id in self._records:
            raise ValueError("DUPLICATE_EXECUTION_ID")
        record = ExecutionRecord(
            execution_id, project_id, input_version_id, "QUEUED"
        )
        self._records[execution_id] = record
        return record

    def update(self, execution_id: str, state: str,
               result_reference: Optional[str] = None,
               error: Optional[Dict[str, Any]] = None) -> ExecutionRecord:
        record = self.get(execution_id)
        record.state = state
        if result_reference is not None:
            record.result_reference = result_reference
        if error is not None:
            record.error = error
        return record

    def get(self, execution_id: str) -> ExecutionRecord:
        if execution_id not in self._records:
            raise KeyError("EXECUTION_RECORD_NOT_FOUND")
        return self._records[execution_id]

    def public(self, execution_id: str) -> Dict[str, Any]:
        return asdict(self.get(execution_id))
