---
name: global-release-the-hounds
description: "L1 global full-auto implementation supervisor SOP: harness engineering philosophy, milestone + multi-stage TaskTree planning, multi-Codex parallel hounds, isolated worktrees, bounded repair, validation/integration gates, safe checkpoint commits, and owner-level autonomous project execution."
version: 1.0.0
author: Lucy
license: MIT
metadata:
  hermes:
    tags: [L1, global-supervisor, Codex, hounds, TaskTree, taskBoard, harness-engineering, full-auto, milestones, worktrees, integration]
    related_skills: [codex, codex-supervisor-cron-modes, release-the-hounds, tasknode-supervisor, writing-plans, requesting-code-review]
---

# Global Release the Hounds — L1 Full-Auto Implementation Supervisor

Use this skill when the user wants a **global full-auto Codex harness** that acts as the project-level implementation owner, not as a passive planner or per-lane confirmation bot.

This skill absorbs and composes three existing skills:

- `codex-supervisor-cron-modes` — single Codex/tmux/cron harness, repo map, TaskSpec, launch/validate scripts, bounded repair rounds.
- `release-the-hounds` — TaskNode / milestone / worktree / hounds / integration gate execution SOP.
- `tasknode-supervisor` — formal top-down TaskNode task tree, taskBoard.md, milestone gate, isolated full-auto supervisor model.

This skill adds the missing L1 rule:

> **L1 is the global implementation owner. After broad authorization, L1 replaces the user for routine implementation decisions. It should not ask for confirmation before every lane, milestone, or safe next step. It stops only for real blockers, safety boundary changes, credentials risk, unresolved product tradeoffs, destructive operations, or unrecoverable validation failure.**

## Core Philosophy — Harness Engineering

A real full-auto development harness is not “run Codex and hope.” It is a layered control system:

```text
Project intent
  → Milestone roadmap
  → Multi-stage TaskTree
  → taskBoard.md as source of truth
  → isolated TaskNode worktrees
  → bounded Codex hounds
  → supervisor validation loops
  → Lucy-owned integration gate
  → safe checkpoint commit
  → automatic next milestone/lane selection
```

The harness exists to make autonomous implementation **bounded, inspectable, recoverable, and safe**. Codex may write code. It does not choose project direction. The L1 supervisor chooses direction inside the standing authorization, dispatches bounded workers, verifies outcomes, integrates accepted diffs, and keeps moving.

## Trigger Conditions

Load this skill when the user says or implies:

- “全自动放狗”
- “全局管理”
- “L1 代替我推进/实施”
- “不要每次让我确认”
- “多 Codex 并行处理”
- “里程碑 + 多阶段 taskTree”
- “continuous/full-auto project supervisor”
- “Release the Hounds for the whole project”
- “项目级自动推进，只有 blocker 才问我”

Also load it when upgrading an existing feature-level supervisor into a project-level L1 owner.

## Roles

### L1 Global Implementation Owner — Lucy / Master Supervisor

Responsibilities:

- read project state, docs, taskBoards, supervisor state files, git status, active processes;
- infer the next safe lane/milestone/TaskNode from standing project goals;
- create or refresh milestone and TaskTree plans;
- choose ready waves without asking for routine confirmation;
- create isolated worktrees and branches;
- launch multiple Codex hounds in parallel when safe;
- monitor hounds and collect evidence;
- run validation and safety scans;
- perform Lucy-owned integration, not blind branch merging;
- update taskBoard.md and Done Evidence;
- create safe checkpoint commits excluding secrets/runtime artifacts;
- advance to the next milestone/lane automatically;
- stop only for real blocker conditions.

L1 is allowed to mutate the project when the user has granted global full-auto authorization.

### L2 Feature / Stage Supervisor

A scoped supervisor for one feature, stage, or milestone group. L1 may create/manage L2 specs or processes when it is the single authorized master. L2 owns a bounded feature scope but does not choose unrelated project direction.

### L3 Codex Hounds

Codex instances released against exact TaskNodes. They are fast execution workers, not project owners. Each hound must have a TaskNode ID, task spec, repo/codemap, isolated worktree/branch, acceptance criteria, validation commands, safety rules, max repair rounds, and done evidence path.

## Standing Authorization Model

When the user grants global full-auto authorization, L1 should treat the authorization as applying to routine project advancement.

Allowed without additional confirmation:

