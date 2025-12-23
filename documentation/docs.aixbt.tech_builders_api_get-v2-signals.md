---
url: "https://docs.aixbt.tech/builders/api/get-v2-signals"
title: "List Signals"
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

# List Signals

Copy MarkdownOpen

Returns signals (formerly summaries) with filtering and pagination support.

**Filter Behavior:**

- Project filters (projectIds, names, xHandles, tickers) use AND logic between different filters
- Multiple values within a single filter use OR logic
- Cluster filter returns signals containing ANY of the specified cluster IDs
- Category filter returns signals matching ANY of the specified categories (OR logic)
- Date filters (detectedAfter/detectedBefore) filter by original detection date
- Date filters (reinforcedAfter/reinforcedBefore) filter by last reinforced date
- All date filters can be used independently, together, or combined (AND logic)

https://api.aixbt.tech

GET

``/`v2`/`signals`

Send

Authorization

Query

## [Authorization](https://docs.aixbt.tech/builders/api/get-v2-signals\#authorization)

`ApiKeyAuth`

x-api-key<token>

API key to authorize requests

In: `header`

## [Query Parameters](https://docs.aixbt.tech/builders/api/get-v2-signals\#query-parameters)

projectIds?string

Comma-separated list of project IDs to filter by

names?string

Comma-separated list of project names to filter by (case-insensitive regex match)

xHandles?string

Comma-separated list of X/Twitter handles to filter by

tickers?string

Comma-separated list of token tickers to filter by

clusterIds?string

Comma-separated list of cluster IDs to filter by (OR logic)

categories?string

Comma-separated category names to filter by (OR logic).
Valid values: FINANCIAL\_EVENT, TOKEN\_ECONOMICS, TECH\_EVENT, MARKET\_ACTIVITY, ONCHAIN\_METRICS, PARTNERSHIP, TEAM\_UPDATE, REGULATORY, WHALE\_ACTIVITY, RISK\_ALERT, VISIBILITY\_EVENT, OPINION\_SPECULATION

detectedAfter?string

Filter signals originally detected after this date (ISO datetime)

Format`date-time`

detectedBefore?string

Filter signals originally detected before this date (ISO datetime)

Format`date-time`

reinforcedAfter?string

Filter signals reinforced after this date (ISO datetime)

Format`date-time`

reinforcedBefore?string

Filter signals reinforced before this date (ISO datetime)

Format`date-time`

page?integer

Page number for pagination (1-indexed)

Default`1`

limit?integer

Number of results per page (max 50)

Default`50`

Range`value <= 50`

## [Response Body](https://docs.aixbt.tech/builders/api/get-v2-signals\#response-body)

### 200  `application/json`

### 400

cURL

JavaScript

Python

```
curl -X GET "https://api.aixbt.tech/v2/signals?categories=TECH_EVENT%2CPARTNERSHIP&detectedAfter=2025-01-01T00%3A00%3A00Z&detectedBefore=2025-01-31T23%3A59%3A59Z&reinforcedAfter=2025-01-01T00%3A00%3A00Z&reinforcedBefore=2025-01-31T23%3A59%3A59Z" \
  -H "x-api-key: "
```

200400

```
{
  "status": 200,
  "data": [\
    {\
      "id": "string",\
      "detectedAt": "2019-08-24T14:15:22Z",\
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

[GETGet Project\\
\\
Previous Page](https://docs.aixbt.tech/builders/api/get-v2-projects-id) [GETMomentum History\\
\\
Next Page](https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum)