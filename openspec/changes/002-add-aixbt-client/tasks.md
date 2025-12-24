# Tasks: Add AIXBT REST API Client

## 1. Domain Models
- [x] 1.1 Create `src/mcp_aixbt/models/projects.py` with `SignalCategory` enum
- [x] 1.2 Add `Cluster`, `CoingeckoData`, `Signal`, `Project` models
- [x] 1.3 Add `MomentumDataPoint`, `ProjectMomentum` models
- [x] 1.4 Create `src/mcp_aixbt/models/requests.py` with filter models
- [x] 1.5 Add `ProjectFilters`, `SignalFilters`, `MomentumFilters` models

## 2. Caching Utility
- [x] 2.1 Create `src/mcp_aixbt/utils/cache.py`
- [x] 2.2 Implement `TTLCache` class with configurable TTL
- [x] 2.3 Add `get_cached()` and `set_cache()` functions
- [x] 2.4 Support cache key generation from request parameters

## 3. HTTP Client
- [x] 3.1 Create `src/mcp_aixbt/clients/aixbt.py`
- [x] 3.2 Implement `AIXBTClient` class with httpx AsyncClient
- [x] 3.3 Add `x-api-key` header injection
- [x] 3.4 Implement rate limit detection from response headers
- [x] 3.5 Add retry logic for 429 responses with exponential backoff

## 4. API Methods
- [x] 4.1 Implement `list_projects()` method with filtering
- [x] 4.2 Implement `get_project(id)` method
- [x] 4.3 Implement `list_signals()` method with filtering
- [x] 4.4 Implement `get_momentum(project_id)` method
- [x] 4.5 Implement `list_clusters()` method
- [x] 4.6 Implement `list_chains()` method

## 5. Error Handling
- [x] 5.1 Create `src/mcp_aixbt/utils/errors.py`
- [x] 5.2 Define custom exceptions: `AIXBTError`, `RateLimitError`, `AuthenticationError`
- [x] 5.3 Add response status code handling in client

## 6. Validation
- [x] 6.1 Write unit tests for domain models with sample data
- [x] 6.2 Write unit tests for cache TTL behavior
- [x] 6.3 Write integration tests with mocked AIXBT responses (using respx)
- [x] 6.4 Verify rate limit header parsing
