---
name: mcp-build-best-practice
description: Design, build, audit, refactor, or productionize Model Context Protocol servers with evidence-backed contracts, safe tools, appropriate resources and prompts, progressive-disclosure workflow guides, authorization, explicit long-running task lifecycles, protocol-level tests, and live deployment verification. Use for greenfield MCP servers, adding or reorganizing tool families, reviewing schemas and response contracts, introducing OAuth or remote HTTP transport, exposing guide indexes/get_*_use resources, fixing agent usability or safety problems, or deciding whether an MCP integration is ready to ship.
---

# MCP Build Best Practice

Build an MCP server that an unfamiliar agent can discover, invoke safely, recover, and verify. Optimize for correct decisions and stable contracts, not maximum tool count.

## Required outcome

Produce evidence for all applicable layers:

1. A narrow domain and ownership boundary.
2. Appropriate MCP primitives and capability negotiation.
3. Small, strict, accurately annotated tool contracts.
4. Stable structured results, errors, pagination, and lifecycle state.
5. Authorization and mutation controls proportional to risk.
6. Progressive-disclosure guides for nontrivial cross-tool workflows.
7. Registry, protocol, security, forward-agent, and deployed-endpoint tests.

Do not require every server to expose Tools, Resources, and Prompts. Implement only primitives that have a clear control owner and use case.

## Workflow

### 1. Establish current evidence

Inspect the latest official MCP specification, the installed SDK version, target client behavior, repository code, tool registry, tests, transport, authentication, and deployment process.

Record claims in an evidence table:

| Claim | Code/spec/test evidence | Resulting contract |
| --- | --- | --- |
| A timeout stops work | Process implementation and test | State exact termination behavior |
| A path scopes mutation | Staging/write implementation | State what remains in scope |
| A resource is discoverable | Real client `resources/list` | Advertise the resource path |

Do not rely on remembered protocol revisions or SDK examples. Do not document behavior the implementation merely intends to provide.

### 2. Bound the server and choose primitives

Define the server's domain, data authority, users, trust boundary, and external side effects. Split unrelated administrative or high-risk capabilities when they need different credentials, operators, or blast radii.

Use:

- **Tools** for model-selected retrieval or actions.
- **Resources** for client-managed context and durable read surfaces.
- **Prompts** for user-selected templates or workflows.
- **Tasks or explicit handles** when work must outlive one request.

Read [references/architecture-contracts.md](references/architecture-contracts.md) before deciding primitives, transport, tool boundaries, schemas, responses, errors, or pagination.

### 3. Design contracts before handlers

For every tool, specify:

- Stable unique name and one clear responsibility.
- Exact input schema with types, enums, bounds, and mutually exclusive fields.
- Output schema or stable structured envelope.
- Read-only, mutating, destructive, idempotent, and open-world behavior.
- Preconditions, partial-success semantics, pagination, and size budgets.
- Error codes, retryability, recovery action, and residual side effects.
- Authorization scope and audit fields.

Keep per-call parameter facts in tool schemas. Keep cross-call selection, ordering, monitoring, and recovery rules in workflow guides.

Annotations are hints for planning and user experience, not an authorization mechanism. Make descriptions match actual behavior, including negative facts such as “accepted” not proving completion.

### 4. Engineer safety and lifecycle

Read [references/security-lifecycle.md](references/security-lifecycle.md) before implementing remote access, sensitive data, filesystem/shell operations, destructive actions, sessions, jobs, delegates, or long-running work.

At minimum:

- Validate identity, audience, scope, tenant, target, and input before side effects.
- Separate preview from commit when mistakes are costly.
- Prefer exact targets, revision checks, narrow permissions, and recoverable operations.
- Bound time, output, memory, concurrency, queues, and retained state.
- Mint explicit opaque handles for state that crosses calls.
- Distinguish request wait time from process lifetime.
- Distinguish cancellation from rollback and verify the terminal state.
- Redact secrets and bind task/result access to the authorization context.

### 5. Add progressive discovery when schemas are insufficient

If agents must choose among related tools or preserve cross-call safety/lifecycle rules, read [references/progressive-discovery.md](references/progressive-discovery.md) and implement workflow-sized guides.

