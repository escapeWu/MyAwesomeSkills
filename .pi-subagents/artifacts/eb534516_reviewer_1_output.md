## Review

- **Medium**: `market-signals` 安装的 `project-analysis` 存在内部冲突。[mermaid-templates.md](/Users/shancw/workspace/market-signals/.agent/skills/harness/project-analysis/references/mermaid-templates.md:5) 仍强制每个 Mermaid 图附带 ASCII/TUI 图，而 [SKILL.md](/Users/shancw/workspace/market-signals/.agent/skills/harness/project-analysis/SKILL.md:67) 明确说图表可选且不要求成对输出。源 canonical 文件也有同一问题，因此这不是安装漂移，而是 rollout 继承了一个旧式强制要求。它不影响普通实现任务，但会影响读取该 reference 的分析任务。

- **Correct**: 未发现普通任务仍被旧 taskBoard/milestone/TDD gate 强制。LightGBM 在 [AGENTS.md](/Users/shancw/workspace/lightgbm/AGENTS.md:27) 明确取消这些前置要求；market-signals 在 [AGENTS.md](/Users/shancw/workspace/market-signals/AGENTS.md:22)、[CLAUDE.md](/Users/shancw/workspace/market-signals/CLAUDE.md:5) 和 [harness-execution.mdc](/Users/shancw/workspace/market-signals/.cursor/rules/harness-execution.mdc:9) 保持一致。

- **Correct**: 项目安全边界保留。LightGBM 的凭证、评分语义和未来数据泄漏限制位于 [AGENTS.md](/Users/shancw/workspace/lightgbm/AGENTS.md:8)；market-signals 的 Coinglass 授权和保密限制位于 [AGENTS.md](/Users/shancw/workspace/market-signals/AGENTS.md:52)，CLAUDE 和 Cursor 规则也没有放宽该边界。

- **Correct**: 已安装 canonical skill 文件与源目录逐文件一致。LightGBM 的 `progressive-disclosure-docs`、`project-docs-workflow`，以及 market-signals 的这两项和 `project-analysis` 均通过 byte comparison。AGENTS 中引用的 skill/docs 路径全部存在。

- **Correct**: market-signals 已删除的四个 skill entrypoint 均不存在：`harness-engineering-plan/SKILL.md`、`harness-setup/SKILL.md`、`code-organization-harness/SKILL.md`、`codex-design-review/SKILL.md`。保留的四份未跟踪 archived taskBoard 不构成 skill 恢复，因为目录内没有 `SKILL.md`，也符合 [AGENTS.md](/Users/shancw/workspace/market-signals/AGENTS.md:24) 对历史材料的保留规则。

- **Correct**: 未发现 rollout 意外修改业务 docs。rollout 文件的修改时间为 `2026-07-23 19:49:21`；两个仓库当前业务 docs 的修改时间集中在 `2026-07-10` 至 `2026-07-12`，属于更早的独立工作树修改。两个目标仓库均无 staged files。

- **Note**: 请求指定的 `/Users/shancw/project/MyAwesomeSkills/plan.md` 和 `progress.md` 均不存在，无法用它们核对 rollout 过程记录；本次按用户消息中的明确范围和验收要求完成审查。