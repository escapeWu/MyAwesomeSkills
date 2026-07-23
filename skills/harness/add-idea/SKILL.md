---
name: add-idea
description: >-
  Unified, docs-only entry for adding a product or engineering idea to a
  harness-managed repository. Use when the user invokes add-idea or asks to
  turn an idea into a new Feature or a bounded change to an existing Feature.
  Inspect current owners first, Grill unclear ideas one decision at a time,
  then create or patch requirements, a Spec, and conditional ADRs without
  implementing code or publishing external issues.
disable-model-invocation: true
---

# Add Idea

Use this as the single explicit intake for an idea. The outcome is a clear,
routed internal contract, not code implementation.

Read [references/routing-contract.md](references/routing-contract.md) completely
before deciding the route. When writing durable artifacts, also read
`../progressive-disclosure-docs/references/feature-spec-decision-contract.md`.

## Invariants

- Keep the original user outcome visible while refining details.
- Investigate repository facts; ask the user only for decisions.
- Ask one question at a time during Grill and include a recommended answer with
  a short rationale.
- Do not write Feature, requirements, Spec, or ADR docs until the user confirms
  the final shared-understanding summary.
- The agent chooses the owner route from evidence. Ask the user only when two or
  more owners remain equally valid or the choice changes a product boundary.
- This skill never grants code implementation, deployment, training, execution,
  external publication, or issue-tracker actions.
- Do not persist interview transcripts or a separate idea backlog. Confirmed
  content must return to the existing Feature/requirements/Spec/ADR owners.

## Workflow

### 1. Discover the current ownership map

Read progressively:

1. root `AGENTS.md` or equivalent;
2. `docs/OVERVIEW.md`;
3. `docs/feature/INDEX.md`;
4. at most the likely owning Feature README/INDEX and `requirements.md` files;
5. targeted reference docs and code only when they can settle a fact.

Record in the session:

- the problem, actor, and intended outcome;
- candidate Feature owners and supporting evidence;
- existing expected behavior and current implementation;
- safety, authorization, public-contract, and data boundaries;
- facts already established and decisions still open.

Do not create a new Feature merely because the user used a new phrase. Prefer an
existing owner when its responsibility and lifecycle genuinely cover the idea.

### 2. Apply the clarity gate

An idea is ready for routing only when these are clear enough to distinguish
ownership and acceptance:

- problem and intended user/business outcome;
- in-scope and out-of-scope behavior;
- measurable acceptance or an observable completion condition;
- relevant constraints, safety, authorization, and compatibility boundaries;
- candidate owner and affected contracts;
- unresolved decisions that would change the owner, public behavior, schema,
  state ownership, migration, validation, or rollback.

If route-affecting ambiguity remains, enter Grill. If all items are already
clear from the request and repository, skip Grill and summarize the inferred
boundary for confirmation.

### 3. Grill unclear ideas

Walk the unresolved decision tree in dependency order:

1. Ask exactly one decision question.
2. Give the recommended answer and why it best fits current evidence.
3. Wait for the user's answer before advancing.
4. Update the in-session decision ledger: confirmed facts, user decisions,
   rejected alternatives, open questions, and affected owners.
5. Look up newly discoverable facts instead of asking for them.

Do not draft contracts while questions remain open. When all blocking branches
are resolved, present one compact shared-understanding summary containing:

- problem and outcome;
- scope and non-goals;
- acceptance and stop conditions;
- selected owner and affected contracts;
- durable decisions and remaining non-blocking unknowns;
- recommended documentation route.

Ask for explicit confirmation. Continue only after the user confirms the
summary or corrects it.

### 4. Choose two independent routes

Choose one **owner route**:

- `CREATE_FEATURE`: the idea needs an independent durable owner.
- `PATCH_FEATURE`: exactly one existing Feature owns the behavior.
- `BLOCKED_OWNER`: ownership remains ambiguous or conflicts with project
  boundaries; stop and surface the competing owners.

Then choose one or more **artifact routes**:

- `REQUIREMENTS_PATCH`: expected behavior, acceptance, non-goals, constraints,
  or stop rules change.
- `NEW_SPEC`: implementation-relevant contracts change, including public API,
  schema, state machine, module ownership, data flow, migration, compatibility,
  security, validation, rollout, or rollback.
- `ADR_CANDIDATE`: a durable architecture decision meets the decision trigger.
- `STATE_ONLY`: only the Feature's durable current-state summary or routing
  changes; do not invent requirements or a Spec.
- `NO_DURABLE_CHANGE`: the idea is a reversible local detail with no expected
  behavior, contract, decision, or durable state impact; report the owner and
  stop without changing docs.

`CREATE_FEATURE` and `NEW_SPEC` are not opposites. A new Feature normally starts
with requirements and may also receive its first Spec. An existing Feature may
receive a requirements patch, a new Spec, an ADR, or a combination.

State the chosen routes and evidence before writing. Do not ask the user to pick
between routes when the repository evidence is decisive.

### 5. Materialize the confirmed contract

Follow the shared Feature/Spec/ADR contract.

For `CREATE_FEATURE`:

- create the Feature from
  `../progressive-disclosure-docs/assets/feature-template/`;
- replace every placeholder with confirmed content;
- after faithfully materializing the confirmed boundary, set requirements to
  `CONFIRMED`, record the real confirmation date/authority when known, and
  update README requirements/route status; do not leave initial `DRAFT`
  scaffolding or a stale contract-freeze blocker;
- register it in `docs/feature/INDEX.md` and `docs/OVERVIEW.md`;
- keep Feature lifecycle separate from Spec delivery status.

For `PATCH_FEATURE`:

- update the existing owner in place;
- set a changed requirements revision to `CONFIRMED` only when the confirmed
  shared-understanding summary fully covers that revision; otherwise stop
  rather than writing a partial contract;
- preserve unrelated requirements and current-state content;
- add a new Spec instead of overwriting a validated or superseded Spec;
- update parent routes and back-links only when new artifacts are created.

For artifact routes:

- when `NO_DURABLE_CHANGE` applies, write no docs and explain why;
- write expected behavior only to `requirements.md`;
- create a Spec and lazy index from `../progressive-disclosure-docs/assets/spec-template.md` and `../progressive-disclosure-docs/assets/spec-index-template.md` when `NEW_SPEC` applies;
- create an ADR and lazy index from `../progressive-disclosure-docs/assets/adr-template.md` and `../progressive-disclosure-docs/assets/decision-index-template.md` only when the ADR trigger applies;
- keep ADR-worthy rationale out of README and keep implementation design out of
  requirements;
- update README with links and compact status only;
- append the durable transition to `changelog.md`.

A blocking ADR stays `proposed` until the decision authority accepts it. A Spec
cannot become `frozen` while blocking decisions or contract questions remain.

### 6. Stop at the documentation gate

Finish with:

- selected owner route and rationale;
- artifact routes and files created or updated;
- requirements, Spec, and decision statuses;
- unresolved blockers;
- next documentation or validation gate;
- explicit statement that implementation remains unauthorized.

Do not implement code in the same invocation. A later implementation request
must enter `project-docs-workflow` and re-check the frozen contracts.

## Stop conditions

Stop without expanding the change when:

- the user has not confirmed shared understanding;
- no owner can be selected without changing a product boundary;
- expected behavior conflicts with an existing frozen contract;
- a blocking architecture decision is still unresolved;
- the requested artifact would create a second SSOT;
- the request crosses a safety, authorization, data, or external-publication
  boundary that the user has not explicitly approved.
