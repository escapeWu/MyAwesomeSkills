---
name: add-idea
description: >-
  Lightweight docs-only intake for adding a product or engineering idea to a harness-managed repository.
  Use when the user invokes add-idea or asks to record and route an idea to a new or existing Feature.
  Inspect current owners, ask only the most important unresolved product or hard-boundary question, then
  update the smallest set of core docs once. Do not produce Specs, questionnaires, or code.
disable-model-invocation: true
---

# Add Idea

Use this skill to turn an idea into a clear Feature owner and a small durable documentation update. The outcome is
not a complete implementation plan.

Read [references/routing-contract.md](references/routing-contract.md) before choosing the owner. Use
[`../progressive-disclosure-docs/references/core-docs-guide.md`](../progressive-disclosure-docs/references/core-docs-guide.md)
for document placement.

## Interaction Rules

- Preserve the user's intended outcome instead of expanding the process around it.
- Discover repository facts yourself; do not ask the user to locate files or repeat known context.
- Ask only when the answer changes the product outcome, Feature ownership, or a hard safety/authorization/compatibility
  boundary.
- Ask one compact question about the most consequential unknown and include a recommended default.
- Do not run a checklist interview. Scope details, acceptance wording, file layout, test shape, rollout mechanics, and
  other reversible implementation choices can remain open unless they are the actual decision the user brought.
- If the request and repository are clear enough, skip Grill entirely.
- Do not require a separate confirmation ceremony after restating information the user already supplied.

When the user explicitly says "grill me", ask for the single most important missing decision first. Continue asking only
if the answer exposes another genuine blocker; do not walk a predetermined questionnaire.

## Workflow

### 1. Find the likely owner

Read progressively:

1. root `AGENTS.md` / `CLAUDE.md` if present;
2. `docs/OVERVIEW.md` and `docs/feature/INDEX.md` if present;
3. at most the likely owning Feature README(s);
4. targeted code or references only when they settle ownership.

Prefer an existing Feature when it already owns the user-visible responsibility. A new phrase or implementation detail
is not by itself a new Feature.

### 2. Apply the minimal clarity check

An idea is clear enough when you can state:

- the desired outcome;
- the broad in-scope boundary;
- the likely Feature owner;
- any hard constraint that must not be crossed.

An exact acceptance matrix, module map, API shape, migration plan, test plan, rollback plan, or full non-goal list is not
required at intake. Leave those choices to implementation unless the user is deciding them now.

If one core item remains ambiguous, ask one question. If the ambiguity is safely reversible, state the assumption and
continue.

### 3. Choose the route

Choose one owner route:

- `PATCH_FEATURE`: an existing Feature owns the outcome;
- `CREATE_FEATURE`: the idea has an independent durable outcome or ownership boundary;
- `BLOCKED_OWNER`: choosing an owner would redefine a product or safety boundary without user direction.

Choose the smallest docs route:

- `FEATURE_README_PATCH`: update the owning README with the stable idea boundary;
- `NAVIGATION_PATCH`: create/register a new Feature or repair a route;
- `NO_DOC_CHANGE`: the idea is too transient, already documented, or only a reversible local detail.

Do not create requirements, Spec, ADR, changelog, task board, interview transcript, or parallel idea backlog as part of
this skill. Preserve an existing project convention when it already requires one, but do not introduce it from the harness.

### 4. Apply one documentation patch

After ownership and the core boundary are clear, update docs once:

- for `PATCH_FEATURE`, add the smallest useful section or bullets to the existing Feature README;
- for `CREATE_FEATURE`, copy the lightweight Feature README template, remove unused sections, and register it only in
  the indexes that actually exist;
- update `OVERVIEW.md` only when project-level navigation changes;
- keep implementation detail out of the intake document.

Do not alternate between questions and file writes. Gather the one necessary answer first, then make one coherent patch.

### 5. Finish briefly

Report:

- selected owner and why;
- the core boundary recorded;
- files updated, or why no docs changed;
- the next practical step.

This skill does not implement code. A later implementation request can proceed directly through the repository's normal
workflow without first creating more harness artifacts.

## Stop Conditions

Stop and surface one decision when:

- two owners remain equally plausible and the choice changes product behavior;
- the request crosses a safety, authorization, destructive, privacy, or compatibility boundary;
- the user outcome itself is unknown;
- writing would create a second source for the same durable knowledge.
