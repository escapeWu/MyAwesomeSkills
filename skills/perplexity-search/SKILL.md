---
name: perplexity-search
description: Advanced real-time web search and deep research using Perplexity AI. Instructs the Agent to assess query complexity, route to either a single-shot fast search or an iterative deep investigation, and automatically fill information gaps before returning the final answer.
---

# Perplexity Search & Analysis

Use this skill for fetching real-time data, API docs, news, or performing complex investigations.

## Agent Execution SOP (Standard Operating Procedure)

When handling a user query that requires web search, you MUST follow this precise workflow:

### Step 0: Assess Complexity & Route (评估复杂度与路由)
Analyze the user's prompt to determine its complexity:
- **Simple Queries** (e.g., current weather, quick fact checks, simple definitions, stock prices): Route to **[Fast Path]**.
- **Complex Queries** (e.g., market research, code analysis, multi-step reasoning, comparative analysis): Route to **[Deep Path]**.

---

### [Fast Path] (快速单次调用)
1. **Single Tool Call**: Use `mcp__perplexity-mcp__search` with the exact user query or a directly optimized version.
2. **Direct Answer**: Retrieve the result and provide a concise, direct answer to the user. Do not perform any further iterations or deep analysis.

---

### [Deep Path] (深度迭代检索)

#### 1. Deconstruct & Tool Allocation (问题拆解与工具智能分配)
- Break down complex questions into distinct, logical sub-queries.
- **CRITICAL: Balance Speed and Quality.** Do not use heavy research tools for everything. Intelligently assign the right tool to the right sub-query:
  - **[High Speed]** `mcp__perplexity-mcp__search`: Use for fast, factual lookups, basic definitions, or verifying specific dates/names.
  - **[Balanced]** `mcp__perplexity-mcp__research` + `mode: "reasoning"`: Use for evaluating options, synthesizing arguments, or comparative analysis.
  - **[High Quality, Low Speed]** `mcp__perplexity-mcp__research` + `mode: "deep research"`: Use ONLY for comprehensive market data, deep technical investigations, or exhaustive evidence gathering.

#### 2. Execute Parallel Searches (并发调用)
- Dispatch tool calls for the sub-queries. Execute them concurrently whenever supported to minimize overall latency.

#### 3. Evaluate & Gap Analysis (校验与查漏补缺)
- Synthesize the returned results.
- **CRITICAL STEP**: Cross-check the synthesized data against the original user prompt.
- Ask yourself: *Does this context fully and accurately satisfy the user's request? Are there missing dimensions?*
- If **YES**: Proceed to Step 5.
- If **NO**: Explicitly list the missing information (The "Gaps").

#### 4. Iterative Search (循环补搜)
- Formulate new, highly targeted queries based ONLY on the identified gaps.
- Prioritize using the faster `mcp__perplexity-mcp__search` for gap-filling unless deep analysis is strictly required.
- Repeat Steps 3 and 4 until the context is complete. *(Note: Stop after a maximum of 3 iterations to prevent infinite loops).*

#### 5. Final Synthesis (最终输出)
- Compile all verified context into a cohesive, structured, and comprehensive final answer.
- Ensure no raw tool output is shown unless requested.

## Parameters
- **query**: The targeted search string.
- **language**: Default to "zh-CN" for Chinese.
