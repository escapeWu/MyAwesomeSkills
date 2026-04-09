---
name: project-analysis
description: 深度项目分析工具。用于在现有 docs 不足、代码链路复杂、需要梳理系统架构、模块数据流、时序或性能风险时进行只读取证和结构化分析。常与 `project-docs-workflow` 配套使用，作为其升级步骤；也可在用户明确要求架构分析、数据流分析、时序图、调用链梳理或性能排查时直接使用。默认输出分析结论、证据路径和可回填 section，不默认创建独立长期文档；仅在用户明确要求更新 docs 或生成独立分析报告时写入文档。
---

# 项目分析技能

本技能是项目的**深度分析层**。

它不负责每次开发前后的通用 docs 编排；那由 `project-docs-workflow` 负责。它的职责是：在现有文档不足、链路复杂或用户明确需要时，做只读取证、调用链梳理、图表整理和性能观察，并产出可直接回填到项目 docs 的分析结果。

默认以 `analysis-only` 模式工作：输出结构化结论、证据路径、Mermaid 图和对应的 ASCII/TUI 预览图、可回填 section 草稿，不默认写文件。

**强制要求：凡是输出 Mermaid 图表，必须在同一位置紧跟对应的 ASCII/TUI 预览图，方便用户在终端和代码评审中直接审查结构。不得省略，不得标记为可选。**

## 分析主题

本技能可用于以下分析主题：
- `architecture`：系统架构、模块边界、依赖关系、外部服务
- `dataflow`：模块数据流、调用链、关键数据变换、外部 I/O
- `sequence`：主流程时序、跨层交互、关键分支
- `performance-risk`：性能热点、放大点、瓶颈候选、风险链路

## 执行模式

### 模式 A：analysis-only（默认）
用于理解代码、梳理架构、分析数据流、定位时序或性能风险。

输出：
- 结构化结论
- 证据路径
- Mermaid 图 + ASCII/TUI 预览图
- 可回填的 section 草稿

默认**不写文件**。

### 模式 B：docs-patch
当用户明确要求更新 docs，或由 `project-docs-workflow` 升级调用并指定 patch 目标时使用。

输出：
- 基于现有 `feature-*` / `reference-*` / `OVERVIEW.md` 的增量 patch
- 保留仍然正确的内容
- 仅更新过期、缺失或不准确的部分

### 模式 C：standalone-report
仅当用户明确要求独立分析文档时使用。

输出：
- 独立分析报告
- 默认仍应优先提示用户是否已有更合适的 `feature-*` / `reference-*` 可承接

## 标准执行 SOP

### 1. 理解需求并检查项目 docs

先明确：
- 用户要的是 `architecture` / `dataflow` / `sequence` / `performance-risk` 哪类分析
- 分析范围：全项目 / 模块级
- 目标模块、入口点、关键功能点
- 当前执行模式：`analysis-only` / `docs-patch` / `standalone-report`

优先检查：
- `docs/OVERVIEW.md`
- 相关 `docs/feature-*.md`
- 相关 `docs/reference-*.md`

如果调用方（如 `project-docs-workflow`）已经提供候选文档路径，优先读取这些文档；如果没有，再自行扫描 `docs/`。

这些文档只能作为**半可信上下文**：
- 可用于快速建立模块心智模型
- 但必须继续以当前代码核实
- 文档与代码冲突时，以代码为准

只有在 `docs-patch` 或 `standalone-report` 模式下，才需要进入 patch / overwrite / cancel 的写文档决策。如果只是 `analysis-only`，直接继续分析，不要因为 docs 决策阻塞。

如 `docs/` 中存在旧式分析文档、frontmatter 元数据或需要做补充检索，可选使用 metadata 扫描脚本作为辅助：

```bash
python3 <skills-root>/skills/project-analysis/scripts/scan_docs_metadata.py <项目根目录>/docs
```

它不是主判断依据。主判断依据应是：
- `docs/OVERVIEW.md`
- `docs/feature-*.md`
- `docs/reference-*.md`
- 当前代码

### 2. 拆解子任务

在正式读代码前，先把分析拆成 2-4 个**边界清晰、只读、可并行**的子任务。

拆分原则：
- 每个子任务只负责一类证据收集，不直接写最终文档
- 子任务之间尽量不要共享上下文，避免重复搜索
- 主 agent 负责最终判断、冲突消解、图表整理、section 草稿和文档 patch

