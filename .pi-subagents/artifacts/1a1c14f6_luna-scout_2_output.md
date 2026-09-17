## 1. 确认事实

### Git 状态

- 分支：`main...origin/main`
- 未跟踪文件：`.agents/skills/harness-setup/`
- 没有已暂存文件。
- 当前状态命令：`git status --short --branch`

### 安装 / 注册路径

项目同时维护两套 skill 路径：

- `.agents/skills/`
- `.claude/skills/`

已注册的 harness 相关路径包括：

- `.agents/skills/progressive-disclosure-docs/`
- `.agents/skills/project-analysis/`
- `.agents/skills/project-docs-workflow/`
- `.agents/skills/harness-engineering-plan/`
- `.agents/skills/harness-setup/`，当前未跟踪
- `.claude/skills/progressive-disclosure-docs/`
- `.claude/skills/project-analysis/`
- `.claude/skills/project-docs-workflow/`
- `.claude/skills/harness-engineering-plan/`
- `.claude/skills/code-organization-harness/`

未发现 symlink。`.agents` 与 `.claude` 是独立副本，不是同一 canonical 安装目标。

源套件位置：

- `/Users/shancw/project/MyAwesomeSkills/skills/harness/`
- 源套件没有中央 installer 或自动 overwrite 机制；`UPGRADING.md` 明确规定目标项目逐 skill 比较、目标项目自行维护注册路径。

### canonical skill 分类

源套件包含 7 个 canonical skill：

- `add-idea`
- `document-organization-harness`
- `external-collaboration-workflow`
- `progressive-disclosure-docs`
- `project-analysis`
- `project-docs-workflow`
- `refactor-large-modules`

当前项目中可以直接按 canonical 版本升级的情况：

- `document-organization-harness`：项目没有对应 `.agents` / `.claude` 目录，属于未安装，不应直接覆盖或伪造注册。
- `external-collaboration-workflow`：未安装。
- `refactor-large-modules`：未安装。
- `add-idea`：未安装。
- `project-analysis`：`.agents` 与 `.claude` 内容相同，但都与源套件存在差异；不能无审查直接覆盖。
- `progressive-disclosure-docs`：`.agents`、`.claude` 均与源套件不同；不能直接覆盖。
- `project-docs-workflow`：`.agents`、`.claude` 均与源套件不同；不能直接覆盖。

此外：

- `code-organization-harness` 是项目本地扩展，源套件没有同名 canonical skill，应保留。
- `harness-setup` 是项目本地扩展，当前只存在于 `.agents/skills/harness-setup/`，且未跟踪；不是源套件中的 canonical skill。
- `harness-engineering-plan` 是项目本地扩展 / 旧 harness skill，源套件没有同名目录；不能按 canonical 同步处理。

## 2. 与轻量模型的冲突证据

### 高严重度：`project-docs-workflow` 仍要求同步前置流程和用户确认

文件：[.agents/skills/project-docs-workflow/SKILL.md](/Users/shancw/workspace/tradingsignal/.agents/skills/project-docs-workflow/SKILL.md)

- `:5`：描述中要求“实现完成后……**先询问用户确认后再更新**”。
- `:20`：流程第 5 步为“**先询问用户，再决定是否 patch 文档**”。
- `:121`：明确要求“**先询问用户是否要 patch 对应 docs**”。

这与新模型冲突：

- 新模型要求实现和验证完成后，由主 Agent 异步委派一个 docs SubAgent。
- docs SubAgent 一轮 patch，主 Agent 不等待。
- 不应把普通 docs 更新变成用户确认门槛。

`.claude` 副本同样存在上述冲突，精确行号相同。

另外，当前 `.agents` 版本没有源套件中的轻量语义：

- 没有明确“只读 1-3 份相关 docs”
- 没有明确“不要求 TDD、testing-first、Spec、固定状态机、验证矩阵”
- 没有明确“完成后异步 docs SubAgent、单 writer、不等待”

源套件对应语义位于：

- `/Users/shancw/project/MyAwesomeSkills/skills/harness/project-docs-workflow/SKILL.md:1-25`
- 特别是描述与“快速原则”部分。

