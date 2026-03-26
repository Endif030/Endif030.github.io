#!/bin/bash

# Investment Daily Report Generator
# 投资日报生成器 - 主入口脚本
# 
# 该脚本已重构为调用纯 Node.js 实现
# 主要逻辑在 generate-report.js 中

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查 Node.js
if ! command -v node >/dev/null 2>&1; then
    echo "❌ Node.js not found! Please install Node.js first."
    exit 1
fi

# 检查环境变量
if [ -z "${TAVILY_API_KEY}" ]; then
    echo "❌ TAVILY_API_KEY environment variable is not set!"
    echo ""
    echo "To fix this:"
    echo "1. Get your API key from https://tavily.com"
    echo "2. Run: export TAVILY_API_KEY='your-key-here'"
    echo "3. Or add to ~/.bashrc for persistence"
    exit 1
fi

# 执行 Node.js 报告生成器
echo "🚀 Starting daily investment report generation with Node.js..."
echo ""

export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

cd "${SCRIPT_DIR}/.."
node "${SCRIPT_DIR}/generate-report.js"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ Report generation completed successfully!"
else
    echo ""
    echo "❌ Report generation failed with exit code: $exit_code"
fi

exit $exit_code