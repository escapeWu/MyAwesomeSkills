# Harness Skills：轻量文档协作约定

本目录提供一组可独立采用的 harness skills。它们的目标是让 Agent 快速找到必要上下文、完成任务，
并在结束时维护少量长期文档，而不是把每次开发变成一套文档生命周期流程。

套件变化见 [`CHANGELOG.md`](CHANGELOG.md)，目标项目维护方式见
[`UPGRADING.md`](UPGRADING.md)。目标项目可以只采用真正需要的 skills，不要求完整安装。

## 核心原则

1. **快速进入任务**：先读项目规则，再按需读 1-3 份最相关文档和代码入口。不要全量扫描 `docs/`。
2. **文档不是前置产物**：实施前只读取和确认边界，不为了开工先创建计划、需求、Spec、状态表或日志。
3. **完成后异步写回**：代码与验证完成后，主 Agent 把一次核心 docs 更新交给边界明确的异步 SubAgent；不让附属文档维护阻塞主任务。
4. **单一 docs writer**：异步维护期间由一个 SubAgent 独占目标文档，主 Agent 不再并发修改同一批文件。
5. **只保存长期有用的信息**：会话计划、中间分析、原始输出和临时 checklist 留在会话或工具中。
6. **少问关键问题**：只有目标或硬边界无法可靠判断时才询问用户；可逆实现细节采用仓库惯例和合理默认。
7. **验证与风险匹配**：保留项目已有测试和检查，但 harness 不强制 TDD、测试先行或固定验证矩阵。
8. **不复制治理**：安全、授权、所有权和项目命令继续由目标仓库现有规则持有。

## 核心文档

按项目规模按需使用，不要求所有目录同时存在：

```text
AGENTS.md / CLAUDE.md            # 简短项目规则与上下文入口
docs/OVERVIEW.md                # 项目地图；项目足够复杂时创建
docs/feature/INDEX.md           # Feature 路由；有多个 Feature 时创建
docs/feature/<feature>/README.md # 目标、边界、当前行为、关键接口与状态
docs/reference/INDEX.md         # 稳定跨模块参考的路由；有多份 reference 时创建
docs/reference/*.md             # 架构、接口、运行方式等稳定知识
```

`docs/collaboration/`、`docs/archive/` 和更细的设计文档只在真实需求出现时创建。不要因为模板存在
就预建目录。

## `AGENTS.md` 增量 Patch

先读取目标仓库现有 `AGENTS.md`、`CLAUDE.md` 和文档入口。保留已有安全、授权、所有权、测试命令
和项目规则；只在缺少等价说明时补一个短小章节。示例：

```md
<!-- HARNESS-DOCS:START -->
## 项目上下文与文档维护

- 项目上下文入口：[`docs/OVERVIEW.md`](docs/OVERVIEW.md)。
- 按 `OVERVIEW -> INDEX -> 1-3 份任务相关文档` 逐层读取，不全量读取 `docs/`。
- 开始任务前只读取上下文；不要为了开工创建 Spec、计划、状态表或进度日志。
- 先完成实现和风险匹配的验证，再由主 Agent 异步委派一个 SubAgent，用一轮增量 patch 更新真正受影响的核心 docs。
- docs SubAgent 是该轮唯一文档 writer；主 Agent 不等待附属维护，也不并发修改同一批 docs。
- 临时顺序、中间分析和工具输出留在会话中，不写入长期文档。
- 只有目标或安全、授权、兼容等硬边界无法判断时才询问用户；其余细节沿用仓库惯例。
<!-- HARNESS-DOCS:END -->
```

若 `docs/OVERVIEW.md` 不存在且项目规模不需要它，删除该入口，不要为了符合模板创建空目录。

## Repo-local Skills

- `add-idea`：把想法路由到现有或新的 Feature 文档，只澄清最关键的未知项。
- `document-organization-harness`：建立或修复最小可用的文档地图。
- `progressive-disclosure-docs`：审计和简化文档导航与长期知识边界。
- `project-docs-workflow`：读取任务上下文，并在任务完成后统一写回核心 docs。
- `project-analysis`：在浅层文档不足时分析架构、数据流、调用链或实现差异。
- `external-collaboration-workflow`：需要外部团队协作时保存来源与采纳记录。
- `docs-issue-sync`：在 GitHub Issue 开发收尾前，把已交付行为同步为模块功能事实，并保留 Issue/PR 来源和代码查询线索。
- `github-issue-development`：统一 Issue-to-PR 开发链路、授权边界、精确基线、docs sync 和 PR 等待收尾。
- `refactor-large-modules`：按稳定职责拆分过大或混合职责模块。

每个 skill 都可独立采用。只注册目标仓库真实存在且愿意维护的路径。

## 完成前检查

- 没有覆盖目标仓库原有规则或用户修改。
- Agent 能从入口到达相关 Feature 或 reference，不需要读取整棵文档树。
- 没有新增任务板、阶段日志、重复状态页或仅服务本轮任务的文档。
- 文档只在任务完成后由一个异步 docs SubAgent 更新了一轮，且只包含长期有效的变化。
- 若环境没有 SubAgent，主 Agent 才在最后做同样的一次轻量 patch。
- 路径和链接真实存在；验证使用目标项目已有命令。
