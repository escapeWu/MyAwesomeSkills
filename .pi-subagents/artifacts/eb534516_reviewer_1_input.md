# Task for reviewer

[Read from: /Users/shancw/project/MyAwesomeSkills/plan.md, /Users/shancw/project/MyAwesomeSkills/progress.md]

只读审查以下部分安装项目的 harness rollout，不修改文件：
- /Users/shancw/workspace/lightgbm
- /Users/shancw/workspace/market-signals

源：/Users/shancw/project/MyAwesomeSkills/skills/harness。只应更新它们已安装的 canonical skills，market-signals 已删除的本地 harness-engineering-plan/harness-setup/code-organization/codex-review 不得恢复。
检查：AGENTS/CLAUDE/.cursor 是否符合轻量模型和项目数据/Coinglass安全边界；canonical skill/链接是否一致；是否仍有普通任务强制旧 gate；是否意外触碰业务 docs。Findings first，精确 file:line；无问题明确说明。

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