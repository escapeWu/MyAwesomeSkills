# Task for reviewer

只读审查 /Users/shancw/project/MyAwesomeSkills 当前 harness 改动，不修改。用户最新决定：这里主要维护独立 skills，不要 bundle 安装功能。已删除 tracked harness-bundle.json 和 install_harness_bundle.py，撤掉此前新建 installer tests；CHANGELOG 改为日期型 suite 变更记录，UPGRADING 改为逐项目/逐 skill 人工维护指南。

请重点检查：
1. 仓库是否仍有可执行 bundle 安装、manifest、marker、自动覆盖、统一发布版本语义或死链接残留。
2. CHANGELOG 是否准确记录 add-idea、Feature/Requirements/Spec/ADR 变化及删除 bundle 功能。
3. UPGRADING 是否覆盖 grouped/flat/partial/extended layouts、dirty repo、依赖顺序、目标规则保护、Feature 渐进迁移、验证与 rollback，且不暗示自动部署或授权。
4. README、document-organization-harness SKILL、bootstrap 是否和“维护而非安装”一致。
5. 忽略 grok_search.py 与 .pi-subagents。

按严重度给 absolute file:line。若无 blocker/major 明确说明，列 remaining minor/test risk。

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