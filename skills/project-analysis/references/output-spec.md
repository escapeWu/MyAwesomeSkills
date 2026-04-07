# 输出规范与文档模板

## 文档结构

所有输出文档采用 **YAML Frontmatter Metadata + Markdown Content** 的两段式结构。

### Metadata 规范

文档头部必须包含 YAML frontmatter，用于文档检索和去重判断：

```yaml
---
type: architecture | dataflow | sequence  # 分析类型
scope: full | module                       # 分析范围：全项目 / 模块级
module: ""                                 # 模块名（scope=module 时必填）
date: "YYYY-MM-DD"                         # 生成日期
keywords:                                  # 关键词列表，用于相似性匹配
  - keyword1
  - keyword2
tech_stack:                                # 识别到的技术栈
  - tech1
  - tech2
entry_point: ""                            # 入口点（数据流分析时填写）
---
```

**字段说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | 分析类型：`architecture`（架构）、`dataflow`（数据流）、`sequence`（时序图） |
| `scope` | 是 | 分析范围：`full`（全项目）、`module`（模块级） |
| `module` | 条件 | 当 scope=module 时必填，模块名称 |
| `date` | 是 | 文档生成日期 |
| `keywords` | 是 | 关键词列表，描述分析内容的核心主题，用于后续相似性匹配 |
| `tech_stack` | 否 | 项目涉及的技术栈 |
| `entry_point` | 否 | 数据流分析时的入口点路径 |

---

## 架构分析报告模板

```markdown
---
type: architecture
scope: full
module: ""
date: "YYYY-MM-DD"
keywords:
  - 系统架构
  - 项目名称
tech_stack:
  - React
  - Node.js
---

# 项目架构文档

> 生成时间：YYYY-MM-DD
> 分析范围：全项目

## 项目概述
- 项目名称
- 技术栈
- 项目类型

## 目录结构
- 主要目录说明

## 架构图

[Mermaid 图]

必须紧跟对应的 TUI ASCII 预览图，便于在终端中快速查看结构关系并审查 Mermaid 内容

## 核心模块说明

| 模块名称 | 职责 | 依赖 |
|---------|------|------|
| ... | ... | ... |

## 外部依赖
- 数据库
- 第三方服务
```

---

## 数据流分析报告模板

```markdown
---
type: dataflow
scope: module
module: "模块名称"
date: "YYYY-MM-DD"
keywords:
  - 数据流
  - 模块名称
  - 功能描述
entry_point: "src/path/to/entry.ts"
---

# {模块名} 数据流分析

> 生成时间：YYYY-MM-DD
> 分析模块：{模块路径}

## 分析目标
- 功能/模块名称
- 入口点

## 时序图

[Mermaid 时序图]

必须紧跟对应的 TUI ASCII 预览图，便于在终端中快速查看主流程并审查 Mermaid 内容

## 数据流图

[Mermaid 流程图]

必须紧跟对应的 TUI ASCII 预览图，便于在终端中快速查看数据流向并审查 Mermaid 内容

## 关键节点说明

| 节点 | 文件位置 | 数据变换 |
|-----|---------|---------|
| ... | ... | ... |

## 数据模型
- 输入结构
- 输出结构
```

---

## 文件命名规范

| 分析类型 | 文件名格式 | 示例 |
|---------|-----------|------|
| 系统架构 | `architecture.md` | `docs/architecture.md` |
| 模块架构 | `architecture-{模块}.md` | `docs/architecture-auth.md` |
| 数据流 | `dataflow-{功能}.md` | `docs/dataflow-login.md` |
| 时序图 | `sequence-{流程}.md` | `docs/sequence-order-create.md` |

---

## 文档输出流程

1. **运行 metadata 扫描**（前置检查已完成时跳过此步）
2. **检查 docs 目录**
   - 如果 `docs/` 目录不存在，创建该目录
3. **写入文档**
   - 使用 Write 工具将分析报告写入目标文件
   - 文档必须包含完整的 YAML frontmatter metadata
4. **生成 TUI ASCII 预览图**
   - 每张 Mermaid 图后都必须紧跟一张语义一致的 ASCII/TUI 预览图
5. **确认输出**
   - 告知用户文档已保存的路径

## 最佳实践

- 优先使用项目已有的文档（README、API 文档）作为参考
- 架构图保持简洁，避免过于细节
- 时序图聚焦主流程，分支逻辑可单独说明
- 所有图表使用中文标注
- 为每个模块提供简短的职责说明
- 分析完成后始终将结果保存到 `docs/` 目录
- 更新现有文档时保留历史版本或做增量更新
- **keywords 字段务必准确填写**，这是后续文档去重和相似性匹配的核心依据
