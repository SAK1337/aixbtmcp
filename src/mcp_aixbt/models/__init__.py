"""Pydantic models for MCP AIXBT Server."""

from mcp_aixbt.models.projects import (
    Cluster,
    ClusterCount,
    CoingeckoData,
    MomentumDataPoint,
    Project,
    ProjectMomentum,
    Signal,
    SignalCategory,
)
from mcp_aixbt.models.requests import (
    ChatMessage,
    IndigoRequest,
    MomentumFilters,
    ProjectFilters,
    SignalFilters,
    SurgingProjectsFilters,
)
from mcp_aixbt.models.responses import (
    APIResponse,
    ErrorResponse,
    HealthStatus,
    Pagination,
)

__all__ = [
    # Domain models
    "Cluster",
    "ClusterCount",
    "CoingeckoData",
    "MomentumDataPoint",
    "Project",
    "ProjectMomentum",
    "Signal",
    "SignalCategory",
    # Request models
    "ChatMessage",
    "IndigoRequest",
    "MomentumFilters",
    "ProjectFilters",
    "SignalFilters",
    "SurgingProjectsFilters",
    # Response models
    "APIResponse",
    "ErrorResponse",
    "HealthStatus",
    "Pagination",
]
