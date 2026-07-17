---
name: external-collaboration-workflow
description: 管理本仓库与外部团队之间的问题分析和方案交付闭环。用户要求整理问题或证据包交给外部团队、接收/录入/评审外部 analysis 或 proposal、逐项采纳外部建议、把方案转译成内部 requirements/design/development plan、根据已采纳方案实施开发、追踪外部建议到验证证据、或关闭外部合作 case 时使用。禁止把外部方案直接当作内部合同、当前实现或授权。
---

# 外部团队协作闭环

统一管理 `问题包 -> 外部方案 -> 内部采纳 -> 合同转译 -> 实施验证 -> 关闭`，保留来源可追溯性，
同时避免外部文档成为第二套项目 SSOT 或进度系统。

## 首先确定操作阶段

| 用户意图 | 阶段 | 主要输出 |
|---|---|---|
| 整理问题交给外部团队 | problem intake | 新 case 和 `problem-statement.md` |
| 收到外部分析/方案 | proposal receipt | 忠实的 `external-proposal.md` 与 provenance |
| 评审或讨论外部方案 | internal review | case `INDEX.md` adoption matrix |
| 按方案开发 | contract translation / implementation | 内部 SSOT 变更后才实施代码 |
| 核对方案是否落地 | validation/traceability | SSOT、代码、测试和 evidence 映射 |
| 合作完成/终止 | closure | closed case 和最终证据路由 |

同一请求可能跨多个阶段，但不得跳过版本绑定、内部采纳和合同转译门。

## 必读上下文

1. 读取仓库根 `AGENTS.md` 和 `docs/OVERVIEW.md`。
2. 若仓库存在 `docs/reference/external-collaboration-workflow.md`，完整读取它；若不存在，
   将项目特定协作 policy 标记为 docs gap，并以本 Skill 的来源、采纳和转译门禁作为最低合同。
3. 进入 `docs/collaboration/INDEX.md`，只读目标 case 的 `INDEX.md` 和本阶段所需的一份来源文件。
4. 读取 owning Feature README/INDEX；涉及 expected behavior 时再读 requirements，涉及实施时再读
   development plan/design 和 `docs/reference/code-organization.md`。

外部来源文件是 `source_record`：只提供 provenance/recommendation，不提供实施授权。

## 1. 创建问题 Case

使用确定性脚本，不手工发明目录和字段：

```bash
python3 .agents/skills/harness/external-collaboration-workflow/scripts/create_case.py \
  --case-id EC-YYYY-NNN-short-slug \
  --title "Case title" \
  --feature owning-feature-slug \
  --external-team "External team"
```

脚本从 `assets/case-template/` 创建三文件 case，并注册 Active Cases。创建后补齐问题包：

- expected behavior、current implementation、observed evidence 和 gap 分类；
- 复现命令、artifact/checksum、时间窗、输入版本和脱敏声明；
- 范围内/外、安全、授权、数据、兼容和不可变边界；
- 外部团队必须回答的问题、交付物、验证矩阵、风险、迁移和回滚要求。

发送后设置 `problem_version`、`issued_at` 和 commit/fingerprint。后续实质修改必须升版本并追加
revision history；不得静默覆盖已经发送的输入。

现有 docs 或代码不足以形成证据包时，使用 `project-analysis` 做只读取证，再更新问题包。

## 2. 接收外部方案

1. 保存外部原始文件/链接位置；转换 PDF、Word 或邮件时记录转换说明。
2. 核对 `based_on_problem_version` 和 `based_on_problem_commit`；版本不明时停止评审并请求澄清。
3. 记录 external team、proposal version、received date、source artifact 和 SHA-256 fingerprint。
4. 忠实写入 `external-proposal.md`，保留对方 assumptions、设计、接口、模块、迁移、验证和风险。
5. 内部只修复格式或明显转录错误；内部评价不得混入外部正文。

没有收到外部内容时，保持 `proposal_status: awaiting_external_input`。不得由 Agent 猜测或代写
“外部方案”。

## 3. 内部评审和采纳

把外部建议拆成稳定 ID（`P-01`、`P-02`……），只在 case `INDEX.md` 记录：

- `ACCEPTED`：原建议可直接转译；
- `MODIFIED`：内部接受目标，但冻结不同实现/边界；
- `REJECTED`：不进入内部合同，并记录理由；
- `DEFERRED`：明确延期条件和未来 gate；
- `PENDING`：尚未决定，禁止实施。

每条 `ACCEPTED`/`MODIFIED` 必须有内部 rationale、SSOT target、validation gate 和预期 evidence。
安全、授权、holdout、数据泄漏、公共契约或研究证据冲突时，以项目内部合同为准并暴露 blocker，
不得让外部方案覆盖它。

## 4. 合同转译和实施

实施前同时使用 `project-docs-workflow`，逐条完成：

1. expected behavior、acceptance、stop rules -> owning `requirements.md`；
2. 稳定架构、接口、数据流、状态和责任 -> owning design/reference；
3. 模块图、依赖方向、公共接口、复用边界、文件预算和测试归属 -> development plan/README；
4. current pending/blockers/next gate -> owning README；
5. 采纳与合同迁移 -> append-only `changelog.md`。

只有内部转译完成、case 达到 `READY_FOR_IMPLEMENTATION`，且用户/项目合同授权实施后，才能改
代码。大型模块或 800/1000 行门禁同时使用 `refactor-large-modules`。

实施从 owning Feature 文档进入，不从 `external-proposal.md` 进入。外部建议中的伪代码、文件名、
阈值和测试建议仍需按当前代码和内部合同复核。

## 5. 跟踪和关闭

不要在 case 中复制逐文件进度或建立平行执行控制面：

- current snapshot -> owning README/GOAL；
- expected behavior -> requirements；
- milestone/gate history -> changelog；
- 测试、指标和 checksum -> immutable artifact/ledger/gate report；
- proposal-to-implementation traceability -> case adoption matrix 的链接。

每个内部验证门后，在 adoption matrix 补齐实际 SSOT、完成状态和 evidence route。所有 proposal
item 已决定、采纳项已转译、实施项已完成/延期/拒绝且证据可达后，才能关闭 case，并把它从
Active Cases 移入 Closed Cases。

## 停止条件

遇到以下情况停止扩张性动作并报告：

- 外部方案无法绑定明确的问题包版本；
- 原始来源、external owner 或内容 fingerprint 不可确认；
- 建议仍是 `PENDING`，或虽采纳但尚未转译到内部 SSOT；
- 建议跨越项目安全、授权、数据、holdout、core 或证据边界；
- 用户只要求整理/评审方案，却尚未授权代码实施；
- 外部方案与当前代码不符，且无法分类 contract/implementation/evidence/stale-summary gap。

## 交付合同

最终说明当前 case 状态、problem/proposal 版本、采纳/拒绝/延期条目、内部 SSOT 目标、实际验证
和 evidence、剩余 blocker 与 next gate。不得仅回复“已按外部方案实现”。
