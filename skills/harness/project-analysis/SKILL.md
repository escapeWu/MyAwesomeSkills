---
name: project-analysis
description: 深度项目分析工具。用于在现有 docs 不足、代码链路复杂、harness M0/M1 需要补足 TaskNode 输入上下文、或需要梳理系统架构、模块数据流、时序、性能风险时进行只读取证和结构化分析。常与 `project-docs-workflow`、`harness-engineering-plan` 配套使用；也可在用户明确要求架构分析、数据流分析、时序图、调用链梳理或性能排查时直接使用。默认应落文档：优先更新或新建 `docs/` 下合适长期文档，不停留在仅终端输出的 analysis-only 模式。
---

# 项目分析技能

本技能是项目的**深度分析层**。

它不负责每次开发前后的通用 docs 编排；那由 `project-docs-workflow` 负责。它的职责是：在现有文档不足、链路复杂或用户明确需要时，做只读取证、调用链梳理、图表整理和性能观察，并把结果整理进项目文档。

**默认行为：更新或创建 docs。** 不再使用 `analysis-only`。当用户没有明确指定时，先沿 `docs/OVERVIEW.md -> docs/feature/INDEX.md / docs/reference/INDEX.md -> 相关 README/INDEX/leaf` 判断是否存在合适承接文档：能承接则 `update-doc`，不能承接才 `new-doc`。

**强制要求：凡是输出 Mermaid 图表，必须在同一位置紧跟对应的 ASCII/TUI 预览图，方便用户在终端和代码评审中直接审查结构。不得省略，不得标记为可选。**

## 分析主题

本技能可用于以下分析主题：
- `architecture`：系统架构、模块边界、依赖关系、外部服务
- `dataflow`：模块数据流、调用链、关键数据变换、外部 I/O
- `sequence`：主流程时序、跨层交互、关键分支
- `performance-risk`：性能热点、放大点、瓶颈候选、风险链路

## 执行模式

仅保留两种落点结果，且**默认优先写文档**。默认选择逻辑是 `auto`：先判断 `update-doc` 是否可行；不可行时再落为 `new-doc`。

### 模式 A：update-doc（默认优先）
当已有 `docs/feature/<category>/README.md`、子模块 `README.md` / `INDEX.md`、`docs/reference/*.md` 或 `docs/OVERVIEW.md` 能承接本次分析结果时使用。

适用场景：
- 已存在相关文档，只是内容过期、缺失或不准确
- 用户明确要求“更新 docs”“补充到现有文档”“回填文档”
- 由 `project-docs-workflow` / `harness-engineering-plan` 升级调用并提供候选文档路径

输出：
- 基于现有长期文档的增量更新
- 保留仍然正确的内容
- 仅更新过期、缺失或不准确的部分

### 模式 B：new-doc
当分析结果适合沉淀为一篇新的长期文档，且没有合适现有文档可承接时使用。

适用场景：
- 当前 `docs/` 中没有合适文档可承接
- 需要形成独立、可长期维护的架构 / 数据流 / 时序 / 风险文档
- 用户明确要求“新建文档”“补一篇文档”“单独整理成文档”

输出：
- 新建文档（优先落到 `docs/feature/<category>/<module>/...` 或 `docs/reference/...`）
- 结构化结论
- 证据路径
- Mermaid 图 + ASCII/TUI 预览图
- 可长期维护的 section 结构
- 父级 INDEX/README 路由项与 leaf 顶部“上级”反向链接

模式选择规则：
- **默认先判断 `update-doc` 是否可行**：若存在合适承接文档，优先更新而不是平行新建
- 若没有合适文档，转为 `new-doc`
- 不再允许 `analysis-only`
- 不再使用 `standalone-report` 作为独立模式；用户若要求独立报告，按 `new-doc` 处理并创建合适的新文档

## 标准执行 SOP

### 1. 理解需求并检查项目 docs

先明确：
- 用户要的是 `architecture` / `dataflow` / `sequence` / `performance-risk` 哪类分析
- 分析范围：全项目 / 模块级
- 目标模块、入口点、关键功能点
- 当前执行模式：`new-doc` / `update-doc`

