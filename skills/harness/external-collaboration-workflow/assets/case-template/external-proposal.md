---
type: collaboration-proposal
scope: docs
module: FEATURE_SLUG
date: YYYY-MM-DD
status: draft
role: supporting
lifecycle: proposed
evidence_status: source_record
authorization: none
last_verified: YYYY-MM-DD
next_gate: proposal-receipt
keywords: [CASE_ID, external-proposal, recommendation]
read_by_default: false
case_id: CASE_ID
source_owner: external
external_team: EXTERNAL_TEAM
proposal_status: awaiting_external_input
proposal_version: none
received_at: pending
based_on_problem_version: v0.1
based_on_problem_commit: pending
source_artifact: pending
content_fingerprint: pending
---

# CASE_TITLE — 外部团队方案

> 上级：[Case Index](INDEX.md)

> 本文件保存外部来源方案。`awaiting_external_input` 期间不得由内部 Agent 代写方案正文；收到
> 方案后按原始内容或忠实转换内容保存。内部评价与采纳决定写入 `INDEX.md`。

## 1. Provenance

| 字段 | 值 |
|---|---|
| External team | `EXTERNAL_TEAM` |
| Proposal version | `NONE` |
| Received at | `PENDING` |
| Based on problem version | `v0.1` |
| Based on problem commit | `PENDING` |
| Source artifact/link | `PENDING` |
| Content fingerprint | `PENDING` |
| Conversion note | `PENDING` |

## 2. External Proposal Body

`AWAITING_EXTERNAL_INPUT`

收到方案后，应忠实保留下列外部内容结构；如原文结构不同，可保留原文结构而不强行改写：

- Executive summary
- Assumptions
- Proposed design and responsibility boundaries
- Interfaces, data flow, state ownership, dependencies
- Module split, reuse boundaries, file budgets, test ownership
- Migration and rollback
- Validation matrix and acceptance recommendations
- Risks, alternatives, stop conditions
- Open questions

## 3. Transcription Corrections

仅记录格式转换或明显转录勘误，不写内部技术评价。

| Date | Correction | Reason | External content changed |
|---|---|---|---|
| TODO | TODO | TODO | No |
