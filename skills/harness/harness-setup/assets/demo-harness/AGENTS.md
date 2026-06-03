# Agent 开发规约

> 项目上下文入口：[`docs/OVERVIEW.md`](docs/OVERVIEW.md)

开始任何重要开发前，先读 [`docs/OVERVIEW.md`](docs/OVERVIEW.md)。本仓库是一个 Java 多模块后端项目，采用 docs-first、结构化契约、分层清晰、测试可执行的 harness 工作方式。禁止把密钥、凭证、私有运行时数据或任何敏感内容写入 docs、日志或用户可见输出。

## 核心原则

- **Docs-first**：新增模块、接口或执行方式前，先更新 `docs/feature/` 或 `docs/reference/` 的索引与说明。
- **单一事实来源（SSOT）**：每条稳定规则只保留一个 owner，不在多个模块里重复描述。
- **结构化契约**：API、配置、脚本、目录与测试命名都优先使用明确的结构化约定。
- **分层不反向**：控制层保持薄，编排放在服务层，底层模块不反向依赖上层。
- **真实路径验证**：新增或修改能力必须留下可验证证据，不能只停留在推断或 mock。

## 分层约束

**Backend**: `model -> mapper -> service -> api -> boot`

- `hisense-hr-api/src/main/java/com/mega/hr/<module>/api/` 只做 HTTP 入参、出参和接线。
- `hisense-hr-api/src/main/java/com/mega/hr/<module>/service/` 承载业务编排和可测试逻辑。
- `hisense-hr-api/src/main/java/com/mega/hr/<module>/mapper/` 承载持久化访问。
- `hisense-hr-api/src/main/java/com/mega/hr/<module>/model/` 承载 `po/bo/bpo/dto/param` 等契约对象。
- `hisense-hr-boot/src/main/java/com/mega/` 承载启动入口与运行装配。

## 代码组织约束

新增功能模块、修复跨文件 bug、重构、增加 API / 配置 / 脚本前，先使用 `.agents/skills/harness/code-organization-harness` 判断模块边界、文件落点与上下文 grep 路径。

- **按领域归属优先**：先找 owning module，再按 layer 放文件；不要因为"能复用"就提前放进 `common` / `utils` / 全局层。
- **先 grep 后新建**：按 endpoint、schema、表名、文案、配置键、domain noun 搜索现有 owner；只有现有模块没有清晰归属时才新建模块。
- **文件与测试镜像**：后端 API / service / mapper / model 的测试应与其验证层级保持对应。
- **框架细则进 skill**：Java / Maven / Spring 风格的具体文件组织与最佳实践，统一由 `code-organization-harness` 的 references 承接。

## 文档渐进式披露规则

文档遵循渐进式披露（Progressive Disclosure），Agent 逐层深入、禁止全量读取：

```text
Level 0: AGENTS.md            → 项目开发规约与读取入口
Level 1: docs/OVERVIEW.md     → 项目地图与活动模块
Level 2F: docs/feature/INDEX.md  → 功能模块索引，先选目标模块
Level 2R: docs/reference/INDEX.md → 架构 / 接口 / 测试等稳定参考
Level 2A: docs/archive/INDEX.md   → 已完成计划 / 历史归档，默认不读
Level 3: docs/feature/<module>/  → 模块 README / INDEX，按任务进入
Level 4: 具体设计 / RCA，仅按需读取

(执行层: .agents/skills/harness/harness-engineering-plan/tasks/<module>/taskBoard.md → WIP 控制平面)
```

**Agent 读取规则**：`OVERVIEW.md -> feature/reference INDEX -> 按需读 1-3 个相关文档`。禁止全量读取 `docs/`。`taskBoard.md` 是执行上下文，只在继续实现、监督、验收或审计历史时读取。

### 强制：双向可追溯（Top-Down / Bottom-Up）

任何 docs 维护行为（新增 / 改动 / 删除）必须保证：

