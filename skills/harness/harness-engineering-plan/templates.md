# Harness Engineering Plan — Templates

## Per-TaskNode Codex Subagent Prompt Template

When dispatching a TaskNode to a Codex CLI subagent (one TaskNode per Codex instance running in its own `git worktree`), each prompt file should follow this canonical structure. This template was distilled from a real M1 W0 deployment (OracleBatchVerdict 5 parallel codex CLIs).

### Why a structured prompt is critical

A loosely-defined Codex prompt typically fails in **3 predictable ways**:

1. **Contract drift** — Codex invents schema fields or function signatures because the prompt didn't pin them precisely → merging 5 parallel TaskNodes produces fan-in conflict.
2. **Scope creep** — Codex "helpfully" implements adjacent features (e.g. "while I'm here, let me add reliability gate too") → next milestone's debt list collapses + merge gets huge.
3. **Skipped validation** — Codex declares done without running the gate commands → main agent reviews and finds tests don't actually pass.

This template eliminates all 3 by making `Expected Output`, `Acceptance Criteria`, `Validation Commands`, and `Safety Rules / Non-Goals` first-class structured sections that Codex must satisfy.

### Two-file structure

Create two artifacts per parallel batch:

1. **`_shared_context.md`** (one per wave) — project conventions, env setup, repo layout, "what tools / commands exist", anti-patterns, prohibited actions, commit style, done-file format. Every TaskNode prompt references this.
2. **`<TASK_ID>.prompt.md`** (one per TaskNode) — task-specific Expected Output / Acceptance / Validation, with explicit cross-references to `_shared_context.md`.

### Canonical sections (in order)

```markdown
# Codex Task: <TASK_ID> — <Short Title>

> 你是 Codex agent，被分配实施 <FEATURE> 的 <MILESTONE> <WAVE> 任务 **<TASK_ID>**。
> 在 git worktree `/path/to/<worktree>` 内工作（branch `feat/<branch-name>`）。

## 0. 强制阅读（开始前）

按顺序 read:
1. `_shared_context.md` — 项目通用约束 + 工程约定（必读）
2. `AGENTS.md` / `CLAUDE.md` — 项目开发规约
3. <specific spec.md / contract docs §节>
4. <tasks.md §"TaskNode: <TASK_ID>">
5. <相关现有代码文件，告诉 codex 风格参考从哪里学>

## 1. TaskNode 元数据
- Milestone / Layer / Depends On
- 预计代码量

## 2. 与并行任务的契约协调（如有）
- 防止 codex 写入与并行 TaskNode 冲突的文件
- 说明如何用占位类型 / TYPE_CHECKING / 独立模块来解耦

## 3. Expected Output
- 显式列出要新建/修改的文件路径
- 关键函数签名 / 类型 / schema
- 每个字段的语义 + spec 锚（"严格按 spec §X.Y"）
- M1-placeholder 字段策略（"该占位用 `<value>`，禁止凭直觉发明"）

## 4. Acceptance Criteria（逐条要 PASS）
- [ ] 可机器验证的具体条件
- [ ] 严禁模糊措辞（"能正确工作"是 BAD）

## 5. Validation Commands
- 准确的 shell 命令序列，Codex 必须跑过才能宣布完成
- 必须能在 worktree 内独立跑通（不依赖 W0/W1 其他并行 task 的产物）

## 6. Safety Rules / Non-Goals
- 不允许触碰的文件 / 模块（防止 scope creep）
- 不允许引入的依赖（M1 只允许 `<one specific lib>`）
- 不允许实施的能力（"reliability gate 是 M2-T2 偿还，本任务不做"）
- 不允许写的代码模式（narrative comments / 假实现 / TODO 占位）

## 7. Workflow（实施流程）
- cd worktree
- read context
- 设计 → 实现 → 测试 → commit → 写 done file

## 8. Done File 格式
- 路径：`<outputs-dir>/<TASK_ID>.done.md`
- 模板：Status / Files Changed / Acceptance Criteria 逐条 / Validation Output (tail) / Commit hash / Blockers / Debt 留给后续 milestone

## 9. 时间预算
- "预计 X-Y 分钟。超 Z 分钟报 PARTIAL 到 done file。"

最后一句：开始干活。先 read `_shared_context.md` 和 spec §X.Y。
```

### `_shared_context.md` 必备段落

