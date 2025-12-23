"""Signal service layer."""

from typing import Optional

from mcp_aixbt.clients.aixbt import AIXBTClient
from mcp_aixbt.models.projects import Signal
from mcp_aixbt.models.requests import SignalFilters
from mcp_aixbt.models.responses import APIResponse


class SignalService:
    """Service for signal-related operations."""

    def __init__(self, client: AIXBTClient) -> None:
        self._client = client

    async def list_signals(
        self, filters: Optional[SignalFilters] = None
    ) -> APIResponse[list[Signal]]:
        """Get paginated list of signals."""
        return await self._client.list_signals(filters)
