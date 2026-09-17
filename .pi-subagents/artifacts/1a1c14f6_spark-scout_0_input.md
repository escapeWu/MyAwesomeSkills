# Task for spark-scout

在 /Users/shancw/workspace/agentTrade 做只读升级盘点。

源套件：/Users/shancw/project/MyAwesomeSkills/skills/harness
目标：枚举目标项目当前安装的 harness skills、provider metadata、目标根/嵌套 AGENTS.md、CLAUDE.md、.cursor rules、skill registry/README，以及所有仍引用 requirements/Spec/ADR lifecycle、pre-implementation docs gate、TDD/testing-first、同步 docs write-back、MAINLINE-ROUTE/状态矩阵、旧删除模板/合同路径的规则。
同时报告 git status、目标 skill 内相对源套件的新增本地文件和明显本地扩展；不要修改。

输出紧凑表格：file:line、命中原文、建议分类（直接同步 canonical / 需要保留本地内容后合并 / target governance patch / 可能过时但非规则）。列出实际扫描范围与未覆盖项。

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