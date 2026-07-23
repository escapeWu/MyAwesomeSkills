# FEATURE_TITLE Specs

> 上级：[Feature](../README.md)

只读取当前任务涉及的 Spec。已验证、拒绝或 superseded 的 Spec 按仓库 archive policy 路由，不默认加载。

| ID | Title | Status | Requirements version | Blocking ADRs | Last updated | Document |
|---|---|---|---|---|---|---|
| SPEC-YYYY-NNN | SPEC_TITLE | DRAFT | YYYY-MM-DD.N | none | YYYY-MM-DD | [SPEC_TITLE](SPEC-YYYY-NNN-slug.md) |

## Rules

- IDs immutable；不要覆盖 validated/rejected/superseded Spec。
- README 只 roll up active Spec links 与 compact status。
- Spec freeze 必须通过 `feature-spec-decision-contract.md` 的 gate。
