---
url: "https://docs.aixbt.tech/builders/api/get-v2-clusters"
title: "List Clusters"
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

# List Clusters

Copy MarkdownOpen

Returns all clusters (tracked communities and information sources) with id, name, and description.
Use cluster IDs with the `clusterIds` parameter on the /signals endpoint to filter signals by source.

https://api.aixbt.tech

GET

``/`v2`/`clusters`

Send

Authorization

## [Authorization](https://docs.aixbt.tech/builders/api/get-v2-clusters\#authorization)

`ApiKeyAuth`

x-api-key<token>

API key to authorize requests

In: `header`

## [Response Body](https://docs.aixbt.tech/builders/api/get-v2-clusters\#response-body)

### 200  `application/json`

### 500

cURL

JavaScript

Python

```
curl -X GET "https://api.aixbt.tech/v2/clusters" \
  -H "x-api-key: "
```

200500

```
{
  "status": 200,
  "data": [\
    {\
      "id": "string",\
      "name": "string",\
      "description": "string"\
    }\
  ]
}
```

Empty

[GETMomentum History\\
\\
Previous Page](https://docs.aixbt.tech/builders/api/get-v2-projects-id-momentum) [GETList Chains\\
\\
Next Page](https://docs.aixbt.tech/builders/api/get-v2-projects-chains)