---
name: tasknode-supervisor
description: "Supervisor-orchestrated top-down TaskNode development SOP for milestone-gated task trees, taskBoard.md orchestration, isolated full-auto Codex supervisors, and verified milestone gates."
version: 1.0.0
author: Lucy
license: MIT
metadata:
  hermes:
    tags: [TaskNode, supervisor, Codex, taskboard, orchestration, full-auto, milestones]
    related_skills: [codex, codex-supervisor-cron-modes, writing-plans, subagent-driven-development, test-driven-development]
---

# TaskNode Supervisor Development SOP

Use this skill when the user asks to turn a complex feature or project into a top-down task tree, taskBoard, milestone plan, or when they ask Lucy to orchestrate multiple full-auto Codex supervisors in parallel.

This is an upper-layer development SOP above `codex-supervisor-cron-modes`. Codex remains the execution worker. The supervisor harness monitors each worker. Lucy remains the planner, dispatcher, integrator, and safety gate.

## Core Idea

Do not send one large vague task to Codex.

Instead:

1. Design the work as a top-down TaskNode tree.
2. Group nodes into milestone gates where same-milestone tasks are mostly parallelizable.
3. Save the execution graph in `taskBoard.md` as the source of truth.
4. At each execution wave, select only same-layer, same-milestone, dependency-satisfied ready tasks.
5. For each selected task, generate a task-specific spec, codemap, acceptance checklist, validation commands, safety rules, and isolated worktree.
6. Dispatch each task to a full-auto Codex supervisor.
7. Verify each task independently.
8. Merge completed task worktrees through a milestone integration gate.
9. Advance to the next milestone only when the previous milestone is fully implemented, verified, and integrated.

## Naming

Preferred short name: **TaskNode Supervisor**.

Full concept name: **Supervisor-Orchestrated Top-Down TaskNode Development**.

Use the short name in file names, skill names, and user-facing summaries unless the full concept name is helpful for clarity.

## Roles

### Planner / Architect — Lucy

Responsibilities:
- interpret the product/engineering goal;
- inspect existing code/docs before planning;
- design milestones and TaskNode hierarchy;
- identify parallel boundaries;
- redesign milestones when serial chains appear;
- define safety boundaries and non-goals;
- produce implementation plan and `taskBoard.md`.

### Dispatcher — Lucy

Responsibilities:
- read `taskBoard.md` before every execution wave;
- select current milestone, same-layer, dependency-satisfied `ready` tasks;
- generate task package for each selected TaskNode;
- create isolated git worktree / task branch;
- create or launch the full-auto supervisor;
- avoid dispatching tasks whose dependencies or product decisions are unresolved.

### Supervisor — cron/harness

Responsibilities:
- monitor Codex in tmux;
- collect diffs, logs, and status;
- run validation commands;
- update explicit acceptance booleans;
- relaunch bounded focused repair rounds when safe;
- stop on completion, max rounds, no progress, safety violation, or missing product decision;
- report concise evidence back to origin.

### Integrator / Reviewer — Lucy

Responsibilities:
- independently spot-check completed TaskNodes;
- merge worktrees through a milestone integration branch/worktree;
- resolve or route conflicts;
- run milestone-level validation;
- verify safety boundaries and docs/schema consistency;
- update `taskBoard.md` milestone gate state;
- decide whether to advance to the next milestone.

Codex is never the final architecture authority.

## TaskNode Model

Every executable unit should be represented as a TaskNode.

Recommended fields:

```markdown
## TaskNode: M1-T03

**Title:** <short descriptive name>

**Milestone:** M1 - <milestone name>

**Parent:** <parent TaskNode or epic>

**Layer:** <0 for epic, 1 for milestone-level tasks, 2+ for expanded children>

**Status:** planned | ready | running | validating | repair_needed | done | blocked | failed | abandoned

**Depends On:**
- M1-T01
- M1-T02

**Preconditions:**
- <conditions that must be true before dispatch>

**Input Context:**
- `<exact/path>` — why relevant

**Expected Output:**
- <concrete output artifacts or behavior>

**Acceptance Criteria:**
- [ ] <explicit checkable criterion>
- [ ] <explicit checkable criterion>

**Validation Commands:**
- `<command>`

**Safety Rules:**
- <do-not-cross boundary>

**Supervisor Mode:** full-auto

**Max Rounds:** 3

**Worktree:** `.worktrees/<task-id>`

**Codex Session:** `<project>-<task-id>`

**Done Evidence:**
- <test result, diff summary, acceptance state path, etc.>
```

## Status Flow

Normal path:

```text
planned → ready → running → validating → done
```

Repair / exception paths:

```text
running → blocked
running → failed
validating → repair_needed → running
blocked → ready
failed → abandoned | redesigned
```

Parent state is derived from children:

```text
all children done        → parent done
any child blocked        → parent blocked
any child running        → parent in_progress
dependencies incomplete  → parent pending
```

## Milestone Design Rules

Milestones are phase gates, not topic buckets.

A milestone should represent a wave of work that is mostly parallelizable after its preconditions are met.

