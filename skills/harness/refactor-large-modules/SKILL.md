---
name: refactor-large-modules
description: >-
  Refactor an oversized or mixed-responsibility module when the user asks to split, extract, modularize, or reduce
  duplication, or when the target file is clearly obstructing safe change. Preserve public behavior and state while
  moving responsibilities incrementally. Use repository evidence and risk-matched validation; do not impose fixed
  line-count gates or create pre-implementation docs.
---

# Refactor Large Modules

Use this specialized skill when module size or mixed ownership is the actual problem. Do not invoke it merely because a
file crossed an arbitrary line threshold.

Read [`references/extraction-contract.md`](references/extraction-contract.md) as a practical guide, adapting it to the
language and repository rather than treating its categories as a mandatory architecture.

## Boundaries

- Preserve user-visible behavior, public imports, CLI/config behavior, data shape, error behavior, and state ordering unless
  the user separately authorizes a behavior change.
- Do not mix the refactor with unrelated product changes.
- Keep user modifications and repository-specific conventions intact.
- If the user requested analysis or a split plan only, do not implement.
- Use `project-analysis` only when ownership, state, or call flow cannot be established directly.

## Workflow

### 1. Inventory The Real Surface

Find the target module's entrypoints, public symbols, consumers, side effects, mutable state, external I/O, and relevant
tests. For Python, the included inventory script can provide a starting index:

```bash
REFACTOR_SKILL_ROOT=/absolute/path/from-the-current-skill-registry
python3 "$REFACTOR_SKILL_ROOT/scripts/inventory_python_module.py" <path>
```

Verify dynamic imports, plugin registration, fixtures, mock targets, serialization paths, and configuration strings with
targeted search. An AST inventory is not a complete call graph.

### 2. Capture Invariants In The Session

Record only the behavior that must remain stable for this change: public paths/signatures, inputs/outputs, state and side
effect ordering, compatibility boundaries, and meaningful baseline checks. Keep this in the session plan; do not create a
contract document just to start refactoring.

When behavior is unclear, run an existing focused test or create the smallest useful characterization check. This is a
risk-control choice, not a prescribed TDD sequence.

### 3. Choose Natural Owners

Group code by stable responsibility in a way that matches the repository. Common candidates are domain logic, state,
adapters, orchestration, reporting, contracts/types, and entrypoints. These are heuristics, not required folders.

Avoid numbered part files and catch-all `utils` modules. Extract a shared module only when real consumers need the same
semantics and the new dependency direction remains clear.

### 4. Move Incrementally

- Prefer low-state, low-dependency leaves first.
- Update imports and consumers in small coherent batches.
- Keep compatibility shims only for real external or dynamic consumers, with a clear reason.
- Make state ownership and side effects explicit; avoid hiding them in import behavior or mixins.
- Stop if the proposed split requires cycles or behavior changes.

### 5. Validate To Risk

Use the project's existing checks. Typical evidence may include import smoke tests, focused behavior tests, CLI/config
checks, golden output comparisons, static analysis, and affected integration tests. Run only what the change and project
support; do not force a universal matrix.

### 6. Hand Off Docs After Completion

After code and validation complete, the main Agent includes any durable ownership/interface changes in the one asynchronous
docs handoff from `project-docs-workflow`. One docs SubAgent updates the owning Feature README or reference once. The main
Agent does not wait for ancillary maintenance or write the same docs concurrently.

## Stop Conditions

Stop and report when mutable-state ownership is unknown, compatibility cannot be preserved, required consumers cannot be
found, a cycle is unavoidable, baseline behavior cannot be established for a high-risk move, or the change crosses the
user's authorized scope.

## Final Report

Summarize the ownership changes, compatibility handling, meaningful size/complexity improvement, validation performed,
remaining shims or risks, and the asynchronous docs handoff if needed. A shorter file alone is not a success criterion.
