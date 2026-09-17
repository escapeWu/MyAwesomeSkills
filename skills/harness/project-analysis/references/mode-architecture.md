# Architecture Analysis Guide

Use this guide when the question needs a system or module-level view of boundaries, dependencies, external services, or
risk. Do not use it for a small symbol lookup.

## Focus The Question

State the scope and the decision the analysis should support. Useful questions include:

- Where does this behavior enter the system?
- Which module owns it?
- What dependencies or external services matter?
- Which boundary is causing the bug, risk, or proposed change?

## Read The Minimum Context

Start with the applicable root rules, then use an overview or owning Feature README only when it helps locate code. Open
one relevant architecture/reference document if available. Verify conclusions against targeted code and configuration.

Do not read every module or document to produce a generic architecture inventory.

## Collect Evidence

For a focused module, local search is usually enough. For a genuinely broad system, independent read-only subtasks may
cover entrypoints, module ownership, and external dependencies. Parallelism is optional; use it only when it reduces time
or context cost.

Useful evidence includes:

- runtime and main entrypoints;
- modules participating in the target behavior;
- allowed and actual dependency direction;
- persistent state and external I/O;
- concrete risk or uncertainty.

## Synthesize

Lead with the answer, then show the smallest architecture slice that supports it. A table, short prose flow, Mermaid
diagram, or ASCII diagram may be used. Choose one representation unless another is independently useful.

Avoid producing a whole-system diagram when the user needs one call path or ownership decision.

## Durable Docs

For analysis-only requests, return the result in conversation unless the user asked for a document. When analysis supports
implementation, wait until the implementation and validation finish. The main Agent then includes durable architecture
findings in the single asynchronous docs handoff; the docs SubAgent patches the owning Feature README or reference once.
