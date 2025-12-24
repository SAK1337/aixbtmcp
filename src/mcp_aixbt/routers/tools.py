"""MCP Tool endpoints for executable actions."""

from typing import Annotated, Any, Optional

import httpx
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, Field

from mcp_aixbt.clients.aixbt import AIXBTClient
from mcp_aixbt.clients.x402 import X402Handler
from mcp_aixbt.config import Settings, get_settings
from mcp_aixbt.models.projects import Project, Signal
from mcp_aixbt.models.requests import (
    ChatMessage,
    IndigoRequest,
    ProjectFilters,
    SignalFilters,
    SurgingProjectsFilters,
)
from mcp_aixbt.models.responses import APIResponse
from mcp_aixbt.services.indigo import IndigoService
from mcp_aixbt.services.projects import ProjectService
from mcp_aixbt.services.signals import SignalService
from mcp_aixbt.utils.errors import AIXBTError, BudgetExceededError

router = APIRouter(prefix="/tools", tags=["Tools"])

X402_API_URL = "https://api.aixbt.tech"


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


def get_indigo_service(
    client: Annotated[AIXBTClient, Depends(get_aixbt_client)]
) -> IndigoService:
    """Get Indigo service dependency."""
    return IndigoService(client)


def get_x402_handler(settings: Annotated[Settings, Depends(get_settings)]) -> X402Handler:
    """Get x402 handler dependency."""
    return X402Handler(settings)


@router.post("/query-indigo")
async def query_indigo(
    service: Annotated[IndigoService, Depends(get_indigo_service)],
    request: IndigoRequest = Body(...),
) -> dict[str, Any]:
    """
    Chat with the AIXBT Indigo agent for real-time market insights.

    The Indigo agent provides narrative analysis, sentiment assessment,
    and market intelligence based on current crypto market data.
    """
    try:
        response_text = await service.chat(
            message=request.message,
            conversation_history=request.conversation_history,
        )
        return {"status": 200, "data": {"text": response_text}}
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


class ListProjectsRequest(ProjectFilters):
    """Request body for list-projects tool."""

    pass


@router.post("/list-projects", response_model=APIResponse[list[Project]])
async def list_projects(
    service: Annotated[ProjectService, Depends(get_project_service)],
    request: ListProjectsRequest = Body(default_factory=ListProjectsRequest),
) -> APIResponse[list[Project]]:
    """
    Search and filter crypto projects by various criteria.

    Returns projects with momentum scores, signals, and CoinGecko data.
    """
    try:
        filters = ProjectFilters(
            page=request.page,
            limit=request.limit,
            names=request.names,
            tickers=request.tickers,
            chain=request.chain,
            min_momentum_score=request.min_momentum_score,
            sort_by=request.sort_by,
            exclude_stables=request.exclude_stables,
        )
        return await service.list_projects(filters)
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


class GetSignalsRequest(SignalFilters):
    """Request body for get-signals tool."""

    pass


@router.post("/get-signals", response_model=APIResponse[list[Signal]])
async def get_signals(
    service: Annotated[SignalService, Depends(get_signal_service)],
    request: GetSignalsRequest = Body(default_factory=GetSignalsRequest),
) -> APIResponse[list[Signal]]:
    """
    Retrieve market signals filtered by category, project, or time range.

    Categories include: WHALE_ACTIVITY, TECH_EVENT, PARTNERSHIP, REGULATORY, etc.
    """
    try:
        filters = SignalFilters(
            page=request.page,
            limit=request.limit,
            categories=request.categories,
            tickers=request.tickers,
            names=request.names,
            detected_after=request.detected_after,
            detected_before=request.detected_before,
        )
        return await service.list_signals(filters)
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


class GetSurgingProjectsRequest(BaseModel):
    """Request body for get-surging-projects tool (x402)."""

    limit: int = Field(default=10, ge=1, le=50)
    min_score: Optional[float] = Field(default=None, alias="minScore")

    model_config = {"populate_by_name": True}


@router.post("/get-surging-projects")
async def get_surging_projects(
    handler: Annotated[X402Handler, Depends(get_x402_handler)],
    request: GetSurgingProjectsRequest = Body(default_factory=GetSurgingProjectsRequest),
) -> dict[str, Any]:
    """
    Get projects with surging momentum in real-time.

    **Note:** This endpoint requires x402 payment (USDC on Base chain).
    Requires EVM_PRIVATE_KEY to be configured.
    """
    try:
        params: dict[str, Any] = {"limit": request.limit}
        if request.min_score is not None:
            params["minScore"] = request.min_score

        async with httpx.AsyncClient(base_url=X402_API_URL, timeout=30.0) as client:
            response = await handler.fetch_with_payment(
                client,
                "GET",
                "/x402/v1/projects",
                params=params,
            )

            if response.status_code == 404:
                refund = handler.parse_refund(response.json())
                return {
                    "status": 404,
                    "error": "No surging projects found",
                    "data": {"refund": refund} if refund else {},
                }

            if response.status_code != 200:
                raise AIXBTError(
                    f"x402 request failed: {response.text}",
                    status_code=response.status_code,
                )

            return response.json()

    except BudgetExceededError as e:
        raise HTTPException(
            status_code=402,
            detail={"error": "Budget exceeded", "message": e.message, "limit_type": e.limit_type},
        )
    except AIXBTError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
