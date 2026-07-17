#!/usr/bin/env python3
"""Create a deterministic external-collaboration case from the repo-local template."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


CASE_ID_RE = re.compile(r"EC-\d{4}-\d{3}-[a-z0-9][a-z0-9-]*\Z")
FEATURE_RE = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
ACTIVE_START = "<!-- ACTIVE-CASES:START -->"
ACTIVE_END = "<!-- ACTIVE-CASES:END -->"
TEMPLATE_FILES = ("INDEX.md", "problem-statement.md", "external-proposal.md")


def repository_root() -> Path:
    return Path(__file__).resolve().parents[5]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--external-team", required=True)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--repo-root", type=Path, default=repository_root())
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not CASE_ID_RE.fullmatch(args.case_id):
        raise SystemExit("case ID must match EC-YYYY-NNN-short-slug")
    if not FEATURE_RE.fullmatch(args.feature):
        raise SystemExit("feature must be a lowercase hyphenated slug")
    try:
        date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit("date must use YYYY-MM-DD") from exc
    if not args.title.strip() or not args.external_team.strip():
        raise SystemExit("title and external team must not be blank")


def render_template(path: Path, args: argparse.Namespace) -> str:
    replacements = {
        "CASE_ID": args.case_id,
        "CASE_TITLE": args.title.strip(),
        "FEATURE_SLUG": args.feature,
        "EXTERNAL_TEAM": args.external_team.strip(),
        "YYYY-MM-DD": args.date,
    }
    content = path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def update_active_cases(index_text: str, entry: str, case_id: str) -> str:
    if ACTIVE_START not in index_text or ACTIVE_END not in index_text:
        raise SystemExit("collaboration INDEX is missing Active Cases markers")
    if case_id in index_text:
        raise SystemExit(f"case is already registered in collaboration INDEX: {case_id}")

    prefix, remainder = index_text.split(ACTIVE_START, 1)
    active_body, suffix = remainder.split(ACTIVE_END, 1)
    entries = [line for line in active_body.splitlines() if line.startswith("- [")]
    entries.append(entry)
    rendered = "\n".join(sorted(entries))
    return f"{prefix}{ACTIVE_START}\n{rendered}\n{ACTIVE_END}{suffix}"


def main() -> int:
    args = parse_args()
    validate_args(args)
    root = args.repo_root.resolve()
    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "case-template"
    collaboration_root = root / "docs" / "collaboration"
    target = collaboration_root / args.case_id
    feature_readme = root / "docs" / "feature" / args.feature / "README.md"
    collaboration_index = collaboration_root / "INDEX.md"

    if not feature_readme.exists():
        raise SystemExit(f"owning Feature README does not exist: {feature_readme}")
    if not collaboration_index.exists():
        raise SystemExit(f"collaboration INDEX does not exist: {collaboration_index}")
    if target.exists():
        raise SystemExit(f"target case already exists: {target}")

    rendered_files = {
        filename: render_template(template_root / filename, args) for filename in TEMPLATE_FILES
    }
    entry = (
        f"- [{args.case_id} — {args.title.strip()}]({args.case_id}/INDEX.md) — "
        f"`{args.feature}` / `PROBLEM_DRAFTING`"
    )
    updated_index = update_active_cases(
        collaboration_index.read_text(encoding="utf-8"), entry, args.case_id
    )

    if args.dry_run:
        print(f"Would create: {target}")
        print(entry)
        return 0

    target.mkdir(parents=False)
    for filename, content in rendered_files.items():
        (target / filename).write_text(content, encoding="utf-8")
    collaboration_index.write_text(updated_index, encoding="utf-8")
    print(f"Created external collaboration case: {target.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