- docs/status cleanup within the currently approved plan;
- creating or refreshing public README/taskBoard files only when they are part of the approved initial plan;
- selecting the next TaskNode from the current approved taskBoard;
- creating isolated worktrees and branches for approved TaskNodes;
- launching bounded Codex hounds for approved TaskNodes;
- running tests/typechecks/smokes;
- integrating safe completed work for approved TaskNodes;
- updating docs/taskBoard/tests inside the approved scope;
- making safe local checkpoint commits;
- advancing to the next milestone only when that milestone already exists in the approved taskBoard.

Not allowed without additional owner approval:

- inventing new product lanes after the current plan ends;
- opening new feature directories or taskBoards from heuristic discovery alone;
- turning handoff recommendations into implementation work;
- expanding the milestone/task list beyond the approved taskBoard except to record blockers, validation evidence, and discovered issues.

Still requires stop and owner decision:

- product/strategy tradeoff not inferable from docs/taskBoard;
- safety boundary change;
- request to read/use/commit secrets, config, credentials, private DB/cache/logs;
- need for external account access, wallet/private key, exchange trading permission;
- destructive commands or irreversible operations;
- merge conflict requiring architecture choice;
- validation failure after bounded repair rounds;
- repeated no-progress loops;
- secret leak or prohibited trading capability detected.

Do not use “new lane” itself as a stop reason only when the lane is already part of the approved initial plan or the owner explicitly authorizes that next lane. Otherwise, end the current plan, record unresolved issues and handoff recommendations, report overall progress, and ask the owner before opening a new lane.

### Plan-Bounded Execution

L1 must be bounded by an explicit plan, not by open-ended heuristic development.

The normal flow is:

```text
approved plan
  → approved milestones
  → approved TaskNodes
  → execute/validate/integrate
  → end when the approved task list is complete
  → record discovered issues / recommendations
  → report overall progress and ask for owner decision on any next plan
```

The approved taskBoard is the execution boundary. L1 may reorder, parallelize, repair, and validate TaskNodes inside that boundary, but it must not keep generating new feature work just because it found an adjacent idea. Handoff recommendations are evidence for the owner; they are not automatic authorization to start a new lane.

At plan end, L1 should produce a closure report:

- completed milestones and TaskNodes;
- validation status;
- safety status;
- issues discovered but not fixed;
- recommended next lanes or decisions;
- whether the supervisor should pause pending owner direction.

### Owner-Initiated Stop / Takeover Closeout

When the owner says to stop the current stage, stop the supervisor, take over, close out, or report the full implementation state, do this immediately:

1. Pause the mutating L1 cron first so it cannot launch more hounds while the main session investigates.
2. Inspect live state without reading secrets: `git status --short`, recent commits, active tmux/Codex processes, worktrees, current taskBoard, and relevant durable cron output.
3. Identify whether any hound is still active. If none are active, do not release new hounds. If one is active, stop only after determining whether it has uncommitted useful work or needs a safe abort.
4. Convert any unauthorized or prematurely opened lane into a stopped/hand-off record instead of continuing it. Mark the feature index and taskBoard as `stopped`, `handoff`, `cancelled`, or `awaiting_owner` as appropriate.
5. Preserve useful already-integrated evidence, but do not finish planned future nodes unless the owner explicitly re-approves them.
6. Run only closeout validation/safety checks needed to verify the recorded state. Do not broaden validation into new feature work.
7. Make a safe closeout checkpoint commit when the closeout changes tracked docs/code, explicitly excluding configs, secrets, runtime files, `.hermes/`, and `.worktrees/`.
8. Report full implementation state: what was completed, what was stopped/cancelled, validation results, safety state, current git status, remaining untracked files, and what requires owner approval next.

L1 may create a new lane/taskBoard only if the owner explicitly approves that lane or if the lane was already named in the original authorized roadmap/taskBoard.

### Safe Next-Lane Selection

When a feature/lane completes, L1 may automatically select and open the next lane without asking the owner only when the next lane is already named in the approved plan/roadmap or the owner has explicitly granted that specific continuation, and all of these are true:

- there is owner-approved evidence for the lane in the repo or plan: an approved roadmap entry, approved `taskBoard.md`, explicitly authorized feature index item, or a user-approved continuation from a handoff recommendation;
- the lane is low-risk and inside the current safety envelope: docs-first, validation, contract audit, test inventory, cleanup, reality audit, or small contract hardening;
- the lane does not introduce product-facing trading behavior, new external account access, wallet/private-key use, order execution, deployment, destructive operations, or secret/runtime-data reads;
- the lane can be expressed as a bounded TaskTree with milestone gates, validation commands, and safe checkpoint commits;
- the owner has granted standing global implementation authorization.

