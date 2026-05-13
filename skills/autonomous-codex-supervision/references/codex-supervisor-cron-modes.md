---
name: codex-supervisor-cron-modes
description: Create semi-auto and full-auto cron supervisors for tmux/Codex long-running implementation tasks, including task clarification, acceptance criteria, validation, reporting, bounded retries, and safety stops.
version: 1.0.0
author: Lucy
license: MIT
metadata:
  hermes:
    tags: [Codex, tmux, cron, supervisor, automation, validation]
    related_skills: [codex]
---

# Codex Supervisor Cron Modes

Use this skill when the user asks to run or supervise a long-running Codex implementation task in tmux, especially when they mention semi-auto, full-auto, cron supervision, validation, acceptance criteria, or “run until actually done”.

The user should not have to write detailed acceptance criteria. The assistant is responsible for turning the user's possibly vague task into an executable task spec and verification plan. Ask targeted follow-up questions only when ambiguity materially changes implementation or validation.

## Core Principle

The user gives direction. Lucy turns it into a task specification, acceptance checklist, validation commands, safety boundaries, and cron supervision policy.

Never let full-auto mean “Codex loops forever”. Full-auto means bounded autonomous continuation until the original task is actually complete, or until a stop condition requires user/main-session decision.

## Modes

### semi-auto

Default safe mode.

Responsibilities:
1. Launch or monitor Codex in tmux.
2. Send periodic progress reports to the origin chat.
3. When Codex exits, run validation commands.
4. Report git diff summary, test results, failures, and suspected next steps.
5. Stop after reporting.

Semi-auto MUST NOT:
- auto-fix code;
- re-launch Codex;
- commit changes;
- decide the next implementation stage;
- continue development after validation failure.

Use semi-auto when the user wants control after each agent pass or when the task has uncertain scope.

### full-auto

Autonomous bounded completion mode.

Responsibilities:
1. Clarify/normalize the user's task into a concrete task spec.
2. Define acceptance criteria and validation commands before launch.
3. Launch Codex in tmux.
4. Monitor progress and report periodically.
5. When Codex exits, run validation.
6. Inspect whether the original task is actually complete, not merely whether tests pass.
7. If incomplete and safe, generate a focused follow-up Codex prompt and re-launch.
8. Repeat until acceptance criteria pass or a stop condition is hit.

Full-auto MUST have:
- max retry limit, default 3 Codex implementation rounds;
- clear done_when criteria;
- clear stop_when criteria;
- validation commands;
- safety constraints;
- origin delivery for reports.

## Clarification Workflow

When the user gives a vague task, first decide whether reasonable defaults are enough.

If the ambiguity is low-risk, state the assumed acceptance criteria and proceed. Example:

> 主人，我按 MVP 可运行标准处理：后端 API 可跑、测试通过、前端 typecheck 通过、核心页面能读到数据。不接交易执行，不处理部署。除非你反对，我就这样开 full-auto。

If the ambiguity materially changes what to build or how to validate, ask focused questions. Do not ask broad questions like “what exactly do you want?” Ask only what blocks the spec.

Good clarification questions:
- “这个‘跑起来’是指本地开发环境可运行，还是要部署到服务器？”
- “这个‘接入真实数据’是只接 K 线，还是 K 线 + LML 都要接？”
- “这个‘完成前端’是静态展示就够，还是要实时轮询 API？”

Proceed after enough information exists to write a useful done_when checklist.

## Required Task Spec Format

Before launching full-auto, create a compact spec containing:

