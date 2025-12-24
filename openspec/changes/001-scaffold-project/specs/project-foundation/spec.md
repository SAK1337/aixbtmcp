# Capability: Project Foundation

## ADDED Requirements

### Requirement: Project Directory Structure
The system SHALL organize code into a layered `src/mcp_aixbt/` package structure with separate modules for configuration, models, clients, services, routers, middleware, and utilities.

#### Scenario: Standard module layout
- **WHEN** the project is initialized
- **THEN** the following directories exist under `src/mcp_aixbt/`:
  - `models/` for Pydantic data models
  - `clients/` for external API clients
  - `services/` for business logic
  - `routers/` for FastAPI route definitions
  - `middleware/` for request/response processing
  - `utils/` for shared utilities

### Requirement: Configuration Management
The system SHALL load configuration from environment variables using Pydantic Settings with validation and type coercion.

#### Scenario: Required configuration present
- **WHEN** the application starts with `AIXBT_API_KEY` set
- **THEN** the Settings object is created successfully with validated values

#### Scenario: Required configuration missing
- **WHEN** the application starts without `AIXBT_API_KEY`
- **THEN** a ValidationError is raised with a clear error message

#### Scenario: Invalid configuration value
- **WHEN** `PORT` is set to an invalid value (e.g., "invalid" or "70000")
- **THEN** a ValidationError is raised indicating the constraint violation

### Requirement: Dependency Management
The system SHALL declare all dependencies in `pyproject.toml` and `requirements.txt` with pinned versions for reproducibility.

#### Scenario: Install production dependencies
- **WHEN** `pip install -r requirements.txt` is executed
- **THEN** all required packages (fastapi, uvicorn, pydantic, httpx, etc.) are installed

#### Scenario: Install development dependencies
- **WHEN** `pip install -r requirements-dev.txt` is executed
- **THEN** testing and development packages (pytest, ruff, mypy, etc.) are installed

### Requirement: FastAPI Application Entry Point
The system SHALL provide a FastAPI application instance in `main.py` that can be started with Uvicorn.

#### Scenario: Application startup
- **WHEN** `uvicorn mcp_aixbt.main:app --host 127.0.0.1 --port 8000` is executed
- **THEN** the server starts and is accessible at `http://127.0.0.1:8000`

#### Scenario: Configuration injection
- **WHEN** the application starts
- **THEN** the Settings dependency is available for injection into route handlers

### Requirement: Base Response Models
The system SHALL provide Pydantic models for standardized API responses including success, error, and pagination structures.

#### Scenario: Success response structure
- **WHEN** an endpoint returns data successfully
- **THEN** the response includes `status`, `data`, and optional `pagination` fields

#### Scenario: Error response structure
- **WHEN** an endpoint encounters an error
- **THEN** the response includes `status`, `error`, and optional `code` and `details` fields
