---
name: grok_search
description: 自适应 AI 搜索与最新信息检索 skill。会先评估任务复杂度，再在 grok-4.20-fast / grok-4.20-auto / grok-4.20-expert 之间做路由，必要时采用“fast 侦察 + fast 补缺 + expert 综合”的组合流程，在速度与质量之间取平衡。
---

# grok_search

使用 Grok 兼容 OpenAI-style endpoint 做**最新信息搜索、新闻核验、时间线调查、市场舆情深挖**。

不要手写 HTTP 请求；优先使用本 skill 自带脚本：

- `scripts/grok_search.py`

## 适用场景

当用户要以下事情时，优先考虑这个 skill：

- 最新消息 / breaking news / 刚刚发生了什么
- 快速核验某条新闻、快讯、传闻
- 查当前价格、事件状态、官方/主流媒体最新说法
- 对某个新闻做时间线梳理、交叉验证、矛盾排查
- 对高价值市场消息做更深的 web-aware 调查
- 技术问题搜索：必须覆盖 Reddit 与 Hacker News 这两个社区来源

## 技术问题默认搜索源

当用户的问题属于技术问题（代码、报错、框架/库、API、版本兼容、部署、数据库、模型/benchmark 等）时，脚本会自动在 prompt 里追加硬性来源要求：**必须搜索/覆盖 Reddit 与 Hacker News**，同时仍可使用官方文档、GitHub、厂商博客等来源。若 Reddit 或 Hacker News 没有相关结果，最终回答需要显式说明“未找到相关 Reddit/HN 讨论”，不能静默省略。

## 核心升级：先评估复杂度，再选模型

Grok 当前可用的主要模型：

- `grok-4.20-fast`
- `grok-4.20-auto`
- `grok-4.20-expert`

本 skill 的默认原则：**不要所有任务都用同一个模型。**

### 路由原则

#### 1. Quick Path — 低复杂度、快查快答
适用：
- 单点事实查询
- 简单最新消息
- 单资产价格/状态核验
- 简短定义、快速真伪判断

默认模型：`grok-4.20-fast`

目标：
- 最低延迟
- 单次调用解决问题
- 不做多阶段拆解

#### 2. Balanced Path — 中等复杂度、单次高质量搜索
适用：
- 一般新闻核验
- 简单比较
- 需要来源，但不需要完整深挖
- 对某事件给一个可信总结

默认模型：`grok-4.20-auto`

目标：
- 比 fast 更稳
- 保持一次调用完成
- 适合大多数“查一下 + 给结论”任务

#### 3. Deep Path — 高复杂度、多阶段调查
适用：
- 多问题组合
- 要做时间线
- 要查前后因果 / 矛盾说法 / 是否已被调查
- 市场影响审计 / 微观结构异常调查 / 复杂比较研究
- 任何“不能只靠单次搜索回答”的任务

默认流程：
1. `grok-4.20-fast` 做 **scout**（快速侦察与拆题）
2. 若 scout 发现信息缺口，再用 `grok-4.20-fast` 做 **gap fill**（补缺）
3. 最后用 `grok-4.20-expert` 做 **final synthesis**（最终综合）

目标：
- 先快后深
- 把 expert 用在最值钱的最后一步
- 降低无意义的高成本重推理

## Agent SOP

### Step 0: Assess Complexity & Route
先评估任务复杂度，再决定模式：

- **simple** → `quick`
- **standard** → `balanced`
- **complex** → `deep`

复杂信号包括但不限于：
- 用户要求比较 / 对比 / 分析 / 审计 / 调查 / 深挖
- 同时问多个问题
- 要求时间线、交叉验证、来源、证据
- 市场类高影响消息，需要判断叙事纯度或因果链

### Step 1: 执行对应路径

#### Quick Path
你应该先拆分问题，将一个问题拆成三个不同方向的子问题。并发执行 grok-4.20-fast:

+ grok-4.20-fast：Answer1
+ grok-4.20-fast：Answer2
+ grok-4.20-fast：Answer3


#### Balanced Path
你应该先拆分问题，将一个问题拆成三个不同方向的子问题。并发执行 grok-4.20-auto:

+ grok-4.20-auto：Answer1
+ grok-4.20-auto：Answer2
+ grok-4.20-auto：Answer3

#### Deep Path
按三段式执行：

1. **Scout** — `grok-4.20-auto`
   - 拆解问题为三个不同的子问题
   - 并发调用grok-4.20-auto模型，对该任务进行分析
   - 对subAgents返回的答案进行评估，如果互相有冲突的地方，显式列出 gaps

2. **Gap Fill** — `grok-4.20-fast`（可选）
   - 仅针对 gaps 补搜
   - 避免重复跑全量深搜

3. **Final Synthesis** — `grok-4.20-expert`
   - 重新综合答案
   - 对关键主张做再确认
   - 输出结构化结论与来源

### Step 2: 最终输出
对用户回复时：
- 默认不暴露原始 tool 输出
- 抽取成高信噪比结论
- 明确哪些是已确认、哪些仍待确认

## 脚本

主脚本：

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py --query "latest OpenAI news"
```

## 常用命令

### 1) 自动模式（推荐）

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py \
  --query "latest verified news on OpenAI today"
```

脚本会自动判断使用：
- quick
- balanced
- deep

### 2) 强制 quick

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py \
  --mode quick \
  --query "BTC price now"
```

### 3) 强制 balanced

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py \
  --mode balanced \
  --query "latest verified summary of OpenAI news today"
```

### 4) 强制 expert 单次调用

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py \
  --mode expert \
  --query "compare the latest model releases from OpenAI, Anthropic, and Google"
```

### 5) 强制 deep 多阶段调查

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py \
  --mode deep \
  --query "Reuters April 2026 timeline of suspicious oil shorts before Iran announcements and whether CFTC formally investigated them" \
  --json
```