Good automatic next-step examples inside an approved plan:

- reality-audit an approved feature whose README overstates implemented behavior;
- reconcile reference docs, API contracts, frontend shared types, and tests with live code when the taskBoard asks for that reconciliation;
- close validation/safety/handoff gaps surfaced by the current approved lane;
- advance from one approved milestone to the next approved milestone in the same taskBoard.

Do not automatically open a brand-new lane merely because a completed lane produced a recommendation. Record the recommendation in the closure report and ask the owner whether to approve it as the next plan.

Stop and ask the owner before starting a next lane when it requires a product/strategy choice, expands the safety boundary, productizes a reserved capability, adds new external integrations, changes runtime scheduling semantics, or moves from documentation/contract audit into substantial feature implementation not already implied by the repo evidence.

## Cron Topology

Default topology is **one mutating master plus optional read-only mirrors**.

```text
L1 master cron
  - the only mutating project owner
  - may launch Codex/tmux processes
  - may create worktrees and integrate
  - may commit safe checkpoints

Read-only mirror cron(s)
  - read L1 durable output
  - mirror to Telegram/Discord/etc.
  - never mutate project
  - never launch Codex
  - never create/update/remove master cron
```

Avoid multiple mutating master cron jobs in the same repo. Two masters cause split-brain integration and unsafe duplicate releases.

Cron jobs must be self-contained. Include language/reporting preference, workdir, state files, taskBoard paths, allowed actions, hard safety boundaries, validation commands, stop conditions, durable output requirements, and self job id when known.

Cron runs must not recursively create unmanaged cron trees. If one continuous master is authorized, it should own continuation inside its loop. If it creates any child process/hound, it must track it in state and keep integration ownership.

## Required State Files

Use project-local runtime state, normally under `.hermes/supervisor/` or another ignored supervisor directory.

Recommended files:

```text
.hermes/supervisor/<project>-l1-global.json
.hermes/supervisor/<feature>.repo_map.json
.hermes/supervisor/<feature>/<tasknode>.spec.json
.hermes/supervisor/<feature>/<tasknode>.state.json
.hermes/supervisor/<feature>/<tasknode>.prompt.txt
.hermes/supervisor/<feature>/integration-report.md
```

State must record self job id, current lane/feature, current milestone, ready wave, dispatched hounds, worktree paths and branches, active tmux sessions, validation evidence, acceptance booleans, safety scan results, integration status, checkpoint commits, and stop reason if blocked.

Do not rely on chat memory. Cron ticks are fresh sessions.

## TaskTree / taskBoard Requirements

Every feature/lane should have a `taskBoard.md` or equivalent execution board.

Minimum sections:

```text
Board State
Milestones
Global Done Conditions
Root TaskNode
TaskNodes by milestone
Ready Wave
Integration Gate
Completed Evidence
Blocked / Decisions Needed
```

TaskNode fields:

```markdown
## TaskNode: <ID>

**Title:** <short name>
**Milestone:** <M# - name>
**Parent:** <parent>
**Layer:** <0/1/2/...>
**Status:** planned | ready | running | validating | repair_needed | done | blocked | failed | abandoned
**Depends On:** <IDs>
**Preconditions:** <conditions>
**Input Context:** <exact files/docs>
**Expected Output:** <files/behavior>
**Acceptance Criteria:** <checkable list>
**Validation Commands:** <commands>
**Safety Rules:** <boundaries>
**Supervisor Mode:** full-auto
**Max Rounds:** 3
**Worktree:** `.worktrees/<task-id>`
**Codex Session:** `<project>-<task-id>`
**Done Evidence:** <filled after validation>
```

Status flow:

```text
planned → ready → running → validating → done
validating → repair_needed → running
running/validating → blocked | failed
```

Parent status is derived from children.

## Milestone Design

Milestones are gates, not topic buckets. A milestone should contain a same-layer ready wave that is mostly parallelizable. If a milestone contains a serial chain longer than two nodes, redesign it.

Recommended pattern:

```text
M0 - Planning / Docs Gate
M1 - Contract / Foundation
M2 - Parallel Implementation Inputs
M3 - Core Computation / Feature Logic
M4 - API / UI / Product Surface
M5 - Integration / Validation / Handoff
```

Do not advance to milestone N+1 until milestone N has required TaskNodes done, per-task validation evidence, no active hounds, accepted integration diff, full milestone validation passing, safety scan clean, taskBoard updated, and safe checkpoint commit made.