```text
mode: semi-auto | full-auto
original_task: <user's original task>
normalized_goal: <Lucy’s clarified target>
workdir: <absolute project path>
tmux_session: <session name>
tmux_window: <window name, usually codex>
max_rounds: <default 3 for full-auto>

repo_map:
  source: <generated | existing docs | hybrid>
  include:
    - project purpose and architecture summary
    - entrypoints, services, frontend routes, backend APIs, tests, config boundaries
    - likely files/directories relevant to the task
    - owner hints from AGENTS.md / CLAUDE.md / docs when present
  exclude:
    - secrets, env files, caches, logs, generated artifacts, vendored dependencies

in_scope:
  - <modules/features to change>

out_of_scope:
  - <explicit non-goals>

acceptance:
  - <functional requirement 1>
  - <functional requirement 2>

validation_commands:
  - <test command>
  - <compile/typecheck command>
  - <smoke command if relevant>

safety_rules:
  - <no secrets>
  - <no dangerous operation>
  - <project-specific safety constraints>

stop_when:
  - all acceptance criteria pass
  - max rounds reached
  - secret leak detected
  - destructive/dangerous behavior detected
  - no meaningful progress across repeated rounds
  - missing product decision requires user input
```

## Repo Map Layer

A repo map is the compact navigation layer that tells an agent “where things live and how the project is shaped” without dumping the whole repository into context. It is not a file tree alone. It should combine structure, semantics, and task relevance.

Generate or refresh a repo map before launching a full-auto supervisor, and for semi-auto when the project is unfamiliar or the task spans multiple modules.

The repo map should answer:
1. What is this repository for?
2. What are the major subsystems and entrypoints?
3. Which files/directories are likely relevant to the current task?
4. Where are tests, fixtures, docs, generated files, configs, and unsafe/secrets-adjacent files?
5. What commands are canonical for validation?
6. What project rules are declared in AGENTS.md, CLAUDE.md, README, docs, or package/pyproject config?

Recommended generation approach:
- inspect `git status --short`, top-level files, README, AGENTS.md/CLAUDE.md, docs index, package manifests, pyproject, Makefile, docker compose files, frontend/backend entrypoints, and tests;
- use fast file listing/search, not full recursive content dumps;
- summarize large directories by purpose and a few representative files;
- explicitly mark generated/vendor/cache/runtime directories as “do not edit unless required”;
- include task-relevant candidate files discovered by keyword search;
- keep the map compact enough to paste into Codex prompts and cron prompts.

Supporting script:

```bash
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/generate_repo_map.py \
  /absolute/path/to/project \
  --task "<normalized task>" \
  --json
```

Use the script output as a starting repo map in the Codex prompt and supervisor cron prompt. Redact or remove anything sensitive if the script flags secret-adjacent paths. The script is dependency-free and intentionally avoids reading obvious secret-like files.

A good repo map format is:

```text
repo_map:
  purpose: <1-3 sentences>
  stack: <languages/frameworks/package managers>
  entrypoints:
    backend: <paths>
    frontend: <paths>
    cli/jobs: <paths>
  key_dirs:
    <path>: <purpose / edit guidance>
  tests:
    <path>: <test type and command>
  docs_and_rules:
    <path>: <important instruction>
  task_relevant_files:
    <path>: <why relevant>
  validation_commands:
    - <command>
  do_not_touch_without_reason:
    - <secrets/config/runtime/generated/vendor paths>
```

Supervisor prompts should pass the repo map to Codex as the starting navigation context, then instruct Codex to verify it against the live repository before editing. The map is a guide, not authority. If Codex finds drift, it should report the drift and use current files as source of truth.

## Standard tmux/Codex Launch Pattern

Use the `codex` skill's tmux guidance. Prefer writing long prompts to `/tmp/<project>_codex_prompt.txt`, then sending a shell command to tmux. Ensure the project is a git repo.

Prerequisite checks:

```bash
cd /path/to/project
[ -d .git ] || git init
command -v tmux
command -v codex
```

Create/reuse tmux session:

```bash
tmux has-session -t <session> 2>/dev/null || tmux new-session -d -s <session> -c /path/to/project
tmux rename-window -t <session>:0 codex || true
```

Launch Codex with a prompt file and `--full-auto` when file changes should be auto-approved inside the workspace.

## Supervisor Cron Design

Cron sessions are independent assistant sessions, not the current main chat's continuous consciousness. Therefore cron prompts MUST be self-contained.

