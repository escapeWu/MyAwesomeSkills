# 模块抽离合同

本参考为每次大型文件抽离提供固定决策规则和可复制的计划格式。不得用临时命名或机械切行替代。

## 1. 固定责任决策表

按顺序判断每个符号的 owner；命中后停止继续分类。

| 顺序 | 问题 | Owner | 典型内容 |
|---|---|---|---|
| 1 | 是否定义跨模块交换的数据或稳定接口？ | `contracts` | dataclass、TypedDict、enum、Protocol、schema、稳定常量 |
| 2 | 是否执行无外部 I/O、可由输入完全决定结果的规则？ | `domain` | 计算、归一化、校验规则、转换、选择算法 |
| 3 | 是否拥有随时间变化的内部状态或生命周期？ | `state` | 状态机、缓存 owner、position/episode state |
| 4 | 是否连接文件、网络、数据库、框架或外部格式？ | `adapters` | reader、writer、client、repository、framework adapter |
| 5 | 是否只组织多个 owner 完成一个 use case？ | `orchestration` | service、pipeline、workflow、dependency assembly |
| 6 | 是否产生 artifact、报告、序列化或展示模型？ | `reporting` | report builder、manifest、JSON/CSV output、summary |
| 7 | 是否解析入口并调用 orchestration？ | `entrypoint` | CLI、strategy、FreqAI model、runner |

若同一符号命中多个 owner，先拆符号本身。不要把复合责任原样搬入新文件。

## 2. 抽离优先级

使用以下固定顺序，前一层验证通过后再进入下一层：

1. 稳定 types、schema、protocol 和常量；
2. 无状态纯函数；
3. 独立 validator、parser、formatter 和 report builder；
4. 外部 I/O adapter；
5. 显式 state owner；
6. orchestration service；
7. thin entrypoint 和必要兼容 shim。

优先抽“低入度、低副作用、可独立测试”的叶子。不要先移动中心 orchestrator 或共享可变状态。

## 3. 复用判定

同时满足以下条件才进入共享模块：

- 至少两个真实消费者，而不是预测未来可能复用；
- 消费者需要相同语义、异常、精度和生命周期；
- 可用小型稳定 contract 描述；
- 共享模块不需要 import 任一具体消费者；
- 有 contract test 防止消费者语义漂移。

否则逻辑保留在 owning domain。禁止创建无边界 `utils.py`、`common.py`、`helpers.py`。

## 4. 状态与副作用门禁

- 每个可变状态只有一个 owner；其他模块通过方法或不可变 snapshot 访问。
- 初始化、加载、计算、写出和清理顺序必须显式，不依赖 import side effect。
- 文件、网络、时钟、随机数和环境变量通过 adapter 或显式依赖进入。
- 不把 stateful class 随意拆成 mixin；优先 composition 和明确 protocol。
- 全局缓存迁移时必须冻结 key、失效、并发、序列化和复用周期。

## 5. 兼容策略

| 情况 | 处理 |
|---|---|
| 仅仓库内部消费者，且可一次更新 | 更新 import，不保留 shim |
| 稳定公共 import path 或插件发现依赖旧路径 | 在旧路径 re-export，增加兼容测试和删除条件 |
| CLI/配置字符串按路径动态加载 | 保留薄 adapter，验证动态加载 |
| pickle/checkpoint 记录类路径 | 不直接移动；先设计显式迁移或保持原类路径 |
| artifact schema 或文件名被外部消费 | 保持完全兼容，除非另有已授权版本迁移 |

Shim 必须薄且无业务逻辑。不能用 shim 同时维护两份实现。

## 6. 实施前计划模板

把以下内容写入 owning README 或 development plan：

```markdown
### 模块抽离冻结

目标文件：`path/to/module.py`（当前 N 行）
触发原因：`超过 1000 / 800 行预警 / 多责任 / 重复实现 / 薄入口治理`

#### 不可变合同

- Public API：
- CLI/配置：
- 输入/输出与 artifact：
- 状态和副作用顺序：
- PIT/成本/会计/证据边界：
- Characterization/golden 基线：

#### 目标模块图

| 目标文件 | Owner/单一责任 | 迁入符号 | 公共接口 | 允许依赖 | 禁止依赖 | 预计行数 | 测试归属 |
|---|---|---|---|---|---|---:|---|
| `...` | `contracts` | `...` | `...` | `...` | `...` | 150 | `...` |

依赖方向（A -> B 表示 A 可以 import B）：

- `entrypoint -> orchestration -> domain/state -> contracts`
- `entrypoint -> adapters -> contracts`
- `entrypoint -> reporting -> contracts`
- orchestration 通过 contract 接收 adapter/reporting，不 import 具体实现。

#### 迁移批次

| 批次 | 迁移内容 | 兼容处理 | 批次验证 | 回退边界 |
|---|---|---|---|---|
| 1 | `...` | 无/re-export | `...` | 保留旧实现至等价通过 |
```

## 7. 必须检查的消费者

不要只搜索普通 import。至少检查：

- `from x import y`、`import x`、别名和 re-export；
- 字符串形式的 class/module path；
- CLI entry point、plugin registry、strategy/model discovery；
- fixtures、monkeypatch 路径和 mock target；
- pickle/checkpoint/serialization 的全限定类名；
- 文档命令、配置示例、shell scripts 和 CI；
- artifact reader 和下游 notebook/report。

## 8. 验证矩阵

| 维度 | 最低证据 |
|---|---|
| 行为 | characterization/golden 或已有 contract test 前后均通过 |
| 接口 | import smoke、签名、动态加载、CLI 默认值与退出码 |
| 数据 | schema、排序、精度、缺失值、异常和 artifact path 不变 |
| 状态 | 生命周期、缓存、随机种子和副作用顺序不变 |
| 结构 | 无环依赖、无重复 owner、入口变薄、目标文件小于预算 |
| 静态 | Ruff/format，必要时 mypy |
| 项目 | `validate_code_organization.py` 和受影响 Feature validator |
| 研究 | lineage、causality、cost、accounting、evidence gate（若适用） |

## 9. 拒绝模式

- 按行号建立 `module_part1.py`、`module_part2.py`；
- 把所有函数移动到新的 `utils.py`；
- 为减少行数删除注释、类型或测试；
- 迁移时顺便修改业务规则或研究参数；
- 同时保留新旧两份真实实现；
- 未搜索动态消费者就删除旧 import path；
- 只有 lint 通过，没有前后行为等价证据；
- 只报告新文件行数，不报告责任、依赖和兼容状态。