优先按渐进式披露检查：
- `docs/OVERVIEW.md`
- `docs/feature/INDEX.md`，再进入相关分类 `README.md`、子模块 `README.md` / `INDEX.md`
- `docs/reference/INDEX.md`，再进入相关 reference 文件
- 调用方提供的候选文档路径

如果调用方（如 `project-docs-workflow` 或 `harness-engineering-plan`）已经提供候选文档路径，优先读取这些文档；如果没有，再按 INDEX 路由定位候选文档。禁止全量读取 `docs/`。

这些文档只能作为**半可信上下文**：
- 可用于快速建立模块心智模型
- 但必须继续以当前代码核实
- 文档与代码冲突时，以代码为准

进入分析后，**必须在写文档前完成模式判断**：
- 如果已有合适文档可承接，使用 `update-doc`
- 如果没有合适文档，使用 `new-doc`
- 不再停留在只输出终端结论而不写文件的状态

如 `docs/` 中存在旧式分析文档、frontmatter 元数据或需要做补充检索，可选使用 metadata 扫描脚本作为辅助：

```bash
python3 <skills-root>/skills/project-analysis/scripts/scan_docs_metadata.py <项目根目录>/docs
```

它不是主判断依据。主判断依据应是：
- `docs/OVERVIEW.md`
- `docs/feature/INDEX.md` 与相关分类 / 子模块文档
- `docs/reference/INDEX.md` 与相关 reference 文件
- 当前代码

### 2. 拆解子任务

在正式读代码前，先把分析拆成 2-4 个**边界清晰、只读、可并行**的子任务。

拆分原则：
- 每个子任务只负责一类证据收集，不直接写最终文档
- 子任务之间尽量不要共享上下文，避免重复搜索
- 主 agent 负责最终判断、冲突消解、图表整理、文档落点选择与最终写入

推荐拆分方式：
- **系统架构分析**：技术栈与入口点 / 目录与模块边界 / 依赖关系、外部服务与性能风险
- **模块数据流分析**：入口点定位 / 调用链与关键节点 / 数据模型、外部 I/O 与放大点
- **时序或性能排查**：主流程 / 分支与异常路径 / 热点候选与观察结论

### 3. 子任务并行取证

优先把子任务设计成可并行的只读取证单元。只有在当前工具环境允许、且用户或调用方明确授权并行 agent 时，才启动 SubAgent；否则由主 agent 使用 `rg` / `rg --files` / `sed` / `nl` 等本地工具完成同样的取证。

执行要求：
- 优先做只读工作：Glob、Grep、Read、依赖梳理、调用链追踪、模块职责归纳
- 一次并行 2-4 个子任务即可，只并行真正独立的分析
- 如使用 subagent，每个 prompt 必须写清：分析目标、目标目录/文件/关键词、要返回的结构化结果
- subagent **不要**直接写最终文档，只返回事实、路径、调用链、关键结论、可疑缺口、风险点
- 主 agent **不要**和 subagent 重复执行同样的检索；若未使用 subagent，也要避免重复扫描

### 4. 汇总子任务信息并整理结果

主 agent 汇总各取证单元的结果后，再统一形成分析输出。

主 agent 负责：
- 合并并去重各子任务结论
- 解决冲突信息，必要时补充定向查证
- 产出结构化分析结论
- 生成 Mermaid 图表和对应 ASCII/TUI 预览图
- 如由 harness 调用，生成可直接放入 TaskNode `Input Context` 的摘要：入口点、相关文件、契约、风险、验证建议
- 将结果整理并写入目标文档（新建或更新）
- 维护必要的文档结构，如 frontmatter、section、Changelog 与入口索引

### 5. Review 与写入

写入前至少检查：
- 目标文档是否选对（`docs/feature/<category>/<module>/...` / `docs/reference/...` / `docs/OVERVIEW.md`）
- 若为更新，是否保留了仍然正确的旧内容
- 若为新建，是否真的没有更合适的现有文档可承接
- 若为新建，父级 `INDEX.md` / `README.md` 是否已添加路由项，leaf 顶部是否有 `> 上级：...` 反向链接
- 是否避免了 3 层及以上深 `../` 链接，跨层资源改用 `/docs/...`、`/sandbox/...` 等项目根路径
- 新增结论是否能回溯到文件路径、模块、入口点或调用链
- Mermaid 与 ASCII/TUI 预览图语义一致
- 是否需要同步更新该文档的 Changelog
- 如果是新增模块，是否需要同步更新 `docs/OVERVIEW.md`
- 如果本次形成新的稳定踩坑经验，是否应提示调用方考虑补充“历史教训”或规则文档

