# Skills

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.

## All Skills

| Skill | Description |
|-------|-------------|
| [autonomous-codex-supervision](./skills/autonomous-codex-supervision) | Plan, launch, supervise, and integrate Codex/agent implementation work: tmux/cron supervisors, TaskNode task boards, Release-the-Hounds parallel worktrees, L1 full-auto project ownership, validation gates, bounded repair, safe checkpointing. |
| [codex-review](./skills/codex-review) | AI-powered code review using OpenAI Codex CLI (review / 代码审查 / 审一下). Runs lint + codex review in an isolated context and auto-updates CHANGELOG. |
| [dev-ops/database-schema-analyzer](./skills/dev-ops/database-schema-analyzer) | Analyze PostgreSQL or MySQL schemas from DDL, schema-only dumps, migration SQL, or read-only metadata. Produces tables, keys, indexes, inferred relationships, ER diagrams, DBML, and Mermaid ERD. |
| [dev-ops/news-fetcher-api](./skills/dev-ops/news-fetcher-api) | Work with the news fetcher REST API: supported-site lookup, domain article discovery, URL fetching, batch fetch/crawl, fetch history, and Bearer-authenticated integration. |
| [dev-ops/project-dev-standards](./skills/dev-ops/project-dev-standards) | Bootstrap or refresh repository-specific development standards from a real codebase. Generates evidence-backed `docs/ai-dev-standards/` and updates managed blocks in `AGENTS.md` / `CLAUDE.md`. |
| [grok_search](./skills/grok_search) | 自适应 AI 搜索与最新信息检索。先评估任务复杂度，再在 grok-4.20-fast / auto / expert 之间路由，必要时用「fast 侦察 + fast 补缺 + expert 综合」组合流程。 |
| [harness/document-organization-harness](./skills/harness/document-organization-harness) | Organize or retrofit project documentation: root agent rules, overview/index maps, truth ownership, durable status routing, and validation gates. |
| [harness/progressive-disclosure-docs](./skills/harness/progressive-disclosure-docs) | Design, audit, or refactor docs so agents navigate progressively through maps, indexes, owning feature docs, references, collaboration records, and archives. |
| [harness/project-analysis](./skills/harness/project-analysis) | Deep project analysis for architecture, dataflow, route impact, performance risk, and expected-vs-implemented gaps; stable conclusions return to owning docs. |
| [harness/project-docs-workflow](./skills/harness/project-docs-workflow) | Orchestrate mainline routes and docs maintenance before and after non-trivial feature, bug, refactor, API, or cross-module changes. |
| [harness/external-collaboration-workflow](./skills/harness/external-collaboration-workflow) | Preserve external problem/proposal provenance, record item-level adoption, and translate accepted recommendations into internal contracts before implementation. |
| [harness/refactor-large-modules](./skills/harness/refactor-large-modules) | Split oversized or mixed-responsibility modules by stable ownership while preserving public contracts, behavior, state, and evidence boundaries. |
| [internal-comms](./skills/internal-comms) | Write internal communications using the formats my company prefers (status updates, announcements, etc.). |
| [mcp-builder](./skills/mcp-builder) | Guide for creating high-quality MCP (Model Context Protocol) servers that expose external services as well-designed tools. |
| [mermaid-live-preview](./skills/mermaid-live-preview) | Generate mermaid.live/edit preview URLs from Mermaid diagram code (pako-encoded), for sharing or quick preview. |
| [perplexity-search](./skills/perplexity-search) | escapeWu/perplexity-ai HTTP search with OpenAI-compatible model IDs, config-driven quick/balanced/expert/deep routing, and source extraction. |
| [skill-creator](./skills/skill-creator) | Guide for creating or updating skills: `SKILL.md` structure, workflows, and tool integration. |
| [style-extractor](./skills/style-extractor) | 一个能够最大化提取网页风格的 skill。（submodule: `Lucent-Snow/style-extractor`） |
| [ui-ux-pro-max-skill](./skills/ui-ux-pro-max-skill) | AI skill providing design intelligence for building professional UI/UX across platforms.（submodule: `nextlevelbuilder/ui-ux-pro-max-skill`） |
| [xlsx](./skills/xlsx) | Read, edit, or create spreadsheet files (`.xlsx` / `.xlsm` / `.csv` / `.tsv`) — add columns, compute, fix, or convert. |

> `harness/*` is the reusable harness bundle. Start with
> [`skills/harness/README.md`](./skills/harness/README.md) for the target-repo
> `AGENTS.md` patch contract, then see the
> [`harness-bundle.json`](./skills/harness/document-organization-harness/assets/harness-bundle.json)
> manifest for bundle membership.
> `style-extractor` and `ui-ux-pro-max-skill` are git submodules; run `git submodule update --init` to populate them.

## Structure

```
skills/          # All skill folders
spec/            # Agent Skills specification
template/        # Skill template for creating new skills
```

## Creating a New Skill

Each skill is a folder with a `SKILL.md` file:

```markdown
---
name: my-skill-name
description: What this skill does and when to use it
---

# My Skill Name

Instructions, examples, and guidelines here.
```

See [template/SKILL.md](./template/SKILL.md) for a starting point.
