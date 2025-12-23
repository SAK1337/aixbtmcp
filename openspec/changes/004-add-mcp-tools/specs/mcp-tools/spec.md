# Capability: MCP Tool Endpoints

## ADDED Requirements

### Requirement: Query Indigo Tool
The system SHALL expose a `/tools/query-indigo` POST endpoint that enables chat interaction with the AIXBT Indigo AI agent.

#### Scenario: Simple query
- **WHEN** `POST /tools/query-indigo` with `{"message": "What narratives are gaining traction?"}` is sent
- **THEN** a response with `{"text": "..."}` containing Indigo's analysis is returned

#### Scenario: Query with conversation history
- **WHEN** `POST /tools/query-indigo` includes `conversation_history` array
- **THEN** the conversation context is preserved and Indigo provides a contextual response

#### Scenario: No information found
- **WHEN** Indigo cannot find relevant information for the query
- **THEN** a friendly message like "No relevant information found for your query" is returned
- **AND** the response status is 200 (not an error)

#### Scenario: Message validation
- **WHEN** a message exceeding 10000 characters is submitted
- **THEN** a 422 validation error is returned

### Requirement: List Projects Tool
The system SHALL expose a `/tools/list-projects` POST endpoint that allows dynamic project searching.

#### Scenario: Search by name
- **WHEN** `POST /tools/list-projects` with `{"names": "ethereum,bitcoin"}` is sent
- **THEN** projects matching those names are returned

#### Scenario: Search by ticker
- **WHEN** `POST /tools/list-projects` with `{"tickers": "ETH,BTC"}` is sent
- **THEN** projects with matching ticker symbols are returned

#### Scenario: Filter by chain
- **WHEN** `POST /tools/list-projects` with `{"chain": "base"}` is sent
- **THEN** only projects on the Base chain are returned

#### Scenario: Filter by momentum
- **WHEN** `POST /tools/list-projects` with `{"minMomentumScore": 0.7}` is sent
- **THEN** only high-momentum projects are returned

### Requirement: Get Signals Tool
The system SHALL expose a `/tools/get-signals` POST endpoint for retrieving market signals with filters.

#### Scenario: Filter by category
- **WHEN** `POST /tools/get-signals` with `{"categories": "WHALE_ACTIVITY"}` is sent
- **THEN** only whale activity signals are returned

#### Scenario: Filter by date
- **WHEN** `POST /tools/get-signals` with `{"detectedAfter": "2025-12-01T00:00:00Z"}` is sent
- **THEN** only signals detected after that date are returned

#### Scenario: Filter by ticker
- **WHEN** `POST /tools/get-signals` with `{"tickers": "ETH"}` is sent
- **THEN** only Ethereum-related signals are returned

#### Scenario: Limit results
- **WHEN** `POST /tools/get-signals` with `{"limit": 5}` is sent
- **THEN** at most 5 signals are returned

### Requirement: Tool Request Validation
The system SHALL validate all tool request bodies using Pydantic models.

#### Scenario: Valid request
- **WHEN** a well-formed request body is submitted
- **THEN** the request is processed and a response is returned

#### Scenario: Invalid request body
- **WHEN** an invalid JSON or missing required fields are submitted
- **THEN** a 422 Unprocessable Entity response with validation details is returned

#### Scenario: Invalid enum value
- **WHEN** an invalid category like "INVALID_CATEGORY" is submitted
- **THEN** a 422 response indicating the valid options is returned

### Requirement: Tool Response Format
The system SHALL return tool responses in a consistent format suitable for LLM consumption.

#### Scenario: Indigo response format
- **WHEN** query-indigo succeeds
- **THEN** the response contains `{"text": "<response>"}` for easy LLM parsing

#### Scenario: List response format
- **WHEN** list-projects or get-signals succeeds
- **THEN** the response contains `{"status": 200, "data": [...], "pagination": {...}}`
