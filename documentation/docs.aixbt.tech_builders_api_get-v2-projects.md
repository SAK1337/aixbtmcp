---
url: "https://docs.aixbt.tech/builders/api/get-v2-projects"
title: "List Projects"
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

# List Projects

Copy MarkdownOpen

Returns a paginated list of projects with signals, coingeckoData, and popularityScore.

**Filter Behavior:**

- Multi-value filters (projectIds, names, xHandles, tickers) use OR logic within the same filter
- Different filters use AND logic between them
- Example: `names=eth,btc&tickers=SOL` returns projects matching (name=eth OR name=btc) AND ticker=SOL

https://api.aixbt.tech

GET

``/`v2`/`projects`

Send

Authorization

Query

## [Authorization](https://docs.aixbt.tech/builders/api/get-v2-projects\#authorization)

`ApiKeyAuth`

x-api-key<token>

API key to authorize requests

In: `header`

## [Query Parameters](https://docs.aixbt.tech/builders/api/get-v2-projects\#query-parameters)

page?integer

Page number (1-indexed)

Default`1`

limit?integer

Number of projects per page (max 50)

Default`50`

Range`value <= 50`

projectIds?string

Comma-separated list of project ObjectIds to filter by

names?string

Comma-separated list of project names to filter by (case-insensitive regex)

xHandles?string

Comma-separated list of X/Twitter handles to filter by

tickers?string

Comma-separated list of token tickers to filter by

chain?string

Filter by blockchain platform. See /projects/chains for values.

minMomentumScore?number

Minimum momentum score threshold

sortBy?string

Field to sort results by

Default`"momentumScore"`

Value in`"momentumScore" | "popularityScore"`

excludeStables?boolean

Exclude stablecoin projects

Default`false`

## [Response Body](https://docs.aixbt.tech/builders/api/get-v2-projects\#response-body)

### 200  `application/json`

### 400

cURL

JavaScript

Python

```
curl -X GET "https://api.aixbt.tech/v2/projects" \
  -H "x-api-key: "
```

200400

```
{
  "status": 200,
  "data": [\
    {\
      "id": "string",\
      "name": "string",\
      "description": "string",\
      "rationale": "string",\
      "xHandle": "string",\
      "momentumScore": 0,\
      "popularityScore": 0,\
      "coingeckoData": {\
        "apiId": "string",\
        "type": "coin",\
        "symbol": "string",\
        "slug": "string",\
        "description": "string",\
        "homepage": "string",\
        "contractAddress": "string",\
        "categories": [\
          "string"\
        ]\
      },\
      "tokens": {\
        "property1": "string",\
        "property2": "string"\
      },\
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
      ]\
    }\
  ],
  "pagination": {
    "page": 0,
    "limit": 0,
    "totalCount": 0,
    "hasMore": true
  }
}
```

Empty

[API Reference\\
\\
REST API endpoints for the AIXBT platform](https://docs.aixbt.tech/builders/api) [GETGet Project\\
\\
Next Page](https://docs.aixbt.tech/builders/api/get-v2-projects-id)