---
url: "https://docs.aixbt.tech/builders/api/get-v2-projects-id"
title: "Get Project"
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

# Get Project

Copy MarkdownOpen

Returns a project by ID, including the 10 most recent signals, full coingeckoData, and popularityScore.

https://api.aixbt.tech

GET

``/`v2`/`projects`/`{id}`

Send

Authorization

Path

## [Authorization](https://docs.aixbt.tech/builders/api/get-v2-projects-id\#authorization)

`ApiKeyAuth`

x-api-key<token>

API key to authorize requests

In: `header`

## [Path Parameters](https://docs.aixbt.tech/builders/api/get-v2-projects-id\#path-parameters)

id\*string

MongoDB ObjectId of the project

## [Response Body](https://docs.aixbt.tech/builders/api/get-v2-projects-id\#response-body)

### 200  `application/json`

### 400

### 404

cURL

JavaScript

Python

```
curl -X GET "https://api.aixbt.tech/v2/projects/string" \
  -H "x-api-key: "
```

200400404

```
{
  "status": 200,
  "error": "",
  "data": {
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
      "categories": [\
        "string"\
      ]
    },
    "tokens": {
      "property1": "string",
      "property2": "string"
    },
    "signals": [\
      {\
        "id": "string",\
        "date": "2019-08-24T14:15:22Z",\
        "reinforcedAt": "2019-08-24T14:15:22Z",\
        "description": "string",\
        "projectName": "string",\
        "projectId": "string",\
        "category": "string",\
        "officialSources": [\
          "string"\
        ],\
        "clusters": [\
          {\
            "id": "string",\
            "name": "string"\
          }\
        ]\
      }\
    ]
  }
}
```

Empty

Empty

[GETList Projects\\
\\
Previous Page](https://docs.aixbt.tech/builders/api/get-v2-projects) [GETList Signals\\
\\
Next Page](https://docs.aixbt.tech/builders/api/get-v2-signals)