推荐拆分方式：
- **系统架构分析**：技术栈与入口点 / 目录与模块边界 / 依赖关系、外部服务与性能风险
- **模块数据流分析**：入口点定位 / 调用链与关键节点 / 数据模型、外部 I/O 与放大点
- **时序或性能排查**：主流程 / 分支与异常路径 / 热点候选与观察结论

### 3. 子任务下发 SubAgent 并行实施

使用 Agent 工具启动 SubAgent 并行执行子任务。

执行要求：
- 优先让 subagent 做只读工作：Glob、Grep、Read、依赖梳理、调用链追踪、模块职责归纳
- 一次并行 2-4 个子任务即可，只并行真正独立的分析
- 每个 subagent 的 prompt 必须写清：分析目标、目标目录/文件/关键词、要返回的结构化结果
- subagent **不要**直接写最终文档，只返回事实、路径、调用链、关键结论、可疑缺口、风险点
- 主 agent **不要**和 subagent 重复执行同样的检索

### 4. 汇总子任务信息并整理结果

主 agent 汇总各 subagent 的结果后，再统一形成分析输出。

主 agent 负责：
- 合并并去重各子任务结论
- 解决冲突信息，必要时补充定向查证
- 产出结构化分析结论
- 生成 Mermaid 图表和对应 ASCII/TUI 预览图
- 生成可直接回填到文档的 section 草稿
- 仅在 `docs-patch` 或 `standalone-report` 模式下执行写文档动作

### 5. Review 与 Patch

在 `docs-patch` 模式下，写入前至少检查：
- 目标文档是否选对（`feature-*` / `reference-*` / `OVERVIEW.md`）
- patch 是否保留了仍然正确的旧内容
- 新增结论是否能回溯到文件路径、模块、入口点或调用链
- Mermaid 与 ASCII/TUI 预览图语义一致
- 是否需要同步更新该文档的 Changelog
- 如果是新增模块，是否需要同步更新 `docs/OVERVIEW.md`
- 如果本次形成新的稳定踩坑经验，是否应提示调用方考虑补充“历史教训”或规则文档

如发现更适合沉淀到规则层的经验，只负责识别并提示调用方；**不要默认直接修改 `CLAUDE.md`**。

### 6. 向用户汇报分析结果

完成后，向用户汇报：
- 当前执行模式
- 输出类型：结构化结论 / docs patch / 独立报告
- 包含哪些图表（架构图、时序图、数据流图等）
- 2-4 条关键发现概览
- 如有未覆盖边界、风险点或建议追加分析，也一并说明
- 如果写入了文档，再补充保存路径和本次是 patch / overwrite / new 中的哪一种

## 文档落点优先级

默认优先维护这一套长期项目文档：

1. `docs/feature-*.md`
2. `docs/reference-*.md`
3. `docs/OVERVIEW.md`

优先规则：
- 功能行为、模块实现、接口、数据模型、测试方式、变更记录，优先回填 `feature-*`
- 外部系统、第三方 API、架构参考、限制条件，优先回填 `reference-*`
- 新增模块、模块边界、文档索引入口，更新 `docs/OVERVIEW.md`

仅在下列情况才生成独立分析文档：
- 用户明确要求独立架构 / 数据流 / 时序 / 性能报告
- 当前项目中没有合适的长期文档可承接
- 分析结果本身就是一次性调查稿

## 独立分析文档命名（仅例外使用）

| 分析类型 | 文件名格式 |
|---------|-----------|
| 系统架构 | `architecture.md` |
| 数据流 | `dataflow-{功能}.md` |
| 时序图 | `sequence-{流程}.md` |

注意：这类文件不是默认长期落点。优先仍是 `feature-*` / `reference-*` / `OVERVIEW.md`。

## 来自 project-docs-workflow 的调用约定

如果本技能由 `project-docs-workflow` 升级调用，调用方应尽量提供：
- 当前分析目标
- 当前执行模式：`analysis-only` / `docs-patch` / `standalone-report`
- 候选文档路径（如 `docs/feature-xxx.md`、`docs/reference-xxx.md`）
- 是否已经确认需要 patch docs
- 是否要求输出可直接合并到现有文档的 section 草稿

收到这些信息时，本技能应：
- 优先复用调用方给出的候选文档
- 避免重复做 docs 扫描
- 优先产出可回填 section，而不是重新发明完整文档结构

## 参考文件

- 架构分析详细步骤：`references/mode-architecture.md`
- 数据流 / 时序分析详细步骤：`references/mode-dataflow.md`
- 输出规范与落点优先级：`references/output-spec.md`
- Mermaid 图表模板：`references/mermaid-templates.md`
