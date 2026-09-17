**结果（只读盘点）**

| 文件:行 | 命中原文 | 建议分类 |
|---|---|---|
| `/Users/shancw/workspace/agentTrade/.agents/skills/add-idea/SKILL.md:1` | `name: add-idea`（技能入口存在） | 直接同步 canonical |
| `/Users/shancw/workspace/agentTrade/.agents/skills/document-organization-harness/SKILL.md:1` | `name: document-organization-harness` | 直接同步 canonical |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/SKILL.md:1` | `name: progressive-disclosure-docs` | 直接同步 canonical |
| `/Users/shancw/workspace/agentTrade/.agents/skills/project-docs-workflow/SKILL.md:1` | `name: project-docs-workflow` | 直接同步 canonical |
| `/Users/shancw/workspace/agentTrade/.agents/skills/project-analysis/SKILL.md:1` | `name: project-analysis` | 直接同步 canonical |
| `/Users/shancw/workspace/agentTrade/.agents/skills/external-collaboration-workflow/SKILL.md:1` | `name: external-collaboration-workflow` | 直接同步 canonical |
| `/Users/shancw/workspace/agentTrade/.agents/skills/refactor-large-modules/SKILL.md:1` | `name: refactor-large-modules` | 直接同步 canonical |
| `/Users/shancw/workspace/agentTrade/.agents/skills/add-idea/agents/openai.yaml:3-4` | `short_description...` / `default_prompt...` | **Target governance patch**（与 source 有偏差：更偏 contract/Spec/ADR 分流） |
| `/Users/shancw/workspace/agentTrade/.agents/skills/add-idea/agents/openai.yaml:5-6` | `policy:\n  allow_implicit_invocation: false` | **target-specific 扩展**（source 无该字段） |
| `/Users/shancw/workspace/agentTrade/AGENTS.md:13-14` | `Expected behavior ... Spec ... ADR ...`（核心 truth 拆分） | 直接同步 canonical（当前仓库已承载） |
| `/Users/shancw/workspace/agentTrade/.agents/skills/document-organization-harness/assets/demo-harness/AGENTS.md:5` | 根文档约束明确 + 强制流程化治理 | target governance patch（源示例 AGENTS 更轻量） |
| `/Users/shancw/workspace/agentTrade/.agents/skills/document-organization-harness/assets/demo-harness/.cursor/rules/harness-execution.mdc:1` | `alwaysApply: true` + 实施前门禁与证据流 | **target-specific 本地扩展**（源对应目录无该文件） |
| `/Users/shancw/workspace/agentTrade/.agents/skills/add-idea/SKILL.md:101` | `Do not create a new Feature merely ...`（路由与文档/合同路径） | 直接同步 canonical（但已偏向较重合同化） |
| `/Users/shancw/workspace/agentTrade/.agents/skills/add-idea/SKILL.md:110-122` | `REQUIREMENTS_PATCH/NEW_SPEC/ADR_CANDIDATE/STATE_ONLY/NO_DURABLE_CHANGE` | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/SKILL.md:241-250` | 明确 `Feature/Spec/ADR lifecycle` 与冻结规则 | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/project-docs-workflow/SKILL.md:64-65` | `first parse ... CURRENT DEVELOPMENT MAINLINE` + `MAINLINE-ROUTE` | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/project-docs-workflow/SKILL.md:262-273` | 验证通过后同步 durable state、overview/index/changelog | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/document-organization-harness/SKILL.md:19-33` | 明确 `docs/collaboration/INDEX.md`、`docs/archive/INDEX.md`、`requirements.md`、`specs/`、`decisions/` | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/SKILL.md:211-223` | `MAINLINE-ROUTE` + 机读 manifest 写入 README + 节点变更规范 | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/references/mainline-route-contract.md:21-23` | append 持续 route transitions 到 changelog；机器化 route manifest | target governance patch（已引入高强度路线治理） |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/assets/spec-template.md:2-6` | 新增 `spec-template.md`、`spec-index-template.md` 等模板族 | 需要保留本地内容后合并 |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/assets/feature-template/README.md:30-45` | `MAINLINE-ROUTE` JSON 块（`schema_version`/`route_version`） | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/assets/feature-template/requirements.md:1-11` | 新增 `requirements` 模板与 `authorization/read_by_default` 元数据 | 需要保留本地内容后合并 |
| `/Users/shancw/workspace/agentTrade/.agents/skills/progressive-disclosure-docs/assets/feature-template/requirements.md:18-19` | 唯一 owner 指向 `expected behavior` + `acceptance`，并分离实现设计 | target governance patch |
| `/Users/shancw/workspace/agentTrade/.agents/skills/external-collaboration-workflow/SKILL.md:88-94` | 实施前需 `project-docs-workflow` + 合同迁移 + 证据闭环 | target governance patch |
| `/.agents/skills (find result, no path)` | 目标树内未发现 `README.md`/`CLAUDE.md`、`registry` 清单文件（仅技能目录） | 可能过时但非规则（非规则性：缺少显式注册清单） |
| `/Users/shancw/project/MyAwesomeSkills/skills/harness/project-docs-workflow/SKILL.md:20`、`/Users/.../project-docs-workflow/SKILL.md:20`（source） | source 明确“不要求 TDD、测试先行”；target未再出现该约束 | **缺失/回归风险**（需确认是否故意放宽到文档治理层） |

