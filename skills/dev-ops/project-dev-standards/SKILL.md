---
name: project-dev-standards
description: create and refresh repository-specific development standards for an existing local codebase. use when the user wants to analyze a local repository, extract coding conventions from real files, generate docs/ai-dev-standards, create code review checklists, or update existing agents.md or claude.md files so future coding agents load the right standards before development. do not use for generic programming advice detached from a repository.
---

# Project Development Standards

Use this skill to bootstrap or refresh project-specific engineering standards from a local repository without Trellis. The output is a set of evidence-backed markdown files under `docs/ai-dev-standards/` plus optional updates to existing `AGENTS.md` and `CLAUDE.md` files.

## Core rule

Only document conventions supported by the current repository. Do not invent aspirational best practices. Every normative rule must include at least one concrete file path as evidence. If evidence is weak, mark the item as `Needs confirmation` instead of presenting it as a rule.

## Standard workflow

1. Identify the repository root from the user's local files or explicit path. If no path is given, use the current working directory when available.
2. Run the bundled inventory script:

   ```bash
   python scripts/repo_standards_bootstrap.py <repo-root> --write-docs --apply-agent-snippet
   ```

   Use `--apply-agent-snippet` only when the user wants files changed. The script only updates `AGENTS.md` and `CLAUDE.md` if they already exist.
3. Inspect the generated `_repo-inventory.md` and representative source files. Prefer high-signal files such as app entrypoints, route handlers, controllers, services, database schema/migration files, UI components, test files, config files, and existing agent instruction files.
4. Fill or refresh the generated markdown files under `docs/ai-dev-standards/` using the repository's real patterns.
5. Verify every rule has evidence. Remove generic rules that cannot be traced to source files.
6. Summarize what was created or changed, including any files that still need human confirmation.

## Output structure

Create or maintain this default structure:

```text
docs/ai-dev-standards/
  00-overview.md
  01-architecture.md
  02-backend.md
  03-frontend.md
  04-database.md
  05-testing.md
  06-code-review-checklist.md
  07-agent-instructions.md
  _repo-inventory.md
```

Adapt sections to the repository. For example, keep `03-frontend.md` short or mark it not applicable when no frontend exists. Do not create many extra files unless the repository clearly needs them.

## What each document should contain

- `00-overview.md`: stack, repo layout, how to choose relevant standards, commands, ownership assumptions.
- `01-architecture.md`: module boundaries, dependency direction, where business logic lives, cross-cutting concerns.
- `02-backend.md`: API route conventions, service/repository boundaries, validation, auth, error handling, logging.
- `03-frontend.md`: routing, component structure, state management, forms, styling, API client usage.
- `04-database.md`: schema ownership, migrations, ORM/query patterns, transaction rules, seed/test data.
- `05-testing.md`: test framework, naming, fixtures, mocks, integration vs unit expectations, required commands.
- `06-code-review-checklist.md`: concise review checklist mapped to the standards.
- `07-agent-instructions.md`: how future agents should select and read only the relevant standards before coding.
- `_repo-inventory.md`: generated evidence map and repository signals; keep it as support material, not the main standard.

For detailed templates and rule-writing examples, consult `references/document-templates.md`. For context-routing instructions and snippets, consult `references/agent-context-routing.md`.

## Rule quality standard

Write rules in this form:

```markdown
### [specific convention]

Rule: [one concrete action future developers/agents must follow]

Evidence:
- `path/to/file.ext` — [what this file demonstrates]
- `path/to/another.ext` — [what this file demonstrates]

Good:
```[language]
[short code pattern copied or paraphrased from the repo]
```

Avoid:
```[language]
[anti-pattern that contradicts repo usage]
```

Reason: [why this convention appears to exist in this repo]
```

Keep code examples short. Prefer paraphrasing if exact code is long. Never include secrets or large proprietary code excerpts.

## Updating AGENTS.md and CLAUDE.md

If the repository already has `AGENTS.md` or `CLAUDE.md`, append or replace a managed block that tells future coding agents to load `docs/ai-dev-standards/` selectively before coding. Do not create these files unless the user explicitly asks.

The managed block must state:

- always read `docs/ai-dev-standards/00-overview.md` and `docs/ai-dev-standards/07-agent-instructions.md` before coding;
- choose domain-specific standards based on touched files;
- read backend standards for API, service, auth, validation, logging, or job changes;
- read frontend standards for UI, component, route, state, styling, or form changes;
- read database standards for schema, migration, ORM, query, transaction, or seed changes;
- read testing standards before adding or changing tests;
- cite the relevant standards in the implementation summary.

The bundled script applies this block safely using `<!-- project-dev-standards:start -->` and `<!-- project-dev-standards:end -->` markers.

## Safety and scope

- Do not refactor business code during standards extraction unless explicitly asked.
- Do not treat linter defaults or framework documentation as project rules unless the repo config or examples demonstrate them.
- Do not scan ignored dependency/build directories such as `.git`, `node_modules`, `vendor`, `dist`, `build`, `.next`, `.venv`, or coverage outputs.
- If the repository is large, sample representative files first, then deepen inspection around the user's target area.
- If existing `AGENTS.md` or `CLAUDE.md` conflicts with generated standards, preserve the existing instructions and add a note in the final summary instead of overwriting unmarked content.
