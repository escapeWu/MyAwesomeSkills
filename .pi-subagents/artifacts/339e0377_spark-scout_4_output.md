- AGENTS / CLAUDE / .cursor 盘点  
  - `AGENTS.md:1` 根治理总纲。  
  - `AGENTS.md:54` 明确禁止把 `taskBoard`/`.agents/tasks` 作为活跃控制面。  
  - `AGENTS.md:63-71` 枚举并注册了 `harness` 技能清单（`add-idea`, `document-organization-harness`, `progressive-disclosure-docs`, `project-analysis`, `project-docs-workflow`, `external-collaboration-workflow`, `refactor-large-modules`）。  
  - `AGENTS.md:75-77` 枚举并注册了报告技能：`report-chapter-one-generation`, `build-reference-filemap`, `extract-reference-metadata-tags`。  
  - `.cursor/rules/harness-execution.mdc:1-4` 文件存在且 `alwaysApply: true`，定义执行门控。  
  - `.cursor/rules/harness-execution.mdc:8-17` 定义实现前必须完成的先置检查与逐门验证收口。  
  - `? CLAUDE.md`：未检出任何 `CLAUDE.md`（`rg --files | rg 'CLAUDE\.md'` 无输出）。  
- Spec/requirements/ADR 生命周期与主线路由/任务板约束可追溯  
  - `AGENTS.md:10,39,48-50,54` 明确：expected behavior 归 `requirements.md`，实现合同归 frozen Spec，架构择留归 accepted ADR；并禁止 taskBoard；非 trivial 前要走 frozen Spec/ADR/validation 之类流程。  
  - `AGENTS.md:54` 及 `.cursor/rules/harness-execution.mdc:12-17` 强制实现前检查与持续回写文档。  
  - `.agents/skills/harness/progressive-disclosure-docs/references/feature-spec-decision-contract.md:71-87` 直接写明 Spec 生命周期（`DRAFT -> FROZEN -> IMPLEMENTATION_ACTIVE -> VALIDATION_ACTIVE -> VALIDATED/REJECTED/SUPERSEDED`）与 ADR 生命周期（`PROPOSED -> ACCEPTED/REJECTED -> SUPERSEDED`）。  
  - `.agents/skills/harness/progressive-disclosure-docs/references/feature-spec-decision-contract.md:137` 约束：阻塞 ADR 未 ACCEPTED 前依赖它的 Spec 不可冻结。  
- Docs sync（实现前后文档同步）与测试优先（TDD/验证优先）  
  - `AGENTS.md:47-52`：非 trivial 开发前后要求确定 requirements/spec/ADR、完成目标切片后同步 owning docs/changelog/evidence。  
  - `AGENTS.md:86-92`：测试规则明确“先聚焦验证，再进行范围匹配的广泛检查”，要求真实聚焦/全量测试命令登记。  
  - `.agents/skills/harness/progressive-disclosure-docs/SKILL.md:473-489` 明确“代码改动后未更新 owning docs/INDEX/OVERVIEW = 常见故障”。  
  - `docs/reference/runbook-testing.md:17-24` 验收清单含“每个 leaf 可返回父级、六个（文中描述）harness skill 路径真实存在”。  
- Provider/local 约束与“extras”（可识别清单）  
  - `docs/feature/report-generation/requirements.md:94-142` 明确本地运行边界：`MVP` 本地单机处理、不上传整体资料包、不用 Web 搜索、不启用外部队列，工具默认只读，外部写操作不在 MVP。  
  - `docs/reference/architecture.md:15,37-39` 指明外部适配层（provider/parser/SQLite/filesystem/DOCX）与业务层分离，orchestrator 不导入 provider SDK。  
  - `docs/reference/architecture.md:49` 与 `docs/feature/report-generation/design.md:27`、`docs/reference/code-organization.md:15,20,39` 明确 provider 适配层与本地配置/授权/本地 artifact 的边界（OpenAI/ local policy/provider-neutral port/fake adapter）。  
- MAINLINE/路由状态约束与执行状态  
  - `AGENTS.md:54` 明确任务面板类控制面禁用。  
  - `.agents/skills/harness/project-docs-workflow/SKILL.md:64-70` 明确先读 `OVERVIEW` 的唯一 `CURRENT DEVELOPMENT MAINLINE`，并要求主线变更遵循 `mainline-route-contract.md`。  
  - `mainline-route` 标记搜索在项目 `docs/` 里仅出现在模板/规范中（`rg -n "MAINLINE-ROUTE:START"` 命中：`.../references/mainline-route-contract.md` 与 `.../assets/feature-template/README.md`），而未发现当前 feature/OVERVIEW 的实际 active manifest（见后续“未覆盖项”）。

- 未覆盖 / 需注意项  
  - 未找到 `CURRENT DEVELOPMENT MAINLINE` 的实例状态（`rg` 在 `docs/OVERVIEW.md docs/feature docs/reference` 下无输出）。  
  - 未发现项目层 `CLAUDE.md`，仅存在 `.cursor/rules` 与根 `AGENTS.md` 约束。  
  - 根文档与规范要求/工具中存在数量与口径差异：`runbook-testing.md` 说“六个 harness skill 路径”，而根 AGENTS 注册并执行了 7 个 harness 技能（`add-idea...refactor-large-modules`）。

- 已安装技能目录（当前仓库实际）：  
  - 通过 `ls .agents/skills` / `ls .agents/skills/harness` 观测到 `build-reference-filemap`、`extract-reference-metadata-tags`、`harness`、`report-chapter-one-generation`（包含注册与非注册技能并存，属于可读目录级证据，非文件行号证据）。

- Git 状态（用于 no-staged 判断）  
  - `git status --short --branch` 结果含大量 ` M`/`??`，未见以空格前缀反映 staged 改动（未有 `M `、`A `、`D ` 等 index 状态）。
  - 注：存在工作区脏乱；本任务未改文件。

- 覆盖范围与排除  
  - 覆盖：`AGENTS.md`、`.cursor/rules/harness-execution.mdc`、`.agents/skills/harness/*`（README/UPGRADING/SKILL/refs）、关键 `docs`（`OVERVIEW`、`feature/report-generation/*`、`reference/*`）、相关命令输出。  
  - 排除：未做运行时实现/源码语义测试；未展开 `.agents/skills` 下除目录/文档之外的脚本深度执行（只读检索）。

- 最小升级建议  
  1. 在当前 feature/OVERVIEW 链路补齐一次可达的 `MAINLINE-ROUTE` 路由状态快照（或确认与规范一致的“无 active route”状态）。  
  2. 将 `runbook-testing.md` 中“六个 harness skill 路径”与实际注册口径（含 `report-chapter-one-generation`）对齐，避免执行时口径漂移。  
  3. 如需保留 `CLAUDE.md` 入口，在根层建立并说明其优先级与 `AGENTS.md` 关系；当前可运行仍正常，但“无 CLAUDE”应被明确记录。