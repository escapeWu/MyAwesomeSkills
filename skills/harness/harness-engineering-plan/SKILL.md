---
name: harness-engineering-plan
description: >-
  Harness engineering planning skill. Decomposes software goals into milestones,
  TaskNodes, dependency-aware execution waves, stage gates, and validation evidence.
  Use when the user asks to plan a feature implementation, create a task breakdown,
  design milestones, create a TaskBoard, structure a multi-step engineering effort,
  or dispatch independent TaskNodes to parallel implementation subagents
  (Cursor Task tool or codex CLI). This skill is mandatory before writing
  implementation code for any non-trivial multi-step / multi-file feature.
---

# Harness Engineering Plan

Turn a vague software goal into a controlled execution system: explicit milestones, small TaskNodes, dependency-aware execution waves, stage gates, validation evidence, safety boundaries, and integration checkpoints.

The goal is to make execution boring and auditable. Every task has a target, every milestone has a gate, and every gate has evidence.

## Core Principles

### Milestones are gates, not topic buckets

A milestone represents a phase that can be validated independently. It is complete only when:

- all required TaskNodes are done with validation evidence;
- integrated behavior passes milestone-level validation;
- safety and non-goal boundaries are intact.
- (After the final milestone) conclusions are distilled into `docs/` as SSOT.

### Do not advance before the previous major stage is complete

The next stage starts only after the previous stage has passed its gate. Partial completion is not enough — this prevents downstream work from building on unstable contracts or undocumented assumptions.

### Tasks inside a milestone should be parallel where possible

A good milestone exposes parallel work. Serial chains longer than two tasks indicate the milestone is designed incorrectly.

