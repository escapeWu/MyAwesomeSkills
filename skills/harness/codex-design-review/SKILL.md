---
name: codex-design-review
description: >-
  Targeted design/code review via Codex CLI. Use when a specific design document,
  implementation plan, code module, or feature scope needs focused review — not a
  blanket "review all uncommitted changes". Outputs a structured review report to
  `docs/feature/<module>/review-<slug>.md` as a collaboration artifact between the
  orchestrating agent and Codex. Use when the user asks to "review this design",
  "审查方案", "让 codex 审查", "review this feature", or when a design document
  needs validation before implementation begins.
---

# Codex Design Review Skill

Turn a design document or implementation scope into a structured Codex review task with auditable output.

## Core Concept

`codex review --uncommitted` reviews **all** uncommitted changes — this is wrong for targeted design review because:

1. Unrelated changes dilute the review focus
2. Codex treats Markdown docs as low-priority compared to code
3. No structured output is produced for follow-up

This skill instead uses `codex` in **prompt mode** to review specific content with a focused TaskSpec, and writes a structured review report to the feature's docs directory.

## When to Use

- A design document (README, plan, contract) needs review before implementation
- A specific code module needs focused review (not all changes)
- The user explicitly asks to "review" or "审查" a particular design/feature
- A milestone gate needs design validation evidence

## When NOT to Use

- For blanket uncommitted-changes review → use the global `codex-review` skill
- For code linting only → use `make test` / `ruff` directly
- For simple typo/formatting checks

---

## Execution Steps

### Step 0: Identify Review Target

Determine:

| Field | Description |
|-------|-------------|
| **target_files** | Files to review (1-5 files, focused) |
| **feature_module** | Feature directory under `docs/feature/` |
| **review_slug** | Short identifier for the review (e.g., `design-v1`, `contract-safety`) |
| **review_focus** | What specifically to evaluate (design coherence, safety, feasibility, etc.) |
| **context_files** | Additional files that provide context but aren't the review target |

### Step 1: Build the Review Prompt

Construct a Codex prompt that includes:

1. **Role**: "You are reviewing a design document for a trading signal system."
2. **Target content**: The actual file content(s) to review
3. **Context**: Related code/contracts that inform the review
4. **Review criteria**: Specific aspects to evaluate
5. **Output format**: Structured Markdown report format

Use this template:

```
Review the following design document for the TradingSignal project.

## Review Target
<paste target file content>

## Context Files
<paste relevant context snippets — contracts, schemas, related code>

## Review Criteria
Evaluate the design against these criteria:

1. **Completeness**: Are all necessary aspects covered? Any missing edge cases?
2. **Consistency**: Does it align with existing system contracts and architecture?
3. **Feasibility**: Can it be implemented with the current codebase?
4. **Safety**: Does it maintain system boundaries (no trade execution)?
5. **Defects**: Are there logical errors, contradictions, or incorrect assumptions?
6. **Testability**: Can the design be validated with automated tests?

## Output Format
Respond with a structured review report using this format:

### Summary
One paragraph overall assessment.

### Findings
For each finding:
- **[Severity]** Title — file:line_reference
  Description of the issue and recommended fix.

Severity levels: P0 (blocker), P1 (high), P2 (medium), P3 (low), INFO (observation)

### Recommendations
Numbered list of actionable recommendations.

### Verdict
APPROVE / APPROVE_WITH_CONDITIONS / REQUEST_CHANGES / BLOCK
```

### Step 2: Execute Codex Review

Run codex in prompt mode (NOT --uncommitted):

```bash
codex --prompt "$(cat /tmp/review-prompt.txt)" \
  --config model=gpt-5.5 \
  --config model_reasoning_effort=xhigh
```

**Difficulty-based model selection**:

| Condition | Model + Effort | Timeout |
|-----------|---------------|---------|
| Target files ≥ 5 or total lines ≥ 2000 | `gpt-5.5` + `xhigh` | 40 min |
| Target files ≥ 3 or total lines ≥ 500 | `gpt-5.5` + `xhigh` | 15 min |
| Otherwise | `gpt-5.5` + `high` | 10 min |

### Step 3: Write Review Report

Write the review output to:

```
docs/feature/<feature_module>/review-<slug>.md
```

The report file format:

```markdown
# Review: <slug>

> Reviewed by: Codex (<model>, <effort>)
> Date: <date>
> Target: <target_files list>
> Verdict: <APPROVE / APPROVE_WITH_CONDITIONS / REQUEST_CHANGES / BLOCK>

## Summary

<Codex summary>

## Findings

<Codex findings, preserved as-is>

## Recommendations

<Codex recommendations, preserved as-is>

## Review Metadata

| Field | Value |
|-------|-------|
| Model | <model> |
| Reasoning Effort | <effort> |
| Duration | <seconds> |
| Target Files | <list> |
| Context Files | <list> |
| Review Focus | <focus description> |
```

### Step 4: Report to User

Summarize:
- Verdict (APPROVE / REQUEST_CHANGES / etc.)
- Number of findings by severity
- Key actionable items
- Path to the full review report

---

## Integration with Feature Workflow

This skill fits into the harness engineering plan workflow:

```text
M0 Planning Gate
  └── Design document created
  └── ★ codex-design-review → review-design-v1.md
  └── Design approved or revised

M1 Contract Foundation
  └── Contract files created
  └── ★ codex-design-review → review-contracts.md
  └── Contracts frozen

M5 Integration Gate
  └── Implementation complete
  └── ★ codex-design-review → review-integration.md (code-focused)
  └── Feature shipped
```

Each review report becomes part of the feature's audit trail.

---

## Example: Reviewing Trade Suggestion Design

```
Step 0: Identify
  target_files: [docs/feature/trade-suggestion/README.md]
  feature_module: trade-suggestion
  review_slug: design-v1
  review_focus: Design completeness, calculation logic, safety boundary changes
  context_files: [
    src/api/services/confirmation_contract.py,
    src/api/services/confirmation_resolver.py,
    src/api/services/key_zone.py (lines 19-50, zone dataclass)
  ]

Step 1: Build prompt with target content + context snippets

Step 2: codex --prompt "..." --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh

Step 3: Write to docs/feature/trade-suggestion/review-design-v1.md

Step 4: Report verdict + findings to user
```

---

## Important Notes

- Always include relevant **context files** — Codex needs to see existing contracts/schemas to validate the design against them
- Keep target content focused (1-5 files) — too much content dilutes review quality
- The review report is a **collaboration artifact** — it should be readable by both agents and humans
- Review reports are NOT disposable — they become part of the feature's audit trail in `docs/feature/`
- Do NOT use `--uncommitted` for targeted reviews — that reviews everything
