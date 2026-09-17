# Module Extraction Guide

Use this guide to reason about ownership and compatibility during a large-module refactor. Adapt it to the repository;
these are heuristics, not a required directory taxonomy or fixed plan template.

## Responsibility Heuristics

A symbol often belongs with one of these responsibilities:

| Responsibility | Typical content |
|---|---|
| domain | rules and calculations with little or no external I/O |
| state | mutable state, lifecycle, cache ownership |
| adapter | filesystem, network, database, framework, or external formats |
| orchestration | coordinating several owners for one use case |
| reporting | output artifacts, serialization, summaries, presentation models |
| contract/type | shared data shapes, protocols, enums, stable constants |
| entrypoint | CLI, runner, plugin, strategy, or framework integration |

Use the repository's existing names when they are clearer. If one symbol carries several responsibilities, split the
symbol rather than moving the same mixture into a new file.

## Good Extraction Order

A common low-risk order is:

1. pure types and constants;
2. stateless transformations;
3. independent parsers, validators, or formatters;
4. external adapters;
5. explicit state owners;
6. orchestration and final entrypoint cleanup.

Change the order when dependencies or state make another sequence safer.

## Shared-Code Check

A shared module is justified when real consumers need the same semantics, errors, precision, and lifecycle, and the shared
code does not depend back on one consumer. Predicted future reuse is not enough.

## State And Side Effects

- Keep one clear owner for each mutable state.
- Preserve initialization, read/write, flush, and cleanup order.
- Make file/network/time/random/environment dependencies visible.
- Check cache keys, invalidation, concurrency, and serialization when moving caches.
- Prefer composition when mixins would obscure ownership.

## Compatibility

| Situation | Typical handling |
|---|---|
| repository-internal consumers can move together | update imports directly |
| stable public import or plugin discovery uses old path | thin re-export or adapter |
| strings dynamically load a module/class | preserve path or provide explicit migration |
| persisted data records a class/module path | keep path or design a safe migration |
| external consumers depend on output schema/name | preserve it unless separately versioned and authorized |

A compatibility shim should stay thin and should not duplicate the real implementation.

## Consumers Worth Checking

Search beyond normal imports when relevant:

- re-exports and aliases;
- CLI/plugin registries and dynamic strings;
- fixtures, monkeypatch, and mock targets;
- serialization/checkpoint class paths;
- config examples, scripts, CI, notebooks, and artifact readers.

## Validation Options

Select checks that match the actual risk:

- import and signature smoke checks;
- existing unit/integration tests around moved behavior;
- characterization or golden output comparison;
- CLI/config/default/error behavior;
- state lifecycle and side-effect order;
- cycle/duplicate-owner inspection;
- formatter, linter, and type checker already used by the project.

No universal matrix or testing order is required.

## Avoid

- `module_part1.py` / `module_part2.py` splits;
- moving everything into `utils.py`;
- deleting types, comments, or tests only to reduce line count;
- changing business behavior while claiming a structural refactor;
- keeping two live implementations indefinitely;
- deleting old paths before checking dynamic consumers;
- claiming equivalence from lint alone.
