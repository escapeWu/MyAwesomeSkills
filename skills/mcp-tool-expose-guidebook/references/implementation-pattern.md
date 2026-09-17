# Implementation Pattern

## Contents

1. Architecture
2. Index contract
3. Single-source registry
4. FastMCP example
5. Server discovery
6. Client flow
7. Other SDKs
8. Anti-patterns

## Architecture

Use one content registry to feed two protocol surfaces:

```text
authoritative guide registry
        ├── get_skill_index / get_*_use tools
        └── skill://... index / guide resources
```

The tool route is the compatibility surface. The resource route is the standard MCP content surface. They must not have separately maintained bodies.

## Index contract

Use a compact JSON-compatible shape:

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
      "triggers": [
        "Before the first nontrivial file workflow",
        "Before file mutation"
      ],
      "required_before_tools": ["search", "read", "apply_patch"],
      "guide_tool": "get_file_use",
      "resource_uri": "skill://example-mcp/file-use"
    }
  ]
}
```

Keep ordering deterministic. Treat tool names and resource URIs as public API. Bump the version when operating behavior or routing materially changes.

## Single-source registry

Prefer a data structure that owns metadata and content together:

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

Generate index entries and guide payloads from this structure. Return defensive copies of mutable index data.

## FastMCP example

Register the JSON index resource:

```python
@mcp.resource(
    "skill://example-mcp/index",
    name="skill-index",
    mime_type="application/json",
)
def skill_index_resource() -> str:
    return json.dumps(skill_index_payload(), ensure_ascii=False, indent=2) + "\n"
```

Register one Markdown guide resource:

```python
@mcp.resource(
    "skill://example-mcp/file-use",
    name="file-use",
    mime_type="text/markdown",
)
def file_use_resource() -> str:
    return GUIDES["file-use"]["content"]
```

Register matching read-only tools:

```python
@mcp.tool(
    name="get_skill_index",
    annotations={"readOnlyHint": True},
    description="Discover workflow guides and load the matching guide before its tool family.",
)
def get_skill_index() -> dict[str, object]:
    return {"success": True, **skill_index_payload()}


@mcp.tool(
    name="get_file_use",
    annotations={"readOnlyHint": True},
    description="Load the file workflow operating guide before nontrivial file work.",
)
def get_file_use() -> dict[str, object]:
    guide = GUIDES["file-use"]
    return {
        "success": True,
        "name": "file-use",
        "version": GUIDE_VERSION,
        "resource_uri": guide["uri"],
        "content_type": "text/markdown",
        "content": guide["content"],
    }
```

Use the annotation type required by the installed FastMCP version. Do not copy an example annotation blindly across framework versions.

For many guides, generate resource/tool registrations through a supported provider or a small registration helper. Preserve distinct callable names if the framework derives schemas or routing from function identity.

## Server discovery

Add a short instruction to the MCP server:

```text
Call get_skill_index to discover progressive-disclosure operating guides. Load the matching get_*_use guide before the first workflow in that tool family.
```

If the server has a capability tool, return:

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

Do not remove older compatibility fields without checking existing callers.

## Client flow

Tool-centric client:

```text
tools/list → get_skill_index → get_file_use → search/read/apply_patch
```

Resource-capable client:

```text
resources/list → resources/read(skill://example-mcp/index)
               → resources/read(skill://example-mcp/file-use)
               → search/read/apply_patch
```

A client may mix paths: call the tool index and read the guide resource. Keep the metadata identical so this works.

## Other SDKs

Map the same architecture to the SDK's primitives:

- Register static JSON and Markdown resources.
- Register read-only zero-argument guide tools.
- Return structured content where supported.
- Expose server instructions/capabilities.
- Use streamable HTTP or stdio without changing guide semantics.

Do not make the guide architecture dependent on decorator syntax or Python imports.

## Anti-patterns

- One Skill for every tool.
- One giant guide loaded before every call.
- Guide content duplicated between a tool response and resource function.
- Resources only, without checking client discovery support.
- Tools only, while claiming standard resource discovery.
- Trigger rules described only inside the full guide; the agent cannot see them before loading it.
- Examples that promise rollback, isolation, or persistence the tool does not implement.
- A filesystem mirror edited independently from the server source.
