# Agent Context Routing

Future coding agents should not read every standard for every task. They should choose standards by touched domain.

## Selection matrix

| Task touches | Load these files |
|---|---|
| any coding task | `00-overview.md`, `07-agent-instructions.md` |
| module boundaries, app structure, dependency direction | `01-architecture.md` |
| API routes, controllers, services, auth, validation, errors, logging, jobs | `02-backend.md` |
| UI, pages, routes, components, hooks, forms, state, styling | `03-frontend.md` |
| schema, migrations, ORM models, queries, transactions, seed data | `04-database.md` |
| tests, mocks, fixtures, test commands, CI validation | `05-testing.md` |
| review or handoff | `06-code-review-checklist.md` plus domain docs above |

## Managed block for AGENTS.md / CLAUDE.md

```markdown
<!-- project-dev-standards:start -->

## Project development standards

This repository keeps project-specific development standards in `docs/ai-dev-standards/`. Before coding, load only the standards relevant to the task.

Always read:
- `docs/ai-dev-standards/00-overview.md`
- `docs/ai-dev-standards/07-agent-instructions.md`

Then choose domain standards based on touched files:
- architecture or module-boundary changes: `docs/ai-dev-standards/01-architecture.md`
- API, service, auth, validation, logging, background job, or integration changes: `docs/ai-dev-standards/02-backend.md`
- UI, route, component, form, state, styling, or frontend API-client changes: `docs/ai-dev-standards/03-frontend.md`
- schema, migration, ORM, query, transaction, seed, or data-access changes: `docs/ai-dev-standards/04-database.md`
- test, fixture, mock, or CI-validation changes: `docs/ai-dev-standards/05-testing.md`
- review or handoff: `docs/ai-dev-standards/06-code-review-checklist.md`

In the final implementation summary, mention which standards were loaded and whether any standard should be updated based on new patterns discovered during the task.

<!-- project-dev-standards:end -->
```