```markdown
# Shared Context for <FEATURE> <MILESTONE> <WAVE> Tasks

## 项目背景
- 仓库简介
- 你在 worktree 内独立工作；主分支不会被你直接 push
- 完工后 commit 到当前 branch；主 agent 负责后续 review + merge

## 强制阅读清单（开始任务前先 read）
1. AGENTS.md / CLAUDE.md
2. 相关 spec / design docs
3. 你的 TaskNode 定义
4. 你的 TaskNode 的 Input Context 列出的所有源文件

## 工程约定（必须遵守）
### 语言版本 + 包管理器 + 测试命令
### 项目分层（不可越界）
### 代码风格
- NEVER add narrative comments
- 单文件 ≤ N 行
- pydantic v2 风格 / 类型注解优先
- 测试文件路径约定

### Schema 一致性（跨 TaskNode）
- 严格按 spec 字段名 / 类型 / 嵌套结构
- 禁止凭直觉发明字段
- 不清楚时加 `TODO(M2-followup): ...` 注释，不要擅自决定

## 验证流程
1. cd worktree
2. 安装依赖（`uv sync` / `npm install` / etc.）
3. 跑你的 Validation Commands
4. 全绿后 commit
5. 写 done file

## Commit Message 风格
- 参考最近 commit 给出示例

## 业务 / 架构核心约束（feature-specific 但跨多个 TaskNode）
- 在本 wave 中必须遵守的硬约束
- 例：OracleBatchVerdict B+D 的 "anti-bias 三大核心机制"
- 这些约束在每个 TaskNode prompt 中应再次显式提醒

## 严禁的事
- 修改 contract docs（spec / design / tasks）
- 引入未被允许的依赖
- 写 `pass` 或 `raise NotImplementedError` 糊弄
- 输出违反 safety boundary 的代码（observe-only / no order execution / 等）
- 修改 git config / 跳过 hooks / force push

## 出现问题时
- 编译/导入失败：怎么办
- 单测失败：怎么排查
- spec 矛盾：写 "BLOCKED: spec ambiguity at <锚>"，不要乱发明
- 超时：报 "PARTIAL: done X, blocked on Y"，主 agent 接力
```

### 必须遵守的设计原则

1. **每个 TaskNode prompt 是自包含**：Codex 只读 spec docs + shared context + 自己的 prompt 就能完成；不假设它能看到主 agent 之前的 conversation。
2. **Expected Output 必须列文件路径 + 函数签名**：不能只说"实现 X 功能"，要说"新建 `src/path/file.py`、含 `async def foo(...) -> Bar:`"。
3. **Acceptance Criteria 必须机器可验证**：每条都能映射到一行 pytest assertion 或一个 grep 命令。
4. **Validation Commands 必须独立跑通**：在 W0 阶段的并行 task，每个 task 的单测**不能**依赖其他 task 的产出（用 mock dict 数据，不 import 邻居 task 的类型）。
5. **Safety Rules 必须列举 non-goals**：明确说"这是 M2-T2 偿还，本任务不做"，避免 Codex helpful 越界。
6. **跨 TaskNode 契约协调段**（§2）必须存在：明确告诉 Codex 防止与并行 task 冲突的策略（独立模块 / 占位类型 / TYPE_CHECKING / 复制 catalog 等）。
7. **Done file 是双向沟通通道**：Codex 在 done file 中明示 Status (complete/partial/blocked) + 实际 cross-check 表（如 catalog 实际项目数 vs spec 预期）+ debt 列表 → 主 agent 据此决定合并 / 修复 / 重派。

### 并行调度注意事项

- LLM API rate limit 是真实存在的硬约束。一次性 spawn 5 个 Codex 会撞 OpenAI 429。
- 推荐策略：**错峰启动**（每 60-120 秒一个）或 **限速并行**（最多 2-3 个同时跑）。
- Smoke test 单 TaskNode 跑通后再批量启动，避免重复撞限流。
- 每个 worktree 第一次跑测试需要 `uv sync` 安装 .venv，会比较慢；预算时间要算在内。

### 反例：什么是不好的 Codex prompt

- ❌ "实现 OracleBatchVerdict feature" — 太宽，scope creep 必然发生
- ❌ "看下 spec.md 自己决定怎么做" — 没有 Acceptance Criteria 锚，无法验证
- ❌ "写一个 BDState class" — 没指定文件路径、字段、prompt 与并行 task 的协调
- ❌ 把所有 TaskNodes 塞进一个 prompt — 一旦失败整体回滚成本大、不能并行

