---
name: harness-engineering-plan
description: >-
  Harness engineering planning skill. Decomposes software goals into milestones,
  TaskNodes, dependency-aware execution waves, stage gates, and validation evidence.
  Use when the user asks to plan a feature implementation, create a task breakdown,
  design milestones, create a TaskBoard, or structure a multi-step engineering effort.
---

# Harness Engineering Plan

Turn a vague software goal into a controlled execution system: explicit milestones, small TaskNodes, dependency-aware execution waves, stage gates, validation evidence, safety boundaries, and integration checkpoints.

The goal is to make execution boring and auditable. Every task has a target, every milestone has a gate, and every gate has evidence.

## Core Principles

### Milestones are gates, not topic buckets

A milestone represents a phase that can be validated independently. It is complete only when:

- all required TaskNodes are done with validation evidence;
- integrated behavior passes milestone-level validation;
- docs/contracts are updated;
- safety and non-goal boundaries are intact.

### Do not advance before the previous major stage is complete

The next stage starts only after the previous stage has passed its gate. Partial completion is not enough — this prevents downstream work from building on unstable contracts or undocumented assumptions.

### Tasks inside a milestone should be parallel where possible

A good milestone exposes parallel work. Serial chains longer than two tasks indicate the milestone is designed incorrectly.

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

When a wave of independent TaskNodes is ready and the user wants to parallelize implementation via subagents (each running in its own `git worktree`), use the canonical 8-section prompt structure in [templates.md §"Per-TaskNode Codex Subagent Prompt Template"](templates.md#per-tasknode-codex-subagent-prompt-template).

Two implementation paths are supported — same prompt structure, different dispatchers:

| Path | Dispatcher | Skill | When to use |
|---|---|---|---|
| Codex CLI | `codex` (gpt-5.5/high) | [templates.md §"Per-TaskNode Codex Subagent Prompt Template"](templates.md#per-tasknode-codex-subagent-prompt-template) | 关心 GPT 系列质量；轻量任务；与 sandbox 现有链路对齐 |
| Claude Code CLI headless | `claude --bare -p` (opus default) | [`../claude-headless-subagent/SKILL.md`](../claude-headless-subagent/SKILL.md) | 需预算硬上限 + 实时进度可观测 + JSON 审计；长任务；混合并行 wave |

Key requirements (apply to both paths):

- One subagent instance per TaskNode in its own `git worktree` (branch `feat/<task-id>-<slug>`)
- Two-file structure per wave: `_shared_context.md` + N × `<TASK_ID>.prompt.md`
- Each prompt must satisfy 8 canonical sections: forced reading, metadata, contract coordination, expected output, acceptance, validation, safety, workflow, done-file format
- Main orchestrator agent does **review + merge** sequentially after subagent completes
- Anti-rate-limit: stagger or cap concurrency (LLM API 429 is a real constraint for both)

A wave **can mix** Codex + Claude TaskNodes when the prompt files share the same 8-section structure. The default mode (single agent, single worktree, sequential TaskNodes) remains valid and lower-risk.

## Reference

- Task board structure, integration gate checklist, safety/non-goal template, validation evidence template, **Codex subagent prompt template**: [templates.md](templates.md)
