# Agent 开发规约

> 项目上下文入口：[`docs/OVERVIEW.md`](docs/OVERVIEW.md)

开始任何重要开发前，先读 `docs/OVERVIEW.md`。本仓库采用 docs-first、结构化契约、分层清晰、测试可执行的 harness 工作方式。禁止把密钥、凭证、私有运行时数据或敏感内容写入 docs、日志或用户可见输出。

## 核心原则

- **Docs-first**：新增模块、接口或执行方式前，先确认 owning feature 和参考文档。
- **单一事实来源（SSOT）**：每条稳定规则只保留一个 owner。
- **结构化契约**：API、配置、脚本、目录与测试命名使用明确约定。
- **分层不反向**：控制层保持薄，编排放在服务层，底层不反向依赖上层。
- **真实路径验证**：新增或修改能力必须留下可验证证据。

## 分层约束

按项目实际技术栈填写依赖方向、禁止跨层调用和外部系统边界。

## 代码组织约束

- 先找 owning module，再按 layer 放文件。
- 新建前按 endpoint、schema、表名、配置键和 domain noun 搜索现有 owner。
- 测试布局与被验证的代码层级保持对应。
- 框架细则服从仓库既有约定。
- 非 trivial 实施前冻结模块 owner、公共接口、依赖方向、可变状态 owner、文件预算和测试归属。
- 新增或本轮修改的手写文件不得超过 1000 物理行；800 行触发职责拆分评审，不得机械切成 numbered part 文件。

## 文档渐进式披露规则

```text
Level 0: AGENTS.md               → 项目开发规约与读取入口
Level 1: docs/OVERVIEW.md        → 项目地图与活动模块
Level 2F: docs/feature/INDEX.md  → 功能模块索引
Level 2R: docs/reference/INDEX.md → 架构 / 接口 / 测试等稳定参考
Level 2C: docs/collaboration/INDEX.md → 外部来源、版本绑定与内部采纳路由
Level 2A: docs/archive/INDEX.md  → 历史归档，默认不读
Level 3: docs/feature/<module>/  → 模块 README / INDEX
Level 4: 具体设计 / RCA，仅按需读取
```

Agent 读取规则：`OVERVIEW.md -> feature/reference INDEX -> 按需读 1-3 个相关文档`。禁止全量读取 `docs/`。

### 双向可追溯

1. 从 `AGENTS.md` 沿 OVERVIEW、INDEX、子 INDEX 到 leaf 始终可达。
2. 每个 leaf 顶部必须有上级链接。
3. 跨多层目录的链接优先使用项目根路径。
4. 移动文档时同时修复入口链接和反向链接。

## 文档写入规则

- 独立 feature 命中自有目标、契约、生命周期，或 leaf ≥ 3、单文件 ≥ 500 行时，建立 `docs/feature/<feature>/` 和 README。
- `requirements.md` 记录 expected behavior 与 acceptance。
- `README.md` / `INDEX.md` 记录 current implementation、routing、completed、pending、blockers 和 next validation gate。
- 非 trivial 代码、契约或运行方式变更后，同步 owning README、requirements、feature INDEX、OVERVIEW 及受影响的 reference docs。
- 历史计划、旧结论和 RCA 放入 `docs/archive/` 并标记状态。
- 任何新增 leaf 都要同时增加父级路由和上级链接。

## 项目内置 skills

- `.agents/skills/harness/document-organization-harness`：组织文档结构、索引、模块边界与导航规则。
- `.agents/skills/harness/project-analysis`：现有 docs 不足或链路复杂时进行架构、数据流、时序与风险分析。
- `.agents/skills/harness/project-docs-workflow`：非 trivial 开发前后扫描 owning docs 并判断文档影响。
- `.agents/skills/harness/progressive-disclosure-docs`：审计渐进式披露、SSOT、feature 粒度和双向可追溯。
- `.agents/skills/harness/external-collaboration-workflow`：管理外部问题包、方案来源、采纳和内部合同转译。
- `.agents/skills/harness/refactor-large-modules`：按稳定责任拆分大文件，保持公共契约和行为等价。

## 强制执行流程门（Mandatory Execution Gate）

非 trivial 的实现、修改、开发或修复任务，在写实现代码前依次完成：

1. 定位 owning module、requirements、README 和关键代码入口。
2. 冻结 schema、字段、状态、安全边界和验证矩阵。
3. 在 owning GOAL/README 记录 completed、pending、blockers 和 next validation gate。
4. 在声明边界内实施，保留不相关的现有修改。
5. 运行聚焦验证，再运行与影响范围匹配的广泛检查。
6. 将稳定状态、决策和证据同步到 owning docs 和 append-only artifacts。

本门不自动授权委派。只有用户明确要求时才使用边界清晰的 owner scope；修改重叠时使用隔离 worktree。

Cursor 环境下，本门同时由 `.cursor/rules/harness-execution.mdc` 每轮注入。

## 防目标漂移（Anti-Drift）

- owning GOAL、requirements 和 README current-state section 是执行锚点。
- 每个工作 session 开始、上下文压缩后和推进验证门前重新读取这些文档。
- 验证门通过后立即更新 durable state 与证据。
- 每个非 trivial 动作前确认它直接推进目标且不跨越安全边界。

## Git Worktree 隔离开发

- 只有用户要求或并行修改会重叠时才创建 worktree。
- worktree 使用明确的 owner scope，完成后由主 agent 集成和验证。
- 不得为获得干净状态而丢弃无关修改。

## 测试规则

- 新增或修改功能必须更新对应测试。
- 修改接口、运行方式或验证方式时同步参考文档。
- 先运行聚焦测试，再运行影响范围支持的广泛检查。
- 文档变更至少执行链接校验与格式检查。

## 历史教训

1. 模板不得保留废弃路径诱导新项目走错层级。
2. 架构外部环节应在 OVERVIEW、reference 和 owning README 中可发现。
3. docs 双向可追溯是硬约束。
4. 稳定进度和证据必须回写到 owning docs，不能只存在于会话上下文。
