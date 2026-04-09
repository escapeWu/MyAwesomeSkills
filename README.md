# Skills

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.

## All Skills

### Creative & Design

| Skill | Description |
|-------|-------------|
| [canvas-design](./skills/canvas-design) | Create beautiful visual art in `.png` and `.pdf` documents using design philosophy. For posters, art, and static visual designs. |
| [frontend-design](./skills/frontend-design) | Create distinctive, production-grade frontend interfaces with high design quality. For web components, pages, landing pages, dashboards, etc. |
| [style-extractor](./skills/style-extractor) | Extract evidence-based web UI style + motion guides (Markdown, optional HTML prototype). |
| [theme-factory](./skills/theme-factory) | Toolkit for styling artifacts with a theme. 10 pre-set themes with colors/fonts for slides, docs, reports, HTML pages, etc. |

### Development & Technical

| Skill | Description |
|-------|-------------|
| [claude-agent-sdk-skill](./skills/claude-agent-sdk-skill) | Build production AI agents with the Claude Agent SDK. Covers Python and TypeScript SDKs with custom tools, hooks, multi-agent systems, and session management. |
| [cloudflare-tunnel](./skills/cloudflare-tunnel) | Manage and create Cloudflare Tunnels to expose local ports to the internet without opening firewall ports. |
| [codex-review](./skills/codex-review) | AI-powered code review using codex CLI. Auto-updates CHANGELOG, stages new files, evaluates task difficulty, and runs Lint + codex review in isolated context. |
| [mcp-builder](./skills/mcp-builder) | Guide for creating high-quality MCP (Model Context Protocol) servers in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| [mermaid-live-preview](./skills/mermaid-live-preview) | Generate Mermaid diagram preview URLs for mermaid.live. Encodes diagram code into clickable URLs using pako (zlib) + base64. |
| [perplexity-search](./skills/perplexity-search) | Real-time web search and deep research using Perplexity AI for latest web data, API docs, news, and investigations. |
| [project-analysis](./skills/project-analysis) | Deep repository analysis layer for architecture, data flow, sequence, and risk investigation. Pairs with project-docs-workflow to produce evidence-backed conclusions, Mermaid diagrams, and optional docs patches or standalone reports. |
| [project-docs-workflow](./skills/project-docs-workflow) | Thin docs orchestration layer for non-trivial code changes. Scans OVERVIEW/feature/reference docs as semi-trusted context, escalates to project-analysis when needed, and asks before patching docs. |
| [skill-creator](./skills/skill-creator) | Guide for creating effective skills that extend Claude's capabilities with specialized knowledge and workflows. |
| [webapp-testing](./skills/webapp-testing) | Toolkit for interacting with and testing local web applications using Playwright. Screenshots, browser logs, UI debugging. |
| [web-artifacts-builder](./skills/web-artifacts-builder) | Suite of tools for creating elaborate multi-component HTML artifacts using React, Tailwind CSS, and shadcn/ui. |

### Crypto Utilities

| Skill | Description |
|-------|-------------|
| [agent-toolkit-setup](./skills/agent-toolkit-setup) | Guide for integrating external AI agents with the Agent Toolkit's skill discovery, loading, and version tracking APIs. |
| [coinglass-liquidation-heatmap](./skills/coinglass-liquidation-heatmap) | Crypto liquidation heatmap data from Coinglass for market analysis and visualization. |
| [crypto-info-archive](./skills/crypto-info-archive) | Archive crypto market sentiment and analysis data for historical reference. |
| [crypto-market-data](./skills/crypto-market-data) | Fetch funding rate, long/short ratio, fear & greed index, and K-line screenshots for any trading pair in one parallel batch. |

### Enterprise & Utilities

| Skill | Description |
|-------|-------------|
| [CPA-antigravity-RT-exract](./skills/CPA-antigravity-RT-exract) | Extract Google Refresh Tokens from Antigravity JSON configuration files. Batch process and deduplicate refresh_token values. |
| [internal-comms](./skills/internal-comms) | Write internal communications: status reports, leadership updates, newsletters, FAQs, incident reports, project updates, etc. |

### Document Skills

| Skill | Description |
|-------|-------------|
| [pdf](./skills/pdf) | Read, create, merge, split, rotate, watermark, encrypt/decrypt, OCR, and fill forms in PDF files. |
| [xlsx](./skills/xlsx) | Open, read, edit, create, and convert spreadsheet files (`.xlsx`, `.xlsm`, `.csv`, `.tsv`). Formulas, charts, data cleaning. |

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
