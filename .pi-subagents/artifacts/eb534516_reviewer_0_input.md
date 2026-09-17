# Task for reviewer

[Read from: /Users/shancw/project/MyAwesomeSkills/plan.md, /Users/shancw/project/MyAwesomeSkills/progress.md]

只读审查以下已完成的 harness 轻量化 rollout，不修改文件：
- /Users/shancw/workspace/agentTrade
- /Users/shancw/workspace/tradeMonitor
- /Users/shancw/workspace/freqtrade
- /Users/shancw/workspace/freqtrade-wt-regime-engineering
- /Users/shancw/workspace/reportAgent

源：/Users/shancw/project/MyAwesomeSkills/skills/harness。
目标语义：普通实现前只读少量 docs；无 TDD/testing-first、Spec/requirements/ADR lifecycle、固定 validation matrix/route/status、taskBoard 前置；实现和验证后主 Agent 异步委派一个 docs SubAgent，单 writer 一轮 patch，主 Agent不等待；Grill只问核心 blocker；保留项目安全/授权/研究边界和用户现有改动。

检查 canonical skill 是否同步（允许 add-idea provider policy 差异）、AGENTS/.cursor 是否冲突、删除路径死引用、flat/grouped link问题、是否误改业务 docs。Findings first，按严重度给 file:line；无问题明确说明。

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: changed-files, tests-added, commands-run, residual-risks, no-staged-files

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
`criteriaSatisfied[].status` must be exactly one of: satisfied, not-satisfied, not-applicable.
`commandsRun[].result` must be exactly one of: passed, failed, not-run.
`manualNotes` and `notes` are optional strings; an empty string means no note and does not satisfy `manual-notes` evidence.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```