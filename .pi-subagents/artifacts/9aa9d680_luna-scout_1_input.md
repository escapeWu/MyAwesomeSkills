# Task for luna-scout

在 /Users/shancw/project/MyAwesomeSkills 中对本次 harness 轻量化修改做只读语义核验，不修改文件。范围只包含 skills/harness/**、根 README.md、project-analysis.skill、project-docs-workflow.skill；忽略 skills/grok_search/scripts/grok_search.py 和 .pi-subagents/。

核验目标：
- 普通实现任务开始前只读少量 docs，不创建文档门禁；
- 不强制 TDD/测试先行、Spec/requirements/ADR 生命周期、固定 validation matrix、机器 route/status schema；
- 实现与验证完成后，主 Agent 异步委派一个有界 docs SubAgent，一轮单 writer patch，主 Agent不等待或并发写同一 docs；
- docs 本身是交付物时允许主 Agent处理；无 SubAgent 有轻量 fallback；
- add-idea/grill 只问影响 outcome/owner/hard boundary 的最高优先级问题，不问可逆实现细节；
- 核心 docs 路径最小且可选层按需创建；
- 删除/重命名引用无残留。

请返回确认事实、发现的冲突/遗漏、精确 file:line、对用户目标的总体符合度。只报告能驱动修改的事项。

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope

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