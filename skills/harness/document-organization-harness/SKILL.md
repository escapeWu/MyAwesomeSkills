---
name: document-organization-harness
description: >-
  Organize or retrofit project documentation: author AGENTS.md, docs
  overview/index maps, module documentation boundaries, owning GOAL/README
  status routing, and progressive-disclosure documentation. Use when a
  repository needs a clear documentation structure, navigation hierarchy, or
  documentation governance.
---

# Document Organization Harness

Use this skill when a repo needs a portable harness layer: a root instruction
file, a navigable docs map, explicit module ownership, and a documentation tree
an agent can follow without guessing the repo shape.

## Outcome

Deliver the smallest useful harness that still gives an agent clear entry points:

- root `AGENTS.md` or equivalent
- optional `.cursor/rules/harness-execution.mdc` for an always-applied contract,
  validation, and documentation synchronization gate
- `docs/OVERVIEW.md`
- `docs/feature/INDEX.md`
- `docs/reference/INDEX.md`
- `docs/collaboration/INDEX.md`
- `docs/archive/INDEX.md`
- module-level `README.md` / `INDEX.md` plus `requirements.md` for expected
  product or business behavior and acceptance
- lazy `specs/` for bounded implementation contracts and `decisions/` for ADRs
- owning GOAL/README sections for completed work, pending work, blockers, and
  the next validation gate
- leaf docs with explicit parent links

## Workflow

1. Inspect existing root instructions, docs, and ownership boundaries.
2. Identify the repo's real layers before writing any new structure.
3. Create or repair the docs map first; distinguish `requirements.md` for
   expected behavior, Specs for bounded implementation contracts, ADRs for
   durable rationale, and `README.md` / `INDEX.md` for current state/routing.
4. Route durable progress through the owning GOAL/README instead of creating a
   separate execution-control document.
5. Write leaf docs only after the parent indexes exist.
6. Record stable validation evidence in owning docs or append-only artifacts.
7. Keep top-down discoverability and bottom-up traceability intact.
8. Validate that an agent can start at `AGENTS.md`, find the next doc, and walk
   back.

## Rules

- Treat docs as routing, not as a dumping ground.
- Keep business content out of the harness layer.
- Keep stack-specific details in repo-local adapters or references.
- Prefer repairing an existing partial harness over replacing it.
- Use root-relative links for deep cross-tree references.
- Keep expected behavior, current implementation, current progress, and
  historical evidence distinct, with each routed to its owning durable file.
- Do not persist transient decomposition solely to coordinate the current
  session; use the session's planning surface instead.
- Before non-trivial implementation, freeze module owners, public interfaces,
  dependency direction, mutable-state ownership, file budgets, and test ownership.
- Keep new or changed handwritten files at or below 1000 physical lines; at
  800 lines, review responsibility-based extraction with `refactor-large-modules`.
- Delegation is never implied by this skill. When a user explicitly requests
  delegation, use bounded owner scopes and isolated worktrees where needed.
- **Enforcement must be runtime-injected, not just described.** In a Cursor
  repo, keep the contract, validation, evidence, and documentation synchronization
  gate in BOTH `.cursor/rules/harness-execution.mdc` (`alwaysApply: true`) and
  root `AGENTS.md`.

## Reference

Read `references/harness-bootstrap.md` for:

- AGENTS.md section order
- docs tree templates
- sample feature module with README + requirements separation
- owning GOAL/README status rules
- leaf-document link rules
- validation checklist
- per-project skill maintenance and contract migration

## Demo Pack

If the target repo needs a fast bootstrap, adapt the included demo harness from
`assets/demo-harness/` and replace every placeholder with target-project facts.
The demo pack includes:

- a root `AGENTS.md` with documentation governance and execution-safety rules
- a Cursor-native `.cursor/rules/harness-execution.mdc` gate (`alwaysApply: true`)
- the `docs/` entry points
- reference docs for architecture, interfaces, and validation
- one sample feature module showing README + requirements separation

Use it as a starting shape, not as a final domain model.

## Suite Maintenance Boundary

This repository is the canonical maintenance source for independent harness skills. It does not
provide a bundle manifest, installer, automatic overwrite, or target-project upgrade command.
Projects may maintain the full suite, a subset, or local extensions in grouped or flat paths.

`add-idea` is the explicit docs-only intake for unclear or clear product/engineering ideas. It runs
the Grill protocol when needed, chooses a new or existing Feature owner, and materializes
requirements, Specs, and conditional ADRs before later implementation workflows.

Recommended maintenance flow:

1. Read the suite [`CHANGELOG.md`](../CHANGELOG.md) and
   [`UPGRADING.md`](../UPGRADING.md).
2. Inspect the target project's actual skill registry, layout, local extensions, and working tree.
3. Compare and update only the individual skills the target uses; do not normalize paths or replace
   directories containing unclassified local content.
4. When adopting the full lifecycle change, maintain shared contracts first, then producer and
   consumer skills, then patch target-owned governance.
5. Follow the suite [`AGENTS.md` patch contract](../README.md) to incrementally update existing target
   rules; never replace target-owned rules or Feature docs.

See `references/harness-bootstrap.md` for docs scaffolding and maintenance order. Target repository
history, reviewed diffs, and validation evidence remain the truth for what that project maintains.
