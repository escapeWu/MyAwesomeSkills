# Core Docs Guide

Use this guide when creating or simplifying a repository's durable documentation.

## Goal

A normal task should reach useful context quickly and should not require maintaining a documentation state machine.
Prefer a few well-owned documents over many narrowly typed artifacts.

## Smallest Useful Structures

### Small repository

```text
AGENTS.md or README.md
```

Keep the project map and stable rules in an existing root file when that is enough.

### Growing repository

```text
AGENTS.md
docs/OVERVIEW.md
docs/feature/<feature>/README.md
```

Create `docs/feature/INDEX.md` only when several Features need routing.

### Repository with stable cross-module references

```text
AGENTS.md
docs/OVERVIEW.md
docs/feature/INDEX.md
docs/feature/<feature>/README.md
docs/reference/INDEX.md
docs/reference/architecture.md
docs/reference/interfaces.md
docs/reference/runbook.md
```

Only include the reference files the project actually needs.

## Document Responsibilities

### Root agent rules

Keep stable safety, authorization, architecture, workflow, and context-entry rules. Do not copy full project design or
per-task procedures into this file.

### `docs/OVERVIEW.md`

Answer:

- what the system is;
- which major modules or Features exist;
- where to read next;
- how to perform the most common validation, or where the runbook lives.

If the root README already does this well, an overview may be unnecessary.

### Feature README

Choose sections based on the Feature, for example:

- purpose and scope;
- current behavior;
- important interfaces or data shapes;
- constraints and known limitations;
- concise current status and next step;
- links to stable supporting docs.

Expected and implemented behavior may share this owner when the distinction is written clearly. Split them only when
real project complexity justifies separate documents.

### Reference docs

Use these for stable facts shared across Features: architecture, public interfaces, configuration, operations, and
project-wide validation. Avoid feature status and delivery plans here.

## One-Pass Write-Back

For implementation work:

1. the main Agent reads existing docs as context;
2. it implements and validates;
3. it asynchronously delegates one docs maintenance task with the final summary, changed files, validation, and candidate owners;
4. one docs SubAgent collects the durable facts and patches the smallest owners in one editing pass;
5. that SubAgent updates navigation only if paths changed and verifies links;
6. the main Agent does not wait for ancillary maintenance or write the same docs concurrently.

If the environment has no SubAgent, the main Agent uses the same one-pass fallback at the end.

A task does not need a docs change when it only changes an internal detail and existing documentation remains true.

For docs-only restructuring, finish the inventory and target shape before applying the coherent patch.

## Keep Out of Core Docs

- current-session plans and checklists;
- raw command output, review transcripts, and intermediate reasoning;
- per-file progress mirrors;
- generated status matrices with no consumer;
- documents created only to authorize starting implementation;
- duplicate descriptions copied across multiple levels.

Projects may intentionally keep incident reports, decisions, or external collaboration records. Treat them as optional
project-owned conventions, not default harness requirements.

## Practical Test

The structure is light enough when:

- a new Agent finds the target module after one or two routing hops;
- a normal change reads no more than a few project docs;
- only one document clearly owns each stable fact;
- completing a task launches at most one asynchronous docs write-back pass with one writer;
- deleting an unused template or index does not break the workflow.
