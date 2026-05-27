#!/usr/bin/env python3
"""Bootstrap project-specific development standards for an existing repository.

This script inventories a local repository, creates docs/ai-dev-standards scaffolding,
and optionally updates existing AGENTS.md / CLAUDE.md files with a managed context
routing block. It intentionally does not infer final rules; a coding agent should
inspect evidence and fill standards from real source files.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable

IGNORE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", ".next",
    ".nuxt", ".svelte-kit", ".turbo", ".cache", ".venv", "venv", "env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "coverage",
    ".idea", ".vscode", "target", "out", "tmp", "logs",
}

TEXT_EXTS = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py", ".go", ".rs", ".java",
    ".kt", ".kts", ".rb", ".php", ".cs", ".swift", ".c", ".cpp", ".h", ".hpp",
    ".sql", ".graphql", ".gql", ".json", ".yaml", ".yml", ".toml", ".ini", ".env",
    ".md", ".mdx", ".html", ".css", ".scss", ".sass", ".vue", ".svelte",
    ".xml", ".gradle", ".properties", ".sh", ".bash", ".zsh", ".ps1", ".dockerfile",
}

DOC_NAMES = [
    "00-overview.md",
    "01-architecture.md",
    "02-backend.md",
    "03-frontend.md",
    "04-database.md",
    "05-testing.md",
    "06-code-review-checklist.md",
    "07-agent-instructions.md",
]

MANAGED_START = "<!-- project-dev-standards:start -->"
MANAGED_END = "<!-- project-dev-standards:end -->"

AGENT_BLOCK = f"""{MANAGED_START}

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

