# Capability: Observability (Health Checks, Logging, Request Tracking)

## ADDED Requirements

### Requirement: Structured Logging Configuration
The system SHALL provide configurable structured logging using structlog.

#### Scenario: Configure JSON logging for production
- **GIVEN** LOG_FORMAT is set to "json"
- **WHEN** the application starts
- **THEN** all log output is formatted as JSON with consistent field names
- **AND** timestamps are in ISO 8601 format

#### Scenario: Configure text logging for development
- **GIVEN** LOG_FORMAT is set to "text"
- **WHEN** the application starts
- **THEN** log output is human-readable with colors enabled
- **AND** timestamps are in local timezone

#### Scenario: Configure log level
- **GIVEN** LOG_LEVEL is set to a valid level (DEBUG, INFO, WARNING, ERROR)
- **WHEN** the application starts
- **THEN** only messages at or above that level are emitted

### Requirement: Request Logging Middleware
The system SHALL log all HTTP requests with timing and context information.

#### Scenario: Log request start
- **WHEN** an HTTP request is received
- **THEN** a log entry is created with method, path, and client IP
- **AND** a unique request ID (UUID) is generated

#### Scenario: Log request completion
- **WHEN** an HTTP request completes successfully
- **THEN** a log entry is created with status code and duration in milliseconds
- **AND** the request ID is included for correlation

#### Scenario: Request ID in response headers
- **WHEN** an HTTP response is sent
- **THEN** the `X-Request-ID` header contains the generated request ID

#### Scenario: Request context binding
- **WHEN** a request is being processed
- **THEN** the request ID is bound to structlog context
- **AND** all log entries within the request include the request ID

### Requirement: Exception Logging
The system SHALL log exceptions without exposing sensitive information.

#### Scenario: Log exception details
- **WHEN** an unhandled exception occurs during request processing
- **THEN** the exception type and message are logged at ERROR level
- **AND** the request duration and status code are included

#### Scenario: Sensitive data protection
- **WHEN** logging request or error information
- **THEN** API keys, private keys, and credentials are never included
- **AND** request bodies containing sensitive fields are redacted

### Requirement: Health Check Endpoints
The system SHALL provide health check endpoints for container orchestration.

#### Scenario: Basic health check
- **WHEN** `GET /health` is called
- **THEN** a 200 response with status "healthy" is returned
- **AND** the response includes the application version

#### Scenario: Liveness probe
- **WHEN** `GET /health/live` is called
- **THEN** a 200 response is returned if the process is running
- **AND** this check has minimal overhead (no external calls)

#### Scenario: Readiness probe - healthy
- **WHEN** `GET /health/ready` is called
- **AND** configuration is valid
- **AND** AIXBT API is reachable
- **THEN** a 200 response with status "ready" is returned

#### Scenario: Readiness probe - unhealthy
- **WHEN** `GET /health/ready` is called
- **AND** AIXBT API is unreachable
- **THEN** a 503 response with status "not_ready" is returned
- **AND** the failing check is identified in the response

### Requirement: Health Response Model
The system SHALL return consistent health check response structures.

#### Scenario: Health response structure
- **WHEN** any health endpoint is called
- **THEN** the response includes:
  - `status`: string ("healthy", "unhealthy", "ready", "not_ready")
  - `timestamp`: ISO 8601 datetime
  - `version`: application version string
  - `checks`: optional dict of individual check results
