---
name: project-docs-workflow
description: >-
  项目 docs 与主线路线的薄编排器。用于用户调整或询问当前主线、路线、并行工作面、插入阶段、
  当前进度和下一步，以及非 trivial 开发、bug 修复、重构、API 或跨模块修改前后，也用于询问
  已实现行为、业务口径或 expected-vs-implemented gap。先从 OVERVIEW 和 owning README 获取当前
  route/state，按需读取 requirements/reference，必要时升级 project-analysis，实施后把稳定路线、
  状态和证据回写唯一 owner，避免生成平行控制面。
---

# 项目 docs 维护编排

这是一个**薄编排层**。

它不替代 `AGENTS.md` 的规则，也不替代 `project-analysis` 的深度分析。它负责把两者接起来。

## 目标

在代码实施前后，把项目文档工作流跑完整：

1. 先解析项目当前 Feature、owning README route manifest、当前 focus 与认知输出层级
2. 开发前找 `docs/` 里的相关文档，并从 owning GOAL/README 获取当前状态
3. 按真值类型核对上下文：requirements 管 expected behavior，冻结 Spec 管 bounded implementation contract，accepted ADR 管 durable rationale，代码管 implemented behavior，artifact 管 evidence
4. 识别 requirements、active Spec、accepted ADR 与 current implementation 的差异
5. 实施前确认 contract-affecting work 已有 frozen Spec，并冻结模块拆分、依赖方向、公共接口、复用边界、文件行数预算和测试归属
6. 已实现功能问询、非 trivial bug 或路线依赖冲突时，必要时升级到 `project-analysis`
7. 实施后判断并 patch 受影响 docs
8. 验证门通过后，把稳定路线、状态、决策和证据更新到 owning docs 与 append-only artifacts
9. 外部团队方案先完成来源校验、逐项采纳和内部合同转译，再进入相同实施门禁

## 触发原则

遇到下面这些场景，应主动使用本技能：

- 用户要求实现功能、修改功能、开发新模块、重构
- 用户提供的是尚未形成边界的新想法时，先路由到 `add-idea`，不要在本技能中临时发明 Feature/Spec
- 用户要求调整 API、数据流、调度逻辑或做跨模块代码修改
- 用户要求调整主线、把 A/B 改成并行、插入/暂停/删除阶段、切换当前 Feature
- 用户询问“当前路线”“进度如何”“现在做到哪”“下一步”“继续”
- 用户要求修 bug，且 expected behavior 不明显，或 bug 涉及真实代码修改
- 用户询问已实现功能如何工作、某字段 / 状态 / 页面口径、需求与实现差异
- 用户的问题虽然是解释类，但涉及业务口径、调用链或已实现功能行为
- 用户要求根据外部团队提交的 analysis / proposal / design 开始内部实施

下面这些场景通常不要触发：

- 纯搜索 / 调研，且不涉及业务口径、调用链、已实现功能或需求差异
- 纯测试、纯文案、纯格式、小 typo
- 明确单文件 trivial fix
- 用户明确要求忽略 docs

## 标准流程

### 阶段 -1：识别 idea intake

若请求仍是未成形的 idea，缺少 owner、scope、acceptance 或 route-affecting decisions，先使用
`add-idea` 完成逐题 Grill、shared-understanding confirmation、Feature owner 选择和 requirements/Spec/ADR
物化。本技能只消费其确认后的内部合同，不重复访谈，也不把 idea 直接推进代码实施。

若用户已经提供清晰边界且 owning Feature 与 active Spec 可定位，继续本流程。

### 阶段 0：解析主线路线与认知层级

先从 `docs/OVERVIEW.md` 解析唯一 `CURRENT DEVELOPMENT MAINLINE`，再进入 owning INDEX/README。
若 README 存在 `MAINLINE-ROUTE` manifest，以它作为当前路线 overlay；稳定依赖仍由 development plan
持有，child GOAL 只持有局部状态。

创建、变更、验证或汇报路线时，加载并遵循
[mainline-route-contract.md](../progressive-disclosure-docs/references/mainline-route-contract.md)
作为共享 schema 与认知披露合同；
本 Skill 继续负责端到端编排，不另建路线管理 Skill。

把用户语言规范化为稳定 route mutation：

- `A -> B`：顺序依赖；`A || B`：并行；`[A || B] -> J`：汇合；
- insert、pause、drop、replace：插入、暂停、移除或替换；
- node ID 稳定且不可复用，只供机器使用；每个节点必须另有语义化模块/里程碑名称。

上述字母只用于内部规范化。向用户复述理解、汇报路线或进度时，必须把节点映射成模块/里程碑
名称，不输出 `M0`、`M3C`、`A/BC` 或 raw node ID，除非用户明确要求内部标识。

