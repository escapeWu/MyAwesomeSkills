# Python Organization Reference

Use this when changing `src/`, `tests/`, backend scripts, or Python CLI tools.

## Repository Shape

This project currently packages Python under `src/` and keeps FastAPI code in
`src/api`.

```text
src/api/models/schemas.py        API request/response contracts
src/api/models/tables.py         SQLAlchemy persistence models
src/api/models/repositories.py   async DB query helpers
src/api/services/               business orchestration and domain logic
src/api/routers/                 FastAPI HTTP adapters
src/api/app.py                   app assembly and router registration
src/cli/                         CLI entrypoints and supporting modules
tests/test_api/                  HTTP contract behavior
tests/test_services/             service/domain behavior
tests/test_repositories/         DB helper behavior
tests/test_models/               schema/model behavior
tests/test_cli/                  CLI behavior
```

## Placement Rules

- New HTTP behavior starts with schemas and services, then router wiring.
- Routers should parse HTTP inputs, inject dependencies, translate known
  exceptions to HTTP errors, and return typed response models.
- Services should own orchestration, async workflow, audit/degradation behavior,
  external calls, and domain decisions.
- Repositories should be the place for SQLAlchemy statements. Avoid running
  ad-hoc queries in routers.
- Tables and schemas are different contracts. Do not expose ORM objects as API
  responses unless a schema deliberately models that shape.
- Split a service package when one domain has several cohesive sub-capabilities;
  name files by capability, not by vague technical bucket.

## Naming

- Modules and functions use `snake_case`.
- Pydantic classes use explicit suffixes: `CreateRequest`, `UpdateRequest`,
  `Response`, `ListResponse`, `DetailResponse`.
- Repository functions should read like operations:
  `create_pipeline_run`, `list_pipeline_runs`, `update_scheduler_task`.
- Private helpers use a leading underscore and stay near their owning behavior.
- Avoid catch-all files such as `helpers.py` unless the helper is tiny,
  domain-neutral, and already reused.

## Async And Persistence

- Keep async all the way through FastAPI/service/repository paths.
- Functions that mutate DB state should make transaction ownership clear by
  following nearby patterns.
- Support both Postgres and local sqlite where repository helpers already do.
- Do not log or return secrets. Use existing masking helpers and settings
  contracts.

## Grep Flow

```bash
rg -n "class .*Request|class .*Response|response_model|APIRouter" src/api tests
rg -n "__tablename__|select\\(|update\\(|insert\\(|AsyncSession" src/api/models tests
rg -n "def .*<domain>|async def .*<domain>|<domain>_" src/api tests docs
```

When adding a field, trace it through schema, service, table/repository if
persisted, frontend type if exposed, and tests.

## Validation

Use focused pytest first, then `make test` when the change touches shared
contracts, persistence, runtime dispatch, or more than one module.

## Primary References

- Python Packaging User Guide, src layout vs flat layout:
  https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- Python docs, modules and packages:
  https://docs.python.org/3/tutorial/modules.html
