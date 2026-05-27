#!/usr/bin/env python3
"""Analyze PostgreSQL/MySQL DDL and generate schema report, DBML, Mermaid ERD, and JSON.

This script is intentionally dependency-free. It is a conservative parser for common
schema-only dumps and migration DDL. It does not execute SQL.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

CONSTRAINT_WORDS = {
    "not", "null", "default", "collate", "comment", "primary", "references",
    "unique", "check", "constraint", "generated", "identity", "auto_increment",
    "on", "character", "charset", "after", "first", "encode", "compression",
}

SKIP_TABLE_PREFIXES = (
    "information_schema.", "pg_catalog.", "mysql.", "performance_schema.", "sys.",
)

TYPE_ALIASES = {
    "int4": "integer",
    "int8": "bigint",
    "serial4": "serial",
    "serial8": "bigserial",
    "bool": "boolean",
    "varchar": "varchar",
}


@dataclass
class Column:
    name: str
    data_type: str = ""
    nullable: bool = True
    default: Optional[str] = None
    is_primary: bool = False
    is_unique: bool = False
    is_generated: bool = False
    raw: str = ""


@dataclass
class Index:
    name: str
    columns: List[str]
    unique: bool = False
    raw: str = ""


@dataclass
class Relationship:
    source_table: str
    source_columns: List[str]
    target_table: str
    target_columns: List[str]
    kind: str = "explicit"
    constraint_name: Optional[str] = None
    confidence: str = "high"
    evidence: str = ""


@dataclass
class Table:
    name: str
    schema: Optional[str] = None
    columns: List[Column] = field(default_factory=list)
    primary_key: List[str] = field(default_factory=list)
    uniques: List[List[str]] = field(default_factory=list)
    indexes: List[Index] = field(default_factory=list)
    raw: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}" if self.schema else self.name


def strip_sql_comments(sql: str) -> str:
    """Remove SQL comments while preserving quoted strings."""
    out: List[str] = []
    i = 0
    n = len(sql)
    in_single = False
    in_double = False
    in_backtick = False
    in_bracket = False
    in_dollar: Optional[str] = None
    while i < n:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < n else ""
        if in_dollar:
            if sql.startswith(in_dollar, i):
                out.append(in_dollar)
                i += len(in_dollar)
                in_dollar = None
            else:
                out.append(ch)
                i += 1
            continue
        if in_single:
            out.append(ch)
            if ch == "'" and nxt == "'":
                out.append(nxt)
                i += 2
            elif ch == "'":
                in_single = False
                i += 1
            else:
                i += 1
            continue
        if in_double:
            out.append(ch)
            if ch == '"' and nxt == '"':
                out.append(nxt)
                i += 2
            elif ch == '"':
                in_double = False
                i += 1
            else:
                i += 1
            continue
        if in_backtick:
            out.append(ch)
            if ch == "`":
                in_backtick = False
            i += 1
            continue
        if in_bracket:
            out.append(ch)
            if ch == "]":
                in_bracket = False
            i += 1
            continue
        if ch == "-" and nxt == "-":
            i += 2
            while i < n and sql[i] not in "\r\n":
                i += 1
            out.append("\n")
            continue
        if ch == "/" and nxt == "*":
            i += 2
            while i + 1 < n and not (sql[i] == "*" and sql[i + 1] == "/"):
                i += 1
            i += 2
            out.append(" ")
            continue
        if ch == "'":
            in_single = True
        elif ch == '"':
            in_double = True
        elif ch == "`":
            in_backtick = True
        elif ch == "[":
            in_bracket = True
        elif ch == "$":
            m = re.match(r"\$[A-Za-z0-9_]*\$", sql[i:])
            if m:
                in_dollar = m.group(0)
                out.append(in_dollar)
                i += len(in_dollar)
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def split_statements(sql: str) -> List[str]:
    statements: List[str] = []
    buf: List[str] = []
    depth = 0
    in_single = in_double = in_backtick = in_bracket = False
    in_dollar: Optional[str] = None
    i = 0
    n = len(sql)
    while i < n:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < n else ""
        if in_dollar:
            if sql.startswith(in_dollar, i):
                buf.append(in_dollar)
                i += len(in_dollar)
                in_dollar = None
            else:
                buf.append(ch)
                i += 1
            continue
        if in_single:
            buf.append(ch)
            if ch == "'" and nxt == "'":
                buf.append(nxt)
                i += 2
            elif ch == "'":
                in_single = False
                i += 1
            else:
                i += 1
            continue
        if in_double:
            buf.append(ch)
            if ch == '"' and nxt == '"':
                buf.append(nxt)
                i += 2
            elif ch == '"':
                in_double = False
                i += 1
            else:
                i += 1
            continue
        if in_backtick:
            buf.append(ch)
            if ch == "`":
                in_backtick = False
            i += 1
            continue
        if in_bracket:
            buf.append(ch)
            if ch == "]":
                in_bracket = False
            i += 1
            continue
        if ch == "'":
            in_single = True
        elif ch == '"':
            in_double = True
        elif ch == "`":
            in_backtick = True
        elif ch == "[":
            in_bracket = True
        elif ch == "$":
            m = re.match(r"\$[A-Za-z0-9_]*\$", sql[i:])
            if m:
                in_dollar = m.group(0)
                buf.append(in_dollar)
                i += len(in_dollar)
                continue
        elif ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        if ch == ";" and depth == 0:
            stmt = "".join(buf).strip()
            if stmt:
                statements.append(stmt)
            buf = []
        else:
            buf.append(ch)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        statements.append(tail)
    return statements


def split_top_level(text: str, delimiter: str = ",") -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    in_single = in_double = in_backtick = in_bracket = False
    i = 0
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if in_single:
            buf.append(ch)
            if ch == "'" and nxt == "'":
                buf.append(nxt)
                i += 2
                continue
            if ch == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            buf.append(ch)
            if ch == '"' and nxt == '"':
                buf.append(nxt)
                i += 2
                continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if in_backtick:
            buf.append(ch)
            if ch == "`":
                in_backtick = False
            i += 1
            continue
        if in_bracket:
            buf.append(ch)
            if ch == "]":
                in_bracket = False
            i += 1
            continue
        if ch == "'":
            in_single = True
        elif ch == '"':
            in_double = True
        elif ch == "`":
            in_backtick = True
        elif ch == "[":
            in_bracket = True
        elif ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        if ch == delimiter and depth == 0:
            part = "".join(buf).strip()
            if part:
                parts.append(part)
            buf = []
        else:
            buf.append(ch)
        i += 1
    part = "".join(buf).strip()
    if part:
        parts.append(part)
    return parts


def clean_identifier(identifier: str) -> str:
    ident = identifier.strip().rstrip(",")
    ident = re.sub(r"\s+", " ", ident)
    if ident.lower().startswith("only "):
        ident = ident[5:].strip()
    pieces = []
    for part in split_qualified_identifier(ident):
        p = part.strip()
        if (p.startswith('"') and p.endswith('"')) or (p.startswith("`") and p.endswith("`")):
            p = p[1:-1].replace('""', '"').replace("``", "`")
        elif p.startswith("[") and p.endswith("]"):
            p = p[1:-1]
        pieces.append(p)
    return ".".join(pieces)


def split_qualified_identifier(identifier: str) -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    in_double = in_backtick = in_bracket = False
    for ch in identifier.strip():
        if in_double:
            buf.append(ch)
            if ch == '"':
                in_double = False
            continue
        if in_backtick:
            buf.append(ch)
            if ch == "`":
                in_backtick = False
            continue
        if in_bracket:
            buf.append(ch)
            if ch == "]":
                in_bracket = False
            continue
        if ch == '"':
            in_double = True
            buf.append(ch)
        elif ch == "`":
            in_backtick = True
            buf.append(ch)
        elif ch == "[":
            in_bracket = True
            buf.append(ch)
        elif ch == ".":
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf).strip())
    return parts


def table_parts(name: str) -> Tuple[Optional[str], str]:
    cleaned = clean_identifier(name)
    parts = cleaned.split(".")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, cleaned


def normalized_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def singularize(name: str) -> str:
    n = name.lower()
    if n.endswith("ies") and len(n) > 3:
        return n[:-3] + "y"
    if n.endswith("ses") and len(n) > 3:
        return n[:-2]
    if n.endswith("s") and not n.endswith("ss") and len(n) > 1:
        return n[:-1]
    return n


def extract_parenthesized_after_keyword(text: str, keyword: str) -> Optional[List[str]]:
    m = re.search(keyword + r"\s*\((.*?)\)", text, re.I | re.S)
    if not m:
        return None
    return [clean_identifier(c) for c in split_top_level(m.group(1))]


def parse_column_list(content: str) -> List[str]:
    return [clean_identifier(re.sub(r"\s+(asc|desc)\b.*$", "", c.strip(), flags=re.I)) for c in split_top_level(content) if c.strip()]


def find_matching_paren(text: str, open_pos: int) -> int:
    depth = 0
    in_single = in_double = in_backtick = in_bracket = False
    i = open_pos
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if in_single:
            if ch == "'" and nxt == "'":
                i += 2
                continue
            if ch == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            if ch == '"' and nxt == '"':
                i += 2
                continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if in_backtick:
            if ch == "`":
                in_backtick = False
            i += 1
            continue
        if in_bracket:
            if ch == "]":
                in_bracket = False
            i += 1
            continue
        if ch == "'":
            in_single = True
        elif ch == '"':
            in_double = True
        elif ch == "`":
            in_backtick = True
        elif ch == "[":
            in_bracket = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def first_identifier_and_rest(text: str) -> Tuple[str, str]:
    s = text.strip()
    if not s:
        return "", ""
    if s[0] in ('"', '`'):
        quote = s[0]
        i = 1
        while i < len(s):
            if s[i] == quote:
                if i + 1 < len(s) and s[i + 1] == quote:
                    i += 2
                    continue
                return clean_identifier(s[: i + 1]), s[i + 1 :].strip()
            i += 1
    if s[0] == "[":
        end = s.find("]")
        if end != -1:
            return clean_identifier(s[: end + 1]), s[end + 1 :].strip()
    m = re.match(r"([^\s]+)(.*)$", s, re.S)
    if not m:
        return clean_identifier(s), ""
    return clean_identifier(m.group(1)), m.group(2).strip()


def parse_data_type(rest: str) -> str:
    tokens = []
    buf = []
    depth = 0
    for ch in rest.strip():
        if ch.isspace() and depth == 0:
            if buf:
                tokens.append("".join(buf))
                buf = []
        else:
            if ch == "(":
                depth += 1
            elif ch == ")" and depth > 0:
                depth -= 1
            buf.append(ch)
    if buf:
        tokens.append("".join(buf))
    dtype_parts: List[str] = []
    i = 0
    while i < len(tokens):
        low = tokens[i].lower().strip(",")
        if low in CONSTRAINT_WORDS:
            break
        # Preserve common multi-word types.
        dtype_parts.append(tokens[i].strip(","))
        if "(" in tokens[i] and ")" not in tokens[i]:
            while i + 1 < len(tokens) and ")" not in tokens[i]:
                i += 1
                dtype_parts.append(tokens[i].strip(","))
        i += 1
    dtype = " ".join(dtype_parts).strip()
    return TYPE_ALIASES.get(dtype.lower(), dtype)


def parse_default(rest: str) -> Optional[str]:
    m = re.search(r"\bdefault\b\s+(.+?)(?=\s+\b(?:not|null|primary|unique|references|check|constraint|comment|collate|generated|auto_increment)\b|$)", rest, re.I | re.S)
    if not m:
        return None
    return re.sub(r"\s+", " ", m.group(1).strip().rstrip(","))


def parse_foreign_key(text: str, source_table: str, constraint_name: Optional[str] = None) -> Optional[Relationship]:
    m = re.search(
        r"foreign\s+key\s*\((?P<src>.*?)\)\s+references\s+(?P<target>(?:\"[^\"]+\"|`[^`]+`|\[[^\]]+\]|[\w.]+)+)\s*(?:\((?P<tgt>.*?)\))?",
        text,
        re.I | re.S,
    )
    if not m:
        return None
    src_cols = parse_column_list(m.group("src"))
    target = clean_identifier(m.group("target"))
    tgt_cols = parse_column_list(m.group("tgt")) if m.group("tgt") else ["id"]
    return Relationship(
        source_table=source_table,
        source_columns=src_cols,
        target_table=target,
        target_columns=tgt_cols,
        kind="explicit",
        constraint_name=constraint_name,
        confidence="high",
        evidence="foreign key constraint",
    )


def parse_table_constraint(item: str, table: Table, relationships: List[Relationship]) -> bool:
    text = item.strip().rstrip(",")
    constraint_name = None
    m_cons = re.match(r"constraint\s+([^\s]+)\s+(.*)$", text, re.I | re.S)
    if m_cons:
        constraint_name = clean_identifier(m_cons.group(1))
        text = m_cons.group(2).strip()
    low = text.lower()
    if low.startswith("primary key"):
        cols = extract_parenthesized_after_keyword(text, r"primary\s+key") or []
        table.primary_key = cols
        return True
    if low.startswith("unique") or low.startswith("unique key") or low.startswith("unique index"):
        cols = extract_parenthesized_after_keyword(text, r"unique(?:\s+(?:key|index))?(?:\s+[^\s(]+)?") or []
        if cols:
            table.uniques.append(cols)
            table.indexes.append(Index(name=constraint_name or "unique_" + "_".join(cols), columns=cols, unique=True, raw=item))
        return True
    if "foreign key" in low and "references" in low:
        rel = parse_foreign_key(text, table.full_name, constraint_name)
        if rel:
            relationships.append(rel)
        return True
    if low.startswith(("key ", "index ", "fulltext key", "fulltext index", "spatial key", "spatial index")):
        unique = low.startswith("unique")
        m = re.search(r"(?:key|index)\s+([^\s(]+)?\s*\((.*?)\)", text, re.I | re.S)
        if m:
            name = clean_identifier(m.group(1) or "idx_" + table.name)
            cols = parse_column_list(m.group(2))
            table.indexes.append(Index(name=name, columns=cols, unique=unique, raw=item))
        return True
    return False


def parse_column(item: str, table: Table, relationships: List[Relationship]) -> Optional[Column]:
    name, rest = first_identifier_and_rest(item)
    if not name:
        return None
    low_name = name.lower()
    if low_name in {"primary", "foreign", "unique", "constraint", "key", "index", "check"}:
        return None
    rest_low = rest.lower()
    col = Column(
        name=name,
        data_type=parse_data_type(rest),
        nullable=not bool(re.search(r"\bnot\s+null\b", rest, re.I)),
        default=parse_default(rest),
        is_primary=bool(re.search(r"\bprimary\s+key\b", rest, re.I)),
        is_unique=bool(re.search(r"\bunique\b", rest, re.I)),
        is_generated=bool(re.search(r"\b(generated|identity|auto_increment|serial)\b", rest, re.I)),
        raw=item.strip(),
    )
    if col.is_primary and name not in table.primary_key:
        table.primary_key.append(name)
        col.nullable = False
    if col.is_unique:
        table.uniques.append([name])
    m_ref = re.search(r"\breferences\s+((?:\"[^\"]+\"|`[^`]+`|\[[^\]]+\]|[\w.]+)+)\s*(?:\((.*?)\))?", rest, re.I | re.S)
    if m_ref:
        target = clean_identifier(m_ref.group(1))
        tgt_cols = parse_column_list(m_ref.group(2)) if m_ref.group(2) else ["id"]
        relationships.append(Relationship(
            source_table=table.full_name,
            source_columns=[name],
            target_table=target,
            target_columns=tgt_cols,
            kind="explicit",
            confidence="high",
            evidence="inline references clause",
        ))
    return col


def parse_create_table(stmt: str, relationships: List[Relationship]) -> Optional[Table]:
    m = re.search(r"create\s+(?:temporary\s+|temp\s+|unlogged\s+)?table\s+(?:if\s+not\s+exists\s+)?", stmt, re.I)
    if not m:
        return None
    open_pos = stmt.find("(", m.end())
    if open_pos == -1:
        return None
    table_name = stmt[m.end():open_pos].strip()
    schema, name = table_parts(table_name)
    full = f"{schema}.{name}" if schema else name
    if any(full.lower().startswith(prefix) for prefix in SKIP_TABLE_PREFIXES):
        return None
    close_pos = find_matching_paren(stmt, open_pos)
    if close_pos == -1:
        return None
    body = stmt[open_pos + 1:close_pos]
    table = Table(name=name, schema=schema, raw=stmt)
    for item in split_top_level(body):
        if parse_table_constraint(item, table, relationships):
            continue
        col = parse_column(item, table, relationships)
        if col:
            table.columns.append(col)
    pk_set = set(table.primary_key)
    for col in table.columns:
        if col.name in pk_set:
            col.is_primary = True
            col.nullable = False
    return table


def parse_alter_table(stmt: str, tables: Dict[str, Table], relationships: List[Relationship]) -> None:
    m = re.search(r"alter\s+table\s+(?:only\s+)?(?P<table>(?:\"[^\"]+\"|`[^`]+`|\[[^\]]+\]|[\w.]+)+)\s+(?P<rest>.*)$", stmt, re.I | re.S)
    if not m:
        return
    table_name = clean_identifier(m.group("table"))
    rest = m.group("rest")
    constraint_name = None
    m_cons = re.search(r"add\s+constraint\s+([^\s]+)\s+(.*)$", rest, re.I | re.S)
    if m_cons:
        constraint_name = clean_identifier(m_cons.group(1))
        rest2 = m_cons.group(2)
    else:
        rest2 = rest
    low = rest2.lower()
    tbl = tables.get(table_name) or tables.get(table_name.split(".")[-1])
    if "foreign key" in low and "references" in low:
        rel = parse_foreign_key(rest2, table_name, constraint_name)
        if rel:
            relationships.append(rel)
    elif "primary key" in low:
        cols = extract_parenthesized_after_keyword(rest2, r"primary\s+key") or []
        if tbl and cols:
            tbl.primary_key = cols
            for c in tbl.columns:
                if c.name in cols:
                    c.is_primary = True
                    c.nullable = False
    elif low.strip().startswith(("add unique", "unique")):
        cols = extract_parenthesized_after_keyword(rest2, r"unique(?:\s+key)?") or []
        if tbl and cols:
            tbl.uniques.append(cols)


def parse_create_index(stmt: str, tables: Dict[str, Table]) -> None:
    m = re.search(
        r"create\s+(?P<unique>unique\s+)?index\s+(?:concurrently\s+)?(?:if\s+not\s+exists\s+)?(?P<name>[^\s]+)\s+on\s+(?P<table>(?:\"[^\"]+\"|`[^`]+`|\[[^\]]+\]|[\w.]+)+)(?:\s+using\s+\w+)?\s*\((?P<cols>.*?)\)",
        stmt,
        re.I | re.S,
    )
    if not m:
        return
    table_name = clean_identifier(m.group("table"))
    tbl = tables.get(table_name) or tables.get(table_name.split(".")[-1])
    if not tbl:
        return
    cols = parse_column_list(m.group("cols"))
    tbl.indexes.append(Index(name=clean_identifier(m.group("name")), columns=cols, unique=bool(m.group("unique")), raw=stmt))


def parse_schema(sql: str) -> Tuple[Dict[str, Table], List[Relationship], List[str]]:
    cleaned = strip_sql_comments(sql)
    statements = split_statements(cleaned)
    tables: Dict[str, Table] = {}
    relationships: List[Relationship] = []
    unparsed: List[str] = []
    for stmt in statements:
        s = stmt.strip()
        if not s:
            continue
        low = s.lower()
        if re.search(r"\bcreate\s+(?:temporary\s+|temp\s+|unlogged\s+)?table\b", low):
            table = parse_create_table(s, relationships)
            if table:
                tables[table.full_name] = table
                if table.name not in tables:
                    tables[table.name] = table
            else:
                unparsed.append(s[:300])
    # Deduplicate table aliases into primary dictionary.
    primary_tables: Dict[str, Table] = {t.full_name: t for t in set(tables.values())} if False else {}
    for t in list(tables.values()):
        primary_tables[t.full_name] = t
    tables = primary_tables
    alias: Dict[str, Table] = {}
    for t in tables.values():
        alias[t.full_name] = t
        alias[t.name] = t
    for stmt in statements:
        s = stmt.strip()
        low = s.lower()
        if low.startswith("alter table"):
            parse_alter_table(s, alias, relationships)
        elif low.startswith("create index") or low.startswith("create unique index"):
            parse_create_index(s, alias)
    return tables, dedupe_relationships(relationships), unparsed


def dedupe_relationships(rels: Sequence[Relationship]) -> List[Relationship]:
    seen = set()
    result = []
    for r in rels:
        key = (r.source_table, tuple(r.source_columns), r.target_table, tuple(r.target_columns), r.kind)
        if key in seen:
            continue
        seen.add(key)
        result.append(r)
    return result


def table_lookup_variants(tables: Dict[str, Table]) -> Dict[str, Table]:
    variants: Dict[str, Table] = {}
    for table in tables.values():
        names = {table.name, table.full_name, singularize(table.name), table.name.rstrip("s")}
        for name in names:
            variants[normalized_name(name)] = table
    return variants


def explicit_fk_columns(rels: Sequence[Relationship]) -> set[Tuple[str, str]]:
    cols = set()
    for r in rels:
        if r.kind == "explicit":
            for c in r.source_columns:
                cols.add((r.source_table, c))
    return cols


def infer_relationships(tables: Dict[str, Table], explicit_rels: Sequence[Relationship]) -> List[Relationship]:
    variants = table_lookup_variants(tables)
    pk_by_table = {t.full_name: (t.primary_key or ["id"] if any(c.name == "id" for c in t.columns) else t.primary_key) for t in tables.values()}
    existing = explicit_fk_columns(explicit_rels)
    rels: List[Relationship] = []
    user_like = [t for t in tables.values() if normalized_name(t.name) in {"user", "users", "account", "accounts", "member", "members"}]
    for table in tables.values():
        for col in table.columns:
            if (table.full_name, col.name) in existing:
                continue
            cname = col.name.lower()
            candidates: List[Tuple[Table, str, str]] = []
            base = None
            if cname.endswith("_id"):
                base = cname[:-3]
            elif cname.endswith("_uuid"):
                base = cname[:-5]
            elif cname.endswith("_key"):
                base = cname[:-4]
            elif cname in {"created_by", "updated_by", "deleted_by", "owner_id", "assignee_id", "user_id"} and user_like:
                candidates.extend((u, "medium", f"audit/user-like column {col.name}") for u in user_like)
            if base:
                base_norm = normalized_name(base)
                base_sing = normalized_name(singularize(base))
                for key in {base_norm, base_sing, normalized_name(base + "s")}:
                    if key in variants:
                        candidates.append((variants[key], "high", f"column name {col.name} matches table {variants[key].name}"))
            # Parent self-reference.
            if cname in {"parent_id", "manager_id", "referrer_id", "referred_by_id"}:
                candidates.append((table, "medium", f"hierarchy-like column {col.name}"))
            if not candidates:
                continue
            # Choose the best non-self candidate unless self-reference is explicit by name.
            chosen = None
            for cand in candidates:
                if cand[0].full_name != table.full_name or cname in {"parent_id", "manager_id", "referrer_id", "referred_by_id"}:
                    chosen = cand
                    break
            if not chosen:
                continue
            target, confidence, evidence = chosen
            target_cols = pk_by_table.get(target.full_name) or ["id"]
            rels.append(Relationship(
                source_table=table.full_name,
                source_columns=[col.name],
                target_table=target.full_name,
                target_columns=target_cols[:1],
                kind="inferred",
                confidence=confidence,
                evidence=evidence,
            ))
    return dedupe_relationships(rels)


def detect_join_tables(tables: Dict[str, Table], relationships: Sequence[Relationship]) -> List[str]:
    by_source: Dict[str, List[Relationship]] = {}
    for r in relationships:
        by_source.setdefault(r.source_table, []).append(r)
    join_tables = []
    for table in tables.values():
        rels = by_source.get(table.full_name, [])
        if len(rels) < 2:
            continue
        fk_cols = {c for r in rels for c in r.source_columns}
        pk_set = set(table.primary_key)
        has_composite_key = len(pk_set) >= 2 and fk_cols.issuperset(pk_set)
        has_unique_pair = any(len(u) >= 2 and fk_cols.issuperset(set(u)) for u in table.uniques)
        mostly_fk_cols = len(fk_cols) >= 2 and len(table.columns) <= len(fk_cols) + 3
        if has_composite_key or has_unique_pair or mostly_fk_cols:
            join_tables.append(table.full_name)
    return sorted(set(join_tables))


def to_json(tables: Dict[str, Table], relationships: Sequence[Relationship], inferred: Sequence[Relationship], unparsed: Sequence[str]) -> dict:
    unique_tables = sorted(tables.values(), key=lambda t: t.full_name)
    all_rels = list(relationships) + list(inferred)
    table_dicts = []
    for t in unique_tables:
        d = asdict(t)
        d["full_name"] = t.full_name
        table_dicts.append(d)
    return {
        "tables": table_dicts,
        "relationships": [asdict(r) for r in all_rels],
        "join_tables": detect_join_tables(tables, all_rels),
        "unparsed_statements_sample": list(unparsed[:20]),
        "counts": {
            "tables": len(unique_tables),
            "columns": sum(len(t.columns) for t in unique_tables),
            "explicit_relationships": len(relationships),
            "inferred_relationships": len(inferred),
            "indexes": sum(len(t.indexes) for t in unique_tables),
        },
    }


def dbml_type(dtype: str) -> str:
    return dtype or "unknown"


def quote_dbml_name(name: str) -> str:
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
        return name
    return f'"{name}"'


def generate_dbml(tables: Dict[str, Table], relationships: Sequence[Relationship]) -> str:
    lines: List[str] = ["// Generated by database-schema-analyzer", ""]
    for table in sorted(tables.values(), key=lambda t: t.full_name):
        lines.append(f"Table {quote_dbml_name(table.full_name)} {{")
        pk_set = set(table.primary_key)
        unique_single = {u[0] for u in table.uniques if len(u) == 1}
        for col in table.columns:
            opts = []
            if col.name in pk_set:
                opts.append("pk")
            if not col.nullable:
                opts.append("not null")
            if col.name in unique_single or col.is_unique:
                opts.append("unique")
            opt = f" [{', '.join(opts)}]" if opts else ""
            lines.append(f"  {quote_dbml_name(col.name)} {dbml_type(col.data_type)}{opt}")
        if table.indexes:
            lines.append("  indexes {")
            for idx in table.indexes:
                cols = ", ".join(quote_dbml_name(c) for c in idx.columns)
                opt = " [unique]" if idx.unique else ""
                lines.append(f"    ({cols}){opt}")
            lines.append("  }")
        lines.append("}")
        lines.append("")
    for rel in relationships:
        note = " // inferred" if rel.kind == "inferred" else ""
        src_col = rel.source_columns[0] if rel.source_columns else "id"
        tgt_col = rel.target_columns[0] if rel.target_columns else "id"
        lines.append(
            f"Ref: {quote_dbml_name(rel.source_table)}.{quote_dbml_name(src_col)} > "
            f"{quote_dbml_name(rel.target_table)}.{quote_dbml_name(tgt_col)}{note}"
        )
    lines.append("")
    return "\n".join(lines)


def mermaid_entity_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", name)


def generate_mermaid(tables: Dict[str, Table], relationships: Sequence[Relationship]) -> str:
    lines = ["erDiagram"]
    for table in sorted(tables.values(), key=lambda t: t.full_name):
        ename = mermaid_entity_name(table.full_name)
        lines.append(f"  {ename} {{")
        pk_set = set(table.primary_key)
        for col in table.columns:
            dtype = re.sub(r"\s+", "_", col.data_type or "unknown")
            marker = " PK" if col.name in pk_set else ""
            safe_col = re.sub(r"[^A-Za-z0-9_]", "_", col.name)
            lines.append(f"    {dtype} {safe_col}{marker}")
        lines.append("  }")
    for rel in relationships:
        left = mermaid_entity_name(rel.target_table)
        right = mermaid_entity_name(rel.source_table)
        label = "_".join(rel.source_columns) if rel.source_columns else "fk"
        if rel.kind == "inferred":
            label = f"inferred_{label}"
        lines.append(f"  {left} ||--o{{ {right} : \"{label}\"")
    return "\n".join(lines) + "\n"


def guess_table_purpose(table: Table) -> str:
    n = table.name.lower()
    if any(x in n for x in ["user", "account", "member", "customer"]):
        return "actor/account entity"
    if any(x in n for x in ["order", "trade", "transaction", "payment", "invoice"]):
        return "transactional entity"
    if any(x in n for x in ["log", "event", "audit", "history"]):
        return "event/audit table"
    if any(x in n for x in ["mapping", "map", "join", "link"]):
        return "association table"
    if table.name.endswith("s"):
        return "core entity"
    return "table role unclear"


def generate_report(data: dict) -> str:
    counts = data["counts"]
    tables = data["tables"]
    rels = data["relationships"]
    explicit = [r for r in rels if r["kind"] == "explicit"]
    inferred = [r for r in rels if r["kind"] == "inferred"]
    lines: List[str] = []
    lines.append("# Database schema analysis")
    lines.append("")
    lines.append("## Executive summary")
    lines.append(
        f"Analyzed {counts['tables']} tables, {counts['columns']} columns, "
        f"{counts['explicit_relationships']} explicit relationships, "
        f"{counts['inferred_relationships']} inferred relationships, and {counts['indexes']} indexes."
    )
    if data["join_tables"]:
        lines.append("Likely join tables: " + ", ".join(data["join_tables"]) + ".")
    if data["unparsed_statements_sample"]:
        lines.append("Some statements were not parsed; review `schema.json` for samples.")
    lines.append("")
    lines.append("## Table overview")
    lines.append("| table | columns | primary key | purpose guess | notes |")
    lines.append("|---|---:|---|---|---|")
    for t in tables:
        pk = ", ".join(t["primary_key"]) if t["primary_key"] else "-"
        notes = []
        if not t["primary_key"]:
            notes.append("missing pk")
        if len(t["columns"]) > 40:
            notes.append("wide table")
        if not t["indexes"]:
            notes.append("no parsed indexes")
        role = guess_table_purpose(Table(name=t["name"], schema=t.get("schema")))
        lines.append(f"| {t['full_name']} | {len(t['columns'])} | {pk} | {role} | {', '.join(notes) or '-'} |")
    lines.append("")
    lines.append("## Explicit foreign keys")
    if explicit:
        lines.append("| from | to | constraint | evidence |")
        lines.append("|---|---|---|---|")
        for r in explicit:
            src = f"{r['source_table']}.{', '.join(r['source_columns'])}"
            tgt = f"{r['target_table']}.{', '.join(r['target_columns'])}"
            lines.append(f"| {src} | {tgt} | {r.get('constraint_name') or '-'} | {r.get('evidence') or 'constraint'} |")
    else:
        lines.append("No explicit foreign keys were parsed.")
    lines.append("")
    lines.append("## Inferred relationships")
    if inferred:
        lines.append("| from | likely to | confidence | evidence |")
        lines.append("|---|---|---|---|")
        for r in inferred:
            src = f"{r['source_table']}.{', '.join(r['source_columns'])}"
            tgt = f"{r['target_table']}.{', '.join(r['target_columns'])}"
            lines.append(f"| {src} | {tgt} | {r['confidence']} | {r.get('evidence') or '-'} |")
    else:
        lines.append("No inferred relationships were found.")
    lines.append("")
    lines.append("## Data-model observations")
    missing_pk = [t["full_name"] for t in tables if not t["primary_key"]]
    if missing_pk:
        lines.append("- Tables without parsed primary keys: " + ", ".join(missing_pk[:20]) + ("..." if len(missing_pk) > 20 else ""))
    if inferred:
        lines.append("- Inferred relationships should be validated against application code or production metadata before being treated as constraints.")
    fk_cols = {(r["source_table"], tuple(r["source_columns"])) for r in explicit}
    indexed = set()
    for t in tables:
        for idx in t["indexes"]:
            indexed.add((t["full_name"], tuple(idx["columns"][: len(idx["columns"])])))
    unindexed_fk = []
    for r in explicit:
        key = (r["source_table"], tuple(r["source_columns"]))
        if not any(k[0] == key[0] and list(key[1]) == list(k[1])[: len(key[1])] for k in indexed):
            unindexed_fk.append(f"{r['source_table']}.{', '.join(r['source_columns'])}")
    if unindexed_fk:
        lines.append("- Parsed foreign keys without an obvious matching index: " + ", ".join(unindexed_fk[:20]) + ("..." if len(unindexed_fk) > 20 else ""))
    if not missing_pk and not inferred and not unindexed_fk:
        lines.append("- No obvious structural issues were detected by the conservative parser.")
    lines.append("")
    lines.append("## Generated artifacts")
    lines.append("- `schema.dbml`: DBML table and relationship model.")
    lines.append("- `schema.mmd`: Mermaid ER diagram.")
    lines.append("- `schema.json`: machine-readable parsed schema.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(input_path: Path, out_dir: Path, dialect: Optional[str], infer: bool) -> None:
    sql = input_path.read_text(encoding="utf-8", errors="replace")
    tables, explicit_rels, unparsed = parse_schema(sql)
    inferred_rels = infer_relationships(tables, explicit_rels) if infer else []
    all_rels = explicit_rels + inferred_rels
    data = to_json(tables, explicit_rels, inferred_rels, unparsed)
    data["dialect"] = dialect or "auto"
    data["source_file"] = str(input_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "schema.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "schema.dbml").write_text(generate_dbml(tables, all_rels), encoding="utf-8")
    (out_dir / "schema.mmd").write_text(generate_mermaid(tables, all_rels), encoding="utf-8")
    (out_dir / "report.md").write_text(generate_report(data), encoding="utf-8")
    print(f"Wrote {out_dir / 'report.md'}")
    print(f"Wrote {out_dir / 'schema.dbml'}")
    print(f"Wrote {out_dir / 'schema.mmd'}")
    print(f"Wrote {out_dir / 'schema.json'}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze PostgreSQL/MySQL DDL and generate schema docs.")
    parser.add_argument("input", type=Path, help="DDL/schema SQL file")
    parser.add_argument("--out", type=Path, default=Path("schema_analysis"), help="output directory")
    parser.add_argument("--dialect", choices=["postgres", "mysql", "auto"], default="auto", help="SQL dialect hint")
    parser.add_argument("--no-infer", action="store_true", help="disable inferred relationship detection")
    args = parser.parse_args(argv)
    if not args.input.exists():
        parser.error(f"input file not found: {args.input}")
    write_outputs(args.input, args.out, args.dialect, infer=not args.no_infer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