### Parallelism Rule

If one milestone contains a serial chain longer than two nodes, redesign the milestone.

Bad:

```text
Milestone 2
├── A
│   └── B depends on A
│       └── C depends on B
```

Better:

```text
Milestone 2A: Contract / Foundation
└── A

Milestone 2B: Parallel Implementation
├── B1
├── B2
└── B3

Milestone 2C: Integration Gate
└── C
```

If two or more tasks inside a milestone must be done serially, consider extracting the upstream dependency into an earlier contract/foundation milestone.

### Stage Gate Rule

Do not advance to milestone N+1 until milestone N has:
- all required TaskNodes `done`;
- independent task validation evidence;
- integrated diffs/worktrees;
- milestone-level validation passing;
- safety scan clean;
- taskBoard updated with final evidence.

## taskBoard.md Requirements

`taskBoard.md` is the execution source of truth. It is not a loose TODO list.

Recommended location:

```text
docs/feature/<feature-name>/taskBoard.md
```

or, for internal agent work:

```text
.hermes/plans/<feature-name>-taskBoard.md
```

It should include:

1. Feature goal and non-goals.
2. Safety boundaries.
3. Milestone list and stage-gate criteria.
4. TaskNode tree.
5. Current execution pointer:
   - active milestone;
   - active layer;
   - ready tasks;
   - blocked tasks;
   - completed evidence.
6. Integration gate checklist.
7. Supervisor state file locations.
8. Validation commands.

Before dispatching Codex, read and update taskBoard state. Do not rely on chat memory.

## Tool-Agnostic Harness Plan Export

Use this section when the user asks to turn an existing TaskNode/taskBoard/SOP into a general engineering plan document for humans or external teams, especially when they ask to remove Hermes/Codex/cron/supervisor runtime details.

Class trigger examples:
- “整理一份 harness-engineering-plan-task.md”
- “把当前里程碑和 task 设计浓缩成文档”
- “去掉 Hermes 监管 / cron / Codex 细节，只保留工程方法”
- “make this TaskNode plan tool-agnostic”

Export workflow:
1. Read the controlling taskBoard and implementation plan docs first.
2. Preserve the reusable engineering structure: milestones, TaskNode fields, dependency rules, release-wave selection, stage gates, validation evidence, safety/non-goals, and integration checklist.
3. Remove runtime-specific implementation details: Hermes, cron jobs, Discord/Telegram delivery, Codex command lines, tmux sessions, worktree paths tied to one machine, supervisor state files, and persona language.
4. Generalize project-specific names into reusable patterns where possible, but keep one concrete example roadmap if it teaches the pattern.
5. Keep the document self-contained: explain purpose, principles, TaskNode model, status flow, milestone template, example roadmap, generic taskBoard structure, integration gate checklist, safety template, evidence template, and design review questions.
6. Write to the exact path requested by the user. If they ask to “send” the document, include it as a media/file attachment after writing and verifying it.
7. Do not commit the document unless the user explicitly asks for a checkpoint commit.

A good exported harness plan should read like a reusable engineering method, not like an agent operations log. It should be safe to hand to a non-Hermes engineer and still preserve the milestone/task design lessons.

## Execution Wave Selection

Each wave selects tasks by this filter:

```text
status == ready
AND milestone == active_milestone
AND layer == active_layer
AND all dependencies done
AND preconditions true
AND no product decision missing
```

Dispatch all selected tasks in parallel unless:
- they modify the same high-conflict files and no isolation strategy exists;
- the expected outputs conflict;
- a safety boundary requires sequential review;
- the user explicitly asks for sequential mode.

## Isolated Worktree Rule

Parallel full-auto Codex tasks must not share the same dirty working directory.

Default pattern:

```text
<repo>/.worktrees/<task-id>
```

Before creating worktrees, check whether `.worktrees/` is ignored or intentionally excluded from commits:

```bash
git check-ignore -v .worktrees/ 2>/dev/null || true
git status --short
```

If `.worktrees/` is not ignored, either add it to `.gitignore` as a safe local-agent runtime directory or explicitly report that it will remain untracked. Never stage `.worktrees/` contents into the main repo; task diffs belong on task branches/worktrees and are integrated deliberately through the milestone gate.

Each TaskNode should get:
- a unique task branch;
- a unique worktree;
- a unique tmux session/window or target;
- a unique supervisor state file;
- a unique prompt/spec file.

Benefits:
- clean diffs;
- independent validation;
- safe discard on failure;
- conflict detection at integration time;
- reduced risk of one Codex overwriting another Codex's work.

## Task Package Before Dispatch

Before launching full-auto Codex, Lucy must create or derive a task package containing:

```text
mode: full-auto
original_task: <TaskNode title and source context>
normalized_goal: <clear implementation target>
workdir: <isolated worktree path>
tmux_session: <unique session>
tmux_window: codex
max_rounds: 3
repo_map: <task-specific codemap>
in_scope:
  - <files/modules allowed or expected>
out_of_scope:
  - <explicit non-goals>
preconditions:
  - <must already be true>
expected_outputs:
  - <artifacts/behavior>
acceptance:
  - <checkable criteria>
validation_commands:
  - <commands>
safety_rules:
  - <boundaries>
stop_when:
  - all acceptance criteria pass
  - max rounds reached
  - safety violation
  - no meaningful progress
  - missing product decision
```

