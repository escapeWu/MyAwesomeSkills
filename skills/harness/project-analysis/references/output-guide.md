# Project Analysis Output Guide

Choose the smallest output that answers the request.

## Conversation Answer

Use for one-off investigation, debugging, review, and questions that do not need a durable repository artifact.

Recommended shape:

```text
Conclusion
Evidence
Flow or ownership
Risks / unknowns
Next action or validation
```

Keep facts, inferences, and unknowns distinct. Cite useful file paths, symbols, commands, or artifacts.

## Existing Docs Update

Use only when a stable conclusion will remain useful after the current task. For implementation work, patch docs after
implementation and validation are complete, in the same final docs pass as other durable changes.

Placement:

| Knowledge | Owner |
|---|---|
| Feature purpose, behavior, constraints, current design, or concise state | owning Feature README |
| Stable cross-Feature architecture or interface | related `docs/reference/*.md` |
| Stable project-wide run/validation procedure | runbook/reference |
| New or changed navigation | nearest INDEX and, only if needed, OVERVIEW |
| Temporary hypothesis, gap list, or command output | conversation/tool artifact, not long-term docs |

Update the smallest existing owner. Preserve accurate content and avoid duplicating the same conclusion at several levels.

## New Reference

Create a new document only when:

- the knowledge is stable and substantial;
- no current owner can hold it cleanly;
- future tasks are likely to search for it;
- its parent route will make it discoverable.

Typical names include `architecture.md`, `dataflow-<topic>.md`, or `interfaces-<topic>.md`. Names are examples, not a
required taxonomy.

## Diagrams

Use a diagram when it clarifies a real relationship. Choose one representation that fits the audience. Do not produce
both Mermaid and ASCII unless both are independently useful or the user asks.

A diagram should identify real components and flows, avoid decorative complexity, and agree with the written conclusion.

## Completion Check

- The output answers the requested question directly.
- Important conclusions have evidence.
- The result does not overstate uncertain behavior.
- Any docs change happened once after the task was resolved.
- Navigation was updated only when a new path was introduced.
- No session plan, raw output, or temporary analysis became repository documentation.
