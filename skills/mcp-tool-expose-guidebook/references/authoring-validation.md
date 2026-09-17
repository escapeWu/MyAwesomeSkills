# Authoring and Validation

## Contents

1. Evidence audit
2. Guide template
3. Boundary tests
4. Validation layers
5. Forward testing
6. Live verification
7. Field lessons

## Evidence audit

Before writing prose, inspect:

- Tool registration names, descriptions, schemas, defaults, annotations, and return types.
- The implementation behind every lifecycle or safety claim.
- Tests for edge cases, failures, pagination, rollback, concurrency, and process termination.
- Client behavior for tools, resources, prompts, and structured content.
- Deployment configuration, authentication, canonical public URL, and reload process.

Build a small evidence table:

| Claim | Code/test evidence | Guide wording |
| --- | --- | --- |
| Wait expiry leaves process running | scheduler/process tests | “Wait window is not process lifetime.” |
| Output cursor is per stream | output implementation | “Do not infer stdout/stderr ordering.” |
| Force removal discards dirty worktree | worktree implementation/tests | “Require explicit loss approval.” |

If evidence is missing, weaken the claim or improve the tool. Never fill the gap with confident prose.

## Guide template

Use this structure when the workflow needs it:

```markdown
---
name: example-use
description: What the workflow covers and the concrete situations that require loading it.
---

# Example Use

## Critical rules

1. State the strongest safety boundary.
2. State the lifecycle/pagination boundary most often misunderstood.
3. Require independent verification after mutation.

## Choose the tool

| Need | Tool |
| --- | --- |
| One call pattern | `tool_a` |
| Another lifecycle | `tool_b` |

## Operate safely

- Give the cross-tool sequence.
- State what success fields do and do not prove.
- State continuation, timeout, concurrency, and rollback behavior.

## Recover from failures

| Error/status | Response |
| --- | --- |
| `specific_error` | Concrete recovery action. |

## Minimal examples

```json
{"argument":"value"}
```
```

Keep parameter encyclopedias in tool schemas. Put only non-obvious cross-call rules in the guide.

## Boundary tests

Test the claims most likely to cause data loss or false completion:

- A partial response advances using the documented cursor.
- A timeout does or does not terminate the underlying process as stated.
- Dry-run returns enough revision data for a later protected write.
- A scoped commit cannot silently include unrelated staged entries—or the guide blocks it.
- Accepted terminal input still requires capture/status verification.
- A destructive force option requires explicit authority and exact target resolution.
- Failure after partial mutation reports rollback state accurately.

## Validation layers

### 1. Pure data tests

Assert the index is deterministic, versioned, and complete. Verify each registered tool belongs to the intended guide or is intentionally schema-only.

### 2. Content-contract tests

Assert critical safety phrases and recovery semantics remain present. Avoid snapshotting every word; test durable contracts.

### 3. Registry tests

List tools/resources directly from the server registry. Assert names, URIs, MIME types, read-only annotations, and identical authoritative content.

### 4. MCP protocol tests

Initialize a real client session over the supported transport. Execute:

```text
list_tools
call_tool(get_skill_index)
call_tool(each get_*_use)
list_resources
read_resource(index)
read_resource(each guide)
```

Do not replace this with direct Python function calls; protocol serialization and client compatibility are part of the feature.

### 5. Deployment tests

Reload the actual service, then repeat the protocol test against local and public endpoints. Verify OAuth/protected-resource metadata still advertises the canonical public URL.

## Forward testing

Give a fresh agent the Skill/guide plus a realistic user task. Do not provide expected steps or suspected bugs.

Use scenarios that combine boundaries:

- Unknown file encoding plus concurrent mutation and compare-and-swap replacement.
- A short check, a multi-hour background job, and an interactive debugger.
- Existing staged/unstaged changes, a path-scoped commit request, and a dirty worktree removal request.
- A delegated task whose MCP wait ends before its subprocess finishes.

Review whether the agent:

- Selects the right lifecycle/tool family.
- Follows every continuation cursor.
- Refuses unsafe destructive shortcuts.
- Reads status/logs and verifies results.
- Identifies ambiguity rather than inventing behavior.

Convert discovered ambiguities into clearer guide rules or implementation fixes, then forward-test again.

## Live verification

Record only non-secret evidence:

- Endpoint label, not bearer tokens.
- Guide count, total tool count, and resource count.
- Names/URIs present.
- Tool/resource content headings or hashes.
- Service status and canonical OAuth issuer/resource.

Never print `.env`, authorization headers, token-store contents, or complete audit logs merely to prove connectivity.

## Field lessons

### Workflow guides outperform tool-by-tool guides

Agents need help deciding among related lifecycle models, not repeated schema text. File, process, Git, and delegation are useful boundaries; every read/list/status tool rarely needs a standalone guide.

### Dual exposure is pragmatic

MCP resources are the correct content abstraction, but some gateways surface tools more reliably. Expose both while keeping one source.

### Forward tests find documentation fiction

Real examples frequently reveal that:

- A normal read response may not expose the revision required by a protected mutation; a dry-run may be the actual revision source.
- A commit API with `paths` may still include entries that were already staged before the call.
- Separate stdout/stderr cursors prevent reliable merged ordering.
- “Accepted” terminal input proves transport acceptance, not application consumption.

Write these negative facts explicitly. They prevent more failures than another happy-path example.

### Deployment is part of the feature

A correct registry change is invisible until the long-running service reloads. Test the same client flow users will execute, including authentication metadata and public routing.
