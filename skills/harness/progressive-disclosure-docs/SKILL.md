---
name: progressive-disclosure-docs
description: >-
  Design, audit, or refactor project documentation so AI agents navigate by
  progressive disclosure: AGENTS.md/OVERVIEW.md as maps, feature/reference/archive
  indexes as routing layers, owning module documents loaded only on demand, and
  mutable mainline routes reported from macro status to implementation detail.
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
- Organizing large feature docs, current-state summaries, bugfix notes, RCA docs, API references, or historical plans.
- Migrating a project from scattered Markdown files into a navigable docs-first structure.

Do **not** use for general prose editing, API reference generation alone, or one-off README cleanup.

## Golden Navigation Skeleton

```text
AGENTS.md / CLAUDE.md
  ↓
docs/OVERVIEW.md
  ↓
docs/feature/INDEX.md   docs/reference/INDEX.md   docs/collaboration/INDEX.md   docs/archive/INDEX.md
  ↓                      ↓                         ↓                             ↓
docs/feature/<module>/   stable technical facts    external source records       historical evidence
  ↓
INDEX.md / README.md / requirements.md
  ↓
requirements.md / design.md / dataflow.md / changelog.md / RCA.md
```

`requirements.md` records expected product / business behavior and acceptance.
`README.md` / `INDEX.md` record current implemented state, module routing, API
inventory, and known gaps. Do not use a README as the only source of truth for
both requirements and current implementation once a feature has meaningful
business behavior.

**durable docs 与会话计划的分离**：

| 目录 | 职责 | 生命周期 |
|------|------|------|
| `docs/` | SSOT — 描述系统是什么、当前状态与稳定证据 | 长期维护 |
| 会话计划 | 当前轮次的临时顺序与检查项 | 不持久化为仓库控制面 |

Truth ownership must also be explicit:

| Truth type | Owner |
|---|---|
| Safety and authorization | `AGENTS.md` plus explicit user direction |
| Expected behavior and acceptance | owning `requirements.md` / frozen contract |
| Current implementation | current code |
| Validation and research evidence | immutable artifacts, ledgers, and gate reports |
| External problem/proposal provenance | `docs/collaboration/<case-id>/` source records and adoption map |
| Project current-mainline pointer | `docs/OVERVIEW.md` |
| Stable route topology | owning `development-plan.md` |
| Current route overlay and state summary | owning `README.md` |
| Child workstream detail | owning child GOAL; parent README keeps one-node roll-up |
| State-transition history | owning append-only `changelog.md` |
| Current-turn sequencing | session plan only |

Conflicts must be classified as contract, implementation, evidence, or stale-summary gaps. Never
silently rewrite one truth type from another.

Layer responsibilities:

| Level | File | Job |
|---|---|---|
| 0 | AGENTS.md / AGENTS.md | Stable agent contract. Short enough to always load. |
| 1 | docs/OVERVIEW.md | Project map and the single current-Feature pointer. |
| 2F | docs/feature/INDEX.md | Feature routing table: module categories and entrypoints. |
| 2R | docs/reference/INDEX.md | Stable facts: architecture, API references, contracts, runbooks. |
| 2C | docs/collaboration/INDEX.md | External-collaboration source records, version binding, and adoption routing. |
| 2A | docs/archive/INDEX.md | Historical material: completed plans, bugfix notes, RCA. Default: do not read. |
| 3 | docs/feature/\<module\>/INDEX.md | Module-level map or summary. |
| 4 | Detailed module docs | Requirements, design, data flow. Read only when task-relevant. |

## Required Agent Reading Rule

Include in `AGENTS.md` and `docs/OVERVIEW.md`:

```text
文档遵循渐进式披露（Progressive Disclosure），Agent 逐层深入、禁止全量读取：

Level 0: AGENTS.md / CLAUDE.md     → 项目开发规约与读取入口
Level 1: docs/OVERVIEW.md          → 项目是什么？有哪些模块？去哪里找？
Level 2F: feature/INDEX.md         → 功能模块索引，先选目标模块
Level 2R: reference/INDEX.md       → 架构 / API / 测试 / 运维等稳定参考
Level 2C: collaboration/INDEX.md   → 外部问题包、方案来源和内部采纳路由
Level 2A: archive/INDEX.md         → 已完成计划 / bugfix / RCA 归档，默认不读
Level 3: feature/<module>/INDEX.md → 大型模块内部导航
Level 4: 具体设计 / 数据流 / RCA，仅按需读取

Agent 读取规则：OVERVIEW → INDEX → 按需读 1-3 个相关文档。禁止全量读取 docs。
当前进度、阻塞和下一验证门由 owning GOAL/README 持久化。
外部 proposal 只能作为 provenance/recommendation；先转译到内部合同，再从 owning Feature 实施。
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
Route expected behavior / product acceptance to `requirements.md`; route current
implementation, API lists, current status, and known gaps to `README.md` /
`INDEX.md`.

## Module Directory Requirements

Large module:

```text
docs/feature/<module>/
├── INDEX.md       # module map, always read before details
├── README.md      # current implemented state, API inventory, known gaps
├── requirements.md # expected product/business behavior and acceptance
├── design.md      # detailed design
├── dataflow.md    # data flow / sequence / diagrams
├── changelog.md   # active changelog
└── rca-*.md       # root-cause analysis when relevant
```

Module `INDEX.md` should route by task:
- Need module map / reading order → `INDEX.md`
- Need expected behavior / product requirements / acceptance → `requirements.md`
- Need current implementation / API list / current state / known gaps → `README.md`
- Need implementation design → `design.md`
- Need data flow / sequence → `dataflow.md`
- Need completed work / pending work / blockers / next validation gate → owning `README.md` or GOAL
- Debugging a known incident → matching `rca-*.md`

Medium: `README.md` + `requirements.md` when business behavior or acceptance
matters + optional sub-docs. Small: single `README.md` unless requirements need
their own source of truth.

### Current-state schema

An active feature README must make independent state axes machine-readable and human-readable. Do
not concatenate role, lifecycle, milestone, implementation, model, evidence, and authorization into
one free-form status string. At minimum record:

- role;
- lifecycle;
- current milestone and milestone status;
- implementation status;
- evidence status;
- authorization boundary;
- last verified date;
- next validation gate;
- route version, semantic module/milestone names, human-readable route, focus nodes, parallel groups and joins;
- completed work, pending work, blockers, and evidence routes.

Upper-level indexes should route to the owner and may show a short role/lifecycle label, but must not
copy the full state snapshot.

### Mainline route and cognitive disclosure

Treat a changing mainline as a DAG overlay, not a free-form task list. An active Feature README owns
one machine-readable `MAINLINE-ROUTE` manifest plus one equivalent human route line. Its development
plan owns stable dependencies; child GOALs own local detail; the session plan owns temporary focus.

Normalize route changes as `A -> B`, `A || B`, `[A || B] -> J`, insert, pause, drop or replace. Keep
node IDs stable and machine-only; every node also has a semantic module/milestone name. Default
user-facing output is L0: goal, route, focus, blocker, next gate and authorization, expressed only
with those semantic names. Do not expose phase codes or shorthand IDs unless requested. Expand to
workstream L1 only on request; expose file/interface/test/artifact L2 only for implementation, audit
or blocker evidence.

Read and apply [`references/mainline-route-contract.md`](references/mainline-route-contract.md) when
creating, changing, validating or reporting an active route.

## Feature Granularity: One Feature, One Directory

Do not bury an independent feature as scattered leaf files under a big catch-all
category. A sub-topic must be **promoted to its own** `docs/feature/<feature>/`
(with its own README) when it hits **any** of:

- it has its own long-term goal or milestone roadmap (M0–Mn);
- it has its own data contract / interface / output artifact;
- it has an independent lifecycle (evolves and is accepted on its own);
- it has accumulated **≥ 3 leaf docs**, or a single leaf has grown **≥ 500 lines**.

"Related" or "reusable" is **not** a reason to nest it under a mega-category —
mirror the code-organization rule "ownership by domain first". An overgrown
category that hides several real features behind generic leaf names is an
anti-pattern: agents can no longer route to the right feature from the INDEX.

## New Feature Lifecycle

Use an explicit lifecycle rather than inventing free-form states:

```text
PROPOSED
  -> CONTRACT_FROZEN
  -> IMPLEMENTATION_ACTIVE
  -> VALIDATION_ACTIVE
  -> CLOSED_ACCEPTED | CLOSED_REJECTED | ABANDONED