**新增本地文件（相对源套件）**  
- `/.agents/skills/document-organization-harness/assets/demo-harness/.cursor/rules/harness-execution.mdc:1`  
- `/.agents/skills/document-organization-harness/assets/demo-harness/docs/archive/INDEX.md:1`  
- `/.agents/skills/document-organization-harness/assets/demo-harness/docs/collaboration/INDEX.md:1`  
- `/.agents/skills/document-organization-harness/assets/demo-harness/docs/feature/demo-module/requirements.md:1`  
- `/.agents/skills/progressive-disclosure-docs/assets/adr-template.md:1`  
- `/.agents/skills/progressive-disclosure-docs/assets/decision-index-template.md:1`  
- `/.agents/skills/progressive-disclosure-docs/assets/spec-index-template.md:1`  
- `/.agents/skills/progressive-disclosure-docs/assets/spec-template.md:1`  
- `/.agents/skills/progressive-disclosure-docs/references/feature-spec-decision-contract.md:1`  
- `/.agents/skills/project-analysis/references/output-spec.md:1`  
- `/.agents/skills/document-organization-harness/assets/demo-harness/docs/archive/INDEX.md:1`（在上行已重复）

**源套件但在目标缺失（相对扫描路径）**  
- `/Users/shancw/project/MyAwesomeSkills/skills/harness/CHANGELOG.md:1`  
- `/Users/shancw/project/MyAwesomeSkills/skills/harness/README.md:1`  
- `/Users/shancw/project/MyAwesomeSkills/skills/harness/UPGRADING.md:1`  
- `/Users/shancw/project/MyAwesomeSkills/skills/harness/progressive-disclosure-docs/references/core-docs-guide.md:1`  
- `/Users/shancw/project/MyAwesomeSkills/skills/progressive-disclosure-docs/references/mainline-route-guide.md:1`  
- `/Users/shancw/project/MyAwesomeSkills/skills/project-analysis/references/output-guide.md:1`

**未找到与歧义（含扫描边界）**
- `CLAUDE.md`：未在目标技能树中发现（与目标/源套件一致无文件）。`find` 未命中 `**/CLAUDE.md`。  
- `skill registry/README`：未发现单独 registry/readme；仅有实际 skill 目录与 `SKILL.md`/`agents/*.yaml`。  
- `TDD/testing-first`：在目标 `.agents/skills` 下未命中关键字；源套件有明确“无 TDD/testing-first/固定状态机”约束（见源 `UPGRADING.md`、`project-docs-workflow/SKILL.md`）。  
- 已扫描范围：`/Users/shancw/project/MyAwesomeSkills/skills/harness` 与 `/Users/shancw/workspace/agentTrade/.agents/skills` 全量文本树。未扫描目标非-skill 代码树，仅对 `.agents/skills` 与源套件进行对应比对。  
- 未覆盖项：尚未做 `readme/skill registry/URL` 的交叉读取（如非-skill 注册/索引链路）以外的一致性验证。

**git status（目标）**
- 目标根 `git status --short` 显示大量非暂存变更/未跟踪（非当前盘点新增）：
  - 未暂存修改（`M` / `D`）与未跟踪（`??`）并存；
  - `git diff --name-only --cached` 空输出；无暂存文件。

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "只读扫描完成：对源套件与目标 .agents/skills 做了目录/文件对比、关键规则关键词检索、git status 与暂存区校验，未执行写操作，未扩大作用域。"
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "find /Users/shancw/project/MyAwesomeSkills/skills/harness -r -type d -name '.git' -prune -o -print",
      "result": "passed",
      "summary": "源套件技能目录与文件树已枚举。"
    },
    {
      "command": "python3 ... compute target\\_only/source\\_only files between source and target skill trees",
      "result": "passed",
      "summary": "输出 TARGET_ONLY=13、SOURCE_ONLY=6，用于后续盘点。"
    },
    {
      "command": "git status --short -- .agents/skills",
      "result": "passed",
      "summary": "显示目标技能树下多处未暂存修改与未跟踪文件。"
    },
    {
      "command": "git diff --name-only --cached -- .",
      "result": "passed",
      "summary": "暂存区为空，未发现已暂存变更。"
    }
  ],
  "validationOutput": [
    "目标技能树与源套件相比，安装技能集合为6个 skill（add-idea、document-organization-harness、progressive-disclosure-docs、project-analysis、project-docs-workflow、external-collaboration-workflow、refactor-large-modules）；无增删技能目录。",
    "存在明显本地扩展：新增 .cursor 执行规则、mainline/manifest 体系加重、Spec/ADR 模板族扩展、collaboration/archive demo 索引。"
  ],
  "residualRisks": [
    "未发现 CLAUDE.md 与显式 skill registry/README；若治理依赖此类清单，需人工确认目标侧是否故意省略。",
    "目标现有工作树包含大量预存修改（M/D/??），非本次扫描引入，后续治理判定需与现有未提交状态隔离。"
  ],
  "noStagedFiles": true,
  "diffSummary": "未对文件系统做修改；本次为只读盘点。",
  "reviewFindings": [
    "目标 `.agents/skills/progressive-disclosure-docs` 与 `project-docs-workflow` 已显著偏向“高强度合同+MAINLINE-ROUTE manifest”治理；需在目标项目策略中确认是否按此方向继续。",
    "源套件中的部分轻量约束文件（如 core-docs-guide/mainline-route-guide/UPGRADING）未随 target 直接保留，属于迁移分支差异而非回归。",
    "无 code/test 修改；无 staged 变更。"
  ],
  "manualNotes": "可选后续：如需，我可以基于本表输出“按文件级风险级别”的合并建议（例如可直接保留/建议回收/需要人工决策）。"
}