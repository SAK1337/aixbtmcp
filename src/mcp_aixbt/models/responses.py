"""Response models for API endpoints."""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Pagination(BaseModel):
    """Pagination metadata for list responses."""

    page: int
    limit: int
    total_count: int = Field(alias="totalCount")
    has_more: bool = Field(alias="hasMore")

    model_config = {"populate_by_name": True}


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    status: int
    data: T
    error: Optional[str] = None
    pagination: Optional[Pagination] = None


class ErrorResponse(BaseModel):
    """Error response structure."""

    status: int
    error: str
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[dict[str, Any]] = None


class HealthStatus(BaseModel):
    """Health check response."""

    status: str = Field(pattern="^(healthy|unhealthy)$")
    timestamp: datetime
    version: str
    checks: dict[str, Any] = Field(default_factory=dict)
