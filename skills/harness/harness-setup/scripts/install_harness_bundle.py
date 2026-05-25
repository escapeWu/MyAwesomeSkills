#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _repo_root(path: Path) -> Path:
    if (path / ".git").exists():
        return path
    raise SystemExit(f"not a git repo: {path}")


def _clone_source(source: str) -> tuple[Path, tempfile.TemporaryDirectory[str] | None]:
    source_path = Path(source)
    if source_path.exists():
        return source_path.resolve(), None

    tmp = tempfile.TemporaryDirectory(prefix="harness-bundle-")
    clone_dir = Path(tmp.name) / "source"
    _run(["git", "clone", "--depth", "1", source, str(clone_dir)])
    return clone_dir, tmp


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the harness skill bundle from a source repo.")
    parser.add_argument("--source", required=True, help="Source repo path or Git URL.")
    parser.add_argument("--target", required=True, help="Target repo path.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing skill folders.")
    args = parser.parse_args()

    source_root, tmp = _clone_source(args.source)
    try:
        bundle_path = source_root / "skills" / "harness" / "harness-setup" / "assets" / "harness-bundle.json"
        if not bundle_path.exists():
            raise SystemExit(f"bundle manifest not found: {bundle_path}")

        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        source_bundle_root = source_root / bundle["source_root"]
        target_root = _repo_root(Path(args.target).resolve()) / ".agents" / "skills" / "harness"
        target_root.mkdir(parents=True, exist_ok=True)

        for skill_name in bundle["skills"]:
            src = source_bundle_root / skill_name
            dst = target_root / skill_name
            if dst.exists():
                if not args.overwrite:
                    raise SystemExit(f"target already exists: {dst}")
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

        print(f"installed {len(bundle['skills'])} skills into {target_root}")
        return 0
    finally:
        if tmp is not None:
            tmp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
