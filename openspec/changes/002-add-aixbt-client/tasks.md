# Tasks: Add AIXBT REST API Client

## 1. Domain Models
- [ ] 1.1 Create `src/mcp_aixbt/models/projects.py` with `SignalCategory` enum
- [ ] 1.2 Add `Cluster`, `CoingeckoData`, `Signal`, `Project` models
- [ ] 1.3 Add `MomentumDataPoint`, `ProjectMomentum` models
- [ ] 1.4 Create `src/mcp_aixbt/models/requests.py` with filter models
- [ ] 1.5 Add `ProjectFilters`, `SignalFilters`, `MomentumFilters` models

## 2. Caching Utility
- [ ] 2.1 Create `src/mcp_aixbt/utils/cache.py`
- [ ] 2.2 Implement `TTLCache` class with configurable TTL
- [ ] 2.3 Add `get_cached()` and `set_cache()` functions
- [ ] 2.4 Support cache key generation from request parameters

## 3. HTTP Client
- [ ] 3.1 Create `src/mcp_aixbt/clients/aixbt.py`
- [ ] 3.2 Implement `AIXBTClient` class with httpx AsyncClient
- [ ] 3.3 Add `x-api-key` header injection
- [ ] 3.4 Implement rate limit detection from response headers
- [ ] 3.5 Add retry logic for 429 responses with exponential backoff

## 4. API Methods
- [ ] 4.1 Implement `list_projects()` method with filtering
- [ ] 4.2 Implement `get_project(id)` method
- [ ] 4.3 Implement `list_signals()` method with filtering
- [ ] 4.4 Implement `get_momentum(project_id)` method
- [ ] 4.5 Implement `list_clusters()` method
- [ ] 4.6 Implement `list_chains()` method

## 5. Error Handling
- [ ] 5.1 Create `src/mcp_aixbt/utils/errors.py`
- [ ] 5.2 Define custom exceptions: `AIXBTError`, `RateLimitError`, `AuthenticationError`
- [ ] 5.3 Add response status code handling in client

## 6. Validation
- [ ] 6.1 Write unit tests for domain models with sample data
- [ ] 6.2 Write unit tests for cache TTL behavior
- [ ] 6.3 Write integration tests with mocked AIXBT responses (using respx)
- [ ] 6.4 Verify rate limit header parsing
