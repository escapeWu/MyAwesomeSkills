# Development Standards Document Templates

Use these templates when creating or refreshing `docs/ai-dev-standards/`.

## 00-overview.md

```markdown
# Project Development Standards Overview

## Purpose
These standards capture conventions observed in this repository. They are not generic best practices.

## Evidence policy
Every rule must cite repository files. Rules without evidence are marked `Needs confirmation`.

## Technology stack
| Area | Detected tools | Evidence |
|---|---|---|
| Runtime |  |  |
| Backend |  |  |
| Frontend |  |  |
| Database |  |  |
| Testing |  |  |
| Build / CI |  |  |

## Repository layout
| Path | Purpose | Notes |
|---|---|---|
| `src/` |  |  |

## Required commands
| Purpose | Command | Evidence |
|---|---|---|
| Install |  |  |
| Lint |  |  |
| Typecheck |  |  |
| Test |  |  |
| Build |  |  |

## How agents should use these standards
Read `07-agent-instructions.md`, then load only the domain docs relevant to the files being changed.
```

## 01-architecture.md

```markdown
# Architecture Standards

## Module boundaries

### [boundary name]
Rule:

Evidence:
- `path` — observation

Reason:

## Dependency direction

## Where business logic belongs

## Cross-cutting concerns
- Auth:
- Logging:
- Error handling:
- Configuration:
```

## 02-backend.md

```markdown
# Backend Standards

## API route structure

## Request validation

## Authentication and authorization

## Service / repository boundaries

## Error handling

## Logging

## Background jobs / async work

## External integrations
```

## 03-frontend.md

```markdown
# Frontend Standards

## App routing

## Component organization

## State management

## Forms and validation

## Styling

## API client usage

## Error and loading states
```

## 04-database.md

```markdown
# Database Standards

## Schema ownership

## Migration workflow

## Query / ORM patterns

## Transactions

## Seed and test data

## Data safety rules
```

## 05-testing.md

```markdown
# Testing Standards

## Test framework and commands

## Test file naming

## Unit tests

## Integration tests

## Fixtures and mocks

## What to run before handoff
```

## 06-code-review-checklist.md

```markdown
# Code Review Checklist

Use this checklist after implementation.

## Required checks
- [ ] The change follows architecture boundaries in `01-architecture.md`.
- [ ] Backend changes follow `02-backend.md` when applicable.
- [ ] Frontend changes follow `03-frontend.md` when applicable.
- [ ] Database changes follow `04-database.md` when applicable.
- [ ] Tests follow `05-testing.md`.
- [ ] New or changed conventions are documented with evidence.

## Domain-specific checks
[Add concise bullets based on repository evidence.]
```

## 07-agent-instructions.md

```markdown
# Agent Instructions for Development Standards

Before coding:
1. Read `docs/ai-dev-standards/00-overview.md`.
2. Read this file.
3. Identify the files and domains the task will touch.
4. Load only the relevant domain standards:
   - backend/API/service/auth/logging/jobs: `02-backend.md`
   - frontend/UI/forms/routes/state/styling: `03-frontend.md`
   - schema/migration/ORM/query/transaction/seed data: `04-database.md`
   - tests/fixtures/mocks/CI validation: `05-testing.md`
   - architecture/module boundaries/cross-cutting changes: `01-architecture.md`
5. During handoff, state which standards were loaded and whether any rule needs updating.

Do not load every standards file by default for small tasks. Prefer task-relevant context.
```