{MANAGED_END}
"""


def is_text_candidate(path: Path) -> bool:
    if path.name in {"Dockerfile", "Makefile", "Procfile", "Gemfile", "Rakefile"}:
        return True
    if path.suffix.lower() in TEXT_EXTS:
        return True
    if path.name.startswith(".env"):
        return True
    return False


def iter_files(root: Path, max_files: int) -> Iterable[Path]:
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        current = Path(dirpath)
        for filename in sorted(filenames):
            path = current / filename
            if not is_text_candidate(path):
                continue
            try:
                if path.stat().st_size > 512_000:
                    continue
            except OSError:
                continue
            yield path
            count += 1
            if count >= max_files:
                return


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def detect_stack(root: Path) -> dict[str, list[str]]:
    signals: dict[str, list[str]] = {
        "javascript_typescript": [],
        "python": [],
        "go": [],
        "rust": [],
        "java_jvm": [],
        "php": [],
        "database": [],
        "testing": [],
        "ci_cd": [],
        "agent_instructions": [],
    }
    candidates = {
        "javascript_typescript": ["package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "tsconfig.json", "vite.config.ts", "next.config.js", "next.config.mjs"],
        "python": ["pyproject.toml", "requirements.txt", "setup.py", "poetry.lock", "Pipfile"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "java_jvm": ["pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"],
        "php": ["composer.json", "composer.lock"],
        "database": ["prisma/schema.prisma", "drizzle.config.ts", "knexfile.js", "alembic.ini", "db/schema.rb"],
        "ci_cd": [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", "Dockerfile", "docker-compose.yml", "Makefile"],
        "agent_instructions": ["AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md"],
    }
    for area, names in candidates.items():
        for name in names:
            p = root / name
            if p.exists():
                signals[area].append(name)
    for file in iter_files(root, 2000):
        rp = rel(root, file).lower()
        if any(part in rp for part in ["test", "spec", "__tests__", "pytest", "vitest", "jest", "playwright", "cypress"]):
            signals["testing"].append(rel(root, file))
        if any(part in rp for part in ["migration", "migrations", "schema", "prisma", "alembic"]):
            signals["database"].append(rel(root, file))
    for key in list(signals):
        signals[key] = sorted(dict.fromkeys(signals[key]))[:40]
    return signals


def classify_files(root: Path, files: list[Path]) -> dict[str, list[str]]:
    buckets = {
        "entrypoints_and_config": [],
        "architecture_modules": [],
        "backend_api_service_auth_logging": [],
        "frontend_ui_routes_forms_state": [],
        "database_schema_migrations_queries": [],
        "tests_fixtures_mocks": [],
        "agent_instruction_files": [],
    }
    for path in files:
        rp = rel(root, path)
        low = rp.lower()
        name = path.name.lower()
        if rp in {"AGENTS.md", "CLAUDE.md"} or name in {"agents.md", "claude.md", "copilot-instructions.md"}:
            buckets["agent_instruction_files"].append(rp)
        if name in {"package.json", "pyproject.toml", "go.mod", "cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts", "dockerfile", "makefile"} or "/config" in low or low.endswith("config.ts") or low.endswith("config.js"):
            buckets["entrypoints_and_config"].append(rp)
        if any(token in low for token in ["/app/", "/src/", "/lib/", "/packages/", "/modules/"]):
            buckets["architecture_modules"].append(rp)
        if any(token in low for token in ["api", "route", "controller", "service", "middleware", "auth", "logger", "logging", "job", "worker"]):
            buckets["backend_api_service_auth_logging"].append(rp)
        if any(token in low for token in ["component", "page", "view", "screen", "hook", "form", "store", "style", "css", "scss", "tsx", "jsx", "vue", "svelte"]):
            buckets["frontend_ui_routes_forms_state"].append(rp)
        if any(token in low for token in ["migration", "schema", "model", "repository", "dao", "query", "prisma", "drizzle", "typeorm", "sequelize", "alembic", "sql"]):
            buckets["database_schema_migrations_queries"].append(rp)
        if any(token in low for token in ["test", "spec", "__tests__", "fixture", "mock", "cypress", "playwright", "jest", "vitest", "pytest"]):
            buckets["tests_fixtures_mocks"].append(rp)
    for key in buckets:
        buckets[key] = sorted(dict.fromkeys(buckets[key]))[:80]
    return buckets


def read_command_hints(root: Path) -> list[str]:
    hints: list[str] = []
    package = root / "package.json"
    if package.exists():
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
            scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
            for name in ["lint", "typecheck", "test", "test:unit", "test:integration", "build", "dev"]:
                if name in scripts:
                    hints.append(f"package.json script `{name}`: `{scripts[name]}`")
        except Exception as exc:  # noqa: BLE001
            hints.append(f"package.json could not be parsed: {exc}")
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        hints.append("pyproject.toml present; inspect tool sections for lint/test/typecheck commands")
    makefile = root / "Makefile"
    if makefile.exists():
        hints.append("Makefile present; inspect targets for install/lint/test/build commands")
    return hints


def inventory_markdown(root: Path, max_files: int) -> str:
    files = list(iter_files(root, max_files))
    stack = detect_stack(root)
    buckets = classify_files(root, files)
    command_hints = read_command_hints(root)
    lines: list[str] = []
    lines.append("# Repository Inventory")
    lines.append("")
    lines.append("Generated by `project-dev-standards/scripts/repo_standards_bootstrap.py`.")
    lines.append("Use this inventory as evidence-finding support, not as final standards.")
    lines.append("")
    lines.append("## Repository root")
    lines.append(f"`{root}`")
    lines.append("")
    lines.append("## Detected stack signals")
    for area, items in stack.items():
        lines.append(f"### {area.replace('_', ' ').title()}")
        if items:
            for item in items[:40]:
                lines.append(f"- `{item}`")
        else:
            lines.append("- none detected")
        lines.append("")
    lines.append("## Command hints")
    if command_hints:
        for hint in command_hints:
            lines.append(f"- {hint}")
    else:
        lines.append("- no command hints detected from common manifests")
    lines.append("")
    lines.append("## Representative files by domain")
    for bucket, items in buckets.items():
        lines.append(f"### {bucket.replace('_', ' ').title()}")
        if items:
            for item in items:
                lines.append(f"- `{item}`")
        else:
            lines.append("- none detected")
        lines.append("")
    lines.append("## All scanned text-like files")
    for path in sorted(rel(root, p) for p in files):
        lines.append(f"- `{path}`")
    lines.append("")
    return "\n".join(lines)


def doc_template(name: str, repo_name: str) -> str:
    title = name.removesuffix(".md").replace("-", " ").title()
    base_header = f"# {title}\n\n"
    evidence_note = "Every rule in this file must cite repository file paths as evidence. Remove placeholder sections that do not apply.\n\n"
    if name == "00-overview.md":
        return f"""# Project Development Standards Overview

Repository: `{repo_name}`

These standards capture conventions observed in this repository. They are not generic best practices.

## Evidence policy
Every normative rule must cite repository files. Rules without evidence must be marked `Needs confirmation`.

## Technology stack
| Area | Detected tools | Evidence |
|---|---|---|
| Runtime | Needs confirmation | `_repo-inventory.md` |
| Backend | Needs confirmation | `_repo-inventory.md` |
| Frontend | Needs confirmation | `_repo-inventory.md` |
| Database | Needs confirmation | `_repo-inventory.md` |
| Testing | Needs confirmation | `_repo-inventory.md` |
| Build / CI | Needs confirmation | `_repo-inventory.md` |

## Repository layout
| Path | Purpose | Evidence |
|---|---|---|

## Required commands
| Purpose | Command | Evidence |
|---|---|---|
| Install | Needs confirmation |  |
| Lint | Needs confirmation |  |
| Typecheck | Needs confirmation |  |
| Test | Needs confirmation |  |
| Build | Needs confirmation |  |

