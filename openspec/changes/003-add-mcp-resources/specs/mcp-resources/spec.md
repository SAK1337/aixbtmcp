# Capability: MCP Resource Endpoints

## ADDED Requirements

### Requirement: Projects Resource
The system SHALL expose a `/resources/projects` endpoint that returns paginated project data with filtering support.

#### Scenario: List projects with pagination
- **WHEN** `GET /resources/projects?page=1&limit=10` is requested
- **THEN** the response contains up to 10 projects with pagination metadata

#### Scenario: Filter projects by chain
- **WHEN** `GET /resources/projects?chain=base` is requested
- **THEN** only projects on the Base blockchain are returned

#### Scenario: Filter by momentum threshold
- **WHEN** `GET /resources/projects?minMomentumScore=0.5` is requested
- **THEN** only projects with momentum score >= 0.5 are returned

### Requirement: Project Detail Resource
The system SHALL expose a `/resources/projects/{id}` endpoint that returns detailed information for a single project.

#### Scenario: Get project by ID
- **WHEN** `GET /resources/projects/507f1f77bcf86cd799439011` is requested
- **THEN** the response contains the project details with recent signals

#### Scenario: Project not found
- **WHEN** `GET /resources/projects/invalid_id` is requested
- **THEN** a 404 response with appropriate error message is returned

### Requirement: Project Momentum Resource
The system SHALL expose a `/resources/projects/{id}/momentum` endpoint that returns hourly momentum history.

#### Scenario: Get momentum history
- **WHEN** `GET /resources/projects/{id}/momentum?start=2025-12-01&end=2025-12-23` is requested
- **THEN** hourly momentum data points for the specified range are returned

#### Scenario: Default date range
- **WHEN** `GET /resources/projects/{id}/momentum` is requested without date parameters
- **THEN** the last 7 days of momentum data is returned

### Requirement: Signals Resource
The system SHALL expose a `/resources/signals` endpoint that returns paginated signal data with filtering support.

#### Scenario: List signals with category filter
- **WHEN** `GET /resources/signals?categories=WHALE_ACTIVITY,TECH_EVENT` is requested
- **THEN** only signals matching those categories are returned

#### Scenario: Filter by date range
- **WHEN** `GET /resources/signals?detectedAfter=2025-12-01T00:00:00Z` is requested
- **THEN** only signals detected after that timestamp are returned

#### Scenario: Filter by project
- **WHEN** `GET /resources/signals?tickers=ETH,BTC` is requested
- **THEN** only signals for Ethereum and Bitcoin projects are returned

### Requirement: Clusters Resource
The system SHALL expose a `/resources/clusters` endpoint that returns all tracked communities.

#### Scenario: List all clusters
- **WHEN** `GET /resources/clusters` is requested
- **THEN** all cluster objects with id, name, and description are returned

#### Scenario: Cached response
- **WHEN** `/resources/clusters` is requested multiple times within TTL
- **THEN** the cached response is returned without additional API calls

### Requirement: Chains Resource
The system SHALL expose a `/resources/chains` endpoint that returns supported blockchain platforms.

#### Scenario: List all chains
- **WHEN** `GET /resources/chains` is requested
- **THEN** an array of chain identifiers (e.g., ["arbitrum-one", "base", "ethereum", "solana"]) is returned

### Requirement: Consistent Response Format
The system SHALL return all resource responses in a consistent JSON structure with status, data, and optional pagination.

#### Scenario: Success response format
- **WHEN** any resource endpoint returns successfully
- **THEN** the response body matches `{"status": 200, "data": [...], "pagination": {...}}`

#### Scenario: Error response format
- **WHEN** any resource endpoint encounters an error
- **THEN** the response body matches `{"status": <code>, "error": "<message>", "code": "<error_code>"}`
