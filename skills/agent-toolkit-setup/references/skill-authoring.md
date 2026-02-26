# Skill Authoring Guide

## Directory Structure

Each skill lives in its own directory under `agent-skills/`:

```
agent-skills/
└── my-skill/
    ├── SKILL.md          # Required — skill definition with frontmatter
    ├── version.json      # Auto-generated — do not edit manually
    └── reference/        # Optional — supplementary API/schema docs
        └── api.md
```

---

## SKILL.md Format

Every `SKILL.md` must begin with a YAML frontmatter block:

```yaml
---
name: my-skill
description: |
  Concise description of what this skill does and when an agent should use it.
  1–3 sentences covering the skill's purpose and trigger scenarios.
---

# My Skill

Skill instructions body...
```

### Frontmatter Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Skill identifier (can differ from directory name) |
| `description` | Yes | Shown in manifest; used by agents for skill selection |

The `description` is the primary signal agents use to decide whether to load a skill. Write it from the agent's perspective: "use this skill when...".

---

## Writing Effective Descriptions

Good:
```yaml
description: |
  管理加密货币舆情数据：查询、采集、录入、去重和清理舆情记录。
  当用户需要查询币种舆情、执行爬虫采集、清理重复数据时触发。
```

Bad:
```yaml
description: This skill does stuff with crypto data.
```

Rules:
- State the domain clearly (what system/API this skill operates on)
- Include trigger scenarios ("when user needs to...", "use when...")
- Keep it under 3 sentences

---

## Reference Files

Place detailed API documentation in `reference/`:

```
reference/
├── sentiment-api.md    # Endpoint details, request/response schemas
└── crawler-api.md      # Separate concern per file
```

Reference them from SKILL.md using relative links:

```markdown
> 完整参数见 @reference [sentiment-api.md](reference/sentiment-api.md)
```

---

## Version Management

After creating or modifying any file in a skill directory:

```
POST {BASE_URL}/api/agent-skills/{skill_name}/bump-version
Authorization: Bearer {API_KEY}
```

This updates `version.json` automatically. Agents use version changes to invalidate their skill cache.

**Rules:**
- Never edit `version.json` by hand
- Call bump-version after every content change, including reference files
- New skills must call bump-version once after creation to get an initial version

---

## Checklist: New Skill

- [ ] Create directory under `agent-skills/`
- [ ] Write `SKILL.md` with valid frontmatter (`name` + `description`)
- [ ] Add `reference/` docs if the skill involves API calls
- [ ] Call `POST /api/agent-skills/{skill_name}/bump-version` to generate initial version
- [ ] Verify skill appears in `GET /api/agent-skills/manifest` with non-null description and version
