# Harness Bootstrap Reference

## 1. Target shape

The harness should expose four things:

1. where to start reading;
2. how the repo is organized;
3. how to plan multi-step work;
4. how to verify a change.

The implementation details of the product are not part of the harness.

## 2. Root `AGENTS.md` skeleton

Use this order:

```md
# Agent 开发规约

> 项目上下文入口：[`docs/OVERVIEW.md`](docs/OVERVIEW.md)

## 核心原则

## 分层约束

## 代码组织约束

## 文档渐进式披露规则

## 文档写入规则

## 项目内置 skills

## 强制执行流程门（Mandatory Execution Gate）

## Git Worktree 隔离开发

## 测试规则

## 历史教训
```

Keep the section names stable once published.

The `强制执行流程门` section is what turns the harness from "described" into "enforced".
It must force, in order: scope check → taskBoard via `harness-engineering-plan` →
contracts-first → **parallel dispatch of independent ready TaskNodes to multiple
implementation agents** (Cursor `Task` tool subagent or `codex` CLI) → per-milestone
integration gate → archive + distill to docs. Without this gate, agents default to
single-threaded implementation and skip both the taskBoard and parallel dispatch.

## 2.1 Repo-local skill registry

If the repo uses project-local skills, add a concise registry in `AGENTS.md`.

```md
## Repo-local Skills

- `.agents/skills/harness/harness-setup`: bootstrap or repair the agent/docs/taskBoard harness.
- `.agents/skills/harness/harness-engineering-plan`: create a taskBoard for multi-wave work.
- `.agents/skills/harness/project-docs-workflow`: inspect docs impact before and after non-trivial code changes.
```

Do not force these exact skill names into every repo. The invariant is:

- root instructions list available skills;
- each skill has a clear trigger;
- each skill owns one workflow;
- detailed variants live inside the skill's `references/` or `assets/`.

Source repositories keep the canonical bundle under `skills/harness/`, while
target repositories receive the installed bundle under `.agents/skills/harness/`.

Recommended local skill shape:

```text
.agents/
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        └── assets/
```

## 2.2 Auto-install the harness skill bundle

When the current GitHub repository is the canonical skill source, install the
entire harness bundle from that repository instead of copying individual skills.

Curated bundle manifest:

```text
skills/harness/harness-setup/assets/harness-bundle.json
```

Bundle members:

```text
skills/harness/harness-setup
skills/harness/harness-engineering-plan
skills/harness/progressive-disclosure-docs
skills/harness/project-analysis
skills/harness/project-docs-workflow
skills/harness/codex-design-review
skills/harness/code-organization-harness
```

Install from an existing local clone:

```bash
python skills/harness/harness-setup/scripts/install_harness_bundle.py \
  --source /path/to/MyAwesomeSkills \
  --target /path/to/target-repo \
  --overwrite
```

Install from the current GitHub repo:

```bash
SOURCE_REPO="https://github.com/escapeWu/MyAwesomeSkills.git"
TMP_DIR="$(mktemp -d)"
git clone --depth 1 "$SOURCE_REPO" "$TMP_DIR/MyAwesomeSkills"
python "$TMP_DIR/MyAwesomeSkills/skills/harness/harness-setup/scripts/install_harness_bundle.py" \
  --source "$TMP_DIR/MyAwesomeSkills" \
  --target /path/to/target-repo \
  --overwrite
```

After installing:

1. Register installed skills in the target repo's `AGENTS.md`.
2. Copy or adapt `assets/demo-harness/AGENTS.md` and `assets/demo-harness/docs/`.
3. Replace placeholders with target repo facts.
4. Run the docs navigation validation checklist.

If the target repo already has one of these skills, omit `--overwrite` to make
the installer fail fast, review the difference manually, and only then re-run
with `--overwrite`.

## 2.3 Cursor 原生强制执行门（`.cursor/rules`）

Soft skill descriptions and a buried `AGENTS.md` bullet are **not** enough — agents
ignore them at runtime and fall back to single-threaded implementation. In a Cursor
repo, land the execution gate in two always-injected places:

1. **`.cursor/rules/harness-execution.mdc`** with `alwaysApply: true`. Cursor injects
   this every turn, so the gate is always in context. Copy the template from
   `assets/demo-harness/.cursor/rules/harness-execution.mdc`.
