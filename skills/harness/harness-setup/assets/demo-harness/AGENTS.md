# Agent Guide

> Replace `<project-name>`, `<domain>`, and command placeholders before adopting
> this file in a real repository.

## Project Contract

`<project-name>` uses a docs-first harness so agents can discover context,
plan work, implement changes, and verify outcomes without relying on hidden
memory or ad hoc repository knowledge.

This repository is responsible for:

- `<primary capability 1>`;
- `<primary capability 2>`;
- `<primary capability 3>`.

This repository is not responsible for:

- `<explicit non-goal 1>`;
- `<explicit non-goal 2>`;
- `<safety or permission boundary>`.

Sensitive data, credentials, private keys, tokens, production secrets, and
private runtime dumps must not be committed, logged, copied into docs, or
returned in user-facing output.

## Core Principles

- **Docs-first:** important work starts by reading the docs entry path and
  updating docs when contracts, behavior, or validation change.
- **Single source of truth:** each durable rule has one owner. Avoid copying
  business rules across routers, scripts, UI, tests, and docs.
- **Contracts before implementation:** stable names, schemas, CLI flags, API
  shapes, file formats, and lifecycle states are defined before parallel work.
- **Layer separation:** higher layers call lower layers through documented
  interfaces. Avoid bypasses that make behavior untraceable.
- **Observable execution:** meaningful work leaves evidence: tests, logs,
  snapshots, taskBoard status, or documented manual validation.
- **Progressive disclosure:** agents read maps first, then only the specific
  module docs needed for the task.

## Reading Path

Follow this path for non-trivial work:

```text
AGENTS.md
  -> docs/OVERVIEW.md
  -> docs/feature/INDEX.md or docs/reference/INDEX.md
  -> docs/feature/<module>/README.md
  -> leaf docs or taskBoard.md only when needed
```

Do not read the whole `docs/` tree by default.

## Progressive Disclosure Levels

| Level | File | Purpose |
|------|------|---------|
| L0 | `AGENTS.md` | root rules and reading path |
| L1 | `docs/OVERVIEW.md` | repo map and active domains |
| L2 | `docs/feature/INDEX.md` | feature/module routing |
| L2 | `docs/reference/INDEX.md` | stable architecture, interfaces, runbook |
| L2 | `docs/archive/INDEX.md` | historical material, not active context |
| L3 | `docs/feature/<module>/README.md` | module-specific map |
| L4 | leaf docs / `taskBoard.md` | detailed design, execution, evidence |

## Repo-local Skills

Register repo-local skills here when they exist.

| Skill | Use When | Owns |
|------|----------|------|
| `harness-setup` | bootstrapping or repairing this harness | AGENTS/docs/taskBoard structure |
| `harness-engineering-plan` | planning multi-wave or multi-owner work | milestones, TaskNodes, gates |
| `project-docs-workflow` | non-trivial code changes may affect docs | docs impact review |
| `<domain-skill>` | `<domain trigger>` | `<domain workflow>` |

Skill rules:

- each skill owns one workflow;
- skill triggers must be explicit;
- detailed variants live in the skill's `references/` or `assets/`;
- do not put long implementation manuals in `AGENTS.md`.

Recommended local skill shape:

```text
.agents/
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        └── assets/
```

## Code Organization

Replace this section with the target repo's actual layers.

Generic default:

```text
contracts -> config -> domain/services -> adapters -> interface
```

Rules:

- put orchestration in the owning domain/service layer;
- keep interface layers thin;
- keep reusable helpers small and genuinely cross-domain;
- mirror tests to the layer they validate;
- search for an existing owner before creating a new module.

## Docs Organization

The minimum docs tree is:

```text
docs/
├── OVERVIEW.md
├── feature/
│   ├── INDEX.md
│   └── <module>/
│       ├── README.md
│       └── taskBoard.md
├── reference/
│   ├── INDEX.md
│   ├── architecture.md
│   ├── interfaces.md
│   └── runbook-testing.md
└── archive/
    └── INDEX.md
```

Docs rules:

- add parent index entries before adding leaf docs;
- every leaf doc starts with a parent link;
- active plans stay under `docs/feature/`;
- stable cross-cutting rules stay under `docs/reference/`;
- old plans, one-off summaries, and retired designs go under `docs/archive/`;
- use root-relative links for deep cross-tree references.

Leaf doc header example:

```md
> 上级：[../README.md](../README.md)
```

or:

```md
> 上级：[/docs/OVERVIEW.md](/docs/OVERVIEW.md)
```

## TaskBoard Rules

Create or update `taskBoard.md` when work has:

- more than one wave;
- meaningful task dependencies;
- multiple owners or high-conflict files;
- staged validation;
- an auditable implementation record.

Task status flow:

```text
planned -> ready -> running -> validating -> done
                         \-> repair_needed -> running
running -> blocked | failed
```

Each TaskNode should include:

- id and title;
- owner/layer;
- dependencies;
- input context;
- expected output;
- acceptance criteria;
- validation commands;
- done evidence.

## Change Process

Before editing:

1. Read `docs/OVERVIEW.md`.
2. Pick the relevant feature or reference index.
3. Read the owning module README.
4. Decide whether a `taskBoard.md` is required.

During editing:

1. Keep changes inside the owning module/layer.
2. Update contracts before dependent implementation.
3. Update taskBoard status as work advances.

Before finishing:

1. Run the relevant validation commands.
2. Update docs affected by behavior, interfaces, or runbooks.
3. Confirm top-down and bottom-up doc navigation still works.
4. Summarize evidence, not intentions.

## Validation

Replace placeholders with repo-specific commands.

Recommended categories:

```bash
<unit-test-command>
<typecheck-or-compile-command>
<lint-or-format-command>
<integration-or-smoke-command>
```

Docs navigation validation:

- start at `AGENTS.md`;
- reach `docs/OVERVIEW.md`;
- reach `docs/feature/INDEX.md`;
- reach one module README;
- reach one leaf doc or taskBoard;
- walk back through parent links;
- confirm archive files are not active execution paths.

## Isolation

For non-trivial feature work, prefer an isolated branch or worktree. Keep this
rule aligned with the repo's actual branching model.

Generic branch names:

- `feat/<slug>` for features;
- `fix/<slug>` for bug fixes;
- `docs/<slug>` for documentation-only work.

## History / Exceptions

Use `docs/archive/INDEX.md` to route historical material.

Archive:

- completed taskBoards;
- retired designs;
- old RCA or bugfix notes;
- one-off reports.

Do not archive active contracts or current execution plans.

## Failure Modes To Avoid

- leaf docs that are only discoverable by search;
- taskBoards created after implementation instead of before;
- duplicate business rules in code and docs with no owner;
- interface changes without contract docs;
- tests that pass but do not prove the stated contract;
- archived plans still linked as active context;
- root instructions that mention skills without clear triggers.
