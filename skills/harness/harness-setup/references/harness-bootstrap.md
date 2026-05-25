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

## Git Worktree 隔离开发

## 测试规则

## 历史教训
```

Keep the section names stable once published.

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

## 3. Docs tree skeleton

```text
docs/
├── OVERVIEW.md
├── feature/
│   ├── INDEX.md
│   └── <module>/
│       ├── README.md
│       ├── INDEX.md          # only when the module is large
│       └── taskBoard.md      # only when the module is multi-wave
├── reference/
│   ├── INDEX.md
│   ├── architecture.md
│   ├── interfaces.md
│   └── runbook-testing.md
└── archive/
    └── INDEX.md
```

If the repo is smaller, collapse the module folder to a single `README.md`, but keep
the four top-level docs entry points.

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
