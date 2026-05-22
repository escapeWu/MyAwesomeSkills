---
name: perplexity-search
description: Use when searching with escapeWu/perplexity-ai through its OpenAI-compatible HTTP endpoint. Provides config-driven quick/balanced/expert/deep routing over /v1/chat/completions, matching the current perplexity-ai model IDs.
---

# Perplexity Search & Analysis

This skill uses the current `escapeWu/perplexity-ai` server as an HTTP backend, not the official Perplexity API directly. The backend exposes OpenAI-compatible endpoints:

- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/files`, `GET /v1/files/{file_id}`, `DELETE /v1/files/{file_id}`

Default base URL is therefore the local/proxy server with `/v1` included:

```text
http://127.0.0.1:8000/v1
```

Prefer the bundled script instead of hand-writing HTTP requests:

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --query "latest verified OpenAI news today" \
  --show-plan
```

## Backend Reference

Checked against `https://github.com/escapeWu/perplexity-ai` at commit `2b55705`.

Important current facts:

- Auth is `Authorization: Bearer <MCP_TOKEN>`.
- OpenAI-compatible chat endpoint is `/v1/chat/completions`.
- Non-streaming responses include top-level `sources` from the backend.
- Streaming is fake streaming: the backend fetches the full answer first, streams chars, then emits a final chunk with `sources`.
- Current model IDs are generated from `MODEL_MAPPINGS` in `perplexity/config.py` via `perplexity/server/utils.py`.

## Configuration

Public repos should commit `config.example.json` only. For local use, copy it to `config.json` and set the real token:

```bash
cp /Users/shancw/.hermes/skills/research/perplexity-search/config.example.json \
   /Users/shancw/.hermes/skills/research/perplexity-search/config.json
```

Default config shape:

```json
{
  "model": "perplexity-search",
  "auto_model": "perplexity-search",
  "fast_model": "perplexity-search",
  "expert_model": "perplexity-thinking",
  "deep_model": "perplexity-deepsearch",
  "default_mode": "auto",
  "language": "zh-CN",
  "base_url": "http://127.0.0.1:8000/v1",
  "api_key": "REPLACE_ME",
  "stream": false,
  "timeout_seconds": 240,
  "max_sources": 5,
  "technical_required_sources": ["Reddit", "Hacker News"],
  "extra_body": {}
}
```

Key fields:

- `base_url`: endpoint base URL including `/v1`; the script posts to `${base_url}/chat/completions`.
- `api_key`: backend `MCP_TOKEN`, sent as bearer auth.
- `fast_model`: quick lookup model, default `perplexity-search`.
- `auto_model` / `model`: balanced search model, default `perplexity-search`.
- `expert_model`: single-pass reasoning model, default `perplexity-thinking`.
- `deep_model`: deep research final model, default `perplexity-deepsearch`.
- `extra_body`: optional JSON fields merged into the request body for compatible proxies.

## Current Model IDs

Common IDs exposed by `escapeWu/perplexity-ai`:

| Model ID | Backend mode | Use |
|---|---|---|
| `perplexity-search` | pro | default web-backed search |
| `sonar` | pro | Perplexity sonar option |
| `gpt-5-4` | pro | GPT-5.4 search mode |
| `claude-4-6-sonnet` | pro | Claude search mode |
| `gemini-3-1-pro` | pro | Gemini search mode |
| `perplexity-thinking` | reasoning | default reasoning |
| `gpt-5-4-thinking` | reasoning | GPT thinking mode |
| `claude-4-6-sonnet-thinking` | reasoning | Claude thinking mode |
| `gemini-3-1-pro-thinking` | reasoning | Gemini thinking mode |
| `kimi-k2-thinking` | reasoning | Kimi thinking mode |
| `perplexity-deepsearch` | deep research | slow comprehensive research |

Do not use older official API IDs like `sonar-pro` or `sonar-deep-research` as defaults for this skill; those do not match this backend's current OpenAI-compatible model map.

## Routing Modes

### `auto` 默认模式

The script assesses query complexity and routes automatically:

- simple lookup → `quick`
- standard search / ordinary verification → `balanced`
- complex investigation / timeline / comparison → `deep`

### `quick`

Single HTTP call with `fast_model` (`perplexity-search`). Use for current facts, simple news checks, prices, definitions, or short API lookups.

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --mode quick \
  --query "BTC price now" \
  --show-plan
```

### `balanced`

Single HTTP call with `auto_model` (`perplexity-search`). Use for normal “查一下 + 给结论” tasks where sources matter but exhaustive investigation is unnecessary.

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --mode balanced \
  --query "latest verified summary of Anthropic model releases"
```

### `expert`

Single HTTP call with `expert_model` (`perplexity-thinking`). Use when you want stronger reasoning without a scout/gap-fill chain.

```bash
python /Users/shancw/.hermes/skills/research/perplexity-search/scripts/perplexity_search.py \
  --mode expert \
  --query "compare current OpenAI, Anthropic, and Google frontier model offerings"
```

### `deep`

Three-stage route:

1. Scout with `fast_model` (`perplexity-search`) to collect facts and gaps.
2. Gap-fill with `fast_model` only when gaps are detected.
3. Final synthesis with `deep_model` (`perplexity-deepsearch`).

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
- `--model`: force a specific OpenAI-compatible model ID and skip automatic routing.
- `--base-url`: override endpoint base URL, usually ending in `/v1`.
- `--api-key`: override config token.
- `--max-sources`: number of source URLs to retain.
- `--language`: preferred answer language, default `zh-CN`.
- `--timeout`: HTTP timeout in seconds.
- `--stream`: request SSE streaming. With this backend, streaming is character-by-character after full generation.
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

1. Do not commit a real `config.json` with `MCP_TOKEN`. Commit `config.example.json`; keep `config.json` local.
2. Do not point this skill at `https://api.perplexity.ai` unless you intentionally override the model IDs too. The defaults target `escapeWu/perplexity-ai`.
3. Do not run every query through `perplexity-deepsearch`; use `auto` unless the user explicitly needs deep investigation.
4. If using a custom proxy, keep it OpenAI-compatible: `/v1/chat/completions`, `messages`, `model`, bearer auth.
