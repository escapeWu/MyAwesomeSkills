# Add Idea Routing Contract

Use this contract to decide whether an idea creates a Feature or extends an
existing Feature. Make the decision from repository evidence after the idea is
clear; do not route from keywords alone.

## 1. Session-only intake schema

Keep this ledger in the conversation until shared understanding is confirmed:

```text
Problem:
Actor / beneficiary:
Desired outcome:
In scope:
Out of scope:
Acceptance / observable completion:
Constraints and safety boundaries:
Candidate owners:
Confirmed facts:
User decisions:
Rejected alternatives:
Open questions:
Affected contracts:
```

This ledger is not repository SSOT and must not be saved as `idea.md`,
`interview.md`, or any parallel progress/control file.

## 2. Clarity classification

Classify the intake as:

- `CLEAR`: ownership and acceptance can be decided from the request and current
  repository evidence.
- `GRILL_REQUIRED`: at least one unresolved decision can change ownership,
  scope, public behavior, schema/state, safety, validation, or rollback.
- `BLOCKED_FACT`: a required fact should be discoverable but cannot currently be
  verified. Report the missing source instead of asking the user to guess.

Do not Grill optional implementation details that can remain open in a draft
Spec. Grill only decisions needed to define the boundary or freeze a contract.

## 3. Owner route

### `PATCH_FEATURE`

Choose an existing Feature when all are true:

1. one current Feature already owns the affected user/business behavior;
2. the idea extends or corrects that responsibility without introducing an
   independent long-term outcome;
3. acceptance can be expressed as an addition or revision to that Feature's
   requirements;
4. lifecycle, authorization, evidence, and release boundaries remain owned by
   the same Feature;
5. no new top-level public artifact or cross-Feature coordination owner is
   required.

Evidence should include the owning README/requirements route and, when relevant,
current code or interface references.

### `CREATE_FEATURE`

Create a Feature when any strong ownership signal applies:

- independent user or business outcome;
- independently accepted, deprecated, or maintained lifecycle;
- independent public contract, data product, persistent artifact, or external
  integration boundary;
- distinct safety, authorization, evidence, or rollout boundary;
- cross-Feature change that needs one durable coordination owner;
- its own roadmap or multiple delivery Specs;
- existing owner would become a catch-all with unrelated responsibilities;
- existing granularity rules already require promotion to a Feature.

Do not use document count alone when the content still belongs to one owner.
Document growth is supporting evidence, not a substitute for responsibility.

### `BLOCKED_OWNER`

Stop when:

- two Features both plausibly own the behavior and the difference affects public
  contracts or lifecycle;
- the proposed owner contradicts existing requirements or architecture rules;
- the idea is actually a project-wide policy and no system-level owner exists;
- selecting an owner would silently redefine an existing Feature boundary.

Present the competing owners, consequences, and recommendation as one decision
question.

## 4. Artifact route

Owner routing and artifact routing are independent.

| Change | Required artifact |
|---|---|
| Expected behavior, acceptance, non-goals, NFR, stop rule | `REQUIREMENTS_PATCH` |
| API/schema/state/dataflow/module/migration/test/rollout contract | `NEW_SPEC` |
| Durable architecture choice with real alternatives | `ADR_CANDIDATE` |
| Current snapshot or route only | `STATE_ONLY` |
| Reversible local detail with no durable truth change | `NO_DURABLE_CHANGE` |

A single idea may produce `REQUIREMENTS_PATCH + NEW_SPEC + ADR_CANDIDATE`.

### When a Spec is not required

Do not force a Spec for:

- wording-only requirements clarification with no implementation consequence;
- current-state correction that does not change expected behavior;
- trivial local implementation detail already governed by a frozen or validated Spec;
- reversible local detail with no expected behavior, contract, decision, or durable state impact (`NO_DURABLE_CHANGE`);
- archive or route repair with no contract change.

### When a Spec is required

Create a Spec when implementation must freeze any of:

- public interface or schema;
- data ownership, mutable state, lifecycle, or state transition;
- cross-module dependency or integration behavior;
- migration, compatibility, rollout, rollback, or stop behavior;
- security, privacy, authorization, or evidence boundary;
- module ownership, file/interface boundary, or test seam;
- validation matrix and pass criteria for a non-trivial change.

## 5. ADR trigger

Create an ADR only when the decision is durable and all three default signals
are present:

1. changing it later has meaningful cost;
2. a future maintainer could reasonably choose differently without the context;
3. credible alternatives exist and the choice reflects a real trade-off.

Public data ownership, security boundary, persistence technology, deployment
topology, cross-Feature integration, or irreversible migration decisions should
be treated as strong ADR candidates.

Do not create an ADR for reversible local implementation details, obvious
conformance to an existing contract, formatting, naming with no domain effect,
or choices already owned by an accepted ADR.

## 6. Decision output

Before writing files, report:

```text
Clarity: CLEAR | GRILL_COMPLETED
Owner route: CREATE_FEATURE | PATCH_FEATURE | BLOCKED_OWNER
Selected owner: <path or proposed feature slug>
Owner evidence: <concise evidence>
Artifact routes: [REQUIREMENTS_PATCH, NEW_SPEC, ADR_CANDIDATE, STATE_ONLY, NO_DURABLE_CHANGE]
Blocking decisions: <none or list>
Documentation authorization: docs-only
Implementation authorization: none
```

The user confirms the shared boundary, not a menu of arbitrary route choices.
