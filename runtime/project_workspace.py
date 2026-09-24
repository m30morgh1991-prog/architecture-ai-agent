from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .contracts import PlanModel, ChangeRequest


@dataclass
class ProjectVersion:
    version_id: str
    status: str
    plan_id: str
    source_version_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectWorkspace:
    project_id: str
    name: str
    active_version_id: Optional[str] = None
    versions: List[ProjectVersion] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)


class ProjectWorkspaceAdapter:
    """In-memory boundary for the Project-Centric product model.

    This adapter deliberately does not persist to a database yet. Its job is to
    define the stable boundary between Project Workspace state and the
    deterministic runtime without allowing the workspace layer to bypass
    validation or mutate approved history silently.
    """

    def create_project(self, project_id: str, name: str) -> ProjectWorkspace:
        return ProjectWorkspace(project_id=project_id, name=name)

    def attach_plan(
        self,
        workspace: ProjectWorkspace,
        plan: PlanModel,
        version_id: str,
        status: str = "WORKING",
        source_version_id: Optional[str] = None,
    ) -> ProjectVersion:
        version = ProjectVersion(
            version_id=version_id,
            status=status,
            plan_id=plan.plan_id,
            source_version_id=source_version_id,
        )
        workspace.versions.append(version)
        workspace.active_version_id = version_id
        return version

    def record_change_request(
        self,
        workspace: ProjectWorkspace,
        request: ChangeRequest,
    ) -> None:
        workspace.context.setdefault("change_requests", []).append(
            {
                "change_type": request.change_type,
                "target_ids": list(request.target_ids),
                "instruction": request.instruction,
            }
        )

    def promote_validated_version(
        self,
        workspace: ProjectWorkspace,
        version_id: str,
    ) -> ProjectVersion:
        version = self._get_version(workspace, version_id)
        if version.status != "VALIDATED":
            raise ValueError("Only VALIDATED versions can become the active approved state")
        workspace.active_version_id = version_id
        return version

    def _get_version(self, workspace: ProjectWorkspace, version_id: str) -> ProjectVersion:
        for version in workspace.versions:
            if version.version_id == version_id:
                return version
        raise KeyError(f"Unknown version: {version_id}")
