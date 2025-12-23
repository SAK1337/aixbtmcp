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

Accessing AIXBT's intelligence layer requires navigating a dual-layer authentication stack: the standard Virtuals Protocol authentication for agent interaction and the x402 layer for economic settlement.

### **3.1 x402 Payment Protocol Specification**

The x402 protocol is the primary gatekeeper for AIXBT's premium data services. It facilitates unauthorized, permissionless access contingent on real-time payment.

#### **3.1.1 The x402 Handshake Flow**

The authentication process is not a static API key exchange but a dynamic handshake.

1. **Initial Request:** The client sends a standard HTTP request to a protected endpoint.  
   HTTP  
   GET /api/v1/agents/indigo/signals HTTP/1.1  
   Host: api.aixbt.tech

2. **Payment Challenge (402 Response):** The server denies access with a 402 status and provides payment metadata.8  
   HTTP  
   HTTP/1.1 402 Payment Required  
   Content-Type: application/json  
   WWW-Authenticate: x402 scheme="exact"

   {  
     "error": "Payment Required",  
     "payment": {  
       "amount": "1000000", // units in wei/atomic  
       "currency": "USDC",  
       "token\_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // Base USDC  
       "recipient": "0x4f9fd6be4a90f2620860d680c0d4d5fb53d1a825", // AIXBT Agent Wallet  
       "chain\_id": 8453, // Base Mainnet  
       "deadline": 1735689600  
     }  
   }

3. **Payment Execution/Signing:** The MCP server must sign a transaction or an EIP-712 typed message authorizing the transfer of the specified funds.  
4. **Authenticated Retry:** The client resends the request with the X-Payment header containing the signature or transaction hash.8  
   HTTP  
   GET /api/v1/agents/indigo/signals HTTP/1.1  
   Host: api.aixbt.tech  
   X-Payment: type=paystabl; signature=0x...; context=...

#### **3.1.2 Header Specifications**

* **X-Payment**: The primary header carrying the proof of payment.  
  * Format: type=\<scheme\> signature=\<hex\_string\> \[receipt=\<tx\_hash\>\]  
* **Accept-Payment**: Sent by the server to indicate supported currencies (e.g., USDC on Base, ETH on Mainnet).8

#### **3.1.3 Security Considerations for MCP**

* **Wallet Management:** The MCP server must manage a hot wallet containing stablecoins (USDC) and ETH for gas (if on-chain settlement is required). The private key must be stored securely (e.g., environment variables, encrypted vaults).  
* **Spending Limits:** To prevent wallet draining, the MCP implementation should include strict spending limits per request and per day.  
* **Risk Assessment:** Implementing libraries like x402-secure 14 can provide liability protection and risk scoring before signing transactions.

### **3.2 Virtuals Protocol Authentication**

For interactions that do not require payment (e.g., checking agent status or public logs), or for interactions within the Virtuals ecosystem (e.g., the Terminal API), a standard API key or JWT mechanism is used.

#### **3.2.1 Terminal API Access**

To access the real-time thought logs of the AIXBT agent (useful for debugging or deep context), the Terminal API requires an access token.5

1. **Generate API Key:** Obtained via the Virtuals Platform dashboard ("Configure Agent").  
2. **Exchange for Bearer Token:**  
   * **Endpoint:** POST https://api.virtuals.io/api/accesses/tokens  
   * **Header:** X-API-KEY: \<YOUR\_TERMINAL\_API\_KEY\>  
   * **Response:** { "data": { "accessToken": "\<JWT\_TOKEN\>" } }  
3. **Authenticated Requests:**  
   * **Header:** Authorization: Bearer \<JWT\_TOKEN\>

### **3.3 Hybrid Security Model for MCP**

The MCP application specification will utilize a hybrid model:

* **Read-Only/Public Data:** Accessed via standard HTTP with Virtuals Protocol Bearer tokens.  
* **Premium/Alpha Data:** Accessed via x402 payment headers.  
* **MCP Server Configuration:** The MCP Server configuration must accept configuration parameters for both: VIRTUALS\_API\_KEY and EVM\_PRIVATE\_KEY.

## **4\. API Endpoint Documentation**

Since explicit public documentation for api.aixbt.tech is gated, this section reconstructs the API schema based on the Virtuals Protocol G.A.M.E. SDK specifications 2 and the functional description of the AIXBT agent.13

### **4.1 Base URL**

* **Primary:** https://api.aixbt.tech 16  
* **Virtuals Protocol Gateway:** https://api.virtuals.io  
* **Terminal Logs:** http://api-terminal.virtuals.io

### **4.2 Resource: Agent Intelligence (/signals)**

