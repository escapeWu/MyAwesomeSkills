---
name: news-fetcher-api
description: Use when working with the news fetcher REST API at <news-fetcher-host> for supported-site lookup, domain article discovery, URL fetching, batch fetch/crawl workflows, fetch history queries, and Bearer-authenticated integration examples.
license: Complete terms in LICENSE.txt
---

# News Fetcher API

## Overview

Use this skill for the concrete news fetcher project exposed at `https://<news-fetcher-host>`. The service is a REST API for listing supported publishers, discovering recent URLs for a domain, fetching article/homepage content into markdown, running batch fetch/crawl jobs, and querying fetch history.

Default base URL:

```bash
export NEWS_FETCHER_BASE_URL="https://<news-fetcher-host>"
export NEWS_FETCHER_TOKEN="<token>"
```

Authentication is HTTP Bearer auth:

```bash
-H "Authorization: Bearer $NEWS_FETCHER_TOKEN"
```

Do not use `x-api-key`; live verification showed `x-api-key`, `X-API-Key`, and naked `Authorization: <token>` return 401. Never print or paste the full token into chat/log summaries; redact as `<prefix>****`.

## When to Use

Use this skill when the user asks to:

- check whether a news domain is supported by the fetcher;
- discover recent article/topic URLs for a publisher domain such as `economist.com`;
- fetch a known article or homepage URL into the service output format;
- batch-fetch multiple URLs or crawl from a seed/domain;
- inspect fetch history for a domain before deciding whether to refetch;
- integrate the news fetcher API into scripts, scheduled jobs, or agent workflows;
- troubleshoot fetch-related 401/404/422 responses.

## API Usage Scenarios

Map news-fetch intent to the smallest endpoint that answers it:

| User intent | Endpoint / method | Notes |
|---|---|---|
| Check whether a publisher/domain is supported | Bearer `GET /v1/sites?limit=N` | Returns `total`, `shown`, `sites[]` with domain/name/bypass strategy. Use before planning a domain workflow. |
| Discover recent links for a domain | Bearer `GET /v1/discover/{domain}?since=7d&limit=N` | Best first step for “查某个站最近文章”. Returns candidate article/topic URLs. |
| Fetch a known article/homepage URL | Bearer `POST /v1/fetch` with `{"url":"..."}` | Returns title, output markdown path, image count, text length, strategy, and normalized domain. |
| Search for candidate URLs | Bearer `GET /v1/search?query=...&site=...&limit=N` | Optional path when server-side search is configured. If it reports missing `BRAVE_API_KEY`, use `/v1/discover/{domain}` or provide known URLs. |
| Query previous fetches | Bearer `GET /v1/history?domain=...&limit=N` | Use to avoid unnecessary refetching and to confirm what was already saved. |
| Filter candidate URLs before fetch | Bearer `POST /v1/filter-urls` | Use when a crawler/search source produced noisy URLs and you need fetchable news URLs only. Check schema before sending the body. |
| Fetch many known URLs | Bearer `POST /v1/batch-fetch` | Use for curated URL lists. Check schema before sending the body. |
| Crawl from a site/seed | Bearer `POST /v1/crawl` | Use for broader collection workflows. Check schema before sending the body. |

Typical news-fetch workflows:

- **Discover then fetch a domain**: `/v1/sites` to confirm support → `/v1/discover/{domain}` for candidate URLs → `/v1/fetch` for selected URLs → `/v1/history` to confirm saved records.
- **Known URL extraction**: skip discovery and call `/v1/fetch` directly with the article/homepage URL.
- **Batch ingestion**: collect URLs externally → `/v1/filter-urls` to remove unsupported/noisy URLs → `/v1/batch-fetch` to fetch the accepted list.
- **Refresh existing coverage**: `/v1/history?domain=...` to see what exists → `/v1/discover/{domain}?since=...` to find new candidates → fetch only missing URLs.
- **Search-assisted discovery**: `/v1/search` when search backend is configured → `/v1/fetch` selected results; otherwise fall back to `/v1/discover/{domain}`.

## Calling Modes

The news-fetch API can be called in three practical ways:

| Mode | Best for | Example |
|---|---|---|
| Raw curl | One-off fetches, reproducing fetch bugs, simple cron/CI jobs | Commands in “Common Commands”. |
| Bundled Python helper | Repeated agent/operator usage without rewriting curl | `scripts/news_fetcher_client.py discover economist.com --limit 2`. |
| Programmatic HTTP client | Product integration or scheduled jobs | Standard HTTP client with Bearer auth and JSON bodies. |

## Monitoring Patterns

For investment monitoring, use the fetcher as the collection layer and keep local state outside the API:

| Monitoring level | Flow | Use when |
|---|---|---|
| URL watch | For each watchlist domain, call `/v1/discover/{domain}?since=1d&limit=N`, diff returned URLs against a local `seen_urls.json`, alert only new URLs. | Fast headline/link monitoring. |
| Fetch watch | URL watch → call `/v1/fetch` for new URLs → store returned `path`, `title`, `text_length`, and domain. | Need readable article text for later summarization. |
| Batch ingestion | Accumulate new URLs across domains → `/v1/filter-urls` → `/v1/batch-fetch`. | Many URLs per run; avoid one request per article. |
| Refresh watch | `/v1/history?domain=...` → `/v1/discover/{domain}?since=...` → fetch missing URLs only. | Avoid duplicate fetches and keep coverage fresh. |
| Search-assisted watch | `/v1/search?query=<topic>&site=<domain>` → `/v1/fetch`. | Topic monitoring such as rates, CPI, central bank, earnings. |

Recommended loop for a scheduled monitor:

1. Keep a watchlist of domains and topics in config, not hardcoded in the skill.
2. Discover candidates with `/v1/discover/{domain}` using a short `since` window such as `1d` or `12h`.
3. Normalize URLs and compare against local state to avoid repeated alerts.
4. Fetch only new URLs, usually with `no_images=true` for monitoring jobs.
5. Send a compact alert containing source, title, URL, and why it matters; do not alert when there is no new item.
6. Persist state after a successful run.

## Fetch-Oriented Smoke Check

Run these checks from the news-fetch path. Keep the token out of shell tracing (`set +x`).

```bash
set +x
BASE="${NEWS_FETCHER_BASE_URL:-https://<news-fetcher-host>}"
AUTH=(-H "Authorization: Bearer $NEWS_FETCHER_TOKEN")

curl -sS -i "${AUTH[@]}" "$BASE/v1/sites?limit=2" | sed -n '1,20p'
curl -sS -i "${AUTH[@]}" "$BASE/v1/discover/economist.com?limit=2" | sed -n '1,30p'
curl -sS -i "${AUTH[@]}" -H 'Content-Type: application/json' \
  -d '{"url":"https://www.economist.com/"}' \
  "$BASE/v1/fetch" | sed -n '1,30p'
```

Expected healthy fetch results:

- authenticated `/v1/sites?limit=2`: HTTP 200 with `ok=true`, `total`, `shown`, and `sites`.
- authenticated `/v1/discover/economist.com?limit=2`: HTTP 200 with `ok=true`, `domain=economist.com`, and candidate URLs.
- authenticated `/v1/fetch`: HTTP 200 with `ok=true`, `title`, `path`, `images`, and `text_length`.

If a single curl returns `SSL_ERROR_SYSCALL`, retry before declaring failure; this has appeared once as transient connection jitter while later requests succeeded.

## Endpoint Map

News-fetch related paths:

| Endpoint | Method | Purpose |
|---|---:|---|
| `/v1/sites` | GET | List supported news sites. Auth required. Supports `limit`. |
| `/v1/discover/{domain}` | GET | Discover recent/domain URLs. Auth required. Optional `since`, `limit`. |
| `/v1/fetch` | POST | Fetch one URL. Auth required. JSON body contains at least `url`. |
| `/v1/filter-urls` | POST | Filter candidate URLs through service rules. Auth required. |
| `/v1/batch-fetch` | POST | Fetch multiple URLs. Auth required. |
| `/v1/crawl` | POST | Crawl a site or seed set. Auth required. |
| `/v1/history` | GET | Query fetch history. Auth required. Supports filters such as `domain` and `limit` when available. |
| `/v1/search` | GET | Search endpoint. Auth required. Requires `query`; optional `site`, `limit`. May need `BRAVE_API_KEY` server-side. |

For request bodies not shown here, inspect the service schema first, then keep this skill focused on the news-fetch workflow.