### 高严重度：`harness-engineering-plan` 重新引入固定 planning gate、contract-first 和 validation matrix

文件：[.claude/skills/harness-engineering-plan/SKILL.md](/Users/shancw/workspace/tradingsignal/.claude/skills/harness-engineering-plan/SKILL.md)

- `:22-25`：milestone 完成必须要求所有 TaskNodes、集成验证、docs/contracts 更新和安全边界。
- `:27-29`：要求前一阶段 gate 完成后才能进入下一阶段。
- `:107-113`：明确“**Contracts before implementation**”，并要求 output contract、input contract、safety boundary、fixture/test matrix、interface documentation。
- `:121-125`：要求固定 gate 验证，不仅运行测试，还要验证文件、API/schema 字段、降级行为、安全和 docs/runtime 一致性。
- `:248-256`：内置 M0 Planning Gate、M1 Contract Foundation、M5 Integration & Verification 等固定 roadmap。
- `:282-304`：要求先写 M0 plan/task board、M1 contracts，再执行 implementation waves，并在实施前检查 validation commands。
- `:336-339`：并行 TaskNode 要求 worktree、8-section prompt、forced reading、acceptance、validation、safety、done-file 等固定结构。

这与新模型冲突：

- 普通实现不应被强制进入 TaskBoard / M0/M1 lifecycle。
- 不应强制 contract-first、fixture/test matrix、固定 validation matrix。
- 该 skill 应仅适用于用户明确要求 milestone / task breakdown / multi-wave planning 的场景。

`templates.md` 也继续强化旧流程：

- `.claude/skills/harness-engineering-plan/templates.md:32`
- `:60-61`
- `:94-100`
- `:146-150`

这些行要求强制阅读清单、独立验证命令、机器可验证 acceptance、跨 TaskNode 契约协调等。

### 中严重度：`project-analysis` 默认写 docs 并强制 Mermaid + ASCII 双产物

文件：[.claude/skills/project-analysis/SKILL.md](/Users/shancw/workspace/tradingsignal/.claude/skills/project-analysis/SKILL.md)

- `:10-14`：默认行为是更新或创建 docs；` :14` 强制 Mermaid 后必须紧跟 ASCII/TUI。
- `:26-30`：只保留 `update-doc` / `new-doc`，默认优先写文档。
- `:86-89`：进入分析后必须先完成文档落点判断。
- `:105-126`：正式读代码前必须拆成 2-4 个子任务，并规定 SubAgent 取证结构。
- `:144-152`：新文档必须更新索引、反向链接、深链规则等。
- `:169-179`：再次规定默认文档落点。

这与新模型的冲突程度取决于触发范围：

- 对明确的架构 / 数据流 / 性能分析任务，这些约束可以保留。
- 对普通实现，不应默认触发 `project-analysis`，也不应强制写文档、拆 2-4 个子任务或生成 Mermaid + ASCII。
- 新模型要求“普通实现前只读少量 docs”；当前 skill 的默认写 docs 语义会重新扩大流程。

`.agents/skills/project-analysis/SKILL.md` 与 `.claude` 版本相同，冲突同时存在两处。

### 中严重度：`progressive-disclosure-docs` 的旧治理要求过重

文件：[.claude/skills/progressive-disclosure-docs/SKILL.md](/Users/shancw/workspace/tradingsignal/.claude/skills/progressive-disclosure-docs/SKILL.md)

轻量部分仍然存在：

- `:14`：只读取任务相关的 1-3 份 docs。
- `:181-190`：taskBoard 默认不读，只在执行连续性 / 验收 / 审计时读取。

但仍有旧流程残留：

- `:77-86`：要求 AGENTS 包含完整写规则、测试和更新规则。
- `:99-130`：对 module docs 结构、design/dataflow/changelog/taskBoard/RCA 进行固定规范。
- `:134-175`：固定 proposal 拆分、spec、acceptance、review archive 生命周期。
- `:183-190`：要求 reference/archive routing 与 taskBoard 规则。
- `:197-224`：要求 frontmatter、metadata、索引和文档分类维护。
- `:240-248`：将大量 docs 导航和写入 checklist 固化为验收条件。

