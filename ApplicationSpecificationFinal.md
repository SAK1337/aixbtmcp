# **AIXBT Model Context Protocol (MCP) Integration Specification: A Comprehensive Technical Analysis**

## **1\. Executive Summary**

The rapid convergence of decentralized finance (DeFi), artificial intelligence (AI), and autonomous agent protocols has necessitated the development of new interoperability standards that transcend traditional web service architectures. This report provides an exhaustive technical documentation and architectural specification for integrating AIXBT—an AI-driven market intelligence platform operating on the Base layer-2 blockchain—into a Model Context Protocol (MCP) application.

AIXBT operates not merely as a standalone data provider but as a sophisticated autonomous agent within the Virtuals Protocol ecosystem. Its architecture leverages the Generative Autonomous Multimodal Entities (G.A.M.E.) framework for cognition and decision-making, while its economic layer is governed by the x402 protocol, an open standard for internet-native payments. This unique stack presents specific challenges and opportunities for developers seeking to build MCP applications that consume AIXBT’s intelligence.

The primary objective of this document is to reverse-engineer and document the public-facing interfaces of the AIXBT ecosystem to facilitate the creation of an MCP server. This server will act as a bridge, allowing Large Language Models (LLMs) like Claude or GPT-4 to programmatically access AIXBT’s narrative detection, sentiment analysis, and on-chain whale tracking capabilities.

By synthesizing data from the Virtuals Protocol SDK, the x402 payment specifications, and AIXBT’s reported "Indigo" upgrade capabilities, this report constructs a functional API specification. It details the authentication mechanisms requiring EIP-712 signatures, the request/response schemas for agent interaction, and the precise definitions of MCP Tools and Resources required for seamless integration. The analysis extends to the theoretical implications of "agentic commerce," where software autonomously negotiates and pays for data, a paradigm centrally enabled by the AIXBT and x402 integration.

## **2\. Architectural Landscape and Protocol Stack**

To accurately document the API surface for AIXBT, one must first deconstruct the multilayered architecture that governs its operation. Unlike traditional Web2 services that expose static REST endpoints protected by API keys, AIXBT functions as a decentralized agent. Its "API" is an amalgamation of blockchain interactions, agent-to-agent communication protocols, and paid HTTP gateways.

### **2.1 The Virtuals Protocol Foundation**

AIXBT is deployed as a "Virtual"—a tokenized AI agent—on the Virtuals Protocol.1 This protocol provides the infrastructure for agent existence, ownership, and interaction.

#### **2.1.1 The G.A.M.E. Framework**

The cognitive engine driving AIXBT is the G.A.M.E. (Generative Autonomous Multimodal Entities) framework.2 This framework replaces the traditional "backend" logic of a chatbot with a modular system designed for autonomy.

* **Perception Subsystem:** This module ingests raw data. For AIXBT, this involves scraping social media (X/Twitter), parsing on-chain transaction logs (Base Scan), and ingesting news feeds.3  
* **Strategic Planning Engine:** This is the decision-making core. It processes perceived data against the agent's "Goal" (e.g., "Identify high-momentum crypto narratives") and "Description" (personality and operational constraints).4  
* **Action Executor:** This module executes the plan. In the context of an API, the "actions" are the outputs we wish to consume—posting a tweet, generating a report, or responding to a direct query.3

For an MCP developer, understanding G.A.M.E. is crucial because the API interactions are not simple database lookups. They are requests to an autonomous entity to perform a cognitive task. The latency, determinism, and structure of the response will differ significantly from a standard SQL-backed API.

#### **2.1.2 State and Memory**

Virtuals Protocol agents utilize "long-term memory processors" employing knowledge graphs and embeddings.3 This implies that an MCP application interacting with AIXBT can maintain context over time. Unlike a stateless REST API, the AIXBT agent maintains a stateful session. The "Terminal API" provided by Virtuals allows developers to stream these internal states and logs, offering a window into the agent's "thought process" before a final output is generated.5

### **2.2 The x402 Economic Layer**

A defining characteristic of the AIXBT API is its integration with the x402 protocol.6 This represents a shift from subscription-based SaaS models to "pay-per-request" agentic commerce.

#### **2.2.1 HTTP 402: Payment Required**

The x402 protocol revives the dormant HTTP 402 status code. When an MCP client requests data from AIXBT (e.g., "Get latest whale alerts"), the server does not immediately return data. Instead, it responds with a 402 Payment Required status.