如发现更适合沉淀到规则层的经验，只负责识别并提示调用方；**不要默认直接修改 `AGENTS.md` / `CLAUDE.md`**。

### 6. 向用户汇报分析结果

完成后，向用户汇报：
- 当前执行模式
- 输出类型：新建文档 / 更新文档
- 包含哪些图表（架构图、时序图、数据流图等）
- 2-4 条关键发现概览
- 如有未覆盖边界、风险点或建议追加分析，也一并说明
- 文档保存路径，以及本次属于 `new` 还是 `update`

## 文档落点优先级

默认优先维护这一套长期项目文档：

1. `docs/feature/<category>/README.md`
2. `docs/feature/<category>/<module>/README.md` 或 `INDEX.md`
3. `docs/reference/*.md`
4. `docs/OVERVIEW.md`

优先规则：
- 功能行为、模块实现、数据模型、测试方式、变更记录，优先回填 `docs/feature/<category>/...`
- 接口契约、外部系统、第三方 API、架构参考、限制条件，优先回填 `docs/reference/...`
- 新增模块、模块边界、文档索引入口，更新 `docs/OVERVIEW.md`

仅在下列情况才生成独立分析文档：
- 当前项目中没有合适的长期文档可承接
- 用户明确要求单独成文
- 分析结果本身具备独立维护价值，且不适合硬塞进现有文档

注意：独立文档仍属于 `new-doc`，不是单独的第三种执行模式。

## 独立分析文档命名（仅例外使用）

| 分析类型 | 文件名格式 |
|---------|-----------|
| 系统架构 | `architecture.md` |
| 数据流 | `dataflow-{功能}.md` |
| 时序图 | `sequence-{流程}.md` |

注意：这类文件不是默认长期落点。优先仍是 `docs/feature/<category>/...` / `docs/reference/...` / `docs/OVERVIEW.md`。

## 来自 project-docs-workflow 的调用约定

如果本技能由 `project-docs-workflow` 升级调用，调用方应尽量提供：
- 当前分析目标
- 当前落点偏好：`auto` / `update-doc` / `new-doc`
- 候选文档路径（如 `docs/feature/<category>/README.md`、`docs/reference/architecture.md`）
- 是否已经有明确落点
- 是否要求输出可直接合并到现有文档的完整 section / patch

收到这些信息时，本技能应：
- 优先复用调用方给出的候选文档
- 避免重复做 docs 扫描
- 优先产出可回填 section，而不是重新发明完整文档结构

## 来自 harness-engineering-plan 的调用约定

如果本技能由 `harness-engineering-plan` 在 M0 / M1 调用，调用方应尽量提供：
- 当前 milestone / TaskNode 或待规划 feature 名称
- `taskBoard.md` / `tasks.md` / design / spec 候选路径
- 需要补足的缺口：架构边界、数据流、时序、性能风险、contract 命名或验证证据
- 期望产出是否要被 TaskNode `Input Context` 直接引用

收到这些信息时，本技能应：
- 优先服务 M0 planning gate：补足 TaskNode 拆分所需的代码事实、文档落点、风险边界和验证建议
- 输出一个 **TaskNode-ready Context** section，包含 `Entry Points`、`Relevant Files`、`Contracts / Data Shapes`、`Risks / Open Questions`、`Validation Candidates`
- 只负责分析和文档沉淀；不直接生成完整 taskBoard，除非用户同时明确要求使用 `harness-engineering-plan`
- 若分析产生新 leaf 文档，确保从 `docs/OVERVIEW.md` 沿 INDEX/README 可达，并在 leaf 顶部加入上级链接

## 参考文件

- 架构分析详细步骤：`references/mode-architecture.md`
- 数据流 / 时序分析详细步骤：`references/mode-dataflow.md`
- 输出规范与落点优先级：`references/output-spec.md`
- Mermaid 图表模板：`references/mermaid-templates.md`
