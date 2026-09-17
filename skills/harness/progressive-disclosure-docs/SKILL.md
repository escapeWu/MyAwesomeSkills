---
name: progressive-disclosure-docs
description: >-
  Design, audit, or simplify project documentation so AI agents navigate by progressive disclosure:
  a small AGENTS.md/OVERVIEW map, optional feature/reference indexes, and only the few owning docs needed
  for the current task. Use when creating or refactoring agent-facing docs, reducing an overbuilt docs
  harness, repairing navigation, or migrating scattered Markdown into a lightweight maintainable structure.
---

# Progressive Disclosure Docs

Give the Agent a small map, then only the room it needs. The goal is faster task execution and lower context
cost, not a complete documentation bureaucracy.

Read [`references/core-docs-guide.md`](references/core-docs-guide.md) when creating or materially restructuring
a docs tree. Read [`references/mainline-route-guide.md`](references/mainline-route-guide.md) only when a project
actually maintains a cross-session development route.

## Minimal Shape

Use the smallest subset that fits the project:

```text
AGENTS.md / CLAUDE.md             # short stable rules and context entrypoint
docs/OVERVIEW.md                 # project map for repositories that need one
docs/feature/INDEX.md            # optional routing when several Features exist
docs/feature/<feature>/README.md  # owning Feature knowledge
docs/reference/INDEX.md          # optional routing when several references exist
docs/reference/*.md              # stable architecture, interface, or runbook facts
```

Optional directories such as `docs/collaboration/` and `docs/archive/` should appear only when the project has
real content for them. Do not pre-create empty layers.

A Feature README can hold its goal, scope, current behavior, important constraints, public interfaces, known
limitations, and concise current state. Split a dedicated design/dataflow/reference leaf only when it is stable,
substantial, and easier to maintain separately. The harness does not require separate requirements, Spec, ADR,
changelog, evidence ledger, or progress files.

When a repository already has a useful convention for requirements or decisions, preserve it. Do not create a
second convention or force migration merely to match this skill.

## Reading Rule

Add a short rule to the project instructions when useful:

```text
Read docs progressively: start at docs/OVERVIEW.md, choose the relevant feature or reference,
then open only 1-3 task-related documents. Do not read the entire docs tree.
```

Skip `OVERVIEW.md` when the root README or AGENTS file already provides a sufficient map. Progressive disclosure
is a navigation principle, not a mandatory directory layout.

## Ownership

Keep ownership understandable without a large truth matrix:

- user direction and project rules own the requested and allowed outcome;
- current code owns current implemented behavior;
- the Feature README owns stable feature knowledge and concise state;
- reference docs own stable cross-feature architecture, interfaces, and operating procedures;
- source artifacts own their raw evidence.

If docs and code disagree, verify the intended behavior rather than silently declaring either side correct. Update
the durable owner once the task is resolved.

## Write Timing

For implementation tasks, do not edit docs as a start gate. Read what is useful, finish the implementation and
risk-matched validation, then have the main Agent launch one asynchronous docs SubAgent:

1. the main Agent supplies the final behavior summary, changed files, validation results, and candidate owners;
2. one docs SubAgent identifies the durable facts that changed;
3. that SubAgent patches the smallest owning document once;
4. it updates an INDEX or OVERVIEW only when navigation changed;
5. it checks affected links and stops.

The docs SubAgent is the only writer for that maintenance pass. The main Agent should not wait for ancillary docs work
or modify the same docs concurrently. If no SubAgent is available, the main Agent performs the same single lightweight
pass at the end.

Do not persist session plans, intermediate reasoning, raw command output, review transcripts, or temporary status.
If nothing durable changed, do not modify docs.

For a docs-only organization task, first finish the inventory and target shape, then apply one coherent patch rather
than repeatedly rewriting the tree while exploring.

## Feature Docs

Use one directory per durable feature only when a directory helps navigation. A small feature may be represented by
a single README.

Recommended README sections, chosen as needed rather than copied mechanically:

- purpose and scope;
- current behavior;
- important interfaces or data shapes;
- constraints and known limitations;
- concise current status or next step;
- links to stable supporting references.

Use `assets/feature-template/` as a starting point, then remove unused sections. An `INDEX.md` inside the feature is
only useful when the feature has several stable leaf documents.

## Reference Docs

Put cross-feature, relatively stable knowledge under `docs/reference/`, for example:

- architecture and dependency direction;
- public or external interfaces;
- configuration and operational runbooks;
- project-wide validation commands.

Feature-specific details stay in the Feature README. Avoid copying the same status or interface description into
OVERVIEW, indexes, feature docs, and references.

## Navigation

Top-level files are maps, not summaries of everything below them:

- `AGENTS.md` contains stable rules and an optional context link;
- `OVERVIEW.md` names major modules and where to go next;
- an INDEX explains which document to open for which task;
- a leaf contains the actual knowledge.

Use links that work in the target repository. Parent links are helpful for deep leaves but are not required on every
small document when navigation is already obvious.

## Mainline Routes

Most projects need only a short current-focus or next-step note in the owning README. Use a route document only when
several workstreams, dependencies, or handoffs must survive across sessions. Prefer semantic names and readable text;
do not introduce machine node IDs, mandatory DAG manifests, or multi-axis status schemas unless the project already
needs them.

## Migration

1. Inventory existing Markdown and identify the actual entrypoints.
2. Keep the documents that carry stable, useful knowledge.
3. Choose the smallest navigation shape that makes those documents discoverable.
4. Merge duplicate status, requirement, plan, or design pages into their natural owner.
5. Archive or remove obsolete material according to project policy.
6. Apply the migration in one coherent patch and repair affected links.
7. Verify that an Agent can reach the relevant owner without reading unrelated docs.

Do not reorganize working documentation merely because a different shape looks cleaner.

## Audit Checklist

- The first context file is short and points to the next useful place.
- A normal task needs no more than 1-3 project docs before code exploration.
- Feature and reference knowledge have obvious owners.
- There are no mandatory pre-implementation document writes.
- Docs are updated once after task completion by one asynchronous docs SubAgent, only when durable facts changed.
- The main Agent is not blocked by ancillary docs maintenance and does not create concurrent docs writers.
- The harness does not prescribe TDD, Spec lifecycles, status machines, task boards, or evidence ledgers.
- Optional directories and leaf docs exist only because the project uses them.
- Active links resolve and no duplicate control plane was introduced.