### 执行器映射：把同一份 prompt 派给 Cursor `Task` 或 `codex` CLI

同一套 8-section prompt，两种派发器二选一或混用（见 SKILL.md §"Dispatching TaskNodes to Parallel Subagents"）。

**A. Cursor `Task` 工具 subagent（IDE 内首选）**

- 一个 wave 的 N 个相互独立 TaskNode，在**同一条消息**里发出 N 个 `Task` 调用以实现真正并行。
- 每个 `Task` 的 `prompt` = 该 TaskNode 的完整 8-section prompt（在 prompt 顶部贴 `_shared_context.md` 内容，或让 subagent 先 read 它）。
- `subagent_type` 选择：纯实现 / 多步用 `generalPurpose`；偏命令行 / 脚本用 `shell`；要 N 选优用 `best-of-n-runner`（自带独立 worktree）。
- 长任务设 `run_in_background: true`，完成有通知；主 agent 收齐各 subagent 产出后**串行** review + 合并。
- worktree 默认不开；仅当并行 TaskNode 改**重叠文件**时，用 `best-of-n-runner` 或显式 worktree 隔离。

示例（一条消息内并行 3 个 TaskNode）：

```text
Task(subagent_type="generalPurpose", description="M2-T01 adapter A", prompt="<M2-T01 的 8-section prompt>")
Task(subagent_type="generalPurpose", description="M2-T02 adapter B", prompt="<M2-T02 的 8-section prompt>")
Task(subagent_type="generalPurpose", description="M2-T03 adapter C", prompt="<M2-T03 的 8-section prompt>")
```

**B. `codex` CLI（GPT 系列质量 / 长任务 / 已有 sandbox 链路）**

每个 TaskNode 一个 `/tmp` spec 文件 + stdin 重定向后台启动；禁止裸 prompt、禁止 `"$(cat ...)"`：

```bash
# 1. 写 spec（含 8-section，尤其 acceptance / validation / safety）
SPEC_FILE="/tmp/codex-taskspec-$(date +%s)-$$-M2-T01.md"
cp tasks/<module>/prompts/M2-T01.prompt.md "$SPEC_FILE"

# 2. stdin 重定向后台启动（防 stdin 饿死、零文件改动假活）
codex exec --full-auto - < "$SPEC_FILE" 2>&1 | tee /tmp/codex-M2-T01.log &

# 3. 退出后捡未 git add 的新文件 + 校验 acceptance
git status --short
```

- 错峰启动（每 60-120s 一个）或限并发 2-3 个，避免 OpenAI 429。
- 进阶：cron / tmux 监督、Release-the-Hounds、L1 全自动属于 `autonomous-codex-supervision` skill 的范畴（若已安装）；本 harness 不内置该环境耦合。

---

## Wave Overview Diagram (Top-Down)

Every milestone `tasks.md` should open with a top-down wave overview. **Do not** use multi-column side-by-side ASCII (they break at narrow widths / Markdown preview / Slack paste).

Canonical template — replace `<...>` placeholders:

```text
W0 — <name> (parallel|serial)
├── <ID>-T<n> <slug>
├── <ID>-T<n> <slug>
└── <ID>-T<n> <slug>
                ▼ (准入：W0 全部 done)
W1 — <name> (parallel|serial)
├── <ID>-T<n> <slug>
├── <ID>-T<n> <slug>
└── <ID>-T<n> <slug>
                ▼ (准入：W1 全部 done)
W2 — <name> (parallel|serial)
├── <ID>-T<n> <slug>
├── <ID>-T<n> <slug>
└── <ID>-T<n> <slug>
```

Required:
- One wave per vertical block.
- Tree connectors (`├──` / `└──`).
- Wave gate arrow (`▼`) between blocks, with `(准入：W<n> 全部 done)` annotation.
- Task lines stay flat (one per row); intra-wave dependency lives in TaskNode `Depends On` field, not in the diagram.

Always follow the diagram with a metadata table:

```markdown
| Wave | 并行度 | TaskNodes | 准入 |
|------|--------|-----------|------|
| **W0** <name> | <high|medium|serial> | <T-list> | <entry condition> |
| **W1** <name> | <high|medium|serial> | <T-list> | <entry condition> |
| **W2** <name> | <high|medium|serial> | <T-list> | <entry condition> |
```

See SKILL.md §"Wave overview visualization must be top-down" for full rationale and counter-example.

---

## Milestone Roadmap Details

### M0 - Planning Gate