```

Evidence status and authorization remain independent axes. Starting implementation, training,
holdout access, shadow, dry-run, or execution always requires whatever separate authorization the
project contract demands; a lifecycle transition never grants it implicitly.

For a new feature:

1. start from `assets/feature-template/`, then create
   `docs/feature/<feature>/README.md`, `requirements.md`, and `changelog.md`;
2. add `INDEX.md` when the feature is large or has multiple task routes;
3. register the entry in `docs/feature/INDEX.md` and `docs/OVERVIEW.md`;
4. freeze expected behavior, safety boundary, schema, validation matrix, stop rules, evidence
   outputs, module responsibilities, dependency direction, public interfaces, file-size budgets,
   reuse boundaries, and test ownership before implementation;
5. keep the README current-state snapshot and changelog transition history updated at every gate;
6. close or archive the feature without rewriting negative conclusions.

Before a feature enters `IMPLEMENTATION_ACTIVE`, its owning README or development plan must contain
an implementation module map. New or changed handwritten code files may not exceed 1000 physical
lines; 800 lines is an early decomposition warning. Split by cohesive responsibility and stable
interfaces, not by numbered `part` files. CLI, strategy, model, and runner entrypoints remain thin.
The repository-specific contract is `docs/reference/code-organization.md`. When an existing module
must be extracted or crosses the 800/1000-line gate, route implementation through the repo-local
`refactor-large-modules` skill instead of inventing a new decomposition workflow.

## Autonomous Docs Governance (hard rule)

Docs are part of the deliverable, not an afterthought. The agent maintains and
restructures docs **proactively**, without being told:

1. **Autonomous maintenance**: after a non-trivial code / contract / runbook
   change, in the same task update the owning feature README + `feature/INDEX.md`
   + `OVERVIEW.md` module table + back-links, plus owning `requirements.md` when
   expected behavior / acceptance changed, and affected `interfaces.md` /
   `runbook-testing.md`. "Code changed, docs untouched" is not an acceptable
   end state.
2. **Autonomous restructuring**: when reading or writing docs, if a sub-topic
   under a big category now meets the feature-granularity trigger above, the
   agent must proactively propose splitting it into an independent feature
   (confirm first per the project's interaction rule, then land it).
3. **Split without breaking links**: when splitting / migrating, preserve
   Top-Down reachability (add routes in the parent INDEX and OVERVIEW),
   Bottom-Up traceability (leaf parent back-links), and **migrate old paths
   instead of leaving them alongside the new ones**.

## SSOT Validation Gate（硬性判定）

`docs/` 存放的是 SSOT（Single Source of Truth），描述**系统是什么、应该如何运行**。执行过程文件、一次性分析、gap/diff 记录不属于 SSOT，严禁混入 `docs/`。

### 判定流程

对每个拟放入 `docs/feature/<module>/` 的文件，agent 必须按顺序回答以下问题。任何一个回答为"否"则该文件不属于 `docs/`：

| # | 判定问题 | SSOT（放入 docs/） | 非 SSOT（改放别处） |
|---|---------|-------------------|-------------------|
| 1 | 文件描述的是**稳定的系统知识**（功能是什么、数据流如何、接口契约、组件关系），还是**临时的执行上下文**（本轮顺序、临时检查项）？ | 稳定知识 → SSOT | 临时顺序 → 保留在会话计划中，不落仓库文件 |
| 2 | 功能实现**完成后**，这个文件是否仍然需要**长期维护**（随代码演进持续更新）？ | 是 → SSOT | 否（一次性分析/总结/批注）→ 不持久化；有历史价值时明确归档 |
| 3 | 文件属于**模块功能描述**还是**运行/测试/验证方式**？ | 模块功能 → `docs/feature/<module>/` | 运行/测试方式 → `docs/reference/runbook-testing.md` |
| 4 | 文件记录的是接口/字段/状态/枚举的**稳定契约**吗？ | 是 → SSOT，同步更新 `docs/reference/interfaces.md` | 否 → 属于不稳定草稿或执行上下文 |
| 5 | 文件描述的是**预期行为/验收条件**（requirements），还是**当前实现状态**（implementation），还是两者都不是？ | requirements → `requirements.md`；当前状态 → `README.md`/`INDEX.md` | 两者都不是 → 非 SSOT；临时内容不落盘，有历史价值时明确归档 |

### 典型非 SSOT 文件去向

| 文件类型 | 典型示例 | 正确去向 |
|----------|---------|---------|
| Gap analysis / 差异分析 | `agent-io-gap-analysis.md`（模块A与模块B的接口差异） | 稳定差异并入 owning requirements/README；临时内容不落盘 |
| 一次性总结/总结批注 | `agent-http-call-summary.md`（某次对接后的总结记录） | 关键内容并入 SSOT；仅有历史价值时明确归档 |
| 测试运行方式 | `test.md` 描述如何启动服务、运行 E2E | `docs/reference/runbook-testing.md` |
| 临时执行顺序 | 不含稳定结论的本轮步骤、检查项 | 会话计划；不创建仓库文件 |
| 中间 review 产物 | Codex review 原始输出、一次性 lint 报告 | `docs/archive/<module>-reviews/` |
| 临时设计草稿 | 未经评审的 schema 草稿 | 评审通过后按 SSOT 格式写入 doc，草稿废弃 |

### 目录自检（交叉校验）

每次创建或修改 `docs/feature/<module>/` 后，agent 必须对该目录执行一次自检：

1. 列出目录下所有 `.md` 文件
2. 对每个文件应用上述判定流程
3. 如果发现非 SSOT 文件，立即移出；临时内容不持久化，有历史价值时明确归档
4. 确认每个文件的 `> 上级：` 反链指向正确的父文档
5. 确认 `docs/feature/INDEX.md` 的路由表已同步更新（新增、迁移或删除均需同步）
6. 确认 `docs/OVERVIEW.md` 的模块表和反链无需增补

> **失败模式**：某个 feature 目录下出现 gap analysis、测试运行方式、一次性总结等非 SSOT 文件 → 说明上一步的 SSOT 判定被跳过，需要立即纠正。

### External collaboration exception

External problem packages and proposals are durable provenance records, not system SSOT. They may
live only under `docs/collaboration/<case-id>/`, never loose inside an owning Feature. Route creation,
proposal receipt, adoption, translation and closure through the repo-local
`external-collaboration-workflow` Skill; do not duplicate that workflow here.

- `problem-statement.md` is internally owned and versioned after issuance.
- `external-proposal.md` is externally owned; internal agents preserve the source and do not rewrite
  it into an internal design.
- `INDEX.md` records version binding and item-level `ACCEPTED` / `MODIFIED` / `REJECTED` / `DEFERRED`
  decisions, then links each accepted item to an internal SSOT target and validation evidence.
- No implementation starts from an external proposal. Accepted content is first translated into the
  owning requirements/design/development plan; progress remains in owning README/changelog/evidence.

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

## docs/reference/INDEX.md, docs/collaboration/INDEX.md & docs/archive/INDEX.md

**Reference**: stable technical facts (architecture, interfaces, runbooks, external API). Not feature work logs.

**Collaboration**: source records exchanged with external teams plus internal adoption routing. Not
requirements, implementation truth, authorization, or a parallel progress tracker.

**Archive**: completed plans, bugfix notes, RCA, old changelogs, deprecated proposals. Default: **do not read**. Only enter when task explicitly requires historical context.

Both must include agent routing instructions and forbid full reads.

## Durable Progress Rule

```text
README.md / INDEX.md explains what the module is, its current implemented state,
current API inventory, known gaps, completed work, pending work, blockers, the
next validation gate, and routing.
requirements.md explains expected product/business behavior and acceptance.
Stable evidence lives in owning docs or append-only artifacts. Transient
sequencing stays in the session planning surface and is not persisted as a
parallel control plane.
```

## Frontmatter Convention

For feature, archive, and RCA docs:

```yaml
---
type: feature | bugfix | rca | changelog | plan | reference | archive
scope: backend | frontend | fullstack | docs | ops
module: module-name
date: YYYY-MM-DD
status: active | implemented | deprecated | archived | draft
role: current-mainline | separate-planned | supporting | historical
lifecycle: proposed | contract_frozen | implementation_active | validation_active | closed_accepted | closed_rejected | abandoned
evidence_status: contract_only | source_record | engineering | discovery | validation | accepted | rejected
authorization: project-specific-boundary
last_verified: YYYY-MM-DD
next_gate: stable-gate-id
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
3. Classify docs into: requirements / feature current state / reference / archive.
4. Create or update: `OVERVIEW.md`, `feature/INDEX.md`, `reference/INDEX.md`,
   `collaboration/INDEX.md`, `archive/INDEX.md`.
