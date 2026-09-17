**检索结果（只读扫描，未改文件）**

**1) 入口/路由规则**
- `skills/harness/project-docs-workflow/SKILL.md:54-58` — `用户未成形 idea` 先走 `add-idea`（明确“明确边界”前不直接用本技能）。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:69-71` — 主路线解析时加载 `mainline-route-contract.md`，路由合同由本技能编排，非独立路由技能。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:91-107` — 扫描 `OVERVIEW/INDEX/README/requirements/spec` 的读法，禁止全量读 `docs/`。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:197-203` — 开发阶段输出需区分 expected behavior、Spec、ADR、实现与 evidence。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:238-260` — 实施后按影响范围 patch docs，并定义哪些路径同步更新。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:262-275` — 验证门后回写 owning docs、`feature/INDEX`、`OVERVIEW`、artifact。`强制`
- `skills/harness/README.md:48-50` — 所有未成形 idea 从 `.agents/skills/harness/add-idea` 进入；并定义 docs-only 入口真值归属（requirements/spec/ADR）。`强制`
- `skills/harness/add-idea/SKILL.md:7-9` — 入口协议：先 inspect owner，逐题 Grill，再创建/修改 requirements/spec/ADR。`强制`
- `skills/harness/add-idea/references/routing-contract.md:36-43` — 仅对会改变 boundary/行为/安全/验证/回滚的问题做 Grill；可选实现细节不 Grill。`强制`
- `skills/harness/add-idea/references/routing-contract.md:97-105` — Owner 路由与 artifact 路由矩阵（`REQUIREMENTS_PATCH`、`NEW_SPEC`、`ADR_CANDIDATE` 等）。`强制`
- `skills/harness/add-idea/references/routing-contract.md:146-158` — 路由输出字段包含 `Clarity / Owner route / Artifact routes`，`implementation authorization: none`。`强制`
- `skills/harness/progressive-disclosure-docs/references/mainline-route-contract.md:3-9` — 路由合同说明：`project-docs-workflow` 编排、`project-analysis` 仅用于歧义升级。`强制`
- `skills/harness/progressive-disclosure-docs/references/mainline-route-contract.md:25-35` — 路由操作（A->B/A||B/pause/drop/replace）对应 README/development-plan/changelog 的持久化写面。`强制`
- `skills/harness/progressive-disclosure-docs/references/mainline-route-contract.md:90-93` — 用户默认 L0 输出，非必要不展开实现细节；仅必要时追问。`可选/上下文策略`

**2) requirements / spec / specification 规则**
- `skills/harness/progressive-disclosure-docs/SKILL.md:48-53` — `requirements.md`=expected behavior/acceptance；README/INDEX 不应承载 requirements。`强制`
- `skills/harness/progressive-disclosure-docs/SKILL.md:150-153` / `171-177` — feature module 路由：expected behavior→`requirements.md`，bounded implementation→`specs/SPEC-*.md`。`强制`
- `skills/harness/add-idea/SKILL.md:112-116` — `REQUIREMENTS_PATCH` / `NEW_SPEC` 的触发条件。`强制`
- `skills/harness/add-idea/references/routing-contract.md:99-103` / `119-127` — 需求变更与 Spec 触发规则。`强制`
- `skills/harness/progressive-disclosure-docs/references/feature-spec-decision-contract.md:11-13` / `71-78` — 真值分离：requirements/Spec/ADR/README；生命周期独立。`强制`
- `skills/harness/progressive-disclosure-docs/references/feature-spec-decision-contract.md:94-99` — 新 Feature 需 problem/范围/验收/边界和注册。`强制`
- `skills/harness/progressive-disclosure-docs/assets/spec-template.md:45-75` / `87-95` — Spec 模板含 Public contracts、module ownership、validation matrix、test/ evidence/pass criteria。`强制（模板约束）`
- `skills/harness/progressive-disclosure-docs/assets/feature-template/requirements.md:18` / `53-59` — requirements 模板声明唯一 owner 与 acceptance/stop rules。`强制（模板约束）`
- `skills/harness/project-analysis/SKILL.md:12-13` / `93-101` — expected behavior/acceptance 主要归 `requirements.md`；冲突时以 code 优先，记录 requirement-gap。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:150-151` / `167-169` — 若存在合适承接，优先 update-doc；否则 new-doc。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:171-173` — 实施前须有 frozen Spec 且冻结 schema/state/接口/依赖/验证等。`强制`

**3) 文档更新时机（分阶段）**
- `skills/harness/project-docs-workflow/SKILL.md:19-29` — 目标中的 9 步完整编排（前置读、识别差异、升级分析、后置回写）。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:91-105` — 阶段1 读文档与判断依据。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:207-233` — 阶段5 判定影响文档范围并列出 4/7 类。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:233-241` — 实质变化触发 docs patch；无实质变化避免无意义改动。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:262-275` — 阶段7 回写 durable state（requirements/spec/interfaces/changelog）。`强制`
- `skills/harness/document-organization-harness/SKILL.md:36-47` — 组织类工作流顺序（先读现状、建 map、承载 docs、父子路由）`可选（方法框架）`
- `skills/harness/project-analysis/SKILL.md:34-67` — `update-doc/new-doc` 先判；默认优先 `update-doc`，`analysis-only` 禁止。`强制`
- `skills/harness/progressive-disclosure-docs/SKILL.md:269-286` — 新功能后同任务更新 owning README/feature INDEX/OVERVIEW/changelog+接口/验证文档。`强制`
- `skills/harness/progressive-disclosure-docs/SKILL.md:316-324` — 目录自检：索引路由同步、上级反链完整性检查。`强制`

**4) Grill / 澄清 / 用户询问相关**
- `skills/harness/add-idea/SKILL.md:25-30` — “Investigate repo facts; ask user only for decisions”；无最终确认前不写持久文档。`强制`
- `skills/harness/add-idea/SKILL.md:73-76` / `81-86` — ambiguous 时进入 Grill；每次只问一个问题并给推荐答案。`强制`
- `skills/harness/add-idea/SKILL.md:88-99` — 所有阻塞问题解完后再请求用户确认。`强制`
- `skills/harness/add-idea/references/routing-contract.md:34-39` / `41-42` — `GRILL_REQUIRED` 分类与只 Grill 会影响 boundary/行为/安全/回滚问题。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:35-43` — 明确 user intent 列表（实现/调整主线/修 bug/询问行为）。`强制`
- `skills/harness/project-docs-workflow/SKILL.md:144-148` / `157-159` — 升级 `project-analysis` 的触发包含“用户询问已实现细节、版本行为差异”等。`可选`
- `skills/harness/external-collaboration-workflow/SKILL.md:64-65` / `69-70` — 来源版本/commit 缺失时停止评审并请求澄清。`强制`
- `skills/harness/progressive-disclosure-docs/SKILL.md:90-93` / `315-322` — 用户问题若影响合同/授权才提问；否则以会话理解后继续。`强制策略`