Purpose: establish the plan before implementation begins.

Responsibilities:
- define feature goal, non-goals, safety boundaries;
- create implementation plan and task board;
- identify existing code/docs/contracts;
- call `project-analysis` first when module boundaries, data flow, sequence, or performance risk are too unclear to fill TaskNode `Input Context` with evidence;
- decide milestone shape.

Example TaskNodes:

```text
M0-T01 Create implementation plan
M0-T02 Create task board
```

Gate: Plan and task board exist; M1 can start without guessing field names, scope, or safety boundaries.
If `project-analysis` was needed, its new or updated docs are linked from the relevant TaskNodes and reachable through the docs indexes.

### M1 - Contract Foundation

Purpose: freeze names, schemas, statuses, input/output boundaries, safety metadata, and test matrix before implementation.

Responsibilities:
- define output contract and safety metadata;
- define input snapshot and freshness/degradation contract;
- define fixture/test matrix;
- update architecture/interface docs with reserved stage and boundaries.

Example TaskNodes:

```text
M1-T01 Define output contract and safety metadata
M1-T02 Define input snapshot and freshness/degradation contract
M1-T03 Define fixture and test matrix
M1-T04 Update architecture/interface docs with reserved stage and boundaries
```

Parallelism: High. All M1 tasks depend on M0 but should not depend heavily on each other if M0 is clear.

Gate: Contracts/docs/tests define stable names and boundaries. Implementation tasks no longer need to invent schema fields or safety semantics.

### M2 - Input Adapters

Purpose: normalize upstream/cache/source data into a stable input contract.

Responsibilities:
- read existing source/cache helper outputs;
- normalize missing/stale data;
- preserve timestamps, freshness, and degradation reasons;
- aggregate per-source input snapshots into a unified document.

Example TaskNodes:

```text
M2-T01 Implement Source A adapter
M2-T02 Implement Source B adapter
M2-T03 Implement Source C adapter
M2-T04 Implement input aggregator and degradation summary
```

Parallelism: High. Each source adapter can be implemented independently once M1 contracts exist.

Gate: All adapters pass unit tests. Aggregated input documents preserve source health and degrade safely instead of fabricating success.

### M3A - Evidence Scorers

Purpose: convert normalized inputs into independent, auditable evidence items.

Responsibilities:
- classify proximity or trigger candidates;
- score each source independently;
- produce evidence items with source, direction, confidence/strength, reason, and timestamps;
- preserve degraded reasons;
- avoid final decision logic inside individual scorers.

Example TaskNodes:

```text
M3A-T01 Implement proximity / trigger candidate classifier
M3A-T02 Implement Source A evidence scorer
M3A-T03 Implement Source B evidence scorer
M3A-T04 Implement Source C evidence scorer
```

Parallelism: High after M1/M2. Scorers should be independent and produce a common evidence contract.

Gate: Independent evidence scorers pass unit tests and produce auditable evidence without mutating upstream data.

### M3B - Resolver & Document Builder

Purpose: combine evidence into final status decisions and produce the feature document.

Responsibilities:
- resolve aligned evidence;
- detect conflicts and invalidations;
- preserve degraded source reasons;
- produce final per-item/per-symbol summaries;
- preserve upstream fields unchanged;
- keep safety metadata explicit.

Example TaskNodes:

```text
M3B-T01 Implement conflict and invalidation resolver
M3B-T02 Implement document builder and summary aggregator
```

Parallelism: Medium. Resolver usually comes before document builder if the document builder depends on final status semantics.

Gate: Resolver and document builder pass status tests covering waiting, candidate, confirmed, rejected, conflicted, and degraded states.

### M4 - Product Surface Integration

Purpose: connect the completed core behavior into the runtime pipeline, APIs, UI, notifications, and docs.

Responsibilities:
- add a new pipeline stage or runtime step;
- persist input/output snapshots;
- expose the result through existing detail APIs;
- update frontend/shared types;
- render a human-readable summary;
- update notification summaries if applicable;
- update architecture/interface/runbook docs.

Example TaskNodes:

```text
M4-T01 Add runtime pipeline stage
M4-T02 Add API compatibility and snapshot tests
M4-T03 Update frontend types/components
M4-T04 Update notification summary
M4-T05 Update docs and runbook
```

Parallelism: Medium-high. API/frontend/notify/docs can often run in parallel after the pipeline stage contract is stable.

Gate: The new capability appears in runtime snapshots and product surfaces without changing safety boundaries or breaking existing APIs.

