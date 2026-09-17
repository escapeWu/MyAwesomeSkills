# Task for spark-scout

在 /Users/shancw/project/MyAwesomeSkills 中进行只读扫描。

目标：
- 枚举 skills/harness 下所有与 TDD、tests-first、spec/specification、requirements、任务过程中/每阶段文档更新、grill me/用户询问/澄清相关的规则和模板。
- 枚举仓库根 README.md 与 .claude-plugin/marketplace.json 中 harness 的注册和说明位置。

检索范围：
- skills/harness/**
- README.md
- .claude-plugin/marketplace.json

排除范围：
- 其他技能和构建产物。

需要返回：
1. 按“入口/路由规则、TDD、spec/requirements、文档更新时机、grill me/澄清、模板/资产、注册文档”分类的命中列表。
2. 每项包含精确 file:line、必要原文和它属于强制规则还是可选建议（只根据措辞分类，不评价设计）。
3. 标出相互引用关系与可能因删除文件而失效的链接。

事实来源：仅报告当前仓库材料。

输出格式：紧凑表格/列表；未找到明确说明。单列覆盖范围、歧义和需要主代理判断的事项。不要修改文件。

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