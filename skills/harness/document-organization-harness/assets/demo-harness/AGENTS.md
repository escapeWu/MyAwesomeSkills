# Agent 开发规约

> 项目上下文入口：[`docs/OVERVIEW.md`](docs/OVERVIEW.md)

这是一个轻量 harness 示例。目标是快速找到上下文、完成任务，并在结束后维护少量长期文档。

## 工作规则

- 先读本文件，再按 `OVERVIEW -> INDEX -> 1-3 份任务相关文档` 定位上下文。
- 不全量读取 `docs/`，也不因为目录缺失就创建空文档层。
- 开工前只读文档；不先写 Spec、计划、状态表、进度日志或测试阶段文档。
- 沿用仓库现有代码结构和验证方式；本 harness 不要求 TDD 或测试先行。
- 只有目标或安全、授权、兼容、数据损失等硬边界不清时才询问用户。
- 可逆实现细节由 Agent 根据当前代码和仓库惯例决定。
- 保留用户已有修改，不扩张到无关重构。

## 文档结构

```text
docs/OVERVIEW.md                 # 项目地图
docs/feature/INDEX.md            # Feature 路由
docs/feature/<feature>/README.md  # Feature 稳定知识与简洁状态
docs/reference/INDEX.md          # 跨 Feature 稳定参考路由
docs/reference/*.md              # 架构、接口、runbook
```

Feature 很小时可以直接从 OVERVIEW 链接它的 README。只有真实内容需要时才增加 collaboration、archive
或更细的设计文档。

## 完成后文档维护

1. 主 Agent 先完成实现和与风险匹配的验证。
2. 然后异步委派一个 docs SubAgent，提供最终行为摘要、修改文件、验证结果和候选文档 owner。
3. 该 SubAgent 是这一轮唯一 docs writer，只用一轮增量 patch 更新长期稳定事实。
4. 主 Agent 不等待附属文档维护，也不并发修改同一批 docs。
5. 没有 SubAgent 时，主 Agent 才在结束阶段做一次同样的轻量 patch。
6. 没有长期文档影响时不改 docs；只有导航变化时才更新 INDEX/OVERVIEW。

临时顺序、中间分析、原始命令输出和逐文件进度留在会话中。

## 项目内 Harness Skills

只注册项目实际维护的 skills。`project-docs-workflow` 负责完成后的异步 docs handoff；
`project-analysis` 只在链路复杂时使用；`add-idea` 只澄清最核心的未知项。
