---
name: progressive-disclosure-docs
description: >-
  Design, audit, or refactor project documentation so AI agents navigate by
  progressive disclosure: AGENTS.md/OVERVIEW.md as maps, feature/reference/archive
  indexes as routing layers, and detailed docs/task boards loaded only on demand.
  Use when creating or refactoring project docs for AI coding agents, auditing
  docs compatibility with context engineering, adding AGENTS.md or docs indexes,
  or migrating scattered Markdown into a navigable docs-first structure.
---

# Progressive Disclosure Docs Harness

Keep AI agents from loading an entire repository's documentation at once. Instead, expose a small stable map first, then route the agent into only the 1-3 documents relevant to the current task.

```text
Do not make agents read the city.
Give them a map, then signs, then the room they actually need.
```

## When to Use

- Creating or refactoring project docs for AI coding agents.
- Auditing whether a repo's docs are compatible with Harness Engineering / Context Engineering practices.
- Adding `AGENTS.md`, `AGENTS.md`, `docs/OVERVIEW.md`, or docs indexes.
- Organizing large feature docs, task boards, bugfix notes, RCA docs, API references, or historical plans.
- Migrating a project from scattered Markdown files into a navigable docs-first structure.

Do **not** use for general prose editing, API reference generation alone, or one-off README cleanup.

## Golden Navigation Skeleton

```text
AGENTS.md / AGENTS.md
  ↓
docs/OVERVIEW.md
  ↓
docs/feature/INDEX.md      docs/reference/INDEX.md      docs/archive/INDEX.md
  ↓                         ↓                            ↓
docs/feature/<module>/      stable technical facts        historical plans / bugfixes / RCA
  ↓
README.md or INDEX.md
  ↓
design.md / dataflow.md / changelog.md / taskBoard.md / RCA.md
```

Layer responsibilities:

| Level | File | Job |
|---|---|---|
| 0 | AGENTS.md / AGENTS.md | Stable agent contract. Short enough to always load. |
| 1 | docs/OVERVIEW.md | Project map: what the system is, main modules, where to go next. |
| 2F | docs/feature/INDEX.md | Feature routing table: module categories and entrypoints. |
| 2R | docs/reference/INDEX.md | Stable facts: architecture, API references, contracts, runbooks. |
| 2A | docs/archive/INDEX.md | Historical material: completed plans, bugfix notes, RCA. Default: do not read. |
| 3 | docs/feature/\<module\>/INDEX.md | Module-level map or summary. |
| 4 | Detailed module docs | Design, data flow, task board, logs. Read only when task-relevant. |

## Required Agent Reading Rule

Include in `AGENTS.md` and `docs/OVERVIEW.md`:

```text
文档遵循渐进式披露（Progressive Disclosure），Agent 逐层深入、禁止全量读取：

Level 0: AGENTS.md / AGENTS.md     → 项目开发规约与读取入口
Level 1: docs/OVERVIEW.md          → 项目是什么？有哪些模块？去哪里找？
Level 2F: feature/INDEX.md         → 功能模块索引，先选目标模块
Level 2R: reference/INDEX.md       → 架构 / API / 测试 / 运维等稳定参考
Level 2A: archive/INDEX.md         → 已完成计划 / bugfix / RCA 归档，默认不读
Level 3: feature/<module>/INDEX.md → 大型模块内部导航
Level 4: 具体设计 / 数据流 / taskBoard / RCA，仅按需读取

Agent 读取规则：OVERVIEW → INDEX → 按需读 1-3 个相关文档。禁止全量读取 docs。
```

## AGENTS.md Requirements

Stay small and stable. Include:

1. **Context entrypoint**: `> 项目上下文入口：[docs/OVERVIEW.md](docs/OVERVIEW.md)`
2. **One-paragraph project description**: what this project is and must not become.
3. **Hard architecture constraints**: layer dependencies, no-bypass rules.
4. **Progressive disclosure rule**: the level table above.
5. **Write rules**: when to create feature/reference/archive docs, when to update indexes.
6. **Testing and update rules**: which docs/tests to update when interfaces change.

## docs/OVERVIEW.md Requirements

First docs file an agent reads. Must answer:
- What is this system?
- What are the main modules?
- Which docs index should I enter next?
- What should I avoid reading by default?
- How do I run or validate the project?

Keep it compact. If it grows into full design documentation, split details into feature/reference docs.

## docs/feature/INDEX.md Requirements

Classify modules by reading depth — not just list files:

- **Large modules** (subdir + INDEX + multi-file): link to `module/INDEX.md`
- **Medium modules** (README + sub-files): link to `module/README.md`
- **Small modules** (single file): link to `module/README.md`

Include agent routing: "先读本 INDEX.md 确定目标模块，再按需进入子目录。禁止全量读取。"

## Module Directory Requirements

Large module:

```text
docs/feature/<module>/
├── INDEX.md       # module map, always read before details
├── design.md      # detailed design
├── dataflow.md    # data flow / sequence / diagrams
├── changelog.md   # active changelog
├── taskBoard.md   # execution plan; default do not read
└── rca-*.md       # root-cause analysis when relevant
```

Module `INDEX.md` should route by task:
- Need high-level behavior → `README.md`
- Need implementation design → `design.md`
- Need data flow / sequence → `dataflow.md`
- Continuing execution work → `taskBoard.md`
- Debugging a known incident → matching `rca-*.md`

Medium: `README.md` + optional sub-docs. Small: single `README.md`.