Set `deliver="origin"` so status reports return to the current thread unless the user requested a different target.

Toolset rule: if the supervisor prompt instructs the cron run to manage its own lifecycle (`cronjob list/update/run/pause/remove`) or to recover/replay delivery state, the cron job's `enabled_toolsets` MUST include `cronjob` in addition to `terminal`/`file`. A common failure mode is creating a supervisor with only `["terminal", "file"]`: the Codex task can complete and the state file can say `complete`, but the cron-run session cannot actually call `cronjob(action="pause")`, leaving the job scheduled and forcing the main chat to pause it manually. For chat-bound supervisors that should self-pause on completion, create/update them with `enabled_toolsets=["terminal", "file", "cronjob"]`.

Language and visibility preferences must be explicit inside every cron prompt. Cron runs do not reliably inherit the main chat's persona/language habits. If the user wants Chinese reports, dual-channel updates, or a specific address style, write that directly into both the master supervisor prompt and any read-only mirror prompt. A good pattern is: final responses must be Chinese, address the user as `主人`, keep technical identifiers such as `job_id`, file paths, commands, commit hashes, and API field names unchanged when useful, and produce a non-empty report unless the mirror is explicitly allowed to return `[SILENT]` when there is no new master output.

Delivery reliability pitfall: `cronjob list` may show `last_status=ok` and `last_delivery_error=null` even when the user did not actually see the Discord/Telegram report. Treat delivery metadata as necessary but not sufficient. For any user complaint like “the cron did not report” or “why no update?”, verify all three layers before concluding:
1. scheduler state: `cronjob list` for `last_run_at`, `next_run_at`, `last_status`, `last_delivery_error`, `deliver`, and `origin`;
2. durable output: inspect `~/.hermes/cron/output/<job_id>/` for the latest markdown run files and read the `## Response` tail;
3. live task state: inspect the project supervisor state file, tmux/Codex process, git status/log, and relevant worktree state.
If local output exists but the user did not see it, report it as a delivery visibility gap, replay the latest local report in the main chat, and keep the supervisor running unless there is a real blocker. Do not assume `[SILENT]` unless the output file explicitly contains it. Continuous supervisors should include the durable output path and job_id in reports when delivery reliability is being investigated.

If `cronjob list` shows a newly created or manually triggered job as `enabled=true` / `state=scheduled` but `last_run_at=null` and `~/.hermes/cron/output/<job_id>/` is empty, do **not** claim the cron has run or that only delivery failed. Treat it as a scheduler/runner execution gap: the job exists, but no run evidence has landed yet. `cronjob(action="run")` may update `next_run_at` or enqueue work without immediately producing `last_run_at`/output, so verify again after the scheduled tick. For visibility-critical supervisors, update the prompt to require a non-empty final report every run (job_id, timestamp, inspected state, action/no-op reason, next step, safety) instead of allowing an empty response; mirrors may still use `[SILENT]` only when explicitly read-only and no new master report exists.

Dual-channel delivery preference: if the user explicitly says not to create a new cron, do **not** create a separate Telegram mirror cron. Keep a single master supervisor. Short-term supported configuration on this Hermes build: set the same supervisor cron's `deliver` string to a comma-separated target list, usually `origin,telegram`, and keep `enabled_toolsets=["terminal", "file", "cronjob"]` for supervisors that must self-pause/update. The scheduler resolves comma-separated `deliver` via `_resolve_delivery_targets()`, deduplicates concrete targets, and `_deliver_result()` sends the same final cron response to each resolved platform. This avoids a second mirror cron while preserving one mutating supervisor.

Recommended create/update shape for TradingSignal supervisors:
```python
cronjob(
  action="create" or "update",
  deliver="origin,telegram",
  enabled_toolsets=["terminal", "file", "cronjob"],
  # ... same schedule/prompt/workdir/skills as usual
)
```