## How agents should use these standards
Read `07-agent-instructions.md`, then load only the domain docs relevant to the files being changed.
"""
    if name == "06-code-review-checklist.md":
        return """# Code Review Checklist

Use this checklist after implementation.

## Required checks
- [ ] The change follows architecture boundaries in `01-architecture.md` when applicable.
- [ ] Backend changes follow `02-backend.md` when applicable.
- [ ] Frontend changes follow `03-frontend.md` when applicable.
- [ ] Database changes follow `04-database.md` when applicable.
- [ ] Tests follow `05-testing.md` when applicable.
- [ ] New or changed conventions are documented with evidence.

## Repository-specific checks
- [ ] Needs confirmation: add checks only after inspecting real code patterns.
"""
    if name == "07-agent-instructions.md":
        return """# Agent Instructions for Development Standards

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
"""
    section_map = {
        "01-architecture.md": ["Module boundaries", "Dependency direction", "Where business logic belongs", "Cross-cutting concerns"],
        "02-backend.md": ["API route structure", "Request validation", "Authentication and authorization", "Service / repository boundaries", "Error handling", "Logging", "Background jobs / async work", "External integrations"],
        "03-frontend.md": ["App routing", "Component organization", "State management", "Forms and validation", "Styling", "API client usage", "Error and loading states"],
        "04-database.md": ["Schema ownership", "Migration workflow", "Query / ORM patterns", "Transactions", "Seed and test data", "Data safety rules"],
        "05-testing.md": ["Test framework and commands", "Test file naming", "Unit tests", "Integration tests", "Fixtures and mocks", "What to run before handoff"],
    }
    lines = [base_header, evidence_note]
    for section in section_map.get(name, []):
        lines.extend([
            f"## {section}",
            "",
            "Status: Needs confirmation",
            "",
            "Rule:",
            "",
            "Evidence:",
            "- `path/to/file` — observation",
            "",
            "Reason:",
            "",
        ])
    return "\n".join(lines)


def write_docs(root: Path, out_dir: Path, max_files: int, overwrite: bool) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    changed: list[str] = []
    inventory = out_dir / "_repo-inventory.md"
    inventory.write_text(inventory_markdown(root, max_files), encoding="utf-8")
    changed.append(rel(root, inventory) if inventory.is_relative_to(root) else str(inventory))
    for name in DOC_NAMES:
        path = out_dir / name
        if path.exists() and not overwrite:
            continue
        path.write_text(doc_template(name, root.name), encoding="utf-8")
        changed.append(rel(root, path) if path.is_relative_to(root) else str(path))
    return changed


def upsert_managed_block(path: Path) -> bool:
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    if MANAGED_START in original and MANAGED_END in original:
        before = original.split(MANAGED_START, 1)[0].rstrip()
        after = original.split(MANAGED_END, 1)[1].lstrip()
        updated = f"{before}\n\n{AGENT_BLOCK}\n{after}".rstrip() + "\n"
    else:
        updated = original.rstrip() + "\n\n" + AGENT_BLOCK
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def apply_agent_snippets(root: Path) -> list[str]:
    changed: list[str] = []
    for name in ["AGENTS.md", "CLAUDE.md"]:
        path = root / name
        if path.exists():
            if upsert_managed_block(path):
                changed.append(name)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap project development standards from a local repository.")
    parser.add_argument("repo", nargs="?", default=".", help="repository root path")
    parser.add_argument("--output", default="docs/ai-dev-standards", help="output directory relative to repo root")
    parser.add_argument("--max-files", type=int, default=2500, help="maximum text-like files to inventory")
    parser.add_argument("--write-docs", action="store_true", help="write docs/ai-dev-standards scaffold")
    parser.add_argument("--overwrite", action="store_true", help="overwrite existing standards documents except inventory")
    parser.add_argument("--apply-agent-snippet", action="store_true", help="update existing AGENTS.md and CLAUDE.md with context-routing block")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"repository path does not exist or is not a directory: {root}")

    print(f"Repository: {root}")
    stack = detect_stack(root)
    print("Detected signals:")
    for area, items in stack.items():
        if items:
            print(f"- {area}: {', '.join(items[:8])}{' ...' if len(items) > 8 else ''}")

    if args.write_docs:
        out_dir = root / args.output
        changed_docs = write_docs(root, out_dir, args.max_files, args.overwrite)
        print("\nWrote standards files:")
        for item in changed_docs:
            print(f"- {item}")
    else:
        print("\nNo docs written. Pass --write-docs to create standards scaffold.")

    if args.apply_agent_snippet:
        changed_agents = apply_agent_snippets(root)
        if changed_agents:
            print("\nUpdated existing agent instruction files:")
            for item in changed_agents:
                print(f"- {item}")
        else:
            print("\nNo AGENTS.md or CLAUDE.md found; no agent instruction files created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
