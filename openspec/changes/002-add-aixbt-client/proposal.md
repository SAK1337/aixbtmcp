# Change: Add AIXBT REST API Client

## Why
The MCP server needs to communicate with the AIXBT API to fetch market intelligence data. This proposal implements the HTTP client layer with proper authentication, error handling, rate limit awareness, and domain models for all AIXBT data structures.

## What Changes
- Create `src/mcp_aixbt/clients/aixbt.py` with async HTTP client
- Implement API key authentication via `x-api-key` header
- Add rate limit handling with retry logic
- Create domain models in `src/mcp_aixbt/models/projects.py` and `signals.py`
- Add caching utility in `src/mcp_aixbt/utils/cache.py`

## Impact
- Affected specs: `aixbt-client` (new capability)
- Affected code: `src/mcp_aixbt/clients/`, `src/mcp_aixbt/models/`, `src/mcp_aixbt/utils/`
- Dependencies: Requires `001-scaffold-project` to be completed first

## Sequence
**Proposal 2 of 7** - Depends on proposal 001 (project foundation).

## References
- `ApplicationSpecificationFinal.md` Section 4.3 (REST API Endpoints)
- `ApplicationSpecificationFinal.md` Section 8.2 (Domain Models)
- `openspec/project.md` Domain Context (AIXBT API Structure)
