"""Request models for API endpoints."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Message in a conversation with Indigo."""

    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=10000)


class IndigoRequest(BaseModel):
    """Request to chat with Indigo agent."""

    message: str = Field(min_length=1, max_length=10000)
    conversation_history: Optional[list[ChatMessage]] = None


class ProjectFilters(BaseModel):
    """Filters for project list endpoint."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=50, ge=1, le=50)
    project_ids: Optional[str] = Field(default=None, alias="projectIds")
    names: Optional[str] = None
    x_handles: Optional[str] = Field(default=None, alias="xHandles")
    tickers: Optional[str] = None
    chain: Optional[str] = None
    min_momentum_score: Optional[float] = Field(default=None, ge=0, le=1, alias="minMomentumScore")
    sort_by: str = Field(default="momentumScore", alias="sortBy")
    exclude_stables: bool = Field(default=False, alias="excludeStables")

    model_config = {"populate_by_name": True}


class SignalFilters(BaseModel):
    """Filters for signals list endpoint."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=50, ge=1, le=50)
    project_ids: Optional[str] = Field(default=None, alias="projectIds")
    names: Optional[str] = None
    x_handles: Optional[str] = Field(default=None, alias="xHandles")
    tickers: Optional[str] = None
    cluster_ids: Optional[str] = Field(default=None, alias="clusterIds")
    categories: Optional[str] = None
    detected_after: Optional[datetime] = Field(default=None, alias="detectedAfter")
    detected_before: Optional[datetime] = Field(default=None, alias="detectedBefore")
    reinforced_after: Optional[datetime] = Field(default=None, alias="reinforcedAfter")
    reinforced_before: Optional[datetime] = Field(default=None, alias="reinforcedBefore")

    model_config = {"populate_by_name": True}


class MomentumFilters(BaseModel):
    """Filters for momentum history endpoint."""

    start: Optional[datetime] = None
    end: Optional[datetime] = None


class SurgingProjectsFilters(BaseModel):
    """Filters for surging projects (x402 endpoint)."""

    limit: int = Field(default=50, ge=1, le=50)
    name: Optional[str] = None
    ticker: Optional[str] = None
    x_handle: Optional[str] = Field(default=None, alias="xHandle")
    sort_by: str = Field(default="score", alias="sortBy")
    min_score: Optional[float] = Field(default=None, alias="minScore")

    model_config = {"populate_by_name": True}
