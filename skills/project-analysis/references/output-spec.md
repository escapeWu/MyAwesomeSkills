# 输出规范与文档落点指南

本文件定义 `project-analysis` 在当前两种执行模式下的输出形态、长期文档落点优先级，以及新建独立分析文档时的命名方式。

## 执行模式与输出

### 模式 A：new-doc

用于当前没有合适长期文档承接，或用户明确要求单独成文时。

输出：
- 新建文档
- 结构化结论
- 证据路径
- Mermaid 图
- 与 Mermaid 语义一致的 ASCII/TUI 预览图
- 可长期维护的文档结构

### 模式 B：update-doc

用于在已有长期项目文档中做增量更新。

输出：
- 基于 `docs/feature-*.md` / `docs/reference-*.md` / `docs/OVERVIEW.md` 的增量更新
- 保留仍然正确的旧内容
- 仅更新过期、缺失或不准确的部分

### 模式选择规则

- 默认优先判断是否存在可承接的现有文档
- 若存在，使用 `update-doc`
- 若不存在，使用 `new-doc`
- 不再使用 `analysis-only`
- 不再使用 `docs-patch` / `standalone-report` 作为独立模式

---

## 文档落点优先级

默认优先维护这一套长期项目文档：

1. `docs/feature-*.md`
2. `docs/reference-*.md`
3. `docs/OVERVIEW.md`

优先规则：
- 功能行为、模块实现、接口、数据模型、测试方式、变更记录，优先回填 `feature-*`
- 外部系统、第三方 API、架构参考、限制条件，优先回填 `reference-*`
- 新增模块、模块边界、文档索引入口，优先更新 `docs/OVERVIEW.md`

只有在以下情况才生成新文档：
- 当前项目中没有合适的长期文档可承接
- 用户明确要求独立成文
- 分析结果具备独立维护价值，不适合硬塞进现有文档

---

## new-doc 输出要求

当处于 `new-doc` 模式时，推荐输出/写入结构如下：

```markdown
# 文档标题

## 分析结论
- 结论 1
- 结论 2

## 证据路径
- `src/foo.ts`
- `src/bar.ts`

## 图表
[Mermaid 图]
[ASCII/TUI 预览图]

## 详细分析
...
```

说明：
- 新文档应尽量遵循项目 docs 体系的命名和结构约定
- 分析结论必须能回溯到文件路径、模块、入口点或调用链
- 每张 Mermaid 图后必须紧跟一张语义一致的 ASCII/TUI 预览图

---

## update-doc 输出要求

在 `update-doc` 模式下，写入前至少检查：
- 目标文档是否选对（`feature-*` / `reference-*` / `OVERVIEW.md`）
- update 是否保留了仍然正确的内容
- 新增结论是否能回溯到文件路径、模块、入口点或调用链
- Mermaid 与 ASCII/TUI 预览图语义一致
- 是否需要同步更新该文档的 Changelog
- 如果是新增模块，是否需要同步更新 `docs/OVERVIEW.md`

如果需要枚举候选文档，可优先读取：
- `docs/OVERVIEW.md`
- 相关 `docs/feature-*.md`
- 相关 `docs/reference-*.md`

如 `docs/` 中存在旧式分析文档、frontmatter 元数据或需要额外补充检索，可选使用 metadata 扫描脚本辅助检查：

```bash
python3 <skills-root>/skills/project-analysis/scripts/scan_docs_metadata.py <项目根目录>/docs
```

它是**辅助工具**，不是主判断依据。

---

## 独立分析文档命名（仅 new-doc 场景使用）

| 分析类型 | 文件名格式 | 示例 |
|---------|-----------|------|
| 系统架构 | `architecture.md` | `docs/architecture.md` |
| 数据流 | `dataflow-{功能}.md` | `docs/dataflow-login.md` |
| 时序图 | `sequence-{流程}.md` | `docs/sequence-order-create.md` |

注意：这类文件不是默认长期落点。优先仍是 `feature-*` / `reference-*` / `OVERVIEW.md`。

---

## 结构化 section 草稿建议

当需要把分析结果回填到长期文档时，可优先产出以下 section 草稿：

### 回填到 `feature-*`
- 功能概述
- 入口点 / 调用链
- 关键数据模型
- 外部依赖
- 测试方式 / 验证方式
- 本次变更或新增分析结论

### 回填到 `reference-*`
- 第三方服务说明
- 外部接口约束
- 架构参考
- 限制条件 / 注意事项
- 排障或性能观察要点

### 回填到 `OVERVIEW.md`
- 模块边界
- 新增模块索引
- 目录入口变化
- 文档索引入口

---

## 最佳实践

- 优先把分析结果沉淀进长期文档，而不是停留在终端结论
- 文档只能作为半可信上下文，代码才是最终依据
- 如调用方已提供候选文档路径，优先复用，避免重复扫描 `docs/`
- 新建文档前先判断现有文档是否可承接
- 若分析结果能稳定沉淀，应优先更新长期项目文档，而不是生成一次性报告文件