This endpoint retrieves the high-level market insights generated by the "Indigo" engine.

* **Endpoint:** GET /x402/v1/agents/indigo/signals (Inferred from 16)  
* **Description:** Fetches the latest narrative detection signals, sentiment analysis, and whale alerts.  
* **Authentication:** x402 (Payment Required).  
* **Query Parameters:**  
  * limit (int, optional): Number of signals to retrieve. Default: 10\.  
  * category (string, optional): Filter by narrative, whale, sentiment.  
  * token (string, optional): Filter by specific token symbol (e.g., BTC, VIRTUAL).

#### **Response Schema (JSON)**

JSON

{  
  "data": {  
    "signals":,  
        "metadata": {  
          "whale\_volume\_24h": 1500000,  
          "social\_mentions\_1h": 450  
        }  
      }  
    \]  
  },  
  "meta": {  
    "count": 1,  
    "cost\_incurred": "0.05 USDC"  
  }  
}

### **4.3 Resource: Agent Interaction (/chat)**

This endpoint allows direct interaction with the AIXBT agent, leveraging the G.A.M.E. framework's conversational capabilities.

* **Endpoint:** POST /api/v1/chat/completions (OpenAI-compatible format supported by vLLM/Virtuals runners 17).  
* **Description:** Send a prompt to the agent to perform specific analysis or answer questions.  
* **Authentication:** x402 or Bearer Token.

#### **Request Schema**

JSON

{  
  "model": "aixbt-indigo",  
  "messages":,  
  "temperature": 0.7,  
  "max\_tokens": 500  
}

#### **Response Schema**

JSON

{  
  "id": "chatcmpl-123",  
  "object": "chat.completion",  
  "created": 1677652288,  
  "choices":,  
  "usage": {  
    "prompt\_tokens": 15,  
    "completion\_tokens": 45,  
    "total\_tokens": 60  
  }  
}

### **4.4 Resource: Agent State (/logs)**

This endpoint connects to the "Terminal" view, streaming the agent's internal reasoning steps.

* **Endpoint:** GET /logs (via api-terminal.virtuals.io 5).  
* **Description:** Retrieve the internal "thoughts" or execution logs of the agent's workers (Planner, Action Executor).  
* **Authentication:** Bearer Token (Virtuals API Key).

#### **Response Schema**

JSON

{  
  "logs":  
}

## **5\. MCP Application Specification**

This section translates the API documentation above into a formal specification for a Model Context Protocol (MCP) server. This server will expose AIXBT's capabilities as **Resources** (data), **Tools** (functions), and **Prompts** (templates) to an MCP Host (e.g., Claude).

### **5.1 Server Configuration**

* **Server Name:** mcp-aixbt-server  
* **Version:** 1.0.0  
* **Transport:** Stdio (Standard Input/Output)  
* **Dependencies:** mcp, x402-client, viem (for signing), axios.

### **5.2 MCP Resources**

Resources in MCP represent read-only data that the LLM can access as context.

#### **5.2.1 aixbt://signals/latest**

* **URI:** aixbt://signals/latest  
* **Name:** "Latest AIXBT Market Signals"  
* **MIME Type:** application/json  
* **Description:** Returns the most recent 10 market intelligence signals generated by the AIXBT Indigo agent, including narrative shifts and whale alerts.  
* **Implementation Logic:**  
  1. The server initiates a GET request to the AIXBT signals endpoint.  
  2. If a 402 is received, the server automatically handles the x402 payment flow using the configured wallet.  
  3. The JSON response is returned as the resource content.

#### **5.2.2 aixbt://token/{symbol}/sentiment**

