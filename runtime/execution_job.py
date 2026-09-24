from dataclasses import dataclass, field
from typing import Any, Dict, Optional


JOB_STATES = {
    "QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "BLOCKED", "CANCELLED"
}


@dataclass
class ExecutionJob:
    job_id: str
    project_id: str
    execution_id: str
    state: str = "QUEUED"
    current_stage: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExecutionJobStore:
    """Small provider-neutral job state boundary.

    Persistence is intentionally left to a future backend adapter. The store
    enforces valid state transitions and keeps execution identity separate from
    project/version identity.
    """

    TRANSITIONS = {
        "QUEUED": {"RUNNING", "CANCELLED"},
        "RUNNING": {"SUCCEEDED", "FAILED", "BLOCKED", "CANCELLED"},
        "SUCCEEDED": set(),
        "FAILED": set(),
        "BLOCKED": set(),
        "CANCELLED": set(),
    }

    def __init__(self):
        self._jobs: Dict[str, ExecutionJob] = {}

    def create(self, job_id: str, project_id: str, execution_id: str) -> ExecutionJob:
        if job_id in self._jobs:
            raise ValueError("JOB_ID_ALREADY_EXISTS")
        job = ExecutionJob(job_id, project_id, execution_id)
        self._jobs[job_id] = job
        return job

    def transition(
        self,
        job_id: str,
        new_state: str,
        *,
        current_stage: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
    ) -> ExecutionJob:
        if new_state not in JOB_STATES:
            raise ValueError("INVALID_JOB_STATE")
        job = self.get(job_id)
        if new_state not in self.TRANSITIONS[job.state]:
            raise ValueError(f"INVALID_JOB_TRANSITION:{job.state}->{new_state}")
        job.state = new_state
        if current_stage is not None:
            job.current_stage = current_stage
        if result is not None:
            job.result = result
        if error is not None:
            job.error = error
        return job

    def get(self, job_id: str) -> ExecutionJob:
        try:
            return self._jobs[job_id]
        except KeyError:
            raise KeyError("JOB_NOT_FOUND") from None


class ExecutionApiBoundary:
    """Maps product/API operations to the provider-neutral job store."""

    def __init__(self, store: Optional[ExecutionJobStore] = None):
        self.store = store or ExecutionJobStore()

    def submit(self, project_id: str, execution_id: str, job_id: str) -> Dict[str, Any]:
        job = self.store.create(job_id, project_id, execution_id)
        return self._public(job)

    def start(self, job_id: str, stage: str) -> Dict[str, Any]:
        return self._public(
            self.store.transition(job_id, "RUNNING", current_stage=stage)
        )

    def complete(self, job_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        return self._public(
            self.store.transition(job_id, "SUCCEEDED", result=result)
        )

    def fail(self, job_id: str, error: Dict[str, Any]) -> Dict[str, Any]:
        return self._public(
            self.store.transition(job_id, "FAILED", error=error)
        )

    def block(self, job_id: str, error: Dict[str, Any]) -> Dict[str, Any]:
        return self._public(
            self.store.transition(job_id, "BLOCKED", error=error)
        )

    def cancel(self, job_id: str) -> Dict[str, Any]:
        return self._public(self.store.transition(job_id, "CANCELLED"))

    def get(self, job_id: str) -> Dict[str, Any]:
        return self._public(self.store.get(job_id))

    @staticmethod
    def _public(job: ExecutionJob) -> Dict[str, Any]:
        return {
            "job_id": job.job_id,
            "project_id": job.project_id,
            "execution_id": job.execution_id,
            "state": job.state,
            "current_stage": job.current_stage,
            "result": job.result,
            "error": job.error,
            "metadata": job.metadata,
        }