新模型并不禁止这些作为项目已有 docs 约束，但它们不应成为普通代码实现的强制 lifecycle。

### 中严重度：`AGENTS.md` 将 taskBoard 和测试写成强规则

文件：[AGENTS.md](/Users/shancw/workspace/tradingsignal/AGENTS.md)

- `:13`：后端新增能力“必须补测试”。
- `:31`：新增模块、跨文件 bug、重构、API/UI/Worker/CLI 前“先使用” `code-organization-harness`。
- `:56-64`：任何 docs 维护都必须满足双向可追溯，且新需求要能从入口发现 taskBoard/design 文档。
- `:85-100`：新增/变更模块、接口、运行方式时要求同步多份 docs/index/types/test docs，并要求 proposal ≥500 行拆分成 design/spec/acceptance。
- `:106`：新 milestone / 多 Wave / 多 TaskNode 必须先生成 taskBoard。
- `:110`：明确“**强制规则**”：新 milestone（≥2 wave 或 ≥5 TaskNode）必须先生成并实时更新 taskBoard。
- `:137`：后端新增或修改功能必须更新 `tests/`。
- `:146`：历史教训再次把 `harness-engineering-plan` taskBoard 固化为必须流程。

判断：

- `:13`、`:137` 是项目级测试安全规则，不等价于 harness 的 TDD/testing-first；可保留，但应避免被解释成所有实现必须测试先行。
- `:31`、`:106`、`:110`、`:146` 会重新引入旧 planning gate；需要改为仅在明确的 multi-wave/multi-node 规划任务中适用。
- `:56-64`、`:85-100` 属于 docs 维护治理，可保留用于实际 docs 变更，但不应阻塞普通实现。
- `:59` 对每个 leaf 包括 taskBoard 的反向链接要求与项目已有 docs 结构强绑定，不属于轻量模型核心，可暂不改动，除非目标是全面简化 docs 治理。

### 低严重度：`CLAUDE.md` 仍使用“significant implementation”前置读取

文件：[CLAUDE.md](/Users/shancw/workspace/tradingsignal/CLAUDE.md)

- `:5`：`Read AGENTS.md and docs/OVERVIEW.md before significant implementation work.`
- `:6`：渐进式读取规则本身符合新模型。

`:5` 可以保留，但“significant”应由任务风险判断，不应被解释为所有普通实现必须启动完整 docs workflow。当前没有 TDD、Spec、ADR、固定 validation matrix 或等待 docs writer 的直接要求。

### `harness-setup` 的旧 taskBoard 默认倾向

文件：[.agents/skills/harness-setup/SKILL.md](/Users/shancw/workspace/tradingsignal/.agents/skills/harness-setup/SKILL.md)

- `:22-26`：Outcome 默认包含 `taskBoard.md`。
- `:32-35`：多 wave、依赖或 validation gate 时添加 taskBoard。
- `:43-45`：taskBoard 被定义为 execution control plane。

参考文件：[.agents/skills/harness-setup/references/harness-bootstrap.md](/Users/shancw/workspace/tradingsignal/.agents/skills/harness-setup/references/harness-bootstrap.md)

- `:140-150`：work 超过一个 wave、存在依赖、分阶段验证或多 owner 时创建 taskBoard。
- `:152-158`：提供固定 taskBoard skeleton。

判断：

- 对 harness bootstrap / 复杂 multi-wave work，保留是合理的。
- 对普通实现，该 skill 不应被 AGENTS 作为默认触发器。
- 当前 `.agents/skills/harness-setup/` 未跟踪，属于工作区用户内容；升级时不应擅自删除或覆盖。

## 3. 最小安全升级方案

### 应修改

1. `.agents/skills/project-docs-workflow/SKILL.md`
2. `.claude/skills/project-docs-workflow/SKILL.md`

将其收敛为：

- 开始前只读 `AGENTS/CLAUDE` 与 1-3 份相关 docs。
- 缺 docs 不阻塞实现。
- 实现和风险匹配验证完成后，主 Agent 异步委派一次 docs SubAgent。
- docs SubAgent 是单 writer，一轮 patch。
- 主 Agent 不等待 docs patch。
- 删除“先询问用户是否 patch docs”的普通流程门槛；仅目标、授权、安全、兼容性等硬边界不明确时询问。