### M5 - Integration & Verification

Purpose: final gate after all implementation waves are integrated.

Responsibilities:
- verify all task outputs are integrated;
- run full test suite, compile/typecheck;
- run bounded smoke validation and safety scan;
- confirm no unresolved dirty source changes remain;
- record final evidence.

Example TaskNodes:

```text
M5-T01 Verify integrated diff and task completion
M5-T02 Run full validation and safety scan
M5-T03 Run bounded smoke test
```

Parallelism: Controlled serial gate. M5 is intentionally not a broad parallel implementation wave.

Gate: Full validation passes, bounded smoke passes, safety scan is clean, and final evidence is recorded.

---

## Generic Task Board Structure

> taskBoard 是临时执行文件，存放在 `.agents/skills/harness/harness-engineering-plan/tasks/<module>/taskBoard.md`，不放入 `docs/`。
> 任务完成后移入 `tasks/archive/`，然后提炼结论更新 `docs/`。

```markdown
# <Feature Name> Task Board

## Board State

**Feature:** <feature name>

**Active Milestone:** M0 - Planning Gate

**Active Layer:** 1

**Global Status:** planned | in_progress | complete | blocked

**Global Safety Boundary:** <explicit boundary>

**Core Rule:** <one sentence invariant>

## Milestone Overview

| Milestone | Purpose | Parallelism Expectation | Status | Gate |
|---|---|---:|---|---|
| M0 | Planning Gate | n/a | planned | Plan + taskBoard saved |
| M1 | Contract Foundation | high | planned | Contracts/docs/tests stable |
| M2 | Input Adapters | high | planned | Inputs normalize missing/stale data |
| M3A | Evidence Scorers | high | planned | Independent scorers pass tests |
| M3B | Resolver & Document | medium | planned | Final document statuses pass tests |
| M4 | Product Integration | medium-high | planned | Runtime/API/UI surfaces expose output |
| M5 | Verification | serial gate | planned | Full validation + smoke + safety clean |

## Global Validation Commands

```bash
<test command>
<compile/typecheck command>
```

## Global Done Conditions

- [ ] All milestone gates complete.
- [ ] Runtime smoke proves feature is visible.
- [ ] Safety boundary intact.
- [ ] Tests and compile/typecheck pass.
- [ ] Final evidence recorded.

---

# TaskNode Tree

## Root TaskNode: <ROOT>

**Title:** <feature title>

**Status:** planned

**Children:** M0, M1, M2, M3A, M3B, M4, M5
```

---

## Integration Gate Checklist

Use this checklist before advancing to the next milestone:

- [ ] All required TaskNodes are done.
- [ ] Each TaskNode has validation evidence.
- [ ] No implementation work remains unreviewed.
- [ ] No unresolved merge or integration conflicts.
- [ ] Shared files were synthesized intentionally, not overwritten by last writer.
- [ ] Targeted tests pass.
- [ ] Full milestone validation passes.
- [ ] Compile/typecheck passes where applicable.
- [ ] Safety scan is clean.
- [ ] Docs/API/schema references are updated.
- [ ] Runtime smoke passes if the milestone changes runtime behavior.
- [ ] Local secrets/configs/runtime artifacts are excluded.
- [ ] Checkpoint is recorded.

---

## Safety and Non-Goal Template

Every feature should explicitly state what it must not do:

```markdown
## Safety Boundaries / Non-Goals

This feature must not:

- read or expose local secrets, tokens, cookies, private config, or credentials;
- commit runtime data, caches, logs, database files, or generated build output;
- change unrelated upstream scoring semantics;
- introduce execution capabilities outside the feature boundary;
- degrade existing API compatibility unless explicitly approved;
- fabricate successful output when source data is missing or stale.
```

For observe-only analysis systems, add:

```markdown
- no order execution;
- no wallet/private-key access;
- no private exchange trading calls;
- no executable entry/exit/SL/TP instructions;
- analysis output must remain advisory/diagnostic only.
```

---

## Validation Evidence Template

Every completed milestone should record evidence:

```markdown
## Done Evidence

- Implemented files:
  - `src/...`
  - `tests/...`
- Targeted validation:
  - `<command>` → passed, N tests
- Full validation:
  - `<command>` → passed
- Smoke validation:
  - `<what was exercised>` → passed
- Safety scan:
  - clean; no secrets or prohibited capability found
- Checkpoint:
  - `<commit hash or artifact id>`
```