## Ready Wave Selection

On each L1 tick:

1. Read the current taskBoard.
2. Determine active milestone and active layer.
3. Select TaskNodes where:

```text
status == ready
AND milestone == active_milestone
AND layer == active_layer
AND dependencies done
AND preconditions true
AND no unresolved product/safety decision
```

4. Release all selected nodes in parallel unless they modify the same high-conflict central files, outputs are mutually exclusive, safety requires sequential review, or integration risk is high enough to justify a contract/foundation split.

## Worktree and Branch Rules

Each hound gets an isolated worktree and branch:

```text
.worktrees/<task-id>
feature/<task-id>
```

Before creating worktrees:

```bash
git check-ignore -v .worktrees/ 2>/dev/null || true
git status --short
git log -1 --oneline
```

Do not stage `.worktrees/` contents in the main repo. Integrate accepted diffs deliberately. Leave local configs/secrets/runtime files untracked and explicitly reported.

## Task Package Generation

For each hound, generate a task spec JSON:

```json
{
  "mode": "full-auto",
  "task_id": "M1-T01",
  "normalized_goal": "...",
  "workdir": "/abs/path/.worktrees/M1-T01",
  "tmux_session": "project-M1-T01",
  "tmux_window": "codex",
  "max_rounds": 3,
  "repo_map": "...",
  "in_scope": [],
  "out_of_scope": [],
  "preconditions": [],
  "expected_outputs": [],
  "acceptance": [],
  "validation_commands": [],
  "safety_rules": [],
  "stop_when": []
}
```

Generate repo maps with:

```bash
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/generate_repo_map.py \
  /absolute/path/to/worktree \
  --task "<normalized task>" \
  --json > .hermes/supervisor/<task-id>.repo_map.json
```

Launch hounds using the script-backed harness when possible:

```bash
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/launch_codex_round.py \
  --spec .hermes/supervisor/<task-id>.spec.json \
  --repo-map .hermes/supervisor/<task-id>.repo_map.json \
  --state .hermes/supervisor/<task-id>.state.json \
  --session <project-task-id> \
  --window codex \
  --execute
```

If launching manually through tmux, always quote prompt file content:

```bash
tmux send-keys -t <session>:codex 'codex exec --full-auto "$(cat /tmp/<task-id>.prompt.txt)"' C-m
```

Do not use unquoted command substitution; it breaks prompts into shell words.

## Bounded Repair Loop

For each TaskNode:

```text
launch round 1
  ↓
monitor until Codex exits
  ↓
collect git status, diff, pane logs
  ↓
run validation commands
  ↓
run static acceptance checks
  ↓
scan for secrets/out-of-scope/prohibited behavior
  ↓
update acceptance booleans
  ↓
if accepted: mark done
elif safe and rounds < max_rounds: relaunch focused repair
else: mark blocked/failed and report
```

Do not treat tests passing as sufficient. Validate task behavior against acceptance criteria.

## Integration Gate

After all ready wave TaskNodes are done:

1. Ensure no hound is still active for the milestone.
2. Inspect each worktree diff and validation evidence.
3. Merge or synthesize changes into main/integration branch deliberately.
4. For same-file hounds, preserve the union of accepted behavior, not the last writer.
5. Run milestone-level validation.
6. Run safety scan.
7. Update taskBoard Done Evidence.
8. Advance active milestone only if gate passes.
9. Commit safe checkpoint.

Safe checkpoint staging pattern:

```bash
git status --short
git check-ignore -v .env config.json auth.json data/ frontend/.next/ .worktrees/ .hermes/ 2>/dev/null || true
git add -u
git add <explicit-safe-new-files>
git diff --cached --stat
git diff --cached | grep '^+' | grep -iE '(api_key|secret|password|token|passwd)\s*=\s*["'"'][^"'"']{6,}["'"']' || true
git commit -m "<type(scope): message>"
```

Never blindly `git add -A` when local config/runtime files exist.

## Validation Defaults

For Python/FastAPI + frontend projects, default validation:

```bash
uv run python -m pytest tests/ -v
uv run python -m compileall src tests -q
```

If frontend changed:

```bash
cd frontend && npm run typecheck
```

Also run task-specific smoke/static checks based on acceptance criteria.

## Safety Defaults

Always adapt to project-specific safety boundaries. For TradingSignal-like projects:

