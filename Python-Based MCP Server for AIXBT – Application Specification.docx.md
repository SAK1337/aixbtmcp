# Python-Based MCP Server for AIXBT – Application Specification

## System Architecture Overview

The **AIXBT MCP server** is a Python application that bridges a local AI assistant (the *MCP Host*, e.g. a GPT-based agent) and the AIXBT market intelligence agent running on the Virtuals Protocol[\[1\]\[2\]](file://file_00000000e18471f7b02f158417076028#:~:text=The%20primary%20objective%20of%20this,chain%20whale%20tracking%20capabilities). AIXBT is not a traditional REST service but a **decentralized AI agent**; it uses the Virtuals Protocol’s **Generative Autonomous Multimodal Entities (G.A.M.E.)** framework for its internal logic, and relies on the **x402** protocol for on-demand payments[\[3\]](file://file_00000000e18471f7b02f158417076028#:~:text=AIXBT%20operates%20not%20merely%20as,applications%20that%20consume%20AIXBT%E2%80%99s%20intelligence)[\[4\]](file://file_00000000e18471f7b02f158417076028#:~:text=interaction%2C%20and%20the%20precise%20definitions,the%20AIXBT%20and%20x402%20integration). The MCP server operates as middleware that handles this complexity, exposing AIXBT’s capabilities through simple HTTP endpoints. It interacts with AIXBT’s public API (via HTTP calls and blockchain signatures) and presents **Resources** (read-only data), **Tools** (functions/actions), and **Prompts** (pre-defined query templates) to the local AI assistant in a standardized way[\[5\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Host%20that%20calls%20the%20Server)[\[6\]](file://file_00000000e18471f7b02f158417076028#:~:text=This%20section%20translates%20the%20API,Claude).

Key components of the architecture include:

* **MCP Host (Client):** The local AI (e.g. LLM in a desktop app or IDE) that will call the MCP server’s interfaces to query AIXBT[\[5\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Host%20that%20calls%20the%20Server).

* **MCP Server (this application):** A FastAPI-based HTTP server running locally. It wraps AIXBT’s APIs, manages payment negotiation (x402), and enforces security and budget rules[\[5\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Host%20that%20calls%20the%20Server). The server will later be containerized (Docker) for easy deployment in various environments.

* **AIXBT Agent (Remote):** The AI agent on Base L2 blockchain that provides market insights (via the Virtuals and x402 protocols). It receives requests and returns data or answers. AIXBT’s “Indigo” engine generates outputs like narrative **signals**, **whale alerts**, and **sentiment scores** based on on-chain data and social feeds[\[7\]](file://file_00000000e18471f7b02f158417076028#:~:text=,11).

The MCP server’s architecture is designed for **local deployment** (running on localhost with FastAPI’s HTTP interface) initially, ensuring easy integration and testing. In the future, the same server can be packaged as a Docker container for cloud or on-premise deployment, with environment variables used for all sensitive configurations (keys, tokens, etc.) to facilitate containerization.

## Authentication and Wallet Setup

Access to AIXBT’s premium data requires a dual authentication approach: **(1) an EVM crypto wallet** for x402 payment handshakes, and **(2) Virtuals Protocol credentials** for agent access (especially for protected logs). Proper generation and security of these credentials is paramount.

* **EVM Wallet (x402 Payments):** The server must have an Ethereum-compatible wallet (private key) to negotiate payments via the x402 protocol[\[8\]](file://file_00000000e18471f7b02f158417076028#:~:text=,risk%20scoring%20before%20signing%20transactions). The developer should **generate an EVM keypair** (for example, via MetaMask or web3.py) and fund the wallet with sufficient **USDC on Base** (for payments) as well as a small amount of ETH on Base for gas fees[\[9\]](file://file_00000000e18471f7b02f158417076028#:~:text=,via%20QuickNode%20or%20Alchemy). The **private key** should be stored securely – e.g. as an environment variable EVM\_PRIVATE\_KEY loaded at runtime – and never hard-coded or exposed in logs[\[8\]](file://file_00000000e18471f7b02f158417076028#:~:text=,risk%20scoring%20before%20signing%20transactions). The server will use this key to sign payment authorization messages (via EIP-712 signing, described later) for each request that requires payment.

* **Virtuals API Key (Terminal Access):** For certain interactions (like retrieving the agent’s internal logs or using the Virtuals “Terminal” API), a JWT bearer token from the Virtuals platform is required[\[10\]](file://file_00000000e18471f7b02f158417076028#:~:text=)[\[11\]](file://file_00000000e18471f7b02f158417076028#:~:text=%2A%20%2A%2AHeader%3A%2A%2A%20X,Authorization%3A%20Bearer%20%5C%3CJWT%5C_TOKEN). The developer should obtain a **Virtuals API key** from the AIXBT agent’s dashboard on the Virtuals Platform (often via a “Configure Agent” interface). Using this API key, the server can obtain a **JWT access token** by calling the Virtuals.io authentication endpoint (e.g. POST https://api.virtuals.io/api/accesses/tokens with the API key)[\[12\]](file://file_00000000e18471f7b02f158417076028#:~:text=1.%20,Authorization%3A%20Bearer%20%5C%3CJWT%5C_TOKEN). For convenience, the API key (as VIRTUALS\_API\_KEY) or the resulting bearer token can be provided via environment variables. The server should retrieve or refresh the token on startup so that authorized endpoints (like agent log streaming) can include Authorization: Bearer \<token\> in their requests[\[12\]](file://file_00000000e18471f7b02f158417076028#:~:text=1.%20,Authorization%3A%20Bearer%20%5C%3CJWT%5C_TOKEN). This JWT should be treated securely, similar to the private key.

* **Configuration and Environment:** In summary, the server’s configuration will include:

* EVM\_PRIVATE\_KEY: The hex-encoded private key for the wallet used in x402 payments.

* VIRTUALS\_API\_KEY: The API key for Virtuals (to be exchanged for a token) or alternatively a VIRTUALS\_ACCESS\_TOKEN if the token is obtained externally.

* BASE\_RPC\_URL: URL of an Ethereum RPC endpoint for the Base network (needed if on-chain transactions or nonce checks are required, e.g. an Alchemy/QuickNode URL)[\[9\]](file://file_00000000e18471f7b02f158417076028#:~:text=,via%20QuickNode%20or%20Alchemy).

* Other settings like AIXBT API base URL (default https://api.aixbt.tech) and desired network (chain ID 8453 for Base mainnet) which are generally constant[\[13\]](file://file_00000000e18471f7b02f158417076028#:~:text=,1735689600).

When deploying, ensure these secrets are loaded into the environment or a secure config. The private key especially should be in a secure store if possible. It is also recommended to run the server on a machine you trust (since it holds a hot wallet). In a Docker container scenario, these values would be passed in as environment variables at container runtime rather than baked into the image.

## MCP Interface Definitions (Resources, Tools, and Prompts)

The MCP server exposes AIXBT’s capabilities through three types of interfaces:

* **Resources:** Read-only data endpoints that the AI assistant can fetch for context (e.g. latest market signals or sentiment metrics).

* **Tools:** Actions or queries that can be executed with parameters, causing the server to retrieve or compute something (e.g. ask the AIXBT agent a question, or get whale transaction alerts).

* **Prompts:** Pre-defined prompt templates that assist the AI assistant in formulating requests for common tasks (these are not API endpoints per se, but reusable query patterns the server can provide or document).

Each interface is derived from AIXBT’s public API endpoints or its G.A.M.E. framework functions. Below is a list of the supported interfaces:

### Resources

* **aixbt://signals/latest** – **Latest Market Signals**: Returns the most recent market intelligence signals generated by AIXBT’s Indigo engine[\[14\]](file://file_00000000e18471f7b02f158417076028#:~:text=This%20endpoint%20retrieves%20the%20high,engine). This includes up to \~10 insights on emerging crypto narratives, large “whale” transactions, and sentiment analysis summaries. Internally, this resource triggers a GET request to AIXBT’s /signals endpoint (which is x402-protected) to fetch the latest signals[\[15\]](file://file_00000000e18471f7b02f158417076028#:~:text=,BTC). The server will handle the payment challenge automatically and return a JSON payload containing an array of signals along with metadata (e.g. a 24h whale volume sum, social mention counts, etc.)[\[16\]](file://file_00000000e18471f7b02f158417076028#:~:text=%7B%20,450%20%7D%20%7D)[\[17\]](file://file_00000000e18471f7b02f158417076028#:~:text=,%7D). By using this resource, the AI assistant can quickly get a snapshot of current market movers and sentiment shifts without crafting a full query.

* **aixbt://token/{symbol}/sentiment** – **Token Sentiment Analysis**: Provides detailed sentiment and on-chain metrics for a specific token. The {symbol} placeholder in the URI is replaced with a token ticker (e.g. BTC, ETH, or VIRTUAL). This resource queries AIXBT for sentiment analysis focused on that token – including sentiment score/trend, notable on-chain volume changes, and any narrative context for the token[\[18\]](file://file_00000000e18471f7b02f158417076028#:~:text=). Implementation-wise, the server might call the same signals endpoint with a query parameter to filter by token symbol[\[19\]](file://file_00000000e18471f7b02f158417076028#:~:text=,BTC%2C%20VIRTUAL), or use a dedicated API if available. The result is returned as JSON, giving the assistant focused insight on that asset.

* **aixbt://agent/logs** – **Real-Time Agent Logs**: Streams or retrieves the internal “thought process” logs of the AIXBT agent. This resource connects to the Virtuals *Terminal API* to fetch the agent’s live reasoning steps and state (for example, the chain of thought from its Planner or Action Executor modules)[\[20\]](file://file_00000000e18471f7b02f158417076028#:~:text=). The server will perform a GET request to the Terminal logs endpoint (e.g. api-terminal.virtuals.io/logs) using the required Bearer token authentication[\[21\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Virtuals%20API%20Key). The response is typically a JSON with the latest log entries or a continuously updated stream. This allows a developer or an AI assistant to peek into *how* AIXBT is reaching its conclusions, which is useful for debugging or detailed analysis. Because this endpoint is sensitive and token-protected, the MCP server must include the Authorization: Bearer \<JWT\> header and will not incur an x402 charge for logs (it uses the Virtuals API key authentication instead)[\[21\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Virtuals%20API%20Key).

### Tools

* **query\_agent** – Ask AIXBT a Question: This tool allows the caller to send a free-form **natural language query** to the AIXBT agent and get a contextual answer[\[22\]](file://file_00000000e18471f7b02f158417076028#:~:text=,). It leverages AIXBT’s G.A.M.E-based reasoning engine to produce a bespoke analysis or narrative. For example, an AI assistant could invoke query\_agent with a question like *“What is the whale activity on token XYZ today?”*; the MCP server will relay this to AIXBT’s chat/completion API and return the agent’s answer. **Input:** A JSON object with at least a "query" string is expected (optionally one can request different detail levels, e.g. {"complexity": "brief|detailed"})[\[23\]](file://file_00000000e18471f7b02f158417076028#:~:text=,brief). The server constructs a request to AIXBT’s chat completion endpoint (POST /api/v1/chat/completions) with the query, handles the payment handshake if required, and returns the textual answer back to the caller[\[24\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Returns%20the%20agent%27s%20textual%20response)[\[25\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C,Payment%22%3A%20payment%5C_header). This effectively gives the AI assistant an interactive “ask an expert” channel into AIXBT’s knowledge.

* **get\_whale\_alerts** – Retrieve Whale Transaction Alerts: This tool returns recent **high-value transaction alerts** from the market, as detected by AIXBT’s monitoring of blockchains. It is essentially a filtered view of transactions that exceed a certain USD value threshold. **Input:** parameters such as "chain" (which blockchain to check – e.g., "base", "ethereum", or others) and "min\_value\_usd" (the minimum transaction size in USD to report, default might be 10,000)[\[26\]\[27\]](file://file_00000000e18471f7b02f158417076028#:~:text=,). The MCP server will likely query AIXBT for whale alerts (AIXBT might have an internal feed or include these in its signals; the server can use the signals endpoint with a “whale” category filter[\[28\]](file://file_00000000e18471f7b02f158417076028#:~:text=,BTC%2C%20VIRTUAL) or a dedicated API if one exists). The result is returned as a list of recent big transactions or addresses accumulating tokens. This tool enables real-time alerting use-cases (e.g., the AI assistant warning a user of unusual large buys or sells).

*(Additional tools could be added as AIXBT’s API expands, but query\_agent and get\_whale\_alerts cover the primary interactive queries – general Q\&A and specific whale monitoring.)*

### Prompts

* **market\_briefing** – Daily Market Briefing Template: A reusable prompt template that guides the AI assistant to produce a comprehensive daily crypto market briefing using AIXBT data. The template might say, for example: *“Using the aixbt://signals/latest resource, summarize the top 3 emerging narratives in the crypto market today. Focus on on-chain evidence and sentiment shifts, and identify any tokens showing 'whale accumulation' signals.”*[\[29\]](file://file_00000000e18471f7b02f158417076028#:~:text=,are%20showing%20%27whale%20accumulation%27%20signals). When the assistant uses this prompt, it will automatically pull the latest signals and craft a summary, ensuring that the output highlights AIXBT’s key insights for the day. This prompt is designed to save time for common tasks by providing a structure to the AI’s response.

* **token\_deep\_dive** – Token Deep-Dive Analysis Template: A prompt template for analyzing a specific token in depth. It might be parameterized with a token symbol. For example: *“Use the query\_agent tool to perform a deep dive analysis on* *{{symbol}}. Ask AIXBT specifically about: 1\. Current holder distribution (whale vs retail), 2\. Recent social sentiment spikes, 3\. Major support/resistance levels based on on-chain volume.”*[\[30\]](file://file_00000000e18471f7b02f158417076028#:~:text=,chain%20volume). This prompt helps an AI assistant break down a complex analysis into a structured query for AIXBT, ensuring that the response covers multiple aspects of the token’s status. It effectively chains the use of query\_agent tool with specific sub-questions that AIXBT is well-suited to answer.

The **MCP server** may provide these prompt templates either as part of its documentation or via an endpoint that lists available prompts. They serve as guidance for end-users or AI systems on how to best utilize the tools and resources for common objectives.

## FastAPI Routing and Middleware Architecture

The server is implemented as a **FastAPI** web application, organizing the above interfaces into HTTP routes. The design emphasizes clarity and security, using FastAPI’s features like dependency injection, Pydantic models for request/response, and middleware hooks for tasks like caching and payment handling. Below is an overview of the routing structure and supporting architecture:

* **Routing Structure:** Routes are grouped logically by interface type:

* **Resource Routes (GET):** e.g. GET /resources/signals for aixbt://signals/latest, GET /resources/token/{symbol}/sentiment for token sentiment, and GET /resources/logs for agent logs. These endpoints typically return JSON data. For instance, GET /resources/signals will internally call AIXBT’s signals API and return the JSON signals array. GET /resources/logs will call the Terminal logs API (requiring the bearer token). Each resource route is read-only and idempotent.

* **Tool Routes (POST):** e.g. POST /tools/query-agent and POST /tools/whale-alerts. These accept JSON bodies matching the input schema for the tool (FastAPI will use Pydantic models to validate input fields like “query” or “chain”). On call, the server executes the action: for query-agent, call the chat completion API; for whale-alerts, fetch whale transactions. The response is typically JSON or text. For consistency, the server might wrap outputs in a JSON with a field for result (or simply return raw JSON/text from AIXBT as appropriate).

* **Prompt Listing (optional):** The server might expose a route like GET /prompts that returns the available prompt templates and their descriptions. This can help clients discover the market\_briefing and token\_deep\_dive patterns. (Prompts themselves are not executed on the server – they are client-side guidance – so this route would just serve static content or be documented.)

* **Dependency Injection and Config:** Using FastAPI’s dependency system, the app will load necessary config and clients at startup. For example, a startup event handler can:

* Initialize a Web3 instance (connecting to Base using BASE\_RPC\_URL if needed) and ensure the PRIVATE\_KEY is loaded.

* Fetch a Virtuals JWT token using the provided VIRTUALS\_API\_KEY (if present) so that it’s ready for use in log requests.

* Create an httpx.AsyncClient (or synchronous client) that will be reused for outbound HTTP calls to AIXBT’s API. Reusing a client improves performance by keeping connections alive.

* These can be provided to route functions via dependencies or via closure scope variables. For instance, a dependency could provide an AixbtClient object that has methods like get\_signals() or post\_chat(prompt) encapsulating the API calls and payment handling.

* **x402 Payment Middleware:** The server implements the x402 handshake logic (detailed in the next section) in a reusable way. Rather than duplicating code in each route, a helper function (or middleware) handles it:

* The helper (say call\_with\_payment(...)) attempts an HTTP call via httpx. If a 402 status is encountered, it will parse the challenge and perform the signing process, then **retry the request with the X-Payment header**[\[31\]](file://file_00000000e18471f7b02f158417076028#:~:text=3.%20,Payment%3A%20type%3Dpaystabl%3B%20signature%3D0x...%3B%20context). This function returns the successful response (or propagates an error if payment fails).

* This logic may be wrapped in a try/except to handle cases like insufficient funds or invalid signatures, returning a clear error message to the caller in such cases (HTTP 402 or 500 with explanation).

* FastAPI **middleware** could also be used to catch any outgoing request returning 402, but since the requests to AIXBT are made within route handlers (not returned by FastAPI itself), it’s more practical to handle it in code. However, the concept is similar to middleware: abstract away the payment negotiation so each endpoint can call AIXBT data in one line.

* The server will include the web3.py library to generate EIP-712 signatures. This requires constructing the typed data (domain, types, message) as specified by x402 and using the loaded private key to sign[\[32\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C%23%20EIP,challenge.get%28%27nonce%27%29)[\[33\]](file://file_00000000e18471f7b02f158417076028#:~:text=signed). The resulting signature is inserted into the X-Payment header on the retried request.

* **Caching Layer:** To improve efficiency and avoid redundant payments, an in-memory caching layer is integrated, particularly for frequently accessed resources. A simple approach uses a dictionary or LRU cache with a timestamp:

* When a resource like /resources/signals is requested, the server will first check if it has a recent cached result (e.g. stored within the last 5 minutes). If yes, it returns that immediately instead of calling AIXBT again. If not, it will fetch fresh data and then cache it.

* The cache duration for signals and similar data is set to a **TTL of 5 minutes** by default[\[34\]](file://file_00000000e18471f7b02f158417076028#:~:text=,calls%20by%20the%20LLM%20Host), as these insights update periodically but not every second. This dramatically reduces token spend if an AI assistant asks for the same context repeatedly in a short span.

* Each cache entry might key off the endpoint and query parameters. For example, token sentiment could be cached per token symbol separately.

* FastAPI could use an in-memory object (which will reset on server restart) or a more persistent cache if needed (file or Redis for long-lived caching, though not required for local use).

* Real-time logs and ad-hoc query results are generally **not cached** (logs because they change continuously; query\_agent because each question is unique). Caching is mainly for static data endpoints.

* **Rate Limiting:** The server may implement basic rate limiting to prevent abuse or runaway costs. For instance, a **per-minute request cap** (e.g. no more than N requests per minute for the signals endpoint) can be enforced. This can be done via an in-memory counter that resets every minute, or using a third-party FastAPI middleware (like slowapi) if needed. The goal is to throttle any loop that might spam paid endpoints. Since this MCP server is typically used by a single client (the local AI), the rate limiting can be global. If the limit is exceeded, the server can return HTTP 429 Too Many Requests.

* **Error Handling and Logging:** The FastAPI app will include error handlers to catch and log exceptions. For example, if the x402 payment process fails (due to network issues or an on-chain rejection), the server should catch that and respond with a clear error (possibly 402 or 500 with a message) rather than crashing. Logging should record important events: when a 402 challenge is received, when a payment signature is sent, how much was paid, etc., as well as any budget limit triggers. This helps in auditing spend and debugging issues.

* **CORS and Security:** If the MCP server is purely local (accessed by a local AI process), CORS may not be an issue. If the server could be accessed from a browser or other remote clients, appropriate CORS headers can be enabled via FastAPI’s middleware to allow trusted origins. Also, since this server holds a hot wallet, it’s recommended to run it in a restricted environment (localhost or behind a firewall) to minimize exposure. In a containerized deployment, ensure that external access is locked down or requires an authentication token to call the MCP endpoints, to prevent unauthorized usage.

In summary, the FastAPI architecture cleanly separates different kinds of interactions (data fetch vs. action execution), and leverages middleware/helper functions to handle cross-cutting concerns like payment negotiation, caching, and rate limiting. This makes the system robust and maintainable, while providing a straightforward HTTP interface.

## x402 Payment Handshake Handling

One of the core responsibilities of the MCP server is to handle the **HTTP 402 Payment Required** handshake mandated by AIXBT’s paid API. The x402 protocol flow is as follows[\[35\]](file://file_00000000e18471f7b02f158417076028#:~:text=2.%20,Authenticate%3A%20x402%20scheme%3D%22exact)[\[31\]](file://file_00000000e18471f7b02f158417076028#:~:text=3.%20,Payment%3A%20type%3Dpaystabl%3B%20signature%3D0x...%3B%20context):

1. **Initial Request:** The server makes an HTTP request to a protected AIXBT endpoint (for example, GET /x402/v1/agents/indigo/signals). This request is sent without any payment info on first attempt.

2. **402 Challenge Response:** The AIXBT server responds with 402 Payment Required instead of the data[\[35\]](file://file_00000000e18471f7b02f158417076028#:~:text=2.%20,Authenticate%3A%20x402%20scheme%3D%22exact). The response includes a **payment challenge** payload (typically in the JSON body) detailing what payment is needed. For example, the JSON may contain fields like:

3. amount: the price in smallest units (e.g. “1000000” wei for 0.000001 USDC, or similar)[\[36\]](file://file_00000000e18471f7b02f158417076028#:~:text=%7B%20,8453%2C%20%2F%2F%20Base%20Mainnet),

4. currency: the token/currency (e.g. “USDC”),

5. token\_address: the contract address of the token to pay (USDC on Base in this case)[\[37\]](file://file_00000000e18471f7b02f158417076028#:~:text=,1735689600),

6. recipient: the wallet address of the AIXBT agent (who will receive the payment)[\[38\]](file://file_00000000e18471f7b02f158417076028#:~:text=USDC%20,1735689600),

7. chain\_id: the blockchain network ID on which payment is to be made (8453 for Base mainnet)[\[39\]](file://file_00000000e18471f7b02f158417076028#:~:text=Wallet%20,1735689600),

8. possibly a nonce or deadline for the payment request[\[13\]](file://file_00000000e18471f7b02f158417076028#:~:text=,1735689600). The HTTP response will also contain a header like WWW-Authenticate: x402 indicating a payment is required. The server might also send an Accept-Payment header listing acceptable currencies or formats (e.g. it might specify it accepts USDC on Base)[\[40\]](file://file_00000000e18471f7b02f158417076028#:~:text=,8).

9. **Payment Preparation (Off-chain Signature):** Upon receiving this challenge, the MCP server prepares a payment authorization using its EVM wallet. Instead of immediately sending an on-chain transaction, x402 often uses an **EIP-712 signed message** to prove intent to pay[\[31\]](file://file_00000000e18471f7b02f158417076028#:~:text=3.%20,Payment%3A%20type%3Dpaystabl%3B%20signature%3D0x...%3B%20context). The server will construct the typed data structure that includes the challenge details (recipient, amount, token, chain, nonce, etc.) as defined by the x402 standard. Using web3.py (specifically the account’s sign\_message or signTypedData functionality), the server signs this data with its private key[\[41\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Standard%20x402%20types). This produces a digital signature (a hex string) that effectively says “I, the owner of wallet X, agree to pay Y amount to Z recipient.”

10. **Authenticated Retry:** The server then resends the original API request, this time adding an X-Payment header carrying the signature (and payment scheme info)[\[31\]](file://file_00000000e18471f7b02f158417076028#:~:text=3.%20,Payment%3A%20type%3Dpaystabl%3B%20signature%3D0x...%3B%20context). For example:  
    X-Payment: type=exact; signature=0xabcdef...  
    Here type=exact might refer to the payment scheme (exact payment of specified amount) as per x402, and the signature is the EIP-712 signature hex string[\[42\]](file://file_00000000e18471f7b02f158417076028#:~:text=%2A%20%2A%2AX,8). In some cases, if an on-chain transaction was used instead, the header might include a receipt=\<tx\_hash\>, but for off-chain signatures this isn’t needed[\[42\]](file://file_00000000e18471f7b02f158417076028#:~:text=%2A%20%2A%2AX,8). The server attaches this header and repeats the same GET/POST request to AIXBT.

11. **Data Response:** If the signature (or payment) is valid, AIXBT responds with the normal 200 OK and the requested data. The previously required payment is now either deducted from the user’s balance or simply recorded as a completed micro-transaction. The response may include metadata confirming the charge, e.g., a field "cost\_incurred": "0.05 USDC" indicating how much was spent for this request[\[43\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C%5D%20%7D%2C%20,%7D).

12. **Error Handling:** If the payment was insufficient, expired, or the signature invalid, the server might again respond with 402 or an error code. The MCP server should then log an error and not infinitely retry. It may propagate a 402 error back to the client indicating payment failed. Additionally, if the wallet lacks funds (detected either by checking balance beforehand or by an on-chain failure), the server should abort the process and return an error indicating insufficient balance.

The MCP server’s implementation of this handshake will use a helper function (as described earlier, e.g., handle\_x402\_payment) to encapsulate steps 2–4. Key points in implementation:

* Use the challenge JSON to fill in an EIP-712 **TypedData** payload (domain might be fixed to x402 spec, message includes recipient/amount/token)[\[32\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C%23%20EIP,challenge.get%28%27nonce%27%29).

* The signing uses the loaded private key and should be done in-memory – the key should never leave the application. The web3.eth.account.sign\_message() or signTypedData() from eth\_account can produce the required signature bytes[\[44\]](file://file_00000000e18471f7b02f158417076028#:~:text=).

* Attach the signature in hex form to the header with the correct format exactly as the API expects (the example uses type=exact which corresponds to the payment scheme negotiated)[\[44\]](file://file_00000000e18471f7b02f158417076028#:~:text=).

* Only after successfully receiving a 2xx response with data will the server forward the data to the original caller. Until then, the call is considered incomplete.

*Security note:* Every payment request is independent, and the signature is only valid for that specific request (often including a nonce or one-time token). This prevents replay of the signature for other data. The server must still be cautious: we implement a **check against excessive costs** before signing (see Budget Enforcement below)[\[45\]](file://file_00000000e18471f7b02f158417076028#:~:text=,prevent%20draining%20funds%20on%20repeated). Also, any library usage (like an x402 client SDK or viem in JavaScript) should be kept up to date, but in Python we handle it directly with web3.py.

In summary, the x402 handshake is seamlessly handled by the MCP server, making it transparent to the AI assistant using the service. The assistant simply calls an endpoint like /resources/signals and the MCP server will either return data (possibly incurring a micro-payment under the hood) or an error if the payment couldn’t be completed. This turns **“agentic commerce”** into a behind-the-scenes process – the software (MCP server) negotiates and pays for data on-demand[\[46\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Agentic%20Commerce), enabling pay-per-request access to AIXBT’s intelligence.

## Budget Enforcement and Cache Design

Because the MCP server controls a wallet with potentially real funds, it must enforce strict budgetary limits and optimize usage to prevent accidental overspending. Two main strategies are used: **cost limits (budgets)** and **caching of results**.

* **Per-Request Spend Limit:** The server config includes a **maximum price per call** (e.g., MAX\_PRICE\_PER\_CALL in USDC or wei). Before signing any x402 payment challenge, the server will inspect the amount in the challenge payload. If the requested amount exceeds the configured cap, the server will refuse to pay and will not sign the message[\[45\]](file://file_00000000e18471f7b02f158417076028#:~:text=,prevent%20draining%20funds%20on%20repeated). In practice, if AIXBT ever demands more than, say, $1.00 for a single request when your cap is $0.50, the server can abort and return an error like *“Cost exceeds maximum allowed per request.”* This protects against unexpected price spikes or misconfiguration. The threshold can be set based on the user’s risk tolerance.

* **Daily/Total Budget Limit:** In addition to per-call limits, a **daily budget** (e.g., MAX\_SPEND\_PER\_DAY) can be enforced[\[47\]](file://file_00000000e18471f7b02f158417076028#:~:text=,risk%20scoring%20before%20signing%20transactions). The server will keep track of the total amount spent (perhaps by summing the amount of each successful payment) over a rolling 24-hour window or calendar day. If the sum would exceed the daily budget, further paid requests are denied until the window resets (or unless manually overridden). This ensures that even if an AI assistant goes into a loop or high-frequency usage, there is an upper bound on how much will be spent in a day. The tracking can be done in memory (which would reset on restart, so for stricter accounting a small persistent log or database could be used). Given the local usage, a simple in-memory counter for daily spend is acceptable, with log entries to audit usage.

* **Rate Limiting:** As discussed in the FastAPI design, rate limiting complements budget limits by controlling call frequency. This prevents scenarios like an LLM calling the signals tool in a tight loop that, even if each call is cheap, could add up quickly. For example, limit to e.g. 5 paid requests per minute. This can be tuned based on typical usage patterns. If a rate limit is hit, the server can respond with 429 or a custom error indicating too many requests, advising the client to slow down.

* **Caching of Results:** Caching is a powerful tool to minimize repeated costs for the same data. The MCP server caches certain resource results for a short time (default \~5 minutes)[\[34\]](file://file_00000000e18471f7b02f158417076028#:~:text=,calls%20by%20the%20LLM%20Host):

* The **signals data** (aixbt://signals/latest) is cached aggressively. If an AI agent requests the latest signals multiple times (which could happen if the user asks similar questions or if multiple prompts use that resource within a few minutes), the server will serve the cached result after the first call. This means the x402 payment is only done once per cache window. The cache entry includes not just the data but also the timestamp and maybe the cost incurred (for logging).

* **Token sentiment** results can also be cached per token symbol. These might be updated continuously by AIXBT, but short-term reuse is likely fine. The server can store the last result for each {symbol} for a few minutes.

* **Tool outputs**: For query\_agent, caching is less straightforward since each query could be unique. By default we do not cache query\_agent responses, as they answer specific questions. However, if the same exact query string is received again in a short span, one could cache that too – this is optional and would need the query as a key.

* **Whale alerts** for a given chain could be cached for a short period as well (whale transactions in a blockchain within the last few minutes will be part of the same result set).

* The cache can be implemented with a simple dictionary of {key: (timestamp, data)}. The key could be the route name plus relevant params (e.g., "signals" or "sentiment:BTC"). A background task or on-demand check will purge entries older than TTL to keep memory usage in check.

* It’s important that caching does not serve stale data beyond the TTL, especially in a fast-moving market context. Five minutes is a reasonable trade-off between freshness and cost-saving, but this can be configurable.

* **Handling of Cost Metadata:** It can be useful for the server to log or even return the cost of each call. For instance, after a successful paid request, the AIXBT API might return a field like "cost\_incurred": "0.05 USDC"[\[43\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C%5D%20%7D%2C%20,%7D). The server could surface this in its response metadata or at least log it. That way, the user knows how much that query cost. This transparency is good for trust. It also allows the server to tally costs for the budget enforcement. If the API doesn’t return the cost explicitly, the server can assume the cost from the challenge (since it signed for X amount).

* **Use of a Secure Payment Library (Optional):** The specification recommends possibly using libraries like x402-secure (if available) for risk scoring or safety checks[\[47\]](file://file_00000000e18471f7b02f158417076028#:~:text=,risk%20scoring%20before%20signing%20transactions). In practice, our implementation uses simple checks as above. But as the ecosystem matures, integrating a specialized library could provide additional safeguards, such as verifying that the payment recipient is indeed the expected agent address (to avoid phishing) and that the token\_address is known (to avoid signing a payment in an unexpected token).

The combined effect of these measures is that the MCP server will only spend what it’s configured to spend, and reuse data when appropriate to maximize value. This prevents the **“wallet draining”** scenario: even though the server holds a hot wallet for convenience, it will not sign away funds beyond the set limits, and it makes efficient use of each paid response by caching it for reuse.

## Instructions for Running and Testing the Server

This section describes how to set up the development environment, run the MCP server, and verify its functionality. The server is intended for developers or advanced users, so familiarity with Python and environment variables is assumed.

### Setup and Installation

1. **Prerequisites:** Ensure you have **Python 3.10+** installed on your system[\[48\]](file://file_00000000e18471f7b02f158417076028#:~:text=,via%20QuickNode%20or%20Alchemy). It’s also recommended to have Node.js v18+ if you plan to compare with any Node-based tools, but it’s not required for the Python server. You will also need internet access to reach AIXBT’s API and the Base blockchain network.

2. **Install Dependencies:** The server uses FastAPI and supporting libraries. Install the required packages via pip. For example, in your project directory:

* pip install fastapi uvicorn\[standard\] httpx web3 mcp-sdk pydantic python-dotenv

* (In practice, an requirements.txt or pyproject.toml will list exact versions. The mcp-sdk is a placeholder name if an MCP Python SDK is available; otherwise the server code will be custom using FastAPI as described.)

3. **Configure Environment Variables:** Before running, set up the necessary environment variables:

4. **EVM\_PRIVATE\_KEY** – The hex string of your EVM wallet private key for x402 payments. *Example:* export EVM\_PRIVATE\_KEY="0xabc123..." (64 hex chars after 0x). Keep this secret. **Do not** commit it to code.

5. **VIRTUALS\_API\_KEY** – Your Virtuals Platform API key for the AIXBT agent’s Terminal API. This is a long alphanumeric string provided by Virtuals. If you already have a JWT token and prefer to use that directly, you could set VIRTUALS\_ACCESS\_TOKEN instead/in addition.

6. **BASE\_RPC\_URL** – A URL to connect to Base blockchain. For instance, export BASE\_RPC\_URL="https://base-mainnet.rpc.thirdweb.com" or an Alchemy endpoint. This is used by web3.py to potentially send transactions or lookup chain ID info if needed. (For off-chain x402 signatures, the RPC is not strictly necessary, but having it can help if on-chain fallback is needed.)

7. **(Optional)** AIXBT\_API\_URL – Base URL for AIXBT API if different from default. Defaults to https://api.aixbt.tech/x402/v1. Similarly, AIXBT\_TERMINAL\_URL for the logs API (default https://api-terminal.virtuals.io).

It’s convenient to put these in a .env file and use python-dotenv to load them, or you can export them in your shell before running.

1. **Obtain Virtuals JWT Token:** The server can fetch a JWT at runtime, but you may also manually get one for initial testing. Using curl or a tool, call:

* curl \-X POST https://api.virtuals.io/api/accesses/tokens \\  
       \-H "X-API-KEY: $VIRTUALS\_API\_KEY"

* This will return a JSON with an "accessToken". You can copy that and set VIRTUALS\_ACCESS\_TOKEN if you want the server to use a static token. Otherwise, ensure VIRTUALS\_API\_KEY is set and the server will perform this step internally on startup.

2. **Wallet Funding:** Make sure the wallet corresponding to EVM\_PRIVATE\_KEY is funded on Base chain. You should have some **USDC** (the amount depends on how many calls you plan to make; each call might cost around a few cents to a few dollars at most, e.g. 0.05 USDC for a signals request[\[17\]](file://file_00000000e18471f7b02f158417076028#:~:text=,%7D)) and also a small amount of **ETH** on Base for gas fees (a few tenths of a dollar worth of ETH is usually sufficient for many meta-transactions)[\[9\]](file://file_00000000e18471f7b02f158417076028#:~:text=,via%20QuickNode%20or%20Alchemy). You can obtain USDC on Base via a bridge or exchange that supports Base Network, and send it to your wallet address. *Skipping this step will result in the server being unable to complete any paid requests\!* It’s also wise to test a micro-transaction with the wallet to confirm it works on Base.

### Running the Server

With configuration in place, you can start the FastAPI server. Typically, you would have a Python file (e.g. main.py) that creates the FastAPI app and includes all routes. To run with Uvicorn (the ASGI server), use:

uvicorn main:app \--reload \--port 8000

This will start the server on http://127.0.0.1:8000 (or adjust host/port as needed). The \--reload flag is useful during development (it auto-restarts on code changes).

On startup, check the console logs: \- The server should log that it loaded configuration (but it will **not** print the private key or API key). \- It may log a message like "Obtained Virtuals access token" if it successfully exchanged the API key for a JWT. \- It might also log the wallet address (public) and the configured budget limits for confirmation.

If the server fails to start due to missing config, ensure all required env vars are set properly.

### Testing the Endpoints

You can test the MCP server endpoints using curl, Postman, or even a browser for GET requests. Here are some tests to verify each major functionality:

* **Get Latest Signals:**  
  Make a GET request to the signals resource, for example:

* curl \-X GET "http://localhost:8000/resources/signals"

* The server should respond with a JSON containing a list of signals. For example, a simplified snippet:

* {  
    "data": {  
      "signals": \[  
        { "narrative": "DeFi Revival", "sentiment": "Bullish", "whale\_tx\_count": 3, ...},  
        { "narrative": "BTC ETF Rumors", "sentiment": "Neutral", "whale\_tx\_count": 0, ...},  
        ...  
      \],  
      "metadata": {  
        "whale\_volume\_24h": 1500000,  
        "social\_mentions\_1h": 450  
      }  
    },  
    "meta": {  
      "count": 10,  
      "cost\_incurred": "0.05 USDC"  
    }  
  }

* The exact fields may vary, but this verifies the server can fetch signals. On the first call, you might notice in the server log that a 402 challenge was handled and a payment was made (cost \~0.05 USDC as shown in meta). If you repeat the request immediately, the server should this time return cached data (and possibly indicate it’s cached by the absence of a new 402 log or by a faster response). The cost\_incurred might still show last cost; it’s up to implementation whether to indicate 0 cost on cached responses or just repeat the last known cost.

* **Token Sentiment:**  
  Try GET /resources/token/ETH/sentiment (replace ETH with any known token symbol). For example:

* curl \-X GET "http://localhost:8000/resources/token/ETH/sentiment"

* The response should be JSON with sentiment analysis for ETH. If the token is not recognized or has no data, the server should handle that gracefully (perhaps returning an empty result or an error message). A valid response might include fields like sentiment score, trend (rising/falling), and key drivers (like mentions or whale actions for that token).

* **Agent Logs:**  
  If you have provided a valid Virtuals token, test GET /resources/logs:

* curl \-X GET "http://localhost:8000/resources/logs"

* The response could be a JSON with the latest log entries from AIXBT’s internal state. This might look like:

* {  
    "logs": \[  
      "\[Planner\] Considering strategy for DeFi narrative...",  
      "\[Perception\] New whale transaction detected: 500k USDC into XYZ token",  
      ...  
    \]  
  }

* The exact content and format depends on AIXBT’s Terminal output. If not much is happening, it might be sparse. This test ensures your Virtuals JWT is working. If this endpoint returns an authorization error, double-check your token.

* **Query Agent Tool:**  
  Test the interactive query via POST /tools/query-agent. For example:

* curl \-X POST "http://localhost:8000/tools/query-agent" \\  
       \-H "Content-Type: application/json" \\  
       \-d '{ "query": "What trends are you seeing in the NFT market today?" }'

* The server will forward this question to AIXBT. This is a paid endpoint (chat completions), so it will likely do a 402 handshake. The response, if successful, will be AIXBT’s answer, for example:

* {  
    "answer": "I am observing increased interest in gaming NFTs. Over the past 24 hours, on-chain metrics show ... (full analysis here)"  
  }

* The text of the answer is generated by AIXBT’s AI. The server simply relays it in a JSON structure (or possibly just raw text). If you set up the server to return the answer as a JSON with a field "answer" or "result", verify it matches that design. This confirms that the query\_agent flow and x402 signing for a chat completion work end-to-end.

* **Whale Alerts Tool:**  
  Test retrieving whale alerts via POST /tools/whale-alerts. For example:

* curl \-X POST "http://localhost:8000/tools/whale-alerts" \\  
       \-H "Content-Type: application/json" \\  
       \-d '{ "chain": "base", "min\_value\_usd": 50000 }'

* The result should be a JSON list of recent transactions on Base network exceeding $50k in value. For instance:

* {  
    "alerts": \[  
      { "tx\_hash": "...", "from": "0xABC...", "to": "0xDEF...", "amount\_usd": 120000, "token": "USDC", "timestamp": "2025-12-23T12:00:00Z" },  
      { "tx\_hash": "...", "from": "0x123...", "to": "0x456...", "amount\_usd": 80000, "token": "DAI", "timestamp": "2025-12-23T11:45:00Z" }  
    \]  
  }

* This confirms that the server can filter and return whale transactions. If AIXBT charges for this (likely part of signals), the server will handle the payment. If no alerts meet the criteria, the server should return an empty list.

During testing, also observe the server’s console output. You should see logs corresponding to each external call: initial 402 responses and successful retries with X-Payment. If an error occurs (like insufficient USDC or a mis-signed request), the server should log the error and return an HTTP error to the client. Debugging those may involve checking the wallet balance, correctness of the private key, or ensuring the chainId is correct in the EIP-712 domain (should be 8453 for Base).

### Docker Containerization Roadmap

While the initial deployment is intended to be local (directly running the FastAPI app), a Docker container can encapsulate the server for ease of deployment. A future update will include a Dockerfile. The containerization plan is as follows:

* **Dockerfile:** Base it on an official Python 3.10 (or higher) image. Copy the server code into the image and install dependencies (possibly using poetry or pip). For example:

* FROM python:3.11-slim  
  WORKDIR /app  
  COPY . /app  
  RUN pip install \-U pip && pip install \-r requirements.txt  
  CMD \["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"\]

* (This is illustrative; the real one will consider security best practices like not running as root, etc.)

* **Configuration in Docker:** The container will not contain the secrets. At runtime, the user must supply the environment variables (EVM\_PRIVATE\_KEY, VIRTUALS\_API\_KEY, etc.) through Docker \-e flags or a mounted config file. This ensures keys are not baked into the image. For instance, run with:

* docker build \-t aixbt-mcp-server .  
  docker run \-p 8000:8000 \-e EVM\_PRIVATE\_KEY=$EVM\_PRIVATE\_KEY \-e VIRTUALS\_API\_KEY=$VIRTUALS\_API\_KEY \-e BASE\_RPC\_URL=$BASE\_RPC\_URL aixbt-mcp-server

* The server should then start inside the container and listen on port 8000 (mapped to host).

* **Verification:** The same tests described above can be performed against the container (e.g. curl http://localhost:8000/resources/signals). The behavior should be identical.

* **Future Enhancements:** Containerization will facilitate deploying the MCP server in cloud environments or as a microservice in a larger architecture. We might add health-check endpoints (for Kubernetes readiness/liveness), and possibly a small web UI for monitoring usage. These are beyond the basic spec, but are part of the roadmap.

## Conclusion

This specification provides a comprehensive blueprint for implementing the Python-based MCP server for AIXBT. In summary, the server will leverage **FastAPI** for a clean HTTP interface, use **httpx and web3.py** under the hood to communicate with AIXBT and sign payments, and expose a rich set of interfaces (resources, tools, prompts) covering AIXBT’s core capabilities: narrative market signals, token sentiment, whale alerts, and direct Q\&A with the agent[\[49\]](file://file_00000000e18471f7b02f158417076028#:~:text=By%20implementing%20the%20query,generation%20of%20intelligent%20financial%20applications).

Critical considerations like the **x402 payment handshake** are handled transparently but securely, with safeguards (budget limits, rate limiting, caching) to prevent misuse of the pay-per-request model[\[45\]](file://file_00000000e18471f7b02f158417076028#:~:text=,prevent%20draining%20funds%20on%20repeated). The **authentication setup** ensures that both the economic layer (crypto wallet) and the Virtuals agent access (API keys) are properly configured by the developer before use. The design also keeps the system **extensible** – as AIXBT or Virtuals introduce new features, the MCP server can add new resources/tools or adjust to changes in the protocol.

By following this specification, developers can implement and run the MCP server to allow any AI assistant (or other client) to tap into AIXBT’s advanced crypto market intelligence in real-time. This unlocks a form of **“agentic commerce”** where AI agents can trade value for insights on the fly[\[46\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Agentic%20Commerce), enabling more autonomous and financially-aware AI applications. The provided instructions and testing steps should help validate the setup and ensure the server operates reliably before integrating it with your AI host system. With future containerization, this server can be deployed broadly, bringing AIXBT’s capabilities to various environments and use-cases while maintaining control over costs and security.

**Sources:** The above design is informed by AIXBT’s integration specs and Virtuals Protocol documentation[\[50\]](file://file_00000000e18471f7b02f158417076028#:~:text=AIXBT%20operates%20not%20merely%20as,applications%20that%20consume%20AIXBT%E2%80%99s%20intelligence)[\[36\]](file://file_00000000e18471f7b02f158417076028#:~:text=%7B%20,8453%2C%20%2F%2F%20Base%20Mainnet), ensuring alignment with the expected API behavior and best practices for secure payment handling. Each component of the specification references those details to provide a developer-ready roadmap for implementation.

---

[\[1\]](file://file_00000000e18471f7b02f158417076028#:~:text=The%20primary%20objective%20of%20this,chain%20whale%20tracking%20capabilities) [\[2\]](file://file_00000000e18471f7b02f158417076028#:~:text=The%20primary%20objective%20of%20this,chain%20whale%20tracking%20capabilities) [\[3\]](file://file_00000000e18471f7b02f158417076028#:~:text=AIXBT%20operates%20not%20merely%20as,applications%20that%20consume%20AIXBT%E2%80%99s%20intelligence) [\[4\]](file://file_00000000e18471f7b02f158417076028#:~:text=interaction%2C%20and%20the%20precise%20definitions,the%20AIXBT%20and%20x402%20integration) [\[5\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Host%20that%20calls%20the%20Server) [\[6\]](file://file_00000000e18471f7b02f158417076028#:~:text=This%20section%20translates%20the%20API,Claude) [\[7\]](file://file_00000000e18471f7b02f158417076028#:~:text=,11) [\[8\]](file://file_00000000e18471f7b02f158417076028#:~:text=,risk%20scoring%20before%20signing%20transactions) [\[9\]](file://file_00000000e18471f7b02f158417076028#:~:text=,via%20QuickNode%20or%20Alchemy) [\[10\]](file://file_00000000e18471f7b02f158417076028#:~:text=) [\[11\]](file://file_00000000e18471f7b02f158417076028#:~:text=%2A%20%2A%2AHeader%3A%2A%2A%20X,Authorization%3A%20Bearer%20%5C%3CJWT%5C_TOKEN) [\[12\]](file://file_00000000e18471f7b02f158417076028#:~:text=1.%20,Authorization%3A%20Bearer%20%5C%3CJWT%5C_TOKEN) [\[13\]](file://file_00000000e18471f7b02f158417076028#:~:text=,1735689600) [\[14\]](file://file_00000000e18471f7b02f158417076028#:~:text=This%20endpoint%20retrieves%20the%20high,engine) [\[15\]](file://file_00000000e18471f7b02f158417076028#:~:text=,BTC) [\[16\]](file://file_00000000e18471f7b02f158417076028#:~:text=%7B%20,450%20%7D%20%7D) [\[17\]](file://file_00000000e18471f7b02f158417076028#:~:text=,%7D) [\[18\]](file://file_00000000e18471f7b02f158417076028#:~:text=) [\[19\]](file://file_00000000e18471f7b02f158417076028#:~:text=,BTC%2C%20VIRTUAL) [\[20\]](file://file_00000000e18471f7b02f158417076028#:~:text=) [\[21\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Virtuals%20API%20Key) [\[22\]](file://file_00000000e18471f7b02f158417076028#:~:text=,) [\[23\]](file://file_00000000e18471f7b02f158417076028#:~:text=,brief) [\[24\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Returns%20the%20agent%27s%20textual%20response) [\[25\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C,Payment%22%3A%20payment%5C_header) [\[26\]](file://file_00000000e18471f7b02f158417076028#:~:text=,) [\[27\]](file://file_00000000e18471f7b02f158417076028#:~:text=,) [\[28\]](file://file_00000000e18471f7b02f158417076028#:~:text=,BTC%2C%20VIRTUAL) [\[29\]](file://file_00000000e18471f7b02f158417076028#:~:text=,are%20showing%20%27whale%20accumulation%27%20signals) [\[30\]](file://file_00000000e18471f7b02f158417076028#:~:text=,chain%20volume) [\[31\]](file://file_00000000e18471f7b02f158417076028#:~:text=3.%20,Payment%3A%20type%3Dpaystabl%3B%20signature%3D0x...%3B%20context) [\[32\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C%23%20EIP,challenge.get%28%27nonce%27%29) [\[33\]](file://file_00000000e18471f7b02f158417076028#:~:text=signed) [\[34\]](file://file_00000000e18471f7b02f158417076028#:~:text=,calls%20by%20the%20LLM%20Host) [\[35\]](file://file_00000000e18471f7b02f158417076028#:~:text=2.%20,Authenticate%3A%20x402%20scheme%3D%22exact) [\[36\]](file://file_00000000e18471f7b02f158417076028#:~:text=%7B%20,8453%2C%20%2F%2F%20Base%20Mainnet) [\[37\]](file://file_00000000e18471f7b02f158417076028#:~:text=,1735689600) [\[38\]](file://file_00000000e18471f7b02f158417076028#:~:text=USDC%20,1735689600) [\[39\]](file://file_00000000e18471f7b02f158417076028#:~:text=Wallet%20,1735689600) [\[40\]](file://file_00000000e18471f7b02f158417076028#:~:text=,8) [\[41\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Standard%20x402%20types) [\[42\]](file://file_00000000e18471f7b02f158417076028#:~:text=%2A%20%2A%2AX,8) [\[43\]](file://file_00000000e18471f7b02f158417076028#:~:text=%5C%5D%20%7D%2C%20,%7D) [\[44\]](file://file_00000000e18471f7b02f158417076028#:~:text=) [\[45\]](file://file_00000000e18471f7b02f158417076028#:~:text=,prevent%20draining%20funds%20on%20repeated) [\[46\]](file://file_00000000e18471f7b02f158417076028#:~:text=,Agentic%20Commerce) [\[47\]](file://file_00000000e18471f7b02f158417076028#:~:text=,risk%20scoring%20before%20signing%20transactions) [\[48\]](file://file_00000000e18471f7b02f158417076028#:~:text=,via%20QuickNode%20or%20Alchemy) [\[49\]](file://file_00000000e18471f7b02f158417076028#:~:text=By%20implementing%20the%20query,generation%20of%20intelligent%20financial%20applications) [\[50\]](file://file_00000000e18471f7b02f158417076028#:~:text=AIXBT%20operates%20not%20merely%20as,applications%20that%20consume%20AIXBT%E2%80%99s%20intelligence) Documenting AIXBT Public API.md

[file://file\_00000000e18471f7b02f158417076028](file://file_00000000e18471f7b02f158417076028)