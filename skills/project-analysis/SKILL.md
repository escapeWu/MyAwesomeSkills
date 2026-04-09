---
name: project-analysis
description: 项目分析工具，用于分析代码库的系统架构和模块数据流。当用户需要理解项目结构、生成架构图、分析模块间的数据流向、生成时序图时使用此技能。支持输出 Mermaid 语法的可视化图表。适用场景：(1) 项目架构梳理 (2) 模块依赖分析 (3) 数据流追踪 (4) 新成员项目入门 (5) 技术文档生成
---

# 项目分析技能

本技能用于在代码库中生成系统架构、模块架构、数据流与时序图报告。执行时遵循固定 SOP：先检查是否已有高相似度文档，再拆解子任务，使用并行 SubAgent 收集证据，最后由主 agent 汇总、review、patch 并输出报告。

**强制要求：凡是输出 Mermaid 图表，必须在同一位置紧跟对应的 ASCII/TUI 预览图，方便用户在终端和代码评审中直接审查结构。不得省略，不得标记为可选。**

## 标准执行 SOP

### 1. 理解用户需求并检查已有文档

**在执行任何分析之前，必须先执行此步骤。**

先明确以下信息：
- 用户要的分析类型：`architecture` / `dataflow` / `sequence`
- 分析范围：全项目 / 模块级
- 目标模块、入口点、关键功能点
- 用户是否希望生成新文档，还是更新已有文档

然后使用 metadata 扫描脚本检查目标项目的 `docs/` 目录：

```bash
python3 <skills-root>/skills/project-analysis/scripts/scan_docs_metadata.py <项目根目录>/docs
```

脚本会输出 JSON 格式的文档列表，包含每份文档的 metadata（type、scope、module、keywords、date）和内容摘要。

对照用户请求与已有文档，重点判断：
- **类型匹配**：分析类型是否一致
- **范围匹配**：分析范围和目标模块是否一致
- **关键词匹配**：需求关键词是否与 `keywords` 高度重叠

如果发现与用户请求**高度相似**的已有文档，**必须暂停分析任务**，使用 AskUserQuestion 向用户提问，并提供以下三种选择：

- **Patch（Recommended）**：基于现有文档增量修补，保留仍然正确的内容，仅更新缺失、过期或不准确的部分
- **Overwrite**：重新完整生成并覆盖旧文档
- **Cancel**：停止本次分析，沿用现有文档

提问内容必须包含：
1. 已有文档的文件路径
2. 已有文档的类型 / 范围 / 模块
3. 已有文档的生成日期
4. 已有文档的简要概述
5. `patch / overwrite / cancel` 三选一

只有当用户明确选择 **patch** 或 **overwrite** 后，才进入后续分析步骤。

如果 `docs/` 目录不存在或无相似文档，直接进入下一步。

### 2. 拆解子任务

在正式读代码前，先把分析拆成 2-4 个**边界清晰、只读、可并行**的子任务。

拆分原则：
- 每个子任务只负责一类证据收集，不直接写最终文档
- 子任务之间尽量不要共享上下文，避免重复搜索
- 主 agent 负责最终判断、冲突消解、图表整理和文档写入

推荐拆分方式：
- **系统架构分析**：技术栈与入口点 / 目录与模块边界 / 依赖关系与外部服务
- **模块数据流分析**：入口点定位 / 调用链与关键节点 / 数据模型与外部 I/O

### 3. 子任务下发 SubAgent 并行实施

使用 Agent 工具启动 SubAgent（可理解为 task）并行执行子任务。

执行要求：
- 优先让 subagent 做只读工作：Glob、Grep、Read、依赖梳理、调用链追踪、模块职责归纳
- 一次并行 2-4 个子任务即可，只并行真正独立的分析
- 每个 subagent 的 prompt 必须写清：分析目标、目标目录/文件/关键词、要返回的结构化结果
- subagent **不要**直接写最终分析文档，只返回事实、路径、调用链、关键结论、可疑缺口
- 主 agent **不要**和 subagent 重复执行同样的检索

### 4. 汇总子任务信息并整理报告

主 agent 汇总各 subagent 的结果后，再统一生成报告。

主 agent 负责：
- 合并并去重各子任务结论
- 解决冲突信息，必要时补充定向查证
- 生成 Markdown 报告正文
- 生成 Mermaid 图表和对应 ASCII/TUI 预览图
- 补齐 YAML frontmatter metadata
- 将结果写入 `docs/` 目录

### 5. Review 与 Patch

写入前必须做一次总 review，至少检查：
- frontmatter 字段完整且准确
- Mermaid 与 ASCII/TUI 预览图语义一致
- 关键结论能回溯到文件路径、模块、入口点或调用链
- 没有遗漏核心模块、关键链路或外部依赖
- 如果用户选择 **patch**，必须基于现有文档增量修补，而不是默认整篇重写
- 如果汇总后发现明显缺口，先 patch 草稿，再写最终文档

### 6. 向用户汇报生成的报告概览

保存后，必须向用户汇报：
- 文档已保存的完整路径
- 本次是 **新建 / patch / overwrite** 中的哪一种
- 报告包含哪些图表（架构图、时序图、数据流图等）
- 2-4 条关键发现概览
- 如仍有未覆盖边界或建议补充的后续分析，也一并说明

---

## 分析模式

### 模式一：系统架构分析

从宏观层面分析项目，生成整体架构视图。

> 详细分析步骤和推荐子任务拆分参考：`references/mode-architecture.md`

### 模式二：模块数据流分析

深入分析特定模块或功能的数据流转过程。

> 详细分析步骤和推荐子任务拆分参考：`references/mode-dataflow.md`

---

## 文档输出步骤

分析完成后，按以下步骤将结果保存到 `docs/` 目录。

### 步骤 1：确定输出文件路径

根据分析类型确定文件名（命名规范见 `references/output-spec.md`）：

| 分析类型 | 文件名 |
|---------|--------|
| 系统架构 | `docs/architecture.md` |
| 模块架构 | `docs/architecture-{模块}.md` |
| 数据流 | `docs/dataflow-{功能}.md` |
| 时序图 | `docs/sequence-{流程}.md` |

### 步骤 2：按用户选择写入文档

- **Patch**：读取并保留有效内容，增量更新过期或缺失部分，并刷新 metadata
- **Overwrite**：重新生成完整文档并覆盖目标文件
- **New**：没有相似文档时，直接生成新文档
- **Cancel**：停止，不写文件

文档必须采用两段式结构：

**第一段：YAML Frontmatter Metadata**

```yaml
---
type: architecture | dataflow | sequence
scope: full | module
module: ""          # scope=module 时必填
date: "YYYY-MM-DD"
keywords:
  - 关键词1
  - 关键词2
tech_stack:
  - 技术栈1
entry_point: ""     # 数据流分析时填写
---
```

**第二段：Markdown 正文**

按对应分析类型的报告模板填写（模板见 `references/output-spec.md`）。其中所有 Mermaid 图表后必须紧跟对应的 ASCII/TUI 预览图，作为审查用文本视图。

### 步骤 3：确认输出

告知用户：
- 文档已保存的完整路径
- 本次操作类型：新建 / patch / overwrite / cancel
- 报告概览与关键发现

---

## 参考文件

- 分析模式详细步骤：`references/mode-architecture.md`、`references/mode-dataflow.md`
- 文档模板与命名规范：`references/output-spec.md`
- Mermaid 图表模板：`references/mermaid-templates.md`
