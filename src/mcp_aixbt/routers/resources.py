"""MCP Resource endpoints for read-only data access."""

from datetime import datetime
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from mcp_aixbt.clients.aixbt import AIXBTClient
from mcp_aixbt.config import Settings, get_settings
from mcp_aixbt.models.projects import Cluster, Project, ProjectMomentum, Signal
from mcp_aixbt.models.requests import MomentumFilters, ProjectFilters, SignalFilters
from mcp_aixbt.models.responses import APIResponse
from mcp_aixbt.services.projects import ProjectService
from mcp_aixbt.services.signals import SignalService
from mcp_aixbt.utils.errors import AIXBTError, NotFoundError

router = APIRouter(prefix="/resources", tags=["Resources"])


def get_aixbt_client(settings: Annotated[Settings, Depends(get_settings)]) -> AIXBTClient:
    """Get AIXBT client dependency."""
    return AIXBTClient(settings)


def get_project_service(
    client: Annotated[AIXBTClient, Depends(get_aixbt_client)]
) -> ProjectService:
    """Get project service dependency."""
    return ProjectService(client)


def get_signal_service(
    client: Annotated[AIXBTClient, Depends(get_aixbt_client)]
) -> SignalService:
    """Get signal service dependency."""
    return SignalService(client)


@router.get("/projects", response_model=APIResponse[list[Project]])
async def list_projects(
    service: Annotated[ProjectService, Depends(get_project_service)],
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=50),
    names: Optional[str] = Query(default=None, description="Comma-separated project names"),
    tickers: Optional[str] = Query(default=None, description="Comma-separated token tickers"),
    chain: Optional[str] = Query(default=None, description="Filter by blockchain"),
    min_momentum_score: Optional[float] = Query(
        default=None, ge=0, le=1, alias="minMomentumScore"
    ),
    sort_by: str = Query(default="momentumScore", alias="sortBy"),
) -> APIResponse[list[Project]]:
    """Get paginated list of projects with momentum scores and signals."""
    try:
        filters = ProjectFilters(
            page=page,
            limit=limit,
            names=names,
            tickers=tickers,
            chain=chain,
            min_momentum_score=min_momentum_score,
            sort_by=sort_by,
        )
        return await service.list_projects(filters)
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get("/projects/{project_id}", response_model=dict[str, Any])
async def get_project(
    project_id: str,
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> dict[str, Any]:
    """Get detailed information about a specific project."""
    try:
        project = await service.get_project(project_id)
        return {"status": 200, "data": project.model_dump(by_alias=True)}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get("/projects/{project_id}/momentum", response_model=dict[str, Any])
async def get_project_momentum(
    project_id: str,
    service: Annotated[ProjectService, Depends(get_project_service)],
    start: Optional[datetime] = Query(default=None, description="Start timestamp (ISO 8601)"),
    end: Optional[datetime] = Query(default=None, description="End timestamp (ISO 8601)"),
) -> dict[str, Any]:
    """Get hourly momentum history with cluster breakdown for a project."""
    try:
        filters = MomentumFilters(start=start, end=end)
        momentum = await service.get_momentum(project_id, filters)
        return {"status": 200, "data": momentum.model_dump(by_alias=True)}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get("/signals", response_model=APIResponse[list[Signal]])
async def list_signals(
    service: Annotated[SignalService, Depends(get_signal_service)],
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=50),
    categories: Optional[str] = Query(
        default=None, description="Comma-separated categories (e.g., WHALE_ACTIVITY,TECH_EVENT)"
    ),
    tickers: Optional[str] = Query(default=None, description="Comma-separated token tickers"),
    names: Optional[str] = Query(default=None, description="Comma-separated project names"),
    detected_after: Optional[datetime] = Query(
        default=None, alias="detectedAfter", description="Filter signals after this date"
    ),
    detected_before: Optional[datetime] = Query(
        default=None, alias="detectedBefore", description="Filter signals before this date"
    ),
) -> APIResponse[list[Signal]]:
    """Get paginated list of market signals with filtering support."""
    try:
        filters = SignalFilters(
            page=page,
            limit=limit,
            categories=categories,
            tickers=tickers,
            names=names,
            detected_after=detected_after,
            detected_before=detected_before,
        )
        return await service.list_signals(filters)
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get("/clusters", response_model=dict[str, Any])
async def list_clusters(
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> dict[str, Any]:
    """Get all tracked communities and information sources."""
    try:
        clusters = await service.list_clusters()
        return {
            "status": 200,
            "data": [c.model_dump(by_alias=True) for c in clusters],
        }
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get("/chains", response_model=dict[str, Any])
async def list_chains(
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> dict[str, Any]:
    """Get list of supported blockchain platforms for filtering."""
    try:
        chains = await service.list_chains()
        return {"status": 200, "data": chains}
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