Operational notes:
- `origin` preserves the Discord thread/topic captured when the job was created; `telegram` resolves to the configured Telegram home channel.
- If a target needs an explicit destination, use comma-separated refs such as `origin,telegram:<chat_id>`.
- Do not use `send_message` from inside cron just for mirroring; cron-run final response delivery should handle both channels.
- Check `last_delivery_error` plus durable output when a platform appears silent. Current scheduler records delivery error as one combined string, not a per-target status, so partial-failure observability is weaker than a future first-class `deliver_targets` list.
- If the running Hermes gateway/scheduler predates comma-separated delivery support, restart/update Hermes before relying on this pattern; otherwise report the limitation instead of creating a mirror cron.

Legacy mirror pattern: only when the user explicitly allows a second cron, keep exactly one mutating master supervisor and create a separate read-only mirror cron with `deliver` set to the backup channel. The mirror cron should only read the master job's durable output directory and project supervisor state, remember the last mirrored output filename in a small state file, and emit `[SILENT]` when there is no new master report. It must never launch Codex, modify project source, run integration, commit, pause/remove the master, or create additional cron jobs. This gives visibility redundancy without duplicate execution.

Supervisor design should be treated as a harness, not only a timer. The cron prompt and persisted state should carry these layers:
- task spec and acceptance checklist;
- repo map / navigation context;
- execution state: current round, active tmux target, last pane digest, last meaningful diff stat;
- validation state: command results plus explicit acceptance booleans;
- safety state: secret scan result, destructive command warnings, out-of-scope file changes;
- decision state: continue / wait / focused retry / stop for user decision.

For full-auto, persist a compact state file under the project, for example `.hermes/supervisor/<task-id>.json`, and optionally write a small human-readable run log next to it. The state file must be the source of truth between cron ticks; do not rely on chat memory. When a round exits, update acceptance booleans with evidence, then decide whether to relaunch Codex with a focused repair prompt.

A stronger full-auto loop is:
1. generate/refresh repo map before round 1;
2. launch Codex with task spec + repo map + safety rules;
3. monitor tmux and report progress;
4. on exit, collect git status/diff/pane output;
5. run validation commands;
6. run static acceptance checks for expected files/endpoints/UI fields when tests are insufficient;
7. scan diff/logs for secrets and out-of-scope changes;
8. update persisted acceptance booleans;
9. if incomplete and safe, relaunch with a narrow prompt containing only failed criteria and evidence;
10. stop when accepted, blocked, unsafe, repeated no-progress, or max rounds reached.

### Script-backed execution workflow

For new supervisors, prefer this script-backed harness flow instead of making every cron prompt improvise from natural language:

```bash
# 1) Generate repo map once before round 1, refresh if the repo structure changes materially.
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/generate_repo_map.py \
  /absolute/path/to/project \
  --task "<normalized task>" \
  --json > /absolute/path/to/project/.hermes/supervisor/<task-id>.repo_map.json

# 2) Launch a Codex round from task spec + repo map + persisted state.
# Omit --execute for dry-run prompt generation.
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/launch_codex_round.py \
  --spec /absolute/path/to/project/.hermes/supervisor/<task-id>.spec.json \
  --repo-map /absolute/path/to/project/.hermes/supervisor/<task-id>.repo_map.json \
  --state /absolute/path/to/project/.hermes/supervisor/<task-id>.json \
  --session <tmux-session> \
  --window codex \
  --execute

# 3) After Codex exits, collect evidence and update acceptance state.
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/supervisor_validate.py \
  --workdir /absolute/path/to/project \
  --state /absolute/path/to/project/.hermes/supervisor/<task-id>.json \
  --validation "<test/typecheck command>"
```

The task spec JSON should contain the same fields as the Required Task Spec Format: `mode`, `original_task`, `normalized_goal`, `workdir`, `tmux_session`, `tmux_window`, `in_scope`, `out_of_scope`, `acceptance`, `validation_commands`, `safety_rules`, and `stop_when`.

