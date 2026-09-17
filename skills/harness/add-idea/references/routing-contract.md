# Add Idea Routing Guide

Use this guide to choose a Feature owner with minimal ceremony. Repository evidence should settle ownership whenever
possible; user questions are reserved for product choices and hard boundaries.

## Session Note

Keep only a small in-session note:

```text
Outcome:
Broad scope:
Likely owner:
Hard boundary:
Open core decision:
```

Do not save this note as an interview, idea, task, or progress file.

## Clarity

Classify the idea as:

- `CLEAR`: outcome, broad scope, and owner are clear enough to document;
- `CORE_QUESTION`: one unresolved answer can materially change the outcome, owner, or hard boundary;
- `BLOCKED_FACT`: a repository fact should answer the question but cannot currently be verified.

A missing implementation detail is not a reason to Grill. File layout, API naming, internal design, test shape, rollout,
rollback, metrics, and detailed acceptance can stay open unless the user explicitly wants to decide them now.

For `CORE_QUESTION`, ask the single highest-impact question and offer a recommended default. Re-evaluate after the
answer; do not follow a fixed questionnaire.

## Owner Route

### `PATCH_FEATURE`

Choose an existing Feature when its current responsibility already covers the intended outcome and the change does not
need an independent long-term owner.

Useful evidence includes its README, current code ownership, existing interfaces, and project navigation.

### `CREATE_FEATURE`

Create a Feature when the idea has an independent durable user/business outcome, public integration, data ownership,
safety boundary, or maintenance lifecycle that would be awkward inside an existing owner.

Document count and naming differences are weak signals. Prefer responsibility over taxonomy.

### `BLOCKED_OWNER`

Stop when two owners are equally plausible and choosing one changes public behavior, authority, data ownership, or a
long-term boundary. Present the trade-off as one concise question.

## Docs Route

| Change | Route |
|---|---|
| Existing Feature gains a durable outcome, boundary, or important limitation | `FEATURE_README_PATCH` |
| A new Feature owner or navigation entry is needed | `NAVIGATION_PATCH` |
| The idea is transient, already represented, or only a reversible local detail | `NO_DOC_CHANGE` |

One idea may use `FEATURE_README_PATCH + NAVIGATION_PATCH` when a new Feature is created. Do not generate additional
artifact types just because more detail could be written.

## Compact Decision Output

Before the final patch, be able to state:

```text
Clarity: CLEAR | CORE_QUESTION_RESOLVED
Owner: PATCH_FEATURE | CREATE_FEATURE | BLOCKED_OWNER
Selected path: <existing or proposed Feature README>
Core boundary: <one or two sentences>
Docs route: FEATURE_README_PATCH | NAVIGATION_PATCH | NO_DOC_CHANGE
```

This is an internal check, not a mandatory user-facing form.