## Common Commands

List supported sites:

```bash
curl -sS "${NEWS_FETCHER_BASE_URL}/v1/sites?limit=20" \
  -H "Authorization: Bearer ${NEWS_FETCHER_TOKEN}" | jq .
```

Discover recent URLs for a domain:

```bash
curl -sS "${NEWS_FETCHER_BASE_URL}/v1/discover/economist.com?since=7d&limit=5" \
  -H "Authorization: Bearer ${NEWS_FETCHER_TOKEN}" | jq .
```

Fetch one URL:

```bash
curl -sS "${NEWS_FETCHER_BASE_URL}/v1/fetch" \
  -H "Authorization: Bearer ${NEWS_FETCHER_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.economist.com/"}' | jq .
```

Search, when server-side search is configured:

```bash
curl -sS -G "${NEWS_FETCHER_BASE_URL}/v1/search" \
  -H "Authorization: Bearer ${NEWS_FETCHER_TOKEN}" \
  --data-urlencode 'query=economist.com' \
  --data-urlencode 'site=economist.com' \
  --data-urlencode 'limit=5' | jq .
```

A healthy fetch response for the Economist homepage has been observed as:

```json
{
  "ok": true,
  "url": "https://www.economist.com/",
  "domain": "economist.com",
  "strategy": "ua:custom",
  "title": "The Economist",
  "path": "articles/the-economist/the-economist.md",
  "images": 20,
  "text_length": 12231
}
```

## Bundled Script

This skill includes `scripts/news_fetcher_client.py`, a dependency-free Python helper for common checks.

```bash
python skills/dev-ops/news-fetcher-api/scripts/news_fetcher_client.py sites --limit 2
python skills/dev-ops/news-fetcher-api/scripts/news_fetcher_client.py discover economist.com --limit 2
python skills/dev-ops/news-fetcher-api/scripts/news_fetcher_client.py fetch https://www.economist.com/
```

The script reads `NEWS_FETCHER_BASE_URL` and `NEWS_FETCHER_TOKEN`. It refuses authenticated commands when the token is missing.

## Reporting Format

When reporting fetch results, be concrete and include HTTP status plus the useful fetch output:

```markdown
News Fetcher 抓取验证通过。

- Bearer 认证 `/v1/sites?limit=2`: HTTP 200，返回站点总数和示例站点
- Bearer 认证 `/v1/discover/economist.com?limit=2`: HTTP 200，返回候选 URL
- Bearer 认证 `/v1/fetch`: HTTP 200，返回标题、输出路径、图片数、文本长度
```

Do not include the full token in the report. If the user pasted a token into chat, treat it as exposed and recommend rotation.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| 401 `invalid or missing bearer token` | Missing/incorrect Bearer header | Use `Authorization: Bearer $NEWS_FETCHER_TOKEN`. |
| 401 with `x-api-key` | Wrong auth scheme | Switch to Bearer auth. |
| 422 on `/v1/search` | Missing required `query` | Add `--data-urlencode 'query=...'`. |
| `/v1/search` returns hint about `BRAVE_API_KEY` | Search backend not configured server-side | Use `/v1/discover/{domain}` or configure server-side `BRAVE_API_KEY`. |
| 404 on guessed endpoints like `/v1/articles` | Endpoint does not exist | Use the news-fetch paths in this skill; inspect schema only when adding unsupported bodies. |
| domain appears as `domain` instead of real domain | Literal `{domain}` was not replaced in path | Call `/v1/discover/economist.com`, not `/v1/discover/{domain}?domain=...`. |
| intermittent SSL error | transient network/TLS jitter | Retry once or twice before escalating. |

## Verification Checklist

- [ ] Base URL is `https://<news-fetcher-host>` unless the user specified another news-fetcher API host.
- [ ] `NEWS_FETCHER_TOKEN` is present for authenticated endpoints.
- [ ] No command uses shell tracing with secrets visible.
- [ ] Auth uses `Authorization: Bearer ...`.
- [ ] The workflow stays focused on news-fetch actions: sites, discover, fetch, filter, batch, crawl, history, or search.
- [ ] The final report includes HTTP status codes and semantic checks.
- [ ] The final report redacts tokens and recommends rotation if a token was posted publicly.