5. Move or link root-level stray docs into the right index.
6. Add the required reading rule to `AGENTS.md`.
7. Add module-level `INDEX.md` for large modules.
8. Mark historical docs as not read by default.
9. Run a broken-link check.
10. Report new navigation path and remaining historical debt.

## Common Pitfalls

1. **Too much in `AGENTS.md`** — it should be rules and navigation, not full design.
2. **`OVERVIEW.md` becomes a giant manual** — overview is a map; move details down a layer.
3. **Indexes only list filenames** — indexes must explain when to read each file.
4. **Transient planning becomes repository SSOT** — keep temporary sequencing in the session and durable state in the owning README/GOAL.
5. **Old docs at root with no status** — archive or index clearly.
6. **No archive layer** — agents confuse historical plans with current requirements.
7. **No write-back rule** — if new modules don't require index updates, the map rots.
8. **Overgrown catch-all category** — an independent feature (own goal/milestones/contract, or ≥3 leaf docs) buried as leaf files under a mega-module; promote it to its own `docs/feature/<feature>/`.
9. **Code changed, docs untouched** — non-trivial code/contract change shipped without updating the owning feature README + INDEX + OVERVIEW + back-links.

## Audit Checklist

- [ ] Agent can start from `AGENTS.md` and reach the right module without reading unrelated docs.
- [ ] `docs/OVERVIEW.md` has a clear module table and docs navigation table.
- [ ] `feature/INDEX.md` tells agents which module entrypoint to read.
- [ ] Large modules have module-local routing.
- [ ] Reference and archive docs are separated.
- [ ] External collaboration cases preserve source ownership/version binding and translate accepted
      recommendations into internal SSOT before implementation.
