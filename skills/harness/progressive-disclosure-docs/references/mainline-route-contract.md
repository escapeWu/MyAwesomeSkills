# Mainline Route and Cognitive Disclosure Contract

Use this reference when the user changes or asks about the project mainline, execution route,
parallel workstreams, inserted stages, current progress, blockers, or next step.

This is a shared contract, not a standalone route-management skill. `project-docs-workflow`
orchestrates the full loop; `project-analysis` is only an escalation for real dependency, join,
contract, evidence, or authorization ambiguity.

## Ownership stack

```text
AGENTS.md             stable collaboration and output rules
  -> OVERVIEW.md      single current-Feature pointer
    -> README.md      current route overlay and macro roll-up
      -> development-plan.md  stable DAG, dependencies and gates
      -> child GOALs           local workstream progress
        -> code/artifacts      implementation and evidence detail
```

- Do not copy current route state into AGENTS, OVERVIEW or Feature indexes.
- Keep current-turn ordering in the session plan.
- Append durable route transitions to the owning changelog.

## Route operations

| User intent | Normalized operation | Durable write |
|---|---|---|
| A then B | `A -> B` | README; development plan if dependency changed |
| A and B together | `A || B` | README + development plan + changelog |
| join after A/B | `[A || B] -> J` | README + development plan + changelog |
| insert X | `A -> X -> B` | README + development plan + changelog |
| do B first this turn | focus only | session plan |
| pause/drop/replace a node | explicit mutation | README + development plan + changelog |
| switch current Feature | project pointer mutation | OVERVIEW + old/new owners + changelog |

The letters above are abstract machine notation, not user-facing labels. Use stable, unique node IDs
internally and give every node a semantic `name` taken from the owning module or milestone. A name may
change; a retired ID must not be reassigned.

## README manifest

Place one hidden JSON block in every active Feature README:

```markdown
<!-- MAINLINE-ROUTE:START
{
  "schema_version": 2,
  "route_version": "YYYY-MM-DD.N",
  "summary": "合同冻结已完成 → [观测工程进行中 ∥ 模拟器工程已准备] → 集成验证 → 模型训练未授权",
  "nodes": [
    {"id": "a", "name": "合同冻结", "progress": "passed", "authorization": "completed-scope", "owner": "README.md"},
    {"id": "b", "name": "观测工程", "progress": "active", "authorization": "authorized", "owner": "b-goal.md"},
    {"id": "c", "name": "模拟器工程", "progress": "prepared", "authorization": "authorized", "owner": "c-goal.md"},
    {"id": "join", "name": "集成验证", "progress": "planned", "authorization": "authorized", "owner": "development-plan.md"},
    {"id": "d", "name": "模型训练", "progress": "planned", "authorization": "unauthorized", "owner": "development-plan.md"}
  ],
  "edges": [["a", "b"], ["a", "c"], ["b", "join"], ["c", "join"], ["join", "d"]],
  "focus_nodes": ["b", "c"],
  "parallel_groups": [["b", "c"]],
  "joins": [{"id": "join", "requires": ["b", "c"]}],
  "next_gate": "join"
}
MAINLINE-ROUTE:END -->
```

Immediately below it, render the exact `summary` in one visible route line, followed by at most:
current focus, blocker, next gate, authorization boundary, and links to child owners.
Every user-visible field must use semantic module/milestone names. Keep raw node IDs, phase codes,
and shorthand such as `M0`, `M3C`, or `A/BC` inside the manifest or implementation docs unless the
user explicitly asks for them.

When a node owner is a child `*-goal.md`, keep one hidden roll-up state in that GOAL:

```markdown
<!-- ROUTE-NODE:START
{"id":"b","progress":"active","authorization":"authorized"}
ROUTE-NODE:END -->
```

The child GOAL remains the detailed owner. The parent README carries only the same node ID, progress,
and authorization as a macro roll-up; update both in one change whenever any of those three values moves.

## Output levels

- **L0 — default**: goal, route, current focus, blocker, next gate, authorization, all expressed with semantic module/milestone names. No implementation inventory or internal IDs.
- **L1 — expand one workstream**: local STEP, dependency, completion condition, blocker and next action.
- **L2 — implementation/evidence**: files, interfaces, tests, commands and artifacts only when requested or necessary.

When a user asks for progress without specifying depth, always return L0. When route interpretation is
unambiguous, state the normalized route briefly and proceed. Ask only if an alternative interpretation
would change dependency, contract, evidence meaning or authorization.

## Validation expectations

Validate one manifest per active owner, unique node IDs, non-empty semantic node names, existing owner paths, valid edge endpoints,
an acyclic graph, valid focus/parallel/join references, explicit join edges, one next gate matching
README metadata, an identical visible summary, child-GOAL roll-up consistency, and no copied
manifest/summary in upper routing docs.
