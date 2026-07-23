# Maintaining And Upgrading Harness Skills

This repository maintains canonical harness skills and shared documentation contracts. It does not
provide a bundle installer, manifest, installation marker, automatic overwrite, or fleet deployment
tool. Every target project chooses which skills it maintains and upgrades them through its own
reviewed change process.

## Ownership Boundary

| Surface | Owner | Maintenance rule |
|---|---|---|
| Canonical `skills/harness/<skill>/` | This source repository | Defines the current reusable skill |
| Target project skill copy | Target project | Compare and update individually |
| Root/nested `AGENTS.md` and `CLAUDE.md` | Target project | Patch existing sections; never replace wholesale |
| `.cursor/rules` and other runtime rules | Target project | Keep consistent with accepted target policy |
| `docs/OVERVIEW.md`, indexes, Features, Specs, ADRs, changelogs | Target project | Migrate only through project-owned docs workflows |
| Source code, tests, configuration, artifacts, and evidence | Target project | Never changed merely because a skill changed |

A canonical skill update is a maintenance input, not authorization to change a target project. A
proposal, shared-understanding confirmation, existing implementation, or copied skill also does not
grant implementation, deployment, publication, training, or destructive-operation authorization.

## Supported Target Layouts

Existing projects may use any of these layouts:

1. **Grouped**: `.agents/skills/harness/<skill>/`.
2. **Flat**: `.agents/skills/<skill>/`.
3. **Partial**: only the harness skills relevant to that project.
4. **Extended**: canonical skills plus project-specific skills or local references.

Do not normalize layout as part of a functional upgrade. Moving paths changes the project skill
registry and should be a separate reviewed migration.

## Per-Project Maintenance Flow

### 1. Audit Before Editing

Record the target branch and working state:

```bash
git -C /path/to/target-repo status --short --branch
```

Identify:

- the actual paths registered in target `AGENTS.md` or provider configuration;
- which harness skills are present and actually used;
- local references, assets, scripts, provider metadata, and project-specific extensions;
- target-owned safety, authorization, ownership, validation, and command rules;
- active Feature documents that depend on the old contract.

A dirty target may be audited, but do not mix a suite maintenance change with unrelated work. Use
the target project's normal branch/worktree policy and preserve all existing changes.

### 2. Read The Coordinated Change

Read [`CHANGELOG.md`](CHANGELOG.md), then identify only the canonical skills and shared contracts
needed by the target. For the 2026-07-23 change, the coordinated surfaces are:

- `add-idea`;
- `progressive-disclosure-docs` contracts and templates;
- `project-docs-workflow`;
- `project-analysis`;
- `external-collaboration-workflow`;
- `document-organization-harness` bootstrap and governance guidance;
- target `AGENTS.md` or runtime gate only when the target accepts the new workflow.

`refactor-large-modules` has no direct lifecycle migration requirement from this change.

### 3. Compare One Skill At A Time

Use read-only directory comparison before editing. `git diff --no-index` returns `1` when it finds a
difference; that result means review is required, not that the command malfunctioned.

```bash
git diff --no-index -- \
  /path/to/target-repo/.agents/skills/harness/add-idea \
  /path/to/MyAwesomeSkills/skills/harness/add-idea
```

Adjust the target path for flat or custom layouts. Review each changed file and classify it as:

- canonical behavior the target should adopt;
- target-specific behavior that must remain local;
- obsolete local behavior replaced by the new shared contract;
- unrelated or uncertain content that must not be changed in this maintenance pass.

Do not replace an entire skill directory when it contains unclassified local content. Apply the
reviewed changes with the target project's normal editor and version-control workflow.

### 4. Apply Coordinated Changes In Dependency Order

For projects adopting the full idea-to-implementation contract, maintain these surfaces in order:

1. `progressive-disclosure-docs/references/feature-spec-decision-contract.md` and its templates;
2. `add-idea` and its routing contract;
3. `project-docs-workflow` and `project-analysis` consumers;
4. `external-collaboration-workflow` contract translation;
5. `document-organization-harness` bootstrap/governance guidance;
6. target-owned `AGENTS.md` and runtime rules.

A project that does not need `add-idea` may keep a smaller skill set. In that case, do not add its
registry entry or rules, and verify that remaining skills do not link to absent local paths.

### 5. Patch Target-Owned Governance Manually

Patch existing sections instead of copying a canonical `AGENTS.md` or demo file. Preserve project
safety, authorization, ownership, validation, and commands.

When the target adopts the new contract:

- register `add-idea` only if its target path exists;
- route product/engineering ideas through the explicit docs-only entry;
- state that requirements own expected behavior, frozen Specs own bounded implementation contracts,
  and accepted ADRs own durable architecture rationale;
- require confirmed requirements, accepted blocking ADRs, and a frozen Spec before later
  contract-affecting implementation;
- keep external proposals as provenance/recommendations rather than implementation authorization;
- keep always-on runtime rules consistent with root instructions.

The managed governance block must appear at most once. Existing equivalent sections should be
updated in place.

## Existing Feature Migration

Do not rewrite every active Feature during suite maintenance. Migrate on touch:

1. Preserve existing text and identify its current owner before moving content.
2. Keep expected behavior, acceptance, NFRs, non-goals, and stop rules in `requirements.md`.
3. Create a new Spec only for a bounded implementation contract; do not overwrite validated or
   superseded historical Specs.
4. Create an ADR only when the decision is costly to reverse, would be confusing without context,
   and has real alternatives with material trade-offs.
5. Keep README focused on current state, active routes, blockers, next gate, and links.
6. Append durable route and lifecycle transitions to the Feature changelog.
7. Use `NO_DURABLE_CHANGE` for reversible local details that change no durable truth.

An untouched legacy Feature can remain in its old shape. Before its next contract-affecting
implementation, establish confirmed requirements, resolve blocking ADRs, and freeze the active Spec.

## Validation

After maintaining each target project:

- review `git diff` and confirm unrelated changes remain untouched;
- validate every maintained skill's frontmatter and provider metadata;
- check that all registered skill and documentation paths exist;
- check links from `AGENTS.md` to overview/index/Feature leaves and back-links;
- confirm Requirements/Spec/ADR states and owner links are internally consistent;
- confirm root and runtime rules preserve project-specific safety and authorization boundaries;
- run the target project's existing docs, lint, and relevant test commands;
- run `git diff --check`.

Do not declare the project upgraded merely because canonical files were copied. The target-specific
diff and validation evidence are the completion criteria.

## Rollback

Keep each project's harness maintenance in an isolated commit or otherwise clearly reviewable diff.
Rollback uses that target project's normal version-control process. Restore the previous individual
skill files and governance sections together; do not leave new producer contracts with old consumer
skills, or new registry entries pointing to removed paths.

Preserve failed migration evidence until the target owner confirms restoration. Rollback does not
imply that active Feature or code changes made under separate authorization should also be reverted.

## Multi-Project Rollout

Maintain multiple projects in small, reviewable groups:

1. Inventory each target's grouped, flat, partial, or extended layout.
2. Record which coordinated skills each target actually uses.
3. Compare files read-only and classify local differences.
4. Start with one clean representative project.
5. Apply and validate one target-owned change at a time.
6. Defer dirty projects until unrelated work is isolated by their owners.
7. Migrate Feature documents only when active work touches them.
8. Record target, source revision, changed skills, preserved customizations, governance diff,
   validation commands/results, owner, and rollback status.

There is intentionally no central marker or automated fleet status. The target repository history,
reviewed diff, and validation evidence are the source of truth for its maintained skill state.
