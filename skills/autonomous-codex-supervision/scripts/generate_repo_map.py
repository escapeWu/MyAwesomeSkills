#!/usr/bin/env python3
"""Generate a compact repo map for Codex supervisor harness prompts.

This script is intentionally dependency-free. It inspects common project files,
lightweight directory structure, task-relevant keyword hits, validation commands,
and high-risk paths. It avoids reading secret-like files.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Iterable

SECRET_NAME_RE = re.compile(
    r"(^\.env$|\.env\.|secret|secrets|token|password|passwd|credential|credentials|private[_-]?key|auth\.json$|id_rsa|id_ed25519|keychain)",
    re.I,
)
SKIP_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "node_modules", "dist", "build", ".next", ".nuxt",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache", "coverage", ".coverage",
    "logs", "log", "tmp", "temp", ".hermes", ".idea", ".vscode",
}
DOC_NAMES = ["AGENTS.md", "CLAUDE.md", "README.md", "README.rst", "README.txt", "CONTRIBUTING.md"]
MANIFEST_NAMES = [
    "pyproject.toml", "package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json",
    "Makefile", "docker-compose.yml", "compose.yml", "Dockerfile", "requirements.txt", "uv.lock",
]
TEXT_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".kt", ".md", ".toml", ".yaml", ".yml", ".json"}


def run(cmd: list[str], cwd: Path) -> str:
    try:
        return subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=15).stdout.strip()
    except Exception as exc:
        return f"<failed: {exc}>"


def safe_read(path: Path, limit: int = 6000) -> str:
    if SECRET_NAME_RE.search(path.name):
        return ""
    try:
        data = path.read_text(errors="ignore")
    except Exception:
        return ""
    return data[:limit]


def iter_files(root: Path, max_files: int = 5000) -> Iterable[Path]:
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dpath = Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not SECRET_NAME_RE.search(d)]
        for name in filenames:
            if count >= max_files:
                return
            p = dpath / name
            count += 1
            yield p


def rel(root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(root))
    except Exception:
        return str(p)


def detect_stack(root: Path) -> list[str]:
    stack = []
    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
        stack.append("Python")
    if (root / "package.json").exists():
        pkg = safe_read(root / "package.json", 4000)
        stack.append("Node/JavaScript")
        if "react" in pkg.lower():
            stack.append("React")
        if "next" in pkg.lower():
            stack.append("Next.js")
        if "vite" in pkg.lower():
            stack.append("Vite")
    if (root / "go.mod").exists():
        stack.append("Go")
    if (root / "Cargo.toml").exists():
        stack.append("Rust")
    if (root / "docker-compose.yml").exists() or (root / "compose.yml").exists() or (root / "Dockerfile").exists():
        stack.append("Docker")
    return stack or ["unknown"]


def summarize_docs(root: Path) -> dict[str, str]:
    out = {}
    for name in DOC_NAMES:
        p = root / name
        if p.exists():
            txt = safe_read(p, 3000).strip().replace("\r", "")
            first = " ".join([line.strip() for line in txt.splitlines() if line.strip()][:6])
            out[name] = first[:800]
    docs = root / "docs"
    if docs.exists() and docs.is_dir():
        md_files = sorted([p for p in docs.rglob("*.md") if not any(part in SKIP_DIRS for part in p.parts)])[:12]
        for p in md_files:
            txt = safe_read(p, 1200).strip()
            first = " ".join([line.strip() for line in txt.splitlines() if line.strip()][:4])
            out[rel(root, p)] = first[:500]
    return out


def top_dirs(root: Path) -> dict[str, str]:
    hints = {}
    candidates = [p for p in root.iterdir() if p.is_dir() and p.name not in SKIP_DIRS and not SECRET_NAME_RE.search(p.name)]
    for p in sorted(candidates, key=lambda x: x.name)[:40]:
        files = []
        try:
            for child in sorted(p.iterdir(), key=lambda x: x.name)[:12]:
                if child.name in SKIP_DIRS or SECRET_NAME_RE.search(child.name):
                    continue
                files.append(child.name + ("/" if child.is_dir() else ""))
        except Exception:
            pass
        guidance = "contains: " + ", ".join(files[:10]) if files else "directory"
        if p.name.lower() in {"src", "app", "backend", "frontend", "server", "client", "tests", "test", "docs", "scripts"}:
            guidance += " (likely important)"
        hints[rel(root, p)] = guidance
    return hints


def validation_commands(root: Path) -> list[str]:
    cmds = []
    if (root / "pyproject.toml").exists():
        py = safe_read(root / "pyproject.toml", 8000)
        if "pytest" in py or (root / "tests").exists():
            cmds.append("uv run python -m pytest tests/ -v  # or project pytest command")
        cmds.append("uv run python -m compileall . -q")
    elif (root / "requirements.txt").exists() and (root / "tests").exists():
        cmds.append("python -m pytest tests/ -v")
    if (root / "package.json").exists():
        pkg = safe_read(root / "package.json", 8000)
        try:
            scripts = json.loads(pkg).get("scripts", {})
            for key in ["typecheck", "test", "lint", "build"]:
                if key in scripts:
                    cmds.append(f"npm run {key}")
        except Exception:
            cmds.append("npm test  # inspect package.json scripts")
    if (root / "Makefile").exists():
        cmds.append("make test  # if defined")
    return list(dict.fromkeys(cmds))[:8]


def keywords_from_task(task: str) -> list[str]:
    words = re.findall(r"[A-Za-z_][A-Za-z0-9_/-]{2,}|[\u4e00-\u9fff]{2,}", task or "")
    stop = {"the", "and", "for", "with", "this", "that", "into", "from", "我们的", "这个", "实现", "优化", "修复"}
    out = []
    for w in words:
        lw = w.lower()
        if lw not in stop and lw not in out:
            out.append(lw)
    return out[:12]


def task_relevant(root: Path, task: str, max_hits: int = 30) -> dict[str, str]:
    kws = keywords_from_task(task)
    if not kws:
        return {}
    hits: dict[str, int] = {}
    for p in iter_files(root):
        if p.suffix.lower() not in TEXT_EXTS or SECRET_NAME_RE.search(p.name):
            continue
        txt = safe_read(p, 12000).lower()
        if not txt:
            continue
        score = sum(txt.count(k) for k in kws if len(k) >= 3)
        path_l = rel(root, p).lower()
        score += sum(3 for k in kws if k in path_l)
        if score:
            hits[rel(root, p)] = score
    ranked = sorted(hits.items(), key=lambda kv: (-kv[1], kv[0]))[:max_hits]
    return {path: f"keyword relevance score={score}" for path, score in ranked}


def risky_paths(root: Path) -> list[str]:
    out = []
    for p in iter_files(root, max_files=3000):
        r = rel(root, p)
        if SECRET_NAME_RE.search(p.name) or p.name in {"config.json", ".env", "auth.json"}:
            out.append(r)
    for name in ["node_modules", ".venv", "dist", "build", "logs", ".hermes", ".git"]:
        if (root / name).exists():
            out.append(name + "/")
    return sorted(set(out))[:80]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--task", default="")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.workdir).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"workdir not found: {root}")

    manifest = {name: "present" for name in MANIFEST_NAMES if (root / name).exists()}
    docs = summarize_docs(root)
    repo_map = {
        "workdir": str(root),
        "git_status_short": run(["git", "status", "--short"], root) if (root / ".git").exists() else "<not a git repo>",
        "purpose": docs.get("README.md", "")[:500] or "Infer from repo files; verify before editing.",
        "stack": detect_stack(root),
        "manifests": manifest,
        "key_dirs": top_dirs(root),
        "docs_and_rules": docs,
        "task_relevant_files": task_relevant(root, args.task),
        "validation_commands": validation_commands(root),
        "do_not_touch_without_reason": risky_paths(root),
        "note": "Repo map is guidance, not authority. Verify against live files before editing. Do not read/print/commit secrets.",
    }
    if args.json:
        print(json.dumps(repo_map, ensure_ascii=False, indent=2))
    else:
        print("repo_map:")
        for k, v in repo_map.items():
            print(f"  {k}: {json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v}")


if __name__ == "__main__":
    main()