`launch_codex_round.py` creates a round prompt from the spec, repo map, and previous validation state. Round 1 gets the full task. Later rounds get a focused repair prompt containing only failed/uncertain acceptance booleans and evidence excerpts. It runs in dry-run mode unless `--execute` is passed, refuses to run outside a git repository, and refuses to launch if another Codex process appears active unless `--allow-if-codex-running` is explicitly set.

For a deliberate parallel wave with isolated worktrees and unique tmux sessions, pass `--allow-if-codex-running` after verifying the selected tasks are dependency-satisfied and do not share a dirty workdir. Without this flag, the second and later hounds in the same release wave may fail to launch because the script's global Codex process guard sees the first running Codex instance. Do not use the flag to pile multiple Codex processes into one shared worktree/session.

Pitfall fixed: when launching Codex through tmux, the prompt file content must be quoted (`codex exec --full-auto "$(cat prompt.txt)"`). Unquoted command substitution splits the prompt into shell words and Codex fails with errors such as `unexpected argument 'are' found`. If you see that error, relaunch with the current `launch_codex_round.py` or a manually quoted prompt file command.

Supporting validation script:

```bash
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/supervisor_validate.py \
  --workdir /absolute/path/to/project \
  --state /absolute/path/to/project/.hermes/supervisor/<task-id>.json \
  --validation "uv run python -m pytest tests/ -v" \
  --validation "uv run python -m compileall src tests -q"
```

Optional static checks can be passed as a JSON list, for example:

```bash
python /Users/shancw/.hermes/skills/autonomous-ai-agents/codex-supervisor-cron-modes/scripts/supervisor_validate.py \
  --workdir /absolute/path/to/project \
  --state /absolute/path/to/project/.hermes/supervisor/<task-id>.json \
  --validation "npm run typecheck" \
  --static-checks-json '[{"name":"task polling","path":"frontend/src/api/tasks.ts","patterns":["/api/pipeline/tasks","task_id"]}]'
```

The script updates the state file with validation evidence, static check results, secret-like diff findings, and acceptance booleans. Treat it as evidence collection; the supervisor still decides whether the original task is truly complete.

### Two-phase cron creation for self-stop

Cron jobs do not reliably know their own `job_id` at creation time because `cronjob(action="create")` returns the ID only after the prompt has already been saved. Never guess job IDs.

For any semi-auto or full-auto supervisor that should stop itself, use this two-phase pattern:

1. Create the cron job with a temporary prompt containing a unique `supervisor_name`, `task_id`, and state path.
2. Read the returned `job_id` from the create result.
3. Immediately call `cronjob(action="update", job_id=<returned_id>, prompt=<full prompt>)` to inject:
   - `self_job_id: <returned_id>`;
   - the task spec;
   - validation commands;
   - stop/remove instructions;
   - the persisted state path.
4. Also write `self_job_id` into the persisted supervisor state file.

Completion behavior:

```text
if acceptance passes or a terminal stop condition occurs:
  1. write final state: complete / blocked / failed
  2. write the final report to a durable local output path under .hermes/supervisor/ or the cron output directory
  3. deliver final report to origin
  4. prefer cronjob pause self_job_id with a completion reason for chat-bound supervisors, so the job remains inspectable if delivery is swallowed
  5. remove self_job_id only after the final report has been observed in chat or when the user explicitly prefers cleanup over retention
```

Default retention rule:
- For Discord/Telegram/thread-delivered Codex supervisors, prefer `pause` on completion, not `remove`, unless the user explicitly asked for removal. This prevents a completed monitor from disappearing when the final delivery is lost or hidden by the platform.
- The final report must include the durable local output path and the `self_job_id`, so the main session can recover it with `cronjob list`, `cronjob run`, or by reading the output file.
- If the supervisor does remove itself, it must first persist a compact final report beside the task state and state why removal was chosen.

Prefer `remove` only for short-lived local-only supervisors or after an explicit cleanup step. Prefer `pause` for chat-bound supervisors where delivery reliability matters.

