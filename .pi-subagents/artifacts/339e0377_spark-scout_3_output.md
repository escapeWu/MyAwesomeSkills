已按只读方式完成目录盘点。主要结论如下（基于可直接定位的 `file:line` 引用）：

- `AGENTS.md:1-5`、`AGENTS.md:59-77`、`AGENTS.md:85-95` 明确仓库治理入口与“先读文档 + 分层约束 + 强制执行门（非平凡任务）”的主线要求。
- `CLAUDE.md:1-8` 明确 docs-first 约束和架构同步要求（读 `docs/OVERVIEW.md`、更新 docs 与实现一致）。
- `.cursor/rules/harness-execution.mdc:8-31` 明确了 `taskBoard` 先行、契约先行、逐 milestone gate、测试与归档闭环为“强制执行流程门”。
- `.agent/skills/harness` 当前可见技能（已安装/存在）仅 3 个：  
  - `.agent/skills/harness/project-docs-workflow/SKILL.md:1-3`  
  - `.agent/skills/harness/project-analysis/SKILL.md:1-3`  
  - `.agent/skills/harness/progressive-disclosure-docs/SKILL.md:1-3`  
  对照 `AGENTS.md:47-57`，声明的技能集合还包含 `code-organization-harness`、`codex-design-review`（当前文件系统与技能文件实际可见范围存在偏差）。
- `git status --short` 与 `find` 扫描显示 `.agent/skills/harness/harness-engineering-plan/SKILL.md` 与 `.../code-organization-harness/SKILL.md`、`.../codex-design-review/SKILL.md` 等文件处于 D（被删除）状态（未恢复到工作树）：
  - `git status --short` 显示多条 `D .agent/skills/harness/...SKILL.md`。
  - `find .agent/skills/harness -maxdepth 2 -type f -name 'SKILL.md'` 仅输出 3 个文件（无 `harness-engineering-plan/SKILL.md`）。
- `docs/feature/INDEX.md:20-22` 明确“多 wave/multinode 工作上下文在 `.../harness-engineering-plan/tasks/<module>/taskBoard.md`”；对应流程证据在 `project-docs-workflow` 与 `.cursor/rules` 中均有描述（`project-docs-workflow:16-17`, `22-23`, `53-54`, `155-158`，`.cursor/rules:22-31`）。
- `Spec/requirements/ADR 生命周期` 强制路径：
  - Requirements/预期行为路径：`AGENTS.md:59-60`（implementation 后先扫 `requirements`）、`AGENTS.md:62-64`（非平凡任务必须执行流程）、`project-docs-workflow:16-18`（对比 requirements 与 README/INDEX）。
  - `project-analysis:12-13,82-89,95` 明确 `requirements.md` 为 expected behavior/验收源。
  - `progressive-disclosure:49-53,211` 明确 `requirements.md` 与 `README/INDEX` 的职责分离与归档生命周期判断标准。
  - `ADR`：项目当前未检索到任何 ADR 命名文件（`find docs -pattern "**/*ADR*.md"` 无结果）；`docs` 现有目录下只有 `feature/signal-plugin-framework/requirements.md`（`find docs -pattern "**/requirements.md"` 命中 1）。
- `TDD/testing-first`：未检索到明确“testing-first/TDD”语义短语（见空结果检索）。
- Pre-doc/文档优先与同步更新：
  - `project-docs-workflow:166-167,18-21` 要求功能变更后“提炼结论更新 docs”，并在 taskBoard 完成后归档。
  - `AGENTS.md:90-95` 要求任务完成后测试与 `docs/OVERVIEW.md` 同步，且 backend tests README 与实现匹配。
- `taskBoard/MAINLINE route` 现有可定位主线为文档路由：
  - `docs/OVERVIEW.md:64-66`（主入口 + feature/reference/archive 索引）
  - `docs/feature/INDEX.md:1-6,18-22`（功能索引到 taskBoard）
  - `docs/reference/INDEX.md:1-3`（参考索引）
  - 未检索到明确“MAINLINE”术语或独立 MAINLINE 文档路径。
- `provider / local extras` 证据：
  - 依赖 extras：`backend/pyproject.toml:16-21`（`extra = "dev"`）以及 `project` 里的标准 extra 包依赖 `uvicorn[standard]`、`httpx[socks]`（`lines 8-13`）；
  - provider 层存在：`backend/app/providers/__init__.py:1`、`docs/reference-architecture.md:87`、`docs/feature-ccxt-relay.md:243-247`（ccxt connector provider 结构）；
  - local provider-like 入口（coinglass 池化请求）在功能文档中有配置路径：`docs/feature-coinglass-liquidation.md:43-47`（`fetcher_pool`+代理池）与 `117-118`（可配代理 URL 列表）。

- 覆盖范围与排除项：
  - 覆盖范围：`AGENTS.md`、`CLAUDE.md`、`.cursor/rules/harness-execution.mdc`、`.agent/skills/harness/*`、`docs/*`、`backend/pyproject.toml`、`backend/app/providers`、`backend/tests/README.md`、`docs/feature-coinglass-liquidation.md`、`docs/feature-ccxt-relay.md`、`git status` 与 `find/ripgrep` 结果。  
  - 未覆盖：未做代码语义推断/行为判断（按你的要求只读）；未做命令外执行/测试运行；未触达未在仓库根路径下的外部历史（`git status` 之外的未列目录）。

最小升级建议：
1. 可补齐/还原缺失的 harness 技能 SKILL 文件（当前声明 5 项 vs 实际可见 3 项）并清理 `docs`/`harness` 中不一致引用，避免扫描与执行流程分歧。
2. 若需要“MAINLINE route”可明确定义一个与文档路由一致的术语（例如在 `AGENTS.md` 新增显式条目），并补齐 `ADR` 入口（若组织策略要求）。