## Large Proposal Decomposition

Design proposals (under `docs/feature/<module>/proposals/`) often carry three different audiences:

| Audience | What they want | What hurts them |
|----------|----------------|-----------------|
| Reviewer / decision-maker | "Why, big direction, key decisions, risks" | Drowning in schema details and SQL DDL |
| Implementer | "Full schema, DDL, pseudocode, integration points" | Hunting through high-level prose to find concrete spec |
| Progress tracker | "Task matrix, stage gates, week-by-week path" | Reading the entire proposal each time |

**Hard rule**: if a single proposal file grows to **≥ 500 lines**, decompose into a subfolder:

```text
docs/feature/<module>/proposals/<topic>/
├── README.md       # 30-50 lines — entry, routing, audience map
├── design.md       # 200-400 lines — why, direction, decisions, risks
├── spec.md         # 400-700 lines — schema, DDL, pseudocode, integration
└── acceptance.md   # 150-300 lines — task matrix, stage gates, path map
```

### Anti-pattern: "summary stacking"

Avoid revising a proposal by appending "v1 → v2 review feedback summary" + "T1-Tn task list" sections at the bottom while leaving the v1 body intact. This produces a Frankenstein document where:

- New schema fields are mentioned only in the summary
- Old schema is still in the body
- Reviewer cannot tell which is current

**Correct pattern** (after each review round):

1. `inline rewrite` the relevant section in `design.md` / `spec.md`
2. Archive the codex review to `docs/archive/<module>-reviews/`
3. Update `README.md` if audience routing changes

### Codex review archival

Once a review is consumed (findings inlined into design/spec), move the review file to `docs/archive/<module>-reviews/` with a versioned name (e.g. `review-<topic>-v1.md` → `review-<topic>-v2.md` → `review-<topic>-v3-synthesis.md`). Keep the top-of-file frontmatter pointing back to the **current authoritative** location, but preserve in-body line-number references to the version that was reviewed.

### Example

`docs/feature/ai-evaluation/proposals/oracle-batch-verdict/` (created 2026-05-14):
- v3 single-file was 995 lines, deemed "too much implementation spec for a proposal"
- decomposed into README (36) + design.md (286) + spec.md (614) + acceptance.md (202)
- 4 historical codex reviews moved to `docs/archive/ai-evaluation-reviews/review-oracle-batch-verdict-{v1,v2,v3-synthesis}.md`

## docs/reference/INDEX.md & docs/archive/INDEX.md

**Reference**: stable technical facts (architecture, interfaces, runbooks, external API). Not feature work logs.

**Archive**: completed plans, bugfix notes, RCA, old changelogs, deprecated proposals. Default: **do not read**. Only enter when task explicitly requires historical context.

Both must include agent routing instructions and forbid full reads.

## TaskBoard Rule

```text
README.md / INDEX.md explains what the module is.
taskBoard.md explains what was or will be executed.
Agents read taskBoard.md only when continuing implementation, supervising execution, validating task completion, or auditing task history.
```

If a task board grows beyond a few hundred lines, add a `Current status` section at the top and move old completed tasks to archive.

## Frontmatter Convention

For feature, archive, and RCA docs:

```yaml
---
type: feature | bugfix | rca | changelog | plan | reference | archive
scope: backend | frontend | fullstack | docs | ops
module: module-name
date: YYYY-MM-DD
status: active | implemented | deprecated | archived | draft
keywords: [short, searchable, terms]
read_by_default: false
---
```

- `OVERVIEW.md` and `INDEX.md` do not need frontmatter unless project already enforces it.
- Large detailed docs: `read_by_default: false`.
- Historical docs: `status: archived` or under `docs/archive/`.

## Migration Recipe

1. Inventory Markdown files excluding runtime/build directories.
2. Identify current entrypoints: `AGENTS.md`, `AGENTS.md`, `README.md`, `docs/OVERVIEW.md`.
3. Classify docs into: feature / reference / archive / task boards.
4. Create or update: `OVERVIEW.md`, `feature/INDEX.md`, `reference/INDEX.md`, `archive/INDEX.md`.
5. Move or link root-level stray docs into the right index.
6. Add the required reading rule to `AGENTS.md`.
7. Add module-level `INDEX.md` for large modules.
8. Mark large task boards and historical docs as not read by default.
9. Run a broken-link check.
10. Report new navigation path and remaining historical debt.

## Common Pitfalls

1. **Too much in `AGENTS.md`** — it should be rules and navigation, not full design.
2. **`OVERVIEW.md` becomes a giant manual** — overview is a map; move details down a layer.
3. **Indexes only list filenames** — indexes must explain when to read each file.
4. **`taskBoard.md` becomes default context** — load only for execution continuity.
5. **Old docs at root with no status** — archive or index clearly.
6. **No archive layer** — agents confuse historical plans with current requirements.
7. **No write-back rule** — if new modules don't require index updates, the map rots.

## Audit Checklist

- [ ] Agent can start from `AGENTS.md` and reach the right module without reading unrelated docs.
- [ ] `docs/OVERVIEW.md` has a clear module table and docs navigation table.
- [ ] `feature/INDEX.md` tells agents which module entrypoint to read.
- [ ] Large modules have module-local routing.
- [ ] Reference and archive docs are separated.
- [ ] Task boards are not default context.
- [ ] `禁止全量读取` or equivalent appears in agent-facing rules.
- [ ] No critical broken links in active docs.
- [ ] New docs write rules specify which indexes must be updated.
