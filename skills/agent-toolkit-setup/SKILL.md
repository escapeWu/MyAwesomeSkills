---
name: agent-toolkit-setup
description: Guide for integrating with the AI Trade Toolkit's Agent Skills system. Use when setting up agent skill discovery, loading skill definitions via the manifest API, or creating new skills that follow the platform's SKILL.md frontmatter conventions. Covers manifest endpoint usage, skill file retrieval, version tracking, and authoring new skills.
---

# Agent Toolkit — Skill Integration Guide

Integrate external AI agents with the AI Trade Toolkit's Agent Skills registry. The platform exposes a REST API that allows agents to discover, load, and consume skill definitions at runtime.

## Overview

The Agent Skills system serves structured skill documents (Markdown + YAML frontmatter) via HTTP. An agent can:

1. Discover all available skills in one request (manifest)
2. Selectively load skill content into its context
3. Track skill versions to avoid redundant fetches

## Prerequisites — Environment Check

Before any API call, check that the required environment variables are set:

- `AGENT_TOOLKIT_BASE_URL` — the platform base URL
- `AGENT_TOOLKIT_API_KEY` — API key with `agent-skills` permission

### Detection

Read the current project's `.env` file (or shell environment). If either variable is missing or empty:

1. Stop and inform the user:
   > "Agent Toolkit 尚未配置。需要提供 Base URL 和 API Key 才能继续。"
2. Ask the user for the missing values:
   - Base URL (e.g. `https://your-domain.example.com`)
   - API Key (the full token string)
3. Write both values into the project's `.env` file:
   ```
   AGENT_TOOLKIT_BASE_URL=https://your-domain.example.com
   AGENT_TOOLKIT_API_KEY=your-api-key-here
   ```
4. If `.env` already exists, append only the missing variables — do not overwrite existing entries.

### Validation

After writing `.env`, verify the connection works by calling the public endpoint:

```
GET ${AGENT_TOOLKIT_BASE_URL}/api/docs
```

If this returns a valid OpenAPI JSON response, the base URL is correct. Then verify the API key:

```
GET ${AGENT_TOOLKIT_BASE_URL}/api/agent-skills
Authorization: Bearer ${AGENT_TOOLKIT_API_KEY}
```

If this returns a JSON array (even empty `[]`), the key is valid. If it returns `401` or `403`, inform the user the API key is invalid or lacks `agent-skills` permission.

Only proceed to the workflow steps below after both checks pass.

## Quick Start

```
# 0. Get full OpenAPI schema (no auth required)
GET ${AGENT_TOOLKIT_BASE_URL}/api/docs

# 1. Discover skills
GET ${AGENT_TOOLKIT_BASE_URL}/api/agent-skills/manifest

# 2. Load a specific skill's instructions
GET ${AGENT_TOOLKIT_BASE_URL}/api/agent-skills/{skill_name}/SKILL.md

# 3. Load reference docs if needed
GET ${AGENT_TOOLKIT_BASE_URL}/api/agent-skills/{skill_name}/reference/{file}.md
```

All protected endpoints require `Authorization: Bearer ${AGENT_TOOLKIT_API_KEY}` with `agent-skills` permission.

## API Docs (No Auth)

The platform exposes its complete OpenAPI schema at a public endpoint — no authentication required:

```
GET ${AGENT_TOOLKIT_BASE_URL}/api/docs
```

Returns the full OpenAPI 3.x JSON schema covering all modules (market, sentiment, analysis, crawler, agent-skills, etc.). Use this to:

- Understand all available API capabilities before integrating
- Auto-generate client code or type definitions
- Discover endpoints beyond agent-skills (market data, chart generation, etc.)

An interactive Swagger UI is also available at `${AGENT_TOOLKIT_BASE_URL}/docs` for manual exploration.

## Workflow

### Step 1 — Skill Discovery via Manifest

Call the manifest endpoint to get a full inventory:

```
GET ${AGENT_TOOLKIT_BASE_URL}/api/agent-skills/manifest
Authorization: Bearer ${AGENT_TOOLKIT_API_KEY}
```

Response:

```json
{
  "name": "AI Trade Toolkit",
  "description": "加密货币市场数据、舆情管理、技术分析的 Agent 技能集合",
  "api_base": "/api/agent-skills",
  "skills": [
    {
      "name": "crypto-sentiment-apis",
      "display_name": "crypto-sentiment",
      "description": "管理加密货币舆情数据：查询、采集、录入、去重和清理舆情记录。...",
      "version": "297fc0a8",
      "updated_at": "2026-02-23T12:49:19.461784+00:00",
      "files": ["SKILL.md", "reference/舆情api.md", "reference/爬虫api.md", "version.json"]
    }
  ]
}
```

Use `description` to decide which skills are relevant to the current task. Use `version` to cache and invalidate.

### Step 2 — Load Skill Content

Fetch the SKILL.md for the chosen skill:

```
GET ${AGENT_TOOLKIT_BASE_URL}/api/agent-skills/{skill_name}/SKILL.md
Authorization: Bearer ${AGENT_TOOLKIT_API_KEY}
```

Returns plain text Markdown. Inject this into the agent's system/user prompt as operational instructions.

### Step 3 — Load References (Optional)

If the skill lists reference files, load them for detailed API schemas:

```
GET ${AGENT_TOOLKIT_BASE_URL}/api/agent-skills/{skill_name}/{file_path}
Authorization: Bearer ${AGENT_TOOLKIT_API_KEY}
```

Only text files are served (`.md`, `.json`, `.yaml`, `.txt`, etc.).

## Caching Strategy

- Store `version` from manifest alongside cached skill content
- On subsequent runs, fetch manifest and compare versions
- Only re-fetch SKILL.md + references when version changes
- `version` is an 8-char hex string, changes on every skill update

## API Reference

See [agent-skills-api.md](references/agent-skills-api.md) for the full endpoint reference.

## Authoring New Skills

See [skill-authoring.md](references/skill-authoring.md) for the SKILL.md format specification and best practices.

## Rules

- Environment variables `AGENT_TOOLKIT_BASE_URL` and `AGENT_TOOLKIT_API_KEY` must be set before any API call — see Prerequisites above
- Never hardcode real URLs or API keys in code or prompts
- API keys require `agent-skills` permission scope
- All file content is UTF-8 encoded
- Path traversal is blocked server-side; only files within the skill directory are accessible
- `version.json` is auto-generated — never edit it manually, use the bump-version endpoint