If a legacy supervisor lacks `self_job_id`, it may use `cronjob(action="list")` and match by exact unique job name plus workdir, but this is a fallback. It must not remove anything if more than one candidate matches.

For semi-auto jobs, include the supervisor `job_id` in the prompt when known. After Codex exits and final validation/reporting is complete, the supervisor should remove or pause its own cron job if it can do so safely; otherwise it must explicitly report that the job can be removed. This prevents completed monitors from continuing to send stale reports.

For full-auto jobs, persist minimal supervisor state outside the chat context (for example `.hermes/supervisor/<task-id>.json` under the project or another explicitly chosen local state path). Record current round, max rounds, last validation result, acceptance status, last focused repair prompt, stop reason, and `self_job_id`. Cron runs are fresh sessions, so full-auto must not rely on memory of prior ticks.

### semi-auto supervisor prompt requirements

The prompt must include:
- workdir;
- tmux target;
- original task summary;
- validation commands;
- safety rules;
- instruction to monitor and report;
- instruction to validate on Codex exit;
- instruction NOT to modify files or re-launch Codex;
- instruction to stop/report after validation.

### Continuous TaskBoard Full-Auto Mode

When the user explicitly authorizes cron-based autonomous advancement (for example, they say they do not want to keep saying “continue”), use a persistent master supervisor cron instead of a semi-auto stop-after-report loop.

Continuous mode responsibilities:
- keep reading the project `taskBoard.md` and persisted supervisor state on every tick;
- if no Codex is running and the active milestone has ready dependency-satisfied TaskNodes, create/refresh isolated worktrees and launch the next bounded Codex wave;
- if Codex is running, monitor and report progress periodically;
- after a wave exits, validate each worktree, run focused repair rounds when safe, then perform Lucy-owned integration gate on the main/integration branch;
- run milestone-level validation, safety scans, docs/taskBoard updates, and a safe checkpoint commit that explicitly excludes local configs/secrets/runtime artifacts;
- advance to the next milestone automatically when the gate passes;
- stop or pause only for a real blocker: missing product decision, repeated no-progress/max rounds, validation failure that cannot be safely repaired, merge conflict requiring architecture choice, secret/safety violation, or destructive/dangerous behavior.

Continuous mode must still be bounded per TaskNode/wave (`max_rounds`, default 3) and must not create new cron jobs from inside cron runs. The single originally authorized master cron owns continuation. It may launch tmux/Codex processes, create worktrees, run validation, integrate, commit safe checkpoints, and update its own state file. Chat-bound continuous supervisors should pause, not remove, when all taskBoard milestones are complete or when blocked, so final state remains inspectable.

## Validation Discipline

Validation must check both command results and task completeness.

Always check:
1. Codex process/tmux state.
2. `git status --short`.
3. `git diff --stat`.
4. Relevant diffs for safety and actual implementation.
5. Test/compile/typecheck output.
6. Whether placeholder code remains when the task required real implementation.
7. Whether secrets were copied, printed, or committed.
8. Whether prohibited capabilities were added.
9. Whether implementation still conforms to the controlling design/spec docs (for example `docs/framework.md`, `docs/reference/interfaces.md`, `AGENTS.md`, or an implementation plan). If the code intentionally improves or supersedes the plan, report the drift and recommend updating the docs instead of forcing the code back to an outdated design.

Do not treat tests passing as sufficient if the original task asked for behavior that is not implemented. Do not treat documentation conformity as a blind rule: distinguish harmful drift from intentional design evolution that needs a documentation patch.

### Full-auto acceptance verification pattern

For full-auto runs, write acceptance as explicit booleans in the persisted supervisor state and update them only after checking evidence. Example:

```json
{
  "status": "complete",
  "acceptance": {
    "feature_visible": true,
    "create_flow": true,
    "update_flow": true,
    "audit_detail": true,
    "server_filters": true,
    "typecheck_pass": true,
    "pytest_pass": true,
    "compileall_pass": true,
    "safety_clean": true
  },
  "last_validation": {
    "pytest": "pass: 10 passed",
    "compileall": "pass",
    "frontend_typecheck": "pass"
  },
  "stop_reason": "acceptance criteria passed"
}
```

