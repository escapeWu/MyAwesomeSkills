#!/usr/bin/env python3
"""Produce a deterministic extraction inventory for one Python module."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any


DECLARATION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def target_names(target: ast.expr) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        return [name for item in target.elts for name in target_names(item)]
    return []


def assigned_names(node: ast.Assign | ast.AnnAssign) -> list[str]:
    if isinstance(node, ast.Assign):
        return [name for target in node.targets for name in target_names(target)]
    return target_names(node.target)


def imported_names(node: ast.Import | ast.ImportFrom) -> list[str]:
    names: list[str] = []
    for alias in node.names:
        if alias.asname:
            names.append(alias.asname)
        elif isinstance(node, ast.Import):
            names.append(alias.name.split(".", 1)[0])
        else:
            names.append(alias.name)
    return names


def import_source(node: ast.Import | ast.ImportFrom) -> str:
    if isinstance(node, ast.Import):
        return ", ".join(alias.name for alias in node.names)
    prefix = "." * node.level
    module = node.module or ""
    return f"{prefix}{module}: " + ", ".join(alias.name for alias in node.names)


def referenced_names(node: ast.AST) -> set[str]:
    return {
        child.id
        for child in ast.walk(node)
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)
    }


def line_span(node: ast.AST) -> tuple[int, int, int]:
    start = getattr(node, "lineno", 0)
    end = getattr(node, "end_lineno", start)
    return start, end, max(0, end - start + 1)


def symbol_kind(node: ast.AST) -> str:
    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"
    if isinstance(node, ast.FunctionDef):
        return "function"
    if isinstance(node, ast.ClassDef):
        return "class"
    return "assignment"


def inventory(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    imports: list[dict[str, Any]] = []
    declaration_nodes: list[ast.AST] = []
    assignments: list[dict[str, Any]] = []
    side_effects: list[dict[str, Any]] = []
    top_level_names: set[str] = set()

    for index, node in enumerate(tree.body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(
                {
                    "line": node.lineno,
                    "source": import_source(node),
                    "bound_names": imported_names(node),
                }
            )
            continue
        if isinstance(node, DECLARATION_NODES):
            declaration_nodes.append(node)
            top_level_names.add(node.name)
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            names = assigned_names(node)
            start, end, lines = line_span(node)
            assignments.append(
                {
                    "names": names,
                    "line_start": start,
                    "line_end": end,
                    "lines": lines,
                    "constant_style": bool(names) and all(name.isupper() for name in names),
                }
            )
            top_level_names.update(names)
            continue
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                continue
        start, end, lines = line_span(node)
        side_effects.append(
            {
                "kind": type(node).__name__,
                "line_start": start,
                "line_end": end,
                "lines": lines,
            }
        )

    symbols: list[dict[str, Any]] = []
    for node in declaration_nodes:
        start, end, lines = line_span(node)
        dependencies = sorted((referenced_names(node) & top_level_names) - {node.name})
        record: dict[str, Any] = {
            "name": node.name,
            "kind": symbol_kind(node),
            "public": not node.name.startswith("_"),
            "line_start": start,
            "line_end": end,
            "lines": lines,
            "local_dependencies": dependencies,
        }
        if isinstance(node, ast.ClassDef):
            record["methods"] = [
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            record["bases"] = [ast.unparse(base) for base in node.bases]
        symbols.append(record)

    return {
        "path": str(path),
        "physical_lines": len(source.splitlines()),
        "imports": imports,
        "symbols": symbols,
        "assignments": assignments,
        "module_side_effects": side_effects,
    }


def markdown(report: dict[str, Any]) -> str:
    output = [
        f"# Python module inventory: `{report['path']}`",
        "",
        f"- Physical lines: `{report['physical_lines']}`",
        f"- Imports: `{len(report['imports'])}`",
        f"- Declarations: `{len(report['symbols'])}`",
        f"- Assignments: `{len(report['assignments'])}`",
        f"- Module side-effect candidates: `{len(report['module_side_effects'])}`",
        "",
        "## Declarations",
        "",
        "| Symbol | Kind | Lines | Span | Local dependencies |",
        "|---|---|---:|---|---|",
    ]
    for symbol in report["symbols"]:
        dependencies = ", ".join(symbol["local_dependencies"]) or "-"
        output.append(
            f"| `{symbol['name']}` | {symbol['kind']} | {symbol['lines']} | "
            f"{symbol['line_start']}-{symbol['line_end']} | {dependencies} |"
        )

    output.extend(["", "## Module-level assignments", ""])
    if report["assignments"]:
        for assignment in report["assignments"]:
            label = ", ".join(assignment["names"]) or "<complex target>"
            style = "constant-style" if assignment["constant_style"] else "mutable/state review"
            output.append(f"- `{label}` at {assignment['line_start']}: {style}")
    else:
        output.append("- None")

    output.extend(["", "## Module side-effect candidates", ""])
    if report["module_side_effects"]:
        for effect in report["module_side_effects"]:
            output.append(f"- `{effect['kind']}` at {effect['line_start']}-{effect['line_end']}")
    else:
        output.append("- None")

    output.extend(
        [
            "",
            "> AST output is an inventory, not a complete call graph. Confirm consumers, dynamic",
            "> imports, monkeypatch paths, serialization paths, I/O, and mutable state with `rg`.",
        ]
    )
    return "\n".join(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Python module to inspect")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.path.is_file():
        raise SystemExit(f"not a file: {args.path}")
    report = inventory(args.path)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
