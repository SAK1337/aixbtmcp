"""Indigo chat service layer."""

from typing import Optional

from mcp_aixbt.clients.aixbt import AIXBTClient
from mcp_aixbt.models.requests import ChatMessage
from mcp_aixbt.utils.errors import NotFoundError


class IndigoService:
    """Service for Indigo agent interactions."""

    def __init__(self, client: AIXBTClient) -> None:
        self._client = client

    async def chat(
        self,
        message: str,
        conversation_history: Optional[list[ChatMessage]] = None,
    ) -> str:
        """Chat with the Indigo agent."""
        messages: list[dict[str, str]] = []

        if conversation_history:
            for msg in conversation_history:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": message})

        try:
            return await self._client.chat_with_indigo(messages)
        except NotFoundError:
            return "No relevant information found for your query."