When the feature is a frontend/UI integration over existing backend APIs, combine command validation with static implementation checks. Search the relevant frontend files for API endpoints, required fields, and UI components from the acceptance checklist. For example, verify that table/detail views expose identifiers and audit fields (`task_id`, `run_id`, `trigger_source`, `stage_order`, `input`, `output`), and that filter pages send query params to the server rather than only filtering client-side.

When the task is to make a long-running backend operation non-blocking (for example, “do not wait; return a taskID; query logs/stages by taskID”), write acceptance around the asynchronous contract rather than only around final success:
- the trigger endpoint returns quickly (usually under 3–5 seconds) before the underlying work completes, with a stable `task_id` and, when applicable, `run_id`;
- status/detail endpoints by `task_id` expose queued/running/terminal status, current or last completed stage, timestamps, and audit identifiers;
- log endpoints by `task_id` expose live/persisted logs and stage records with secret redaction;
- existing synchronous/detail endpoints remain backward compatible unless explicitly deprecated;
- validation includes a smoke test through the same frontend/proxy path that previously timed out or hung, not only direct backend calls;
- tests simulate a slow underlying worker so they prove the trigger returns before completion and that polling shows running → terminal state.

After a full-auto supervisor reports completion, the main session should independently spot-check:
- no Codex process remains;
- persisted supervisor state says `status=complete` with all required booleans true;
- validation commands still pass;
- representative files contain the expected integration points;
- safety scans only show fake test secrets, not real credentials;
- the cron job has been removed or paused.

## Default Stop Conditions

Full-auto stops when any of these is true:
- all acceptance criteria pass;
- max rounds reached, default 3;
- consecutive rounds show no meaningful progress;
- repeated same failure after focused repair attempts;
- a secret/token/key appears in tracked files, logs, or diff;
- destructive command or dangerous permission escalation is attempted;
- task requires a product decision that was not specified;
- safety boundary is crossed.

## TradingSignal Project Defaults

For `/Users/shancw/workspace/tradingsignal`:

```text
workdir: /Users/shancw/workspace/tradingsignal
tmux_session: tradingSignal
tmux_window: codex
```

Default validation:

```bash
uv run python -m pytest tests/ -v
uv run python -m compileall src tests -q
```

If frontend changed:

```bash
cd frontend && npm run typecheck
```

Safety rules:
- keep the system observe-only;
- do not add order execution, wallet access, exchange private-key use, entry/exit/SL/TP execution instructions, or live trading permissions;
- do not migrate or expose `/Users/shancw/workspace/trendbox_keyzon/config.json`;
- never print or commit API keys or secrets;
- do not copy the old `trendbox_keyzon` directory wholesale into the new repository;
- adapt old logic into the template layers instead.

Useful checks:

```bash
tmux has-session -t tradingSignal 2>/dev/null && echo ok || echo missing
ps -axo pid,etime,command | grep -E '[c]odex exec|[n]ode.*codex' | head -20
tmux capture-pane -t tradingSignal:codex -p -S -240 | tail -160
git status --short
git diff --stat
```

## Reporting Format

Keep reports concise but actionable:

```text
主人，supervisor 第 N 轮状态：
- Codex: running/exited/failed
- Changed files: <summary>
- Validation: pass/fail/not run yet
- Acceptance: complete/incomplete/blocked
- Safety: clean/issue found
- Next action: stop / wait / relaunch Codex with focused repair / need your decision
```

For failures, include the smallest useful error excerpt and the next focused repair target.

## Safety Notes

Do not create a full-auto cron unless the task spec is clear enough to define completion. If not, ask the user targeted questions first.

Do not allow cron to recursively create unrelated cron jobs. If full-auto needs continuation, it should operate within the originally authorized supervisor job and bounded rounds.

Do not commit, push, deploy, or edit secrets unless explicitly authorized and safe.