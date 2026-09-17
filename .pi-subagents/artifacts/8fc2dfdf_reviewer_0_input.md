# Task for reviewer

只读审查 /Users/shancw/project/MyAwesomeSkills 当前与 harness 轻量化有关的 diff（README.md、skills/harness/**、project-analysis.skill、project-docs-workflow.skill）。忽略 skills/grok_search/scripts/grok_search.py 和 .pi-subagents/，不要修改文件。

只寻找 actionable bugs：规则矛盾、删除后死引用、异步 docs 单 writer/不等待语义缺口、create_case.py 行为错误、包内容与源码不一致。用户目标是无 TDD/Spec 前置门禁、最小核心 docs、任务完成后一个异步 docs SubAgent 写一轮、grill 只问核心问题、规则轻量灵活。

输出 findings first，按严重度，精确 file:line；没有问题就明确说无 findings，并列剩余风险。

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