---
name: perplexity-search
description: Advanced real-time web search and deep research using Perplexity AI. Instructs the Agent to perform iterative searching, evaluate results, and automatically fill information gaps before returning the final answer.
---

# Perplexity Search & Analysis

Use this skill for fetching real-time data, API docs, news, or performing complex investigations. Do not just use it once; use it iteratively.

## Agent Execution SOP (Standard Operating Procedure)

When handling a user query that requires web search, you MUST follow this precise workflow:

### 1. Deconstruct (拆解问题)
- **Do not** blindly search the entire user prompt.
- Break down complex questions into distinct, logical sub-queries.
- Determine the best tool for each sub-query:
  - `mcp__perplexity-mcp__search` (Quick Search: simple facts, lookups)
  - `mcp__perplexity-mcp__research` + `mode: "reasoning"` (Reasoning: analysis, comparisons)
  - `mcp__perplexity-mcp__research` + `mode: "deep research"` (Deep Research: market trends, comprehensive reports)

### 2. Execute Parallel Searches (并发调用)
- Dispatch tool calls for the sub-queries. Execute them concurrently whenever supported to gather diverse information efficiently.

### 3. Evaluate & Gap Analysis (校验与查漏补缺)
- Synthesize the returned results.
- **CRITICAL STEP**: Cross-check the synthesized data against the original user prompt.
- Ask yourself: *Does this context fully and accurately satisfy the user's request? Are there missing dimensions or unverified claims?*
- If **YES**: Proceed to Step 5.
- If **NO**: Explicitly list the missing information (The "Gaps").

### 4. Iterative Search (循环补搜)
- Formulate new, highly targeted queries based ONLY on the identified gaps.
- Call the appropriate search tools again.
- Repeat Steps 3 and 4 until the context is complete. *(Note: Stop after a maximum of 3 iterations to prevent infinite loops).*

### 5. Final Synthesis (最终输出)
- Compile all verified context into a cohesive, structured, and comprehensive final answer.
- Ensure no raw tool output is shown unless requested; synthesize the findings naturally.

## Parameters
- **query**: The targeted search string.
- **language**: Default to "zh-CN" for Chinese.
