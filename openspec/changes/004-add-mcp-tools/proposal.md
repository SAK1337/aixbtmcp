# Change: Add MCP Tool Endpoints

## Why
MCP Tools are executable functions that AI assistants can call to perform actions or queries with dynamic arguments. This proposal implements the action-oriented endpoints including the Indigo AI chat, project search, and signal retrieval tools.

## What Changes
- Create `src/mcp_aixbt/routers/tools.py` with FastAPI POST routes
- Create `src/mcp_aixbt/services/indigo.py` for Indigo chat service
- Implement `query_indigo` tool with conversation history support
- Implement `list_projects` and `get_signals` tools with dynamic filtering
- Add request models in `src/mcp_aixbt/models/requests.py`

## Impact
- Affected specs: `mcp-tools` (new capability)
- Affected code: `src/mcp_aixbt/routers/tools.py`, `src/mcp_aixbt/services/indigo.py`
- Dependencies: Requires `002-add-aixbt-client` and `003-add-mcp-resources`

## Sequence
**Proposal 4 of 7** - Depends on proposals 001, 002, and 003.

## References
- `ApplicationSpecificationFinal.md` Section 5.3 (MCP Tools)
- `ApplicationSpecificationFinal.md` Section 4.3.7 (Chat with Indigo)
