---
name: document-organization-harness
description: >-
  Organize or simplify project documentation: a short root agent rule, an optional docs overview,
  lightweight feature/reference routing, and clear owners for stable knowledge. Use when a repository
  needs a usable docs map, when an existing harness is too heavy, or when scattered Markdown needs a
  smaller progressive-disclosure structure.
---

# Document Organization Harness

Build the smallest documentation layer that helps an Agent work without guessing. A documentation harness should reduce
reading and maintenance, not introduce a new project-management system.

## Default Outcome

Choose only the pieces the repository needs:

- a short `AGENTS.md` / `CLAUDE.md` section pointing to context;
- `docs/OVERVIEW.md` when the project needs a module map;
- `docs/feature/INDEX.md` when several Features need routing;
- one `README.md` per durable Feature that needs its own owner;
- `docs/reference/INDEX.md` and targeted references when stable cross-module facts need a home.

Do not pre-create requirements, Specs, ADRs, changelogs, archives, collaboration directories, task boards, evidence
ledgers, route manifests, or status schemas. Preserve any of these that the target project already uses effectively.

## Workflow

1. Inspect existing root instructions, docs entrypoints, and real code ownership.
2. Identify duplicate, stale, or orphaned documentation and the documents people actually use.
3. Design the smallest useful navigation path before editing.
4. Prefer repairing existing files over replacing the tree.
5. Apply the docs reorganization in one coherent patch after the inventory is complete.
6. Verify that a normal task reaches its owner after reading no more than a few documents.
7. Check affected links and report any intentionally retained legacy structure.

## Rules

- Treat overview and index files as maps, not full manuals.
- Keep project-specific content in project-owned docs, not in generic harness rules.
- Keep transient plans, analysis, raw logs, and current-session checklists out of long-term docs.
- Put Feature-specific stable knowledge in its README; put stable cross-Feature facts in reference docs.
- Split a document only when the split improves navigation or ownership. Do not use fixed line counts or document-count
  thresholds as automatic triggers.
- Update upper indexes only when navigation changes.
- Do not duplicate the same rule in root instructions and runtime-specific rule files unless the target platform truly
  requires both.
- Do not imply worktrees, TDD, testing-first, or implementation authorization.
- For implementation tasks, use one asynchronous docs SubAgent after completion; keep one writer and do not block the main Agent.
- Reuse the target repository's existing tests and docs checks; do not invent commands.

## Reference

Read [`references/harness-bootstrap.md`](references/harness-bootstrap.md) for a lightweight bootstrap and migration guide.
Use [`assets/demo-harness/`](assets/demo-harness/) only as a shape example. Remove every placeholder and every unused
file instead of copying the pack wholesale.

## Suite Maintenance

This repository is the canonical source for independent harness skills. Target projects may maintain the full suite, a
subset, or local extensions.

1. Read the suite `CHANGELOG.md` and `UPGRADING.md` when those maintenance files are installed alongside the skills; flat or partial installs may omit them.
2. Inspect the target registry, layout, working tree, and local rules.
3. Compare only the skills the target actually uses.
4. Preserve target-owned safety, authorization, commands, and useful local conventions.
5. Apply the lightweight docs rules only where they replace an accepted harness behavior.
6. Validate the target-specific diff and links.

Never replace a target `AGENTS.md`, docs tree, or skill directory wholesale when it contains unclassified local content.
