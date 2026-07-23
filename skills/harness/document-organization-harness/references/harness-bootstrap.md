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

- `.agents/skills/harness/add-idea`: unified docs-only idea intake; Grill when needed, then choose a new or existing Feature owner and materialize requirements, Specs, and conditional ADRs.
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

This source repository keeps canonical independent skills under `skills/harness/`. Target projects
maintain only the skills they use, either grouped under `.agents/skills/harness/` or in an existing
flat/custom registry. Do not move paths merely to match this repository.

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

## 2.2 Maintain repo-local skills

There is no suite installer or manifest. A target project maintains each selected skill through its
normal reviewed change workflow. Read the source [`CHANGELOG.md`](../../CHANGELOG.md) and
[`UPGRADING.md`](../../UPGRADING.md) before changing an existing copy.

For each target:

1. Read the actual skill registry and locate grouped, flat, partial, and project-specific skills.
2. Record the target working state and isolate unrelated work according to target policy.
3. Compare one canonical skill directory with its target counterpart.
4. Classify canonical updates, local extensions, obsolete behavior, and uncertain content before
   editing.
5. Apply only reviewed changes; do not replace directories containing unclassified local files.
6. Patch existing `AGENTS.md` and runtime-rule sections only after the corresponding target skill
   paths exist.
7. Validate frontmatter, provider metadata, links, docs routes, governance consistency, and the
   target project's own checks.

Projects adopting the full idea-to-implementation lifecycle maintain shared contracts and templates
first, then `add-idea`, then consuming workflow skills, and finally target-owned governance. Projects
may keep a smaller set; do not register or reference an absent skill.

The demo remains a scaffolding example, not an installation payload. Copy or adapt demo files only
when the target lacks an equivalent docs route, replace every demo fact, and preserve existing
project safety, authorization, ownership, commands, and validation rules. Existing Features migrate
to the Requirements/Spec/ADR model only when related work touches them.

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
│       ├── specs/            # bounded implementation contracts; lazy
│       ├── decisions/        # Feature-local ADRs; lazy
│       ├── design.md         # stable shared design reference
│       └── data-model.md     # stable table/contract reference
├── reference/
│   ├── INDEX.md
│   ├── decisions/           # cross-Feature/system ADRs; lazy
│   ├── architecture.md
│   ├── interfaces.md
│   └── runbook-testing.md
├── collaboration/
│   └── INDEX.md
└── archive/
    └── INDEX.md
```

The owning Feature README or GOAL records current implementation state,
contract links, completed work, pending work, blockers, and the next validation
gate. Requirements own expected behavior; Specs own bounded implementation
contracts; ADRs own durable rationale. Do not create a parallel control plane.

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
4. Add repo-local skills to `AGENTS.md` only when their actual target paths exist and the project
   accepts maintaining them.
5. Run the validation checklist above.
