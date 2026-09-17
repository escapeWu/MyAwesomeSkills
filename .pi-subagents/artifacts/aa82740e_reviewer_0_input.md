# Task for reviewer

[Read from: /Users/shancw/project/MyAwesomeSkills/plan.md, /Users/shancw/project/MyAwesomeSkills/progress.md]

复核已修复的 rollout findings，只读不修改：
1. /Users/shancw/workspace/freqtrade 与 /Users/shancw/workspace/freqtrade-wt-regime-engineering 的 research docs validator 是否已兼容轻量 Feature/collaboration templates、active route manifest 是否不再强制、tests/test_docs.sh 是否通过。
2. /Users/shancw/workspace/tradeMonitor 的 runbook-testing.md、code-organization.md、instrument-taxonomy/development-plan.md 是否还会让普通任务落回固定 Spec lifecycle/800-1000 行/全矩阵门禁。
3. 根 AGENTS async single writer 与安全边界是否仍一致。
Findings first，精确 file:line；无 actionable finding 明确说明。

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