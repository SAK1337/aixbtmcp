"""AIXBT REST API client."""

import asyncio
from datetime import datetime
from typing import Any, Optional

import httpx

from mcp_aixbt.config import Settings
from mcp_aixbt.models.projects import Cluster, Project, ProjectMomentum, Signal
from mcp_aixbt.models.requests import MomentumFilters, ProjectFilters, SignalFilters
from mcp_aixbt.models.responses import APIResponse, Pagination
from mcp_aixbt.utils.cache import TTLCache, make_cache_key
from mcp_aixbt.utils.errors import AIXBTError, AuthenticationError, NotFoundError, RateLimitError

AIXBT_API_URL = "https://api.aixbt.tech"


class AIXBTClient:
    """Async HTTP client for AIXBT REST API."""

    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.aixbt_api_key.get_secret_value()
        self._cache = TTLCache(default_ttl_seconds=settings.cache_ttl_seconds)
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=AIXBT_API_URL,
                headers={"x-api-key": self._api_key},
                timeout=30.0,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle API response and errors."""
        if response.status_code == 401:
            raise AuthenticationError()

        if response.status_code == 404:
            raise NotFoundError()

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after) if retry_after else None,
            )

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", "Unknown error")
            except Exception:
                error_msg = response.text or "Unknown error"
            raise AIXBTError(error_msg, status_code=response.status_code)

        return response.json()

    async def _request_with_retry(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> dict[str, Any]:
        """Make request with retry logic for rate limits."""
        client = await self._get_client()

        for attempt in range(max_retries):
            try:
                response = await client.request(method, path, params=params, json=json)
                return await self._handle_response(response)
            except RateLimitError as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = e.retry_after or (2**attempt)
                await asyncio.sleep(wait_time)

        raise AIXBTError("Max retries exceeded")

    def _build_params(self, filters: Any) -> dict[str, Any]:
        """Build query parameters from filter model."""
        params = {}
        for field_name, field_info in filters.model_fields.items():
            value = getattr(filters, field_name)
            if value is not None:
                # Use alias if available
                alias = field_info.alias or field_name
                if isinstance(value, datetime):
                    params[alias] = value.isoformat()
                elif isinstance(value, bool):
                    params[alias] = str(value).lower()
                else:
                    params[alias] = value
        return params

    async def list_projects(
        self, filters: Optional[ProjectFilters] = None
    ) -> APIResponse[list[Project]]:
        """Get paginated list of projects."""
        filters = filters or ProjectFilters()
        cache_key = make_cache_key("projects", **self._build_params(filters))

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        params = self._build_params(filters)
        data = await self._request_with_retry("GET", "/v2/projects", params=params)

        projects = [Project.model_validate(p) for p in data.get("data", [])]
        pagination = None
        if "pagination" in data:
            pagination = Pagination.model_validate(data["pagination"])

        result = APIResponse(
            status=data.get("status", 200),
            data=projects,
            pagination=pagination,
        )

        self._cache.set(cache_key, result)
        return result

    async def get_project(self, project_id: str) -> Project:
        """Get a single project by ID."""
        cache_key = make_cache_key("project", project_id)

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        data = await self._request_with_retry("GET", f"/v2/projects/{project_id}")
        project = Project.model_validate(data.get("data", {}))

        self._cache.set(cache_key, project)
        return project

    async def list_signals(
        self, filters: Optional[SignalFilters] = None
    ) -> APIResponse[list[Signal]]:
        """Get paginated list of signals."""
        filters = filters or SignalFilters()
        cache_key = make_cache_key("signals", **self._build_params(filters))

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        params = self._build_params(filters)
        data = await self._request_with_retry("GET", "/v2/signals", params=params)

        signals = [Signal.model_validate(s) for s in data.get("data", [])]
        pagination = None
        if "pagination" in data:
            pagination = Pagination.model_validate(data["pagination"])

        result = APIResponse(
            status=data.get("status", 200),
            data=signals,
            pagination=pagination,
        )

        self._cache.set(cache_key, result)
        return result

    async def get_momentum(
        self, project_id: str, filters: Optional[MomentumFilters] = None
    ) -> ProjectMomentum:
        """Get momentum history for a project."""
        filters = filters or MomentumFilters()
        params = {}
        if filters.start:
            params["start"] = filters.start.isoformat()
        if filters.end:
            params["end"] = filters.end.isoformat()

        cache_key = make_cache_key("momentum", project_id, **params)

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        data = await self._request_with_retry(
            "GET", f"/v2/projects/{project_id}/momentum", params=params
        )
        momentum = ProjectMomentum.model_validate(data.get("data", {}))

        self._cache.set(cache_key, momentum)
        return momentum

    async def list_clusters(self) -> list[Cluster]:
        """Get all clusters."""
        cache_key = "clusters"

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        data = await self._request_with_retry("GET", "/v2/clusters")
        clusters = [Cluster.model_validate(c) for c in data.get("data", [])]

        self._cache.set(cache_key, clusters)
        return clusters

    async def list_chains(self) -> list[str]:
        """Get all supported chains."""
        cache_key = "chains"

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        data = await self._request_with_retry("GET", "/v2/projects/chains")
        chains = data.get("data", [])

        self._cache.set(cache_key, chains)
        return chains

    async def chat_with_indigo(
        self, messages: list[dict[str, str]]
    ) -> str:
        """Chat with the Indigo agent."""
        data = await self._request_with_retry(
            "POST",
            "/v2/agents/indigo",
            json={"messages": messages},
        )
        return data.get("data", {}).get("text", "")
