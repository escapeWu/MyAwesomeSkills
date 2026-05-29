# Skills

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.

## All Skills

| Skill | Description |
|-------|-------------|
| [autonomous-codex-supervision](./skills/autonomous-codex-supervision) | Use when planning, launching, supervising, or integrating Codex/agent implementation work: tmux/cron supervisors, TaskNode task boards, Release-the-Hounds parallel worktrees, L1 full-auto project ownership, validation... |
| [codex-review](./skills/codex-review) | AI-powered code review using OpenAI Codex CLI. Use when the user asks to review, audit, or check their code — including "代码审核", "代码审查", "审查代码", "review", "code review", "帮我审核", "检查代码", "审一下". Performs lint + codex rev... |
| [dev-ops/database-schema-analyzer](./skills/dev-ops/database-schema-analyzer) | Analyze PostgreSQL or MySQL schemas from DDL files, schema-only dumps, migration SQL, or read-only metadata exports. Produces table summaries, primary/foreign keys, indexes, inferred relationships, ER diagrams, DBML, and Mermaid ERD. |
| [dev-ops/news-fetcher-api](./skills/dev-ops/news-fetcher-api) | Use when working with the news fetcher REST API at <news-fetcher-host> for supported-site lookup, domain article discovery, URL fetching, batch fetch/crawl workflows, fetch history queries, and Bearer-authenticated integration examples. |
| [dev-ops/project-dev-standards](./skills/dev-ops/project-dev-standards) | Bootstrap or refresh repository-specific development standards from a real local codebase. Generates evidence-backed `docs/ai-dev-standards/` and updates managed blocks in existing `AGENTS.md` / `CLAUDE.md`. |
| [grok_search](./skills/grok_search) | 自适应 AI 搜索与最新信息检索 skill。会先评估任务复杂度，再在 grok-4.20-fast / grok-4.20-auto / grok-4.20-expert 之间做路由，必要时采用“fast 侦察 + fast 补缺 + expert 综合”的组合流程，在速度与质量之间取平衡。 |
| [internal-comms](./skills/internal-comms) | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (stat... |
| [mcp-builder](./skills/mcp-builder) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or service... |
| [mermaid-live-preview](./skills/mermaid-live-preview) | Generate Mermaid diagram preview URLs for mermaid.live. Use when the user asks to preview, share, or create a link for a Mermaid diagram. Encodes Mermaid diagram code into a clickable mermaid.live/edit URL using pako... |
| [perplexity-search](./skills/perplexity-search) | escapeWu/perplexity-ai HTTP endpoint search with current OpenAI-compatible model IDs, config-driven quick/balanced/expert/deep routing, and source extraction. |
| [project-analysis](./skills/project-analysis) | 深度项目分析工具。用于在现有 docs 不足、代码链路复杂、需要梳理系统架构、模块数据流、时序或性能风险时进行只读取证和结构化分析。常与 `project-docs-workflow` 配套使用，作为其升级步骤；也可在用户明确要求架构分析、数据流分析、时序图、调用链梳理或性能排查时直接使用。默认应落文档：优先新建或更新 `docs/` 下合适文档，不再停留在仅终端输出的 analysis-only 模式。 |
| [project-docs-workflow](./skills/project-docs-workflow) | 项目 docs 维护编排器。用于非 trivial 的开发任务、功能开发、bug 修复、重构、API 变更、跨模块修改前后：先扫描 docs/OVERVIEW.md、feature-*、reference-*，把相关文档作为半可信上下文；判断是否需要升级使用 project-analysis 做深度分析；实现完成后判断哪些文档受影响，并先询问用户确认后再更新。看到用户要“实现/修改/开发/修复”项目代码时，应优先触发此技能，而不是... |
| [skill-creator](./skills/skill-creator) | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool inte... |
| [webapp-testing](./skills/webapp-testing) | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. |
| [xlsx](./skills/xlsx) | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, comp... |

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
