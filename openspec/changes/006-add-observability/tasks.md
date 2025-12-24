# Tasks: Add Observability (Health Checks, Logging, Metrics)

## 1. Logging Configuration
- [x] 1.1 Add `LOG_LEVEL` setting (default: INFO)
- [x] 1.2 Add `LOG_FORMAT` setting (json or text, default: json)
- [x] 1.3 Create `src/mcp_aixbt/middleware/logging.py`
- [x] 1.4 Implement `configure_logging()` function with structlog
- [x] 1.5 Add `get_logger()` helper function

## 2. Request Logging Middleware
- [x] 2.1 Implement `RequestLoggingMiddleware` class
- [x] 2.2 Generate unique request IDs (UUID)
- [x] 2.3 Log request start (method, path, client IP)
- [x] 2.4 Log request completion (status code, duration)
- [x] 2.5 Add request ID to response headers (`X-Request-ID`)
- [x] 2.6 Bind request context using structlog contextvars

## 3. Health Check Endpoints
- [x] 3.1 Create `src/mcp_aixbt/routers/health.py`
- [x] 3.2 Implement `GET /health` basic check
- [x] 3.3 Implement `GET /health/ready` readiness check with:
  - Configuration validation
  - AIXBT API connectivity test
- [x] 3.4 Implement `GET /health/live` minimal liveness check
- [x] 3.5 Add `HealthStatus` response model

## 4. Router Registration
- [x] 4.1 Update `main.py` to include health router
- [x] 4.2 Register logging middleware
- [x] 4.3 Call `configure_logging()` on startup

## 5. Error Logging
- [x] 5.1 Add exception logging in middleware
- [x] 5.2 Log error details without sensitive information
- [x] 5.3 Include error type and duration in failed request logs

## 6. Validation
- [x] 6.1 Test health endpoints return correct structure
- [x] 6.2 Test readiness check fails when AIXBT unreachable
- [x] 6.3 Verify JSON log format in production mode
- [x] 6.4 Verify text log format in development mode
- [x] 6.5 Test request ID propagation in headers
- [x] 6.6 Verify sensitive data (API keys) not logged