1. **Top-Down 可达**：从 `AGENTS.md` 出发，沿 OVERVIEW → INDEX → 子 INDEX → leaf 一路下钻，每一步都能找到下一层入口链接。
2. **Bottom-Up 可溯**：每个 leaf 文档顶部必须有类似 `> 上级：../README.md` 的反向引用，能一路向上回到 AGENTS.md。
3. **新需求 context 发现**：开发任何新需求时，agent 必须能从 `AGENTS.md` 开始，仅用渐进式披露规则就发现待开发清单（`taskBoard.md`）和设计依据（如需要）。如果做不到，立即修补 docs 链路：
   - 在缺失环节的父 INDEX 加路由表项；
   - 在新建文件顶部加上级链接；
   - 在子模块 INDEX 同步登记。
4. **失败模式自检**：每次改 docs 前，先问自己"如果我清空记忆，从 AGENTS.md 出发能不能找到这个文件？" 答否即修。
5. **路径书写约定（项目根目录优先）**：跨多层目录的链接（即 ≥ 3 个连续 `../`）必须改用项目根目录起始的路径，前缀 `/`。

## 文档写入规则

- 新增功能优先归入已有 `docs/feature/<module>/`；没有合适模块时再新建目录。
- 大型模块使用 `INDEX.md` 或 `README.md` 作为模块地图，详细设计、数据流、RCA 放子文件。
- taskBoard 不放在 docs/ 下。执行过程文件统一存放在 `.agents/skills/harness/harness-engineering-plan/tasks/<module>/taskBoard.md`。
- 中小型模块使用 `README.md`，必要时补少量子文件。
- 历史计划、一次性总结、旧执行记录进入 `docs/archive/`，并同步更新 `docs/archive/INDEX.md`。
- 新增或变更模块时，同步更新 `docs/feature/INDEX.md` 与 `docs/OVERVIEW.md`。
- 修改接口或契约时同步更新 `docs/reference/interfaces.md`。
- 修改运行、测试、验证方式时同步更新 `docs/reference/runbook-testing.md`。
- 保持每层信息密度一致：`OVERVIEW.md` 是地图，`INDEX.md` 是路由，模块文档放细节。

## 项目内置 skills

- `.agents/skills/harness/code-organization-harness`：新增功能模块、修 bug、重构、增加 API 前使用；帮助 Agent 先按模块和领域 grep 上下文，再按项目约定创建文件、放置测试与同步契约。
- `.agents/skills/harness/project-analysis`：当现有 docs 不足、链路复杂，或需要架构 / 数据流 / 风险分析时使用；分析结果应沉淀到 `docs/`。
- `.agents/skills/harness/project-docs-workflow`：非 trivial 的功能开发、bug 修复、重构、接口变更前后，先用它扫描 docs 并判断文档影响。
- `.agents/skills/harness/harness-engineering-plan`：多 Wave、多 TaskNode 的功能开发必须先用它生成 `taskBoard.md`，作为该 milestone 唯一执行控制平面。

> **强制规则**：开始任何新 milestone（≥ 2 wave 或 ≥ 5 TaskNode）的功能开发前，agent 必须用 `harness-engineering-plan` 生成 `taskBoard.md` 并在推进期间实时更新；wave 内相互独立的 ready TaskNode 必须并行派发给多个实施 agent（见下方「强制执行流程门」）。仅修文档 / 单条 bug fix 等 trivial 改动不在此约束。

## 强制执行流程门（Mandatory Execution Gate）

非 trivial 的「实现 / 修改 / 开发 / 修复」类编码任务，**在写任何实现代码前**必须按顺序走完这道门，不能跳步：