> **并行是执行形态，不只是规划形态。** 一个 wave 里 ready 且相互独立的 TaskNode，**默认派发给多个实施 agent 并行执行**（Cursor `Task` 工具 subagent 或 `codex` CLI），主 agent 做 orchestrator 负责 review + 合并，而不是自己把所有 TaskNode 单线程写完。详见本文件末尾 [§Dispatching TaskNodes to Parallel Subagents](#dispatching-tasknodes-to-parallel-subagents)。

Bad shape:

```text
M2
└── T01 → T02 → T03 → T04
```

Better shape — extract the shared contract into an earlier milestone:

```text
M2A - Contract/Foundation
└── T01

M2B - Parallel Implementation
├── T02
├── T03
└── T04

M2C - Integration Gate
└── T05
```

### Wave overview visualization must be top-down, not side-by-side columns

When drawing the wave dependency graph in a milestone's `tasks.md`, **always use a top-down vertical tree** with one wave per block, separated by a downward arrow `▼` indicating the wave gate. This format is robust to narrow terminal widths, Markdown preview rendering, and copy/paste into review comments.

Bad shape (multi-column ASCII):

```text
W0 (Contracts)              W1 (Implementation)             W2 (Gate)
─────────────────           ──────────────────              ──────────

M1-T1 ─┐
M1-T3 ─┼─►  M1-T5b ──────►  M1-T5c ──┐
M1-T4 ─┤                              ├─►  M1-T-Gate
M1-T6 ─┘                    M1-T9 ──┘
```

Side-by-side columns break visually below ~120 cols (Markdown preview, narrow editor split, mobile, Slack/Linear paste). Arrows and box lines wrap mid-row and become unreadable.

Good shape (top-down tree, one wave per block, downward gate arrow):

```text
W0 — Contracts (parallel)
├── M1-T1  build_verdict_core
├── M1-T3  summary_schema
├── M1-T4  plan_schema
├── M1-T6  sampling_tools
└── M1-T5a bdstate_schema
                ▼ (准入：W0 全部 done)
W1 — Implementation (parallel)
├── M1-T5b nodes_impl
├── M1-T5c routing_compile
├── M1-T9  verdict_dispatch
└── M1-T2  invariants_tests
                ▼ (准入：W1 全部 done)
W2 — Integration + Gate (serial)
├── M1-T5d entry_persistence
├── M1-T5e mermaid_export
├── M1-T7  cap_rules
├── M1-T10 antibias_unit_tests
└── M1-T-Gate E2E_mock_and_real
```

Properties:
- One wave per vertical block; each task on its own line → no width pressure.
- Tree connectors (`├──` / `└──`) + downward gate arrow (`▼`) convey "list within wave" + "wave-to-wave gate" without horizontal arrows.
- Stays readable down to ~50 cols; ports cleanly into GitHub/Linear/Slack.
- After the diagram, follow up with a `| Wave | TaskNodes | 并行度 | 准入 |` table for at-a-glance metadata.

If a wave's parallelism or dependency requires more detail (e.g., a single intra-wave fan-in), prefer expressing it in the per-TaskNode `Depends On` field rather than enriching the diagram with horizontal arrows.

### Board State 是北极星：长任务防目标漂移

上下文窗口易失且有限，taskBoard 持久。taskBoard 顶部 `## Board State`（Goal / Acceptance / Active Milestone / Active TaskNode / Core Rule）是整个任务的**北极星**与唯一事实来源。**目标存文件，不存脑子。**

- 每个 wave / session 开工前先 re-read `## Board State`，用一句话复述「主目标 + 当前在哪个 TaskNode」再动手；
- 上下文变长或被压缩(compaction)后，**以 taskBoard 恢复目标，不靠记忆**；
- 把 `Goal` + `Acceptance` 固定为 TodoWrite 第 0 项常驻锚点（始终可见、不删）；
- 每完成一个 TaskNode / wave，立即把 `Active TaskNode`、`Global Status` 与证据回写 taskBoard。

详见 [templates.md §"Board State 北极星 + Re-read 协议（防目标漂移）"](templates.md)。

### Contracts before implementation

Implementation tasks should not invent field names, schema names, lifecycle states, or safety semantics. A strong plan starts with:

- output contract → input contract → safety boundary → fixture/test matrix → interface documentation

Then implementation tasks run in parallel against stable names.

### Integration is its own gate

Parallel task outputs should not be merged by last-writer-wins. The integration gate must synthesize accepted behavior from all completed tasks, resolve conflicts intentionally, and run milestone-level validation.

### Tests are not enough unless they prove the contract

A passing test suite is necessary but not sufficient. The gate must verify:

- expected files, API/schema fields, and degradation behavior exist;
- safety non-goals are not violated;
- docs and runtime behavior agree.

## TaskNode Model

Every executable unit is represented as a TaskNode with these fields:

```markdown
## TaskNode: M2-T03

**Title:** Short descriptive name

**Milestone:** M2 - Input Adapters

**Parent:** Root feature or parent TaskNode

**Layer:** 1

**Status:** planned | ready | running | validating | repair_needed | done | blocked | failed | abandoned

**Depends On:**
- M1-T01
- M1-T02

**Preconditions:**
- Contract names are finalized.
- Required fixtures exist.

**Input Context:**
- `path/to/file.py` — why this file matters.
- `docs/path.md` — governing design or contract.

**Expected Output:**
- Concrete files, behavior, schema, API response, UI component, or docs.

**Acceptance Criteria:**
- [ ] Checkable condition 1.
- [ ] Checkable condition 2.

**Validation Commands:**
- `pytest tests/path/test_file.py -v`
- `python -m compileall src tests -q`

**Safety Rules / Non-Goals:**
- Do not change unrelated contracts.
- Do not introduce prohibited capabilities.

**Done Evidence:**
- Test result summary.
- Commit or diff summary.
- Any manual or smoke validation evidence.
```

## TaskNode Status Flow

Normal: `planned → ready → running → validating → done`

Repair: `validating → repair_needed → running → validating → done`

Exception: `running → blocked | failed`, `blocked → ready`, `failed → abandoned | redesigned`

Parent status derived from children:

| Children state | Parent status |
|---|---|
| all done | done |
| any blocked | blocked |
| any running | in_progress |
| dependencies incomplete | pending |

## Release Wave Selection

A release wave is the set of TaskNodes that can be executed together:

```text
status == ready
AND milestone == active_milestone
AND layer == active_layer
AND all dependencies are done
AND all preconditions are true
AND no product decision is missing
AND no safety boundary is ambiguous
```

Exclude from parallel execution when tasks:

- must edit the same high-conflict central file;
- have conflicting expected outputs;
- depend on unresolved product decisions;
- require sequential safety review.

## Milestone Design Template

Each milestone should include:

```markdown
# M2 - Input Adapters

**Purpose:** Normalize upstream data into a stable internal contract.

**Parallelism Expectation:** High after M1 contracts are complete.

**Milestone Gate:** All adapters pass unit tests, missing/stale data degrades safely, integrated output matches the input snapshot contract.

**TaskNodes:**
- M2-T01: Adapter A
- M2-T02: Adapter B
- M2-T03: Adapter C
- M2-T04: Aggregator / integration helper

**Gate Validation:**
- targeted adapter tests;
- integrated contract tests;
- compile/typecheck;
- safety scan;
- docs update check.
```

## Standard Milestone Roadmap

A typical feature follows this milestone sequence:

| Milestone | Purpose | Parallelism |
|---|---|---|
| M0 | Planning Gate — plan, task board, scope, safety boundaries | n/a |
| M1 | Contract Foundation — schemas, statuses, degradation, test matrix, docs | high |
| M2 | Input Adapters — normalize upstream data into stable contract | high |
| M3A | Evidence Scorers — independent, auditable evidence items | high |
| M3B | Resolver & Document Builder — combine evidence into decisions | medium |
| M4 | Product Surface Integration — pipeline, API, UI, notifications, docs | medium-high |
| M5 | Integration & Verification — final gate, full suite, smoke, safety scan | serial gate |

Not every feature uses all milestones. Adapt the shape — but keep the invariant: **contracts before implementation, integration as a first-class gate**.

For detailed milestone descriptions and example TaskNodes, see [templates.md](templates.md#milestone-roadmap-details).

## Using project-analysis in M0 / M1

Use `project-analysis` as the read-only evidence layer when M0 or M1 cannot confidently define TaskNodes from existing docs and code.

Trigger it before finalizing the task board when:

- existing docs do not reveal the relevant module boundary through `docs/OVERVIEW.md -> docs/feature/INDEX.md` or `docs/reference/INDEX.md`;
- the feature crosses multiple services, routers, workers, frontend surfaces, or external systems;
- TaskNode `Input Context` would otherwise contain guesses instead of concrete entry points and files;
- contract names, data shapes, sequence boundaries, or performance risks need analysis before implementation waves.

Expected handoff from `project-analysis`:

- a new or updated long-lived docs entry, reachable through the project docs indexes;
- Mermaid diagrams paired with ASCII/TUI previews when diagrams are produced;
- a **TaskNode-ready Context** section with `Entry Points`, `Relevant Files`, `Contracts / Data Shapes`, `Risks / Open Questions`, and `Validation Candidates`.

Then copy those facts into the TaskNode `Input Context`, `Acceptance Criteria`, and `Validation Commands`. Do not use `project-analysis` to replace the task board; it supplies evidence for the harness, while this skill owns milestones, waves, gates, and TaskNode shape.

## Minimal Execution Flow

```text
1. Write M0 plan and task board.
2. Complete M1 contracts before implementation.
3. Release independent M2 input tasks.
4. Integrate M2 and pass gate.
5. Release independent M3A scorer tasks.
6. Integrate M3A and pass gate.
7. Complete M3B resolver/document builder.
8. Integrate into product surfaces in M4.
9. Run M5 full verification.
10. Record final evidence and close the feature.
```

## TaskBoard Location & Lifecycle

**taskBoard is a temporary execution artifact, not a permanent doc.** It lives under this skill's own `tasks/` directory, separate from `docs/`.

### Directory Layout

```text
.agents/skills/harness/harness-engineering-plan/
├── SKILL.md
├── templates.md
└── tasks/                       ← temporary execution files (WIP)
    ├── <module>/
    │   └── taskBoard.md         ← active taskBoard
    └── archive/                 ← completed taskBoards
        └── <module>/
            └── taskBoard-<phase>.md
```

### Lifecycle Rule

```
1. 任务启动 → 生成 taskBoard 到 tasks/<module>/taskBoard.md
2. 执行中   → 在 tasks/ 下更新状态，不碰 docs/
3. 完成后   → taskBoard 移入 tasks/archive/
4. 然后     → 提炼结论更新 docs/feature/<module>/ 中的 SSOT
```

**Why**: taskBoard carries transient execution state (Status: planned→running→done, Evidence, wave gate status). Mixing it into `docs/` confuses WIP process with stable truth. `docs/` is SSOT — update it only after completion, not during execution.

**docs/** stays clean of taskBoards. After a feature ships, the stable conclusions (data model, design rationale, new API contracts) flow into `docs/feature/<module>/` and `docs/reference/`. The spent taskBoard lives in `tasks/archive/` for audit only.

## Design Review Questions

Before execution, review the plan:

1. Does every implementation task have a stable contract to target?
2. Are milestone gates explicit and testable?
3. Can tasks inside each milestone run in parallel?
4. If not, should the milestone be split?
5. Are safety boundaries written as hard non-goals?
6. Are validation commands known before implementation starts?
7. Are docs/API/schema updates included where needed?
8. Is integration handled as a first-class gate?
9. Is there a final smoke test proving runtime visibility?
10. Is there a clear stop condition for blocked/product-decision cases?

## Why This Works

This structure reduces ambiguity at every layer:

- milestones define phase gates;
- TaskNodes define executable units;
- dependencies define safe ordering;
- acceptance criteria define done;
- validation commands provide evidence;
- safety boundaries prevent scope creep;
- integration gates prevent parallel work from overwriting itself.

The result is an engineering harness: not just a plan, but a repeatable control structure for moving from vague intent to verified implementation.

## Dispatching TaskNodes to Parallel Subagents

> **默认行为，不是可选项**：当一个 wave 里有 **≥ 2 个相互独立、依赖已满足的 ready TaskNode** 时，默认把它们**并行派发给多个实施 agent**，而不是主 agent 自己单线程顺序写完。主 agent 的角色是 **orchestrator**（拆分 → 派发 → review → 合并 → 过 gate），不是唯一的 coder。

### 何时并行派发（触发条件）

满足以下全部即应并行派发：

- 当前 wave 有 ≥ 2 个 `status == ready` 且依赖已满足的 TaskNode；
- 这些 TaskNode 的 Expected Output 不写同一个高冲突中心文件；
- 契约（M1）已冻结，TaskNode 不需要互相发明字段；
- 没有未决的产品决策或安全边界歧义。

只有一个 ready TaskNode、或任务是单文件 trivial fix 时，单 agent 顺序执行即可（默认低风险路径仍然有效）。

### 两种执行器（按场景选）

同一套 8-section prompt 结构（见 [templates.md §"Per-TaskNode Codex Subagent Prompt Template"](templates.md#per-tasknode-codex-subagent-prompt-template)），两种派发器都支持，按运行环境与任务特征选：

| 执行器 | 怎么派发 | 适用场景 |
|---|---|---|
| **Cursor `Task` 工具 subagent** | 在**同一条消息**里发出多个 `Task` 调用（`subagent_type` 选 `generalPurpose` / `shell` / `best-of-n-runner`），每个 Task 携带一个 TaskNode 的完整 8-section prompt；可加 `run_in_background` | 在 Cursor IDE 内运行；要真正并行、低环境耦合——**首选** |
| **`codex` CLI** | 把 TaskNode spec 写到 `/tmp/codex-taskspec-*.md`，用 `codex exec --full-auto - < spec.md` 后台启动，主 agent 轮询 + 退出后校验 | 需要 GPT 系列质量、长任务、与已有 codex sandbox 链路对齐；进阶 cron/tmux 监督见 `autonomous-codex-supervision`（若你的 skills 库里已安装） |

一个 wave 可以**混用**两种执行器，只要每个 prompt 都满足同一套 8-section 结构。

### worktree 隔离（按需，不强制）

- **默认**：在当前工作区内并行/顺序实施即可，不必每个 TaskNode 都开 worktree。
- **触发 worktree**：当 ≥ 2 个并行 TaskNode 会改到**重叠文件**、或需要互不干扰的独立分支验证时，才给涉及的 TaskNode 各开一个 `git worktree`（branch `feat/<task-id>-<slug>`），合并仍由主 agent 串行处理。

### 所有路径都必须遵守

- 每个 subagent / Codex 实例只领 **一个 TaskNode**，prompt 自包含（8 段：forced reading + metadata + contract coordination + expected output + acceptance + validation + safety + workflow + done-file）；不假设它能看到主 agent 的对话历史；
- 每个 wave 两类文件：`_shared_context.md`（一份）+ N × `<TASK_ID>.prompt.md`；
- 主 orchestrator 在每个 subagent 完成后**串行 review + merge**，按"接受行为的并集"整合，**禁止 last-writer-wins 覆盖**；
- 防限流：LLM API 429 是真实约束，错峰启动或限并发（一次 2-3 个）；
- 全部合并完成后过 milestone integration gate（验证证据齐全）才进入下一个 wave。

### Codex CLI 派发的关键安全模式（仅当用执行器 2）

- **永远先写 task spec**（含 acceptance / validation_commands / safety_rules），禁止 `codex exec --full-auto "do X"` 裸跑——否则 Codex 会走最省力路径（只改 `.md` 不写真实实现）。
- **永远用 `/tmp` 文件 + stdin 重定向**：`codex exec --full-auto - < "$SPEC_FILE"`，禁止 `"$(cat spec.md)"`（会让后台进程 stdin 饿死、零文件改动假活）。
- Codex 退出后先 `git status --short` 捡未 `git add` 的新文件，主 agent 校验 acceptance 通过后再合并。

## Reference

- Task board structure, integration gate checklist, safety/non-goal template, validation evidence template, **Codex subagent prompt template**: [templates.md](templates.md)
