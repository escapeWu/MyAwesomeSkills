# Task for reviewer

最终只读审查 /Users/shancw/project/MyAwesomeSkills 当前改动，忽略 skills/grok_search/scripts/grok_search.py，不修改文件。

目标：确认 add-idea 统一显式入口与 Feature/requirements/Spec/ADR 合同已完整落地。前两轮问题已修：显式字段加入 repo spec/validator/skill-creator 并有 4 个 unittest；confirmed requirements 物化；NO_DURABLE_CHANGE；五个 eval cases。

请检查全部相关 diff，重点：
- add-idea 入口、Grill confirmation、owner/artifact route；
- Feature/requirements/Spec/ADR owner/lifecycle/gates；
- later implementation integration；
- frontmatter extension validator correctness；
- bundle/plugin/README/demo/bootstrap registrations；
- links/paths/template references；
- no hidden implementation/publication authorization；
- no unrelated grok_search change included in conclusions。

按严重度返回 findings 与绝对 file:line。若无 blocker/major，明确说明 remaining minor/test risks。

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