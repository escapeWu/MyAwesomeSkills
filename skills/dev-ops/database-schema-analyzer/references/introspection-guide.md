# Safe Database Introspection Guide

Prefer uploaded schema-only dumps. Direct database connections should be used only when the user explicitly provides connection information and wants direct introspection.

## PostgreSQL schema-only dump

Recommended command when `pg_dump` is available:

```bash
pg_dump "$DATABASE_URL" --schema-only --no-owner --no-privileges > schema.sql
```

Alternative psql metadata query for tables, columns, primary keys, and foreign keys:

```sql
select table_schema, table_name, column_name, data_type, is_nullable, column_default
from information_schema.columns
where table_schema not in ('pg_catalog', 'information_schema')
order by table_schema, table_name, ordinal_position;
```

## MySQL schema-only dump

Recommended command when `mysqldump` is available:

```bash
mysqldump --no-data --skip-comments --single-transaction --set-gtid-purged=OFF "$DATABASE_NAME" > schema.sql
```

For URL-based credentials, prefer a redacted local environment variable rather than writing credentials into shell history.

## Rules for direct connections

- Use read-only credentials when possible.
- Run metadata extraction only.
- Do not execute write operations.
- Redact credentials in final answers and logs.
- If tools are unavailable or the connection fails, ask the user for a schema-only dump instead of guessing.