* **The Challenge:** The response body contains a "payment challenge"—a structured JSON object detailing the cost (e.g., 0.05 USDC), the recipient address (AIXBT's wallet), and the required network (Base).8  
* **The Resolution:** The client (the MCP server) must use a crypto wallet to sign a transaction or message authorization matching these requirements and resend the request with a proof-of-payment header.10

This mechanism is critical for the MCP specification. The MCP server implementation *must* include a wallet (likely a hot wallet or a secure signing module) to handle these real-time micro-negotiations.

### **2.3 The "Indigo" Data Layer**

The "Indigo" upgrade represents the specific capability set of the AIXBT agent.11 While Virtuals Protocol provides the brain, and x402 provides the payment rails, Indigo defines the *content*.

* **Data Sources:** CoinGecko, DeFiLlama, BubbleMaps.12  
* **Processing:** The agent synthesizes this raw data into "narratives." It doesn't just return the price of Bitcoin; it returns a contextual analysis of *why* Bitcoin is moving, citing on-chain flows and social sentiment.  
* **Outputs:** The API outputs include "Alpha signals," "Whale tracking alerts," and "Sentiment scores".11

### **2.4 MCP Architecture Fit**

The Model Context Protocol (MCP) is designed to standardize how AI models interact with external data. In this architecture:

* **MCP Host:** The user's AI assistant (e.g., Claude Desktop, IDE).  
* **MCP Server:** The middleware we are specifying. This server interacts with the AIXBT/Virtuals endpoints.  
* **MCP Client:** The internal logic within the Host that calls the Server.

The MCP Server for AIXBT will act as a wrapper. It will expose "Tools" (executable functions) and "Resources" (read-only data) to the Host. Internally, it will manage the complex x402 authentication and G.A.M.E. framework session management, presenting a clean interface to the user.

## **3\. Authentication and Security Specification**

AIXBT provides two distinct authentication methods: **API Key authentication** for the REST API and **x402 payment protocol** for pay-per-request access. Understanding both is essential for MCP integration.

### **3.1 REST API Authentication (Primary Method)**

The primary way to access AIXBT's data is through API key authentication on the `/v2` endpoints.

#### **3.1.1 API Key Types**

| Type | Access | How to Obtain |
|------|--------|---------------|
| **Demo Key** | Non-agentic endpoints, Bitcoin data only | Sign in at [aixbt.tech/settings/api-keys](https://aixbt.tech/settings/api-keys) |
| **Full-Access Key** | Non-agentic endpoints, full dataset | Subscribe to a [Data Plan](https://aixbt.tech/subscribe) |

Both key types use the same authentication method. The difference is the data returned and rate limits. For agentic endpoints (Indigo chat), use x402 pay-per-request or contact AIXBT support for API key access.

#### **3.1.2 Authentication Header**

Include your API key in the `x-api-key` header with every request:

```
curl -X GET "https://api.aixbt.tech/v2/projects" \
  -H "x-api-key: YOUR_API_KEY"
```

#### **3.1.3 Rate Limits**

- **Per minute:** 100 requests
- **Per day:** 100,000 requests

**Rate Limit Headers:** Every response includes headers showing current usage:
```
X-RateLimit-Limit-Minute: 100
X-RateLimit-Remaining-Minute: 99
X-RateLimit-Reset-Minute: 2025-01-15T12:01:00.000Z
X-RateLimit-Limit-Day: 100000
X-RateLimit-Remaining-Day: 99999
X-RateLimit-Reset-Day: 2025-01-16T00:00:00.000Z
```

When limits are exceeded, a `429 Too Many Requests` response is returned with a `Retry-After` header.

### **3.2 x402 Payment Protocol (Pay-Per-Request)**

The x402 protocol, developed by Coinbase, enables pay-per-request access without API keys. It uses the HTTP 402 status code for instant, on-chain micropayments.

#### **3.2.1 The x402 Handshake Flow**

1. **Initial Request:** The client sends a request to an x402-enabled endpoint.
```http
POST /x402/v1/agents/indigo HTTP/1.1
Host: api.aixbt.tech
Content-Type: application/json

{"messages": [{"role": "user", "content": "What narratives are gaining traction?"}]}
```

2. **Payment Challenge (402 Response):** The server responds with payment requirements.
```http
HTTP/1.1 402 Payment Required
Content-Type: application/json

{
  "error": "Payment Required",
  "payment": {
    "amount": "50000",
    "currency": "USDC",
    "token_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "recipient": "0x8e4b195c14f20e1ba4c40234f471e1781f293b45",
    "chain_id": 8453
  }
}
```

3. **Payment Signing:** The client signs an EIP-712 typed message authorizing the payment using their wallet private key.

4. **Authenticated Retry:** The client resends the request with the `X-Payment` header containing the signature.
```http
POST /x402/v1/agents/indigo HTTP/1.1
Host: api.aixbt.tech
X-Payment: type=exact; signature=0x92f...
```

5. **Data Response:** If valid, the server returns the requested data with HTTP 200.

#### **3.2.2 Automatic Refunds**

If a request fails to return meaningful results, AIXBT provides automatic on-chain refunds for:
- **404 errors** — No information found for your query
- **500 errors** — Server encountered an internal error

The refund response includes a transaction hash for on-chain verification:
```json
{
  "status": 404,
  "error": "No information found",
  "data": {
    "message": "The request was processed but no meaningful information was found.",
    "refund": {
      "attempted": true,
      "successful": true,
      "transactionHash": "0x...",
      "reason": "No information found"
    }
  }
}
```

#### **3.2.3 x402 Integration Libraries**

Use the official x402 helper libraries for automatic payment handling:

```bash
npm install x402-fetch viem
```

```javascript
import { wrapFetchWithPayment } from 'x402-fetch'
import { privateKeyToAccount } from 'viem/accounts'

const account = privateKeyToAccount(process.env.WALLET_PRIVATE_KEY)
const fetchWithPayment = wrapFetchWithPayment(fetch, account)

const response = await fetchWithPayment(
  'https://api.aixbt.tech/x402/v1/agents/indigo',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: [{ role: 'user', content: 'What narratives are gaining traction?' }],
    }),
  },
)
```

### **3.3 Security Considerations for MCP**

* **Wallet Management:** For x402, the MCP server must manage a hot wallet containing USDC on Base. The private key must be stored securely (environment variables, encrypted vaults).
* **Spending Limits:** Implement strict per-request and daily spending limits to prevent wallet draining.
* **API Key Security:** Store `AIXBT_API_KEY` securely; never commit to version control.

### **3.4 Hybrid Security Model for MCP**

The MCP server should support both authentication methods:

| Data Type | Authentication | Endpoint Prefix |
|-----------|----------------|-----------------|
| Projects, Signals, Clusters, Chains, Momentum | API Key (`x-api-key`) | `/v2/` |
| Indigo Chat (agentic) | API Key or x402 | `/v2/agents/indigo` or `/x402/v1/agents/indigo` |
| Surging Projects (real-time) | x402 only | `/x402/v1/projects` |

**MCP Server Configuration:**
- `AIXBT_API_KEY`: For REST API access
- `EVM_PRIVATE_KEY`: For x402 payment signing (optional)

## **4\. API Endpoint Documentation**

This section documents the official AIXBT API based on the public documentation at [docs.aixbt.tech](https://docs.aixbt.tech).

### **4.1 Base URLs**

| Purpose | Base URL |
|---------|----------|
| **REST API (v2)** | `https://api.aixbt.tech` |
| **x402 Endpoints** | `https://api.aixbt.tech/x402/v1` |
| **Virtuals Terminal (logs)** | `https://api-terminal.virtuals.io` |

All REST API endpoints are prefixed with `/v2`.

### **4.2 Response Format**

All endpoints return a consistent JSON structure:

**Success Response:**
```json
{
  "status": 200,
  "data": { ... },
  "pagination": {
    "page": 1,
    "limit": 50,
    "totalCount": 1000,
    "hasMore": true
  }
}
```

**Error Response:**
```json
{
  "status": 400,
  "error": "Invalid request parameters",
  "data": []
}
```

### **4.3 REST API Endpoints**

#### **4.3.1 List Projects**

Returns a paginated list of projects with signals, coingeckoData, and scores.

* **Endpoint:** `GET /v2/projects`
* **Authentication:** API Key (`x-api-key` header)

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | int | Page number (1-indexed). Default: 1 |
| `limit` | int | Results per page (max 50). Default: 50 |
| `projectIds` | string | Comma-separated project ObjectIds |
| `names` | string | Comma-separated project names (case-insensitive regex) |
| `xHandles` | string | Comma-separated X/Twitter handles |
| `tickers` | string | Comma-separated token tickers |
| `chain` | string | Filter by blockchain (see `/v2/projects/chains`) |
| `minMomentumScore` | number | Minimum momentum score threshold |
| `sortBy` | string | `momentumScore` (default) or `popularityScore` |
| `excludeStables` | boolean | Exclude stablecoins. Default: false |

**Response Schema:**
```json
{
  "status": 200,
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "ethereum",
      "description": "string",
      "rationale": "string",
      "xHandle": "ethereum",
      "momentumScore": 0.85,
      "popularityScore": 18,
      "coingeckoData": {
        "apiId": "ethereum",
        "type": "coin",
        "symbol": "eth",
        "slug": "string",
        "description": "string",
        "homepage": "string",
        "contractAddress": "string",
        "categories": ["string"]
      },
      "tokens": {
        "base": "0x...",
        "ethereum": "0x..."
      },
      "signals": [
        {
          "id": "string",
          "date": "2019-08-24T14:15:22Z",
          "reinforcedAt": "2019-08-24T14:15:22Z",
          "description": "string",
          "projectName": "string",
          "projectId": "string",
          "category": "TECH_EVENT",
          "officialSources": ["string"],
          "clusters": [{"id": "string", "name": "string"}]
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "totalCount": 1000,
    "hasMore": true
  }
}
```

#### **4.3.2 Get Project**

Returns a single project by ID with the 10 most recent signals.

* **Endpoint:** `GET /v2/projects/{id}`
* **Authentication:** API Key
* **Path Parameter:** `id` - MongoDB ObjectId of the project

#### **4.3.3 List Signals**

Returns signals with filtering and pagination support.

* **Endpoint:** `GET /v2/signals`
* **Authentication:** API Key

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `projectIds` | string | Comma-separated project IDs |
| `names` | string | Comma-separated project names (regex) |
| `xHandles` | string | Comma-separated X handles |
| `tickers` | string | Comma-separated token tickers |
| `clusterIds` | string | Comma-separated cluster IDs (OR logic) |
| `categories` | string | Comma-separated categories (OR logic) |
| `detectedAfter` | datetime | Filter by detection date (ISO 8601) |
| `detectedBefore` | datetime | Filter by detection date (ISO 8601) |
| `reinforcedAfter` | datetime | Filter by reinforced date (ISO 8601) |
| `reinforcedBefore` | datetime | Filter by reinforced date (ISO 8601) |
| `page` | int | Page number. Default: 1 |
| `limit` | int | Results per page (max 50). Default: 50 |

**Valid Categories:**
`FINANCIAL_EVENT`, `TOKEN_ECONOMICS`, `TECH_EVENT`, `MARKET_ACTIVITY`, `ONCHAIN_METRICS`, `PARTNERSHIP`, `TEAM_UPDATE`, `REGULATORY`, `WHALE_ACTIVITY`, `RISK_ALERT`, `VISIBILITY_EVENT`, `OPINION_SPECULATION`

**Response Schema:**
```json
{
  "status": 200,
  "data": [
    {
      "id": "string",
      "detectedAt": "2019-08-24T14:15:22Z",
      "reinforcedAt": "2019-08-24T14:15:22Z",
      "description": "string",
      "projectName": "string",
      "projectId": "string",
      "category": "WHALE_ACTIVITY",
      "officialSources": ["https://..."],
      "clusters": [{"id": "string", "name": "string"}]
    }
  ],
  "pagination": {...}
}
```

#### **4.3.4 Momentum History**

Returns hourly momentum history with cluster breakdown for a project.

* **Endpoint:** `GET /v2/projects/{id}/momentum`
* **Authentication:** API Key
* **Path Parameter:** `id` - The project ID

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | datetime | Start timestamp (ISO 8601). Default: 7 days ago |
| `end` | datetime | End timestamp (ISO 8601). Default: now |

**Response Schema:**
```json
{
  "status": 200,
  "data": {
    "projectId": "507f1f77bcf86cd799439011",
    "projectName": "ethereum",
    "data": [
      {
        "timestamp": "2025-11-30T12:00:00.000Z",
        "momentumScore": 0.43,
        "clusters": [
          {"id": "67ffa0cdd37b7e33fb723561", "name": "ethereum", "count": 3}
        ]
      }
    ]
  }
}
```

#### **4.3.5 List Clusters**

Returns all clusters (tracked communities and information sources).

* **Endpoint:** `GET /v2/clusters`
* **Authentication:** API Key

**Response Schema:**
```json
{
  "status": 200,
  "data": [
    {
      "id": "string",
      "name": "string",
      "description": "string"
    }
  ]
}
```

#### **4.3.6 List Chains**

Returns all available blockchain platforms for filtering.

* **Endpoint:** `GET /v2/projects/chains`
* **Authentication:** API Key

**Response Schema:**
```json
{
  "status": 200,
  "data": ["arbitrum-one", "base", "ethereum", "solana"]
}
```

#### **4.3.7 Chat with Indigo (REST API)**

Get a response from the AIXBT Indigo agent for market insights and narrative analysis.

* **Endpoint:** `POST /v2/agents/indigo`
* **Authentication:** API Key (requires special access) or use x402 endpoint

**Request Schema:**
```json
{
  "messages": [
    {"role": "user", "content": "Which developing narrative has the most potential?"},
    {"role": "assistant", "content": "Based on current momentum, ..."},
    {"role": "user", "content": "What are the main risks with that narrative?"}
  ]
}
```

**Response Schema:**
```json
{
  "status": 200,
  "error": "",
  "data": {
    "text": "This is a response from the Indigo agent."
  }
}
```

### **4.4 x402 Endpoints**

These endpoints require x402 payment instead of API keys.

#### **4.4.1 Indigo Chat (x402)**

* **Endpoint:** `POST /x402/v1/agents/indigo`
* **Authentication:** x402 payment
* **Request/Response:** Same schema as REST API `/v2/agents/indigo`

#### **4.4.2 Surging Projects (x402)**

Returns projects with surging momentum, updated in real-time.

* **Endpoint:** `GET /x402/v1/projects`
* **Authentication:** x402 payment

**Query Parameters:**

| Parameter | Description |
|-----------|-------------|
| `limit` | Maximum results (default: 50, max: 50) |
| `name` | Filter by project name (regex) |
| `ticker` | Filter by exact ticker symbol |
| `xHandle` | Filter by X handle |
| `sortBy` | Sort by `score` (default) or `popularityScore` |
| `minScore` | Minimum score threshold |

### **4.5 Virtuals Terminal API (Optional)**

For accessing the agent's internal reasoning logs.

* **Endpoint:** `GET /logs` via `api-terminal.virtuals.io`
* **Authentication:** Bearer Token (Virtuals API Key → JWT exchange)

**Response Schema:**
```json
{
  "data": [
    {
      "worker": "planner_module",
      "timestamp": "2025-12-23T10:00:00Z",
      "message": "Evaluating DeFi narrative signals..."
    }
  ]
}
```

## **5\. MCP Application Specification**

This section translates the API documentation above into a formal specification for a Model Context Protocol (MCP) server. This server will expose AIXBT's capabilities as **Resources** (data), **Tools** (functions), and **Prompts** (templates) to an MCP Host (e.g., Claude).

### **5.1 Server Configuration**

* **Server Name:** mcp-aixbt-server
* **Version:** 1.0.0
* **Transport:** Stdio (Standard Input/Output)
* **Dependencies:** `mcp`, `httpx`, `web3.py`, `eth-account`, `pydantic`

**Environment Variables:**
| Variable | Required | Description |
|----------|----------|-------------|
| `AIXBT_API_KEY` | Yes | API key for REST API access |
| `EVM_PRIVATE_KEY` | No | Private key for x402 payments (if using pay-per-request) |
| `BASE_RPC_URL` | No | Base chain RPC endpoint |

### **5.2 MCP Resources**

Resources in MCP represent read-only data that the LLM can access as context.

#### **5.2.1 aixbt://projects**

* **URI:** `aixbt://projects`
* **Name:** "AIXBT Projects List"
* **MIME Type:** application/json
* **Description:** Returns paginated list of crypto projects with momentum scores, signals, and CoinGecko data.
* **Implementation:** `GET /v2/projects` with API key auth
* **Parameters:** `page`, `limit`, `chain`, `sortBy`, `minMomentumScore`

#### **5.2.2 aixbt://projects/{id}**

* **URI Template:** `aixbt://projects/{id}`
* **Name:** "Project Details"
* **MIME Type:** application/json
* **Description:** Returns detailed information about a specific project including the 10 most recent signals.
* **Implementation:** `GET /v2/projects/{id}` with API key auth

#### **5.2.3 aixbt://signals**

* **URI:** `aixbt://signals`
* **Name:** "Market Signals"
* **MIME Type:** application/json
* **Description:** Returns market intelligence signals with filtering support.
* **Implementation:** `GET /v2/signals` with API key auth
* **Parameters:** `categories`, `tickers`, `names`, `clusterIds`, `detectedAfter`, `detectedBefore`

#### **5.2.4 aixbt://projects/{id}/momentum**

* **URI Template:** `aixbt://projects/{id}/momentum`
* **Name:** "Project Momentum History"
* **MIME Type:** application/json
* **Description:** Returns hourly momentum history with cluster breakdown for a project.
* **Implementation:** `GET /v2/projects/{id}/momentum` with API key auth
* **Parameters:** `start`, `end` (ISO 8601 timestamps)

#### **5.2.5 aixbt://clusters**

* **URI:** `aixbt://clusters`
* **Name:** "Information Clusters"
* **MIME Type:** application/json
* **Description:** Returns all tracked communities and information sources.
* **Implementation:** `GET /v2/clusters` with API key auth

#### **5.2.6 aixbt://chains**

* **URI:** `aixbt://chains`
* **Name:** "Supported Blockchains"
* **MIME Type:** application/json
* **Description:** Returns list of supported blockchain platforms for filtering.
* **Implementation:** `GET /v2/projects/chains` with API key auth

### **5.3 MCP Tools**

Tools in MCP are executable functions that the LLM can call to perform actions or queries with dynamic arguments.

#### **5.3.1 query_indigo**

* **Name:** `query_indigo`
* **Description:** Chat with the AIXBT Indigo agent for real-time market insights and narrative analysis.
* **Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "The question or analysis request for Indigo (e.g., 'What narratives are gaining traction?')"
    },
    "conversation_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "role": {"type": "string", "enum": ["user", "assistant"]},
          "content": {"type": "string"}
        }
      },
      "description": "Optional prior conversation for context"
    }
  },
  "required": ["message"]
}
```
* **Implementation:**
  1. Constructs messages array with conversation history + new message
  2. Calls `POST /v2/agents/indigo` (API key) or `POST /x402/v1/agents/indigo` (x402)
  3. Returns `data.text` from response

#### **5.3.2 list_projects**

* **Name:** `list_projects`
* **Description:** Search and filter crypto projects by various criteria.
* **Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "names": {
      "type": "string",
      "description": "Comma-separated project names to search (e.g., 'ethereum,bitcoin')"
    },
    "tickers": {
      "type": "string",
      "description": "Comma-separated token tickers (e.g., 'ETH,BTC')"
    },
    "chain": {
      "type": "string",
      "enum": ["arbitrum-one", "base", "ethereum", "solana"],
      "description": "Filter by blockchain"
    },
    "minMomentumScore": {
      "type": "number",
      "description": "Minimum momentum score threshold"
    },
    "sortBy": {
      "type": "string",
      "enum": ["momentumScore", "popularityScore"],
      "default": "momentumScore"
    },
    "limit": {
      "type": "integer",
      "default": 10,
      "maximum": 50
    }
  }
}
```
* **Implementation:** `GET /v2/projects` with query parameters

