# Tasks: Add MCP Resource Endpoints

## 1. Service Layer
- [x] 1.1 Create `src/mcp_aixbt/services/__init__.py`
- [x] 1.2 Create `src/mcp_aixbt/services/projects.py` with `ProjectService` class
- [x] 1.3 Implement `list_projects()`, `get_project()`, `get_momentum()` methods
- [x] 1.4 Create `src/mcp_aixbt/services/signals.py` with `SignalService` class
- [x] 1.5 Implement `list_signals()` method with filtering

## 2. Resource Router
- [x] 2.1 Create `src/mcp_aixbt/routers/__init__.py`
- [x] 2.2 Create `src/mcp_aixbt/routers/resources.py`
- [x] 2.3 Implement `GET /resources/projects` endpoint
- [x] 2.4 Implement `GET /resources/projects/{id}` endpoint
- [x] 2.5 Implement `GET /resources/projects/{id}/momentum` endpoint
- [x] 2.6 Implement `GET /resources/signals` endpoint
- [x] 2.7 Implement `GET /resources/clusters` endpoint
- [x] 2.8 Implement `GET /resources/chains` endpoint

## 3. Router Registration
- [x] 3.1 Update `main.py` to include resources router
- [x] 3.2 Add router prefix `/resources`
- [x] 3.3 Configure OpenAPI tags for documentation

## 4. Dependency Injection
- [x] 4.1 Create service factory functions using `Depends()`
- [x] 4.2 Inject AIXBT client into services
- [x] 4.3 Inject settings for cache configuration

## 5. Validation
- [x] 5.1 Write integration tests for each resource endpoint
- [x] 5.2 Test pagination parameters (page, limit)
- [x] 5.3 Test filter parameter validation
- [x] 5.4 Verify response schemas match specification
- [x] 5.5 Test with FastAPI TestClient
