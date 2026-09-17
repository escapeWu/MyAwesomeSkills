# Task for luna-scout

对 /Users/shancw/workspace 下本次更新的 9 个 harness 安装点做只读语义核验：agentTrade、tradeMonitor、freqtrade、freqtrade-wt-regime-engineering、lightgbm、market-signals、reportAgent、tradingsignal、tradingsignal-services-modules。不要修改。

回答：1) 是否还有 active governance 让普通任务强制 Spec/TDD/taskBoard/sync docs；2) async docs SubAgent 单 writer/不等待是否在各根规则可见；3) 是否保留关键项目安全边界；4) 是否有死 skill/path 引用；5) 哪些项目无 git 或已有脏工作树构成残余风险。
只报告 actionable findings，精确 file:line；无 blocker 明确说明。

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