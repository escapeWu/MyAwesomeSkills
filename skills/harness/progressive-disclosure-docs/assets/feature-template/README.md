---
type: feature
scope: docs
module: FEATURE_SLUG
date: YYYY-MM-DD
status: draft
role: separate-planned
lifecycle: proposed
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
  "summary": "合同冻结当前焦点 → 功能实施未授权",
  "nodes": [
    {"id": "contract-freeze", "name": "合同冻结", "progress": "active", "authorization": "docs-only", "owner": "requirements.md"},
    {"id": "implementation", "name": "功能实施", "progress": "planned", "authorization": "unauthorized", "owner": "README.md"}
  ],
  "edges": [["contract-freeze", "implementation"]],
  "focus_nodes": ["contract-freeze"],
  "parallel_groups": [],
  "joins": [],
  "next_gate": "contract-freeze"
}
MAINLINE-ROUTE:END -->

路线：`合同冻结当前焦点 → 功能实施未授权`

- **当前焦点**：冻结合同。
- **当前阻塞**：expected behavior、schema、validation matrix 与 stop rules 尚未冻结。
- **下一验证门**：合同冻结。
- **授权边界**：仅 docs/contract；无实施授权。

## 当前状态

| 状态轴 | 当前值 |
|---|---|
| Role | `SEPARATE_PLANNED` |
| Lifecycle | `PROPOSED` |
| Milestone | `NOT_STARTED` |
| Implementation | `NOT_STARTED` |
| Evidence | `CONTRACT_ONLY` |
| Authorization | `NONE` |
| Last verified | `YYYY-MM-DD` |
| Next gate | 合同冻结 |

## 已完成

- Feature owner 与初始路由已建立。

## 待完成

- 冻结 scope、expected behavior、schema、validation matrix、stop rules 和 evidence outputs。

## 当前阻塞

- 尚未完成合同冻结；尚无实施授权。

## 下一验证门

合同冻结

## 证据

- 仅存在初始合同脚手架，无 engineering、validation 或 execution evidence。

## 开发日志

见 [changelog.md](changelog.md)。

## 实施前模块设计

Lifecycle 进入 `IMPLEMENTATION_ACTIVE` 前必须完成下表；手写代码文件最多 1000 物理行，
800 行进入拆分预警。

| 模块 | 单一责任 | 公共接口 | 允许依赖 | 文件预算 | 测试归属 |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | `< 800` | TODO |

- 可变状态 owner：TODO。
- 共享/复用边界与现有消费者：TODO。
- CLI/adapter/runner 薄层入口：TODO。
- 禁止的反向或环形依赖：TODO。

## 文档所有权

- [requirements.md](requirements.md) 持有 expected behavior、acceptance 和 stop rules。
- 本页持有 current route overlay 与 current snapshot。
- 稳定节点、依赖、并行和汇合关系进入 development plan（需要时创建）。
- [changelog.md](changelog.md) 持有 milestone/gate/route 级迁移历史。
