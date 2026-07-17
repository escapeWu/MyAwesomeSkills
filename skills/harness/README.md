# Harness Bundle：`AGENTS.md` Patch 合同

本目录是可复用 harness skills 的规范来源。把 bundle 安装到目标仓库的
`.agents/skills/harness/` 后，Agent 必须按本文**增量 patch** 根 `AGENTS.md`，使文档路由、
真值所有权、实施门禁和大文件拆分规则在每轮任务中可见。

## Patch 原则

1. 先读取目标仓库现有的根 `AGENTS.md`、适用的嵌套 `AGENTS.md`、`CLAUDE.md`、
   `docs/OVERVIEW.md` 和相关索引；现有安全、授权、代码所有权、验证命令和项目特定规则必须保留。
2. 只做 section 级合并，不整篇替换，不把 demo 项目名、占位符或本仓库业务规则复制到目标仓库。
3. 若目标仓库已有等价章节，更新原章节；没有时才追加下方 managed block。后续运行只更新同一
   block，不能制造第二套规则。
4. 只有实际存在于 `.agents/skills/harness/` 的 skill 才能注册到 `AGENTS.md`。
5. 若 `docs/OVERVIEW.md` 或索引尚不存在，先从
   `document-organization-harness/assets/demo-harness/` 复制并按目标仓库事实改造，再写入链接。
6. 本 harness 不创建活跃 `taskBoard` / `.agents/tasks` 控制面，也不默认要求 SubAgent、并行派发、
   worktree、训练或任何执行授权。临时顺序留在会话计划；委派必须由用户明确授权。

## 合并位置

| 现有 `AGENTS.md` 章节 | 合并内容 |
|---|---|
| Documentation / Context | 渐进式披露、真值所有权、写回规则 |
| Development Workflow | Mandatory Execution Gate、Anti-Drift |
| Code Organization | 模块 owner、依赖方向、800/1000 行门禁 |
| Skills | 仅注册实际安装的 harness skills |
| Delegation / Worktrees | 明确“用户授权后才允许” |
| Testing | 保留项目原命令，补充从聚焦到广泛的验证顺序 |

## 无等价章节时追加的 Managed Block

把下方内容追加到根 `AGENTS.md`，并把不适用于目标仓库的条件项删掉。不得保留占位符或无效路径。

```md
<!-- HARNESS-GOVERNANCE:START -->
## Harness 文档与实施门禁

### 上下文与渐进式披露

- 项目上下文入口：[`docs/OVERVIEW.md`](docs/OVERVIEW.md)。
- 按 `AGENTS.md -> docs/OVERVIEW.md -> feature/reference/collaboration/archive INDEX -> 1-3 个任务相关 leaf` 逐层读取；禁止全量读取 `docs/`。
- `requirements.md` 持有 expected behavior 与 acceptance；当前代码持有 implemented behavior；不可变 artifact、ledger 和 gate report 持有 evidence。
- owning README/GOAL 持有 current state、completed、pending、blockers 和 next validation gate；会话计划只持有本轮临时顺序。
- 外部 proposal 只提供 provenance/recommendation，先完成内部采纳与合同转译，不能直接作为实现合同或授权。

### Mandatory Execution Gate

非 trivial 实施前按顺序完成：

1. 定位 owning module、requirements、README/GOAL、稳定 reference 和当前代码入口。
2. 冻结安全与授权边界、schema、公共接口、依赖方向、可变状态 owner、文件预算、测试归属和 validation matrix。
3. 把 durable completed/pending/blockers/next gate 写回唯一 owning README/GOAL；临时执行顺序只放会话计划。
4. 确认当前动作直接推进 active goal，且没有从开发状态、代码存在或实验结果推导出额外执行授权。
5. 在声明边界内实施，保留无关修改；先跑聚焦验证，再跑影响范围支持的广泛检查。
6. 验证通过后同步 owning docs、索引、changelog 和声明的 append-only evidence；没有实质影响时不要制造形式化文档改动。

禁止把 `taskBoard`、`.agents/tasks` 或其他平行进度文件作为活跃控制面。禁止在用户未明确要求时委派 SubAgent 或强制并行开发。

### Code Organization Gate

- CLI、adapter、strategy、model 和 runner 保持薄入口；domain、state、I/O、reporting 和 orchestration 各有明确 owner。
- 新增或本轮修改的手写代码文件不得超过 1000 物理行；达到 800 行时必须进行职责拆分评审。
- 按稳定责任与公共接口拆分，不创建 numbered `part` 文件，也不建立无边界 `utils/common/helpers`。
- 触发拆分时使用 `.agents/skills/harness/refactor-large-modules`，先冻结公共契约和行为基线，再按叶子优先迁移并验证等价性。

### Repo-local Harness Skills

- `.agents/skills/harness/document-organization-harness`：建立或修复 AGENTS、docs 路由、所有权和治理规则。
- `.agents/skills/harness/progressive-disclosure-docs`：审计渐进式披露、真值所有权、Feature 生命周期和主线路由。
- `.agents/skills/harness/project-analysis`：在 shallow docs 不足时分析架构、数据流、路线影响和 expected-vs-implemented gap。
- `.agents/skills/harness/project-docs-workflow`：编排非 trivial 开发前后的 owning docs、路线、状态和证据写回。
- `.agents/skills/harness/external-collaboration-workflow`：管理外部问题包、方案 provenance、逐项采纳和内部合同转译。
- `.agents/skills/harness/refactor-large-modules`：在保持行为与公共契约的前提下拆分大文件或混合职责模块。
<!-- HARNESS-GOVERNANCE:END -->
```

## Patch 后验证

Agent 在结束前必须确认：

- `git diff -- AGENTS.md` 只包含预期的增量合并，原有安全、授权、所有权和测试规则未丢失；
- managed block 最多一个，已有等价章节没有被重复创建；
- `docs/OVERVIEW.md`、各 INDEX 和注册的 skill 路径真实存在，链接可从上到下到达并能反向返回；
- `AGENTS.md` 不把 taskboard、SubAgent、并行派发、worktree、训练或执行权限设为默认要求；
- 详细流程仍留在 skill/reference 中，根 `AGENTS.md` 只保留稳定规则、路由和硬门禁；
- 若目标仓库使用 `.cursor/rules/harness-execution.mdc`，其 contract、validation、docs write-back
  和 delegation boundary 与 `AGENTS.md` 一致；
- 使用目标仓库已有的 docs、链接、lint 和测试验证命令；不要凭空发明项目命令。

## 相关入口

- Bundle 清单：[`document-organization-harness/assets/harness-bundle.json`](document-organization-harness/assets/harness-bundle.json)
- 安装与脚手架参考：[`document-organization-harness/references/harness-bootstrap.md`](document-organization-harness/references/harness-bootstrap.md)
- 可复制 demo：[`document-organization-harness/assets/demo-harness/`](document-organization-harness/assets/demo-harness/)
