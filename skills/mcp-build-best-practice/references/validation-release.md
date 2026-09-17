# Validation and Release

## Contents

1. Evidence matrix
2. Contract and registry tests
3. Protocol tests
4. Security and lifecycle tests
5. Forward-agent tests
6. Compatibility and deployment tests
7. Release evidence
8. Readiness gate

## Evidence matrix

Plan tests by claim rather than by module:

| Claim | Minimum evidence |
| --- | --- |
| Tool schema rejects invalid combinations | Schema/handler test plus protocol call |
| Read-only annotation is exposed | Registry and `tools/list` assertion |
| Cursor resumes without gaps | Multi-page integration test |
| Wait expiry leaves work running | Clock/process lifecycle test |
| Cancel reaches terminal state | Race-aware cancellation test |
| Guide tool and resource share content | Identity/hash assertion through MCP |
| OAuth protects the transport | Unauthorized and scoped authorized requests |
| Release is live | Real client against reloaded endpoint |

Test boundaries most likely to cause data loss, cross-tenant exposure, false completion, or irrecoverable context loss.

## Contract and registry tests

Test pure domain behavior independently of the SDK. Then inspect the actual server registry:

- Unique stable tool names.
- Input/output schemas and defaults.
- Annotations and execution/task declarations.
- Resource and prompt names, URIs, MIME types, and templates.
- Server instructions and advertised capabilities.
- Deterministic guide index and exact required-tool coverage.

Use targeted contract assertions instead of snapshotting every description word. Snapshot only when public serialization itself is the contract.

## Protocol tests

Initialize a real MCP client session over every supported transport. Exercise:

```text
initialize / capability negotiation
tools/list
tools/call for representative success and every error class
resources/list and resources/read when supported
prompts/list and prompts/get when supported
task/status/result/cancel operations when supported
notifications or other negotiated capabilities when applicable
```

Assert serialized structured content, tool errors, MIME types, pagination, and capability fields. Direct Python/TypeScript function calls do not test registration, JSON-RPC serialization, middleware, or client compatibility.

For stdio, verify stdout contains protocol traffic only. For Streamable HTTP, verify session handling, content types, reconnect behavior required by the current specification, and middleware ordering.

## Security and lifecycle tests

Cover:

- Missing, invalid, expired, wrong-audience, and insufficient-scope credentials.
- Cross-tenant object, task, resource, and cancellation attempts.
- Token/resource metadata discovery and canonical public URL.
- Path traversal, command injection, SSRF, unsafe redirects, and oversized/nested input.
- Rate, concurrency, queue, memory/output, and execution-time limits.
- Idempotency keys, duplicate requests, revision conflicts, and partial mutation.
- Timeout, disconnect, cancellation races, process-tree cleanup, and server restart.
- TTL expiry and durable-state reconciliation.
- Secret redaction in errors, logs, metadata, prompts, and artifacts.

Use real upstream sandboxes or faithful fakes for externally consequential actions. Never point destructive evaluation cases at production data without explicit authority and recovery controls.

## Forward-agent tests

Give a fresh agent the MCP connection or packaged Skill plus a realistic request. Do not provide expected steps, suspected bugs, intended fixes, or hidden implementation context.

Scenarios should combine boundaries:

- A large paginated search followed by revision-protected mutation.
- A short command, a durable background job, and an interactive session.
- Existing staged changes plus a narrowly scoped commit request.
- A task whose client wait ends before execution finishes.
- An unauthorized or wrong-tenant handle.
- A client that exposes tools but not resources.

Evaluate whether the agent:

- Discovers the relevant capabilities and guide.
- Chooses the correct primitive and lifecycle.
- Advances every cursor correctly.
- Avoids destructive shortcuts and overbroad targets.
- Interprets timeout, acceptance, cancellation, and partial success correctly.
- Verifies results independently.
- Identifies unknown behavior instead of inventing guarantees.

Fix the guide or implementation when the agent fails. Do not leak the desired solution into the next prompt.

## Compatibility and deployment tests

Before release:

- Compare tool/resource/prompt schemas with the previous version.
- Classify changes as additive, behavior-changing, or breaking.
- Preserve old fields/routes or provide an explicit migration and version policy.
- Test representative target clients and gateways, not only the SDK inspector.
- Verify local stdio/HTTP and public HTTPS paths separately when both exist.
- Verify OAuth/protected-resource metadata uses the canonical endpoint.
- Reload or restart the actual long-running service.
- Repeat initialize/list/call/read against the reloaded process.

Registry code committed to disk is not live evidence. A reverse proxy health page is not an MCP protocol test.

## Release evidence

Record only non-secret evidence:

- Commit/build/version identifier.
- Endpoint label and transport, not tokens.
- Negotiated protocol revision.
- Tool, resource, prompt, and guide counts.
- Stable names/URIs and representative schema/content hashes.
- Test commands and summarized results.
- Service reload/status evidence.
- Known unsupported clients, lifecycle gaps, and residual risks.

Do not print `.env`, authorization headers, token stores, complete process logs, or customer content to prove connectivity.

## Readiness gate

A reasonable MCP server is ready only when:

- The domain and trust boundary are understandable.
- Agents can discover and correctly select capabilities.
- Inputs, outputs, errors, and pagination are machine-actionable.
- Authorization and mutation controls are enforced, not merely described.
- Long-running state has explicit ownership and cleanup.
- Real protocol and fresh-agent tests cover critical workflows.
- The deployed endpoint was exercised after reload.
- Operators know what remains after failure, timeout, cancellation, and upgrade.

If one layer is intentionally absent, state why it is unnecessary for this server rather than silently treating it as complete.
