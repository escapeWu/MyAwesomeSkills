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
- owning GOAL/README sections for completed work, pending work, blockers, and
  the next validation gate
- leaf docs with explicit parent links

## Workflow

1. Inspect existing root instructions, docs, and ownership boundaries.
2. Identify the repo's real layers before writing any new structure.
3. Create or repair the docs map first; distinguish `requirements.md` for
   expected behavior from `README.md` / `INDEX.md` for current implemented
   state and routing.
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
- bundle installation from the source GitHub repo

## Demo Pack

If the target repo needs a fast bootstrap, copy the bundled demo harness from
`assets/demo-harness/` into the repo root and then replace the placeholder names.
The demo pack includes:

- a root `AGENTS.md` with documentation governance and execution-safety rules
- a Cursor-native `.cursor/rules/harness-execution.mdc` gate (`alwaysApply: true`)
- the `docs/` entry points
- reference docs for architecture, interfaces, and validation
- one sample feature module showing README + requirements separation

Use it as a starting shape, not as a final domain model.

## Bundle Install

If the current GitHub repository is the source of truth for reusable skills,
install the curated harness bundle instead of copying skills one by one.

Use this when you want a target repo to receive the same harness stack,
including skills that support a requirements-first docs layer:

- `document-organization-harness`
- `progressive-disclosure-docs`
- `project-analysis`
- `project-docs-workflow`
- `external-collaboration-workflow`
- `refactor-large-modules`

Recommended install flow:

1. Clone or point at the source GitHub repository.
2. Run the bundle installer in `scripts/install_harness_bundle.py`.
3. The installer copies this bundle README and the source skills into
   `.agents/skills/harness/` in the target repo.
4. Follow the bundle-level [`AGENTS.md` patch contract](../README.md) to
   incrementally update the target repo's root `AGENTS.md`.

See `references/harness-bootstrap.md` and `assets/harness-bundle.json` for the
bundle source layout and selection order.
