#!/usr/bin/env python3
"""Launch a focused Codex round in tmux from a supervisor task spec.

This script is the execution bridge for the Codex supervisor harness. It reads a
self-contained task spec, optional repo map, and persisted supervisor state,
creates a compact prompt for either round 1 or a focused repair round, writes the
prompt to a file, and optionally sends a safe `codex exec --full-auto` command to
a tmux target.

By default it runs in --dry-run mode unless --execute is passed.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        raise SystemExit(f"failed to parse JSON {path}: {exc}")


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)


def compact_json(data: Any, limit: int = 24000) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if len(text) <= limit:
        return text
    return text[:limit] + "\n... <truncated>"


def failed_acceptance(state: dict[str, Any]) -> dict[str, Any]:
    acc = state.get("acceptance", {}) or {}
    return {k: v for k, v in acc.items() if v is not True}


def validation_excerpt(state: dict[str, Any], limit: int = 8000) -> str:
    ev = state.get("evidence", {}) or {}
    parts = []
    for key in ["git_status_short", "git_diff_stat"]:
        if key in ev:
            parts.append(f"## {key}\n{compact_json(ev[key], 3000)}")
    for item in ev.get("validation", []) or []:
        cmd = item.get("cmd")
        code = item.get("exit_code")
        tail = item.get("output_tail", "")[-2500:]
        parts.append(f"## validation: {cmd}\nexit_code={code}\n{tail}")
    if ev.get("static_checks"):
        parts.append("## static_checks\n" + compact_json(ev.get("static_checks"), 4000))
    if ev.get("secret_findings_in_diff"):
        parts.append("## secret_findings_in_diff\n" + compact_json(ev.get("secret_findings_in_diff"), 2000))
    text = "\n\n".join(parts)
    return text[:limit] + ("\n... <truncated>" if len(text) > limit else "")


def build_prompt(spec: dict[str, Any], repo_map: dict[str, Any], state: dict[str, Any], round_number: int) -> str:
    original_task = spec.get("original_task") or spec.get("task") or "<unspecified>"
    normalized_goal = spec.get("normalized_goal") or spec.get("goal") or original_task
    acceptance = spec.get("acceptance", [])
    validation_commands = spec.get("validation_commands", [])
    safety_rules = spec.get("safety_rules", [])
    out_of_scope = spec.get("out_of_scope", [])
    in_scope = spec.get("in_scope", [])
    mode = spec.get("mode", "full-auto")

    if round_number <= 1 or not state:
        round_directive = """This is round 1. Implement the normalized goal with the smallest safe change set. Use the repo map as navigation context, but verify it against the live repository before editing. Do not over-refactor."""
    else:
        failed = failed_acceptance(state)
        round_directive = f"""This is repair round {round_number}. Do not restart from scratch. Focus only on the failed or uncertain acceptance criteria below, using the evidence from the previous round. Avoid unrelated refactors and preserve working behavior.\n\nFailed/uncertain acceptance booleans:\n{compact_json(failed, 6000)}\n\nPrevious validation evidence excerpt:\n{validation_excerpt(state)}"""

    prompt = f"""You are Codex running inside a supervised agent harness.

MODE
{mode}

ORIGINAL USER TASK
{original_task}

NORMALIZED GOAL
{normalized_goal}

ROUND DIRECTIVE
{round_directive}

IN SCOPE
{compact_json(in_scope, 4000)}

OUT OF SCOPE / NON-GOALS
{compact_json(out_of_scope, 4000)}

ACCEPTANCE CRITERIA
{compact_json(acceptance, 8000)}

VALIDATION COMMANDS TO RUN BEFORE FINISHING
{compact_json(validation_commands, 6000)}

SAFETY RULES
{compact_json(safety_rules, 8000)}

REPO MAP / NAVIGATION CONTEXT
{compact_json(repo_map, 24000)}

