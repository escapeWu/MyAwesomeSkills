# FEATURE_TITLE 索引

> 上级：[功能索引](../INDEX.md)

先在本页选择任务，再按需读取 1 至 3 份 leaf docs。

| 任务 | 文档 | 所有权 |
|---|---|---|
| Feature map、当前路线、contract links、completed、pending、blockers、next gate | [README.md](README.md) | route overlay + current snapshot |
| expected behavior、acceptance、NFR、non-goals、stop rules | [requirements.md](requirements.md) | requirements contract |
| bounded implementation contract | `specs/INDEX.md`（首个 Spec 时惰性创建） | Spec routing + lifecycle |
| Feature-local architecture decisions | `decisions/INDEX.md`（首个 ADR 时惰性创建） | decision routing + status |
| milestone/gate/Feature/Spec/ADR 迁移历史 | [changelog.md](changelog.md) | append-only development log |
| 外部问题包、方案来源与采纳决策 | [`docs/collaboration/INDEX.md`](../../collaboration/INDEX.md) | provenance only; accepted items must return to this Feature's internal SSOT |

创建 Feature 后必须同步注册 `docs/feature/INDEX.md` 和 `docs/OVERVIEW.md`，并运行仓库已有的文档链接与结构校验。不要引用目标仓库中不存在的验证脚本。
