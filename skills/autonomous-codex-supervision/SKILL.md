---
name: autonomous-codex-supervision
description: "Use when planning, launching, supervising, or integrating Codex/agent implementation work: tmux/cron supervisors, TaskNode task boards, Release-the-Hounds parallel worktrees, L1 full-auto project ownership, validation gates, bounded repair, and safe checkpointing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [codex, supervisor, tmux, cron, tasknode, taskboard, hounds, full-auto, worktrees, validation, integration]
    related_skills: [codex, writing-plans, requesting-code-review, subagent-driven-development]
---

# Autonomous Codex Supervision

## Overview

This is the umbrella skill for class-level Codex/agent implementation supervision. It covers the whole ladder from one supervised tmux Codex task to a project-level L1 owner that decomposes work into TaskNodes, releases parallel hounds in isolated worktrees, validates results, integrates accepted diffs, and safely checkpoints progress.

Use this skill instead of narrow one-session variants named around a specific supervisor mode, hound metaphor, TaskNode export, or global L1 run. Session-specific mechanics and historical variants live in `references/`; reusable scripts live in `scripts/`.

## When to Use

Load this skill when the user asks for any of these:

- run Codex until a task is actually complete;
- supervise Codex in tmux or cron;
- create semi-auto or full-auto implementation loops;
- decompose complex work into milestones / TaskNodes / taskBoard.md;
- run multiple Codex agents in parallel worktrees;
- "release the hounds";
- create a global L1 full-auto project owner;
- validate and integrate autonomous agent work;
- investigate a stuck supervisor, missing cron report, delivery gap, or incomplete hound output.

Do not use this skill for a quick one-off code edit that you can do directly with file/terminal tools.

## CRITICAL: Never Skip Task Spec

**Pitfall (2026-05-11):** Running `codex exec --full-auto "<prompt>"` without a structured task spec leads to Codex choosing the minimum-effort path (e.g., only modifying prompt/markdown files instead of implementing actual functionality). This happened with MAR-10 where Codex added 18 lines to a prompt file instead of implementing `group_by='trigger_status'` in Python.

**Mandatory before any Codex delegation:**
1. Write a task spec with explicit `acceptance` criteria (what "done" looks like, verifiable)
2. Include `validation_commands` (e.g., `make test`, specific curl calls)
3. Include `safety_rules` / constraints (e.g., "DO NOT only modify .md files")
4. After Codex completes, verify acceptance criteria — if not met, relaunch with focused repair prompt
5. Never present Codex output to user without first validating it yourself

## Umbrella Map

### 1. Single-task Codex supervisor

Use for one bounded implementation task. Build a task spec before launching:

```text
mode: semi-auto | full-auto
original_task: <user request>
normalized_goal: <concrete target>
workdir: <absolute repo path>
tmux_session: <session>
tmux_window: codex
max_rounds: 3
repo_map: <compact navigation context>
in_scope: []
out_of_scope: []
acceptance: []
validation_commands: []
safety_rules: []
stop_when: []
```

Semi-auto monitors, validates, reports, and stops. Full-auto may relaunch focused repair rounds until acceptance passes or a stop condition triggers.

### 2. TaskNode / taskBoard orchestration

Use when the task is too large for one Codex prompt. Create a milestone-gated task tree and save it in `taskBoard.md` as the execution source of truth.

TaskNodes should include: ID, title, milestone, parent, layer, status, dependencies, preconditions, input context, expected output, acceptance criteria, validation commands, safety rules, supervisor mode, max rounds, worktree, Codex session, and done evidence.

Status flow:

```text
planned → ready → running → validating → done
validating → repair_needed → running
running/validating → blocked | failed
```

Milestones are gates, not topic buckets. If a milestone contains a serial chain longer than two nodes, split it into foundation, parallel implementation, and integration milestones.

### 3. Release-the-Hounds parallel execution

Only release hounds after each target has a leash:

1. TaskNode is ready and dependency-satisfied.
2. Task package exists: spec, repo map, acceptance, validation, safety.
3. Each hound has an isolated worktree and branch.
4. Each hound has a unique tmux/Codex target and state file.
5. A bounded repair loop is attached.
6. Lucy/Hermes owns integration; Codex does not choose architecture or merge itself.

Use `.worktrees/<task-id>` and `feature/<task-id>` by default. Never stage `.worktrees/` into the main repo.

### 4. L1 global full-auto owner

Use only when the user has granted broad project-level authorization. L1 replaces the user for routine implementation decisions inside an approved plan, but remains bounded by that plan.

Allowed without repeated confirmation inside an approved plan:

- select the next ready TaskNode and keep advancing across all approved milestones, not just the first milestone;
- create worktrees and launch bounded hounds;
- run tests/typechecks/smokes and choose additional local validation needed to prove acceptance;
- perform local implementation review and merge readiness review with the highest project-authorized rigor;
- integrate safe completed work;
- update taskBoard/docs/current-status evidence;
- make safe local checkpoint commits;
- when explicitly authorized for highest-level L1 full-auto, continue from milestone to milestone through final validation and local merge review unless a stop condition fires.

