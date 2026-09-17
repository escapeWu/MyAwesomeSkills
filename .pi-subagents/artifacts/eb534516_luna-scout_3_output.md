## 1. 确认事实

- **无 active governance 强制普通任务使用 Spec/TDD/taskBoard/sync docs。** 九个根规则均明确取消这些前置门禁：
  - `agentTrade/AGENTS.md:14-15,43`
  - `tradeMonitor/AGENTS.md:14-15,44`
  - `freqtrade/AGENTS.md:23,27`
  - `freqtrade-wt-regime-engineering/AGENTS.md:31,35`
  - `lightgbm/AGENTS.md:27-29`
  - `market-signals/AGENTS.md:22-23`
  - `reportAgent/AGENTS.md:20-22`
  - `tradingsignal/AGENTS.md:12-13,41-42`
  - `tradingsignal-services-modules/AGENTS.md:12-13,41-42`
- **async docs SubAgent 单 writer / 不等待规则可见于全部九个根规则。** 代表性精确位置：
  - `agentTrade/AGENTS.md:44-46`
  - `tradeMonitor/AGENTS.md:45-47`
  - `freqtrade/AGENTS.md:55-59`
  - `freqtrade-wt-regime-engineering/AGENTS.md:53-57`
  - `lightgbm/AGENTS.md:37-39`
  - `market-signals/AGENTS.md:32-34`
  - `reportAgent/AGENTS.md:31-33`
  - `tradingsignal/AGENTS.md:51-53`
  - `tradingsignal-services-modules/AGENTS.md:51-53`
- **关键安全边界仍保留：**
  - AgentTrade / tradeMonitor 禁止将代码、配置、页面、验证结果解释为交易、账户、计费或公网执行授权：`agentTrade/AGENTS.md:7,12`；`tradeMonitor/AGENTS.md:7,12`
  - Freqtrade 两根规则保留禁止训练/holdout/dry-run/shadow/live/force-entry/order 执行授权、禁止 secrets、future leakage，并要求 sealed holdout 等只读：`freqtrade/AGENTS.md:10-17`；`freqtrade-wt-regime-engineering/AGENTS.md:10-17`
  - LightGBM 保留评分不是交易动作、Step4 禁止未来收益/oracle/MFE/MAE 等 post-hoc 字段进入 candidate events：`lightgbm/AGENTS.md:8-14`
  - TradingSignal 两根规则保留禁止交易执行、钱包权限及 secret 回显：`tradingsignal/AGENTS.md:6-7`；`tradingsignal-services-modules/AGENTS.md:6-7`
  - Market-signals 保留 Coinglass 付费数据保密边界：`market-signals/AGENTS.md:52-56`
- **死 skill/path 引用核验：未发现根规则中指向不存在路径的引用。** 对各根规则列出的 `.agents/skills`、`.agent/skills`、`.claude/skills` 路径逐项检查，均能在对应项目中解析到实际目录。Market-signals 同时明确已删除 skill 不应恢复：`market-signals/AGENTS.md:44`；当前目录也未发现这些已删除 skill。
- **Git 状态：**
  - `tradeMonitor` 无 `.git`，且当前目录无 git 状态可供审计。
  - 其余八个项目均有 `.git`。
  - `tradeMonitor` 是九个项目中唯一无 git 的安装点，因此其更新无法通过提交/diff 追踪。
  - 其余八个项目均存在脏工作树：
    - `agentTrade`: 93 tracked changes，50 untracked
    - `freqtrade`: 28 tracked changes，2323 untracked
    - `freqtrade-wt-regime-engineering`: 22 tracked changes，39 untracked
    - `lightgbm`: 9 tracked changes，27 untracked
    - `market-signals`: 56 tracked changes，120 untracked
    - `reportAgent`: 60 tracked changes，1567 untracked
    - `tradingsignal`: 16 tracked changes，21 untracked
    - `tradingsignal-services-modules`: 10 tracked changes，5 untracked
  - `tradeMonitor`: 无 git、无 tracked/untracked 状态可比对。

## 2. 推断

- 本次 harness 更新后，普通任务的控制面已回到 session plan / 当前代码与用户指令；现有 taskBoard 仅被规则作为历史或按需材料，不构成默认门禁：
  - `freqtrade/AGENTS.md:35-37`
  - `freqtrade-wt-regime-engineering/AGENTS.md:61`
  - `tradingsignal/AGENTS.md:70-72`
  - `tradingsignal-services-modules/AGENTS.md:67-69`
- 规则层面的安全授权边界没有因移除强制 Spec/TDD/taskBoard 而被一并删除。
- 最大残余风险不是规则语义，而是**工作树归因风险**：尤其 `freqtrade` 和 `reportAgent` 的大量 untracked 文件，以及 `tradeMonitor` 完全没有 Git 审计能力。

## 3. 未覆盖、矛盾与不确定项

- 本核验只检查九个项目根级 `AGENTS.md` 及 `tradingsignal` / `tradingsignal-services-modules` 的 `CLAUDE.md` 相关规则、skill 路径和 Git 元数据；未逐文件审计所有源码、深层子目录规则或 skill 内容。
- 未发现 blocker。残余风险为工作树脏状态和 `tradeMonitor` 无 Git，不是根规则语义 blocker。