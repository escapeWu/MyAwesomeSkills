---
name: code-organization-harness
description: >-
  Use when adding a new feature module, fixing a bug, refactoring, or deciding
  where code/tests/docs should live. Guides agents to discover context with
  targeted grep, choose module boundaries, place files by domain and layer, and
  follow project-specific Next.js, Python, and Java code organization patterns.
---

# Code Organization Harness

Use this skill before creating or moving code for any non-trivial feature, bug
fix, API change, refactor, or new module. Its job is to make file placement
boring: find the owning domain, extend the right layer, and keep new code easy
for the next agent to grep.

## Fast Workflow

1. **Name the capability first.** Write down the domain noun and verb in plain
   language: `scheduler task cancel`, `evaluation proposal approve`,
   `time-axis replay compare`.
2. **Map existing ownership.** Use docs as a map and code as truth. Start from
   `docs/OVERVIEW.md`, then `docs/feature/INDEX.md` or
   `docs/reference/INDEX.md` only when relevant.
3. **Grep before placing.** Search by endpoint, schema name, table name, UI
   label, config key, task id, and domain noun before adding files.
4. **Extend the nearest owner.** Prefer the existing module that already owns
   the invariant, data shape, or user workflow. Create a new module only when
   no current module has a clean reason to change with the new behavior.
5. **Place by domain, then layer.** Avoid dumping new code into `common`,
   `utils`, `components`, or `services` just because the code is reusable.
   Promote to shared only after there are at least two real callers and a stable
   contract.
6. **Mirror tests and docs.** New behavior gets tests near the corresponding
   layer. API/schema/runtime changes update the docs listed in `AGENTS.md`.

## Context Grep Recipes

Prefer `rg` and `rg --files`.

```bash
# Find likely owners by noun / route / schema / table.
rg -n "evaluation|proposal|scheduler|time_axis|run_id" src frontend/src tests docs
rg --files | rg "(evaluation|proposal|scheduler|time_axis|run|worker)"

# Trace an API path end to end.
rg -n "APIRouter|include_router|response_model|/api/evaluations" src/api tests frontend/src

# Trace a typed contract.
rg -n "class .*Response|class .*Request|model_validate|frontend/src/types" src frontend/src tests

# Trace persistence and repository ownership.
rg -n "class .*\\(Base\\)|__tablename__|repo_|AsyncSession|select\\(" src/api tests

# Trace frontend callers.
rg -n "apiGet|apiPost|apiPut|apiDelete|/api/" frontend/src tests

# Detect whether Java is present before applying Java guidance.
rg --files | rg "(^|/)(pom.xml|build.gradle|settings.gradle|src/(main|test)/java/)"
```

When grep finds several candidates, choose the file whose tests would naturally
fail if the new behavior were broken.

## Boundary Rules

- **Router/page code is an adapter.** It handles HTTP or UI composition, then
  calls service/domain code. Do not hide business rules in FastAPI routers or
  Next.js pages.
- **Services own orchestration.** Backend workflows, async dispatch, external
  reads, masking, degradation, and audit behavior belong in service/domain
  modules.
- **Models own contracts.** API contracts go through Pydantic schemas and
  frontend shared types. Persistence contracts go through SQLAlchemy tables and
  repository helpers.
- **Shared code needs a stable name.** Create `common`-style helpers only for
  narrow, domain-neutral behavior. If the helper name needs "misc", it is not
  ready to be shared.
- **Large modules get subpackages.** A service area that grows beyond a few
  cohesive files should become a package such as
  `src/api/services/ai_evaluation/`, with internal files named by capability.
- **Tests follow behavior, not implementation trivia.** Put API contract tests
  under `tests/test_api`, service/domain tests under `tests/test_services`,
  repository tests under `tests/test_repositories`, CLI tests under
  `tests/test_cli`, and schema-only tests under `tests/test_models`.

## Project Placement Matrix

| Change type | Primary location | Also check |
|---|---|---|
| Backend API endpoint | `src/api/routers/<domain>.py` | `src/api/app.py`, schemas, service, API tests |
| Backend business behavior | `src/api/services/<domain>.py` or package | service tests, docs feature module |
| API request/response | `src/api/models/schemas.py` | `frontend/src/types/index.ts`, `docs/reference/interfaces.md` |
| Persistence table/query | `src/api/models/tables.py`, `repositories.py`, Alembic | repository tests, runbook docs |
| Worker runtime/source | `src/api/services/workers/` | worker tests, scheduler/runtime docs |
| CLI command | `src/cli/<tool>/` | CLI tests, runbook docs |
| Frontend route | `frontend/src/app/<route>/page.tsx` | API helper, shared types, UI tests/typecheck |
| Shared frontend UI | `frontend/src/components/` | keep route-only UI local until reused |
| Frontend data access | `frontend/src/lib/api.ts` | never hardcode backend host in components/pages |
| Feature docs | `docs/feature/<module>/` | `docs/feature/INDEX.md`, `docs/OVERVIEW.md` when adding modules |

## Framework References

Load only the reference that matches the code being changed:

- Next.js App Router / React: `references/nextjs.md`
- Python / FastAPI / async SQLAlchemy: `references/python.md`
- Java / Maven / Gradle / Spring-style modules: `references/java.md`

If a framework reference conflicts with existing project conventions, follow the
project convention unless the task is explicitly to migrate it.

## Pre-Patch Checklist

- I can name the owning module and why it owns this behavior.
- I searched by domain noun, endpoint/schema/table name, and UI label.
- I am extending an existing file/module unless there is a clear new boundary.
- Any new shared helper has at least two callers or an obvious stable contract.
- API changes update backend schemas, frontend types, and interface docs.
- Tests are placed where the behavior is observed, not where the helper happens
  to live.