Stop for owner decision when the task requires a new product lane, safety boundary change, secrets/private data access, destructive operation, unresolved strategy tradeoff, repeated validation failure, merge conflict requiring architecture choice, plan completion with only speculative follow-up remaining, or pushing/merging to a protected remote that the user has not explicitly included in the L1 authorization.

## Standard Harness Workflow

1. Inspect project rules and current git state.
2. Build or refresh repo map: purpose, stack, entrypoints, tests, docs/rules, task-relevant files, generated/runtime/secret-adjacent paths.
3. Write task spec or taskBoard before launch.
4. Create isolated worktree/branch if running parallel work.
5. **ATOMIC: Launch Codex + Create Cron Supervisor (不可分割)**
   This is ONE step. You are NOT done until BOTH sub-actions are complete. Do NOT verify launch, do NOT check output, do NOT respond to user between 5a and 5b.
   - **5a.** Write task spec to `/tmp/codex-taskspec-<timestamp>-<pid>.md`, then run `codex exec --full-auto - < /tmp/codex-taskspec-xxx.md 2>&1` with `background=true, notify_on_complete=true`. NEVER use `"$(cat ...)"` shell substitution.
   - **5b.** IMMEDIATELY (same tool-call batch or next sequential call, NO intervening user response) create a cron supervisor (every 5 min) that polls Codex status, runs validation on exit, and reports using the Reporting Template below.
   - **5c.** Only AFTER both 5a+5b are done, verify launch health (check output_preview).
   
   ⚠️ If you find yourself reporting "Codex launched" without having created the cron — STOP, go back, create it NOW. This failure has occurred 3+ times historically.
7. Monitor tmux/cron and process state.
7. On exit, collect `git status`, diff stat, pane output, validation output, static acceptance checks, and safety scan evidence.
8. Update acceptance booleans in persisted state.
9. If incomplete and safe, relaunch with a focused repair prompt only for failed criteria.
10. Integrate accepted work deliberately; preserve the union of accepted behavior when hounds touched the same files.
11. Run milestone-level validation and safety checks.
12. Update taskBoard Done Evidence and create a safe checkpoint commit.

## Pitfalls

### Bare `codex exec --full-auto` without task spec

Never run `codex exec --full-auto "do X"` without acceptance criteria. Codex will choose the minimum-effort path (e.g., editing a prompt file instead of implementing code). Always build a task spec first with `acceptance`, `validation_commands`, and `stop_when` fields.

### Codex hangs on "Reading additional input from stdin..." (stdin starvation)

**Root cause (2026-05-13):** When `codex exec --full-auto "$(cat TASK_SPEC.md)"` is run in a background process, Codex may attempt to read additional input from stdin. Background processes have no interactive stdin, so Codex blocks indefinitely — zero files changed, process alive but idle.

**Mandatory pattern — always use /tmp file + stdin redirect:**

```bash
# 1. Write spec to /tmp with unique name
SPEC_FILE="/tmp/codex-taskspec-$(date +%s)-$$.md"
cp TASK_SPEC.md "$SPEC_FILE"

# 2. Launch with explicit stdin redirect (prevents stdin starvation)
codex exec --full-auto - < "$SPEC_FILE" 2>&1
```

**NEVER do this:**
```bash
# BAD: shell substitution — Codex may still try to read stdin
codex exec --full-auto "$(cat TASK_SPEC.md)" 2>&1
```

**Why /tmp:** Task specs can be large (3KB+). Shell argument substitution has length limits and doesn't close stdin. Redirecting from a file guarantees Codex receives the full spec and sees EOF on stdin immediately.

### Codex does not `git add` new files

Codex creates new files but does NOT stage or commit them. After Codex exits, `git status` will show new files as `??` (untracked) while modified files show as `M`. The supervisor must `git add` new files explicitly before committing. Always run `git status --short` after Codex exits to catch untracked files.

### Cron supervisor `deliver: "origin"` thread affinity

`deliver: "origin"` sends reports to the **specific conversation thread** where the cron was created. If the user moves to a different thread/channel, they won't see reports. For long-running supervisors (>1 session), consider using a fixed delivery target (e.g., a dedicated Discord channel) instead of `origin`. Always do a manual `cronjob(action="run")` immediately after creation to verify the delivery path works.

### Forgetting to create cron supervisor after launch

This has happened multiple times. The skill's Standard Harness Workflow step 6 explicitly says "Create a cron supervisor" and marks it NOT optional. If you find yourself reporting "Codex launched, waiting for completion" without having created a cron job — stop, go back, create it. The user should never have to ask "where's my status update?"

### Problem → Fix → Prevent pattern (user mandate)

When the user raises any issue, do not stop at fixing the immediate problem. Always ask: "What mechanism prevents this from recurring?" Then take action (patch a skill, add a checklist step, update a rule). This is a persistent work habit, not a one-time instruction.

