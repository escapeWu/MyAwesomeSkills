# Task for luna-scout

在 /Users/shancw/workspace/tradingsignal 做只读升级分析。

源套件：/Users/shancw/project/MyAwesomeSkills/skills/harness
目标只升级该项目实际维护的 canonical harness skills，并判断本地扩展 harness-setup、harness-engineering-plan、AGENTS/CLAUDE/.cursor/docs rules 是否与新的轻量模型冲突。
新模型：普通实现前只读少量 docs；不强制 TDD/testing-first、requirements/Spec/ADR lifecycle、固定 validation matrix、机器 route/status schema；实现与验证后主 Agent异步委派一个 docs SubAgent，单 writer 一轮 patch，主 Agent不等待；Grill只问核心 blocker。

需要返回：
1. 当前 git status 和安装/注册路径。
2. canonical skill 哪些可以直接同步，哪些含本地修改需合并。
3. 本地扩展与治理文件中仍会重新引入旧重流程的精确 file:line 与语义判断。
4. 最小安全升级方案，明确应修改/保留/不触碰文件。
不要修改文件。

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