2. **Root `AGENTS.md` → `## 强制执行流程门（Mandatory Execution Gate）`** as the
   human-readable SSOT of the same gate.

The gate must encode, in order:

```text
scope check (≥2 wave / ≥5 TaskNode / multi-file)
  → taskBoard via harness-engineering-plan (禁止跳过)
  → contracts-first (M1)
  → 并行派发独立 ready TaskNode 给多个实施 agent
       · Cursor `Task` 工具 subagent（同一条消息多个 Task 调用）
       · 或 `codex` CLI（/tmp spec + codex exec --full-auto - < spec.md）
       · 禁止 last-writer-wins；主 agent 串行 review + merge
  → per-milestone integration gate
  → archive taskBoard + distill to docs/
```

The `.mdc` frontmatter is minimal:

```md
---
description: <one line>
alwaysApply: true
---
```

Non-Cursor repos can skip the `.mdc` file and rely on `AGENTS.md` + the skill, but
should still keep the `强制执行流程门` section.

## 3. Docs tree skeleton

```text
docs/
├── OVERVIEW.md
├── feature/
│   ├── INDEX.md
│   └── <module>/
│       ├── README.md
│       ├── INDEX.md          # only when the module is large
│       ├── design.md         # detailed design (SSOT)
│       └── data-model.md     # table/contract definitions (SSOT)
├── reference/
│   ├── INDEX.md
│   ├── architecture.md
│   ├── interfaces.md
│   └── runbook-testing.md
└── archive/
    └── INDEX.md

(separate: .agents/skills/harness/harness-engineering-plan/tasks/<module>/taskBoard.md — WIP)
```

taskBoard 不在 docs/ 下。它是 harness-engineering-plan 的临时产物，存放在 skill 自身的 `tasks/` 目录中。
任务完成后移入 `tasks/archive/`，然后蒸馏稳定结论到 `docs/`。

## 4. Leaf-document rules

Every leaf doc should begin with a parent link.

Examples:

```md
> 上级：../README.md
```

or, for deeper locations, use repo-root links:

```md
> 上级：[/docs/OVERVIEW.md](/docs/OVERVIEW.md)
```

Rules:

- every leaf must be reachable from a parent index;
- every leaf must point back up;
- avoid orphan docs;
- avoid deep `../` chains when a repo-root link is clearer.

## 5. TaskBoard decision rule

Create `taskBoard.md` when at least one of these is true:

- the work has more than one wave;
- tasks have meaningful dependencies;
- validation must happen in stages;
- multiple files or owners need coordination;
- the change needs an auditable execution record.

If the work is a single small fix, a taskBoard is optional.

**Location**: `.agents/skills/harness/harness-engineering-plan/tasks/<module>/taskBoard.md`

**Lifecycle**:
1. Generate → `tasks/<module>/taskBoard.md`
2. Execute → update status in `tasks/`
3. Complete → move to `tasks/archive/<module>/taskBoard-<phase>.md`
4. Distill → update `docs/feature/<module>/` with stable conclusions

## 6. TaskBoard skeleton

```md
# TaskBoard

## Goal

## Milestones

## Wave plan

## TaskNodes

## Validation gates

## Done evidence
```

Keep task status explicit and update it as work progresses.

## 7. Validation checklist

- Start at `AGENTS.md`.
- Reach `docs/OVERVIEW.md`.
- Reach `docs/feature/INDEX.md` and `docs/reference/INDEX.md`.
- Reach at least one module README.
- Walk back to the root through parent links.
- Confirm no leaf doc is orphaned.
- Confirm archive material is not mixed into active paths.

## 8. Demo harness pack

This skill includes a copyable demo pack at `assets/demo-harness/`.

Expected copy target:

```text
<target-repo>/
├── AGENTS.md
└── docs/
```

After copying:

1. Replace generic names with the target repo's actual module names.
2. Delete the demo module if the repo already has a real feature module.
3. Keep `OVERVIEW.md`, `feature/INDEX.md`, `reference/INDEX.md`, and `archive/INDEX.md`.
4. Add repo-local skills to `AGENTS.md` only if they exist or will be installed.
5. Run the validation checklist above.
