# Agent Skills API Reference

## Base URL

`{BASE_URL}` — replace with the actual deployment address. All endpoints below are relative to this base.

## Authentication

Protected endpoints require a Bearer token with `agent-skills` permission:

```
Authorization: Bearer {API_KEY}
```

Obtain API keys via `POST {BASE_URL}/api/apikeys` (requires management access).

---

## Endpoints

### List All Skills

```
GET /api/agent-skills
```

Returns an array of skill summaries.

Response:

```json
[
  {
    "name": "crypto-sentiment-apis",
    "description": "管理加密货币舆情数据...",
    "version": "297fc0a8",
    "updated_at": "2026-02-23T12:49:19.461784+00:00"
  }
]
```

---

### Get Manifest

```
GET /api/agent-skills/manifest
```

Returns the full skill registry with file listings. Preferred for agent integration — one request gives everything needed for skill discovery.

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
      "description": "管理加密货币舆情数据...",
      "version": "297fc0a8",
      "updated_at": "2026-02-23T12:49:19.461784+00:00",
      "files": ["SKILL.md", "reference/舆情api.md", "version.json"]
    }
  ]
}
```

---

### List Skill Files

```
GET /api/agent-skills/{skill_name}
```

Returns all files in the skill directory.

Response:

```json
[
  { "path": "SKILL.md", "size": 1968, "is_text": true },
  { "path": "reference/api.md", "size": 2375, "is_text": true },
  { "path": "version.json", "size": 79, "is_text": true }
]
```

---

### Read Skill File

```
GET /api/agent-skills/{skill_name}/{file_path}
```

Returns the file content as `text/plain`. Only text files are supported.

Supported extensions: `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`, `.py`, `.js`, `.ts`, `.sh`, `.css`, `.html`, `.xml`, `.csv`, `.ini`, `.cfg`, `.conf`, `.env`, `.mdc`, `.rst`, `.log`

Error codes:
- `400` — path traversal attempt
- `404` — file not found
- `415` — unsupported file type (binary)

---

### Bump Version

```
POST /api/agent-skills/{skill_name}/bump-version
```

Generates a new 8-char hex version and updates `version.json`.

Response:

```json
{
  "version": "a1b2c3d4",
  "updated_at": "2026-02-23T12:53:47.029167+00:00"
}
```

Use this after modifying any file in a skill directory.
