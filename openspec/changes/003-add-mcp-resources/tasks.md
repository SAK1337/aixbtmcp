# Tasks: Add MCP Resource Endpoints

## 1. Service Layer
- [ ] 1.1 Create `src/mcp_aixbt/services/__init__.py`
- [ ] 1.2 Create `src/mcp_aixbt/services/projects.py` with `ProjectService` class
- [ ] 1.3 Implement `list_projects()`, `get_project()`, `get_momentum()` methods
- [ ] 1.4 Create `src/mcp_aixbt/services/signals.py` with `SignalService` class
- [ ] 1.5 Implement `list_signals()` method with filtering

## 2. Resource Router
- [ ] 2.1 Create `src/mcp_aixbt/routers/__init__.py`
- [ ] 2.2 Create `src/mcp_aixbt/routers/resources.py`
- [ ] 2.3 Implement `GET /resources/projects` endpoint
- [ ] 2.4 Implement `GET /resources/projects/{id}` endpoint
- [ ] 2.5 Implement `GET /resources/projects/{id}/momentum` endpoint
- [ ] 2.6 Implement `GET /resources/signals` endpoint
- [ ] 2.7 Implement `GET /resources/clusters` endpoint
- [ ] 2.8 Implement `GET /resources/chains` endpoint

## 3. Router Registration
- [ ] 3.1 Update `main.py` to include resources router
- [ ] 3.2 Add router prefix `/resources`
- [ ] 3.3 Configure OpenAPI tags for documentation

## 4. Dependency Injection
- [ ] 4.1 Create service factory functions using `Depends()`
- [ ] 4.2 Inject AIXBT client into services
- [ ] 4.3 Inject settings for cache configuration

## 5. Validation
- [ ] 5.1 Write integration tests for each resource endpoint
- [ ] 5.2 Test pagination parameters (page, limit)
- [ ] 5.3 Test filter parameter validation
- [ ] 5.4 Verify response schemas match specification
- [ ] 5.5 Test with FastAPI TestClient
