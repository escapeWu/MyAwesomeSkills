已完成只读盘点。未修改任何文件。

- 已安装/可见 Canonical Harness Skills（均有 SKILL 注册，`name` 字段可识别）  
  - `.agents/skills/freqai-rl-development/SKILL.md:2-3`（name: `freqai-rl-development`，含 `description`）  
  - `.agents/skills/harness/project-docs-workflow/SKILL.md:2-3`（name: `project-docs-workflow`）  
  - `.agents/skills/harness/project-analysis/SKILL.md:2-3`（name: `project-analysis`）  
  - `.agents/skills/harness/external-collaboration-workflow/SKILL.md:2-3`（name: `external-collaboration-workflow`）  
  - `.agents/skills/harness/progressive-disclosure-docs/SKILL.md:2-3`（name: `progressive-disclosure-docs`）  
  - `.agents/skills/harness/refactor-large-modules/SKILL.md:2-3`（name: `refactor-large-modules`）  

- 治理文件可见性  
  - `AGENTS.md:1-205` 存在且作为入口（包含安全、权限、路由、行文规则）。  
  - `CLAUDE.md` 不存在（`[ -f CLAUDE.md ] && ...` 命令返回 `missing`）。  
  - `.cursor` 不存在（`[ -f .cursor ] && ...` 命令返回 `missing`）。  

- Git/Worktree 状态（只读）  
  - `git status --short --branch`：未暂存修改在 `M .gitignore`、`M docs/feature/reinforcement-trading-part-2-reproduction/INDEX.md`、`M docs/feature/reinforcement-trading-part-2-reproduction/changelog.md`，以及 `??` 新文件 7 个（见命令输出）。  
  - `git diff --cached --name-only`：无 staged 文件（空输出）。  
  - `git worktree list`：当前分支为 `codex/regime-engineering-goal`，另有主 worktree 分支 `develop`。  

- Spec / requirements / 生命周期（含“ADR”路径）  
  - 预期行为归属：`docs/feature/reinforcement-trading-part-2-reproduction/requirements.md:1-205`（文档说明 expected behavior、范围、停止与完成条件）。  
  - 运行状态/生命周期归属：`docs/feature/reinforcement-trading-part-2-reproduction/README.md:29-39`（`CURRENT DEVELOPMENT MAINLINE`、`IMPLEMENTATION_ACTIVE`、里程碑与门禁）。  
  - 全局生命周期模板：`docs/reference/research-docs-workflow.md:87-95`（`PROPOSED -> CONTRACT_FROZEN -> IMPLEMENTATION_ACTIVE -> VALIDATION_ACTIVE -> ...`）。  
  - 外部协作生命周期：`docs/reference/external-collaboration-workflow.md:1-21` 和 `11-22`（`PROBLEM_DRAFTING -> ... -> CLOSED_ACCEPTED`）。  
  - 严格 ADR 文档（按 `ADR*` 名称）未检出：`find docs -name "*ADR*.md"` 无结果。  

- TDD / testing-first / pre-doc gate / docs 同步  
  - `docs/reference/research-docs-workflow.md:176-182`：研究文档变更至少要求运行 `validate_research_docs.py`、`validate_code_organization.py`、`tests/test_docs.sh`（可视作 pre-doc governance gate）。  
  - `AGENTS.md:89-90` + `docs/reference/research-docs-workflow.md:156-172`：实施前后要先读 docs 路线、确认状态、并有实施前后更新要求。  
  - `docs/reference/research-docs-workflow.md:134-145`：变更后 README/changelog/docs 验证矩阵要求，含 state transition、next gate。  
  - 未检出“显式 `TDD`/`testing-first` 专有口径字符串”，但存在“开发前/后测试优先级”与文档门禁（如 `AGENTS.md:140-143` 和 `project-docs-workflow`/skill 文档）。  

- taskBoard / MAINLINE route 与任务线  
  - MAINLINE 路由入口：`docs/OVERVIEW.md:10-15`、`docs/feature/INDEX.md:5-9`（BTC v2.0 标记为 `CURRENT DEVELOPMENT MAINLINE`）。  
  - 任务进入规则：`docs/feature/INDEX.md:24-29`（先读模块 INDEX/README，再按需读 requirements）。  
  - taskBoard 退役与文档化迁移：`docs/reference/research-docs-workflow.md:163`（废弃活动 taskBoard 表述）、`docs/reference/research-docs-workflow.md:188-190`、`docs/feature/reinforcement-trading-part-2-reproduction/README.md:57`（taskBoard 已退出活动进度控制面）、`.../changelog.md:27`（迁移确认）。  

- Provider / local extras 识别  
  - `pyproject.toml:[project.optional-dependencies]`（`plot`/`hyperopt`/`freqai`/`freqai_rl`/`develop`/`all`/`dev`）及 `all`/`dev` 复合引用：`pyproject.toml:80-134`。  
  - requirements 分层 extras：`requirements-dev.txt:2-7`（`-r` 包含其他文件）+ 各模块 `requirements-*.txt` 的 `-r` 与模块依赖（如 `requirements-freqai.txt:2-3`, `requirements-freqai-rl.txt:2,4-11`, `requirements-hyperopt.txt:2-8`, `requirements-plot.txt:2-4`, `docs/requirements-docs.txt`）。  
  - MkDocs providers：`mkdocs.yml:121-127`（`extra.version.provider: mike`，`extra.analytics.provider: google`）。  

- 覆盖范围与排除项  
  - 实际检索范围：`AGENTS.md`、`.agents/skills/**/SKILL.md`、`docs/OVERVIEW.md`、`docs/feature/**`、`docs/reference/**`、`requirements*.txt`、`pyproject.toml`、`mkdocs.yml`、Git 状态命令输出。  
  - 未全量读 `docs/`（仅按治理索引和关键文件读取）。  
  - 未发现新增的 test/源码相关问题证据（只读扫描）。  

最小升级建议：
1. 若希望“ADR 生命周期”被精确满足其名称语义，建议在 `docs/feature/reinforcement-trading-part-2-reproduction` 下补一份 `ADR` 命名的架构决策记录模板或在 `reference` 中新增 ADR 索引声明。  
2. 如需更严格对齐“TDD/testing-first”术语，可在 `AGENTS.md` 或 `docs/reference/research-docs-workflow.md` 增加一条显式测试优先序列（例如 `RED -> GREEN -> REFACTOR` 或 `tests-before-contract`）与示例场景。