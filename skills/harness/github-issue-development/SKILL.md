---
name: github-issue-development
description: >-
  Global GitHub Issue-to-PR development workflow. Use whenever a user asks to add, defer, triage, manage, implement, fix, or resolve a GitHub Issue, or asks about Issues, Projects, worktrees, PRs, or completion. For an existing Issue delivery request, read and normalize the canonical Issue, implement from an exact base in an isolated worktree, commit, push, create or update the PR, then wait for merge unless explicitly narrowed. Keep validation, merge, deployment, production, force-push, and secret-use gates separate.
metadata:
  version: "1.2.0"
---

# GitHub Issue Development

Provide one reusable Issue-to-PR workflow without turning GitHub into a requirements database or treating work-item status as permission to change code.

## Precedence

Apply rules in this order:

1. explicit current user direction and authorization;
2. repository `AGENTS.md`, `CLAUDE.md`, local workflow Skills, Issue templates, contribution rules, and protected-operation gates;
3. this global workflow.

When a repository has a local project workflow or specialist, classify here and hand off the affected write surface. Local policy may be stricter; it must not weaken authorization, credential, or clean-base guarantees.

## Routes

| User intent | Route | Default action |
|---|---|---|
| Explain, compare, brainstorm, or explicitly request no writes | `DISCUSSION_ONLY` | Answer without GitHub, task, docs, branch, or code writes |
| Remember, defer, triage, create/update an Issue, or change Project fields | `ISSUE_INBOX` | Follow the repository's Issue intake workflow without implementation |
| Confirm stable expected behavior, public semantics, acceptance, or a durable decision | `CONTRACT_CONFIRMATION` | Use the repository's unique contract/docs owner; create an Issue only when tracking is also requested |
| Implement or fix repository work not sourced from an existing Issue | `IMPLEMENT_NOW` | Perform local implementation; push and PR remain separate unless explicitly requested |
| Implement, fix, resolve, or deliver an existing Issue | `ISSUE_TO_PR` | Normalize the Issue, implement in an exact-base worktree, commit, push, create/update the PR, then wait for merge |

Classify from the requested outcome and canonical source. A current request to solve an existing Issue authorizes its routine Issue-to-PR delivery writes. Issue or Project status alone does not. Explicit limits such as `local only`, `do not push`, or `no PR` narrow the route.

## Authority boundaries

- Discussion does not authorize Issue, Project, docs, branch, worktree, code, validation, push, deployment, or production writes.
- `ISSUE_INBOX` authorizes only requested tracking writes.
- An Issue, Label, priority, milestone, assignee, or Project `Ready` never authorizes implementation by itself.
- `IMPLEMENT_NOW` authorizes local code changes only; push and PR require explicit request.
- `ISSUE_TO_PR` authorizes canonical Issue reading, required tracking updates, exact-base worktree creation, implementation, local commits, feature-branch push, PR creation/update, and waiting for merge.
- `ISSUE_TO_PR` does not authorize pytest or other opt-in validation, merge, force-push, deployment, production access, destructive cleanup, or secret use.
- Never expose credentials, private attachments, tokens, signed URLs, account data, or secrets in Issues, commands, branches, commits, or PRs.

## Progressive reading

Read only the repository material needed for the selected route:

- Issue/Project operations: the repository's Issue intake instructions and templates;
- Issue delivery, branch/worktree, or PR handoff: the repository's implementation and worktree instructions;
- docs impact: `docs/OVERVIEW.md`, the owning module document, and `docs-issue-sync` when installed;
- local policy: `AGENTS.md`, `CLAUDE.md`, and referenced owner Skills.

Do not preload every reference or every document for a discussion-only request.

## Standard workflow

1. Identify the repository, default/base branch, configured Git remotes, local rules, and requested outcome.
2. Classify the request and record explicit opt-outs.
3. For `ISSUE_INBOX`, search duplicates before creation and preserve one canonical work item through partial failures.
4. For `ISSUE_TO_PR`, read the current Issue and repository facts, normalize the title/body to the repository contract, preserve intent, and never infer priority.
5. Before creating a feature branch/worktree, run the repository's stronger local preflight when present; otherwise use its exact-base check and capture `WORKTREE_BASE_SHA`.
6. Keep implementation on a feature branch/worktree. Uncommitted content in another worktree is absent from the base.
7. Implement the canonical Issue scope and update stable contract docs only through the repository owner. Validate only as authorized.
8. Run `docs-issue-sync` after implementation and authorized validation when the delivered behavior changes a documented functional, contract, architecture, risk, or query-clue fact. It attaches Issue/PR references to those facts; it never creates a recent-completions history section or copies Issue details.
9. Inspect and commit the scoped diff, push the feature branch, create/update a PR against the exact base, link the canonical Issue, and read back PR URL/base/head/state.
10. Enter `WAITING_FOR_MERGE` after the PR is ready. Do not merge without explicit authorization; avoid tight polling.
11. After an observed merge, follow repository completion rules for base synchronization, safe cleanup, Issue closure, and Project `Done`. Deployment and production operations remain separate.
12. For `IMPLEMENT_NOW` not sourced from an Issue, do not infer push or PR authorization.

## Handoff

```text
Route: DISCUSSION_ONLY | ISSUE_INBOX | CONTRACT_CONFIRMATION | IMPLEMENT_NOW | ISSUE_TO_PR
Repository: <owner/name and local root>
Canonical work item: <Issue URL/number or none>
Requested writes: <GitHub | docs | worktree | code | commit | push | PR | deployment>
Authorization: <grants, opt-outs, and protected operations still missing>
Project state: <actual value, unavailable, or none>
Base: <remote/branch@sha, BLOCKED_BASELINE, or not applicable>
Delivery state: <FORMATTING_ISSUE | IMPLEMENTING | PR_OPEN | WAITING_FOR_MERGE | MERGED | BLOCKED | not applicable>
PR: <URL/base/head/state or none>
Next owner/action: <local specialist, wait condition, or exact next step>
```

Do not report routing, normalization, a commit, an open PR, or a passing local check as merged or accepted delivery.

## Stop conditions

Stop before the affected write when the repository, canonical Issue, write surface, or authorization is ambiguous; a duplicate cannot be distinguished; required permissions or policy are unavailable; the base is dirty, divergent, stale, or unresolved; unpublished work is assumed from another worktree; secrets would enter GitHub/Git; or a protected operation lacks authorization.
