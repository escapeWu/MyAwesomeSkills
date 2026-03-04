# Crypto Trading Logger

记录加密货币交易员的思考过程、执行动作和结果到本地 Markdown 日志文件中。确保交易过程透明且可追溯。

## 🚀 快速安装与配置 (Quick Start)

为了让你的 Agent 具备专业的交易记录能力，请遵循以下步骤：

### 1. 安装 Skill
将此目录克隆或移动到你的 OpenClaw Skill 加载路径中（例如 `~/project/skills/skills/` 或 Agent 的 `skills/` 目录）。

```bash
# 示例：克隆仓库
git clone https://github.com/escapeWu/MyAwesomeSkills.git
```

### 2. 配置行为准则 (Update SOUL.md)
将以下内容复制到你工作目录下的 `SOUL.md` 中。这是确保 Agent **自觉调用**此工具的关键。

```markdown
## 交易员准则 (Trader's Code)

- **透明性**：每一笔交易操作（包括分析、下单、结果）必须调用 `crypto-trading-logger` 进行本地持久化记录。
- **可追溯性**：严禁在没有日志记录的情况下执行实盘操作。日志是复盘的唯一依据。
- **严谨性**：思考过程必须包含逻辑支撑（如技术指标、情绪分析、风险评估）。
```

### 3. 权限设置
确保脚本具有执行权限：
```bash
chmod +x skills/crypto-trading-logger/scripts/log_trade.sh
```

## 🛠️ 功能特性

- **自动化日志**：按日期自动生成 `logs/YYYY-MM-DD.md`。
- **结构化记录**：包含【思考过程】、【执行动作】、【执行结果】三个核心区块。
- **动态路径**：自动识别当前工作目录 (`pwd`)，无需硬编码配置。

## 📖 使用示例 (Internal Use)

Agent 在执行任务时应按如下方式调用：

```bash
./scripts/log_trade.sh "观察到 RSI 背离" "市价买入 0.1 BTC" "✅ 成功"
```

---
*由 escapeWu 交易员团队维护。📈*