### 6) 显示路由计划

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py \
  --query "latest verified details on unusual oil shorts before Hormuz reopening announcement" \
  --show-plan
```

### 7) 结构化输出

```bash
python /Users/shancw/.hermes/skills/research/grok_search/scripts/grok_search.py \
  --query "latest OpenAI news" \
  --json
```

## 参数

- `--query`：必填，用户问题
- `--mode`：`auto | quick | balanced | expert | deep`
- `--model`：强制指定模型；指定后会跳过自动路由
- `--base-url`：覆盖 endpoint
- `--api-key`：覆盖密钥
- `--max-sources`：最多保留多少个来源 URL
- `--language`：回答语言，默认 `zh-CN`
- `--json`：输出 JSON
- `--show-reasoning`：输出 reasoning
- `--show-plan`：输出复杂度评估和模型路由计划

## 配置文件

`config.json` 示例：

```json
{
  "model": "grok-4.20-auto",
  "auto_model": "grok-4.20-auto",
  "fast_model": "grok-4.20-fast",
  "expert_model": "grok-4.20-expert",
  "default_mode": "auto",
  "language": "zh-CN",
  "technical_required_sources": ["Reddit", "Hacker News"],
  "base_url": "https://example.com/v1/",
  "api_key": "REPLACE_ME"
}
```

说明：
- `model` / `auto_model`：balanced 路径默认模型
- `fast_model`：quick / scout / gap-fill 默认模型
- `expert_model`：deep 最终综合模型
- `default_mode`：默认 `auto`
- `technical_required_sources`：技术问题搜索时必须覆盖的社区来源，默认 `Reddit` + `Hacker News`

## 输出契约

默认文本模式：

```text
概述：xxxx
搜索结果：
xxxxxxx
来源：
1. xxxx
2. xxxx
```

若 `--show-plan`，会先打印：
- requested_mode
- selected_mode
- complexity / score
- stages / models
- routing reasons

`--json` 返回：
- `query`
- `model`
- `route`
- `base_url`
- `overview`
- `search_results`
- `sources`
- `reasoning`
- `stages`
- `raw_response`

## 什么时候该用哪条路径

### 用 quick
- “BTC 现在多少钱？”
- “今天 OpenAI 有什么新消息？”
- “某新闻是真的吗？”（单点核验）

### 用 balanced
- “总结一下今天 AI 圈最重要的 3 条新闻并附来源”
- “核验一下某条新闻并给我可信摘要”

### 用 deep
- “把这件事的时间线梳理清楚，并检查前后说法有没有矛盾”
- “调查这条宏观新闻背后是否存在提前交易 / 监管跟进 / 模式重复”
- “比较多家公司最新模型发布，给出差异、证据和限制”

## 对 sentiment / audit 类任务的特别建议

若任务涉及：
- 宏观市场冲击
- 异常成交
- 监管/调查跟进
- 事件前后时间线核验
- 是否存在抢跑、信息优势交易、矛盾说法

优先考虑 `--mode deep`，因为这类问题通常天然需要：
- scout 拆题
- gap fill 补缺
- expert 最终综合

## Sub-agent Delegation（委派子 Agent 时的模式选择）

当通过 `delegate_task` 把 grok_search 委派给子 Agent 时，**不要用 `--mode deep`**。实测：

- `--mode deep`（scout → gap fill → expert 三段串行）：子 Agent 600s 必然超时，无一成功
- `--mode balanced`（grok-4.20-auto 三并发子查询）：在子 Agent 中大概率超时，成功率不足 50%
- `--mode quick`（grok-4.20-fast 三并发子查询）：子 Agent 中稳定完成，结果质量对大多数场景足够

**规则：委派子 Agent 做 grok_search 时，统一用 `--mode quick`。** 如果需要更深度的交叉验证，后续在主 Agent 中单独跑 `--mode deep` 或 `--mode expert` 补搜。

## 超时建议

从 terminal 调用时，不同模式需要不同超时：
- `quick`：60s 通常够用
- `balanced`：建议 90-120s（涉及更长推理）
- `deep`：建议 180s+（多阶段串行）
- `expert`：建议 120s（单次但重推理）

如果 balanced 在 60s 内超时，降级到 quick 模式重试是合理的 fallback。

## 注意事项

- 这个 skill 适合**快速 current-awareness + 中轻量调查**，不是完整人工情报系统
- 若结果用于高风险结论，仍应继续做更广的主流来源验证
- 不要退回到手写 requests + responses.create() 的老方式；统一走当前脚本
- 不要默认每个问题都上 expert；先做复杂度判断，控制延迟和资源消耗

## 已知陷阱：委派 sub-agent 时避免 deep 模式

当在 delegate_task 子代理内部使用 grok_search 做多场景研究时，**不要用 --mode deep**。deep 模式需要 3 个顺序阶段（scout → gap fill → expert），每个阶段一次 API 调用。当一个 agent 被分配 2 个场景时，每个场景 3 次调用，每次 60-180s，很容易超过 delegate_task 的 600s 超时。

已观察到的时间表现：
- --mode deep：3 次 API 调用后超时（600s），无结果
- --mode balanced：2 个场景约 350-370s，成功完成（grok-4.20-auto 偶尔超时会自动降级到 quick）
- --mode quick：单场景约 60s，最可靠但深度最浅

**推荐模式：** 多场景研究任务中，直接在 Hermes 主进程中运行 --mode balanced 的 grok_search（不做 sub-agent 委派），每个场景一个终端调用。这是最可靠的模式。如果必须用 delegate_task，使用 --mode quick 或明确告知 agent 每个场景限用 balanced 模式，并声明不要降级到 deep。
