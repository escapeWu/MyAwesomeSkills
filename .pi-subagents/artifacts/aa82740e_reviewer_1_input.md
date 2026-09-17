# Task for reviewer

[Read from: /Users/shancw/project/MyAwesomeSkills/plan.md, /Users/shancw/project/MyAwesomeSkills/progress.md]

复核已修复的 canonical/tradingsignal findings，只读不修改：
- /Users/shancw/project/MyAwesomeSkills/skills/harness/project-analysis/references/mermaid-templates.md 不再强制双图；所有安装副本与源一致。
- project-docs-workflow partial install 不再假设 add-idea 必定存在。
- /Users/shancw/workspace/tradingsignal 两套和 tradingsignal-services-modules 的 harness-engineering-plan templates 不再引用旧章节或要求 project-analysis 先写 docs。
- services 根规则和 skill 不得引用未安装 skill。
- packages 与 source 一致。
只列 actionable findings；无问题明确说明。

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