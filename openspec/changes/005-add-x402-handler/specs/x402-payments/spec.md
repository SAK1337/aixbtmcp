# Capability: x402 Payment Protocol Handler

## ADDED Requirements

### Requirement: Payment Challenge Parsing
The system SHALL parse HTTP 402 responses to extract payment challenge details.

#### Scenario: Parse payment challenge
- **WHEN** an x402 endpoint returns HTTP 402 with payment JSON
- **THEN** the system extracts amount, recipient, token_address, and chain_id
- **AND** validates the chain_id is 8453 (Base mainnet)

#### Scenario: Invalid challenge format
- **WHEN** a 402 response lacks required payment fields
- **THEN** an error is raised indicating the malformed challenge

### Requirement: EIP-712 Signature Generation
The system SHALL sign payment authorizations using EIP-712 typed data.

#### Scenario: Sign payment authorization
- **WHEN** a valid payment challenge is received
- **THEN** an EIP-712 typed message is constructed and signed with the configured private key
- **AND** the signature is formatted as hex string for the X-Payment header

#### Scenario: No private key configured
- **WHEN** x402 payment is required but EVM_PRIVATE_KEY is not set
- **THEN** an error indicating x402 is not configured is raised

### Requirement: Budget Controls
The system SHALL enforce spending limits to prevent wallet draining.

#### Scenario: Per-request limit exceeded
- **WHEN** a payment challenge amount exceeds MAX_PRICE_PER_CALL_USDC
- **THEN** the payment is rejected with a `BudgetExceededError`
- **AND** no signature is generated

#### Scenario: Daily limit exceeded
- **WHEN** the cumulative daily spend plus the new payment would exceed MAX_SPEND_PER_DAY_USDC
- **THEN** the payment is rejected with a `BudgetExceededError`

#### Scenario: Daily limit reset
- **WHEN** a new UTC day begins
- **THEN** the daily spend counter is reset to zero

#### Scenario: Budget warning
- **WHEN** daily spend exceeds 80% of MAX_SPEND_PER_DAY_USDC
- **THEN** a warning is logged indicating approaching limit

### Requirement: Automatic Payment Flow
The system SHALL automatically handle the x402 handshake flow.

#### Scenario: Successful payment flow
- **WHEN** `fetch_with_x402()` is called for an x402 endpoint
- **THEN** the initial request is made
- **AND** if 402 is received, the payment is signed and request retried with X-Payment header
- **AND** the final response data is returned

#### Scenario: Payment already sufficient
- **WHEN** the x402 endpoint returns 200 directly
- **THEN** no payment flow is triggered and data is returned immediately

### Requirement: Refund Handling
The system SHALL recognize and track automatic refunds for failed requests.

#### Scenario: Refund on 404
- **WHEN** an x402 request returns 404 with refund information
- **THEN** the refund transaction hash is logged
- **AND** a friendly "no information found" message is returned

#### Scenario: Refund on 500
- **WHEN** an x402 request returns 500 with refund information
- **THEN** the refund is tracked and the error is surfaced appropriately

### Requirement: Surging Projects Tool
The system SHALL expose a `/tools/get-surging-projects` endpoint using x402 payment.

#### Scenario: Get surging projects
- **WHEN** `POST /tools/get-surging-projects` is called with valid x402 configuration
- **THEN** real-time surging project data from `/x402/v1/projects` is returned

#### Scenario: x402 not configured
- **WHEN** `POST /tools/get-surging-projects` is called without EVM_PRIVATE_KEY
- **THEN** a 503 Service Unavailable response indicates x402 is not configured

### Requirement: Security Constraints
The system SHALL protect sensitive payment credentials.

#### Scenario: Private key protection
- **WHEN** the private key is accessed
- **THEN** it is retrieved via SecretStr.get_secret_value() only when needed for signing
- **AND** it is never logged or included in error messages

#### Scenario: Chain ID validation
- **WHEN** a payment challenge specifies an unexpected chain_id
- **THEN** the payment is rejected to prevent signing for wrong networks
