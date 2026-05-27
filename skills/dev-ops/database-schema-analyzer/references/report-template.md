# Database Schema Analysis Report Template

Use this template after running `scripts/analyze_schema.py` or manually analyzing a schema.

## Required sections

1. **Executive summary**
   - Number of tables, explicit relationships, inferred relationships, and indexes.
   - Main schema domains, based on table names and relationship clusters.
   - Key caveats about partial input, parser limitations, missing constraints, or inferred-only relationships.

2. **Table overview**
   - Table name.
   - Primary key.
   - Important columns.
   - Table role guess, stated as a guess when not documented.
   - Quality notes such as missing PK, no timestamps, or unusually wide table.

3. **Relationships**
   - Separate explicit FKs from inferred FKs.
   - Include evidence for inferred relationships.
   - Identify join tables and hub tables.

4. **ER diagram**
   - Prefer Mermaid ERD when responding inline.
   - Attach or link generated `.mmd` when output is too large.

5. **DBML**
   - Provide generated DBML or attach `schema.dbml`.
   - Preserve explicit relationships and mark inferred relationships with comments.

6. **Data model observations**
   - Missing constraints.
   - Missing supporting indexes on foreign key columns.
   - Naming inconsistencies.
   - Nullable foreign keys that might indicate optional relationships.
   - Soft-delete/audit patterns.

7. **Next steps**
   - Recommend concrete validation queries, stakeholder questions, or migration cleanup tasks.

## Tone

Be direct and practical. Separate facts from guesses. Use words like "explicit", "inferred", and "likely" carefully.
