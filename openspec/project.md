# Project Context

## Purpose
Build a Python-based MCP (Model Context Protocol) server that bridges AI assistants (like Claude) with the AIXBT market intelligence platform. The server exposes AIXBT's crypto market analysis capabilities—including narrative detection, whale tracking, sentiment analysis, and project signals—through standardized MCP Resources, Tools, and Prompts.

**Key Goals:**
- Provide seamless access to AIXBT's REST API (with API key auth) and x402 pay-per-request endpoints
- Handle x402 payment protocol negotiations transparently using EVM wallet signatures
- Implement caching, rate limiting, and budget controls to manage costs
- Enable local development with Docker containerization for future deployment

## Tech Stack
- **Language:** Python 3.10+
- **Web Framework:** FastAPI (with Uvicorn ASGI server)
- **HTTP Client:** httpx (async)
- **Blockchain/Crypto:** web3.py, eth-account (for EIP-712 signing)
- **Data Validation:** Pydantic
- **Configuration:** python-dotenv
- **Future:** Docker for containerization

## Project Conventions

### Code Style
- Follow PEP 8 for Python code style
- Use type hints throughout
- Pydantic models for request/response schemas
- Async/await for all HTTP operations
- Environment variables for all secrets (never hardcode)
- Clear docstrings for public functions and classes

### Architecture Patterns
- **Layered Architecture:**
  - Routes (FastAPI endpoints) → Services (business logic) → Clients (external API calls)
- **Dependency Injection:** Use FastAPI's `Depends()` for config, clients, and services
- **x402 Handler:** Centralized payment negotiation helper that wraps external calls
- **Caching Layer:** In-memory TTL cache for frequently accessed resources (5-minute default)
- **MCP Interface Types:**
  - **Resources** (GET): Read-only data endpoints (signals, sentiment, logs)
  - **Tools** (POST): Action endpoints with parameters (query_agent, whale_alerts)
  - **Prompts**: Reusable query templates (market_briefing, token_deep_dive)

### Testing Strategy
- Unit tests for payment signing logic and caching
- Integration tests against AIXBT API (with mocked responses for CI)
- Manual endpoint testing with curl/Postman
- Verify x402 handshake flow with test wallet on Base testnet

### Git Workflow
- **Main branch:** `main` - stable, production-ready code
- **Feature branches:** `feature/<name>` or `<username>/<feature>`
- **Commits:** Conventional commits preferred (feat:, fix:, docs:, refactor:)
- **PRs:** Required for merging to main

## Domain Context

### AIXBT API Structure
AIXBT provides two access methods:

1. **REST API (API Key Auth)** - Base URL: `https://api.aixbt.tech/v2`
   - `GET /v2/projects` - List projects with momentum scores and signals
   - `GET /v2/projects/{id}` - Get single project details
   - `GET /v2/signals` - List market signals with filtering
   - `GET /v2/projects/{id}/momentum` - Hourly momentum history
   - `GET /v2/clusters` - List tracked communities/sources
   - `GET /v2/projects/chains` - List supported blockchains
   - `POST /v2/agents/indigo` - Chat with Indigo AI agent
   - **Auth:** `x-api-key` header
   - **Key Types:** Demo (Bitcoin only), Full-Access (subscription required)

2. **x402 Pay-Per-Request** - Base URL: `https://api.aixbt.tech/x402/v1`
   - `POST /x402/v1/agents/indigo` - Chat with Indigo (paid)
   - `GET /x402/v1/projects` - Surging projects (paid)
   - **Auth:** HTTP 402 challenge → EIP-712 signature → X-Payment header
   - **Payment:** USDC on Base chain (chain_id: 8453)

### Signal Categories
`FINANCIAL_EVENT`, `TOKEN_ECONOMICS`, `TECH_EVENT`, `MARKET_ACTIVITY`, `ONCHAIN_METRICS`, `PARTNERSHIP`, `TEAM_UPDATE`, `REGULATORY`, `WHALE_ACTIVITY`, `RISK_ALERT`, `VISIBILITY_EVENT`, `OPINION_SPECULATION`

### x402 Payment Flow
1. Request protected endpoint → Receive 402 with payment challenge
2. Parse challenge (amount, recipient, token_address, chain_id)
3. Sign EIP-712 typed data with wallet private key
4. Retry request with `X-Payment: type=exact; signature=0x...` header
5. Receive data (automatic refund on 404/500 errors)

## Important Constraints

### Security
- Private key (`EVM_PRIVATE_KEY`) must never be logged or exposed
- API keys stored only in environment variables
- Server should run locally or behind firewall (hot wallet risk)
- Validate payment challenge amounts before signing

### Budget Controls
- `MAX_PRICE_PER_CALL`: Reject payments exceeding threshold
- `MAX_SPEND_PER_DAY`: Daily spending cap with tracking
- Rate limiting: Prevent runaway costs from loops

### API Limits
- REST API: 100 requests/minute, 100,000 requests/day
- Pagination: max 50 results per page

## External Dependencies

### AIXBT API
- **REST API:** `https://api.aixbt.tech` (v2 endpoints)
- **x402 API:** `https://api.aixbt.tech/x402/v1`
- **Docs:** `https://docs.aixbt.tech`

### Blockchain
- **Network:** Base Mainnet (chain_id: 8453)
- **RPC:** Requires Base RPC endpoint (e.g., QuickNode, Alchemy, ThirdWeb)
- **Payment Token:** USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)

### x402 Protocol
- **Spec:** https://x402.org
- **Libraries:** `x402-fetch`, `x402-axios` (JS), custom implementation for Python
- **Developer:** Coinbase

### Optional: Virtuals Protocol Terminal
- **Logs API:** `https://api-terminal.virtuals.io` (for agent internal state)
- **Auth:** Bearer token from Virtuals Platform API key exchange