Use one authoritative registry to generate:

- `get_skill_index` plus a JSON index resource.
- One read-only `get_<workflow>_use` tool per guide.
- One stable Markdown resource URI per guide.
- Server instructions and capability metadata that advertise discovery.

Do not create one guide per tool. Do not maintain separate handwritten tool, resource, filesystem-skill, and README bodies.

### 6. Implement behind stable boundaries

Separate protocol registration from domain services, upstream clients, persistence, authorization, and process supervision. Make policy visible at one layer rather than scattering it across handlers.

Preserve compatibility unless a migration is intentional:

- Keep names, schemas, resource URIs, and error codes stable.
- Add fields compatibly; version material routing or lifecycle changes.
- Translate provider-specific behavior behind adapters.
- Keep transport details from changing domain semantics.
- Use server-owned state only when the lifecycle and cleanup policy are explicit.

### 7. Validate through the protocol

Read [references/validation-release.md](references/validation-release.md) before declaring completion.

Run the smallest sufficient matrix, including:

1. Domain and pure-contract tests.
2. Schema, annotation, registry, and resource identity tests.
3. Real MCP initialize/list/call/read tests over each supported transport.
4. Authorization, tenant isolation, injection, limits, timeout, cancel, and cleanup tests.
5. Fresh-agent scenarios without hidden implementation context.
6. Reloaded local and public endpoint verification.

Direct function calls do not replace MCP protocol tests. A passing unit suite does not prove that a long-running deployed server reloaded the new registry.

### 8. Report readiness honestly

Report:

- Implemented primitives, tools, resources, guides, and transports.
- Safety and lifecycle guarantees with their evidence.
- Validation commands and protocol scenarios executed.
- Authentication and deployment status without secrets.
- Compatibility decisions, unsupported paths, and known residual risks.

Do not call a server production-ready while protocol, authorization, forward-agent, or live deployment evidence is missing.

## Decision gates

Stop and resolve the design when any answer is unclear:

- Who controls this primitive: user, client, or model?
- Can a repeated call duplicate or destroy state?
- Can an output exceed the response or context budget?
- Does timeout terminate work, or only stop waiting?
- Can one caller retrieve another caller's task or resource?
- What proves a mutating call completed correctly?
- Can a fresh agent discover the required operating guide?
- Has the exact deployed transport been exercised by a real client?

## Hard requirements

- Treat workspace roots, friendly path resolution, and annotations as non-security boundaries unless enforcement proves otherwise.
- Never promise atomicity, rollback, idempotency, persistence, isolation, or cancellation beyond implementation and tests.
- Never place credentials in source, tool output, URLs, prompts, or diagnostic logs.
- Never expose unbounded collection, output, process, or queue behavior.
- Never hide destructive behavior behind a generic tool name or optimistic success message.
- Never substitute README prose for protocol-visible discovery.
- Never make direct SDK calls the only integration evidence.

## Completion checklist

- [ ] Domain, users, data authority, and trust boundary are explicit.
- [ ] Primitive and transport choices match their control model.
- [ ] Tool schemas, annotations, results, errors, and pagination are stable.
- [ ] Auth, scopes, target validation, secrets, and destructive actions are tested.
- [ ] Long-running work has status, output, cancellation, cleanup, and ownership semantics.
- [ ] Complex workflows have discoverable single-source guides.
- [ ] Registry and real MCP protocol tests pass.
- [ ] Fresh-agent forward tests pass without leaked context.
- [ ] The actual local/remote service was reloaded and verified.
- [ ] Release evidence and residual risks are reported.

## References

- Read [references/architecture-contracts.md](references/architecture-contracts.md) for primitive selection, tool design, response envelopes, errors, pagination, transports, and boundaries.
- Read [references/security-lifecycle.md](references/security-lifecycle.md) for authorization, mutation safety, long-running tasks, concurrency, retention, and secret handling.
- Read [references/progressive-discovery.md](references/progressive-discovery.md) for the integrated guide-index, dual-exposure, single-source, and agent-discovery pattern.
- Read [references/validation-release.md](references/validation-release.md) for contract, protocol, security, forward-agent, compatibility, deployment, and release gates.