Use `codex-supervisor-cron-modes` for the actual full-auto harness and its script-backed flow.

## Codemap Requirements

A codemap is not a full file dump. It is a navigation and boundary layer.

It should answer:
- what the project does;
- major subsystems and entrypoints;
- files relevant to this TaskNode;
- tests and validation commands;
- docs/specs that govern the task;
- generated/runtime/secret-adjacent files not to touch;
- known safety boundaries and previous design decisions.

Generate or refresh with the `codex-supervisor-cron-modes` repo map script when applicable:

```bash
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/generate_repo_map.py \
  /absolute/path/to/worktree \
  --task "<TaskNode normalized goal>" \
  --json
```

Then reduce it into the TaskSpec prompt so Codex starts with the correct map but still verifies live files before editing.

## Full-Auto Supervisor Loop

For each TaskNode:

```text
launch Codex round 1
  ↓
Codex exits
  ↓
collect git status / diff / pane logs
  ↓
run validation commands
  ↓
update acceptance booleans with evidence
  ↓
if complete:
  persist final report and pause chat-bound supervisor for inspectability
elif safe and max_rounds not reached:
  generate focused repair prompt for failed criteria only
  relaunch Codex
else:
  mark blocked or failed, persist final report, and pause for user/main-session decision
```

For Discord/Telegram/thread-delivered supervisors, prefer pausing the completed cron job rather than removing it immediately. The final report should also be written to a durable local path under the task state or cron output directory, so the main session can recover it if platform delivery is swallowed. Remove completed supervisor jobs only after the final report has been observed or when the user explicitly asks for cleanup.

Do not treat tests passing as sufficient when the TaskNode behavior is not implemented. Do not treat documentation conformity as sufficient when the code violates safety or acceptance.

## Milestone Integration Gate

After all ready tasks in a milestone are done, perform integration before moving on.

Checklist:

- [ ] all required TaskNodes are `done`;
- [ ] each TaskNode has validation evidence;
- [ ] no active Codex processes remain for the milestone;
- [ ] supervisor cron jobs are removed or paused;
- [ ] task branches/worktrees are clean except intended diffs;
- [ ] merge diffs into integration branch/worktree;
- [ ] resolve conflicts intentionally;
- [ ] run full milestone validation commands;
- [ ] scan for secrets and out-of-scope changes;
- [ ] verify docs/schema/API compatibility;
- [ ] update taskBoard with final evidence;
- [ ] advance active milestone only if all checks pass.

If integration fails, create a repair TaskNode or redesign the milestone. Do not continue to the next milestone with unresolved integration failures.

## Safety Rules

Always preserve project-specific safety boundaries.

For TradingSignal defaults:
- keep the system observe-only;
- do not add order execution, wallet access, private exchange trading calls, entry/exit/SL/TP execution instructions, or live trading permissions;
- do not leak API keys, tokens, passwords, connection strings, cookies, or private config;
- do not change Step2 Key Zone `snr_score` semantics when implementing Step3 confirmation;
- do not copy old external project directories wholesale into the repo;
- treat TA_5/dingdi/OFSignal/CVD/orderflow as Step3 confirmation inputs, not Step2 zone scoring inputs.

## When to Redesign Instead of Dispatch

Stop and redesign the taskBoard when:
- the active milestone contains a serial chain longer than two tasks;
- two parallel tasks must modify the same central contract without a prior contract milestone;
- acceptance criteria cannot be made checkable;
- Codex would need a product decision to proceed;
- safety boundaries are ambiguous;
- integration conflicts are predictable and severe;
- the taskBoard no longer matches the actual repository state.

## Reporting Format

Use concise reports:

```text
主人，TaskNode Supervisor 当前状态：
- Active milestone: M2 - <name>
- Ready wave: M2-T01, M2-T02, M2-T03
- Dispatched: <count>
- Done: <count>
- Blocked: <count + reason>
- Validation: <pass/fail summary>
- Safety: clean / issue found
- Next gate: <what must pass before next milestone>
```

## Minimal Workflow

1. Load this skill.
2. Load `writing-plans` for plan detail and `codex-supervisor-cron-modes` for execution harness details.
3. Inspect project context and controlling docs.
4. Create implementation plan and `taskBoard.md`.
5. Review milestone parallelism; redesign if needed.
6. Stop and ask/confirm if the user only requested planning.
7. When authorized to execute, select current ready wave from taskBoard.
8. Create worktrees and TaskSpecs.
9. Launch full-auto supervisors in parallel.
10. Validate and integrate milestone.
11. Update taskBoard and advance only after the gate passes.

## Golden Rule

Codex executes TaskNodes. Supervisors close task loops. Lucy owns orchestration, integration, and safety.