已完成只读盘点，结果如下（按证据优先级）。

- `file:line` 依据
  - `.agents/skills/harness/code-organization-harness/SKILL.md:10-20`  
    - 说明该 harness 被安装/定义；含“mirror to docs and tests”与 `requirements.md`/`references` 更新规则（例如 `requirements.md`、`docs/reference/interfaces.md`）。
  - `.agents/skills/harness/progressive-disclosure-docs/SKILL.md:12-16, 49-53, 66-74, 96-106, 118-129, 177-187, 197-212`  
    - 定义分层治理骨架（AGENTS/OVERVIEW/docs）；明确 requirements/readme分工；定义 SSOT 验收流程；列出 taskBoard 临时执行文件路径；要求 docs 同步。
  - `.agents/skills/harness/project-docs-workflow/SKILL.md:16-23, 115-137, 146-151, 153-158, 166`  
    - 规定执行前读 docs 与 taskBoard；docs变更回流；列出 docs 更新触发项；taskBoard 完成后蒸馏进 SSOT。
  - `AGENTS.md:10-13, 27-54, 61-65`  
    - AGENTS 本体要求“先读 docs/OVERVIEW”和“接口/契约/运行方式变更必须同步 owning docs”；禁止全量读 docs；明确证据边界。
  - `docs/feature/INDEX.md:3-12, 30-47, 53-56, 148-166`  
    - 实现了“先读模块索引”的主路由；在入口清单中标注 requirements/README/数据模型关系；提供常用读取路径。
  - `docs/reference/INDEX.md:66-74, 68-74`  
    - 引用 docs/测试/运行入口与 `runbook-testing.md`（当前为“待补”），并声明缺失文件应补齐（`docs/reference/runbook-testing.md`）。
  - `docs/OVERVIEW.md:5-14, 26-34, 51-77`  
    - 维护“主链路”与模块入口路由；禁止执行上下文落 `docs/`；明确主链路与 Step1..Step7 路由。
  - `docs/feature/step4-candidate-events/requirements.md:1-97`  
    - 示例需求文档：`Expected behavior` 明确且结构化（契约型要求、PIT、主线约束），支持“requirements 生命周期”治理证据。
  - `docs/feature/time-grid-continuous-scoring/H_RR_SINGLE_ARCHITECTURE_RCA.md:1-7`  
    - 命名为 “Architecture Decision / RCA”，属于 ADR/决策类文档方向证据；明确 readonly 与结论边界。
  - `docs/topbottomUpgrade/TOPBOTTOM_FROZEN_CONCLUSION_20260707.md:9-18, 95-98`  
    - 显式 decision record 与冻结结论（可作为非主线 ADR 类证据对照）。
  - `docs/long_term_goals_and_current_progress.md:116-117, 130-133, 142`  
    - 标明当前/下一主线（主线路由）：`下一主线`与 `H-RR` 的当前研究主线状态与阻塞边界；对应任务总控与 mainline/主线演进定位。
  - `docs/archive/INDEX.md:1-5, 16-22`  
    - 明确 archive 任务是历史/已完成 taskBoard 的沉淀仓；并非持续真相源。

- 未发现 / 未命中（按反证）
  - `rg -n --hidden --files -g '.cursor*' -g 'CLAUDE.md' .` 仅返回 `./AGENTS.md`（命令输出无 CLAUDE.md 或 .cursor 文件）。
  - 未检索到明确 `TDD`/`testing-first`/“pre-doc gate” 关键短语（全库 `.md` 级检索无显式命中）。
  - “provider/local extras”术语未见成组配置项；仅见本地数据源规则（例如 `README.md:86-91`）与 provider 类本体性文字，不是“provider/local extras”配置块。

- 变更与执行状态
  - 严格只读扫描，未做文件修改。
  - git 状态已确认：无暂存项（`git diff --name-only --cached` 空；`git status --short | awk '{print $1}'` 仅 `??`/`M` 工作区状态）。

最小升级建议（按优先级）
1. 高：把 “TDD/测试优先（至少 testing-first）”与 “pre-doc gate（文档入场前门禁）”写入 `.agents/skills/harness/project-docs-workflow/SKILL.md` 的强制流程并链接到 AGENTS/OVERVIEW（当前仅见 SSOT/Docs流程，不是明确 pre-doc/test-first）。
2. 中：创建并落地 `docs/reference/runbook-testing.md`（`docs/reference/INDEX.md` 已声明待补），并在 `docs/reference/INDEX.md` 标注 route 回指，避免 reference 流水化断链。
3. 中：把 `H-RR`/主线切换、taskBoard 与主线状态同步约束（例如从 `输出/plan` 到 `OVERVIEW + feature/INDEX`）收敛为一个最小脚本化 checklist，避免同义/重复状态漂移。