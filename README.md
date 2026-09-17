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
| [harness/add-idea](./skills/harness/add-idea) | Lightweight docs-only intake: find the owning Feature, ask only the most important unresolved product or hard-boundary question, and update the smallest core docs once. |
| [harness/document-organization-harness](./skills/harness/document-organization-harness) | Build or simplify a minimal docs map with short root rules, optional overview/index routing, Feature READMEs, and targeted references. |
| [harness/progressive-disclosure-docs](./skills/harness/progressive-disclosure-docs) | Reduce context and maintenance cost through a small progressive-disclosure docs structure with no mandatory Spec or status lifecycle. |
| [harness/project-analysis](./skills/harness/project-analysis) | Focused architecture, dataflow, route, performance, bug, and behavior-gap analysis; persist only durable findings after the task is resolved. |
| [harness/project-docs-workflow](./skills/harness/project-docs-workflow) | Read minimal task context, finish implementation and validation, then asynchronously delegate one bounded core-docs update. |
| [harness/external-collaboration-workflow](./skills/harness/external-collaboration-workflow) | Preserve external proposal provenance and concise adoption decisions without creating a parallel contract or progress system. |
| [harness/docs-issue-sync](./skills/harness/docs-issue-sync) | Sync completed Issue/PR work into existing module documentation as concise functional facts with provenance and executable query clues; never create recent-completion history sections. |
| [harness/github-issue-development](./skills/harness/github-issue-development) | Global Issue-to-PR workflow with exact-base worktrees, authorization boundaries, validation handoff, docs sync, commit, push, PR, and merge wait states. |
| [harness/refactor-large-modules](./skills/harness/refactor-large-modules) | Split oversized or mixed-responsibility modules by stable ownership while preserving public contracts, behavior, state, and evidence boundaries. |
| [internal-comms](./skills/internal-comms) | Write internal communications using the formats my company prefers (status updates, announcements, etc.). |
| [mcp-build-best-practice](./skills/mcp-build-best-practice) | Design, audit, and productionize robust MCP servers from protocol contracts and safety controls through progressive discovery, protocol tests, and live deployment verification. |
| [mcp-builder](./skills/mcp-builder) | Guide for creating high-quality MCP (Model Context Protocol) servers that expose external services as well-designed tools. |
| [mcp-tool-expose-guidebook](./skills/mcp-tool-expose-guidebook) | Design and validate progressive-disclosure MCP guide indexes exposed through both callable tools and standard resources. |
| [mermaid-live-preview](./skills/mermaid-live-preview) | Generate mermaid.live/edit preview URLs from Mermaid diagram code (pako-encoded), for sharing or quick preview. |
| [perplexity-search](./skills/perplexity-search) | escapeWu/perplexity-ai HTTP search with OpenAI-compatible model IDs, config-driven quick/balanced/expert/deep routing, and source extraction. |
| [skill-creator](./skills/skill-creator) | Guide for creating or updating skills: `SKILL.md` structure, workflows, and tool integration. |
| [style-extractor](./skills/style-extractor) | 一个能够最大化提取网页风格的 skill。（submodule: `Lucent-Snow/style-extractor`） |
| [ui-ux-pro-max-skill](./skills/ui-ux-pro-max-skill) | AI skill providing design intelligence for building professional UI/UX across platforms.（submodule: `nextlevelbuilder/ui-ux-pro-max-skill`） |
| [xlsx](./skills/xlsx) | Read, edit, or create spreadsheet files (`.xlsx` / `.xlsm` / `.csv` / `.tsv`) — add columns, compute, fix, or convert. |

> `harness/*` is a coordinated suite of independently maintained skills. Start with
> [`skills/harness/README.md`](./skills/harness/README.md) for the target-repo
> `AGENTS.md` patch contract, then review the suite [changelog](./skills/harness/CHANGELOG.md)
> and [per-project maintenance guide](./skills/harness/UPGRADING.md). The repository does not
> provide bundle installation or automatic target-project upgrades.
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
