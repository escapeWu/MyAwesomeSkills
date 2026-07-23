---
name: refactor-large-modules
description: 在本仓库中一致地规划、实施和审查大型文件或职责混杂模块的抽离重构。用户要求拆分、抽离、模块化、消除重复、瘦身 CLI/strategy/model/runner，或新增/修改手写文件接近 800 行、达到或超过 1000 行时使用；也用于开发前决定模块如何拆分。保持公共契约、研究语义、数据时序、证据边界和输出行为不变，不用于借重构改变业务或实验结论。
---

# 大型模块抽离

按固定的责任分类、迁移顺序和验证矩阵完成模块抽离，避免按行数或临场偏好随机拆分。

## 先守住边界

1. 读取仓库根 `AGENTS.md`、`docs/OVERVIEW.md`、owning Feature 文档和
   `docs/reference/code-organization.md`。
2. 同时使用 `project-docs-workflow`。现有文档不足、跨模块链路不清、状态所有权不明或需要
   expected-vs-implemented 分析时，再使用 `project-analysis`。
3. 只在用户授权实现重构时改代码。若用户只要求方案、审查或诊断，只产出证据和拆分方案。
4. 把重构作为独立变更轴：不得顺便改变策略逻辑、标签、阈值、费用、PIT 语义、holdout、
   artifact schema、CLI 默认值或证据状态。
5. 不修改本项目禁止修改的 Freqtrade core，不覆盖无关工作，不为获得干净工作树执行 reset/clean。

每次实际规划或实施抽离前，完整读取
[references/extraction-contract.md](references/extraction-contract.md)。该文件定义唯一的责任分类、
拆分优先级、迁移模板、兼容门禁和交付格式。

## 固定工作流

### 1. 盘点而不是猜测

- 记录目标文件的物理行数、入口、公共符号、内部符号、imports、模块级副作用、可变状态、I/O、
  artifact 和所有已知消费者。
- Python 文件先从当前 skill registry 或已加载 skill 元数据解析 `refactor-large-modules` 的实际
  根目录，再运行附带脚本；不得假设 grouped、flat 或 custom 布局：

```bash
REFACTOR_SKILL_ROOT=/absolute/path/from-the-current-skill-registry
python3 "$REFACTOR_SKILL_ROOT/scripts/inventory_python_module.py" <path>
```

- 再用 `rg` 核对每个公共符号、CLI、动态 import、配置路径和测试消费者。AST 清单不是完整调用图。
- 先运行现有聚焦测试或建立 characterization test，冻结重构前行为。没有可比较基线时不得声称
  行为等价。

### 2. 冻结不可变合同

在 owning README 或 development plan 记录：

- 不得改变的公共 import path、函数/类签名、CLI 参数和退出码；
- 输入/输出 schema、排序、精度、缺失值、异常类型、日志与 artifact 路径；
- 可变状态 owner、初始化顺序、缓存生命周期和序列化边界；
- 研究任务的 PIT、成本、会计、label、holdout 和 evidence boundary；
- 重构前的 golden/characterization 证据及允许的明确例外。

合同未冻结或存在不确定项时，先停止迁移并暴露 blocker。

### 3. 使用统一责任分类

只按以下 owner 分类符号，不创建 `part1` / `part2`：

1. `contracts`：schema、type、enum、protocol、稳定常量；
2. `domain`：无 I/O 的业务规则和纯计算；
3. `state`：状态机、生命周期和可变状态 owner；
4. `adapters`：文件、网络、数据库、框架或外部格式适配；
5. `orchestration`：用例编排和依赖组装；
6. `reporting`：artifact、序列化、摘要和展示模型；
7. `entrypoint`：CLI、strategy、FreqAI model、runner 的薄入口。

每个符号只能有一个 owner。无法归类通常说明责任仍未理解，不应先建通用 helper。

### 4. 冻结目标模块图

对每个目标文件写明：单一责任、迁入符号、公共接口、允许依赖、禁止依赖、状态归属、预计行数和
测试归属。以下 `A -> B` 表示 A 可以 import B；依赖方向固定为：

```text
entrypoint -> orchestration -> domain/state -> contracts
entrypoint -> adapters ---------------------> contracts
entrypoint -> reporting --------------------> contracts
```

Adapter/reporting 实现或消费 contract，由 entrypoint 注入；orchestration 不 import 具体 adapter。
Domain 不 import adapter、runner 或具体 Feature 入口。禁止环形 import。

### 5. 按叶子优先迁移

1. 先补 characterization/golden 测试。
2. 先抽无状态、依赖少的 contract 和纯函数。
3. 再抽 adapter、report builder 和独立 validator。
4. 状态逻辑通过显式 composition 迁移；不要用 mixin 隐藏状态所有权。
5. 最后把原文件收敛为 orchestration 或 thin entrypoint。
6. 只有真实外部消费者需要时才保留 re-export/compatibility shim，并记录删除条件。
7. 每一小步更新 imports 并运行聚焦测试；不要一次移动全部符号后才验证。

### 6. 验证等价性和结构

至少验证：

- import smoke、公共签名、CLI `--help`/默认值和异常类型；
- 受影响模块的 unit/contract/property/integration 测试；
- golden artifact 或同输入输出 diff；
- 无新环依赖、无重复实现、无死 re-export、原文件不再持有被抽离责任；
- `ruff check`、`ruff format --check`，以及任务需要的 mypy；
- `python3 scripts/validate_code_organization.py`；
- owning GOAL 指定的 lineage、causality、cost 和 evidence validator。

结构检查不能替代行为等价证据。

## 停止条件

遇到任一情况时停止扩张性修改并报告：

- 不知道哪个模块拥有可变状态或副作用顺序；
- 无法冻结公共契约，也无法建立 characterization/golden 证据；
- 拆分需要跨越用户未授权的仓库、core 或研究边界；
- 新模块必须形成环依赖才能工作；
- 所谓复用逻辑的消费者语义并不一致；
- 重构结果依赖更改业务行为才能通过测试。

## 交付合同

最终必须报告：

1. 目标与重构前证据；
2. 冻结的不变量；
3. 原责任到新 owner 的映射；
4. 目标依赖方向与公共接口；
5. 迁移和兼容处理；
6. 行数变化及是否清除 800/1000 行风险；
7. 实际运行的等价性、结构和研究门禁验证；
8. 未解决风险、临时 shim 和后续删除条件。

不得仅以“文件变短”作为完成结论。
