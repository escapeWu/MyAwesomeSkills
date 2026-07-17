---
type: collaboration-case
scope: docs
module: FEATURE_SLUG
date: YYYY-MM-DD
status: draft
role: supporting
lifecycle: proposed
evidence_status: source_record
authorization: none
last_verified: YYYY-MM-DD
next_gate: problem-package-issue
keywords: [CASE_ID, external-team, collaboration]
read_by_default: false
case_id: CASE_ID
owning_feature: FEATURE_SLUG
case_status: problem_drafting
problem_version: v0.1
proposal_version: none
decision_status: not_started
implementation_route: none
---

# CASE_TITLE

> 上级：[外部协作索引](../INDEX.md)

## Case 状态

| 字段 | 当前值 |
|---|---|
| Case ID | `CASE_ID` |
| Owning Feature | [`FEATURE_SLUG`](../../feature/FEATURE_SLUG/README.md) |
| Case status | `PROBLEM_DRAFTING` |
| Problem version | `v0.1` |
| Proposal version | `NONE` |
| Decision status | `NOT_STARTED` |
| Next gate | `PROBLEM_PACKAGE_ISSUE` |

## 来源绑定

- [problem-statement.md](problem-statement.md) — 内部问题与证据包。
- [external-proposal.md](external-proposal.md) — 外部团队方案快照。
- Problem commit/fingerprint：`TODO`。
- Proposal source/fingerprint：`TODO`。

## Adoption Matrix

| Proposal ID | Summary | Decision | Internal rationale | SSOT target | Implementation/evidence |
|---|---|---|---|---|---|
| `P-01` | TODO | `PENDING` | TODO | TODO | TODO |

允许的 decision：`PENDING`、`ACCEPTED`、`MODIFIED`、`REJECTED`、`DEFERRED`。
外部方案不构成实施授权；`ACCEPTED`/`MODIFIED` 必须先转译到 owning internal docs。

## 内部转译状态

- Requirements/acceptance：`TODO`。
- Design/interfaces：`TODO`。
- Module map/file budgets/test ownership：`TODO`。
- Owning README next gate：`TODO`。
- Changelog entry：`TODO`。

## 开发与验证追踪

- 当前开发状态：见 owning Feature README/GOAL；本 case 不复制进度。
- 状态迁移：见 owning Feature `changelog.md`。
- 验证与 evidence：`TODO`。

## Close Checklist

- [ ] 每条 proposal item 已有明确决定。
- [ ] 所有采纳项已转译到内部 SSOT。
- [ ] 实施项已完成、延期或拒绝，并有 evidence route。
- [ ] 外部来源、版本和 fingerprint 可追溯。
- [ ] 本页已从 Active Cases 移到 Closed Cases。
