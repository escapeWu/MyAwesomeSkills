# FEATURE_TITLE 索引

> 上级：[功能索引](../INDEX.md)

先在本页选择任务，再按需读取 1 至 3 份 leaf docs。

| 任务 | 文档 | 所有权 |
|---|---|---|
| 当前路线、focus、completed、pending、blockers、next gate | [README.md](README.md) | route overlay + current snapshot |
| expected behavior、acceptance、stop rules | [requirements.md](requirements.md) | frozen contract |
| 实施前模块职责、依赖、公共接口、文件预算与测试归属 | [README.md](README.md) | code-organization gate |
| milestone/gate 级迁移历史 | [changelog.md](changelog.md) | append-only development log |
| 外部问题包、方案来源与采纳决策 | [`docs/collaboration/INDEX.md`](../../collaboration/INDEX.md) | provenance only; accepted items must return to this Feature's internal SSOT |

创建 Feature 后必须同步注册 `docs/feature/INDEX.md` 和 `docs/OVERVIEW.md`，并运行
`python3 scripts/validate_research_docs.py`。
