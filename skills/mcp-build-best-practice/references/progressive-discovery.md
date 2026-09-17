# Progressive Discovery

## Contents

1. When guides are justified
2. Workflow boundaries
3. Index contract
4. Single-source registry
5. Dual exposure
6. Guide contents
7. Discovery and compatibility
8. Validation and anti-patterns

## When guides are justified

A tool schema should explain one call. Add a workflow guide when an agent must know how to choose, order, monitor, continue, verify, or recover across multiple calls.

Good guide boundaries include:

- File discovery, reading, revision-protected mutation, and verification.
- Repository inspection, staging, commits, history, and worktrees.
- Synchronous commands, durable jobs, and interactive sessions.
- Delegated execution, scheduling, output, and cancellation.

Do not create a guide for every simple read/list/status tool. Do not load one giant server manual before every call.

## Workflow boundaries

Audit real tool schemas, handlers, tests, transports, and target clients. Capture:

- Cross-tool decisions and preconditions.
- Read-only, mutating, destructive, idempotent, and open-world behavior.
- Cursor, timeout, concurrency, process, and session semantics.
- Partial success, rollback limits, and recovery.
- Which clients reliably expose tools, resources, or both.

Derive rules from implementation evidence. Guide wording must become weaker when the guarantee is weaker.

## Index contract

Expose a compact deterministic index:

```json
{
  "version": "1.0",
  "namespace": "example-mcp",
  "resource_uri": "skill://example-mcp/index",
  "discovery_tool": "get_skill_index",
  "skills": [
    {
      "name": "file-use",
      "description": "Safe file discovery, reading, and mutation workflows.",
      "triggers": ["Before nontrivial file work", "Before file mutation"],
      "required_before_tools": ["search", "read", "apply_patch"],
      "guide_tool": "get_file_use",
      "resource_uri": "skill://example-mcp/file-use"
    }
  ]
}
```

Treat names and URIs as public API. Keep trigger text visible in the index because an unloaded guide cannot trigger itself. Bump the version when routing or operating behavior changes materially.

## Single-source registry

Store metadata and content once:

```python
GUIDES = {
    "file-use": {
        "tool": "get_file_use",
        "uri": "skill://example-mcp/file-use",
        "description": "Safe file discovery, reading, and mutation workflows.",
        "triggers": ["Before file mutation"],
        "required_before_tools": ["search", "read", "apply_patch"],
        "content": FILE_USE_MARKDOWN,
    }
}
```

Generate the index, tool payloads, resources, and capability maps from this registry. Return defensive copies of mutable index data. Keep README content descriptive rather than copying the guide body.

If a filesystem Skill mirror is unavoidable, generate and version it from the authoritative server content. Do not hand-edit both.

## Dual exposure

Expose:

- `get_skill_index` as a zero-argument read-only tool.
- `skill://<namespace>/index` as an `application/json` resource.
- `get_<workflow>_use` as a zero-argument read-only tool.
- `skill://<namespace>/<workflow>` as a `text/markdown` resource.

Return tool payload metadata such as name, version, URI, content type, and content. Use the exact same content value for the matching resource.

Dual exposure is a compatibility decision. Resource-capable clients use `resources/list` and `resources/read`; tool-centric gateways can call `get_*_use`. A client may mix the tool index and resource guide, so routing metadata must agree.

Use the annotation type and registration API of the installed SDK version. Do not copy decorator syntax across FastMCP or other SDK releases without checking signatures.

## Guide contents

Use imperative operating contracts:

1. Critical safety rules.
2. Tool-selection table.
3. Recommended cross-tool sequence.
4. Pagination, cursor, timeout, concurrency, and lifecycle semantics.
5. Mutation and destructive-action guards.
6. Error/status recovery table.
7. Two to four minimal structured examples.

State what a success-looking field does not prove. Examples:

- A wait timeout does not prove the process stopped.
- A path filter may not isolate an already-populated Git index.
- Accepted terminal input does not prove application consumption.
- Separate output cursors do not establish merged stream ordering.

Keep parameter encyclopedias in schemas. Keep guides concise enough to load on demand.

## Discovery and compatibility

Include protocol-visible server instructions such as:

```text
Call get_skill_index to discover operating guides. Load the matching get_*_use guide before the first workflow in that tool family.
```

When a capability/status tool exists, advertise:

```json
{
  "skill_guidance": {
    "discovery_tool": "get_skill_index",
    "index_resource": "skill://example-mcp/index",
    "guide_tools": {"file-use": "get_file_use"},
    "guide_resources": {"file-use": "skill://example-mcp/file-use"},
    "progressive_disclosure": true
  }
}
```

Preserve existing capability fields for compatibility. External documentation alone is insufficient: a freshly attached agent must discover the path through MCP-visible surfaces.

## Validation and anti-patterns

Test:

- Deterministic index order, version, and coverage.
- Every registered workflow tool is covered or intentionally schema-only.
- Exact tool/URI routing and MIME types.
- Read-only guide annotations.
- Byte-equivalent authoritative guide content across tool/resource surfaces.
- Real MCP initialize, list, call, and read operations.
- Fresh-agent scenarios with no hidden implementation context.
- Reloaded local and remote endpoint counts and content.

Avoid:

- Resource-only guides without client compatibility evidence.
- Tool-only guides while claiming standard Resource support.
- Copied content in tool handlers and resource handlers.
- Trigger rules that exist only inside an unloaded guide.
- Examples that invent rollback, isolation, persistence, or timeout guarantees.
- A filesystem mirror that silently diverges from server content.
