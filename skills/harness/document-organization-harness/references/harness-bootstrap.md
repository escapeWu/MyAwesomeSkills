# Harness Bootstrap Reference

## 1. Target shape

The harness should expose four things:

1. where to start reading;
2. how the repo is organized;
3. where expected behavior, current state, and durable progress are owned;
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

## 防目标漂移（Anti-Drift）

## Git Worktree 隔离开发

## 测试规则

## 历史教训
```

Keep the section names stable once published.

The `强制执行流程门` section turns the harness from described guidance into an
enforced workflow. It must require, in order:

```text
scope and ownership check
  → freeze contracts, safety boundaries, and validation matrix
  → update the owning GOAL/README current-state section
  → implement within the declared boundary
  → collect focused validation evidence
  → update durable docs and append-only artifacts
```

The `防目标漂移` section keeps long runs aligned. The owning GOAL,
`requirements.md`, and README current-state section are the durable anchors.
Re-read them at the start of each work session, after context compaction, and
before advancing through a validation gate.

### Recommended current-state section

```md
## Current State

- Status:
- Completed:
- Pending:
- Blockers:
- Next validation gate:
- Evidence:
```

Use the session's planning surface for transient sequencing. Persist only
durable state, decisions, blockers, and evidence in the owning documents.

## 2.1 Repo-local skill registry

If the repo uses project-local skills, add a concise registry in `AGENTS.md`.

```md
## Repo-local Skills

- `.agents/skills/harness/document-organization-harness`: organize or repair project documentation, navigation, ownership, and governance.
- `.agents/skills/harness/progressive-disclosure-docs`: enforce progressive disclosure, truth ownership, route overlays, and lifecycle structure.
- `.agents/skills/harness/project-analysis`: investigate architecture, dataflow, route impact, and expected-vs-implemented gaps when shallow docs are insufficient.
- `.agents/skills/harness/project-docs-workflow`: inspect docs impact before and after non-trivial code changes.
- `.agents/skills/harness/external-collaboration-workflow`: preserve external proposal provenance and translate accepted items into internal contracts.
- `.agents/skills/harness/refactor-large-modules`: split oversized or mixed-responsibility modules while preserving behavior and public contracts.
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
skills/harness/document-organization-harness/assets/harness-bundle.json
```

Bundle members:

```text
skills/harness/document-organization-harness
skills/harness/progressive-disclosure-docs
skills/harness/project-analysis
skills/harness/project-docs-workflow
skills/harness/external-collaboration-workflow
skills/harness/refactor-large-modules
```

Install from an existing local clone:

```bash
python skills/harness/document-organization-harness/scripts/install_harness_bundle.py \
  --source /path/to/MyAwesomeSkills \
  --target /path/to/target-repo \
  --overwrite
```

Install from the current GitHub repo:

```bash
SOURCE_REPO="https://github.com/escapeWu/MyAwesomeSkills.git"
TMP_DIR="$(mktemp -d)"
git clone --depth 1 "$SOURCE_REPO" "$TMP_DIR/MyAwesomeSkills"
python "$TMP_DIR/MyAwesomeSkills/skills/harness/document-organization-harness/scripts/install_harness_bundle.py" \
  --source "$TMP_DIR/MyAwesomeSkills" \
  --target /path/to/target-repo \
  --overwrite
```

After installing:

1. Read the installed `.agents/skills/harness/README.md` (source:
   [`skills/harness/README.md`](../../README.md)) to incrementally patch the
   target repo's `AGENTS.md` and register only installed skills.
2. Copy or adapt `assets/demo-harness/AGENTS.md` and `assets/demo-harness/docs/`.
3. Replace placeholders with target repo facts.
4. Run the docs navigation validation checklist.

If the target repo already has one of these skills, omit `--overwrite` to make
the installer fail fast, review the difference manually, and only then re-run
with `--overwrite`.

## 2.3 Cursor native execution gate (`.cursor/rules`)

In a Cursor repo, land the execution gate in two always-visible places:

1. `.cursor/rules/harness-execution.mdc` with `alwaysApply: true`;
2. root `AGENTS.md` under `## 强制执行流程门（Mandatory Execution Gate）`.

The gate enforces contract freeze, bounded implementation, focused validation,
and durable documentation synchronization. It does not require delegation.
Delegation remains opt-in and requires explicit user authorization.

## 3. Docs tree skeleton

```text
docs/
├── OVERVIEW.md
├── feature/
│   ├── INDEX.md
│   └── <module>/
│       ├── README.md
│       ├── INDEX.md          # only when the module is large
│       ├── requirements.md   # expected behavior and acceptance
│       ├── design.md         # detailed design
│       └── data-model.md     # table and contract definitions
├── reference/
│   ├── INDEX.md
│   ├── architecture.md
│   ├── interfaces.md
│   └── runbook-testing.md
├── collaboration/
│   └── INDEX.md
└── archive/
    └── INDEX.md
```

The owning feature README or GOAL records current implementation state,
completed work, pending work, blockers, and the next validation gate. Do not
create a parallel execution-control hierarchy.

## 3.1 Feature granularity and autonomous governance

Encode these rules in root `AGENTS.md`:

```text
一功能一目录：独立 feature（自有目标/里程碑、或自有契约/产出、或独立生命周期、
  或 leaf ≥ 3 / 单文件 ≥ 500 行）必须独立成 docs/feature/<feature>/ 带自己的 README。
自主维护：非 trivial 代码 / 契约变更后，同任务内主动更新 owning feature README、
  requirements、feature/INDEX、OVERVIEW、反链及受影响的 interfaces/runbook。
自主调整：发现大类下子主题膨胀时，主动提议拆成独立 feature。
拆分不破链：父 INDEX/OVERVIEW 增路由、leaf 增反链、旧路径迁移而非并存。
```

## 4. Leaf-document rules

Every leaf doc should begin with a parent link.

```md
> 上级：../README.md
```

For deeper locations, use a repo-root link:

```md
> 上级：[/docs/OVERVIEW.md](/docs/OVERVIEW.md)
```

Rules:

- every leaf must be reachable from a parent index;
- every leaf must point back up;
- avoid orphan docs;
- avoid deep `../` chains when a repo-root link is clearer.

## 5. Durable status rule

Use the owning GOAL/README when work has meaningful dependencies, staged
validation, multiple owners, or a durable audit requirement.

Update only these durable fields:

1. expected behavior and acceptance;
2. current implementation state;
3. completed and pending work;
4. blockers and decisions;
5. next validation gate;
6. stable evidence and append-only artifact locations.

Transient session sequencing stays in the active planning surface and is not
promoted into a separate repository control plane.

## 6. Validation checklist

- Start at `AGENTS.md`.
- Reach `docs/OVERVIEW.md`.
- Reach `docs/feature/INDEX.md` and `docs/reference/INDEX.md`.
- Reach `docs/collaboration/INDEX.md` without treating external sources as internal contracts.
- Reach at least one module README.
- Walk back to the root through parent links.
- Confirm no leaf doc is orphaned.
- Confirm archive material is not mixed into active paths.
- Confirm the owning GOAL/README exposes current state and the next gate.

## 7. Demo harness pack

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
3. Keep `OVERVIEW.md`, `feature/INDEX.md`, `reference/INDEX.md`, and
   `archive/INDEX.md`.
4. Add repo-local skills to `AGENTS.md` only if they exist or will be installed.
5. Run the validation checklist above.
