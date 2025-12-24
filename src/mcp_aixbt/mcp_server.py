"""MCP stdio server for AIXBT market intelligence."""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceTemplate,
)

from mcp_aixbt.clients.aixbt import AIXBTClient
from mcp_aixbt.config import get_settings
from mcp_aixbt.models.projects import Project, Signal
from mcp_aixbt.models.requests import ProjectFilters, SignalFilters

# Create MCP server instance
server = Server("mcp-aixbt")

# Global client instance
_client: AIXBTClient | None = None


def get_client() -> AIXBTClient:
    """Get or create AIXBT client."""
    global _client
    if _client is None:
        settings = get_settings()
        _client = AIXBTClient(settings)
    return _client


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="list-projects",
            description="Search and filter crypto projects by various criteria. Returns projects with momentum scores, signals, and CoinGecko data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                    "names": {"type": "string", "description": "Comma-separated project names"},
                    "tickers": {"type": "string", "description": "Comma-separated token tickers"},
                    "chain": {"type": "string", "description": "Filter by blockchain"},
                    "minMomentumScore": {"type": "number", "minimum": 0, "maximum": 1},
                    "sortBy": {"type": "string", "default": "momentumScore"},
                },
            },
        ),
        Tool(
            name="get-signals",
            description="Retrieve market signals filtered by category, project, or time range. Categories: WHALE_ACTIVITY, TECH_EVENT, PARTNERSHIP, REGULATORY, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                    "categories": {"type": "string", "description": "Comma-separated categories"},
                    "tickers": {"type": "string", "description": "Comma-separated token tickers"},
                    "names": {"type": "string", "description": "Comma-separated project names"},
                },
            },
        ),
        Tool(
            name="query-indigo",
            description="Chat with the AIXBT Indigo agent for real-time market insights and narrative analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Your question or message for Indigo",
                        "minLength": 1,
                        "maxLength": 10000,
                    },
                },
                "required": ["message"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    client = get_client()

    try:
        if name == "list-projects":
            filters = ProjectFilters(
                page=arguments.get("page", 1),
                limit=arguments.get("limit", 10),
                names=arguments.get("names"),
                tickers=arguments.get("tickers"),
                chain=arguments.get("chain"),
                min_momentum_score=arguments.get("minMomentumScore"),
                sort_by=arguments.get("sortBy", "momentumScore"),
            )
            result = await client.list_projects(filters)
            return [TextContent(
                type="text",
                text=_format_projects(result.data, result.pagination),
            )]

        elif name == "get-signals":
            filters = SignalFilters(
                page=arguments.get("page", 1),
                limit=arguments.get("limit", 10),
                categories=arguments.get("categories"),
                tickers=arguments.get("tickers"),
                names=arguments.get("names"),
            )
            result = await client.list_signals(filters)
            return [TextContent(
                type="text",
                text=_format_signals(result.data, result.pagination),
            )]

        elif name == "query-indigo":
            message = arguments.get("message", "")
            result = await client.chat_with_indigo([{"role": "user", "content": message}])
            return [TextContent(
                type="text",
                text=result,
            )]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available MCP resources."""
    return [
        Resource(
            uri="aixbt://chains",
            name="Supported Chains",
            description="List of supported blockchain platforms",
            mimeType="application/json",
        ),
        Resource(
            uri="aixbt://clusters",
            name="Information Clusters",
            description="Tracked communities and information sources",
            mimeType="application/json",
        ),
    ]


@server.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """List resource templates for dynamic resources."""
    return [
        ResourceTemplate(
            uriTemplate="aixbt://projects/{project_id}",
            name="Project Details",
            description="Get detailed information about a specific project",
            mimeType="application/json",
        ),
        ResourceTemplate(
            uriTemplate="aixbt://projects/{project_id}/momentum",
            name="Project Momentum",
            description="Get momentum history for a project",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI."""
    import json
    client = get_client()

    try:
        if uri == "aixbt://chains":
            result = await client.list_chains()
            return json.dumps(result, indent=2)

        elif uri == "aixbt://clusters":
            result = await client.list_clusters()
            return json.dumps([c.model_dump() for c in result], indent=2)

        elif uri.startswith("aixbt://projects/"):
            parts = uri.replace("aixbt://projects/", "").split("/")
            project_id = parts[0]

            if len(parts) == 1:
                result = await client.get_project(project_id)
                return json.dumps(result.model_dump(), indent=2)
            elif len(parts) == 2 and parts[1] == "momentum":
                result = await client.get_momentum(project_id)
                return json.dumps(result.model_dump(), indent=2)

        return json.dumps({"error": f"Unknown resource: {uri}"})

    except Exception as e:
        return json.dumps({"error": str(e)})


def _format_projects(projects: list[Project], pagination: Any) -> str:
    """Format projects for text output."""
    lines = [f"Found {pagination.total_count} projects (page {pagination.page})\n"]

    for p in projects:
        lines.append(f"## {p.name}")
        lines.append(f"- Momentum Score: {p.momentum_score:.2%}")
        lines.append(f"- Popularity: {p.popularity_score}")
        if p.rationale:
            lines.append(f"- Rationale: {p.rationale}")
        if p.x_handle:
            lines.append(f"- Twitter: @{p.x_handle}")
        if p.signals:
            lines.append(f"- Recent Signals: {len(p.signals)}")
        lines.append("")

    return "\n".join(lines)


def _format_signals(signals: list[Signal], pagination: Any) -> str:
    """Format signals for text output."""
    lines = [f"Found {pagination.total_count} signals (page {pagination.page})\n"]

    for s in signals:
        category = s.category.value if s.category else "UNKNOWN"
        lines.append(f"## [{category}] {s.project_name}")
        lines.append(f"- {s.description}")
        lines.append(f"- Detected: {s.detected_at.strftime('%Y-%m-%d %H:%M')}")
        if s.clusters:
            cluster_names = ", ".join(c.name for c in s.clusters)
            lines.append(f"- Sources: {cluster_names}")
        lines.append("")

    return "\n".join(lines)


async def run_server() -> None:
    """Run the MCP stdio server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """Entry point for MCP stdio server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
