# 输出规范与文档落点指南

本文件定义 `project-analysis` 在不同执行模式下的输出形态、长期文档落点优先级，以及仅在例外情况下使用的独立分析文档命名方式。

## 执行模式与输出

### 模式 A：analysis-only（默认）

用于深度理解代码、梳理架构、分析数据流、时序或性能风险。

输出：
- 结构化结论
- 证据路径
- Mermaid 图
- 与 Mermaid 语义一致的 ASCII/TUI 预览图
- 可直接回填到 docs 的 section 草稿

默认**不写文件**。

### 模式 B：docs-patch

用于在已有长期项目文档中做增量修补。

输出：
- 基于 `docs/feature-*.md` / `docs/reference-*.md` / `docs/OVERVIEW.md` 的 patch
- 保留仍然正确的旧内容
- 仅更新过期、缺失或不准确的部分

### 模式 C：standalone-report

仅当用户明确要求独立分析报告，或当前没有合适长期文档承接时使用。

输出：
- 独立分析文档
- 仍应优先提示用户是否已有更合适的长期文档可承接

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

只有在以下情况才生成独立分析文档：
- 用户明确要求独立架构 / 数据流 / 时序 / 性能报告
- 当前项目中没有合适的长期文档可承接
- 分析结果本身就是一次性调查稿

---

## analysis-only 输出结构

当处于 `analysis-only` 模式时，推荐输出结构如下：

```markdown
## 分析结论
- 结论 1
- 结论 2

## 证据路径
- `src/foo.ts`
- `src/bar.ts`

## 图表
[Mermaid 图]
[ASCII/TUI 预览图]

## 可回填 section 草稿
### 可写入 docs/feature-xxx.md 的段落
...
```

说明：
- 分析结论必须能回溯到文件路径、模块、入口点或调用链
- 每张 Mermaid 图后必须紧跟一张语义一致的 ASCII/TUI 预览图
- 若当前不写文档，也应尽量给出可直接粘贴的 section 草稿

---

## docs-patch 输出要求

在 `docs-patch` 模式下，写入前至少检查：
- 目标文档是否选对（`feature-*` / `reference-*` / `OVERVIEW.md`）
- patch 是否保留了仍然正确的内容
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

## standalone-report 输出要求

仅在明确需要独立分析报告时，才使用单独文件。

报告可包含：
- 结构化结论
- 证据路径
- Mermaid 图
- ASCII/TUI 预览图
- 可追加到长期文档的 section 草稿

如果独立报告中形成了稳定、长期有效的项目知识，应进一步提示用户或调用方考虑将其中稳定部分回填到 `feature-*` / `reference-*` / `OVERVIEW.md`。

---

## 独立分析文档命名（仅例外使用）

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

- 优先把分析视为“读代码 + 结构化结论”，而不是“默认生成新报告”
- 文档只能作为半可信上下文，代码才是最终依据
- 如调用方已提供候选文档路径，优先复用，避免重复扫描 `docs/`
- 使用独立分析文档时，应说明为什么长期文档无法承接
- 若分析结果能稳定沉淀，应优先回填到长期项目文档，而不是新增一次性报告文件
