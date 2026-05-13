#!/usr/bin/env python3
"""Validate a Codex supervisor round and update a compact state file.

The script is conservative: it records evidence, command results, diff summary,
secret-like findings in tracked diffs, and optional static acceptance checks.
It does not modify project code.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

SECRET_VALUE_RE=***
    r"(?i)(api[_-]?key|secret|token|password|passwd|private[_-]?key|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_./+=:-]{16,})"
)
FAKE_HINT_RE = re.compile(r"(?i)(fake|dummy|example|test|placeholder|xxxx|your[_-]?)")


def run(cmd: str, cwd: Path, timeout: int = 120) -> dict[str, Any]:
    started = time.time()
    try:
        p = subprocess.run(cmd, cwd=str(cwd), shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        return {"cmd": cmd, "exit_code": p.returncode, "duration_sec": round(time.time() - started, 2), "output_tail": p.stdout[-6000:]}
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        return {"cmd": cmd, "exit_code": 124, "duration_sec": round(time.time() - started, 2), "output_tail": out[-6000:] + "\n<TIMEOUT>"}
    except Exception as exc:
        return {"cmd": cmd, "exit_code": 127, "duration_sec": round(time.time() - started, 2), "output_tail": f"<failed: {exc}>"}


def load_state(path: Path) -> dict[str, Any]:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return {"state_read_error": True}
    return {}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def scan_diff_for_secrets(diff: str) -> list[str]:
    findings = []
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        m = SECRET_VALUE_RE.search(line)
        if m and not FAKE_HINT_RE.search(line):
            redacted = line[:120]
            if len(redacted) > 80:
                redacted = redacted[:80] + "..."
            findings.append(redacted)
    return findings[:20]


def static_checks(root: Path, checks: list[dict[str, Any]]) -> dict[str, Any]:
    results = {}
    for check in checks:
        name = check.get("name") or check.get("path") or "unnamed"
        path = root / check.get("path", "")
        patterns = check.get("patterns", [])
        mode = check.get("mode", "all")
        if not path.exists() or not path.is_file():
            results[name] = {"pass": False, "reason": f"file missing: {check.get('path')}"}
            continue
        txt = path.read_text(errors="ignore")
        matched = [pat for pat in patterns if re.search(pat, txt, re.M)]
        ok = len(matched) == len(patterns) if mode == "all" else bool(matched)
        results[name] = {"pass": ok, "matched": matched, "missing": [p for p in patterns if p not in matched]}
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--validation", action="append", default=[], help="Validation command; may be repeated")
    ap.add_argument("--static-checks-json", default="", help="JSON list of {name,path,patterns,mode}")
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    root = Path(args.workdir).expanduser().resolve()
    state_path = Path(args.state).expanduser().resolve()
    state = load_state(state_path)

    git_status = run("git status --short", root, timeout=30)
    diff_stat = run("git diff --stat", root, timeout=30)
    diff = run("git diff -- . ':(exclude).env' ':(exclude)*auth*' ':(exclude)*secret*'", root, timeout=60)
    secret_findings = scan_diff_for_secrets(diff.get("output_tail", ""))

    validations = [run(cmd, root, timeout=args.timeout) for cmd in args.validation]
    validation_pass = all(v["exit_code"] == 0 for v in validations) if validations else None

    checks = []
    if args.static_checks_json:
        try:
            checks = json.loads(args.static_checks_json)
        except Exception as exc:
            checks = [{"name": "static_checks_json_parse", "error": str(exc)}]
    static_result = static_checks(root, checks) if checks and "error" not in checks[0] else {c.get("name", "parse_error"): c for c in checks}
    static_pass = all(v.get("pass") for v in static_result.values()) if static_result else None

    safety_clean = not secret_findings
    status = "complete" if validation_pass is True and (static_pass is not False) and safety_clean else "needs_review"

    state.update({
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": status,
        "evidence": {
            "git_status_short": git_status,
            "git_diff_stat": diff_stat,
            "secret_findings_in_diff": secret_findings,
            "validation": validations,
            "static_checks": static_result,
        },
        "acceptance": {
            **state.get("acceptance", {}),
            "validation_commands_pass": validation_pass,
            "static_checks_pass": static_pass,
            "safety_clean": safety_clean,
        },
        "stop_reason": "validation/static/safety passed" if status == "complete" else "validation, static checks, or safety requires review",
    })
    save_state(state_path, state)
    print(json.dumps({"state_path": str(state_path), "status": status, "acceptance": state["acceptance"], "stop_reason": state["stop_reason"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()