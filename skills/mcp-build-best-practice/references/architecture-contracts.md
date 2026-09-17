# Architecture and Contracts

## Contents

1. Evidence-first design
2. Domain and trust boundaries
3. Primitive selection
4. Tool contract design
5. Response and error contracts
6. Pagination and budgets
7. Transport and implementation boundaries
8. Anti-patterns

## Evidence-first design

Before changing a server, inspect:

- The current official MCP specification and negotiated protocol revision.
- The installed SDK APIs rather than examples for another version.
- Registered names, schemas, annotations, resources, prompts, and server instructions.
- Domain implementations behind handlers, including failure and partial-mutation paths.
- Target clients and gateways: which protocol surfaces they actually expose.
- Tests, transport, authorization, public routing, and reload mechanics.

Use the specification to establish protocol facts and code/tests to establish server facts. If they disagree, fix the implementation or describe the current limitation; do not average them into ambiguous prose.

Official starting points:

- `https://modelcontextprotocol.io/specification/`
- `https://modelcontextprotocol.io/docs/`
- The official SDK repository for the language and version in use.

## Domain and trust boundaries

Define:

- **Domain**: the cohesive system or workflow this server owns.
- **Authority**: which upstream data and actions it is allowed to access.
- **Principal**: the user, tenant, service account, or local operator represented by a call.
- **Blast radius**: the maximum data or state one mistaken call can affect.
- **Trust boundary**: where identity, authorization, validation, and escaping must occur.

Split a server when tool families require materially different credentials, operators, exposure, retention, or risk. A single server may expose many related tools; it should not become an accidental universal control plane.

## Primitive selection

| Need | Primitive | Controller | Notes |
| --- | --- | --- | --- |
| Retrieve or mutate on model choice | Tool | Model | Validate and authorize every invocation. |
| Supply browsable context | Resource | Client/application | Use stable URI and MIME type. |
| Offer a user-selected template | Prompt | User | Do not use as hidden mandatory policy. |
| Work outlives one request | Task or explicit handle | Requestor + server | Define ownership, TTL, status, result, and cancellation. |
| Cross-tool operating knowledge | Guide tool + resource | Agent/client | Use progressive discovery and one content source. |

Do not expose a resource as a mutating back door. Do not turn every read into a Resource when the model needs parameterized search. Do not require Prompts merely to claim feature completeness.

## Tool contract design

Prefer cohesive operations over thin endpoint mirrors and over giant “do anything” tools. Split when operations differ in authorization, destructiveness, lifecycle, or output shape. Combine only when the agent otherwise must reproduce a fragile transaction without gaining control.

For each tool define:

- A unique stable name using characters supported by the current specification.
- One-sentence action, exact side effects, and important negative guarantees.
- JSON Schema types, required fields, bounds, enums, formats, and descriptions.
- `oneOf`/equivalent constraints for mutually exclusive shapes when supported.
- Defaults that are safe, bounded, and visible in the schema.
- Stable output fields and machine-actionable status.
- Read-only, destructive, idempotent, and open-world annotations where supported.
- Required authorization scope and audit identity.

Annotations are untrusted hints outside a trusted server relationship. Enforce permissions in code.

Avoid boolean piles such as `force`, `delete`, `recursive`, and `overwrite` whose combinations create hidden modes. Prefer explicit operation names or tagged input variants.

## Response and error contracts

Use a consistent envelope when the SDK does not already impose one:

```json
{
  "success": true,
  "data": {},
  "pagination": {
    "complete": true,
    "next_cursor": null
  },
  "warnings": [],
  "request_id": "req_opaque"
}
```

For failures, make recovery machine-readable:

```json
{
  "success": false,
  "error": {
    "code": "revision_conflict",
    "message": "The target changed after it was read.",
    "retryable": true,
    "recovery": "Read the target again and retry with the new revision."
  },
  "side_effects": {
    "occurred": false
  }
}
```

Use protocol-level errors for malformed/unsupported protocol requests. Represent domain/tool execution failures using the SDK's tool-error mechanism and stable structured content. Do not leak stack traces, queries, credentials, internal paths, or upstream response bodies by default.

Differentiate:

- Invalid arguments.
- Authentication failure.
- Authorization failure.
- Missing or conflicting state.
- Rate/queue/size limits.
- Retryable upstream failure.
- Timeout, cancellation, and partial completion.
- Internal failure with a request ID for operators.

## Pagination and budgets

All open-ended collections and large content need bounds. Prefer opaque cursors when the upstream source can change; use offsets only when ordering and continuation semantics remain valid.

Return:

- Items actually returned.
- `complete` or equivalent.
- Opaque `next_cursor` when more data exists.
- Limit/budget applied.
- Truncation or partial-result reason.

Never infer the next cursor from visible item count unless the contract defines that rule. Keep stdout/stderr, pages, byte streams, or partitions on separate cursors when their ordering cannot be merged correctly.

Bound both upstream work and MCP response size. A tool that fetches everything and truncates only after serialization still has an availability problem.

## Transport and implementation boundaries

Use stdio for local subprocess integrations when process ownership and environment credentials are acceptable. Use Streamable HTTP for remote/multi-client deployments. Follow the current official transport and authorization specification; do not revive deprecated transport patterns from old examples.

For stdio, reserve stdout for protocol messages and send diagnostics to stderr. For HTTP, validate origins/hosts where applicable, use HTTPS outside localhost, bound request bodies, and put authentication before transport session creation.

Separate:

```text
protocol registration
    → policy/authorization
        → domain service
            → upstream adapter or state store
```

This keeps SDK churn, business rules, credentials, and transport concerns independently testable.

## Anti-patterns

- One generic `execute` tool with an undocumented mini-language.
- One tool per upstream HTTP endpoint without agent-oriented workflows.
- Descriptions that promise behavior not enforced by code.
- Natural-language-only results that cannot be classified reliably.
- Returning unlimited rows, logs, binary data, or directory trees.
- Marking a tool read-only while it updates caches, sessions, or remote state materially.
- Treating annotations, workspace roots, or friendly path resolution as a sandbox.
- Adding Resources or Prompts only to make the capability list look complete.
