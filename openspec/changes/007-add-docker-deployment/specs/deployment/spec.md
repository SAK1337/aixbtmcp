# Capability: Docker Deployment Configuration

## ADDED Requirements

### Requirement: Multi-Stage Docker Build
The system SHALL use multi-stage Docker builds for optimized image size.

#### Scenario: Builder stage
- **WHEN** the Docker image is built
- **THEN** dependencies are installed in a builder stage
- **AND** only runtime artifacts are copied to the final image

#### Scenario: Runtime stage
- **WHEN** the final image is created
- **THEN** it uses python:3.11-slim as the base
- **AND** the image size is under 200MB
- **AND** only production dependencies are included

### Requirement: Container Security
The system SHALL follow container security best practices.

#### Scenario: Non-root execution
- **WHEN** the container runs
- **THEN** the application runs as a non-root user
- **AND** the user has minimal filesystem permissions

#### Scenario: Secret handling
- **WHEN** secrets are provided to the container
- **THEN** they are passed via environment variables
- **AND** they are never baked into the image

#### Scenario: Read-only filesystem
- **WHEN** the container runs in production
- **THEN** the root filesystem can be mounted read-only
- **AND** only designated directories are writable

### Requirement: Health Check Integration
The container SHALL expose health checks for orchestration.

#### Scenario: Docker health check
- **WHEN** the container is running
- **THEN** Docker health check uses the `/health/live` endpoint
- **AND** the container is marked unhealthy if the check fails

#### Scenario: Startup probe
- **WHEN** the container starts
- **THEN** the `/health/ready` endpoint indicates when the service is ready
- **AND** orchestrators wait for readiness before routing traffic

### Requirement: Environment Configuration
The system SHALL support configuration via environment variables.

#### Scenario: Required variables
- **WHEN** the container starts without AIXBT_API_KEY
- **THEN** the application fails fast with a clear error message

#### Scenario: Optional variables
- **WHEN** optional variables (EVM_PRIVATE_KEY, LOG_LEVEL) are not set
- **THEN** sensible defaults are used
- **AND** the application starts successfully

#### Scenario: Environment template
- **WHEN** developers clone the repository
- **THEN** `.env.example` documents all configuration options
- **AND** each variable includes a description and default value

### Requirement: Development Workflow
The system SHALL support local development with Docker Compose.

#### Scenario: Development mode
- **WHEN** `docker-compose up` is run
- **THEN** the application starts with hot-reload enabled
- **AND** local source code is mounted as a volume

#### Scenario: Port mapping
- **WHEN** the container runs via docker-compose
- **THEN** port 8000 is mapped to the host
- **AND** the API is accessible at http://localhost:8000

#### Scenario: Environment file
- **WHEN** docker-compose runs
- **THEN** it loads variables from `.env` file
- **AND** environment variables override file values

### Requirement: Build Optimization
The system SHALL optimize Docker build context and caching.

#### Scenario: Dockerignore
- **WHEN** the Docker build runs
- **THEN** .dockerignore excludes tests, docs, .git, and cache files
- **AND** build context is minimal for fast builds

#### Scenario: Layer caching
- **WHEN** only source code changes
- **THEN** dependency installation layers are cached
- **AND** rebuilds complete quickly
