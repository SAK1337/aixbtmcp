"""Domain models for AIXBT projects and signals."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, field_validator


class SignalCategory(str, Enum):
    """Valid signal categories from AIXBT API."""

    FINANCIAL_EVENT = "FINANCIAL_EVENT"
    TOKEN_ECONOMICS = "TOKEN_ECONOMICS"
    TECH_EVENT = "TECH_EVENT"
    MARKET_ACTIVITY = "MARKET_ACTIVITY"
    ONCHAIN_METRICS = "ONCHAIN_METRICS"
    PARTNERSHIP = "PARTNERSHIP"
    TEAM_UPDATE = "TEAM_UPDATE"
    REGULATORY = "REGULATORY"
    WHALE_ACTIVITY = "WHALE_ACTIVITY"
    RISK_ALERT = "RISK_ALERT"
    VISIBILITY_EVENT = "VISIBILITY_EVENT"
    OPINION_SPECULATION = "OPINION_SPECULATION"


class Cluster(BaseModel):
    """Information cluster (tracked community or source)."""

    id: str
    name: str
    description: Optional[str] = None


class CoingeckoData(BaseModel):
    """CoinGecko metadata for a project."""

    api_id: Optional[str] = Field(default=None, alias="apiId")
    type: Optional[str] = None
    symbol: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    contract_address: Optional[str] = Field(default=None, alias="contractAddress")
    categories: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class Signal(BaseModel):
    """Market intelligence signal."""

    id: str
    detected_at: datetime = Field(alias="detectedAt")
    reinforced_at: Optional[datetime] = Field(default=None, alias="reinforcedAt")
    description: str
    project_name: str = Field(alias="projectName")
    project_id: str = Field(alias="projectId")
    category: Optional[SignalCategory] = None
    official_sources: list[str] = Field(default_factory=list, alias="officialSources")
    clusters: list[Cluster] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

    @field_validator("category", mode="before")
    @classmethod
    def parse_category(cls, v: Any) -> Optional[SignalCategory]:
        """Handle empty string or invalid category from API."""
        if v is None or v == "":
            return None
        if isinstance(v, SignalCategory):
            return v
        try:
            return SignalCategory(v)
        except ValueError:
            return None


class Project(BaseModel):
    """Cryptocurrency project with momentum data."""

    id: str
    name: str
    description: Optional[str] = None
    rationale: Optional[str] = None
    x_handle: Optional[str] = Field(default=None, alias="xHandle")
    momentum_score: float = Field(ge=0, le=1, alias="momentumScore")
    popularity_score: int = Field(ge=0, alias="popularityScore")
    coingecko_data: Optional[CoingeckoData] = Field(default=None, alias="coingeckoData")
    tokens: dict[str, str] = Field(default_factory=dict)
    signals: list[Signal] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

    @field_validator("tokens", mode="before")
    @classmethod
    def parse_tokens(cls, v: Any) -> dict[str, str]:
        """Handle empty list or invalid tokens from API."""
        if v is None or v == []:
            return {}
        if isinstance(v, dict):
            return v
        return {}


class ClusterCount(BaseModel):
    """Cluster with count for momentum breakdown."""

    id: str
    name: str
    count: int


class MomentumDataPoint(BaseModel):
    """Single point in momentum history."""

    timestamp: datetime
    momentum_score: float = Field(alias="momentumScore")
    clusters: list[ClusterCount] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ProjectMomentum(BaseModel):
    """Momentum history for a project."""

    project_id: str = Field(alias="projectId")
    project_name: str = Field(alias="projectName")
    data: list[MomentumDataPoint]

    model_config = {"populate_by_name": True}