### Issue body for Symphony/Linear-driven Codex must be structured

When Codex is triggered via Linear issue (Symphony path), the issue body must follow the structured spec format:
- `## Problem Statement` (not hypothesis/suggestion)
- `## Acceptance Criteria` (verifiable conditions)
- `## Constraints` (include "DO NOT only modify prompt/skill markdown files")
- `## Baseline` (backtest metrics for comparison)
- NO `## Target Files` — Codex must self-locate

Without this structure, Codex picks the laziest path (proven by MAR-9/MAR-10 vs MAR-11 comparison).

### Symphony vs Hermes supervisor — different tools for different jobs

Do NOT unify these into one path:
- **Symphony** (Linear → Docker → Codex → PR): for unattended automated optimization. Has Section C Review Gate.
- **Hermes supervisor** (user says "do X" → local codex exec → Hermes reviews): for attended iterative development. Faster feedback loop.

Both share the same quality standard (task spec + acceptance criteria + validation), just different execution environments.

## Supporting Scripts

This umbrella carries reusable scripts under `scripts/`:

- `generate_repo_map.py` — create compact repo navigation context. If it fails, fix the script rather than silently falling back; the known-good version defines `SECRET_NAME_RE` as a normal `re.compile(...)` and must pass `python -m py_compile`.
- `launch_codex_round.py` — build/launch a round prompt from spec + repo map + state.
- `supervisor_validate.py` — collect validation/static-check evidence and update supervisor state.

Example:

```bash
python ~/.hermes/skills/autonomous-ai-agents/autonomous-codex-supervision/scripts/generate_repo_map.py \
  /absolute/path/to/project --task "<normalized task>" --json
```

## Cron Supervisor Rules

Cron prompts must be self-contained. Include workdir, state paths, task spec, validation commands, safety rules, reporting language, delivery target, and `self_job_id` when known.

For L1 / full-auto Codex supervision, **tmux alone is not sufficient**. Before reporting that L1 supervision is active, ensure all four pieces exist: saved task spec, isolated worktree + tmux Codex, persisted supervisor state, and a cron job that monitors, validates, and launches bounded repair rounds. See `references/l1-cron-supervisor-checklist.md`.

After creating or updating a cron supervisor, inspect `next_run_at` and trigger one manual `cronjob(action="run")` to verify the schedule/prompt/delivery path. Prefer explicit cron expressions such as `*/5 * * * *` over natural-language schedules when the job must run in the near future; if `next_run_at` is unexpectedly far away, patch the schedule immediately.

For chat-bound supervisor reports, explicitly require a non-empty report every run unless the user asked for silent watchdog behavior. Do **not** let the agent append `[SILENT]` after a real report: Hermes cron injects a `[SILENT]` convention, and a final response that mixes useful content with `[SILENT]` can be suppressed by delivery. Add wording such as: “Every run must output a non-empty report; never include `[SILENT]`, even when there is no new progress.” After the first manual run, inspect the saved output under `~/.hermes/cron/output/<job_id>/` to confirm the response contains no accidental `[SILENT]` marker.

For self-pausing chat-bound supervisors, use a two-phase create/update so the returned `job_id` is injected into the prompt and state file. Prefer pausing completed chat-bound supervisors over removing them immediately, so final reports remain inspectable if platform delivery is swallowed.

Do not create recursively spawning cron trees. One authorized master owns continuation; mirrors, if any, are read-only.

## Validation Discipline

Tests passing are not enough. Verify the original acceptance criteria:

- required files/functions/endpoints/UI fields exist;
- slow operations are asynchronous when requested;
- frontend proxy and direct backend behavior match where relevant;
- no placeholders remain where real implementation was required;
- no secrets or runtime files were copied into tracked diffs;
- project-specific safety boundaries remain intact.

## Reporting Template

**Mandatory:** Every cron supervisor prompt MUST embed this template verbatim as the required output format. Do not create cron supervisors with free-form reporting — the template ensures consistent, parseable status updates.

```text
主人，supervisor 状态：
- 范围：<single task | TaskNode wave | L1 plan>
- 当前阶段：<TaskNode or milestone>
- Codex/hounds：<running/exited/done/blocked counts>
- Validation：<pass/fail/not run + key evidence>
- Acceptance：<complete/incomplete/blocked>
- Safety：<clean/issue>
- Next action：<wait / repair / integrate / stop for decision>
```

When creating a cron supervisor (step 6 of Standard Harness Workflow), copy this template into the cron prompt's "输出格式" section and instruct the cron agent to strictly follow it.

## References

Historical narrow skills absorbed into this umbrella are preserved as support files:

- `references/codex-supervisor-cron-modes.md`
- `references/release-the-hounds.md`
- `references/tasknode-supervisor.md`
- `references/global-release-the-hounds.md`
- `references/codex-post-exit-checklist.md`

Use those references for detailed legacy wording, examples, TradingSignal defaults, delivery-reliability notes, and tool-agnostic export instructions.
