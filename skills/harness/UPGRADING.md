# Maintaining And Upgrading Harness Skills

This repository maintains canonical harness skills. Each target project chooses which skills it uses and updates them
through its own reviewed workflow. There is no bundle installer or automatic overwrite.

## Ownership

| Surface | Owner | Rule |
|---|---|---|
| Canonical `skills/harness/<skill>/` | this repository | reusable source |
| Target skill copies and registry | target project | compare and update individually |
| `AGENTS.md`, `CLAUDE.md`, runtime rules | target project | patch, never replace wholesale |
| Core project docs | target project | update through the target workflow |
| Code, tests, configuration, and artifacts | target project | never changed merely because a skill changed |

A skill update does not authorize implementation, deployment, publication, destructive actions, or broad docs migration.

## Supported Layouts

Targets may use grouped, flat, partial, or locally extended skill layouts. Do not normalize paths during a functional
upgrade. Register only skills that actually exist and are intentionally maintained.

## Upgrade Flow

### 1. Audit

Record the target branch and working state, then identify:

- registered harness paths;
- local skill changes and extensions;
- existing project rules and validation commands;
- current docs entrypoints and owners;
- references to old harness artifacts or gates.

Preserve unrelated and user-owned changes.

### 2. Compare Used Skills

Compare one skill directory at a time. Classify each difference as canonical behavior to adopt, target-specific behavior
to preserve, obsolete harness behavior, or uncertain content to leave untouched.

Do not replace a directory containing unclassified local content.

### 3. Apply The Lightweight Model

For targets adopting this version, update coordinated surfaces in this order:

1. `progressive-disclosure-docs` and its core docs guide/templates;
2. `add-idea` and its lightweight owner routing;
3. `project-docs-workflow` asynchronous docs handoff;
4. `project-analysis` and external collaboration consumers;
5. `document-organization-harness` bootstrap/demo;
6. target-owned root or runtime rules.

A partial installation may update only the surfaces it uses. Remove links to absent skills or references.

### 4. Patch Target Governance

Preserve project safety, authorization, ownership, commands, and useful local conventions. Add only the accepted behavior:

- read a few relevant docs instead of the whole tree;
- do not create documentation as a start gate;
- do not prescribe TDD, testing-first, fixed status machines, or typed implementation-contract lifecycles;
- finish implementation and risk-matched validation first;
- then have the main Agent asynchronously delegate one bounded docs update to a single SubAgent writer;
- do not make the main Agent wait for ancillary docs maintenance;
- ask the user only about the desired outcome or a hard boundary that cannot be inferred safely.

When the environment has no SubAgent, retain a one-pass main-Agent fallback at task completion.

## Migrating Older Harness Docs

Do not bulk-delete working project knowledge. Migrate when related work touches it or when the user requests cleanup:

1. Identify stable content in legacy requirements, implementation-contract, decision, changelog, route-manifest, or
   status-matrix documents.
2. Move only still-useful Feature knowledge into the owning Feature README.
3. Move stable cross-Feature architecture, interfaces, or runbook content into existing references.
4. Keep a legacy document when it still has a real audience or project-owned purpose.
5. Remove obsolete files only after active links and agent rules no longer depend on them.
6. Update navigation once after the migration patch.

Do not convert old typed docs into a new set of typed docs. The goal is fewer owners and lower ongoing maintenance.

## Validation

After each target update:

- review the diff and preserve unrelated work;
- validate skill frontmatter and provider metadata;
- check registered paths and active documentation links;
- confirm root and runtime rules do not contradict each other;
- confirm one asynchronous docs writer is used after task completion and the main Agent is not required to wait;
- confirm old start gates and dead template links are gone;
- run the target project's existing docs/lint checks and `git diff --check`.

## Rollback

Keep the target change reviewable. Roll back through the target project's normal version-control process, restoring skill
files and governance references together so no registry path points to a removed file.

## Multiple Projects

Upgrade a small representative target first. Record which skills were updated, which local behavior was preserved,
validation results, and rollback status. There is intentionally no central installation marker; target history remains
the source of truth.
