# Capability: AIXBT REST API Client

## ADDED Requirements

### Requirement: HTTP Client with API Key Authentication
The system SHALL provide an async HTTP client that authenticates with the AIXBT API using the `x-api-key` header.

#### Scenario: Successful authenticated request
- **WHEN** a request is made to `https://api.aixbt.tech/v2/projects`
- **THEN** the `x-api-key` header is included with the configured API key
- **AND** the response is parsed into domain models

#### Scenario: Invalid API key
- **WHEN** a request is made with an invalid API key
- **THEN** an `AuthenticationError` is raised with the 401 status details

### Requirement: Rate Limit Handling
The system SHALL detect rate limit responses and implement retry logic with exponential backoff.

#### Scenario: Rate limit exceeded
- **WHEN** the API returns HTTP 429 Too Many Requests
- **THEN** the client waits for the duration specified in `Retry-After` header
- **AND** retries the request automatically (up to 3 attempts)

#### Scenario: Rate limit headers tracked
- **WHEN** a successful response is received
- **THEN** the client parses `X-RateLimit-Remaining-Minute` and `X-RateLimit-Remaining-Day` headers
- **AND** makes this information available for monitoring

### Requirement: Domain Model Mapping
The system SHALL map AIXBT API responses to strongly-typed Pydantic models.

#### Scenario: Project response parsing
- **WHEN** a project list response is received
- **THEN** each item is parsed into a `Project` model with nested `Signal` and `CoingeckoData` objects

#### Scenario: Signal category validation
- **WHEN** a signal is parsed
- **THEN** the `category` field is validated against the `SignalCategory` enum
- **AND** invalid categories raise a validation error

### Requirement: Request Caching
The system SHALL cache GET request responses with a configurable TTL to reduce API calls.

#### Scenario: Cache hit
- **WHEN** the same request is made within the TTL period
- **THEN** the cached response is returned without making an API call

#### Scenario: Cache miss after TTL
- **WHEN** a request is made after the TTL has expired
- **THEN** a new API call is made and the cache is updated

#### Scenario: Cache disabled
- **WHEN** `CACHE_TTL_SECONDS` is set to 0
- **THEN** no caching occurs and every request hits the API

### Requirement: Project Listing
The system SHALL support listing projects with filtering by name, ticker, chain, and momentum score.

#### Scenario: List all projects
- **WHEN** `list_projects()` is called without filters
- **THEN** the first page of projects sorted by momentum score is returned

#### Scenario: Filter by chain
- **WHEN** `list_projects(chain="base")` is called
- **THEN** only projects on the Base chain are returned

#### Scenario: Filter by minimum momentum
- **WHEN** `list_projects(min_momentum_score=0.5)` is called
- **THEN** only projects with momentum >= 0.5 are returned

### Requirement: Signal Listing
The system SHALL support listing signals with filtering by category, project, and date range.

#### Scenario: Filter by category
- **WHEN** `list_signals(categories="WHALE_ACTIVITY,TECH_EVENT")` is called
- **THEN** only signals matching those categories are returned

#### Scenario: Filter by date range
- **WHEN** `list_signals(detected_after="2025-12-01T00:00:00Z")` is called
- **THEN** only signals detected after that timestamp are returned

### Requirement: Momentum History
The system SHALL support fetching hourly momentum history for a specific project.

#### Scenario: Get momentum history
- **WHEN** `get_momentum(project_id, start, end)` is called
- **THEN** hourly momentum data points with cluster breakdown are returned

### Requirement: Reference Data
The system SHALL support fetching clusters and chains reference data.

#### Scenario: List clusters
- **WHEN** `list_clusters()` is called
- **THEN** all tracked communities and information sources are returned

#### Scenario: List chains
- **WHEN** `list_chains()` is called
- **THEN** all supported blockchain platforms are returned