#### **5.3.3 get_signals**

* **Name:** `get_signals`
* **Description:** Retrieve market signals filtered by category, project, or time range.
* **Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "categories": {
      "type": "string",
      "description": "Comma-separated categories: WHALE_ACTIVITY, TECH_EVENT, PARTNERSHIP, etc."
    },
    "tickers": {
      "type": "string",
      "description": "Comma-separated token tickers to filter"
    },
    "detectedAfter": {
      "type": "string",
      "format": "date-time",
      "description": "Filter signals detected after this date (ISO 8601)"
    },
    "limit": {
      "type": "integer",
      "default": 20,
      "maximum": 50
    }
  }
}
```
* **Implementation:** `GET /v2/signals` with query parameters

#### **5.3.4 get_surging_projects**

* **Name:** `get_surging_projects`
* **Description:** Get projects with surging momentum in real-time (requires x402 payment).
* **Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "default": 10,
      "maximum": 50
    },
    "minScore": {
      "type": "number",
      "description": "Minimum surge score threshold"
    }
  }
}
```
* **Implementation:** `GET /x402/v1/projects` with x402 payment handling

### **5.4 MCP Prompts**

Prompts are reusable templates that help users interact with the server effectively.

#### **5.4.1 market_briefing**

* **Name:** `market_briefing`
* **Description:** Generates a comprehensive daily crypto market briefing using AIXBT's data.
* **Template:**
```
Using the list_projects tool sorted by momentumScore and the get_signals tool filtered to the last 24 hours, provide:
1. Top 3 projects by momentum with brief explanations
2. Key signals across categories (WHALE_ACTIVITY, TECH_EVENT, PARTNERSHIP)
3. Any notable narrative shifts or emerging trends
```

