# Security and Lifecycle

## Contents

1. Threat model
2. Authentication and authorization
3. Input and target safety
4. Mutation and destructive actions
5. Long-running work
6. Concurrency, ownership, and retention
7. Secrets and observability
8. Failure questions

## Threat model

Treat tool names, descriptions, model-generated arguments, resource content, upstream responses, and filesystem data as potentially untrusted. Identify risks from:

- Prompt or content injection.
- Cross-tenant object references.
- Token theft, confused deputy behavior, or token passthrough.
- Path traversal, command injection, SSRF, unsafe deserialization, and archive extraction.
- Excessive output, process creation, queues, recursion, or retained state.
- Destructive retries and cancellation races.
- Task/result identifiers leaked across principals.

Map each risk to an enforced control and a test. Documentation is not a control.

## Authentication and authorization

For local stdio servers, retrieve credentials through the environment or an OS credential mechanism and document the local trust assumption. Do not implement the remote HTTP OAuth flow on stdio merely for symmetry.

For protected HTTP servers, follow the current MCP authorization specification. At minimum:

- Serve production endpoints over HTTPS.
- Publish Protected Resource Metadata and supported authorization-server discovery.
- Validate token signature, issuer, expiry, audience/resource, and scopes.
- Require authorization on every protected request, including requests in one logical session.
- Never accept tokens minted for another resource.
- Never pass the MCP client's bearer token through to an upstream service.
- Use separate upstream credentials or an explicit delegated authorization flow.
- Prefer narrow and incremental scopes over a catch-all scope.

Return 401 for missing/invalid authentication and 403 for insufficient permission when the transport/specification requires those semantics. Redact authentication headers and tokens before logging.

## Input and target safety

Validate before side effects:

- Principal and tenant.
- Exact object, repository, file, process, or remote account.
- Path normalization and allowed roots when a real sandbox is intended.
- URL scheme, hostname/IP class, redirects, and egress policy.
- Command arguments without unsafe shell interpolation.
- Input length, nesting, count, ranges, encoding, and content type.
- Revision, ETag, generation, or other compare-and-swap token.

A workspace root used to resolve relative paths is not automatically a confinement boundary. Enforce containment explicitly if the contract claims it.

## Mutation and destructive actions

Classify actions:

| Class | Examples | Required controls |
| --- | --- | --- |
| Read-only | Search, inspect, status | Bounds, authorization, privacy filters |
| Mutating | Create, update, start | Exact target, idempotency/revision policy, verification |
| Destructive | Delete, force remove, overwrite | Explicit authority, preview where practical, recovery statement |
| Externally consequential | Send message, publish, charge | Recipient/account confirmation, deduplication, audit |

Provide dry-run or a plan when the cost of a wrong target is high. Make the preview contain the identifiers and revision needed to protect the real mutation. Do not claim dry-run safety if planning itself creates remote state.

Prefer recoverable operations. If force mode can lose data, require exact target resolution and explicit approval that describes the loss. Cancellation or a failed response does not undo already completed side effects.

Define retry behavior:

- Idempotent: the same request key produces no additional effect.
- Deduplicated: repeated submission returns the existing operation.
- Non-idempotent: retries may duplicate effects and require user/operator judgment.

## Long-running work

Choose a lifecycle explicitly:

| Work | Pattern |
| --- | --- |
| Short, bounded, noninteractive | One synchronous tool call |
| Durable noninteractive work | Task/job handle with status and output |
| Interactive TTY | Session handle with capture and input |
| Scheduled or delegated work | Queue/task handle with dependency and cancellation policy |

For any handle, define:

- Cryptographically unguessable ID.
- Principal/tenant ownership.
- States and legal transitions.
- Created/updated/expiry timestamps.
- Status and result retrieval.
- Output cursor, MIME/encoding, and maximum chunk.
- Request wait timeout versus execution timeout.
- Cancellation semantics and race handling.
- Retention, cleanup, and restart recovery.

Start acceptance proves only that work was accepted. It does not prove execution or completion. An expired client wait window does not prove that the process stopped. Accepted terminal input proves transport acceptance, not that the application consumed it. A terminal snapshot is not automatically a lossless stdout/stderr log.

After cancellation, verify the documented terminal state. State whether partial output and side effects remain. Never call cancellation rollback unless compensating operations are implemented and tested.

## Concurrency, ownership, and retention

Bound:

- Per-principal and global concurrency.
- Queue size and fairness.
- Process tree and child cleanup.
- CPU, memory, wall time, open files, and output bytes.
- Task/resource TTL and retained log storage.

Serialize writers when shared state cannot support safe concurrency. Prevent later readers from starving a queued writer when consistency depends on fairness. Use project/tenant/resource identity, not only caller-provided paths, as the scheduling key.

Task IDs are capabilities. Bind retrieval, listing, cancellation, and output access to the same authorization context. If the server cannot identify requestors, use high-entropy IDs, short retention, and avoid global task listing that exposes other users' metadata.

## Secrets and observability

Keep secrets out of:

- Repository files and generated artifacts.
- Tool arguments when a credential provider can be used.
- URLs and query strings.
- Tool output and structured errors.
- Prompts, guide content, transcripts, and complete environment dumps.
- Request, subprocess, and upstream logs.

Record non-secret audit evidence: request ID, principal/tenant ID or safe hash, tool, target class, decision, duration, result code, task ID, and side-effect status. Separate application observability from protocol-visible messages and follow the current specification before exposing protocol logging capabilities.

## Failure questions

Before shipping, answer:

- What remains after timeout, cancellation, or client disconnect?
- Can a retry duplicate an external action?
- Can a caller enumerate or guess another caller's state?
- Does a failed batch leave partial writes, and is rollback status observable?
- Can queued work survive a server restart, and should it?
- When are task output and audit logs deleted?
- Which limits apply before expensive upstream work starts?
- Which operator evidence exists without revealing secrets?
