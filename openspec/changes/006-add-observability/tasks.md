# Tasks: Add Observability (Health Checks, Logging, Metrics)

## 1. Logging Configuration
- [ ] 1.1 Add `LOG_LEVEL` setting (default: INFO)
- [ ] 1.2 Add `LOG_FORMAT` setting (json or text, default: json)
- [ ] 1.3 Create `src/mcp_aixbt/middleware/logging.py`
- [ ] 1.4 Implement `configure_logging()` function with structlog
- [ ] 1.5 Add `get_logger()` helper function

## 2. Request Logging Middleware
- [ ] 2.1 Implement `RequestLoggingMiddleware` class
- [ ] 2.2 Generate unique request IDs (UUID)
- [ ] 2.3 Log request start (method, path, client IP)
- [ ] 2.4 Log request completion (status code, duration)
- [ ] 2.5 Add request ID to response headers (`X-Request-ID`)
- [ ] 2.6 Bind request context using structlog contextvars

## 3. Health Check Endpoints
- [ ] 3.1 Create `src/mcp_aixbt/routers/health.py`
- [ ] 3.2 Implement `GET /health` basic check
- [ ] 3.3 Implement `GET /health/ready` readiness check with:
  - Configuration validation
  - AIXBT API connectivity test
- [ ] 3.4 Implement `GET /health/live` minimal liveness check
- [ ] 3.5 Add `HealthStatus` response model

## 4. Router Registration
- [ ] 4.1 Update `main.py` to include health router
- [ ] 4.2 Register logging middleware
- [ ] 4.3 Call `configure_logging()` on startup

## 5. Error Logging
- [ ] 5.1 Add exception logging in middleware
- [ ] 5.2 Log error details without sensitive information
- [ ] 5.3 Include error type and duration in failed request logs

## 6. Validation
- [ ] 6.1 Test health endpoints return correct structure
- [ ] 6.2 Test readiness check fails when AIXBT unreachable
- [ ] 6.3 Verify JSON log format in production mode
- [ ] 6.4 Verify text log format in development mode
- [ ] 6.5 Test request ID propagation in headers
- [ ] 6.6 Verify sensitive data (API keys) not logged