- keep observe-only;
- no order execution;
- no wallet/private-key access;
- no private exchange trading calls;
- no entry/exit/SL/TP execution instructions;
- no live trading permission fields;
- do not leak API keys, tokens, passwords, cookies, connection strings, or private config;
- do not commit local config/runtime artifacts;
- do not change protected score semantics unless explicitly approved.

## L1 Tick Algorithm

Every L1 master cron tick should do:

1. Print timestamp.
2. Read global state file.
3. Inspect git status/log without reading secret files.
4. Inspect current taskBoard.
5. Inspect active tmux/Codex processes.
6. If hounds are running: report progress, capture pane summaries, do not interfere unless blocked.
7. If hounds exited: collect diff/evidence, run validation, update states, repair or integrate.
8. If no hounds active and milestone has ready wave: create worktrees/specs and release hounds.
9. If milestone gate is ready: integrate, validate, update taskBoard, commit safe checkpoint, advance milestone.
10. If feature done: close the current plan, record discovered issues and recommendations, report overall progress, and pause or ask for owner approval before opening any new lane unless that lane was already explicitly approved.
11. Stop only for real blocker conditions inside the approved plan, or for plan-completion handoff when no approved next lane remains.

## Reporting

Reports should be concise, visible, durable, and predictable. For L1 global supervisors, prefer a fixed three-section report so the owner can scan progress without parsing a free-form operations log.

Default concise Chinese L1 report template:

```text
主人，L1 汇报：

## 1. 当前的总体进度
- 当前阶段：<当前节点名称> - <当前里程碑名称>
- 阶段简述：<用一句话说明这个阶段主要在做什么>
- 总体状态：<running | validating | integrating | blocked | complete | awaiting_owner>
- 最新提交：<commit hash + message>
- 安全状态：<clean | issue>

## 2. 剩余 Task
- <里程碑1>：<里程碑描述> - <剩余 Task 数 / Task IDs>
- <里程碑N>：<里程碑描述> - <剩余 Task 数 / Task IDs>

## 3. 本轮完成的内容
- <关键动作/结果 1>
- <关键验证/commit/taskBoard 结果 2>

## 4. 下一步 / 问题记录
- 存在的问题：<如果没有写“无新增问题”>
- 推荐下一步：<如果当前 plan 未完成，写继续哪个 approved TaskNode；如果已完成，写等待主人批准新 plan>
- 下一步动作：<继续监控 / 验证 / 集成 / 结束并等待主人决策>
```

Current stage must use the format `<TaskNode title or current node name> - <Milestone name>`, not just `<Feature / Milestone>`. `阶段简述` should explain the purpose of the current stage in natural language. `剩余 Task` should summarize remaining approved tasks by milestone, using the milestone description plus remaining count or IDs. Do not list unapproved future lanes as remaining tasks.

Keep the report short. Do not expand into a full operations log unless there is a blocker, safety issue, failed validation, or the user explicitly asks for details.

If delivery reliability matters, include durable output path and self job id. Mirrors may output `[SILENT]` only when they are explicitly read-only and there is no new master output.

## Stop Conditions

Stop and ask the user only for:

- unresolved product/strategy decision;
- safety boundary change;
- credentials/secrets/private data access requirement;
- destructive/irreversible operation;
- repeated validation failure after max rounds;
- repeated no-progress loops;
- merge conflict requiring architecture choice;
- secret leak or prohibited capability detected;
- taskBoard/design ambiguity that cannot be resolved safely.

Do **not** stop simply because an approved milestone is ready, docs need cleanup inside the approved scope, safe tests need running, or a safe checkpoint commit is needed.

Do stop or pause for owner direction when the approved plan/taskBoard is complete and the only remaining work is a new lane, new feature, new taskBoard, or speculative follow-up that was merely recommended by the handoff.

## Minimal Setup Procedure

When installing this pattern into a project:

1. Load this skill, `codex-supervisor-cron-modes`, and `release-the-hounds` if detailed mechanics are needed.
2. Read project instructions (`AGENTS.md`, `CLAUDE.md`, docs index, runbook, interfaces).
3. Confirm standing authorization exists or obtain it once.
4. Create/refresh public taskBoard.md and roadmap.
5. Create global L1 state file.
6. Generate repo map.
7. Create exactly one mutating L1 master cron with a self-contained prompt.
8. Create optional read-only mirror cron(s) for visibility.
9. Let L1 run continuously; main session intervenes only for blocker review or policy updates.

## Golden Rule

One master holds the wheel. Many hounds can run. Every hound has a tag, a fence, a leash, and a vet check.

L1 owns the project. Codex bites TaskNodes. The harness decides when the bite is safe to keep.