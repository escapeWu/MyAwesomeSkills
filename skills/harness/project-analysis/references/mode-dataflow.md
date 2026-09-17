# Data Flow And Sequence Analysis Guide

Use this guide for a concrete request, event, job, or data path whose transformations, state, I/O, branches, or failure
behavior need to be understood.

## Start At A Real Entry

Identify the API endpoint, command, event handler, scheduler, UI action, or other trigger. Define the endpoint of the trace
so the investigation does not expand indefinitely.

Read the applicable root rules and, when useful, the owning Feature README or one reference. Verify behavior in targeted
code, tests, configuration, logs, or artifacts.

## Trace The Flow

Follow the path in execution order and record only meaningful transitions:

- input and validation;
- important transformations;
- state reads and writes;
- database, cache, queue, file, or third-party I/O;
- output, emitted events, and observable errors;
- branches relevant to the question.

Keep file paths and symbols for key steps. Distinguish confirmed flow from inferred or unobserved behavior.

## Scale The Investigation

Use local search for short flows. For a broad path, optional independent read-only subtasks may cover the entry, core call
chain, and external I/O/exception paths. Do not split into a fixed number of subtasks when one pass is clearer.

## Present The Result

Answer the requested question first. Then use the smallest useful representation:

- ordered call chain;
- input/transform/output table;
- sequence diagram;
- data-flow diagram;
- concise risk list.

Mermaid and ASCII are alternatives, not a mandatory pair. Do not produce both a sequence and data-flow diagram unless
both clarify different aspects of the problem.

## Durable Docs

One-off traces and debugging hypotheses stay in the conversation. If implementation follows, wait for implementation and
validation to complete. The main Agent then passes durable flow changes to the single asynchronous docs SubAgent, which
updates the owning Feature README or stable reference once.
