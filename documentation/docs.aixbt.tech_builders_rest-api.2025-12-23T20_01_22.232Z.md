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

REST APIBase URL

# REST API

Copy MarkdownOpen

API key authentication and setup

Access the AIXBT API using API key authentication. For pay-per-request access without API keys, see [x402](https://docs.aixbt.tech/builders/x402).

## [Base URL](https://docs.aixbt.tech/builders/rest-api\#base-url)

```
https://api.aixbt.tech
```

All endpoints are prefixed with `/v2`.

## [Authentication](https://docs.aixbt.tech/builders/rest-api\#authentication)

Include your API key in the `x-api-key` header with every request:

```
curl -X GET "https://api.aixbt.tech/v2/projects" \
  -H "x-api-key: YOUR_API_KEY"
```

### [Key Types](https://docs.aixbt.tech/builders/rest-api\#key-types)

| Type | Access | How to Get |
| --- | --- | --- |
| Demo Key | Non-agentic endpoints, Bitcoin data only | Sign in and go to [Settings → API Keys](https://aixbt.tech/settings/api-keys) |
| Full-Access Key | Non-agentic endpoints, full dataset | Subscribe to a [Data Plan](https://aixbt.tech/subscribe) |

Both key types use the same authentication method. The difference is the data returned and rate limits. For agentic endpoints (Indigo), use [x402](https://docs.aixbt.tech/builders/x402) pay-per-request, or [get in touch](https://docs.aixbt.tech/support/get-support) to discuss API key access.

## [Rate Limits](https://docs.aixbt.tech/builders/rest-api\#rate-limits)

- **Per minute:** 100 requests
- **Per day:** 100,000 requests

### [Rate Limit Headers](https://docs.aixbt.tech/builders/rest-api\#rate-limit-headers)

Every response includes headers showing your current usage:

```
X-RateLimit-Limit-Minute: 100
X-RateLimit-Remaining-Minute: 99
X-RateLimit-Reset-Minute: 2025-01-15T12:01:00.000Z
X-RateLimit-Limit-Day: 100000
X-RateLimit-Remaining-Day: 99999
X-RateLimit-Reset-Day: 2025-01-16T00:00:00.000Z
```

### [Rate Limit Exceeded](https://docs.aixbt.tech/builders/rest-api\#rate-limit-exceeded)

When you exceed a limit, you'll receive a `429` response:

```
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded (minute). Try again after 2025-01-15T12:01:00.000Z",
  "code": "RATE_LIMIT_EXCEEDED",
  "limitType": "minute"
}
```

The response includes a `Retry-After` header with the number of seconds to wait.

## [Response Format](https://docs.aixbt.tech/builders/rest-api\#response-format)

All endpoints return a consistent JSON structure:

### [Success Response](https://docs.aixbt.tech/builders/rest-api\#success-response)

```
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

The `pagination` object is included for list endpoints.

### [Error Response](https://docs.aixbt.tech/builders/rest-api\#error-response)

```
{
  "status": 400,
  "error": "Invalid request parameters",
  "data": []
}
```

## [HTTP Status Codes](https://docs.aixbt.tech/builders/rest-api\#http-status-codes)

| Status | Code | Meaning |
| --- | --- | --- |
| `200` | - | Success |
| `400` | - | Bad request - check your parameters |
| `401` | `MISSING_API_KEY` | No API key provided |
| `401` | `INVALID_API_KEY` | API key is invalid or inactive |
| `403` | `INVALID_API_KEY_SCOPE` | API key lacks required permissions |
| `404` | - | Resource not found |
| `429` | `RATE_LIMIT_EXCEEDED` | Rate limit exceeded |
| `500` | - | Server error |

## [Pagination](https://docs.aixbt.tech/builders/rest-api\#pagination)

List endpoints support pagination with these query parameters:

| Parameter | Default | Max | Description |
| --- | --- | --- | --- |
| `page` | 1 | - | Page number (1-indexed) |
| `limit` | 50 | 50 | Results per page |

Example:

```
curl "https://api.aixbt.tech/v2/projects?page=2&limit=25" \
  -H "x-api-key: YOUR_API_KEY"
```

## [Filtering](https://docs.aixbt.tech/builders/rest-api\#filtering)

Most list endpoints support filtering. Filters use AND logic between different parameters, and OR logic for multiple values within a parameter.

```
# Projects matching (name=eth OR name=btc) AND chain=base
curl "https://api.aixbt.tech/v2/projects?names=eth,btc&chain=base" \
  -H "x-api-key: YOUR_API_KEY"
```

See the [API Reference](https://docs.aixbt.tech/builders/api) for available filters on each endpoint.

## [Next Steps](https://docs.aixbt.tech/builders/rest-api\#next-steps)

- [Quickstart](https://docs.aixbt.tech/builders/quickstart) \- Make your first request
- [API Reference](https://docs.aixbt.tech/builders/api) \- Complete endpoint documentation
- [x402](https://docs.aixbt.tech/builders/x402) \- Pay-per-request alternative

[Quickstart\\
\\
Make your first API request](https://docs.aixbt.tech/builders/quickstart) [x402\\
\\
Pay-per-request access via the x402 protocol](https://docs.aixbt.tech/builders/x402)

### On this page

[Base URL](https://docs.aixbt.tech/builders/rest-api#base-url) [Authentication](https://docs.aixbt.tech/builders/rest-api#authentication) [Key Types](https://docs.aixbt.tech/builders/rest-api#key-types) [Rate Limits](https://docs.aixbt.tech/builders/rest-api#rate-limits) [Rate Limit Headers](https://docs.aixbt.tech/builders/rest-api#rate-limit-headers) [Rate Limit Exceeded](https://docs.aixbt.tech/builders/rest-api#rate-limit-exceeded) [Response Format](https://docs.aixbt.tech/builders/rest-api#response-format) [Success Response](https://docs.aixbt.tech/builders/rest-api#success-response) [Error Response](https://docs.aixbt.tech/builders/rest-api#error-response) [HTTP Status Codes](https://docs.aixbt.tech/builders/rest-api#http-status-codes) [Pagination](https://docs.aixbt.tech/builders/rest-api#pagination) [Filtering](https://docs.aixbt.tech/builders/rest-api#filtering) [Next Steps](https://docs.aixbt.tech/builders/rest-api#next-steps)