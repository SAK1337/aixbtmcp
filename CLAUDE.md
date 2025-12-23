# MCP AIXBT Server

A Model Context Protocol (MCP) server that wraps the AIXBT cryptocurrency intelligence API, enabling AI assistants to access real-time crypto market insights.

## Project Overview

- **Purpose**: Bridge between AIXBT API and MCP-compatible AI clients
- **Architecture**: FastAPI server with layered design (routers → services → clients)
- **Status**: In development - see `openspec/changes/` for implementation proposals

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- httpx (async HTTP client)
- Pydantic v2 (data validation)
- structlog (structured logging)
- eth-account + web3.py (x402 payments)

## Key Files

- `ApplicationSpecificationFinal.md` - Complete application specification
- `openspec/project.md` - Project context and domain knowledge
- `openspec/changes/` - Implementation proposals (001-007)
- `documentation/` - Official AIXBT API documentation

## Development Commands

```bash
# Install dependencies
pip install -e ".[dev]"

# Run server
uvicorn src.mcp_aixbt.main:app --reload

# Run tests
pytest

# Type checking
mypy src/

# Linting
ruff check src/
```

## Conventions

- Use `async/await` for all I/O operations
- Pydantic models for all request/response schemas
- Environment variables for configuration (via pydantic-settings)
- Structured logging with request ID correlation
- TTL-based caching (5 min default, 1 min for volatile data)

## API Authentication

- **Standard endpoints**: `x-api-key` header with AIXBT API key
- **Premium endpoints**: x402 payment protocol (HTTP 402 + EIP-712 signatures)

## Implementation Sequence

1. `001-scaffold-project` - Foundation
2. `002-add-aixbt-client` - HTTP client
3. `003-add-mcp-resources` - GET endpoints
4. `004-add-mcp-tools` - POST endpoints
5. `005-add-x402-handler` - Payments (optional)
6. `006-add-observability` - Health/logging
7. `007-add-docker-deployment` - Containers

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->