然后分类：

- 仅本轮先做哪一项 → session plan，不改 durable docs；
- 跨会话 current focus 变化 → owning README route manifest；
- 节点、依赖、并行、汇合、插入、暂停或删除变化 → development plan + README + changelog；
- 当前 Feature 切换 → OVERVIEW 指针 + 新旧 owner role/README + changelog。

只有解释会改变依赖、合同、证据含义或授权时才询问用户；否则简短声明理解后继续。

### 阶段 1：开发前扫描 owning docs

先检查：

- `docs/OVERVIEW.md`
- `docs/feature/INDEX.md`
- owning module 的 `docs/feature/<module>/README.md` / `INDEX.md`
- owning module 的 `docs/feature/<module>/requirements.md`（存在且任务涉及期望行为 / bug 时）
- active `docs/feature/<module>/specs/SPEC-*.md`（contract-affecting implementation 时）
- blocking Feature-local ADR 与相关 system ADR（只读当前 Spec 引用的 decision）
- `docs/reference/INDEX.md`
- 可能相关的 `docs/reference/*.md`
- `docs/reference/code-organization.md`
- owning GOAL / README 的 current-state section — completed、pending、blockers、next validation gate 和 evidence
- 若任务来自外部团队：`docs/collaboration/<case-id>/INDEX.md`、问题包版本和外部方案 provenance

优先用 `Glob` 找文件，再用 `Read` 读取候选文档。

匹配时重点看：

- 模块名
- 功能名
- API 名称
- 关键词
- 最近 changelog

如果找到相关文档：

- 把 `AGENTS.md` 和用户明确授权视为安全与权限真值
- 把 owning `requirements.md` / confirmed contract 视为 expected behavior 真值
- 把 active frozen Spec 视为本次 bounded implementation contract
- 把 accepted ADR 视为 durable architecture rationale；`proposed` ADR 不能授权依赖它的实现
- 把当前代码视为 implemented behavior 真值
- 把不可变 artifact / ledger / gate report 视为 evidence 真值
- 把 owning README 视为上述事实的当前快照，不用它替代合同、代码或证据
- 任何冲突都必须分类为 contract gap、implementation gap、evidence gap 或 stale summary，不得用一层静默覆盖另一层
- 外部 proposal 只作为 recommendation/provenance；只有 adoption matrix 中 `ACCEPTED` 或
  `MODIFIED`，且已转译为 confirmed requirements、conditional accepted ADR、frozen Spec 与
  owning README current-state link 的条目才可能进入后续实施门

如果没找到相关文档：

- 新 idea 或 contract-affecting 功能先进入 `add-idea`；不得因缺 owner 而直接编码
- 已有明确 owner 的 trivial 局部修复可直接定向分析/实施
- 不要求为无合同影响的 trivial 修改强制创建 Spec

### 阶段 2：判断是否需要升级到 `project-analysis`

只在下面情况升级：

- 涉及跨模块调用链
- 需要梳理架构 / 数据流 / 时序
- 现有 docs 明显过旧，且单靠读代码难以快速建立全局视图
- 用户明确在问“这个模块怎么工作”“是否有性能问题”“帮我梳理链路”这类问题
- 用户询问已实现功能细节、字段 / 状态 / 页面口径或调用链
- 需要判断 expected behavior 与 current implementation 的差异
- 涉及非 trivial bug、RCA 或可能存在历史设计偏差
- 缺少 `requirements.md`，但当前任务依赖 expected behavior 判断
- 拟议路线变化与稳定 dependency/gate 冲突，或无法判断能否并行、在哪里汇合

如果是 trivial 修改、口径已经明确的局部变更：

- 可以不升级到 `project-analysis`
- 直接读相关代码和现有 docs 即可

如果用户已明确给出合法的顺序、并行、插入或 focus 调整，且不改变合同/授权，不要为了路线表述
升级到深度分析。需要升级时，以 `route-impact` 调用 `project-analysis`，要求只返回 Proposed Route、
Dependency/Gate Impact、Owner/Docs Impact、Risks、Validation，不向用户展开实现清单。

如果升级到 `project-analysis`：

- 明确告诉它默认目标是写入文档，而不是停留在纯终端分析
- 优先判断当前结果应走 `update-doc` 还是 `new-doc`
- 若已有合适长期文档承接，优先 `update-doc`
- 若没有合适长期文档承接，再 `new-doc`
- 长期知识仍应优先回填 `docs/feature/<module>/` / `docs/reference/*.md` / `OVERVIEW.md`
- 不要默认再造平行的长期文档体系

