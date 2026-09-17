# Lightweight Mainline Route Guide

Use this guide only when a project needs a development route to survive across sessions. Most tasks need only the
session plan and no durable route update.

## Owner

Keep a short route or current-focus section in the owning Feature README. Use a separate development-plan document only
when several durable workstreams and dependencies would make the README hard to scan.

Do not create a route manifest, machine node IDs, status axes, or append-only route log by default.

## Useful Content

A durable route usually needs only:

```text
Goal: <durable outcome>
Current focus: <semantic module or milestone>
Next: <next meaningful step>
Blocked by: <none or real dependency>
```

Use readable module and milestone names. Describe parallel work or joins in plain text when they matter.

## Update Timing

- Keep current-turn ordering in the session plan.
- Update the durable route only when cross-session focus or dependencies genuinely change.
- For implementation tasks, make that update in the single docs pass after implementation and validation complete.
- Do not write progress after every command, file, test, or subtask.

## Clarification

Ask the user only when two route choices produce materially different outcomes, ownership, cost, or risk. If the order is
reversible and does not affect a hard boundary, select a reasonable sequence and proceed.

## Reporting

When asked for progress, answer directly with the goal, current focus, blocker, and next step. Add implementation detail
only when the user asks for it or when it explains a blocker.
