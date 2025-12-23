---
url: "https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum"
title: "Momentum History"
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

# Momentum History

Copy MarkdownOpen

Returns hourly momentum history with cluster breakdown. Includes tweet counts by cluster and score history for a project over a specified time period. Default period is the last 7 days.

https://api.aixbt.tech

GET

``/`v2`/`projects`/`{id}`/`momentum`

Send

Authorization

Path

Query

## [Authorization](https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum\#authorization)

`ApiKeyAuth`

x-api-key<token>

API key to authorize requests

In: `header`

## [Path Parameters](https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum\#path-parameters)

id\*string

The project ID

## [Query Parameters](https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum\#query-parameters)

start?string

Start timestamp (ISO 8601 format). Defaults to 7 days ago.

Format`date-time`

end?string

End timestamp (ISO 8601 format). Defaults to now.

Format`date-time`

## [Response Body](https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum\#response-body)

### 200  `application/json`

### 400

### 404

### 500

cURL

JavaScript

Python

```
curl -X GET "https://api.aixbt.tech/v2/projects/string/momentum?start=2025-11-21T00%3A00%3A00.000Z&end=2025-11-28T00%3A00%3A00.000Z" \
  -H "x-api-key: "
```

200400404500

```
{
  "status": 200,
  "error": "",
  "data": {
    "projectId": "507f1f77bcf86cd799439011",
    "projectName": "ethereum",
    "data": [\
      {\
        "timestamp": "2025-11-30T12:00:00.000Z",\
        "momentumScore": 0.43,\
        "clusters": [\
          {\
            "id": "67ffa0cdd37b7e33fb723561",\
            "name": "ethereum",\
            "count": 3\
          }\
        ]\
      }\
    ]
  }
}
```

Empty

Empty

Empty

[GETList Signals\\
\\
Previous Page](https://docs.aixbt.tech/builders/api/get-v2-signals) [GETList Clusters\\
\\
Next Page](https://docs.aixbt.tech/builders/api/get-v2-clusters)