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

## Quick Start

```
# 1. Discover skills
GET {BASE_URL}/api/agent-skills/manifest

# 2. Load a specific skill's instructions
GET {BASE_URL}/api/agent-skills/{skill_name}/SKILL.md

# 3. Load reference docs if needed
GET {BASE_URL}/api/agent-skills/{skill_name}/reference/{file}.md
```

All protected endpoints require `Authorization: Bearer {API_KEY}` with `agent-skills` permission.

## Workflow

### Step 1 — Skill Discovery via Manifest

Call the manifest endpoint to get a full inventory:

```
GET {BASE_URL}/api/agent-skills/manifest
Authorization: Bearer {API_KEY}
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
GET {BASE_URL}/api/agent-skills/{skill_name}/SKILL.md
Authorization: Bearer {API_KEY}
```

Returns plain text Markdown. Inject this into the agent's system/user prompt as operational instructions.

### Step 3 — Load References (Optional)

If the skill lists reference files, load them for detailed API schemas:

```
GET {BASE_URL}/api/agent-skills/{skill_name}/{file_path}
Authorization: Bearer {API_KEY}
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

- `{BASE_URL}` and `{API_KEY}` are environment-specific — never hardcode real values
- API keys require `agent-skills` permission scope
- All file content is UTF-8 encoded
- Path traversal is blocked server-side; only files within the skill directory are accessible
- `version.json` is auto-generated — never edit it manually, use the bump-version endpoint
