# Feature, Spec, and Decision Contract

Use this contract whenever a harness-managed repository creates or changes a
Feature, implementation Spec, or architecture decision.

## 1. Separate durable owners

| Truth | Owner | Must not contain |
|---|---|---|
| Feature map and current capability/state | Feature `README.md` | detailed implementation design or decision rationale |
| Expected behavior and acceptance | `requirements.md` | module layout, pseudocode, current implementation claims |
| Bounded implementation contract | active `Spec` | product rationale duplicated from requirements |
| Durable architecture rationale | `ADR` | progress tracking or full implementation plan |
| Current implementation | code | claims about unimplemented future behavior |
| State-transition history | `changelog.md` | mutable current snapshot |
| Validation evidence | immutable artifact, ledger, or gate report | unsupported narrative claims |

README links these owners and reports compact statuses; it does not duplicate
their bodies.

## 2. Default paths

```text
docs/feature/<feature>/
├── INDEX.md                 # optional for large Features
├── README.md                # Feature map and current state
├── requirements.md          # expected behavior and acceptance
├── specs/                   # create lazily
│   ├── INDEX.md
│   └── SPEC-YYYY-NNN-slug.md
├── decisions/               # create lazily for Feature-local decisions
│   ├── INDEX.md
│   └── ADR-YYYY-NNN-slug.md
└── changelog.md

docs/reference/decisions/    # create lazily for cross-Feature/system decisions
├── INDEX.md
└── ADR-YYYY-NNN-slug.md
```

Create lazy indexes from `assets/spec-index-template.md` and
`assets/decision-index-template.md`. Preserve an existing repository ADR
convention when it already has one clear owner. Never create a second ADR tree.
Every Spec/ADR must be reachable from its Feature or reference index and link
back to that owner.

IDs are immutable. Use the next available year-local sequence in the owning
index unless the repository already defines another scheme.

## 3. Independent lifecycles

### Feature lifecycle

```text
PROPOSED -> ACTIVE -> MAINTENANCE -> DEPRECATED -> RETIRED
     \-> ABANDONED
```

A Feature is a durable capability owner. Its lifecycle does not move to
`IMPLEMENTATION_ACTIVE` every time a new change is built.

### Requirements status

```text
DRAFT -> CONFIRMED -> SUPERSEDED
```

Changing confirmed expected behavior requires a new revision entry and reopens
any affected frozen Spec.

### Spec lifecycle

```text
DRAFT -> FROZEN -> IMPLEMENTATION_ACTIVE -> VALIDATION_ACTIVE
      -> VALIDATED | REJECTED | SUPERSEDED
```

A Spec is `FROZEN` only when its required contracts and decisions are resolved.
Changing a frozen public contract returns it to `DRAFT` or creates a superseding
Spec; record the transition in the Feature changelog.

### ADR lifecycle

```text
PROPOSED -> ACCEPTED | REJECTED
ACCEPTED -> SUPERSEDED | DEPRECATED
```

Do not rewrite an accepted ADR to express a new decision. Create a new ADR and
link `supersedes` / `superseded_by` in both records.

## 4. Feature creation gate

A new Feature requires:

- an independent durable owner under the Feature granularity rules;
- problem, actor/outcome, scope, and non-goals;
- expected behavior and measurable/observable acceptance;
- constraints, NFRs, safety/authorization, and stop rules;
- a README current-state route and changelog;
- registration in `docs/feature/INDEX.md` and `docs/OVERVIEW.md`.

Creating a Feature does not automatically require an ADR. Create the first Spec
only when implementation-relevant contracts are known or need to be frozen.

## 5. Spec freeze gate

A Spec may become `FROZEN` only when applicable fields are complete:

- requirements version/reference;
- scope and non-goals;
- accepted blocking ADR references;
- public API, schema, artifact, and compatibility contracts;
- data flow, state machine, mutable-state owner, and serialization boundaries;
- module responsibilities, interfaces, dependency direction, and reuse boundary;
- security, privacy, authorization, and evidence boundaries;
- migration and backward-compatibility behavior;
- validation matrix with seams, tests, evidence, and pass criteria;
- rollout, rollback, stop conditions, and failure handling;
- zero blocking open questions;
- explicit docs-only versus implementation authorization.

Not every Spec needs every section. Mark a section `Not applicable` with a
reason rather than silently omitting a risk-bearing category.

A frozen Spec is `IMPLEMENTATION_READY` only when code entry points, file
budgets, test owners, next gate, and separate implementation authorization are
also clear.

## 6. ADR trigger and gate

Create an ADR when a decision is difficult to reverse, surprising without its
context, and based on a real trade-off. Strong candidates include system/Feature
boundaries, data ownership, persistent storage, public protocol, deployment
topology, security model, and irreversible migration.

A blocking ADR must be `ACCEPTED` before a dependent Spec becomes `FROZEN`.
`PROPOSED` ADRs contain a recommendation, not an accepted decision. `REJECTED`
ADRs remain discoverable so the same option is not repeatedly reconsidered.

## 7. Patch rules

For an existing Feature:

- patch `requirements.md` only when expected behavior changes;
- create a new Spec for a new bounded implementation change;
- do not overwrite a validated or superseded Spec;
- create an ADR only for ADR-worthy choices, not every design detail;
- keep current implementation claims in README aligned with code;
- append state transitions to `changelog.md`;
- route completed historical Specs according to the repository archive policy.

## 8. Progressive disclosure

Default reading remains:

```text
AGENTS -> OVERVIEW -> Feature INDEX -> Feature README/requirements
```

Read an active Spec only for implementation, review, validation, or contract
questions. Read an ADR only when its scope affects the current decision. Do not
load every historical Spec or ADR.

## 9. Confirmation and authorization

A user confirmation freezes the described product/engineering boundary; it does
not grant implementation, deployment, execution, publication, or destructive
actions. When `add-idea` faithfully materializes the confirmed boundary, change
the affected requirements revision from `DRAFT` to `CONFIRMED` and update the
Feature README route/status in the same write. Store decision authority and date
only when the project can name them accurately. Never invent an approver identity.
