# Task for reviewer

[Read from: /Users/shancw/project/MyAwesomeSkills/plan.md, /Users/shancw/project/MyAwesomeSkills/progress.md]

对 /Users/shancw/project/MyAwesomeSkills 当前未提交 diff 中仅与 skills/harness/**、README.md、project-analysis.skill、project-docs-workflow.skill 有关的修改做只读审查。不要修改文件，忽略 skills/grok_search/scripts/grok_search.py 和 .pi-subagents/（它们是用户/环境已有改动）。

用户目标：harness 要快速轻量；去除 TDD/测试先行与实施 Spec 生命周期；只保留核心 docs；实现与验证结束后才更新一轮文档；该 docs 更新由主 Agent 异步委派给一个 SubAgent，主 Agent 不等待，且同一轮只有一个 docs writer；grill me 只问最核心、真正阻塞的内容，不做详尽问卷；规则不要过度僵化。

请重点检查：
1. 当前 diff 是否实现目标，是否存在相互矛盾或仍会强制旧重流程的规则。
2. 删除/重命名文件后的引用、模板、README、打包产物是否一致。
3. async docs SubAgent 规则是否存在竞态、双 writer、过早写 docs 或主 Agent仍必须等待的问题。
4. 外部协作脚本的惰性 INDEX 创建是否有行为 bug。
5. 只列 actionable findings，按严重度排序，给精确 file:line；若无问题明确说明，并列剩余验证风险。

不要要求恢复用户明确删除的 Spec/TDD 重流程。

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