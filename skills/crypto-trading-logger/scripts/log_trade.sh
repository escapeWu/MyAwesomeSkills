#!/bin/bash
# scripts/log_trade.sh
# Usage: ./log_trade.sh "Thinking..." "Action..." "Result..."

# 动态获取当前工作目录，不再硬编码
WORKSPACE_DIR=$(pwd)
LOG_DIR="$WORKSPACE_DIR/logs"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
LOG_FILE="$LOG_DIR/$DATE.md"

mkdir -p "$LOG_DIR"

if [ ! -f "$LOG_FILE" ]; then
    echo "# Trading Log - $DATE" > "$LOG_FILE"
fi

cat <<EOF >> "$LOG_FILE"

## [$TIME] 交易员日志
### 🧠 思考过程 (Thinking Process)
$1

### ⚡ 执行动作 (Execution)
$2

### ✅/❌ 执行结果 (Result)
$3
---
EOF
