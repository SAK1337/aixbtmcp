# Tasks: Scaffold MCP AIXBT Server Project Foundation

## 1. Project Setup
- [ ] 1.1 Create `src/mcp_aixbt/` package directory structure
- [ ] 1.2 Create `__init__.py` files for all packages
- [ ] 1.3 Create `pyproject.toml` with project metadata and tool configurations
- [ ] 1.4 Create `requirements.txt` with production dependencies
- [ ] 1.5 Create `requirements-dev.txt` with development dependencies

## 2. Configuration Management
- [ ] 2.1 Implement `src/mcp_aixbt/config.py` with Pydantic Settings class
- [ ] 2.2 Add environment variable validation with field validators
- [ ] 2.3 Create `.env.example` template file
- [ ] 2.4 Add `get_settings()` dependency function with caching

## 3. Base Models
- [ ] 3.1 Create `src/mcp_aixbt/models/__init__.py`
- [ ] 3.2 Create `src/mcp_aixbt/models/responses.py` with base response models
- [ ] 3.3 Add `APIResponse`, `Pagination`, `ErrorResponse`, `HealthStatus` models

## 4. Application Entry Point
- [ ] 4.1 Create `src/mcp_aixbt/main.py` with FastAPI app initialization
- [ ] 4.2 Add lifespan context manager for startup/shutdown events
- [ ] 4.3 Configure CORS middleware (if needed for local development)
- [ ] 4.4 Add basic exception handlers

## 5. Validation
- [ ] 5.1 Verify project structure matches specification
- [ ] 5.2 Run `python -c "from mcp_aixbt.config import Settings"` to test imports
- [ ] 5.3 Start server with `uvicorn mcp_aixbt.main:app` and verify startup
- [ ] 5.4 Confirm `.env.example` documents all required variables
