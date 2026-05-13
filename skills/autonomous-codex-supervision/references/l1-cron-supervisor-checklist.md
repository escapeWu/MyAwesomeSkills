# L1 Cron Supervisor Checklist

Use this when the user authorizes L1 / full-auto Codex supervision or any long-running Codex task that should keep progressing without the main chat manually polling.

## Non-negotiable launch shape

A valid L1 launch has all four pieces before the assistant reports that supervision is active:

1. **Task spec / prompt** — saved to a file with acceptance criteria, validation commands, safety rules, max rounds, and stop conditions.
2. **Worktree + tmux Codex** — Codex runs in an isolated worktree / branch inside a named tmux session/window.
3. **Supervisor state file** — JSON or markdown state persisted in the worktree, including current round, acceptance booleans, validation commands, and safety rules.
4. **Cron supervisor** — scheduled job that monitors tmux/Codex, validates on exit, relaunches bounded repair rounds, and reports to the origin/user.

If only tmux is started, that is **not** L1 full-auto; it is manual polling.

## Cron creation discipline

- Create the cron job immediately after launching or before launching Codex; do not wait for the first manual poll.
- Prefer an explicit cron expression such as `*/5 * * * *` over natural language like `every 5m` when exact near-term scheduling matters.
- After creating/updating the job, inspect `next_run_at`. If it is not in the expected near future, patch the schedule immediately.
- Trigger one manual `cronjob(action="run")` after creation to validate the prompt, toolsets, and delivery path.
- The cron prompt must explicitly say it must not recursively create/update/delete cron jobs.

## Minimal cron prompt responsibilities

Each run should:

1. Read the supervisor state file.
2. Check tmux session/window and capture recent output.
3. Check whether Codex is still running.
4. If running: report progress and avoid expensive validation.
5. If exited: collect git status/diff, run validation commands, perform static acceptance checks and safety scan.
6. If incomplete and safe: write a focused repair prompt, increment round state, relaunch Codex in the same tmux/worktree.
7. If complete: update state and report changed files, validation evidence, and waiting-for-integration status.
8. If blocked: report the stop reason and preserve the worktree.

## Highest-level L1 full-auto authority

When the user explicitly says L1 full-auto should “自动推进所有实施” or have “最高级别的测试、合并、审核权限”, encode that authority in both the supervisor state and cron prompt. The loop should not stop after one milestone: after a milestone passes validation, it should update evidence, checkpoint commit, generate the next milestone prompt, and launch the next Codex round automatically. Treat local testing, local integration review, and local merge-readiness review as in-scope. Still stop for safety boundary changes, destructive actions, secrets/private data access, unresolved product/architecture choices, repeated repair failure, or protected remote push/merge not explicitly authorized.

## Common miss caught by user correction

Do not answer “L1 full-auto started” after only running `codex exec --full-auto` in tmux. L1 requires a cron-backed supervisor loop plus persisted state. The main chat may still monitor manually, but manual polling is not a substitute for cron supervision.