* **URI Template:** aixbt://token/{symbol}/sentiment  
* **Name:** "Token Sentiment Analysis"  
* **MIME Type:** application/json  
* **Description:** Provides detailed sentiment analysis and on-chain metrics for a specific token symbol (e.g., aixbt://token/VIRTUAL/sentiment).  
* **Implementation Logic:**  
  1. Parses the {symbol} from the URI.  
  2. Queries AIXBT with a filter for that token.  
  3. Returns structured sentiment data (Score, Trend, Keyword Clusters).

### **5.3 MCP Tools**

Tools in MCP are executable functions that the LLM can call to perform actions or queries with dynamic arguments.

#### **5.3.1 query\_agent**

* **Name:** query\_agent  
* **Description:** Allows the user to ask a specific natural language question to the AIXBT agent. This uses the agent's G.A.M.E. framework to reason and generate a bespoke answer.  
* **Input Schema (JSON Schema):**  
  JSON  
  {  
    "type": "object",  
    "properties": {  
      "query": {  
        "type": "string",  
        "description": "The market question or analysis request for the agent (e.g., 'What is the whale behavior on AERO token today?')"  
      },  
      "complexity": {  
        "type": "string",  
        "enum": \["brief", "detailed"\],  
        "default": "brief",  
        "description": "The depth of analysis required."  
      }  
    },  
    "required": \["query"\]  
  }

* **Implementation Logic:**  
  1. Constructs a payload for the /chat/completions endpoint.  
  2. Handles potential x402 payment negotiation.  
  3. Returns the agent's textual response.

#### **5.3.2 get\_whale\_alerts**

* **Name:** get\_whale\_alerts  
* **Description:** Fetches recent high-value transaction alerts for a specific chain or token.  
* **Input Schema:**  
  JSON  
  {  
    "type": "object",  
    "properties": {  
      "chain": {  
        "type": "string",  
        "enum": \["base", "solana", "ethereum"\],  
        "default": "base",  
        "description": "The blockchain network to check."  
      },  
      "min\_value\_usd": {  
        "type": "integer",  
        "default": 10000,  
        "description": "Minimum transaction value in USD to filter."  
      }  
    }  
  }

### **5.4 MCP Prompts**

Prompts are reusable templates that help users interact with the server effectively.

#### **5.4.1 market\_briefing**

* **Name:** market\_briefing  
* **Description:** Generates a comprehensive daily crypto market briefing using AIXBT's data.  
* **Template:**"Using the aixbt://signals/latest resource, summarize the top 3 emerging narratives in the crypto market today. Focus on on-chain evidence and sentiment shifts. Identify any tokens that are showing 'whale accumulation' signals."

#### **5.4.2 token\_deep\_dive**

* **Name:** token\_deep\_dive  
* **Arguments:**  
  * symbol: The token to analyze.  
* **Template:**"Use the query\_agent tool to perform a deep dive analysis on {{symbol}}. Ask AIXBT specifically about: 1\. Current holder distribution (Whale vs Retail). 2\. Recent social sentiment spikes. 3\. Major support/resistance levels based on on-chain volume."

## **6\. Implementation Guide**

This section provides the technical roadmap for building the mcp-aixbt-server.

### **6.1 Prerequisites**

* **Node.js v18+** or **Python 3.10+**.  
* **EVM Wallet Private Key:** Required for x402 signing. This wallet must be funded with USDC (on Base) and ETH (for gas, though x402 often uses meta-transactions or off-chain signatures, having gas is a safety net).  
* **RPC Endpoint:** Connection to Base mainnet (e.g., via QuickNode or Alchemy).

### **6.2 Python Implementation Architecture**

Using the mcp Python SDK and web3.py.

Python

\# pseudo-code structure for mcp-aixbt-server

import asyncio  
from mcp.server import Server, NotificationOptions  
from mcp.server.stdio import stdio\_server  
import httpx  
from web3 import Web3  
from eth\_account.messages import encode\_typed\_data

\# Configuration  
AIXBT\_API\_URL \= "https://api.aixbt.tech/x402/v1"  
PRIVATE\_KEY \= "os.environ.get('EVM\_PRIVATE\_KEY')"  
WALLET\_ADDRESS \= "0x..."

app \= Server("aixbt-mcp")

async def handle\_x402\_payment(client, initial\_response):  
    """  
    Handles the 402 Payment Required handshake.  
    1\. Parses the WWW-Authenticate header / response body.  
    2\. Constructs the EIP-712 payment message.  
    3\. Signs the message with the private key.  
    4\. Returns the X-Payment header string.  
    """  
    challenge \= initial\_response.json()\['payment'\]  
      
    \# EIP-712 Signing Logic (Simplified)  
    msg\_data \= {  
        "domain": {"name": "x402", "version": "1", "chainId": challenge\['chain\_id'\]},  
        "message": {  
            "recipient": challenge\['recipient'\],  
            "amount": challenge\['amount'\],  
            "token": challenge\['token\_address'\],  
            "nonce": challenge.get('nonce')  
        },  
        "primaryType": "Payment",  
        "types": {... } \# Standard x402 types  
    }  
      
    signed\_msg \= Web3().eth.account.sign\_typed\_data(PRIVATE\_KEY, full\_message=msg\_data)  
      
    return f"type=exact; signature={signed\_msg.signature.hex()}"

@app.call\_tool()  
async def query\_agent(name: str, arguments: dict) \-\> list:  
    if name\!= "query\_agent":  
        raise ValueError(f"Unknown tool: {name}")

    query \= arguments.get("query")  
      
    async with httpx.AsyncClient() as client:  
        \# Initial Request  
        response \= await client.post(  
            f"{AIXBT\_API\_URL}/chat/completions",  
            json={"messages": \[{"role": "user", "content": query}\]}  
        )  
          
        \# Payment Handling  
        if response.status\_code \== 402:  
            payment\_header \= await handle\_x402\_payment(client, response)  
            \# Retry with payment  
            response \= await client.post(  
                f"{AIXBT\_API\_URL}/chat/completions",  
                json={"messages": \[{"role": "user", "content": query}\]},  
                headers={"X-Payment": payment\_header}  
            )  
              
        return \[{"type": "text", "text": response.json()\['choices'\]\['message'\]\['content'\]}\]

async def main():  
    async with stdio\_server() as (read\_stream, write\_stream):  
        await app.run(read\_stream, write\_stream, app.create\_initialization\_options())

if \_\_name\_\_ \== "\_\_main\_\_":  
    asyncio.run(main())

### **6.3 Handling Rate Limits and Costs**

Given the pay-per-request nature of AIXBT via x402:

* **Cost Control:** The MCP server should implement a strict budget. Before signing any x402 challenge, it should verify challenge\['amount'\] \<= MAX\_PRICE\_PER\_CALL.  
* **Caching:** Resources like aixbt://signals/latest should be cached in memory for a short duration (e.g., 5 minutes) to prevent draining funds on repeated calls by the LLM Host.

## **7\. Strategic Implications and Future Outlook**

The integration of AIXBT into the MCP ecosystem represents a paradigmatic shift in how AI models consume information.

### **7.1 From Data Retrieval to Agentic Commerce**

Traditional APIs are passive; they wait for a subscription-validated request. The AIXBT x402 integration demonstrates **agentic commerce**, where the software (the MCP server) actively negotiates a price and pays for data autonomously. This allows for a "just-in-time" economic model where users pay only for the high-value insights they typically need, rather than a flat monthly subscription.

### **7.2 The Recursive Intelligence Loop**

By exposing AIXBT as an MCP server, developers enable **recursive intelligence**. A Host LLM (like Claude) can query AIXBT for a market anomaly, receive a "whale alert," and then autonomously use that alert to trigger a secondary tool (e.g., a portfolio rebalancing tool). The AIXBT agent becomes a specialized "sub-processor" for the generalist LLM.

### **7.3 Scalability via Base L2**

The choice of the Base blockchain for AIXBT 19 is strategic. The low transaction fees of the Optimism stack allow for the high-frequency micro-transactions required by x402 without making the cost of "asking a question" prohibitive. This scalability ensures that the MCP server remains responsive and cost-effective.

## **8\. Conclusion**

The AIXBT public API, while not documented in a traditional Swagger file, is accessible through the synthesis of the Virtuals Protocol SDK and the x402 payment standard. This report has defined the necessary specifications to build an MCP server that bridges this gap.

By implementing the query\_agent and get\_signals tools defined in Section 5, and wrapping them in the authentication logic detailed in Section 3, developers can create a powerful interface. This interface unlocks the "Indigo" intelligence layer—narrative detection, whale tracking, and sentiment analysis—transforming AIXBT from a standalone chatbot into a composable building block for the next generation of intelligent financial applications.

The key to successful integration lies in the robust handling of the x402 402 Payment Required handshake, ensuring that the autonomous economic negotiation is secure, budget-constrained, and transparent to the end-user.

# **Appendix A: API Request/Response Examples**

### **A.1 Signals Endpoint (x402 Protected)**

**Request:**

HTTP

GET /x402/v1/agents/indigo/signals?limit=5 HTTP/1.1  
Host: api.aixbt.tech  
Accept: application/json

**Response (402 Payment Required):**

JSON

{  
  "error": "Payment Required",  
  "payment": {  
    "amount": "50000",  
    "currency": "USDC",  
    "token\_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  
    "recipient": "0x4f9fd6be4a90f2620860d680c0d4d5fb53d1a825",  
    "chain\_id": 8453  
  }  
}

**Retry Request (with Signature):**

HTTP

GET /x402/v1/agents/indigo/signals?limit=5 HTTP/1.1  
Host: api.aixbt.tech  
X-Payment: type=exact; signature=0x92f...

**Final Response (200 OK):**

JSON

{  
  "signals":  
}

### **A.2 Terminal Logs (Token Protected)**

**Request:**

HTTP

GET /logs?framework\_name=game\&category\_name=planner\_module HTTP/1.1  
Host: api-terminal.virtuals.io  
Authorization: Bearer \<JWT\_TOKEN\>

**Response:**

JSON

{  
  "data":  
}

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