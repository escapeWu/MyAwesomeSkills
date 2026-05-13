---
name: release-the-hounds
description: "Dark-humor Codex orchestration SOP: release the hounds only after TaskNode planning, milestone gates, isolated worktrees, full-auto supervisors, validation loops, and Lucy-owned safety/integration gates are ready."
version: 1.0.0
author: Lucy
license: MIT
metadata:
  hermes:
    tags: [Codex, hounds, TaskNode, supervisor, taskboard, orchestration, full-auto, milestones]
    related_skills: [codex, codex-supervisor-cron-modes, writing-plans, subagent-driven-development, test-driven-development]
---

# Release the Hounds

Use this skill when the user asks Lucy to organize a complex feature into a top-down task tree, `taskBoard.md`, milestone plan, and multiple parallel full-auto Codex supervisors.

Dark-humor metaphor: **Codex instances are the hounds**. They are fast, useful, and not trusted to choose targets by themselves. Lucy does not simply open the cage. Lucy maps the target, leashes each hound to a specific TaskNode, gives each one a fenced worktree, watches the bite, checks the wound, and only then opens the next gate.

This is an upper-layer development SOP above `codex-supervisor-cron-modes`. Codex remains the execution worker. The supervisor harness monitors each worker. Lucy remains the planner, dispatcher, integrator, and safety gate.

## Core Rule

Do not release a hound at a vague feature.

Release only after:

1. the target is decomposed into a top-down TaskNode tree;
2. milestones are designed as mostly parallel execution waves;
3. `taskBoard.md` is written as the execution source of truth;
4. each selected TaskNode has dependencies satisfied;
5. each TaskNode has a task package: spec, codemap, inputs, outputs, acceptance, validation, and safety rules;
6. each hound gets its own isolated worktree / task branch;
7. a full-auto supervisor is attached with bounded repair rounds;
8. integration gates are defined before the next milestone can start.

## Naming

Preferred user-facing name: **Release the Hounds**.

Plain technical name: **TaskNode Supervisor**.

Original formal concept: **Supervisor-Orchestrated Top-Down TaskNode Development**.

Use **Release the Hounds** when the user wants the dark-humor phrasing. Use **TaskNode Supervisor** when writing formal docs for a team that should not see the joke.

## Roles

### Kennel Master / Planner — Lucy

Responsibilities:
- interpret the product/engineering goal;
- inspect existing code/docs before planning;
- design milestones and TaskNode hierarchy;
- identify parallel boundaries;
- redesign milestones when serial chains appear;
- define safety boundaries and non-goals;
- produce implementation plan and `taskBoard.md`.

### Handler / Dispatcher — Lucy

Responsibilities:
- read `taskBoard.md` before every release wave;
- select current milestone, same-layer, dependency-satisfied `ready` tasks;
- generate task package for each selected TaskNode;
- create isolated git worktree / task branch;
- create or launch the full-auto supervisor;
- avoid dispatching tasks whose dependencies or product decisions are unresolved.

### Leash / Supervisor — cron/harness

Responsibilities:
- monitor Codex in tmux;
- collect diffs, logs, and status;
- run validation commands;
- update explicit acceptance booleans;
- relaunch bounded focused repair rounds when safe;
- stop on completion, max rounds, no progress, safety violation, or missing product decision;
- report concise evidence back to origin.

### Vet / Integrator — Lucy

Responsibilities:
- independently spot-check completed TaskNodes;
- merge worktrees through a milestone integration branch/worktree;
- resolve or route conflicts;
- run milestone-level validation;
- verify safety boundaries and docs/schema consistency;
- update `taskBoard.md` milestone gate state;
- decide whether to advance to the next milestone.

Codex is never the final architecture authority. The hound bites only the target on the tag.

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

If two or more tasks inside a milestone must be done serially, extract the upstream dependency into an earlier contract/foundation milestone.

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

## Release Wave Selection

Each release wave selects tasks by this filter:

```text
status == ready
AND milestone == active_milestone
AND layer == active_layer
AND all dependencies done
AND preconditions true
AND no product decision missing
```

Release all selected hounds in parallel unless:
- they modify the same high-conflict files and no isolation strategy exists;
- the expected outputs conflict;
- a safety boundary requires sequential review;
- the user explicitly asks for sequential mode.

## Isolated Kennel / Worktree Rule

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

If `.worktrees/` is not ignored, either add it to `.gitignore` as a safe local-agent runtime directory or explicitly report that it will remain untracked. Never stage `.worktrees/` contents into the main repo; task diffs belong on the task branches/worktrees and are integrated deliberately through the milestone gate.

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

## Task Package Before Release

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

## Full-Auto Leash Loop

For each TaskNode:

```text
release Codex round 1
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
  mark task done
elif safe and max_rounds not reached:
  generate focused repair prompt for failed criteria only
  relaunch Codex
else:
  mark blocked or failed
```

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

### Same-file hound integration pattern

When parallel hounds intentionally touch the same logical module or test file, do **not** merge one branch over the others or accept the last writer as truth. Treat the worktrees as source candidates and perform a Lucy-owned synthesis:

1. Inspect each completed worktree's implementation and tests side by side; identify the public functions/classes, behavior covered, and any overlapping names.
2. Build an integrated version on the main/integration branch that preserves the union of accepted behavior, not the union of code blindly.
3. Create or update an integrated test file that combines the important assertions from each hound, including edge/degraded cases and safety non-goals.
4. Run the milestone targeted tests first, then full project validation (`pytest`, compile/typecheck as relevant).
5. Run a diff safety scan over both tracked and newly-created files; `git diff --stat` alone omits untracked files, so explicitly include safe new files in review.
6. Update `taskBoard.md`: mark the milestone and TaskNodes done, write Done Evidence, advance the active milestone only after validation passes.
7. Leave local configs/secrets/runtime files (for example `config.json`, `.env`, DBs, worktree runtime) untracked and explicitly report them as excluded.

This pattern is especially important for contract/foundation files, shared service modules, schema/types files, and consolidated test files.

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

## When to Redesign Instead of Release

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
主人，Release the Hounds 当前状态：
- Active milestone: M2 - <name>
- Ready pack: M2-T01, M2-T02, M2-T03
- Released: <count>
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
7. Before the first release wave, establish a clean baseline: use `requesting-code-review` checkpoint rules, stage tracked changes plus explicit safe new files, exclude local configs/secrets/runtime artifacts, run relevant validation, and commit or otherwise record the baseline. Do not treat intentionally untracked local config such as `config.json` as release-blocking if it is excluded and reported.
8. For a new plan-bounded L1/global supervisor, create `.hermes/supervisor/<task-id>.json`, `.hermes/supervisor/<task-id>.spec.json`, and a generated repo map before creating cron; use the two-phase cron pattern to inject `self_job_id`, then verify `tmux`, `codex`, JSON validity, `cronjob list`, and whether `last_run_at` is still null before claiming it has run. Supporting Shadow Oracle references:
    - `references/shadow-oracle-l1-supervisor.md` captures the original plan-bounded L1 supervisor setup pattern.
    - `references/shadow-oracle-m9-productization.md` captures the data-quality/report productization pattern and M9-T04 provider-coverage Codex launch checklist.
    - `references/shadow-oracle-data-quality-reporting.md` captures the Discord-report-not-log correction, data-quality labels, FRED DFII10/DGS10 CSV probe, provider explicit-unavailable states, and verification checklist.
9. When authorized to execute, select current ready wave from taskBoard.
10. Create worktrees and TaskSpecs from the clean baseline.
11. Release full-auto Codex supervisors in parallel.
12. Validate and integrate milestone.
13. Update taskBoard and advance only after the gate passes.

## Golden Rule

Do not open the cage until the target, leash, fence, vet check, and extraction route are ready.

Codex bites TaskNodes. Supervisors keep the leash tight. Lucy owns orchestration, integration, and safety.