---
name: perplexity-search
description: Advanced real-time web search and deep research using Perplexity over an HTTP chat-completions endpoint. Use when fetching current web data, API docs, news, or running multi-stage investigations with quick/balanced/expert/deep routing.
---

# Perplexity Search & Analysis

Use this skill for fetching real-time data, API docs, news, current market facts, and complex investigations through Perplexity's HTTP endpoint. Prefer the bundled script instead of hand-writing HTTP requests:

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --query "latest verified OpenAI news today"
```

The script uses an OpenAI-compatible `/chat/completions` API, so it can point at Perplexity directly or at a compatible proxy.

## Configuration

Public repos should commit `config.example.json` only. For local use, copy it to `config.json` and set the real key:

```bash
cp /Users/shancw/.hermes/skills/research/perplexity-search/config.example.json \
   /Users/shancw/.hermes/skills/research/perplexity-search/config.json
```

Default config shape:

```json
{
  "model": "sonar-pro",
  "auto_model": "sonar-pro",
  "fast_model": "sonar",
  "expert_model": "sonar-deep-research",
  "default_mode": "auto",
  "language": "zh-CN",
  "base_url": "https://api.perplexity.ai",
  "api_key": "REPLACE_ME",
  "stream": false,
  "timeout_seconds": 240,
  "max_sources": 5,
  "technical_required_sources": ["Reddit", "Hacker News"],
  "extra_body": {}
}
```

Key fields:

- `base_url`: HTTP endpoint base URL. The script posts to `${base_url}/chat/completions`.
- `api_key`: bearer token for the endpoint.
- `fast_model`: quick lookups, default `sonar`.
- `auto_model` / `model`: balanced searches, default `sonar-pro`.
- `expert_model`: final deep synthesis, default `sonar-deep-research`.
- `extra_body`: optional endpoint-specific JSON fields merged into the request body.

## Routing Modes

### `auto` 默认模式

The script assesses query complexity and routes automatically:

- simple lookup → `quick`
- standard search / ordinary verification → `balanced`
- complex investigation / timeline / comparison → `deep`

### `quick`

Single HTTP call with `fast_model`. Use for current facts, simple news checks, prices, definitions, or short API lookups.

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --mode quick \
  --query "BTC price now" \
  --show-plan
```

### `balanced`

Single HTTP call with `auto_model`. Use for normal “查一下 + 给结论” tasks where sources matter but exhaustive investigation is unnecessary.

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --mode balanced \
  --query "latest verified summary of Anthropic model releases"
```

### `expert`

Single HTTP call with `expert_model`. Use when you want the strongest single-pass synthesis without a scout/gap-fill chain.

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --mode expert \
  --query "compare current OpenAI, Anthropic, and Google frontier model offerings"
```

### `deep`

Three-stage route:

1. Scout with `fast_model` to collect facts and gaps.
2. Gap-fill with `fast_model` only when gaps are detected.
3. Final synthesis with `expert_model`.

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --mode deep \
  --query "build a timeline of the latest SEC crypto ETF decisions and compare issuer status" \
  --json
```

## Technical Queries

For technical questions involving errors, APIs, libraries, versions, frameworks, deployment, databases, or model benchmarks, the script automatically appends a source requirement: cover Reddit and Hacker News when relevant, in addition to official docs, GitHub, and vendor sources. If one of those communities has no useful result, the answer should say so explicitly.

## CLI Parameters

- `--query`: required user query.
- `--mode`: `auto | quick | balanced | expert | deep`.
- `--model`: force a specific model and skip automatic routing.
- `--base-url`: override HTTP endpoint base URL.
- `--api-key`: override config API key.
- `--max-sources`: number of source URLs to retain.
- `--language`: preferred answer language, default `zh-CN`.
- `--timeout`: HTTP timeout in seconds.
- `--stream`: use SSE streaming if the endpoint supports it.
- `--json`: emit structured JSON.
- `--show-plan`: show routing metadata before the answer.
- `--show-reasoning`: print model reasoning fields if the endpoint returns them.

## Output Contract

Text mode prints:

```text
概述：...
搜索结果：
...
来源：
1. https://...
```

JSON mode includes:

- `query`
- `model`
- `route`
- `base_url`
- `overview`
- `search_results`
- `sources`
- `stages`
- `raw_response`

## Common Pitfalls

1. Do not commit a real `config.json` with API keys. Commit `config.example.json`; keep `config.json` local.
2. Do not use MCP-only tool names in this skill. The script calls the HTTP endpoint directly.
3. Do not run every query through `sonar-deep-research`; use `auto` unless the user explicitly needs deep investigation.
4. If a proxy endpoint is used, keep it OpenAI-compatible: `/chat/completions`, `messages`, `model`, bearer auth.