**5) 模板 / 资产（与规则映射）**
- `skills/harness/progressive-disclosure-docs/assets/feature-template/INDEX.md:5-15` — feature-template 的索引任务映射：requirements/specs/decisions/changelog。`强制`
- `skills/harness/progressive-disclosure-docs/assets/feature-template/requirements.md:18` / `53-59` — requirements 模板包含 expected/acceptance/NFR/stop rules。`强制`
- `skills/harness/progressive-disclosure-docs/assets/spec-template.md:45-75` / `87-95` — Spec 模板包含 module/state ownership、validation matrix、测试或检查、pass criteria。`强制`
- `skills/harness/progressive-disclosure-docs/assets/spec-index-template.md:7-15` / `13-15` — Spec 索引模板、ID 不可变、freeze gate 要求。`强制`
- `skills/harness/progressive-disclosure-docs/assets/adr-template.md:20` / `28-33` / `51-55` — ADR 模板上下游关系与相关 contracts。`强制`
- `skills/harness/progressive-disclosure-docs/assets/decision-index-template.md:5-14` — ADR 索引模板与“只读当前相关 ADR/不默认加载历史 ADR”策略。`强制`
- `skills/harness/external-collaboration-workflow/assets/case-template/INDEX.md:47-75` / `42-44` — 外部 case 关联的 adoption matrix 与 SSOT 转译状态。`强制`
- `skills/harness/external-collaboration-workflow/assets/case-template/problem-statement.md:42-60` / `72-74` — 题包字段包含 expected behavior / gap / 验证矩阵 / test ownership。`强制`
- `skills/harness/external-collaboration-workflow/assets/case-template/external-proposal.md:51-60` — 外部方案转写提纲（interfaces/data flow/state/file budgets/test matrix）。`强制`
- `skills/harness/document-organization-harness/assets/demo-harness/AGENTS.md:9-13` / `98-103` — docs-first、阶段性路由、非 trivial 变更同步 tests/docs 的 demo 规则。`可选（演示骨架）`
- `skills/harness/document-organization-harness/SKILL.md:29-33` / `40-47` — 文档树（requirements/specs/decisions）与 owning GOAL/README 要求。`强制`