### 阶段 3：冻结实施前代码组织

若实施来源于外部方案，先确认 case `INDEX.md` 已记录 problem/proposal 版本绑定、逐项采纳决定、
内部 SSOT target 和 next gate。缺少合同转译时停止实施，不得直接从 `external-proposal.md` 编码。
外部来源接收、采纳矩阵和 case 状态由 `external-collaboration-workflow` Skill 负责；本 Skill 只在
采纳完成后负责内部 owning docs 与代码实施闭环。

非 trivial 且影响 public contract、schema、state、module ownership、migration、safety 或 validation matrix 的实施，必须引用 active frozen Spec。模块图和详细实施合同写入 Spec；owning README 只记录 active Spec 链接、compact status 与 next gate：

- 模块名、单一责任和预计文件路径
- 公共 type/function/protocol/artifact 边界
- 允许的依赖方向与禁止的环形/反向依赖
- 可变状态所有权和序列化边界
- 共享逻辑的现有消费者，避免提前建立无边界 `utils.py`
- 每个手写代码文件的行数预算；硬上限 1000 物理行，800 行进入拆分预警
- unit/contract/property/integration 测试的归属

Blocking ADR 未 accepted、requirements 未 confirmed、Spec 仍为 draft 或存在 blocking open question 时，不得进入 contract-affecting implementation。没有模块设计时，不得直接从一个新大文件开始堆叠功能。已有或预计超过
1000 行的手写文件必须先按 domain responsibility 抽离，不得机械切成 part 文件。
用户明确要求拆分/抽离/模块化，或目标文件达到 800 行预警、1000 行硬门禁时，必须加载
`refactor-large-modules`，按其固定责任分类、不可变合同、迁移批次、兼容策略和验证矩阵执行，
不得为当前任务另造一套抽离方法。

### 阶段 4：实施代码变更

代码实施阶段：

- 当前代码决定“现在实现了什么”
- owning confirmed requirements 决定“应该实现什么”
- active frozen Spec 决定“本次如何实现与验证”
- accepted ADR 决定“哪些持久架构取舍不得被局部实现静默改写”
- 不可变 artifact 决定“验证或实验实际发生了什么”
- docs 与代码冲突时，记录 expected-vs-implemented gap；不得默认用代码改写合同，也不得根据未实现文档声称功能已存在
- 涉及安全、权限、数据泄漏、holdout 或 evidence boundary 的冲突必须先停止扩张性实施并暴露 blocker
- CLI、strategy、model adapter 和 runner 保持薄层，domain logic 回到 owning module
- 任一本轮增改的手写代码文件超过 1000 物理行时，停止功能堆叠并在同一任务拆分
- 触发抽离时按 `refactor-large-modules` 叶子优先逐批迁移，每一批都运行行为等价和 import 验证

### 阶段 5：实施后做 docs 影响判断

代码完成后，主动判断是否有 docs 影响。

重点判断这四类：

1. `docs/feature/<module>/requirements.md`
   - expected behavior、验收标准、产品口径是否变化
2. `docs/feature/<module>/README.md` / `INDEX.md`
   - current state、API inventory、active Spec/decision links 是否变化
3. active Spec / ADR
   - implementation contract 是否变化；是否需要 reopen/supersede Spec
   - 是否产生满足 trigger 的 durable decision；是否需要新 ADR supersede 旧 ADR
4. `docs/reference/interfaces.md`
   - 稳定接口、入参 / 出参、外部契约是否变化
5. `docs/reference/runbook-testing.md`
   - 验证方式、测试命令、运行前置条件是否变化
6. `docs/OVERVIEW.md`
   - 是否新增模块、模块边界是否变化、入口索引是否需要更新
7. `AGENTS.md` 的“历史教训”
   - 这次修复是否形成了新的稳定经验，值得追加一条编号记录

如果没有实质变化：

- 不要为了“形式完整”而改 docs

如果确认文档已过时、缺失或与实现不一致：

- 非 trivial 代码、契约、运行方式变更默认同步 docs
- 只有文档拆分 / 迁移 / 大规模重构，或产品口径不确定时，先询问用户确认

### 阶段 6：按影响自主 patch docs

非 trivial 代码、合同、运行方式或 evidence status 变更，默认在同一任务自主 patch owning docs。
只有文档拆分 / 迁移 / 大规模重构，或 expected behavior 仍不确定时，才先请求用户确认。

Patch 时：