WORKING RULES
- First inspect the relevant live files; the repo map is guidance, not authority.
- Keep changes minimal and task-focused.
- Do not read, print, copy, or commit secrets. Avoid .env/auth/credential/private-key files.
- Do not add destructive behavior, production deployment, credential exfiltration, wallet/private-key use, or out-of-scope capabilities.
- If acceptance requires a product decision not specified here, stop and explain the blocking decision instead of guessing.
- Run the listed validation commands when practical. If a command cannot run because of environment issues, capture the exact reason.
- End with a concise summary: files changed, validation results, remaining risks, and any acceptance criteria still not met.
"""
    return prompt


def tmux_has_session(session: str) -> bool:
    p = run(["tmux", "has-session", "-t", session], timeout=10)
    return p.returncode == 0


def ensure_tmux(session: str, window: str, workdir: Path) -> None:
    if not tmux_has_session(session):
        p = run(["tmux", "new-session", "-d", "-s", session, "-c", str(workdir)], timeout=20)
        if p.returncode != 0:
            raise SystemExit(f"tmux new-session failed: {p.stdout}")
    # Rename window best-effort. Existing named windows are fine.
    run(["tmux", "rename-window", "-t", f"{session}:0", window], timeout=10)


def codex_running() -> bool:
    p = run(["bash", "-lc", "ps -axo command | grep -E '[c]odex exec|[n]ode.*codex'"], timeout=10)
    return p.returncode == 0 and bool(p.stdout.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="JSON task spec path")
    ap.add_argument("--repo-map", default="", help="JSON repo map path")
    ap.add_argument("--state", default="", help="JSON supervisor state path")
    ap.add_argument("--workdir", default="", help="Override workdir")
    ap.add_argument("--session", default="", help="Override tmux session")
    ap.add_argument("--window", default="codex", help="Tmux window name")
    ap.add_argument("--round", type=int, default=0, help="Round number; default state.current_round+1 or 1")
    ap.add_argument("--prompt-out", default="", help="Where to write the generated prompt")
    ap.add_argument("--execute", action="store_true", help="Actually send codex command to tmux")
    ap.add_argument("--no-full-auto", action="store_true", help="Use codex exec without --full-auto")
    ap.add_argument("--allow-if-codex-running", action="store_true", help="Do not stop if another codex process is detected")
    args = ap.parse_args()

    spec_path = Path(args.spec).expanduser().resolve()
    spec = load_json(spec_path)
    repo_map = load_json(Path(args.repo_map).expanduser().resolve()) if args.repo_map else spec.get("repo_map", {}) or {}
    state_path = Path(args.state).expanduser().resolve() if args.state else None
    state = load_json(state_path) if state_path and state_path.exists() else {}

    workdir = Path(args.workdir or spec.get("workdir") or repo_map.get("workdir") or ".").expanduser().resolve()
    session = args.session or spec.get("tmux_session") or workdir.name
    window = args.window or spec.get("tmux_window") or "codex"
    round_number = args.round or int(state.get("current_round", 0) or 0) + 1

    if not workdir.exists():
        raise SystemExit(f"workdir does not exist: {workdir}")
    if not (workdir / ".git").exists():
        raise SystemExit(f"workdir is not a git repository: {workdir}")

    prompt = build_prompt(spec, repo_map, state, round_number)
    prompt_out = Path(args.prompt_out).expanduser().resolve() if args.prompt_out else Path(f"/tmp/codex_supervisor_{session}_round_{round_number}.txt")
    prompt_out.write_text(prompt)

    result = {
        "prompt_out": str(prompt_out),
        "workdir": str(workdir),
        "tmux_target": f"{session}:{window}",
        "round": round_number,
        "execute": args.execute,
    }

    if args.execute:
        if codex_running() and not args.allow_if_codex_running:
            raise SystemExit("another Codex process appears to be running; pass --allow-if-codex-running only if this is intentional")
        ensure_tmux(session, window, workdir)
        full_auto = "" if args.no_full_auto else "--full-auto "
        cmd = f"cd {shlex.quote(str(workdir))} && codex exec {full_auto}\"$(cat {shlex.quote(str(prompt_out))})\""
        p = run(["tmux", "send-keys", "-t", f"{session}:{window}", cmd, "C-m"], timeout=20)
        result["tmux_send_exit_code"] = p.returncode
        result["tmux_send_output"] = p.stdout
        if p.returncode != 0:
            raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))

    if state_path:
        state.update({
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "current_round": round_number,
            "last_prompt_file": str(prompt_out),
            "tmux_target": f"{session}:{window}",
            "workdir": str(workdir),
            "status": "codex_launched" if args.execute else "prompt_generated",
        })
        save_json(state_path, state)
        result["state_path"] = str(state_path)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()