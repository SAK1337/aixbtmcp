"""Project service layer."""

from typing import Optional

from mcp_aixbt.clients.aixbt import AIXBTClient
from mcp_aixbt.models.projects import Cluster, Project, ProjectMomentum
from mcp_aixbt.models.requests import MomentumFilters, ProjectFilters
from mcp_aixbt.models.responses import APIResponse


class ProjectService:
    """Service for project-related operations."""

    def __init__(self, client: AIXBTClient) -> None:
        self._client = client

    async def list_projects(
        self, filters: Optional[ProjectFilters] = None
    ) -> APIResponse[list[Project]]:
        """Get paginated list of projects."""
        return await self._client.list_projects(filters)

    async def get_project(self, project_id: str) -> Project:
        """Get a single project by ID."""
        return await self._client.get_project(project_id)

    async def get_momentum(
        self, project_id: str, filters: Optional[MomentumFilters] = None
    ) -> ProjectMomentum:
        """Get momentum history for a project."""
        return await self._client.get_momentum(project_id, filters)

    async def list_clusters(self) -> list[Cluster]:
        """Get all clusters."""
        return await self._client.list_clusters()

    async def list_chains(self) -> list[str]:
        """Get all supported chains."""
        return await self._client.list_chains()
