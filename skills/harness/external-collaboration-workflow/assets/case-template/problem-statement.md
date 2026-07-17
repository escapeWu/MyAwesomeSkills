---
type: collaboration-input
scope: docs
module: FEATURE_SLUG
date: YYYY-MM-DD
status: draft
role: supporting
lifecycle: proposed
evidence_status: source_record
authorization: none
last_verified: YYYY-MM-DD
next_gate: external-analysis
keywords: [CASE_ID, problem-statement, external-analysis]
read_by_default: false
case_id: CASE_ID
source_owner: internal
problem_version: v0.1
issued_at: pending
recipient: EXTERNAL_TEAM
content_fingerprint: pending
---

# CASE_TITLE — 问题与证据包

> 上级：[Case Index](INDEX.md)

## 1. 目的和请求

- 希望外部团队回答的问题：TODO。
- 期望交付物：TODO。
- 回复期限或评审窗口：TODO。

## 2. Owning Context

- Owning Feature：[`FEATURE_SLUG`](../../feature/FEATURE_SLUG/README.md)。
- Expected behavior owner：TODO。
- Current implementation owner：TODO。
- Evidence owner：TODO。

## 3. Current / Expected / Gap

| Truth type | 当前事实 | 证据/链接 |
|---|---|---|
| Expected behavior | TODO | TODO |
| Current implementation | TODO | TODO |
| Observed evidence | TODO | TODO |
| Gap classification | `contract_gap` / `implementation_gap` / `evidence_gap` / `stale_summary` | TODO |

## 4. 范围和边界

- 范围内：TODO。
- 范围外：TODO。
- 安全与授权边界：TODO。
- 数据、隐私和脱敏边界：TODO。
- 兼容性与不可变合同：TODO。

## 5. 复现与证据清单

| Evidence ID | Artifact/command | 时间窗/版本 | Checksum | 说明 |
|---|---|---|---|---|
| `E-01` | TODO | TODO | TODO | TODO |

不得粘贴 secrets、凭据、账户 ID 或未授权的私有数据。

## 6. 已尝试方案和未决问题

- 已尝试：TODO。
- 已排除：TODO。
- 外部团队必须明确的 assumptions：TODO。
- 需要回答的问题列表：TODO。

## 7. 方案交付要求

外部方案至少需要覆盖：

- 设计与责任边界；
- 接口、数据流、状态 owner 和依赖方向；
- 模块拆分、复用边界、每个手写文件预算（不得建议超过 1000 行）；
- 迁移与回滚；
- unit/contract/integration/research validation 矩阵；
- 风险、假设、替代方案和停止条件。

## 8. Revision History

| Version | Date | Commit/fingerprint | Change | Issued to external team |
|---|---|---|---|---|
| `v0.1` | `YYYY-MM-DD` | TODO | Initial draft | No |
