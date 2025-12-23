---
url: "https://docs.aixbt.tech/builders/api/post-v2-agents-indigo"
title: "Chat with Indigo"
---

[AIXBT Docs](https://docs.aixbt.tech/)

[AIXBT Docs](https://docs.aixbt.tech/)

Search
`⌘`  `K`

Introduction

[What is AIXBT?](https://docs.aixbt.tech/introduction/what-is-aixbt) [Core Concepts](https://docs.aixbt.tech/introduction/core-concepts)

Builders

[Building with AIXBT](https://docs.aixbt.tech/builders/building-with-aixbt) [Quickstart](https://docs.aixbt.tech/builders/quickstart) [REST API](https://docs.aixbt.tech/builders/rest-api) [x402](https://docs.aixbt.tech/builders/x402)

[API Reference](https://docs.aixbt.tech/builders/api)

[GETList Projects](https://docs.aixbt.tech/builders/api/get-v2-projects) [GETGet Project](https://docs.aixbt.tech/builders/api/get-v2-projects-id) [GETList Signals](https://docs.aixbt.tech/builders/api/get-v2-signals) [GETMomentum History](https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum) [GETList Clusters](https://docs.aixbt.tech/builders/api/get-v2-clusters) [GETList Chains](https://docs.aixbt.tech/builders/api/get-v2-projects-chains) [POSTChat with Indigo](https://docs.aixbt.tech/builders/api/post-v2-agents-indigo)

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

[API Reference](https://docs.aixbt.tech/builders/api)

# Chat with Indigo

Copy MarkdownOpen

Get a response from the AIXBT Indigo agent. Chat with Indigo for real-time market insights and narrative analysis.

**Capabilities:**

- Exploratory conversation about markets, narratives, and projects
- Structured report generation on demand
- Access to AIXBT's signal and momentum data

**Usage:**
Works like a standard LLM completions endpoint. Each request is stateless—include conversation history in the messages array for multi-turn context. Use `role: "user"` for your prompts and `role: "assistant"` for prior Indigo responses.

https://api.aixbt.tech

POST

``/`v2`/`agents`/`indigo`

Send

Authorization

Body

## [Authorization](https://docs.aixbt.tech/builders/api/post-v2-agents-indigo\#authorization)

`ApiKeyAuth`

x-api-key<token>

API key to authorize requests

In: `header`

## [Request Body](https://docs.aixbt.tech/builders/api/post-v2-agents-indigo\#request-body)

`application/json`

messages?array<object>

## [Response Body](https://docs.aixbt.tech/builders/api/post-v2-agents-indigo\#response-body)

### 200  `application/json`

### 400  `application/json`

### 404  `application/json`

### 500  `application/json`

cURL

JavaScript

Python

```
curl -X POST "https://api.aixbt.tech/v2/agents/indigo" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{}'
```

200400404500

```
{
  "status": 200,
  "error": "",
  "data": {
    "text": "This is a response from the Indigo agent."
  }
}
```

```
{
  "status": 400,
  "error": "Invalid request payload",
  "data": [\
    "string"\
  ]
}
```

```
{
  "status": 404,
  "error": "No information found",
  "data": {
    "message": "The request was processed but no meaningful information was found for your query.",
    "refund": {
      "attempted": true,
      "successful": true,
      "transactionHash": "0x123abc...",
      "reason": "No information found"
    }
  }
}
```

```
{
  "status": 500,
  "error": "Failed to process agent request",
  "data": {
    "message": "An error occurred while processing your request. Please try again later.",
    "refund": {
      "attempted": true,
      "successful": true,
      "transactionHash": "0x123abc...",
      "reason": "Server error"
    }
  }
}
```

[GETList Chains\\
\\
Previous Page](https://docs.aixbt.tech/builders/api/get-v2-projects-chains) [Access\\
\\
AIXBT's analytics interface](https://docs.aixbt.tech/terminal/access)