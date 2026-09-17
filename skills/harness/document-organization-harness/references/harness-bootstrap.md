# Lightweight Harness Bootstrap

Use this reference to add only the documentation structure a target repository needs.

## 1. Inspect Before Editing

Read the existing root instructions, README, docs entrypoints, and a small sample of module docs. Identify:

- which files people and Agents already use;
- how code ownership is actually divided;
- stable safety, authorization, architecture, and validation rules;
- duplicate, stale, or orphaned docs;
- whether a new docs layer would improve navigation at all.

Do not copy the demo before this inventory is complete.

## 2. Choose the Smallest Shape

### Root file only

Use the existing `AGENTS.md`, `CLAUDE.md`, or README when the repository is small and already understandable.

### Overview plus Feature owners

```text
AGENTS.md
docs/OVERVIEW.md
docs/feature/<feature>/README.md
```

Add `docs/feature/INDEX.md` when several Features make direct overview links noisy.

### Stable references

Add `docs/reference/` only when the project has stable cross-Feature architecture, interfaces, configuration, operations,
or validation procedures that do not fit one Feature.

Optional collaboration or archive directories should be created only by a real collaboration or archival need.

## 3. Root Rule

Patch an existing documentation/context section. If none exists, a small block is enough:

```md
## Project Context

- Start from `docs/OVERVIEW.md` when the task needs project context.
- Follow the relevant Feature/reference link and read only 1-3 task-related docs.
- Do not create planning or contract documents before implementation.
- Complete implementation and risk-matched validation first, then update durable docs once.
- Ask the user only when the desired outcome or a hard safety/authorization/compatibility boundary is unclear.
```

Remove the `OVERVIEW.md` line if that file is unnecessary. Preserve existing project rules and commands.

## 4. Overview Template

```md
# Project Overview

## Purpose

<What the system does and its important boundary.>

## Modules

| Module | Responsibility | Read next |
|---|---|---|
| <name> | <stable responsibility> | [Feature README](feature/<slug>/README.md) |

## References

- [Architecture](reference/architecture.md), if present
- [Interfaces](reference/interfaces.md), if present
- [Runbook](reference/runbook.md), if present
```

Keep the overview compact. Omit empty sections.

## 5. Feature README Template

Start from `../progressive-disclosure-docs/assets/feature-template/README.md` and keep only useful sections:

- purpose and scope;
- current behavior;
- important interfaces/data;
- constraints and limitations;
- concise current state or next step;
- supporting links.

A single README is the default. Create a local INDEX only after several stable leaf docs make routing useful.

## 6. Reference Ownership

Use reference docs for facts shared across Features. Typical examples:

- `architecture.md` for system-level components and dependency direction;
- `interfaces.md` for stable public or cross-module interfaces;
- `runbook.md` for stable operating and validation procedures.

Do not copy feature status into these files.

## 7. Write Timing

For code tasks:

1. read relevant context;
2. implement;
3. validate;
4. update affected core docs in one pass;
5. check links.

For a docs bootstrap task, finish the inventory and target shape before writing, then apply one coherent patch.

No pre-implementation Spec, task board, progress log, TDD phase, status matrix, or evidence ledger is required.

## 8. Validation

Check:

- the root entry points to a real file or intentionally uses no docs entry;
- an Agent can reach each major owner without reading unrelated docs;
- feature and reference owners are obvious;
- no empty optional directory or placeholder remains;
- existing safety, authorization, ownership, and project commands were preserved;
- links resolve using the target repository's normal tooling;
- no duplicate runtime rule was added without a platform requirement.

## 9. Maintenance

When updating an existing target project:

1. read the suite `CHANGELOG.md` and `UPGRADING.md`;
2. compare one used skill at a time;
3. preserve local extensions and target-owned rules;
4. replace old heavy gates only where the project accepts the lightweight model;
5. migrate old typed docs gradually or leave them in place if they remain useful;
6. review the target-specific diff and run existing docs checks.

A canonical skill change is maintenance input, not authorization to rewrite a target repository.
