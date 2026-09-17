# Task for reviewer

[Read from: /Users/shancw/project/MyAwesomeSkills/plan.md, /Users/shancw/project/MyAwesomeSkills/progress.md]

只读审查以下 rollout，不修改文件：
- /Users/shancw/workspace/tradingsignal
- /Users/shancw/workspace/tradingsignal-services-modules

检查 canonical progressive-disclosure-docs/project-analysis/project-docs-workflow 双路径/工作树同步；本地 harness-engineering-plan 是否已变成 opt-in 而不是普通任务门禁；tradingsignal 的未跟踪 harness-setup 是否轻量且保留；services worktree 不得引用未安装 skill；AGENTS/CLAUDE 保留 sandbox/worktree/testing安全规则，同时实现完成后异步单 docs writer、不等待。检查死链接和旧 taskBoard/Spec 前置冲突。Findings first，精确 file:line；无问题明确说明。

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