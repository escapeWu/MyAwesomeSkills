---
name: external-collaboration-workflow
description: >-
  Manage a lightweight external-team collaboration record: prepare a problem brief, preserve a received proposal,
  record internal adoption decisions, implement only after explicit authorization, and link the final result to core
  project docs and validation. Use when provenance across an external handoff matters. Do not turn external proposals
  into internal truth or generate a heavy contract lifecycle.
---

# External Collaboration Workflow

Use this skill only when a durable external handoff needs provenance. Ordinary design discussion does not need a case.

## Minimal Case

```text
docs/collaboration/<case-id>/
├── INDEX.md               # status, source versions, adoption decisions, final links
├── problem-statement.md   # concise internal problem and evidence brief
└── external-proposal.md   # faithful external response
```

The case records source and adoption. It is not a parallel implementation plan or progress tracker.

## Stages

### 1. Prepare the problem brief

Read the owning Feature README, relevant code, and only the references needed to explain the problem. Include:

- desired outcome and broad scope;
- current behavior and observed evidence;
- hard safety, authorization, privacy, compatibility, or data boundaries;
- the few questions the external team must answer.

Use the included script when a formal case is warranted:

Run from the target repository root (or pass `--repo-root` explicitly):

```bash
cd /path/to/target-repository
EXTERNAL_COLLAB_SKILL_ROOT=/absolute/path/from-the-current-skill-registry
python3 "$EXTERNAL_COLLAB_SKILL_ROOT/scripts/create_case.py" \
  --case-id EC-YYYY-NNN-short-slug \
  --title "Case title" \
  --feature owning-feature-slug \
  --external-team "External team"
```

Do not ask the user for repository facts that can be inspected. Ask only for an unknown external owner, source, desired
outcome, or hard boundary that is essential to the handoff.

### 2. Preserve the external response

Record the external owner, received date, source location, and source version or fingerprint when available. Keep the
proposal faithful to the source; internal comments belong in the case INDEX.

If the proposal cannot be tied to a recognizable source, say so. Require exact version binding only when later auditing
or multiple revisions make it meaningful.

### 3. Decide what to adopt

Record each material recommendation as accepted, modified, rejected, deferred, or pending, with a short rationale. Small
or tightly coupled recommendations may be grouped; do not atomize every sentence.

An external proposal is advice, not implementation authorization. Internal project rules, current code, and user direction
remain authoritative.

### 4. Implement through the normal workflow

Before code changes, make sure the accepted outcome and hard boundaries are clear in the case or owning Feature README.
Do not require a separate requirements file, Spec, ADR, validation matrix, or status lifecycle.

Then use `project-docs-workflow`:

- implement in current repository patterns;
- verify according to risk and existing project practice;
- keep temporary implementation progress in the session;
- after completion, the main Agent asynchronously delegates one combined docs pass.

The main Agent gives one docs SubAgent the final implementation summary, validation results, candidate Feature/reference
owners, and case path. That SubAgent is the only docs writer and may update the owning Feature README, a stable
interface/runbook reference, and the case INDEX with final implementation and validation links. The main Agent does not
wait for this ancillary work or edit the same docs concurrently. If SubAgents are unavailable, use the same one-pass
fallback at the end. Do not update these documents after every intermediate step.

### 5. Close

Close the case when all material recommendations have a decision and accepted work is completed, deferred, or explicitly
left pending. Link to the durable owner and meaningful validation evidence; do not copy per-file progress into the case.

## Stop Conditions

Stop expansion and report the blocker when:

- the external source is missing or materially ambiguous;
- a recommendation is still pending and implementation depends on it;
- the proposal crosses safety, authorization, privacy, destructive, or compatibility boundaries;
- the user asked only for intake/review and did not authorize implementation;
- current code contradicts the proposal and the intended outcome remains unclear.

## Final Report

State the case status, source, adopted/modified/rejected/deferred recommendations, implementation result, validation, and
remaining blockers. Keep it concise and link to the owners instead of reproducing their contents.
