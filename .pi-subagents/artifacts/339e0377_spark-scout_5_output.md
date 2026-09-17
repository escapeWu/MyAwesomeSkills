已完成只读盘点，未改仓库。  
分类如下（每条均有可复核来源）：

**已强制（有明确证据）**
- `AGENTS.md:95-99` 明确把 `.claude/skills/harness-engineering-plan`、`.claude/skills/project-docs-workflow`、`.claude/skills/project-analysis` 作为内置治理入口，并规定**≥2 wave 或 ≥5 TaskNode 的新里程碑必须先生成 taskBoard**。  
- `AGENTS.md:9-14,74-77,81-84,99,113-117` 强制 docs-first、分层契约、真实路径测试、docs 路由同步、工作树开发和测试同步等（含接口改动必须同步到 `docs/reference/interfaces.md` + `frontend/src/types/index.ts`）。  
- `AGENTS.md:29-34,43-44,50-51,57` + `docs/feature/INDEX.md:33-35` 规定逐层读取索引与仅按需读 docs（含 taskBoard）；`taskBoard.md`属执行上下文，不是默认首次读取。  
- `AGENTS.md:84-91` 对提案生命周期施加硬约束：`README.md`、`design.md`、`spec.md`、`acceptance.md` 4 件套（≥500 行单文件提案必须拆分）。  
- `CLAUDE.md:5-7` 再次要求先读 `AGENTS.md` + `docs/OVERVIEW.md`、按渐进式披露读取 docs，并保持 docs/API/Types/Tests 同步。  
- `sandbox/README.md:33-35` 和 `docs/reference/architecture.md:273-275` 明确：仓库不使用 GitHub Actions/GitLab CI；自动化要么走 host scheduler，要么走 Linear→symphony→Codex。  
- `project-docs-workflow/SKILL.md:14-20,40-20,100-133` 要求开发前先读相关 docs，并在实施后评估是否需 docs 补齐；有变更需先征得用户确认。  
- `harness-engineering-plan/SKILL.md:20-25,27-30,107-114,119-120` 规定 milestone 波次/交付门控、先约束后实现、集成 gate、tests 需证明合同（不是仅凭测试通过）。  
- `docs/OVERVIEW.md:5-5` 将仓库定位为 docs-first + typed contracts + 禁止交易执行/敏感信息回显。  
- Git 与工作树状态证据：当前分支 `codex/services-modules`，提交 `3db566b`，工作树干净（`git status --short` 无输出）、`git diff --stat` / `git diff --cached --stat` 均空；`git worktree list --porcelain` 仅列出主仓与当前工作树。  

**仅建议/软约束（偏执行流程/质量实践）**
- `project-docs-workflow/SKILL.md:117-151,166-170` 建议文档影响评估、保持轻量流程、避免过度引入文档动作（执行前提下）。  
- `harness-engineering-plan/SKILL.md:57-75` 给出波次图形表达和排版规范（风格约束，非语义级硬规则）。  
- `AGENTS.md:56` 及 `docs/reference/architecture.md:248-250` 对 sandbox 配置/阅读顺序的路径提示，属于关键执行守则但在语义上为约束执行链路而非独立里程碑制度。  

**未发现/待标注**
- 未检索到仓库内的 `.cursor` 治理文件：`find . -name ".cursor*"` 未返回结果。  
- 未在根治理文件看到“显式 ADR 生命周期”统一条款；仅见部分模块在 index 中提到 ADR（如 `docs/feature/INDEX.md:17` 的“worker拓扑 ADR”标签）但非 ADR 提交/评审的强制流程。  
- 未发现 `MAINLINE`（大写）固定术语作为专有 route；能证实的“主线流”是里程碑/TaskBoard驱动后再合并到 main（例如 `docs/feature/ai-evaluation/win-rate-evolution/evolution-2026-05/milestone-2/taskBoard.md:146-149`，`docs/feature/ai-evaluation/win-rate-evolution/evolution-2026-05/progress-track.md:43-45`）。  

**provider / local extras（精确来源）**
- 自定义 model provider 为仓库级本地配置：`sandbox/codex-config.toml:1-2,12-16`（`model_provider = "custom"`，`base_url`，`wire_api = "responses"`，`approval_policy = "never"`，`sandbox_mode = "danger-full-access"`）。  
- `docs/feature/ai-evaluation/win-rate-evolution/feat-G3-architecture-brief.md:197` 与 `209-217` 同步说明了 Codex provider 本地化配置策略。  
- `docs/reference/architecture.md:273-279` 与 `sandbox/README.md:33-35,45-46,196-197` 再次补齐自动化链路与外部 API 约束（GitHub REST、`LINEAR`、`OPENAI`、`GITHUB_TOKEN` 等）为执行约束；`sandbox/README.md:197` 标注 `Do NOT modify tests/|docs/`（仅代码面向改动）。  

**已读文件索引（治理与任务文件）**
- `AGENTS.md`, `CLAUDE.md`, `frontend/AGENTS.md`
- `.claude/skills/*/SKILL.md`（见目录枚举）
- `docs/OVERVIEW.md`, `docs/reference/INDEX.md`, `docs/reference/architecture.md`, `docs/feature/INDEX.md`
- `sandbox/README.md`, `sandbox/codex-config.toml`
- `docs/feature/ai-evaluation/win-rate-evolution/evolution-2026-05/milestone-2/taskBoard.md`
- `.claude/skills/project-docs-workflow/SKILL.md`, `.claude/skills/harness-engineering-plan/SKILL.md`