- [ ] Current progress, blockers, and the next validation gate have one owning README/GOAL.
- [ ] The project has exactly one current-mainline Feature pointer in OVERVIEW.
- [ ] Each active Feature has one valid route manifest, stable internal node IDs, semantic user-facing names, an acyclic graph, explicit focus/parallel/join data, and one next gate.
- [ ] Default progress output stays at L0 and upper indexes do not duplicate route summaries.
- [ ] Active feature READMEs use independent state axes instead of composite lifecycle strings.
- [ ] Active features have an append-only milestone changelog.
- [ ] Before implementation, active features freeze module ownership, dependency direction, public interfaces, file budgets, reuse boundaries, and test ownership.
- [ ] New or changed handwritten code files are at most 1000 physical lines and files at 800 lines receive a decomposition review.
- [ ] Oversized or mixed-responsibility extraction is routed through `refactor-large-modules` with frozen invariants and a validation matrix.
- [ ] `禁止全量读取` or equivalent appears in agent-facing rules.
- [ ] No critical broken links in active docs.
- [ ] New docs write rules specify which indexes must be updated.
- [ ] Each independent feature (own goal/milestones/contract, or ≥3 leaf docs) has its own `docs/feature/<feature>/`, not buried under a catch-all category.
- [ ] Agent-facing rules require autonomous docs maintenance and proactive split of overgrown categories.
