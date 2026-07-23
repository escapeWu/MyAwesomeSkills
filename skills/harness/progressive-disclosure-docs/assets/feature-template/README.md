---
type: feature
scope: docs
module: FEATURE_SLUG
date: YYYY-MM-DD
status: draft
role: separate-planned
lifecycle: proposed
requirements_status: draft
spec_status: none
decision_status: clear
milestone: not_started
milestone_status: not_started
implementation_status: not_started
model_status: not_applicable
evidence_status: contract_only
authorization: none
last_verified: YYYY-MM-DD
next_gate: contract-freeze
keywords: [FEATURE_SLUG]
read_by_default: true
---

# FEATURE_TITLE

> 上级：[模块索引](INDEX.md)

## 当前主线路线

<!-- MAINLINE-ROUTE:START
{
  "schema_version": 2,
  "route_version": "YYYY-MM-DD.1",
  "summary": "需求确认与 Spec 判定当前焦点 → 功能实施未授权",
  "nodes": [
    {"id": "contract-freeze", "name": "需求确认与 Spec 判定", "progress": "active", "authorization": "docs-only", "owner": "requirements.md"},
    {"id": "implementation", "name": "功能实施", "progress": "planned", "authorization": "unauthorized", "owner": "README.md"}
  ],
  "edges": [["contract-freeze", "implementation"]],
  "focus_nodes": ["contract-freeze"],
  "parallel_groups": [],
  "joins": [],
  "next_gate": "contract-freeze"
}
MAINLINE-ROUTE:END -->

路线：`需求确认与 Spec 判定当前焦点 → 功能实施未授权`

- **当前焦点**：确认 requirements，并判断是否需要 Spec / ADR。
- **当前阻塞**：expected behavior 与 acceptance 尚未确认；实施合同尚未判定。
- **下一验证门**：requirements confirmation / Spec decision。
- **授权边界**：仅 docs/contract；无实施授权。

## 当前状态

| 状态轴 | 当前值 |
|---|---|
| Role | `SEPARATE_PLANNED` |
| Lifecycle | `PROPOSED` |
| Requirements | `DRAFT` |
| Active Spec | `NONE` |
| Blocking Decisions | `CLEAR` |
| Milestone | `NOT_STARTED` |
| Implementation | `NOT_STARTED` |
| Evidence | `CONTRACT_ONLY` |
| Authorization | `NONE` |
| Last verified | `YYYY-MM-DD` |
| Next gate | Requirements confirmation / Spec decision |

## 已完成

- Feature owner 与初始路由已建立。

## 待完成

- 确认 scope、expected behavior、acceptance、NFR 与 stop rules。
- 判断是否需要首个 Spec，以及是否存在阻塞 Spec freeze 的 ADR candidate。

## 当前阻塞

- requirements 尚未确认；尚无实施授权。

## 下一验证门

Requirements confirmation / Spec decision

## 证据

- 仅存在初始合同脚手架，无 engineering、validation 或 execution evidence。

## 开发日志

见 [changelog.md](changelog.md)。

## 活跃合同

- Requirements：[requirements.md](requirements.md)（`DRAFT`）。
- Active Spec：无；实现相关合同明确后按需在 `specs/` 创建。
- Blocking ADR：无；满足 durable decision trigger 时按需在 `decisions/` 创建。
- Implementation authorization：`NONE`。

## 文档所有权

- [requirements.md](requirements.md) 持有 expected behavior、acceptance、NFR 和 stop rules。
- `specs/` 持有 bounded implementation contracts；详细模块图、接口、状态、迁移和 validation matrix 不写入本页。
- `decisions/` 持有 Feature-local ADR；系统级 ADR 由 `docs/reference/decisions/` 持有。
- 本页只持有 Feature map、current route overlay、contract links 与 current snapshot。
- 稳定节点、依赖、并行和汇合关系进入 development plan（需要时创建）。
- [changelog.md](changelog.md) 持有 Feature/Spec/ADR 的 milestone/gate/route 级迁移历史。
