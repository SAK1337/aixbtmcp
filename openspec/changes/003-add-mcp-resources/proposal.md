# Change: Add MCP Resource Endpoints

## Why
MCP Resources represent read-only data that AI assistants can access as context. This proposal exposes AIXBT's market data through standardized resource endpoints following the MCP pattern, enabling Claude and other LLMs to query projects, signals, clusters, and chains.

## What Changes
- Create `src/mcp_aixbt/routers/resources.py` with FastAPI routes
- Create `src/mcp_aixbt/services/projects.py` for business logic
- Create `src/mcp_aixbt/services/signals.py` for signal queries
- Expose 6 resource endpoints: projects, project detail, signals, momentum, clusters, chains
- Implement pagination support for list endpoints

## Impact
- Affected specs: `mcp-resources` (new capability)
- Affected code: `src/mcp_aixbt/routers/`, `src/mcp_aixbt/services/`
- Dependencies: Requires `002-add-aixbt-client` to be completed first

## Sequence
**Proposal 3 of 7** - Depends on proposals 001 and 002.

## References
- `ApplicationSpecificationFinal.md` Section 5.2 (MCP Resources)
- `ApplicationSpecificationFinal.md` Section 6.2 (Python Implementation)