#### **5.4.2 token_analysis**

* **Name:** `token_analysis`
* **Arguments:** `ticker` - The token ticker to analyze
* **Template:**
```
Analyze {{ticker}} using the following steps:
1. Use list_projects with ticker={{ticker}} to get project details
2. Use get_signals filtered to {{ticker}} for recent activity
3. Use query_indigo to ask: "What is the current sentiment and key developments for {{ticker}}?"

Summarize: momentum score, recent signals, holder sentiment, and outlook.
```

#### **5.4.3 whale_watch**

* **Name:** `whale_watch`
* **Description:** Monitor whale activity across projects.
* **Template:**
```
Use get_signals with categories=WHALE_ACTIVITY to find recent whale movements.
For each significant whale signal, provide:
1. The project and token involved
2. The nature of the activity (accumulation/distribution)
3. Potential market implications
```

## **6\. Implementation Guide**

This section provides the technical roadmap for building the mcp-aixbt-server.

### **6.1 Prerequisites**

* **Python 3.10+**
* **AIXBT API Key:** Obtain from [aixbt.tech/settings/api-keys](https://aixbt.tech/settings/api-keys) (Demo or Full-Access)
* **EVM Wallet Private Key (optional):** Required only for x402 pay-per-request endpoints. Must be funded with USDC on Base.
* **RPC Endpoint (optional):** Connection to Base mainnet for x402 (e.g., via QuickNode or Alchemy)

### **6.2 Python Implementation Architecture**

Using FastAPI for HTTP server and httpx for async API calls.

```python
# mcp-aixbt-server implementation

import asyncio
import os
from typing import Optional
from datetime import datetime, timedelta

import httpx
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# Configuration
AIXBT_API_URL = "https://api.aixbt.tech"
AIXBT_API_KEY = os.environ.get("AIXBT_API_KEY")

app = FastAPI(title="AIXBT MCP Server")

# Pydantic models for request/response
class IndigoRequest(BaseModel):
    message: str
    conversation_history: Optional[list] = None

class SignalFilters(BaseModel):
    categories: Optional[str] = None
    tickers: Optional[str] = None
    detectedAfter: Optional[str] = None
    limit: int = 20

# HTTP client with API key auth
async def get_client():
    async with httpx.AsyncClient(
        base_url=AIXBT_API_URL,
        headers={"x-api-key": AIXBT_API_KEY}
    ) as client:
        yield client

# Simple in-memory cache
cache = {}
CACHE_TTL = timedelta(minutes=5)

def get_cached(key: str):
    if key in cache:
        data, timestamp = cache[key]
        if datetime.now() - timestamp < CACHE_TTL:
            return data
    return None

def set_cache(key: str, data):
    cache[key] = (data, datetime.now())

# REST API endpoints
@app.get("/resources/projects")
async def list_projects(
    page: int = 1,
    limit: int = 50,
    chain: Optional[str] = None,
    sortBy: str = "momentumScore",
    client: httpx.AsyncClient = Depends(get_client)
):
    cache_key = f"projects:{page}:{limit}:{chain}:{sortBy}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    params = {"page": page, "limit": limit, "sortBy": sortBy}
    if chain:
        params["chain"] = chain

    response = await client.get("/v2/projects", params=params)
    response.raise_for_status()
    data = response.json()
    set_cache(cache_key, data)
    return data

@app.get("/resources/signals")
async def get_signals(
    filters: SignalFilters = Depends(),
    client: httpx.AsyncClient = Depends(get_client)
):
    params = {"limit": filters.limit}
    if filters.categories:
        params["categories"] = filters.categories
    if filters.tickers:
        params["tickers"] = filters.tickers
    if filters.detectedAfter:
        params["detectedAfter"] = filters.detectedAfter

    response = await client.get("/v2/signals", params=params)
    response.raise_for_status()
    return response.json()

@app.get("/resources/clusters")
async def list_clusters(client: httpx.AsyncClient = Depends(get_client)):
    cached = get_cached("clusters")
    if cached:
        return cached

    response = await client.get("/v2/clusters")
    response.raise_for_status()
    data = response.json()
    set_cache("clusters", data)
    return data

@app.get("/resources/chains")
async def list_chains(client: httpx.AsyncClient = Depends(get_client)):
    cached = get_cached("chains")
    if cached:
        return cached

    response = await client.get("/v2/projects/chains")
    response.raise_for_status()
    data = response.json()
    set_cache("chains", data)
    return data

@app.post("/tools/query-indigo")
async def query_indigo(
    request: IndigoRequest,
    client: httpx.AsyncClient = Depends(get_client)
):
    messages = []
    if request.conversation_history:
        messages.extend(request.conversation_history)
    messages.append({"role": "user", "content": request.message})

    response = await client.post(
        "/v2/agents/indigo",
        json={"messages": messages}
    )

    if response.status_code == 404:
        return {"text": "No relevant information found for your query."}

    response.raise_for_status()
    return response.json()["data"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### **6.3 x402 Payment Handler (Optional)**

For pay-per-request endpoints, implement the x402 handshake:

```python
from eth_account import Account
from eth_account.messages import encode_typed_data

EVM_PRIVATE_KEY = os.environ.get("EVM_PRIVATE_KEY")

async def handle_x402_payment(response):
    """Handle 402 Payment Required challenge."""
    challenge = response.json()["payment"]

    # EIP-712 typed data for x402
    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"}
            ],
            "Payment": [
                {"name": "recipient", "type": "address"},
                {"name": "amount", "type": "uint256"},
                {"name": "token", "type": "address"}
            ]
        },
        "primaryType": "Payment",
        "domain": {
            "name": "x402",
            "version": "1",
            "chainId": challenge["chain_id"]
        },
        "message": {
            "recipient": challenge["recipient"],
            "amount": int(challenge["amount"]),
            "token": challenge["token_address"]
        }
    }

    account = Account.from_key(EVM_PRIVATE_KEY)
    signed = account.sign_typed_data(typed_data)

    return f"type=exact; signature={signed.signature.hex()}"

async def fetch_with_x402(client, method, url, **kwargs):
    """Wrapper that handles x402 payment automatically."""
    response = await client.request(method, url, **kwargs)

    if response.status_code == 402:
        payment_header = await handle_x402_payment(response)
        kwargs.setdefault("headers", {})
        kwargs["headers"]["X-Payment"] = payment_header
        response = await client.request(method, url, **kwargs)

    return response
```

### **6.4 Handling Rate Limits and Costs**

**Rate Limit Handling:**
```python
import time

async def handle_rate_limit(response):
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        await asyncio.sleep(retry_after)
        return True
    return False
