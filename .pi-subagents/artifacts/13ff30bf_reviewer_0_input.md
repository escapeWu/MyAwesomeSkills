# Task for reviewer

只读审查 /Users/shancw/project/MyAwesomeSkills 中当前未提交改动，排除并忽略用户已有的 skills/grok_search/scripts/grok_search.py。不要修改文件。

用户目标：新增统一显式入口 add-idea。用户描述不清时进入一次一题的 Grill；shared understanding 确认后由 Agent 决定 CREATE_FEATURE 还是 PATCH_FEATURE；再独立决定 requirements patch、new Spec、conditional ADR。整个入口 docs-only，不实施代码、不发布 issue。

重点文件：
- skills/harness/add-idea/**
- skills/harness/progressive-disclosure-docs/SKILL.md
- skills/harness/progressive-disclosure-docs/references/feature-spec-decision-contract.md
- skills/harness/progressive-disclosure-docs/assets/*template*.md
- skills/harness/project-docs-workflow/SKILL.md
- skills/harness/project-analysis/SKILL.md
- bundle/registry/demo changes
- docs/superpowers/plans/2026-07-23-add-idea-workflow.md

请按代码审查姿态返回 findings，按严重度排序并给绝对 file:line。验证这些场景：
1. vague idea 不会在确认前写 docs；
2. independent outcome/lifecycle -> CREATE_FEATURE；
3. one existing owner/local extension -> PATCH_FEATURE；
4. contract-affecting patch -> NEW_SPEC；
5. durable real tradeoff -> ADR_CANDIDATE and blocks Spec freeze until accepted；
6. reversible local detail -> no ADR/no forced Spec when trivial；
7. later implementation requires frozen Spec only when contract-affecting；
8. Feature/requirements/Spec/ADR lifecycles and owners do not conflict；
9. plugin and bundle registration is complete；
10. no instruction grants implementation/deployment/publication.

Also report any missing test/eval coverage or ambiguity. If no findings, say so clearly. Use fresh context and only current files as contract.

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