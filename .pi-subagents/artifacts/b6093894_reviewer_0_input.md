# Task for reviewer

对 /Users/shancw/project/MyAwesomeSkills 当前未提交的 harness 2.0.0 changelog/upgrade 改动做只读 code review，不修改文件。忽略 skills/grok_search/scripts/grok_search.py、.pi-subagents 与此前 add-idea 主体本身，重点审查本轮新增：
- skills/harness/CHANGELOG.md
- skills/harness/UPGRADING.md
- document-organization-harness/assets/harness-bundle.json
- document-organization-harness/scripts/install_harness_bundle.py
- document-organization-harness/scripts/test_install_harness_bundle.py
- README/bootstrap/SKILL 链接与命令更新

要求：
1. 找 correctness、数据丢失、路径穿越、symlink、部分写入、backup/rollback、plan/verify/marker 哈希、版本兼容、CLI 语义问题。
2. 核对 installer 只管理 manifest root files 与 skill dirs，保留额外顶层 skill，不改目标 AGENTS/docs/code。
3. 核对 v2.0.0 changelog 是否覆盖 add-idea 与 Feature/Requirements/Spec/ADR breaking migration。
4. 核对 UPGRADING 对 full/partial/legacy deployments、dirty repo、渐进 Feature 迁移、fleet rollout、rollback 是否可执行且不暗示授权。
5. 核对测试是否覆盖高风险行为，指出缺口。

按严重度列 findings，必须给绝对 file:line。若无 blocker/major，明确说明，并列 residual risks。

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