```

**Cost Controls for x402:**
* **Per-request limit:** Verify `challenge["amount"] <= MAX_PRICE_PER_CALL` before signing
* **Daily budget:** Track cumulative spend and reject when threshold exceeded
* **Caching:** Cache frequently accessed resources (5-minute TTL) to minimize costs

## **7\. Project Structure**

This section defines the directory layout and module organization for the MCP server.

### **7.1 Directory Layout**

```
mcp-aixbt-server/
├── src/
│   └── mcp_aixbt/
│       ├── __init__.py
│       ├── main.py                 # Application entry point
│       ├── config.py               # Configuration management
│       ├── models/
│       │   ├── __init__.py
│       │   ├── projects.py         # Project data models
│       │   ├── signals.py          # Signal data models
│       │   ├── requests.py         # Request schemas
│       │   └── responses.py        # Response schemas
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── aixbt.py            # AIXBT REST API client
│       │   └── x402.py             # x402 payment handler
│       ├── services/
│       │   ├── __init__.py
│       │   ├── projects.py         # Project service layer
│       │   ├── signals.py          # Signals service layer
│       │   └── indigo.py           # Indigo chat service
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── resources.py        # MCP Resource endpoints
│       │   ├── tools.py            # MCP Tool endpoints
│       │   └── health.py           # Health check endpoints
│       ├── middleware/
│       │   ├── __init__.py
│       │   ├── logging.py          # Request/response logging
│       │   └── rate_limit.py       # Rate limit handling
│       └── utils/
│           ├── __init__.py
│           ├── cache.py            # Caching utilities
│           └── errors.py           # Error handling utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_config.py
│   │   ├── test_models.py
│   │   └── test_x402.py
│   └── integration/
│       ├── __init__.py
│       ├── test_aixbt_client.py
│       └── test_endpoints.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example                    # Environment template
├── .gitignore
├── pyproject.toml                  # Project configuration
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
└── README.md
```

### **7.2 Module Responsibilities**

| Module | Responsibility |
|--------|----------------|
| `main.py` | FastAPI app initialization, router registration, lifespan events |
| `config.py` | Environment variable loading, validation, typed settings |
| `models/` | Pydantic schemas for all data types |
| `clients/` | HTTP clients for external APIs (AIXBT, x402) |
| `services/` | Business logic layer between routes and clients |
| `routers/` | FastAPI route definitions |
| `middleware/` | Cross-cutting concerns (logging, rate limiting) |
| `utils/` | Shared utilities (caching, error handling) |

## **8\. Data Models Specification**

Complete Pydantic model definitions for type safety and validation.

### **8.1 Configuration Models**

```python
# src/mcp_aixbt/config.py

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration with validation."""

    # Required
    aixbt_api_key: SecretStr = Field(
        ...,
        description="AIXBT API key for REST API access"
    )

    # Optional - x402 support
    evm_private_key: Optional[SecretStr] = Field(
        default=None,
        description="EVM private key for x402 payments"
    )
    base_rpc_url: Optional[str] = Field(
        default="https://mainnet.base.org",
        description="Base chain RPC endpoint"
    )

    # Server settings
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000, ge=1, le=65535)
    debug: bool = Field(default=False)

    # Rate limiting
    rate_limit_per_minute: int = Field(default=100, ge=1)
    rate_limit_per_day: int = Field(default=100000, ge=1)

    # Caching
    cache_ttl_seconds: int = Field(default=300, ge=0)  # 5 minutes

    # x402 budget controls
    max_price_per_call_usdc: float = Field(default=1.0, ge=0)
    max_spend_per_day_usdc: float = Field(default=10.0, ge=0)

    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")  # "json" or "text"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid:
            raise ValueError(f"log_level must be one of {valid}")
        return v.upper()

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }
```

### **8.2 Domain Models**

```python
# src/mcp_aixbt/models/projects.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class SignalCategory(str, Enum):
    FINANCIAL_EVENT = "FINANCIAL_EVENT"
    TOKEN_ECONOMICS = "TOKEN_ECONOMICS"
    TECH_EVENT = "TECH_EVENT"
    MARKET_ACTIVITY = "MARKET_ACTIVITY"
    ONCHAIN_METRICS = "ONCHAIN_METRICS"
    PARTNERSHIP = "PARTNERSHIP"
    TEAM_UPDATE = "TEAM_UPDATE"
    REGULATORY = "REGULATORY"
    WHALE_ACTIVITY = "WHALE_ACTIVITY"
    RISK_ALERT = "RISK_ALERT"
    VISIBILITY_EVENT = "VISIBILITY_EVENT"
    OPINION_SPECULATION = "OPINION_SPECULATION"

class Cluster(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class CoingeckoData(BaseModel):
    api_id: str = Field(alias="apiId")
    type: Optional[str] = None
    symbol: str
    slug: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    contract_address: Optional[str] = Field(default=None, alias="contractAddress")
    categories: List[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

class Signal(BaseModel):
    id: str
    detected_at: datetime = Field(alias="detectedAt")
    reinforced_at: Optional[datetime] = Field(default=None, alias="reinforcedAt")
    description: str
    project_name: str = Field(alias="projectName")
    project_id: str = Field(alias="projectId")
    category: SignalCategory
    official_sources: List[str] = Field(default_factory=list, alias="officialSources")
    clusters: List[Cluster] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

class Project(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    rationale: Optional[str] = None
    x_handle: Optional[str] = Field(default=None, alias="xHandle")
    momentum_score: float = Field(ge=0, le=1, alias="momentumScore")
    popularity_score: int = Field(ge=0, alias="popularityScore")
    coingecko_data: Optional[CoingeckoData] = Field(default=None, alias="coingeckoData")
    tokens: Dict[str, str] = Field(default_factory=dict)
    signals: List[Signal] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

class MomentumDataPoint(BaseModel):
    timestamp: datetime
    momentum_score: float = Field(alias="momentumScore")
    clusters: List[Dict[str, any]] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

class ProjectMomentum(BaseModel):
    project_id: str = Field(alias="projectId")
    project_name: str = Field(alias="projectName")
    data: List[MomentumDataPoint]

    model_config = {"populate_by_name": True}
```

### **8.3 Request/Response Models**

```python
# src/mcp_aixbt/models/requests.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=10000)

class IndigoRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    conversation_history: Optional[List[ChatMessage]] = None

class ProjectFilters(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=50, ge=1, le=50)
    project_ids: Optional[str] = Field(default=None, alias="projectIds")
    names: Optional[str] = None
    x_handles: Optional[str] = Field(default=None, alias="xHandles")
    tickers: Optional[str] = None
    chain: Optional[str] = None
    min_momentum_score: Optional[float] = Field(default=None, ge=0, le=1, alias="minMomentumScore")
    sort_by: str = Field(default="momentumScore", alias="sortBy")
    exclude_stables: bool = Field(default=False, alias="excludeStables")

class SignalFilters(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=50, ge=1, le=50)
    project_ids: Optional[str] = Field(default=None, alias="projectIds")
    names: Optional[str] = None
    x_handles: Optional[str] = Field(default=None, alias="xHandles")
    tickers: Optional[str] = None
    cluster_ids: Optional[str] = Field(default=None, alias="clusterIds")
    categories: Optional[str] = None
    detected_after: Optional[datetime] = Field(default=None, alias="detectedAfter")
    detected_before: Optional[datetime] = Field(default=None, alias="detectedBefore")
    reinforced_after: Optional[datetime] = Field(default=None, alias="reinforcedAfter")
    reinforced_before: Optional[datetime] = Field(default=None, alias="reinforcedBefore")

class MomentumFilters(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
```

```python
# src/mcp_aixbt/models/responses.py

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List
from datetime import datetime

T = TypeVar("T")

class Pagination(BaseModel):
    page: int
    limit: int
    total_count: int = Field(alias="totalCount")
    has_more: bool = Field(alias="hasMore")

    model_config = {"populate_by_name": True}

class APIResponse(BaseModel, Generic[T]):
    status: int
    data: T
    error: Optional[str] = None
    pagination: Optional[Pagination] = None

class IndigoResponse(BaseModel):
    text: str

class HealthStatus(BaseModel):
    status: str = Field(pattern="^(healthy|unhealthy)$")
    timestamp: datetime
    version: str
    checks: dict = Field(default_factory=dict)

class ErrorResponse(BaseModel):
    status: int
    error: str
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[dict] = None
```

## **9\. Dependency Management**

### **9.1 Production Dependencies (requirements.txt)**

```
# Core framework
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic==2.10.4
pydantic-settings==2.7.0

# HTTP client
httpx==0.28.1

# Blockchain/crypto (optional - for x402)
web3==7.6.0
eth-account==0.13.5

# Utilities
python-dotenv==1.0.1
structlog==24.4.0

# Production server
gunicorn==23.0.0
```

### **9.2 Development Dependencies (requirements-dev.txt)**

```
-r requirements.txt

# Testing
pytest==8.3.4
pytest-asyncio==0.25.0
pytest-cov==6.0.0
pytest-mock==3.14.0
respx==0.22.0  # httpx mocking

# Code quality
ruff==0.8.4
mypy==1.14.0
black==24.10.0

# Development tools
ipython==8.30.0
pre-commit==4.0.1
```

### **9.3 pyproject.toml**

```toml
[project]
name = "mcp-aixbt-server"
version = "1.0.0"
description = "MCP Server for AIXBT Market Intelligence"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["mcp", "aixbt", "crypto", "market-intelligence", "fastapi"]

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.7.0",
    "httpx>=0.28.0",
    "python-dotenv>=1.0.0",
    "structlog>=24.0.0",
]

[project.optional-dependencies]
x402 = [
    "web3>=7.0.0",
    "eth-account>=0.13.0",
]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.25.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.14.0",
]

[project.scripts]
mcp-aixbt = "mcp_aixbt.main:run"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=src/mcp_aixbt --cov-report=term-missing"
```

## **10\. Deployment Configuration**

### **10.1 Environment Template (.env.example)**

```bash
# =============================================================================
# MCP AIXBT Server Configuration
# =============================================================================
# Copy this file to .env and fill in your values

# -----------------------------------------------------------------------------
# Required Configuration
# -----------------------------------------------------------------------------

# AIXBT API Key (obtain from https://aixbt.tech/settings/api-keys)
AIXBT_API_KEY=your_api_key_here

# -----------------------------------------------------------------------------
# Optional: x402 Pay-Per-Request Configuration
# -----------------------------------------------------------------------------

# EVM private key for x402 payments (keep secret!)
# Only needed if using /x402/v1/* endpoints
# EVM_PRIVATE_KEY=0x...

# Base chain RPC URL (default: https://mainnet.base.org)
# BASE_RPC_URL=https://mainnet.base.org

# x402 budget controls
# MAX_PRICE_PER_CALL_USDC=1.0
# MAX_SPEND_PER_DAY_USDC=10.0

# -----------------------------------------------------------------------------
# Server Configuration
# -----------------------------------------------------------------------------

# Server host and port
HOST=127.0.0.1
PORT=8000

# Debug mode (set to false in production)
DEBUG=false

# -----------------------------------------------------------------------------
# Rate Limiting
# -----------------------------------------------------------------------------

RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_DAY=100000

# -----------------------------------------------------------------------------
# Caching
# -----------------------------------------------------------------------------

# Cache TTL in seconds (default: 300 = 5 minutes)
CACHE_TTL_SECONDS=300

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log format: json or text
LOG_FORMAT=json
```

### **10.2 Dockerfile**

```dockerfile
# docker/Dockerfile

# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim as production

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Run application
CMD ["python", "-m", "uvicorn", "mcp_aixbt.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **10.3 Docker Compose**

```yaml
# docker/docker-compose.yml

version: "3.9"

services:
  mcp-aixbt:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: mcp-aixbt-server
    restart: unless-stopped
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - AIXBT_API_KEY=${AIXBT_API_KEY}
      - EVM_PRIVATE_KEY=${EVM_PRIVATE_KEY:-}
      - BASE_RPC_URL=${BASE_RPC_URL:-https://mainnet.base.org}
      - HOST=0.0.0.0
      - PORT=8000
      - DEBUG=${DEBUG:-false}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - LOG_FORMAT=${LOG_FORMAT:-json}
      - CACHE_TTL_SECONDS=${CACHE_TTL_SECONDS:-300}
      - MAX_PRICE_PER_CALL_USDC=${MAX_PRICE_PER_CALL_USDC:-1.0}
      - MAX_SPEND_PER_DAY_USDC=${MAX_SPEND_PER_DAY_USDC:-10.0}
    healthcheck:
      test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Optional: Redis for distributed caching (if scaling horizontally)
  # redis:
  #   image: redis:7-alpine
  #   container_name: mcp-aixbt-redis
  #   restart: unless-stopped
  #   ports:
  #     - "6379:6379"
  #   volumes:
  #     - redis_data:/data
  #   healthcheck:
  #     test: ["CMD", "redis-cli", "ping"]
  #     interval: 10s
  #     timeout: 5s
  #     retries: 5

# volumes:
#   redis_data:
```

## **11\. Testing Strategy**

### **11.1 Testing Approach**

| Test Type | Purpose | Tools | Coverage Target |
|-----------|---------|-------|-----------------|
| **Unit Tests** | Test individual functions/classes in isolation | pytest, pytest-mock | 80%+ |
| **Integration Tests** | Test API client interactions with mocked responses | pytest, respx | Key flows |
| **E2E Tests** | Test full request/response cycle | pytest, TestClient | Critical paths |

### **11.2 Test Configuration (conftest.py)**

```python
# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import httpx

from mcp_aixbt.main import app
from mcp_aixbt.config import Settings

@pytest.fixture
def test_settings():
    """Provide test configuration."""
    return Settings(
        aixbt_api_key="test_api_key_12345",
        host="127.0.0.1",
        port=8000,
        debug=True,
        log_level="DEBUG",
        cache_ttl_seconds=0,  # Disable caching in tests
    )

@pytest.fixture
def client(test_settings):
    """Provide test client with mocked settings."""
    with patch("mcp_aixbt.config.get_settings", return_value=test_settings):
        with TestClient(app) as test_client:
            yield test_client

@pytest.fixture
def mock_aixbt_response():
    """Factory for mock AIXBT API responses."""
    def _make_response(data, status=200, pagination=None):
        response = {"status": status, "data": data}
        if pagination:
            response["pagination"] = pagination
        return response
    return _make_response

@pytest.fixture
def sample_project():
    """Provide sample project data."""
    return {
        "id": "507f1f77bcf86cd799439011",
        "name": "ethereum",
        "xHandle": "ethereum",
        "momentumScore": 0.85,
        "popularityScore": 18,
        "coingeckoData": {
            "apiId": "ethereum",
            "symbol": "eth",
            "categories": ["Smart Contract Platform"]
        },
        "signals": []
    }

@pytest.fixture
def sample_signal():
    """Provide sample signal data."""
    return {
        "id": "signal123",
        "detectedAt": "2025-12-23T10:00:00Z",
        "reinforcedAt": "2025-12-23T11:00:00Z",
        "description": "Major protocol upgrade announced",
        "projectName": "ethereum",
        "projectId": "507f1f77bcf86cd799439011",
        "category": "TECH_EVENT",
        "officialSources": ["https://ethereum.org"],
        "clusters": [{"id": "c1", "name": "DeFi"}]
    }
```

### **11.3 Unit Tests**

```python
# tests/unit/test_models.py

import pytest
from datetime import datetime
from pydantic import ValidationError

from mcp_aixbt.models.projects import Project, Signal, SignalCategory
from mcp_aixbt.models.requests import IndigoRequest, ChatMessage

class TestSignalCategory:
    def test_valid_categories(self):
        for cat in SignalCategory:
            assert cat.value in [
                "FINANCIAL_EVENT", "TOKEN_ECONOMICS", "TECH_EVENT",
                "MARKET_ACTIVITY", "ONCHAIN_METRICS", "PARTNERSHIP",
                "TEAM_UPDATE", "REGULATORY", "WHALE_ACTIVITY",
                "RISK_ALERT", "VISIBILITY_EVENT", "OPINION_SPECULATION"
            ]

class TestProjectModel:
    def test_valid_project(self, sample_project):
        project = Project(**sample_project)
        assert project.name == "ethereum"
        assert project.momentum_score == 0.85
        assert 0 <= project.momentum_score <= 1

    def test_momentum_score_bounds(self):
        with pytest.raises(ValidationError):
            Project(
                id="123",
                name="test",
                momentumScore=1.5,  # Invalid: > 1
                popularityScore=10
            )

class TestIndigoRequest:
    def test_valid_request(self):
        req = IndigoRequest(message="What narratives are trending?")
        assert req.message == "What narratives are trending?"
        assert req.conversation_history is None

    def test_with_history(self):
        req = IndigoRequest(
            message="Follow up question",
            conversation_history=[
                ChatMessage(role="user", content="Initial question"),
                ChatMessage(role="assistant", content="Initial response")
            ]
        )
        assert len(req.conversation_history) == 2

    def test_empty_message_rejected(self):
        with pytest.raises(ValidationError):
            IndigoRequest(message="")

    def test_invalid_role_rejected(self):
        with pytest.raises(ValidationError):
            ChatMessage(role="system", content="test")  # Only user/assistant allowed
```

```python
# tests/unit/test_config.py

import pytest
from pydantic import ValidationError

from mcp_aixbt.config import Settings

class TestSettings:
    def test_required_api_key(self):
        with pytest.raises(ValidationError):
            Settings()  # Missing required aixbt_api_key

    def test_defaults(self):
        settings = Settings(aixbt_api_key="test_key")
        assert settings.host == "127.0.0.1"
        assert settings.port == 8000
        assert settings.debug is False
        assert settings.cache_ttl_seconds == 300

    def test_invalid_port(self):
        with pytest.raises(ValidationError):
            Settings(aixbt_api_key="test", port=70000)

    def test_invalid_log_level(self):
        with pytest.raises(ValidationError):
            Settings(aixbt_api_key="test", log_level="INVALID")

    def test_valid_log_levels(self):
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            settings = Settings(aixbt_api_key="test", log_level=level)
            assert settings.log_level == level
```

### **11.4 Integration Tests**

```python
# tests/integration/test_endpoints.py

import pytest
import respx
from httpx import Response

class TestProjectsEndpoint:
    @respx.mock
    def test_list_projects_success(self, client, mock_aixbt_response, sample_project):
        # Mock AIXBT API
        respx.get("https://api.aixbt.tech/v2/projects").mock(
            return_value=Response(
                200,
                json=mock_aixbt_response(
                    data=[sample_project],
                    pagination={"page": 1, "limit": 50, "totalCount": 1, "hasMore": False}
                )
            )
        )

        response = client.get("/resources/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == "ethereum"

    @respx.mock
    def test_list_projects_with_filters(self, client, mock_aixbt_response, sample_project):
        respx.get("https://api.aixbt.tech/v2/projects").mock(
            return_value=Response(200, json=mock_aixbt_response([sample_project]))
        )

        response = client.get(
            "/resources/projects",
            params={"chain": "ethereum", "minMomentumScore": 0.5}
        )

        assert response.status_code == 200

    @respx.mock
    def test_list_projects_api_error(self, client):
        respx.get("https://api.aixbt.tech/v2/projects").mock(
            return_value=Response(401, json={"error": "Invalid API key"})
        )

        response = client.get("/resources/projects")
        assert response.status_code == 401

class TestSignalsEndpoint:
    @respx.mock
    def test_list_signals_success(self, client, mock_aixbt_response, sample_signal):
        respx.get("https://api.aixbt.tech/v2/signals").mock(
            return_value=Response(200, json=mock_aixbt_response([sample_signal]))
        )

        response = client.get("/resources/signals")

        assert response.status_code == 200
        data = response.json()
        assert data["data"][0]["category"] == "TECH_EVENT"

    @respx.mock
    def test_filter_by_category(self, client, mock_aixbt_response, sample_signal):
        respx.get("https://api.aixbt.tech/v2/signals").mock(
            return_value=Response(200, json=mock_aixbt_response([sample_signal]))
        )

        response = client.get(
            "/resources/signals",
            params={"categories": "WHALE_ACTIVITY,TECH_EVENT"}
        )

        assert response.status_code == 200

class TestIndigoEndpoint:
    @respx.mock
    def test_query_indigo_success(self, client):
        respx.post("https://api.aixbt.tech/v2/agents/indigo").mock(
            return_value=Response(200, json={
                "status": 200,
                "data": {"text": "Based on current momentum..."}
            })
        )

        response = client.post(
            "/tools/query-indigo",
            json={"message": "What narratives are trending?"}
        )

        assert response.status_code == 200
        assert "text" in response.json()

    @respx.mock
    def test_query_indigo_not_found(self, client):
        respx.post("https://api.aixbt.tech/v2/agents/indigo").mock(
            return_value=Response(404, json={"status": 404, "error": "No information found"})
        )

        response = client.post(
            "/tools/query-indigo",
            json={"message": "Unknown topic"}
        )

        assert response.status_code == 200  # We handle 404 gracefully
        assert "No relevant information" in response.json()["text"]

class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
```

### **11.5 Running Tests**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/mcp_aixbt --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run tests matching pattern
pytest -k "test_indigo"

# Run with verbose output
pytest -v --tb=short
```

## **12\. Logging and Monitoring**

### **12.1 Logging Configuration**

```python
# src/mcp_aixbt/middleware/logging.py

import structlog
import logging
from datetime import datetime
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

from mcp_aixbt.config import get_settings

def configure_logging():
    """Configure structured logging."""
    settings = get_settings()

    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name: str = None):
    """Get a configured logger instance."""
    return structlog.get_logger(name)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        # Bind request context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )

        logger = get_logger("http")
        logger.info("request_started")

        try:
            response = await call_next(request)

            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "request_failed",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration_ms, 2),
            )
            raise
```

### **12.2 Log Output Examples**

**JSON format (production):**
```json
{"event": "request_started", "level": "info", "timestamp": "2025-12-23T10:00:00Z", "request_id": "a1b2c3d4", "method": "GET", "path": "/resources/projects"}
{"event": "request_completed", "level": "info", "timestamp": "2025-12-23T10:00:00Z", "request_id": "a1b2c3d4", "status_code": 200, "duration_ms": 45.32}
```

**Text format (development):**
```
2025-12-23 10:00:00 [info     ] request_started    request_id=a1b2c3d4 method=GET path=/resources/projects
2025-12-23 10:00:00 [info     ] request_completed  request_id=a1b2c3d4 status_code=200 duration_ms=45.32
```

### **12.3 Metrics to Track**

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests by method, path, status |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `aixbt_api_calls_total` | Counter | Calls to AIXBT API by endpoint |
| `aixbt_api_errors_total` | Counter | AIXBT API errors by type |
| `x402_payments_total` | Counter | x402 payments made |
| `x402_spend_usdc` | Gauge | Cumulative x402 spend |
| `cache_hits_total` | Counter | Cache hits |
| `cache_misses_total` | Counter | Cache misses |

## **13\. Health Check Endpoints**

### **13.1 Health Router Implementation**

```python
# src/mcp_aixbt/routers/health.py

from fastapi import APIRouter, Depends
from datetime import datetime
import httpx

from mcp_aixbt.config import get_settings, Settings
from mcp_aixbt.models.responses import HealthStatus

router = APIRouter(tags=["Health"])

VERSION = "1.0.0"

@router.get("/health", response_model=HealthStatus)
async def health_check(settings: Settings = Depends(get_settings)):
    """
    Basic health check endpoint.
    Returns healthy if the service is running.
    """
    return HealthStatus(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=VERSION,
        checks={}
    )

@router.get("/health/ready", response_model=HealthStatus)
async def readiness_check(settings: Settings = Depends(get_settings)):
    """
    Readiness check - verifies the service can handle requests.
    Checks:
    - Configuration is valid
    - AIXBT API is reachable
    """
    checks = {}
    overall_healthy = True

    # Check 1: Configuration
    try:
        _ = settings.aixbt_api_key.get_secret_value()
        checks["config"] = {"status": "pass", "message": "Configuration loaded"}
    except Exception as e:
        checks["config"] = {"status": "fail", "message": str(e)}
        overall_healthy = False

    # Check 2: AIXBT API connectivity
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://api.aixbt.tech/v2/projects/chains",
                headers={"x-api-key": settings.aixbt_api_key.get_secret_value()}
            )
            if response.status_code == 200:
                checks["aixbt_api"] = {"status": "pass", "message": "AIXBT API reachable"}
            else:
                checks["aixbt_api"] = {
                    "status": "warn",
                    "message": f"AIXBT API returned {response.status_code}"
                }
    except Exception as e:
        checks["aixbt_api"] = {"status": "fail", "message": str(e)}
        overall_healthy = False

    return HealthStatus(
        status="healthy" if overall_healthy else "unhealthy",
        timestamp=datetime.utcnow(),
        version=VERSION,
        checks=checks
    )

@router.get("/health/live")
async def liveness_check():
    """
    Liveness check - minimal check that service is running.
    Used by Kubernetes liveness probes.
    """
    return {"status": "alive"}
```

### **13.2 Health Check Response Examples**

**GET /health**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-23T10:00:00Z",
  "version": "1.0.0",
  "checks": {}
}
```

**GET /health/ready**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-23T10:00:00Z",
  "version": "1.0.0",
  "checks": {
    "config": {
      "status": "pass",
      "message": "Configuration loaded"
    },
    "aixbt_api": {
      "status": "pass",
      "message": "AIXBT API reachable"
    }
  }
}
```

**GET /health/live**
```json
{
  "status": "alive"
}
```

## **14\. Strategic Implications and Future Outlook**

The integration of AIXBT into the MCP ecosystem represents a paradigmatic shift in how AI models consume information.

### **14.1 From Data Retrieval to Agentic Commerce**

Traditional APIs are passive; they wait for a subscription-validated request. The AIXBT x402 integration demonstrates **agentic commerce**, where the software (the MCP server) actively negotiates a price and pays for data autonomously. This allows for a "just-in-time" economic model where users pay only for the high-value insights they typically need, rather than a flat monthly subscription.

### **14.2 The Recursive Intelligence Loop**

By exposing AIXBT as an MCP server, developers enable **recursive intelligence**. A Host LLM (like Claude) can query AIXBT for a market anomaly, receive a "whale alert," and then autonomously use that alert to trigger a secondary tool (e.g., a portfolio rebalancing tool). The AIXBT agent becomes a specialized "sub-processor" for the generalist LLM.

### **14.3 Scalability via Base L2**

The choice of the Base blockchain for AIXBT 19 is strategic. The low transaction fees of the Optimism stack allow for the high-frequency micro-transactions required by x402 without making the cost of "asking a question" prohibitive. This scalability ensures that the MCP server remains responsive and cost-effective.

## **15\. Conclusion**

The AIXBT public API, while not documented in a traditional Swagger file, is accessible through the synthesis of the Virtuals Protocol SDK and the x402 payment standard. This report has defined the necessary specifications to build an MCP server that bridges this gap.

By implementing the query\_agent and get\_signals tools defined in Section 5, and wrapping them in the authentication logic detailed in Section 3, developers can create a powerful interface. This interface unlocks the "Indigo" intelligence layer—narrative detection, whale tracking, and sentiment analysis—transforming AIXBT from a standalone chatbot into a composable building block for the next generation of intelligent financial applications.

The key to successful integration lies in the robust handling of the x402 402 Payment Required handshake, ensuring that the autonomous economic negotiation is secure, budget-constrained, and transparent to the end-user.

# **Appendix A: API Request/Response Examples**

### **A.1 List Projects (REST API)**

**Request:**
```http
GET /v2/projects?limit=5&sortBy=momentumScore HTTP/1.1
Host: api.aixbt.tech
x-api-key: YOUR_API_KEY
```

**Response (200 OK):**
```json
{
  "status": 200,
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "ethereum",
      "xHandle": "ethereum",
      "momentumScore": 0.85,
      "popularityScore": 18,
      "coingeckoData": {
        "apiId": "ethereum",
        "symbol": "eth",
        "categories": ["Smart Contract Platform"]
      },
      "signals": [
        {
          "id": "signal123",
          "detectedAt": "2025-12-23T10:00:00Z",
          "description": "Major protocol upgrade announced",
          "category": "TECH_EVENT"
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 5,
    "totalCount": 1000,
    "hasMore": true
  }
}
```

### **A.2 List Signals with Filters (REST API)**

**Request:**
```http
GET /v2/signals?categories=WHALE_ACTIVITY,TECH_EVENT&detectedAfter=2025-12-01T00:00:00Z&limit=10 HTTP/1.1
Host: api.aixbt.tech
x-api-key: YOUR_API_KEY
```

**Response (200 OK):**
```json
{
  "status": 200,
  "data": [
    {
      "id": "signal456",
      "detectedAt": "2025-12-23T08:30:00Z",
      "reinforcedAt": "2025-12-23T09:00:00Z",
      "description": "Large ETH accumulation detected in whale wallets",
      "projectName": "ethereum",
      "projectId": "507f1f77bcf86cd799439011",
      "category": "WHALE_ACTIVITY",
      "officialSources": ["https://etherscan.io/tx/..."],
      "clusters": [{"id": "cluster1", "name": "DeFi"}]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "totalCount": 50,
    "hasMore": true
  }
}
```

### **A.3 Chat with Indigo (REST API)**

**Request:**
```http
POST /v2/agents/indigo HTTP/1.1
Host: api.aixbt.tech
x-api-key: YOUR_API_KEY
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "What narratives are gaining traction today?"}
  ]
}
```

**Response (200 OK):**
```json
{
  "status": 200,
  "error": "",
  "data": {
    "text": "Based on current momentum data, the top narratives gaining traction are: 1) AI tokens seeing increased whale accumulation, 2) Layer 2 scaling solutions with new partnership announcements, 3) DeFi protocols launching token burns..."
  }
}
```

### **A.4 Chat with Indigo (x402 Pay-Per-Request)**

**Initial Request:**
```http
POST /x402/v1/agents/indigo HTTP/1.1
Host: api.aixbt.tech
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "What narratives are gaining traction today?"}
  ]
}
```

**Response (402 Payment Required):**
```json
{
  "error": "Payment Required",
  "payment": {
    "amount": "50000",
    "currency": "USDC",
    "token_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "recipient": "0x8e4b195c14f20e1ba4c40234f471e1781f293b45",
    "chain_id": 8453
  }
}
```

**Retry with Payment:**
```http
POST /x402/v1/agents/indigo HTTP/1.1
Host: api.aixbt.tech
Content-Type: application/json
X-Payment: type=exact; signature=0x92f...

{
  "messages": [
    {"role": "user", "content": "What narratives are gaining traction today?"}
  ]
}
```

**Response (200 OK):**
```json
{
  "status": 200,
  "data": {
    "text": "Based on current momentum data..."
  }
}
```

### **A.5 Error Responses**

**Rate Limit Exceeded (429):**
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded (minute). Try again after 2025-01-15T12:01:00.000Z",
  "code": "RATE_LIMIT_EXCEEDED",
  "limitType": "minute"
}
```

**Invalid API Key (401):**
```json
{
  "status": 401,
  "error": "Invalid API key",
  "code": "INVALID_API_KEY"
}
```

**No Results with Refund (404 - x402 only):**
```json
{
  "status": 404,
  "error": "No information found",
  "data": {
    "message": "The request was processed but no meaningful information was found.",
    "refund": {
      "attempted": true,
      "successful": true,
      "transactionHash": "0x123abc...",
      "reason": "No information found"
    }
  }
}
```

#### **Works cited**

1. aixbt by Virtuals \- AI Agent Store, accessed December 23, 2025, [https://aiagentstore.ai/ai-agent/aixbt-by-virtuals](https://aiagentstore.ai/ai-agent/aixbt-by-virtuals)  
2. What is Virtuals' GAME SDK?. Author: Ben Hack | by Compass Labs, accessed December 23, 2025, [https://medium.com/@compasslabs/what-is-virtuals-game-sdk-ac4dd8a9e7d6](https://medium.com/@compasslabs/what-is-virtuals-game-sdk-ac4dd8a9e7d6)  
3. What Is Virtuals Protocol: The Project Turning Digital Characters into ..., accessed December 23, 2025, [https://coinmarketcap.com/academy/article/what-is-virtuals-protocol-the-project-turning-digital-characters-into-revenue-generating-assets](https://coinmarketcap.com/academy/article/what-is-virtuals-protocol-the-project-turning-digital-characters-into-revenue-generating-assets)  
4. Virtual-Protocol/virtuals-python \- GitHub, accessed December 23, 2025, [https://github.com/Virtual-Protocol/virtuals-python](https://github.com/Virtual-Protocol/virtuals-python)  
5. Agent Logs on Virtuals \- Virtuals Protocol Whitepaper, accessed December 23, 2025, [https://whitepaper.virtuals.io/info-hub/builders-hub/agent-logs-on-virtuals](https://whitepaper.virtuals.io/info-hub/builders-hub/agent-logs-on-virtuals)  
6. Understanding X402: Crypto API Protocol for AI Agent Commerce, accessed December 23, 2025, [https://www.tokenmetrics.com/blog/understanding-x402-the-protocol-powering-ai-agent-commerce?74e29fd5\_page=69](https://www.tokenmetrics.com/blog/understanding-x402-the-protocol-powering-ai-agent-commerce?74e29fd5_page=69)  
7. Inside x402: Is It the Future of Online Payments? \- DWF Labs, accessed December 23, 2025, [https://www.dwf-labs.com/research/inside-x402-how-a-forgotten-http-code-becomes-the-future-of-autonomous-payments](https://www.dwf-labs.com/research/inside-x402-how-a-forgotten-http-code-becomes-the-future-of-autonomous-payments)  
8. x402 Headers Reference | PayStabl AgentPay Documentation, accessed December 23, 2025, [https://agentpay-docs.replit.app/reference/x402\_headers](https://agentpay-docs.replit.app/reference/x402_headers)  
9. x402 \- JT Consulting & Media, accessed December 23, 2025, [https://joetechnologist.com/x402/](https://joetechnologist.com/x402/)  
10. Autonomous API & MCP Server Payments with x402 | Zuplo Blog, accessed December 23, 2025, [https://zuplo.com/blog/mcp-api-payments-with-x402](https://zuplo.com/blog/mcp-api-payments-with-x402)  
11. Aixbt agent upgraded for sharper signals and whale tracking \- MEXC, accessed December 23, 2025, [https://www.mexc.com/en-NG/news/63316](https://www.mexc.com/en-NG/news/63316)  
12. Aixbt agent upgraded for sharper signals and whale tracking \- Bitget, accessed December 23, 2025, [https://www.bitget.com/news/detail/12560604890880](https://www.bitget.com/news/detail/12560604890880)  
13. AIXBT by Virtuals.io \- Quicknode, accessed December 23, 2025, [https://www.quicknode.com/builders-guide/tools/aixbt](https://www.quicknode.com/builders-guide/tools/aixbt)  
14. t54-labs/x402-secure \- GitHub, accessed December 23, 2025, [https://github.com/t54-labs/x402-secure](https://github.com/t54-labs/x402-secure)  
15. game-by-virtuals/game-node \- GitHub, accessed December 23, 2025, [https://github.com/game-by-virtuals/game-node](https://github.com/game-by-virtuals/game-node)  
16. x402scan • x402 Ecosystem Explorer, accessed December 23, 2025, [https://www.x402scan.com/composer/agent/a0bb1ba2-49f4-4604-8deb-3355db2c6f47](https://www.x402scan.com/composer/agent/a0bb1ba2-49f4-4604-8deb-3355db2c6f47)  
17. OpenAI-Compatible Server \- vLLM, accessed December 23, 2025, [https://docs.vllm.ai/en/v0.8.3/serving/openai\_compatible\_server.html](https://docs.vllm.ai/en/v0.8.3/serving/openai_compatible_server.html)  
18. Stream Protocols \- AI SDK UI, accessed December 23, 2025, [https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)  
19. Latest aixbt (AIXBT) Price Analysis \- CoinMarketCap, accessed December 23, 2025, [https://coinmarketcap.com/cmc-ai/aixbt/price-analysis/](https://coinmarketcap.com/cmc-ai/aixbt/price-analysis/)