- 优先增量更新现有文档
- 保留仍然正确的部分
- 不默认整篇重写
- expected behavior / acceptance 优先回填到 `docs/feature/<module>/requirements.md`
- bounded implementation contract 优先回填 active Spec；冻结合同发生实质变化时 reopen 或创建 superseding Spec
- ADR-worthy choice 按共享 decision contract 创建/更新 ADR，不把 rationale 塞进 README
- current state / API inventory / active contract links 优先回填到 `docs/feature/<module>/README.md` / `INDEX.md`
- 稳定跨 Feature 接口契约优先回填到 `docs/reference/interfaces.md`
- 验证方式优先回填到 `docs/reference/runbook-testing.md`
- 新模块补 `docs/OVERVIEW.md`
- 新踩坑补”历史教训”并编号递增
- current focus 变化只更新 owning README route manifest/current snapshot
- 稳定路线拓扑变化同步更新 development plan、README manifest 与 append-only changelog
- child GOAL 维护局部 STEP/文件/测试/artifact 与 `ROUTE-NODE` state；父 README 只 roll-up 同一
  node 的 ID/progress/authorization，三者变化时必须同轮同步
- OVERVIEW/Feature INDEX 只在当前 Feature 指针或入口变化时更新，不复制 route summary

### 阶段 7：验证门通过后回写 durable state

当当前 milestone 的验证门通过后：

1. 更新 owning GOAL / README 的 completed、pending、blockers、next validation gate 和 evidence
2. 将稳定结论更新到 `docs/feature/<module>/`：
   - 新增/变更的 expected behavior / 验收口径 → `requirements.md`
   - 本次模块、schema、state、migration、validation contract → active Spec
   - 稳定跨 Feature API 契约 → `docs/reference/interfaces.md`
   - 满足 ADR trigger 的设计决策与取舍 → owning ADR；其余可逆局部设计留在 Spec
3. 将运行结果、checksum、指标或其他过程证据写入声明的 append-only artifact
4. 将 milestone 级状态迁移追加到 owning `changelog.md`；不写原始终端输出或会话步骤
5. 若模块无 `docs/feature/<module>/` 目录，先建目录和 README
6. 同步更新 `docs/feature/INDEX.md` 的路由表
7. 运行 `python3 scripts/validate_code_organization.py`，确认增改手写文件未超过 1000 行
8. 若实现来自外部 proposal，在 collaboration case adoption matrix 回填 owning SSOT、完成状态和 evidence route

**核心原则：临时顺序留在会话计划；durable state、稳定结论和证据由 owning docs 与 append-only artifacts 持有。**

## 文档落点规则

默认只维护这一套长期文档：

- `docs/feature/<module>/requirements.md`
- `docs/feature/<module>/README.md` / `INDEX.md`
- `docs/feature/<module>/specs/`（按需；active bounded implementation contracts）
- `docs/feature/<module>/decisions/`（按需；Feature-local ADRs）
- `docs/feature/<module>/changelog.md`（仅 Feature / Spec / ADR / milestone / gate 级 append-only 记录）
- `docs/reference/interfaces.md`
- `docs/reference/runbook-testing.md`
- 其他相关 `docs/reference/*.md`
- `docs/collaboration/<case-id>/`（仅外部来源、版本绑定、采纳和追溯；不保存开发进度副本）
- `docs/OVERVIEW.md`

不要默认再造长期并行文档体系。

如果 `project-analysis` 产出了时序图、数据流图、性能观察：

- 优先判断是否能更新现有 `docs/feature/<module>/` / `docs/reference/*.md` / `OVERVIEW.md`
- 能承接则走 `update-doc`
- 没有合适承接文档时，再走 `new-doc`
- 不再把 `analysis-only` 作为默认返回形态

## 输出给用户时要说明的事

默认使用 L0 宏观输出，固定为最多六项：

- 目标
- 路线
- 当前 focus
- blocker
- next gate
- authorization boundary

六项都使用语义化模块/里程碑名称，不使用内部阶段编号、字母工作面或 raw node ID。不要默认
输出文件、接口、测试、命令或 artifact。用户要求展开某个工作面时进入 L1；明确要求
实施、审计或 blocker 证据需要时才进入 L2。详细规则由 `progressive-disclosure-docs` 的
`references/mainline-route-contract.md` 持有。

在实施前，如果找到了相关 docs，可以简短说明：

- 找到了哪些相关文档
- 会把它们当半可信上下文

在实施后，如果发现 docs 可能过时，要明确指出：

- 哪份文档可能过时
- 为什么过时
- 是否建议 patch

## 执行提醒

- 本技能的目标是降低 docs 与代码脱节的概率，不是为了增加文档动作。
- 小改动不要强行引入 docs 流程或 Spec。
- 未成形 idea 先进入 `add-idea`；本技能不重复 Grill。
- 真正需要时，再升级到 `project-analysis`。