2. `AGENTS.md`

最小调整：

- `:106`、`:110`、`:146` 改成“仅当用户明确要求 multi-wave / multi-TaskNode planning，或任务确实需要可审计 execution control plane 时使用 `harness-engineering-plan`”。
- 保留项目自己的安全边界、分层规则、真实路径测试规则。
- 在 docs 规则中加入异步 docs SubAgent 单 writer 语义。
- 不把普通实现绑定到 taskBoard、Spec、ADR、固定 validation matrix。

3. `CLAUDE.md`

建议补充一条轻量规则，明确：

- 普通实现只读取少量相关 docs；
- docs 写回发生在实现与验证之后；
- 由一个异步 docs SubAgent 完成一轮 patch，主 Agent 不等待。

4. `.agents/skills/harness-setup/SKILL.md` 与其 reference

只在确认该未跟踪扩展是项目有意保留内容后修改：

- 将 taskBoard 明确限定为 bootstrap 或确实需要 multi-wave/multi-owner coordination 的场景。
- 不把 taskBoard 作为普通实现默认产物。

### 应保留

- `.claude/skills/code-organization-harness/`：项目特定的模块边界、目录和测试镜像规则。
- `AGENTS.md` 中的 TradingSignal 安全边界、后端/前端分层、API 类型契约、secret 不回显、sandbox 禁止 GitHub Actions 等项目规则。
- `.claude/skills/project-analysis/` 中架构/数据流/性能分析场景的事实核验内容；只需取消其对普通实现的默认写 docs / 固定输出强制。
- `.claude/skills/progressive-disclosure-docs/` 的 1-3 docs progressive disclosure 和 taskBoard 默认不读规则。
- `.claude/skills/harness-engineering-plan/` 作为显式 planning 工具，而不是普通实现前置门禁。
- `.agents/skills/harness-setup/` 未跟踪的本地扩展，先保留并单独审查。

### 不应触碰

- 未安装的 canonical skill 目录，不要为了“完整同步”新建：
  - `add-idea`
  - `document-organization-harness`
  - `external-collaboration-workflow`
  - `refactor-large-modules`
- 项目代码、测试、配置、运行时 artifacts。
- `.claude/parallel-runs/`、历史 docs、归档 docs。
- 不要把 `.agents` 和 `.claude` 未分类内容直接覆盖成同一份 canonical 副本。
- 不要删除旧 proposal/spec/ADR/taskBoard；源套件要求仅在相关工作触及时迁移，不能批量清理。

### 同步策略

建议分两阶段：

1. 先统一 `.agents` / `.claude` 的 `project-docs-workflow`、`progressive-disclosure-docs` 轻量语义和注册说明。
2. 再审查 `project-analysis` 与 `harness-engineering-plan` 的触发边界；保留复杂分析和显式规划能力，但移除普通实现默认门禁。

本次不建议直接做整目录覆盖，因为：

- 三个已安装 skill 都有本地修改。
- `.agents` 与 `.claude` 本身也不完全一致。
- `code-organization-harness`、`harness-engineering-plan`、`harness-setup` 都是项目本地扩展。

## 4. 未覆盖、矛盾与不确定项

- 未发现显式 installer、package manager 注册文件或 symlink；当前注册主要由目录存在和 root rules 文本引用构成。
- `.agents/skills/harness-setup/` 是未跟踪目录，无法仅凭 git 判断它是否是用户临时内容还是准备纳入项目的扩展。
- 未对所有非 harness `.agents` / `.claude` skill 做完整语义审计；本分析集中于 canonical harness、`harness-setup`、`harness-engineering-plan`、AGENTS/CLAUDE 与 docs governance。
- 源套件中 `add-idea`、`document-organization-harness`、`external-collaboration-workflow`、`refactor-large-modules` 当前没有目标注册路径，因此“可直接同步”结论为“不适用”，不是建议安装。
- 没有运行测试；本任务是只读升级分析，不涉及代码行为变更。

## Acceptance Report