**6) 注册与说明文档**
- 根 `README.md:15-21` — 列出 harness 全套入口及用途简介（`harness/*` 协同套件入口）。`强制`
- `.claude-plugin/marketplace.json:22-28` — 注册路径枚举：`./skills/harness/{add-idea,document-organization-harness,external-collaboration-workflow,progressive-disclosure-docs,project-analysis,project-docs-workflow,refactor-large-modules}`。`强制（当前仓库插件注册）`
- `skills/harness/README.md:75-82` — Repo-local skills 汇总清单（以 `.agents/skills/harness/...` 形式列出）。`强制（本套件维护指引）`
- `skills/harness/document-organization-harness/references/harness-bootstrap.md:97-103` — 注册清单要求：每个 skill 有触发器且可扩展到仓库本地注册。`强制`
- `skills/harness/UPGRADING.md:61-67` — 维护顺序中明确列出本次变更关联的 harness surfaces（含 `feature-spec-decision-contract`、`add-idea` 等）。`强制`

**7) 相互引用关系与可能失效链接**
- 相互引用链（存在）：
  - `skills/harness/add-idea/SKILL.md:18-20` → `progressive-disclosure-docs/references/feature-spec-decision-contract.md`
  - `skills/harness/add-idea/SKILL.md:7-9` / `skills/harness/project-docs-workflow/SKILL.md:56-58` → `add-idea`（互为前置）
  - `skills/harness/project-docs-workflow/SKILL.md:69-71` → `../progressive-disclosure-docs/references/mainline-route-contract.md`
  - `skills/harness/project-docs-workflow/SKILL.md:157-158` → `project-analysis`
  - `skills/harness/project-analysis/SKILL.md:80` → `metadata` scan script/辅助
  - `skills/harness/external-collaboration-workflow/SKILL.md:88-94` → `project-docs-workflow`、requirements、Spec、ADR、changelog
  - `skills/harness/progressive-disclosure-docs/SKILL.md:55` → `feature-spec-decision-contract.md`
  - `skills/harness/document-organization-harness/references/harness-bootstrap.md` → `add-idea`/`project-docs-workflow`/`external-collaboration-workflow` 等。
- 可能失效/上下文依赖链接（按源仓库当前结构）：
  - `skills/harness/README.md:46` 的 `docs/OVERVIEW.md` 在仓库根不存在（源仓库无 `docs/` 目录），因此文档内链接在本仓库上下文下不可访问。`高`
  - `skills/harness/progressive-disclosure-docs/SKILL.md:46`、`skills/harness/document-organization-harness/references/harness-bootstrap.md:21` 同样指向仓库缺失的 `docs/OVERVIEW.md`（源仓库缺少目标文档）。`中`
  - `skills/harness/progressive-disclosure-docs/assets/spec-template.md:17`、`.../spec-index-template.md:3`、`.../decision-index-template.md:3`、`.../adr-template.md:20`、`.../feature-template/INDEX.md:3` 等均为模板文件内相对链接，当前源路径下无对应目标文件（需在目标项目实例化/渲染后成立）。`中`
  - `skills/harness/external-collaboration-workflow/assets/case-template/problem-statement.md:35` / `INDEX.md:33` / `INDEX.md:33-34`：引用 `../../feature/FEATURE_SLUG/README.md`（占位特征路径，未在当前源仓库实例化）。`中`

**未找到与歧义**
- 未在 `skills/harness/**`、根 `README.md`、`.claude-plugin/marketplace.json` 的检索范围内发现明确 `TDD`/`tests-first` 的术语或强制规则（出现为“测试/validation matrix/test owner”等，但非“测试优先/测试驱动开发”短语）。`未发现直接条款`

**Acceptance Report（结构化）**