已完成扫描：只读盘点、未做任何文件修改。

### 关键发现（按 `file:line`）
- **canonical harness skills 已登记**：根 `AGENTS.md` 的 “Repo-local Skills” 段明确列出 8 个 harness 技能（add-idea、document-organization-harness、project-analysis、project-docs-workflow、external-collaboration-workflow、progressive-disclosure-docs、refactor-large-modules、et-home-research-runner）；见 `AGENTS.md:114-131`。
- **治理文件清单（AGENTS/CLAUDE/.cursor）**：
  - 根治理入口文件：`AGENTS.md`（见 `AGENTS.md:1`）。
  - 本仓库未发现 `CLAUDE.md`（`find` 未命中）。
  - 另见 demo-harness 入口治理：`.agents/skills/harness/document-organization-harness/assets/demo-harness/AGENTS.md:1-58`。
  - Cursor 规则文件存在且可追溯：`.agents/skills/harness/document-organization-harness/assets/demo-harness/.cursor/rules/harness-execution.mdc:1-29`。
- **MAINLINE 路由治理**：
  - 唯一当前主线入口集中在 `docs/OVERVIEW.md`（`docs/OVERVIEW.md:10-18`，表头 `CURRENT DEVELOPMENT MAINLINE`）。
  - 同步路由入口在 `docs/feature/INDEX.md`，并明确“仅标识当前 feature，当前路线状态在 owning README”：`docs/feature/INDEX.md:5-12`。
  - 该主线 feature 自身入口要求先读 `INDEX` 再路由到 owning README（`docs/feature/reinforcement-trading-part-2-reproduction/INDEX.md:1-16`）。
- **Spec/requirements/ADR 生命周期约束仍在执行**：
  - 根治理直接要求：expected behavior/acceptance 在 requirements，bounded Spec，accepted ADR 持久化；见 `AGENTS.md:103-106`。
  - feature 文档模板进一步规定：requirements、`specs/`、`decisions/`、`changelog` 分工（含 Spec/ADR 生命周期/迁移历史）：`.agents/skills/harness/progressive-disclosure-docs/assets/feature-template/README.md:97-109`。
  - 当前主线 requirements 真实存在并定义预期行为与停止规则：`docs/feature/reinforcement-trading-part-2-reproduction/requirements.md:1-11`、`30-49`。
- **testing-first / pre-doc gate（测试与预检）**：
  - 有“先聚焦测试后广泛检查”的顺序要求（非 literal `TDD` 但行为等价）：`docs/reference/code-organization.md:93-95`、`AGENTS.md:109-110`（变更需同步 owning docs）以及 `.agents/skills/.../document-organization-harness/AGENTS.md:100-103`。
  - docs 相关变更有固定验证门：`docs/reference/research-docs-workflow.md:214-216` 与 `docs/OVERVIEW.md:80-82`。
  - **未检索到**仓库内明确字符串 `TDD`/`testing-first`（仅未逐项写死为 TDD 命名法，但存在测试优先顺序）。该点已按“证据缺口”标注为无显式术语而非无行为。
- **taskBoard 与路由同步**：
  - 根治理禁止把 taskBoard 当活动进度控制面：`AGENTS.md:94`。
  - 外部协作与研究-docs workflow 也显式：`docs/reference/external-collaboration-workflow.md:114`、`docs/reference/research-docs-workflow.md:196`、`225`。
  - 主线路线/状态不在外层重复分散，集中到 owning README 与对应索引：`docs/OVERVIEW.md:16-18`。
- **provider / local extras 识别**：
  - 包含标准可选依赖（extras）定义：`pyproject.toml:[project.optional-dependencies]`，含 `plot/hyperopt/freqai/freqai_rl/develop/jupyter/all/dev`；见 `pyproject.toml:80-134`.
  - uv lock 显式记录 extras 提供与 marker 绑定：`uv.lock:1347-1423`，及总清单 `uv.lock:1425`.
  - mkdocs 文档端“provider”字段（非 pip extras 语义）：`mkdocs.yml:121-127`（`provider: mike` / `provider: google`）。
- **工作区状态（扫描一致性）**：
  - `git status --short --branch` 显示大量未暂存/未跟踪更改：`git status` 命令输出（首屏含 `M`/`??` 多项），且未出现 staged 条目（未见 `M ` 前缀）。  

### 任务覆盖与可执行建议
1. 建议补齐一条明确的“testing-first”术语映射文档（例如在 AGENTS/research-docs-workflow 内新增短语映射），减少术语歧义。
2. 建议在本次审核后若要继续开发，先执行一次 `python3 scripts/validate_research_docs.py` 与 `bash tests/test_docs.sh` 的干净基线验证。