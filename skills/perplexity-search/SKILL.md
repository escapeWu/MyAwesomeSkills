---
name: perplexity-search
description: Real-time web search and deep research using Perplexity AI. Use when you need the latest web data, API docs, news, or complex investigations that require current information.
---

# Perplexity Search

Use this skill for fetching real-time data from the web.

## Workflow

1.  **Quick Search**: For simple facts or quick lookups.
    -   Tool: `mcp__perplexity-mcp__search`
2.  **Reasoning**: For complex questions requiring analysis.
    -   Tool: `mcp__perplexity-mcp__research` (mode: "reasoning")
3.  **Deep Research**: For comprehensive investigations.
    -   Tool: `mcp__perplexity-mcp__research` (mode: "deep research")

## Selection Guide

-   **"Latest version of React?"** -> Quick Search
-   **"React 19 vs 18 analysis?"** -> Reasoning
-   **"Market trends of AI in 2025?"** -> Deep Research

## Parameters

-   **query**: The search string.
-   **language**: Default to "zh-CN" for Chinese.
