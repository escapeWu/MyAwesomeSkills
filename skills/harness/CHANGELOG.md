# Harness Skills Changelog

This file records coordinated changes to the harness skills suite. It is not a release manifest or
installation record. Feature-local `changelog.md` files remain the append-only history for one
Feature and must not be used as suite maintenance notes.

## Unreleased

### Changed

- Reduced the suite to a lightweight core-docs model: small navigation files, Feature READMEs, and targeted references.
- Moved documentation maintenance to one asynchronous SubAgent after implementation and validation complete; the main
  Agent supplies a bounded handoff, does not wait for ancillary maintenance, and does not write the same docs concurrently.
- Simplified `add-idea` so Grill asks only the highest-impact unresolved product or hard-boundary question and skips
  questionnaire-style clarification.
- Made `project-analysis` answer directly by default and persist findings only when they are durable or explicitly requested.
- Replaced machine route manifests and multi-axis status schemas with optional, readable route guidance.
- Made suite maintenance references optional so flat and partial target layouts do not receive broken parent links.
- Made diagrams and ASCII/TUI companions optional, and made `add-idea` references safe for partial installations.
- Kept lightweight external-collaboration templates linkable from existing target validators without restoring metadata lifecycles.

### Removed

- Removed required implementation Spec lifecycles, pre-implementation documentation gates, fixed validation matrices,
  and harness-prescribed test ownership/TDD behavior.
- Removed the Spec, requirements, ADR, decision-index, Feature changelog, and route-manifest templates from the default
  harness assets.
- Removed mandatory staged docs updates; implementation tasks now perform at most one asynchronous docs pass after
  completion.

## 2026-07-23 - Idea Intake And Contract Lifecycle

### Added

- Added the explicit, docs-only `add-idea` entry point.
- Added one-question-at-a-time Grill behavior with a user-confirmed shared-understanding gate.
- Added independent owner routes: `CREATE_FEATURE`, `PATCH_FEATURE`, and `BLOCKED_OWNER`.
- Added independent artifact routes for requirements, Specs, ADR candidates, state-only changes, and
  `NO_DURABLE_CHANGE`.
- Added a shared Feature/Requirements/Spec/ADR ownership and lifecycle contract.
- Added Spec, Spec index, ADR, and decision index templates.
- Added routing eval cases for vague ideas, new Features, existing Feature patches, blocking ADRs,
  and reversible local changes.
- Added [`UPGRADING.md`](UPGRADING.md) for manual, per-project maintenance of existing skill copies.

### Changed

- Separated long-lived Feature lifecycle from bounded Spec implementation and validation lifecycle.
- Reduced Feature README ownership to current state, route, blockers, next gate, and contract links.
- Kept expected behavior, acceptance, NFRs, non-goals, and stop rules in `requirements.md`.
- Moved bounded implementation interfaces, schema, state, module boundaries, migration, testing, and
  validation matrices into Specs.
- Required confirmed requirements, accepted blocking ADRs, and a frozen Spec before later
  contract-affecting implementation can become implementation-ready.
- Updated project analysis, project docs, external collaboration, bootstrap, demo, and runtime gate
  guidance to use the new contract.
- Defined trigger-based migration for existing Feature documents instead of bulk rewriting them.

### Removed

- Removed the curated bundle manifest, automated bundle installer, automatic overwrite, and
  suite-level deployment semantics.
- Kept maintenance intentionally per skill and per target project; no bundle version or installation
  marker is introduced.

### Maintenance Notes

- Existing Feature documents remain valid legacy inputs and migrate only when related work touches
  them.
- Target-owned `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `docs/OVERVIEW.md`, Feature documents, and
  project code must be changed only through the target project's normal reviewed workflow.
- Existing projects may maintain all harness skills, a subset, or project-specific extensions. Do
  not add missing skills unless the target project needs and accepts them.
- Follow [`UPGRADING.md`](UPGRADING.md) to audit layout, compare individual skills, preserve local
  changes, validate target-specific routes, and roll back through version control.

## Earlier History

Earlier harness copies had no suite-level changelog. They may use grouped, flat, partial, or
project-customized skill layouts. Treat their current files and target repository history as the
migration evidence; do not infer a common installed version.
