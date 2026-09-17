# Task for reviewer

复审 /Users/shancw/project/MyAwesomeSkills 本轮 harness 2.0.0 upgrade 改动，仅读取、不修改。上一轮 findings 已修复：
- manifest-managed source/target symlink 以及路径组件 symlink 在读写前拒绝；目标外文件有测试保护。
- 安装/升级先复制到 repo 内 staging，写 marker、验证 hashes 后切换 target，staging 失败保持旧树；backup 仍在切换前完成。
- 默认拒绝 marker 版本降级，显式 --allow-downgrade + --overwrite + --backup-dir 才允许。
- verify 检查 hash_algorithm=sha256。
- 所有文档命令改为 python3。
- 测试从 5 增至 11，覆盖上述行为和额外顶层 skill 保留。

请重点验证这些修复是否真实完整，并继续找 blocker/major correctness、安全、数据丢失、事务切换、备份/rollback、plan/verify/marker、版本比较、文档命令/承诺不一致。检查文件仍为 CHANGELOG.md、UPGRADING.md、manifest、installer、tests、README/bootstrap/SKILL。忽略 grok_search.py、.pi-subagents 和旧 add-idea 主体。按严重度给绝对 file:line；若无 blocker/major 明确说明 residual minor/test risks。

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