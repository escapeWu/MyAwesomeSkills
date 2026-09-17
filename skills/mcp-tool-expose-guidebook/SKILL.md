---
name: mcp-tool-expose-guidebook
description: Design, implement, audit, or improve progressive-disclosure guidebooks exposed by an MCP server as both discovery tools and standard MCP resources. Use when adding get_skill_index/get_*_use patterns, grouping a large MCP tool surface into workflow guides, teaching agents cross-tool safety and lifecycle rules, wiring FastMCP or another MCP SDK, validating guide discovery/read paths, or replacing duplicated filesystem instructions with one server-owned source of truth.
---

# MCP Tool Expose Guidebook

Build a small discovery index and load-on-demand workflow guides around an existing MCP tool surface. Keep individual tool schemas focused on one call; use guides for multi-tool selection, ordering, safety, lifecycle, monitoring, and recovery.

## Produce these artifacts

- One machine-readable guide index.
- One guide per cohesive workflow family, not per tool.
- One callable `get_*_use` tool for each guide.
- One stable MCP resource URI for the same guide content.
- Server instructions and capability metadata that make discovery explicit.
- Unit, registry, protocol, forward, and live-deployment evidence.

## Workflow

### 1. Audit the real server

Inspect the registered tools, schemas, annotations, implementations, tests, transport, and target clients. Record:

- Tool families and cross-tool decisions.
- Read-only, mutating, destructive, idempotent, and open-world boundaries.
- Pagination, cursor, timeout, concurrency, session, and process-lifetime semantics.
- Preconditions, partial-success behavior, rollback limits, and recovery paths.
- Whether target clients reliably expose MCP resources, tools, or both.

Derive every guide rule from implementation or tested behavior. Do not document the API you wish existed.

### 2. Choose workflow-sized guide boundaries

Create a guide only when agents need knowledge beyond one tool schema. Group by a decision/lifecycle boundary such as:

- File discovery, reading, mutation, revision protection, and verification.
- Synchronous commands, background jobs, and interactive sessions.
- Repository inspection, staging, commits, history, and worktrees.
- Delegated execution, scheduling, monitoring, logs, and cancellation.

Keep simple administrative tools in schemas or a nearby guide. Avoid one guide per tool and avoid one giant guide for the entire server.

### 3. Design the discovery index

Give every entry:

- `name`: stable lowercase hyphenated identifier.
- `description`: concise workflow scope.
- `triggers`: observable situations that require loading it.
- `required_before_tools`: exact registered tool names.
- `guide_tool`: callable compatibility entry point.
- `resource_uri`: stable MCP resource route.

Include an index version and namespace. Keep the index small enough to load first without crowding the task context.

### 4. Author each guide as an operating contract

Use imperative instructions and include only cross-call knowledge:

1. Critical safety rules.
2. A tool-selection table.
3. The recommended sequence and required checks.
4. Pagination, cursor, timeout, and lifecycle semantics.
5. Mutation or destructive-action guards.
6. Error/status recovery actions.
7. Two to four minimal structured examples.

Explicitly state what a success-looking field does **not** prove. Examples: input accepted by a terminal does not prove application consumption; a wait timeout does not mean a process stopped; a path filter may not isolate an already-populated Git index.

### 5. Establish one source of truth

Store each guide body once in server-owned source. Generate both the tool payload and resource response from that same value. Do not maintain handwritten copies in a filesystem skill, server resource, tool response, and README.

Use a filesystem Skill only for this reusable implementation method or for clients that cannot reach the server. If a mirror is unavoidable, generate and version it from the server source.

### 6. Expose tool and resource paths

Read [references/implementation-pattern.md](references/implementation-pattern.md) before coding registration or reviewing an implementation.

- Expose the index as both `get_skill_index` and a JSON MCP resource.
- Expose every guide as both `get_<name>_use` and a Markdown MCP resource.
- Mark guide tools read-only.
- Return structured metadata with name, version, URI, content type, and content.
- Use stable names and URIs; treat them as public API.

Dual exposure is a compatibility choice: native clients can use `resources/list`/`resources/read`, while tool-centric gateways can call `get_*_use`.

### 7. Advertise discovery

Update server instructions to tell agents to call the index and load the matching guide before the first workflow in that family. Report guide tools/resources from a capability endpoint such as `server_info` when one exists.

Do not rely only on prose documentation outside the MCP connection. An attached agent must be able to discover the guides from protocol-visible surfaces.

### 8. Validate behavior, not just content

Read [references/authoring-validation.md](references/authoring-validation.md) before writing tests or declaring completion.

Validate all of the following:

- Index routes every guide to exact tool names and URIs.
- Tool and resource responses share identical authoritative content.
- Tools have read-only annotations.
- A real MCP client can initialize, list, call, and read every surface.
- Fresh agents can use each guide on realistic scenarios without hidden context.
- Live local and remote endpoints expose the new counts and content after restart/reload.

When a forward test reveals a false assumption, correct the guide or underlying tool. Never weaken the test merely to preserve the prose.

### 9. Deploy and verify

Run the server's normal tests and compile/type checks. Restart or rolling-reload the actual service. Verify authentication metadata, initialize a real MCP session, call the index and every guide tool, list resources, and read every guide resource.

Report the guide count, tool/resource routes, validation evidence, deployment status, and any intentionally unsupported client path.

## Hard requirements

- Preserve tool schemas as the source for per-call parameter facts.
- Preserve guides as the source for cross-tool workflow facts.
- Keep guide content concise and versioned.
- Treat workspace roots and friendly path resolution as anchors unless the implementation proves they are sandbox boundaries.
- Never claim atomicity, rollback, isolation, persistence, or timeout behavior beyond the implementation.
- Never call a guide mandatory unless server instructions/index expose that requirement to agents.
- Do not create duplicate handwritten guide copies.

## Completion checklist

- [ ] Tool families were chosen by workflow complexity.
- [ ] Index names, triggers, required tools, guide tools, and URIs are complete.
- [ ] Tool/resource responses use one content source.
- [ ] Discovery appears in server instructions and capability metadata.
- [ ] Safety and recovery rules are tied to code/tests.
- [ ] Registry and real MCP protocol tests pass.
- [ ] Independent forward tests pass without leaked context.
- [ ] The deployed local/remote service was reloaded and re-read.

## References

- Read [references/implementation-pattern.md](references/implementation-pattern.md) for index schemas, FastMCP registration, capability reporting, and client-call patterns.
- Read [references/authoring-validation.md](references/authoring-validation.md) for guide templates, evidence audits, test layers, forward testing, and field lessons.
