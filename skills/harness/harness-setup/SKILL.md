---
name: harness-setup
description: >-
  Bootstrap or retrofit a repo-wide harness setup: author AGENTS.md, docs
  overview/index maps, taskBoard control planes, and progressive-disclosure
  documentation that stays business- and stack-agnostic.
---

# Harness Setup

Use this skill when a repo needs a portable harness layer: a root instruction file,
a navigable docs map, a task execution board, and a doc tree an agent can follow
without guessing the repo shape.

## Outcome

Deliver the smallest useful harness that still gives an agent clear entry points:

- root `AGENTS.md` or equivalent
- `docs/OVERVIEW.md`
- `docs/feature/INDEX.md`
- `docs/reference/INDEX.md`
- `docs/archive/INDEX.md`
- module-level `README.md` / `INDEX.md`
- `taskBoard.md` for multi-wave or multi-node work
- leaf docs with explicit parent links

## Workflow

1. Inspect existing root instructions, docs, and ownership boundaries.
2. Identify the repo's real layers before writing any new structure.
3. Create or repair the docs map first.
4. Add a taskBoard when the work spans multiple waves, dependencies, or validation gates.
5. Write leaf docs only after the parent indexes exist.
6. Keep top-down discoverability and bottom-up traceability intact.
7. Validate that an agent can start at `AGENTS.md`, find the next doc, and walk back.

## Rules

- Treat docs as routing, not as a dumping ground.
- Keep business content out of the harness layer.
- Keep stack-specific details in repo-local adapters or references.
- Prefer repairing an existing partial harness over replacing it.
- Use root-relative links for deep cross-tree references.
- Keep `taskBoard.md` as the execution control plane, not as a changelog.

## Reference

Read `references/harness-bootstrap.md` for:

- AGENTS.md section order
- docs tree templates
- taskBoard decision rules
- leaf-document link rules
- validation checklist
- bundle installation from the source GitHub repo

## Demo Pack

If the target repo needs a fast bootstrap, copy the bundled demo harness from
`assets/demo-harness/` into the repo root and then replace the placeholder names.
The demo pack includes:

- a root `AGENTS.md`
- the `docs/` entry points
- reference docs for architecture, interfaces, and validation
- one sample feature module
- one sample `taskBoard.md`

Use it as a starting shape, not as a final domain model.

## Bundle Install

If the current GitHub repository is the source of truth for reusable skills,
install the curated harness bundle instead of copying skills one by one.

Use this when you want a target repo to receive the same harness stack:

- `harness-setup`
- `harness-engineering-plan`
- `progressive-disclosure-docs`
- `project-analysis`
- `project-docs-workflow`
- `codex-design-review`
- `code-organization-harness`

Recommended install flow:

1. Clone or point at the source GitHub repository.
2. Run the bundle installer in `scripts/install_harness_bundle.py`.
3. The installer copies the source bundle into `.agents/skills/harness/*` in the target repo.
4. Update the target repo's root `AGENTS.md` to register the installed skills.

See `references/harness-bootstrap.md` and `assets/harness-bundle.json` for the
bundle source layout and selection order.
