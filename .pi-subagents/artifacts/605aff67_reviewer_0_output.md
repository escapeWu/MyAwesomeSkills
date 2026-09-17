## Review

- **Major**: [`/Users/shancw/project/MyAwesomeSkills/skills/harness/README.md:16`](/Users/shancw/project/MyAwesomeSkills/skills/harness/README.md:16) 将可注册 skill 限定为实际存在于 `.agents/skills/harness/` 的 skill，managed block 在 [`:45`](/Users/shancw/project/MyAwesomeSkills/skills/harness/README.md:45) 和 [`:72`](/Users/shancw/project/MyAwesomeSkills/skills/harness/README.md:72) 也硬编码 grouped 路径。这与 [`UPGRADING.md:27`](/Users/shancw/project/MyAwesomeSkills/skills/harness/UPGRADING.md:27) 明确支持 flat layout、且要求不因维护而规范化路径的规则冲突。flat 项目按 README 执行时会得到不存在的路由，或无法注册实际存在的独立 skill。应将规则表述为“仅注册目标 registry 中实际存在的路径”，并要求 managed block 按 grouped/flat/custom 实际路径改写。

- **Minor**: [`/Users/shancw/project/MyAwesomeSkills/skills/harness/document-organization-harness/references/harness-bootstrap.md:273`](/Users/shancw/project/MyAwesomeSkills/skills/harness/document-organization-harness/references/harness-bootstrap.md:273) 仍写着 skills “exist or will be installed”。这既残留安装语义，也与同文件 [`:142`](/Users/shancw/project/MyAwesomeSkills/skills/harness/document-organization-harness/references/harness-bootstrap.md:142) 的“不得注册 absent skill”冲突。应改为仅注册已经存在并被目标项目接受维护的 skill。

- **Correct**: 未发现仍可执行的 harness bundle installer、bundle manifest、安装 marker、自动覆盖命令或统一 suite version。`harness-bundle.json` 与 `install_harness_bundle.py` 均为 tracked deletion；目标检索也没有发现对这两个路径的死链接。

- **Correct**: [`CHANGELOG.md`](/Users/shancw/project/MyAwesomeSkills/skills/harness/CHANGELOG.md:11) 使用当天日期 `2026-07-23`，准确覆盖 `add-idea`、Grill、三种 owner route、artifact route、Feature/Requirements/Spec/ADR 生命周期和模板变化，并在 [`:39`](/Users/shancw/project/MyAwesomeSkills/skills/harness/CHANGELOG.md:39) 明确记录 bundle manifest、installer、版本、marker、自动覆盖和统一部署语义的删除。

- **Correct**: [`UPGRADING.md`](/Users/shancw/project/MyAwesomeSkills/skills/harness/UPGRADING.md:23) 覆盖 grouped/flat/partial/extended layouts；同时包含 dirty repo 处理、逐 skill 比较、依赖顺序、目标规则保护、Feature migrate-on-touch、验证、rollback 及多项目维护。其 ownership boundary 也明确维护输入不构成实施、部署或发布授权。

- **Correct**: README、`document-organization-harness` SKILL 和 bootstrap 的主体已从 bundle 安装改为独立 skill 的逐项目维护；demo 被定位为 scaffolding example，不再是 installation payload。除上述路径规则与残留措辞外，整体方向一致。

- **Remaining test risk**: 本轮按只读要求未运行测试或格式化。未执行全仓 Markdown 链接检查，只进行了 bundle 旧路径和相关语义的定向检索。`add-idea/evals/evals.json` 提供了场景覆盖，但属于声明式 eval case，本轮未实际执行。未发现 installer tests 残留。