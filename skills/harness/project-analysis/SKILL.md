---
name: project-analysis
description: >-
  Analyze architecture, data flow, call chains, route impact, performance risk, bugs, or expected-vs-implemented
  behavior when shallow docs and direct code reading are insufficient. Use a focused read-only investigation,
  answer directly when that is enough, and after the requested task is resolved let the main Agent asynchronously
  delegate one core-docs update when the findings are durable.
---

# Project Analysis

Use this skill for questions that need more than a quick file lookup. It is an analysis tool, not a mandatory phase for
every implementation and not a documentation generator by default.

## Topics

- `architecture`: module boundaries, dependencies, and external services;
- `dataflow`: entrypoints, transformations, state, and external I/O;
- `sequence`: important interactions and branches;
- `performance-risk`: likely bottlenecks and amplification points;
- `route-impact`: durable dependency or workstream conflicts;
- `behavior-gap`: requested or documented behavior versus current implementation;
- `bug-root-cause`: reproduction path, cause, impact, and fix boundary.

## Output Modes

Choose the lightest useful mode:

- **answer**: return findings in the conversation; default for questions and temporary analysis;
- **update-doc**: after the task is resolved, patch an existing Feature README or reference once because the findings are
  stable and useful beyond this session;
- **new-reference**: create a focused long-lived reference only when no existing owner can hold substantial stable knowledge.

Do not force documentation for one-off debugging, tentative hypotheses, or analysis that exists only to complete the
current task.

## Workflow

### 1. Bound the question

Identify the concrete question, likely entrypoint, and what evidence would answer it. Ask the user only if the intended
outcome or a hard product/safety boundary is unknown.

### 2. Read progressively

Use the smallest useful set:

1. applicable `AGENTS.md` / `CLAUDE.md`;
2. `docs/OVERVIEW.md` or the owning Feature README, if useful;
3. one relevant reference;
4. targeted code, tests, configuration, logs, or artifacts.

Do not full-read `docs/`. Existing docs are context, not automatic truth. Current code owns implemented behavior; user
direction and project rules own the requested and permitted outcome.

### 3. Collect focused evidence

Split work only when independent evidence surfaces justify it. Use local search directly for small investigations; use
2-4 read-only subtasks for genuinely broad architecture or call-chain analysis. Subagents are optional and require the
normal tool/user authorization of the environment.

For each conclusion, retain a useful path, symbol, command result, or artifact reference. Separate confirmed facts,
inferences, and unknowns.

### 4. Synthesize

Answer the actual question first. Include diagrams only when they make a relationship materially easier to understand.
Mermaid, ASCII, tables, and prose are options, not mandatory paired outputs.

A useful analysis normally contains:

- conclusion;
- key evidence;
- relevant flow or ownership;
- risks or unknowns;
- recommended next action or validation.

`route-impact` should describe the current route, proposed change, real dependency effects, and blockers in semantic
terms. Do not invent node IDs or route manifests.

### 5. Hand off docs once, if justified

If the analysis supports implementation, wait until implementation and risk-matched validation are complete. The main
Agent then passes the final findings, changed files, validation results, and candidate owners to the single asynchronous
docs SubAgent used by `project-docs-workflow`:

- Feature-specific stable behavior, constraints, design, or state -> owning Feature README;
- stable cross-Feature architecture, interface, or runbook fact -> related reference;
- new navigation -> necessary INDEX/OVERVIEW only.

That SubAgent applies one coherent incremental patch and is the only docs writer for the pass. The main Agent should not
wait for ancillary maintenance or edit the same docs concurrently. If SubAgents are unavailable, use the same one-pass
fallback at the end. Do not write analysis notes before implementation and then rewrite them afterward. Do not persist
raw search output, intermediate hypotheses, temporary gaps, or session plans.

When the user requested analysis only, update docs only if they explicitly asked for it or the repository clearly treats
that document as the requested deliverable.

## Behavior Gaps

When requested behavior, docs, and code disagree:

1. state each source and the mismatch;
2. determine whether the user or existing project rules already resolve the intended behavior;
3. ask one core question only if the expected result remains ambiguous;
4. avoid silently rewriting docs from code or code from stale docs;
5. after resolution, update the smallest durable owner once.

## Integration With `project-docs-workflow`

A caller should provide the question, likely code area, and any candidate Feature/reference docs. Return a compact
implementation context with entrypoints, relevant files, important data/contracts, risks, and validation candidates.
Temporary sequencing remains in the session plan.

## Reference Files

- Architecture investigation: `references/mode-architecture.md`
- Data flow and sequence investigation: `references/mode-dataflow.md`
- Output and docs placement: `references/output-guide.md`
- Optional Mermaid patterns: `references/mermaid-templates.md`
