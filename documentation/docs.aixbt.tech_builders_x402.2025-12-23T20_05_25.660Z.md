[AIXBT Docs](https://docs.aixbt.tech/)

[AIXBT Docs](https://docs.aixbt.tech/)

Search
`⌘`  `K`

Introduction

[What is AIXBT?](https://docs.aixbt.tech/introduction/what-is-aixbt) [Core Concepts](https://docs.aixbt.tech/introduction/core-concepts)

Builders

[Building with AIXBT](https://docs.aixbt.tech/builders/building-with-aixbt) [Quickstart](https://docs.aixbt.tech/builders/quickstart) [REST API](https://docs.aixbt.tech/builders/rest-api) [x402](https://docs.aixbt.tech/builders/x402)

[API Reference](https://docs.aixbt.tech/builders/api)

Terminal

[Access](https://docs.aixbt.tech/terminal/access)

[Projects](https://docs.aixbt.tech/terminal/projects)

[Signals](https://docs.aixbt.tech/terminal/projects/signals) [Momentum Graph](https://docs.aixbt.tech/terminal/projects/momentum-graph)

[Chat](https://docs.aixbt.tech/terminal/chat)

[Prompting Techniques](https://docs.aixbt.tech/terminal/chat/prompting-techniques) [Prompt Examples](https://docs.aixbt.tech/terminal/chat/prompt-examples)

[Automated Tasks](https://docs.aixbt.tech/terminal/automated-tasks) [Socials Integration](https://docs.aixbt.tech/terminal/socials-integration)

Telegram Summaries

[Nuvel](https://docs.aixbt.tech/nuvel/nuvel) [Onboarding](https://docs.aixbt.tech/nuvel/onboarding)

Support

[Get Support](https://docs.aixbt.tech/support/get-support) [FAQ](https://docs.aixbt.tech/support/faq) [LLMs](https://docs.aixbt.tech/support/llms)

Resources

[AIXBT Token](https://docs.aixbt.tech/resources/tokenomics) [Research Group](https://docs.aixbt.tech/resources/research-group) [Links](https://docs.aixbt.tech/resources/links)

Legal

[Terms & Conditions](https://docs.aixbt.tech/legal/terms-and-conditions) [Privacy Policy](https://docs.aixbt.tech/legal/privacy-policy)

x402Available Endpoints

# x402

Copy MarkdownOpen

Pay-per-request access via the x402 protocol

The x402 standard is an open, HTTP-based payment protocol developed by Coinbase. It uses the HTTP 402 status code (Payment Required) to enable instant, on-chain micropayments directly over the web.

No API keys. No registration. No OAuth. Just pay per request with your wallet. See [x402.org](https://www.x402.org/).

## [Available Endpoints](https://docs.aixbt.tech/builders/x402\#available-endpoints)

### [Indigo Chat](https://docs.aixbt.tech/builders/x402\#indigo-chat)

**`POST /v1/agents/indigo`**

Chat with the Indigo AI agent for real-time market insights and narrative analysis.

```
{
  "messages": [\
    {\
      "role": "user",\
      "content": "Which developing narrative has the most potential for growth?"\
    }\
  ]
}
```

This works like a standard LLM completions endpoint. Each request is stateless, so if you want the agent to have context from prior exchanges, include the conversation history in the `messages` array:

```
{
  "messages": [\
    {\
      "role": "user",\
      "content": "Which developing narrative has the most potential for growth?"\
    },\
    {\
      "role": "assistant",\
      "content": "Based on current momentum, ..."\
    },\
    {\
      "role": "user",\
      "content": "What are the main risks with that narrative?"\
    }\
  ]
}
```

### [Surging Projects](https://docs.aixbt.tech/builders/x402\#surging-projects)

**`GET /v1/projects`**

Retrieve the list of projects with surging momentum, updated in real time.

| Parameter | Description |
| --- | --- |
| `limit` | Maximum results (default: 50, max: 50) |
| `name` | Filter by project name (regex) |
| `ticker` | Filter by exact ticker symbol |
| `xHandle` | Filter by X handle |
| `sortBy` | Sort by `score` (default) or `popularityScore` |
| `minScore` | Minimum score threshold |

## [How It Works](https://docs.aixbt.tech/builders/x402\#how-it-works)

1. Make a request to an x402-enabled endpoint
2. Receive a `402 Payment Required` response with payment details
3. Authorize the payment on-chain with your wallet
4. Retry the request with payment proof
5. Receive the data

The x402 helper libraries handle steps 2-4 automatically. You make a single request and get the response—payment happens transparently.

## [Integration](https://docs.aixbt.tech/builders/x402\#integration)

Use the `x402-fetch` or `x402-axios` packages to wrap your HTTP client with automatic payment handling:

```
npm install x402-fetch viem
```

```
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
      messages: [\
        { role: 'user', content: 'What narratives are gaining traction?' },\
      ],
    }),
  },
)
```

For complete examples using both fetch and axios, see the [AIXBT x402 Examples](https://github.com/aixbt/x402) repository.

## [Automatic Refunds](https://docs.aixbt.tech/builders/x402\#automatic-refunds)

If a request fails to return meaningful results, you receive an automatic on-chain refund. This applies to:

- **404 errors** — No information found for your query
- **500 errors** — Server encountered an internal error

The refund response includes a transaction hash you can verify on-chain:

```
{
  status: 404,
  error: "No information found",
  data: {
    message: "The request was processed but no meaningful information was found.",
    refund: {
      attempted: true,
      successful: true,
      transactionHash: "0x...",
      reason: "No information found"
    }
  }
}
```

## [Try It](https://docs.aixbt.tech/builders/x402\#try-it)

Explore available endpoints and test them directly on [x402scan](https://www.x402scan.com/recipient/0x8e4b195c14f20e1ba4c40234f471e1781f293b45/resources).

## [Resources](https://docs.aixbt.tech/builders/x402\#resources)

- [x402 Protocol](https://x402.org/) — Protocol specification
- [AIXBT x402 Examples](https://github.com/aixbt/x402) — Implementation examples
- [x402 Quickstart for Buyers](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers) — Coinbase documentation

[REST API\\
\\
API key authentication and setup](https://docs.aixbt.tech/builders/rest-api) [API Reference\\
\\
REST API endpoints for the AIXBT platform](https://docs.aixbt.tech/builders/api)

### On this page

[Available Endpoints](https://docs.aixbt.tech/builders/x402#available-endpoints) [Indigo Chat](https://docs.aixbt.tech/builders/x402#indigo-chat) [Surging Projects](https://docs.aixbt.tech/builders/x402#surging-projects) [How It Works](https://docs.aixbt.tech/builders/x402#how-it-works) [Integration](https://docs.aixbt.tech/builders/x402#integration) [Automatic Refunds](https://docs.aixbt.tech/builders/x402#automatic-refunds) [Try It](https://docs.aixbt.tech/builders/x402#try-it) [Resources](https://docs.aixbt.tech/builders/x402#resources)