1. **判定规模**：任务命中 ≥ 2 wave 或 ≥ 5 TaskNode、或跨多文件 / 多 owner / 需要分阶段验证 → 进入 harness 流程；单文件 trivial fix 豁免。
2. **拆任务 + 建 taskBoard**：用 `harness-engineering-plan` 把目标拆成 milestone / TaskNode / wave，落到 `.agents/skills/harness/harness-engineering-plan/tasks/<module>/taskBoard.md`，推进期间实时更新状态。**禁止跳过 taskBoard 直接埋头单线程把多步任务写完。**
3. **契约先行**：先冻结契约（M1：schema / 字段 / 状态 / 安全边界 / 测试矩阵），再进入实现 wave。
4. **并行派发**：一个 wave 内 ≥ 2 个相互独立、依赖已满足的 ready TaskNode，**默认并行派发给多个实施 agent**（Cursor `Task` 工具 subagent 或 `codex` CLI），主 agent 当 orchestrator 串行 review + 合并，**禁止 last-writer-wins 覆盖**，也禁止把多个独立 TaskNode 塞进一个串行实现。
5. **逐 milestone 过 gate**：每个 milestone 收齐验证证据、过 integration gate，才进入下一个；未过 gate 不得推进。
6. **收口**：任务完成后 taskBoard 移入 `tasks/archive/`，再把稳定结论提炼进 `docs/`。

执行器与并行细节见 `harness-engineering-plan` 的 SKILL.md §「Dispatching TaskNodes to Parallel Subagents」与 templates.md §「执行器映射」。Cursor 环境下本门同时由 `.cursor/rules/harness-execution.mdc`（alwaysApply）每轮注入。

## 防目标漂移（Anti-Drift）

上下文窗口易失且有限：跑久了主目标会被挤出注意力或被压缩(compaction)摘要掉，agent 就会漂去做局部子任务。**目标存文件，不存脑子。**

1. **目标外置到 taskBoard 北极星**：每个任务的主目标(Goal)、验收(Acceptance)、当前 milestone / TaskNode、一句话不变量(Core Rule) 写在 `taskBoard.md` 顶部 `## Board State`，作为唯一事实来源。上下文丢了，taskBoard 不丢。
2. **每轮重锚**：每个 wave / 工作 session 开工前，先 re-read `## Board State`，用一句话复述「主目标 + 当前在哪个 TaskNode」再动手；上下文变长或被压缩后，**以 taskBoard 为准恢复目标，不靠记忆**。
3. **TodoWrite 常驻锚点**：把主目标 + 验收标准固定为 TodoWrite 第 0 项（始终可见、不删），子任务在其下展开。
4. **动作前自检**：每个非 trivial 动作前问一句「这一步服务于 Board State 的主目标吗？」偏了就停、回 taskBoard 对齐。
5. **及时回写**：每完成一个 TaskNode / wave，立即把状态与证据写回 taskBoard，让外置记忆始终最新。

## Git Worktree 隔离开发

开发新功能或修复 bug 时，优先使用 `git worktree` 在独立工作目录中进行，避免污染当前工作区。

1. 先确认基线分支，再基于它创建 worktree。
2. 功能开发使用 `feat/<slug>`；bug 修复使用 `fix/<slug>`。
3. `<slug>` 使用小写 kebab-case，描述模块与目的。
4. 在新 worktree 中完成所有开发、测试。
5. 开发完毕后再决定是否合并回主分支。
6. 仅修改文档、配置等 trivial 变更时，可直接在当前工作区操作。

## 测试规则

- 后端新增或修改功能必须更新对应测试。
- 修改测试结构后同步更新测试说明文档（如存在）。
- 推荐验证命令：`mvn -pl hisense-hr-api -am test`、`mvn -pl hisense-hr-boot -am test`。
- 新增或调整 docs 后，至少跑一次文档链接校验，确认 Top-Down / Bottom-Up 可达。

## 历史教训

1. 模板必须避免保留旧路径诱导新项目走错层级；废弃路径应迁移后删除，而不是长期并存。
2. 大型计划、taskBoard、一次性说明如果不归档，会被 Agent 误读成当前入口；必须通过 `tasks/archive/` 收口（不放入 `docs/archive/`，以区分执行归档与设计文档归档）。
3. 架构外部环节必须在 `docs/OVERVIEW.md`、`docs/reference/architecture.md` 和子目录 README 三层都可见。
4. 新 milestone 必须强制走 `harness-engineering-plan` 生成 `taskBoard.md`。
5. docs 双向可追溯（Top-Down / Bottom-Up）是硬约束。
6. docs 跨层链接必须优先使用项目根相对路径，杜绝深 `../` 漂移。
