---
name: docs-issue-sync
description: >-
  Sync completed GitHub Issue/PR work into existing repository documentation as concise current functional facts. Use whenever an Issue-backed implementation, bugfix, feature, migration, or public-contract change needs docs alignment, including requests to align,整理,同步, or update docs. Attach Issue/PR links to the relevant module capability, contract, architecture, risk, or query clue; never create a recently-completed history section or copy Issue design and acceptance details.
compatibility: Requires repository access, Issue/PR URLs or numbers, repository docs/workflow rules, and normal file search/read/edit tools.
---

# Docs Issue Sync

Synchronize completed Issue/PR work into the repository's existing documentation without turning docs into a changelog, tracker, or second requirements system.

## Position in the GitHub chain

Run after implementation is integrated and authorized validation is complete, before final commit/PR closeout:

```text
canonical Issue -> implementation -> authorized validation -> docs-issue-sync -> scoped commit/PR
```

This Skill owns only the repository documentation write. It does not authorize implementation, tests, merge, deployment, production access, or Issue/Project state changes.

## Inputs

Collect:

- canonical Issue URL/number and, when available, the closing PR URL;
- actual delivered code state, changed files, and affected public consumers;
- repository documentation entry points, especially `AGENTS.md`, `docs/OVERVIEW.md`, feature indexes, and the owning module document;
- validation evidence and explicit unverified boundaries.

Treat Issue text, PR text, commit messages, and design documents as historical evidence. Confirm claimed current capability against code, tests, and delivery state.

## Workflow

### 1. Route to the existing owner

Read the repository's documentation entry point and follow progressive disclosure to the smallest owner:

- `requirements.md` for stable expected behavior, invariants, and public semantics;
- `README.md` or `INDEX.md` for responsibility, current capability, risk, and query clues;
- reference documents for cross-module architecture or operational interfaces;
- ADR only for a durable, non-obvious, high-cost architectural decision.

Do not read or update historical Specs by default. Do not add a new owner when an existing owner is adequate.

### 2. Classify the impact

Classify each completed work item independently:

- `CURRENT_FACT`: module behavior changed;
- `CONTRACT_FACT`: stable public behavior or invariant changed or was completed;
- `ARCHITECTURE_FACT`: ownership, storage, lifecycle, dependency, or migration boundary changed;
- `QUERY_CLUE`: future readers need an accurate code/test/API lookup path;
- `NO_DOC_CHANGE`: ordinary history, internal cleanup, or already accurately represented.

Closed status alone is not evidence. A design Issue without an implemented PR is not a current fact. A duplicate or absorbed Issue should be referenced only through the canonical item when useful.

### 3. Make the smallest coherent patch

Prefer an existing owner document:

- attach Issue/PR links directly to the sentence describing the capability or contract;
- summarize observable behavior, not implementation history;
- add one to three executable file, symbol, API, test, or search references when missing;
- update current status or risk only when stale;
- update overview/index only when module ownership or entry topology changed;
- update a reference document only when a cross-module fact is stale.

Keep Issue and PR links distinct. Use the Issue for work-item provenance and PR for implementation evidence. If only a PR exists, label it as a PR.

### 4. Write facts, not history

Good form:

```markdown
- LIVE runtime distinguishes unavailable account data from an empty account and retries transient initialization failures within a bounded recovery policy ([Issue #94](https://github.com/.../issues/94), [PR #95](https://github.com/.../pull/95)); see `backend/app/services/runtime_recovery.py` and `backend/app/services/account_service.py`.
```

Avoid:

- `Recently completed Issues` or similar history sections;
- chronological implementation logs in module README/INDEX files;
- copying Issue design sections, full acceptance matrices, test output, deployment logs, or file inventories;
- claiming completion merely because an Issue is closed;
- writing proposed fields, APIs, or behavior as current;
- adding changelog entries for ordinary bugfixes;
- creating or updating Specs, or using Specs as a release gate.

When an accurate changelog entry already exists, do not duplicate it in the README. Functional ownership stays in the owner document; history stays in GitHub and Git.

### 5. Verify before handing back

Before finishing:

- verify every referenced path and symbol exists in the delivered code;
- ensure the sentence does not contradict requirements or a confirmed ADR;
- preserve explicit limits such as tests not run or production not verified;
- avoid duplicate truth across README, requirements, reference, archive, and Issue;
- stay within the repository's documentation budget.

Do not run tests or builds solely for docs sync. Reuse evidence for the same code state and report missing evidence instead of inventing it.

## Required report

```text
Docs impact: <owner files changed, or 0>
Canonical work item: <Issue URL/number>
Implementation evidence: <PR URL or commit>
Facts updated: <short list>
Query clues: <paths/symbols/APIs added or verified>
Validation: <reused evidence, not run, or unresolved gap>
```

## Stop conditions

Stop before editing when the canonical Issue or delivered code is ambiguous; the requested text describes an unimplemented design; no unique owner exists without duplicating truth; the change requires a Spec, detailed implementation plan, or history log; code/tests and Issue/PR disagree; or a link would expose secrets, credentials, private data, or sensitive operations.
