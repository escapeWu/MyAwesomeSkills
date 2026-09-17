## Review

- **Blocker**：[freqtrade/scripts/validate_research_docs.py:429](/Users/shancw/workspace/freqtrade/scripts/validate_research_docs.py:429)、[research_docs_route_contract.py:363](/Users/shancw/workspace/freqtrade/scripts/research_docs_route_contract.py:363) 与 [freqtrade-wt-regime-engineering/scripts/validate_research_docs.py:369](/Users/shancw/workspace/freqtrade-wt-regime-engineering/scripts/validate_research_docs.py:369) 仍强制旧版 `requirements.md`、`changelog.md`、`MAINLINE-ROUTE` 和 collaboration metadata。`tests/test_docs.sh` 在两个仓库分别报 12 和 11 个错误。当前 validator 与已经同步的轻量 canonical assets 不兼容，rollout 不能视为验证通过。

- **Blocker**：[tradeMonitor/AGENTS.md:14](/Users/shancw/workspace/tradeMonitor/AGENTS.md:14) 明确取消 Spec lifecycle、固定验证矩阵和固定行数门，但活动项目文档重新施加了这些门禁：[runbook-testing.md:59](/Users/shancw/workspace/tradeMonitor/docs/reference/runbook-testing.md:59) 固定验证矩阵，[code-organization.md:61](/Users/shancw/workspace/tradeMonitor/docs/reference/code-organization.md:61) 强制 800/1000 行门及合同冻结，[development-plan.md:72](/Users/shancw/workspace/tradeMonitor/docs/feature/instrument-taxonomy/development-plan.md:72) 要求 Spec validation matrix 和 lifecycle transition。这会让 Agent 从少量 docs 进入后重新落回旧 harness 流程。

- **Correct**：canonical 与五个目标中的已安装 skill 内容一致。唯一内容差异是允许的 `add-idea` provider policy；`freqtrade-wt-regime-engineering` 是未注册 `add-idea` 和 bootstrap skill 的合法 partial install。未发现 flat/grouped 相对路径问题或活动文件对已删除 `mainline-route-contract.md`、`output-spec.md`、bundle installer、旧模板的死引用。

- **Correct**：`reportAgent` 的 `.cursor/rules/harness-execution.mdc` 与根 `AGENTS.md` 一致；其他仓库没有额外活动 `.cursor` 规则。各仓库仍保留交易、训练、公网、计费、敏感数据及研究证据授权边界。

- **Correct**：四个 Git 仓库及 canonical 源仓库均无 staged 文件，`git diff --check` 通过。`reportAgent` 文档链接检查通过，共检查 800 个 Markdown 文件。

- **Note**：Git 仓库中的业务文档修改时间均早于 rollout 规则更新，内容也对应独立产品/研究工作，未发现 rollout 批量改写业务 docs 的证据。`tradeMonitor` 不是 Git 仓库，且其四份治理文档在 rollout 时段被修改，因此无法验证基线或准确归因。

- **Note**：请求指定的 `/Users/shancw/project/MyAwesomeSkills/plan.md` 和 `progress.md` 均不存在，本次只能根据 canonical、实际工作树和现有验证命令审查。