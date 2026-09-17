# Task for reviewer

只读终审以下文件，不修改：/Users/shancw/project/MyAwesomeSkills/skills/harness/document-organization-harness/scripts/install_harness_bundle.py、同目录 test_install_harness_bundle.py、/Users/shancw/project/MyAwesomeSkills/skills/harness/UPGRADING.md。上一轮 blocker 已修，11 tests pass。只找仍存在的 blocker/major：边界外写入、数据丢失、staging 切换失败、backup 无效、默认降级、plan/verify 误报、文档命令不可执行。每个 finding 给绝对 file:line 和复现；若无 blocker/major，直接明确说无，并最多列 3 个 residual minor。

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