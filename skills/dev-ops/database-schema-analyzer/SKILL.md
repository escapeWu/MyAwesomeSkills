---
name: database-schema-analyzer
description: analyze postgresql or mysql database schemas from ddl files, schema-only dumps, migration sql, or read-only database metadata. use when the user wants table structure summaries, primary keys, foreign keys, indexes, inferred table relationships, er diagrams, dbml, mermaid erd, schema documentation, or database relationship analysis for postgres/mysql schemas.
---

# Database Schema Analyzer

## Overview

Analyze PostgreSQL and MySQL schemas from DDL, schema-only dumps, migration SQL, or explicit read-only metadata exports. Produce concise schema documentation, table relationship analysis, inferred associations, ER diagrams, Mermaid ERD, and DBML.

Prefer analyzing a schema-only dump or uploaded `.sql` file. Treat direct database connection strings as sensitive and use them only for read-only schema introspection when the user explicitly provides them and the runtime has the required client tools.

## Default workflow

1. Identify the input type:
   - **DDL / schema dump / migration SQL provided or uploaded**: save it to a local file and run `scripts/analyze_schema.py`.
   - **Database connection information**: do not expose credentials. Prefer asking for a schema-only dump. If the user explicitly wants direct introspection and tooling is available, use read-only metadata extraction commands in `references/introspection-guide.md`, save the extracted DDL/metadata locally, then run `scripts/analyze_schema.py`.
   - **Partial schema pasted in chat**: analyze directly when small; for larger input, save to a `.sql` file and run the script.
2. Run the analyzer:
   ```bash
   python scripts/analyze_schema.py input_schema.sql --out schema_analysis
   ```
3. Review generated outputs:
   - `schema_analysis/report.md`
   - `schema_analysis/schema.dbml`
   - `schema_analysis/schema.mmd`
   - `schema_analysis/schema.json`
4. Improve the final answer using judgment:
   - Highlight important tables and modules.
   - Distinguish explicit foreign keys from inferred relationships.
   - Call out missing primary keys, missing foreign keys, suspicious orphan `_id` columns, many-to-many join tables, and high-degree hub tables.
   - Mention parser limitations when the input contains dialect-specific features that may require manual review.

## Script usage

Use `scripts/analyze_schema.py` for repeatable parsing and artifact generation.

```bash
python scripts/analyze_schema.py path/to/schema.sql --out out_dir
```

Optional flags:

```bash
python scripts/analyze_schema.py path/to/schema.sql --out out_dir --dialect postgres
python scripts/analyze_schema.py path/to/schema.sql --out out_dir --no-infer
```

Supported inputs:
- PostgreSQL `CREATE TABLE`, `ALTER TABLE ... FOREIGN KEY`, `CREATE INDEX` statements.
- MySQL `CREATE TABLE`, inline keys, `KEY` / `INDEX`, `CONSTRAINT`, `ENGINE=...` table endings.
- Common schema-only dump formats from `pg_dump --schema-only` and `mysqldump --no-data`.

The parser is intentionally dependency-free and conservative. If it cannot parse a construct, do not invent facts; report that the relevant statement needs manual review.

## Output standards

Use this final response structure unless the user asks for a different format:

```markdown
# Database schema analysis

## Executive summary
[database size, key domains, relationship density, major caveats]

## Table overview
| table | purpose guess | primary key | important columns | notes |

## Relationships
### Explicit foreign keys
| from | to | columns | cardinality guess |

### Inferred relationships
| from | likely to | evidence | confidence |

## ER diagram
[Mermaid ERD code block or link to generated .mmd]

## DBML
[DBML code block or link to generated .dbml]

## Data-model observations
- [missing indexes, missing FKs, join tables, naming inconsistencies, soft-delete columns, audit columns]

## Next steps
- [concrete follow-up checks]
```

Keep relationship confidence explicit:
- **high**: naming convention and referenced table primary key both match, e.g. `orders.user_id -> users.id`.
- **medium**: column name points to an existing table but referenced key is not obvious.
- **low**: only a weak name similarity or ambiguous candidate exists.

## Relationship inference rules

Infer relationships only after listing explicit constraints.

Use these heuristics:
- `table.user_id` likely references `users.id`, `user.id`, or a table whose primary key is `id` and whose normalized name matches `user`.
- `created_by`, `updated_by`, `deleted_by`, `owner_id`, `assignee_id` often reference a user/account table; label as inferred unless explicit.
- A table with two or more foreign keys and a composite unique/primary key over them is likely a many-to-many join table.
- Columns with identical names across tables are not enough by themselves; require `_id`, `*_uuid`, `*_key`, or strong semantic evidence.
- Do not infer self-references unless the column name suggests hierarchy, e.g. `parent_id`, `manager_id`, `referrer_id`.

## Safety and privacy

- Never print full connection strings, passwords, tokens, or hostnames unless the user already made them visible and asks to reproduce them.
- Prefer schema-only dumps over direct production connections.
- For direct connections, use read-only metadata queries only. Do not run migrations, DDL, DML, `ANALYZE`, `VACUUM`, `DROP`, `ALTER`, or any write operation.
- Redact credentials in logs and final answers.
- Do not claim runtime access to a database unless the connection was actually tested in the current session.

## References

- Use `references/report-template.md` for the expected report format and review checklist.
- Use `references/introspection-guide.md` for safe schema extraction from PostgreSQL/MySQL connections.
