#!/bin/bash

# Test script for investment daily report
# 投资日报生成测试脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check dependencies
echo "🔧 Checking dependencies..."

# Check Node.js
if command -v node >/dev/null 2>&1; then
    echo "✅ Node.js found: $(node --version)"
else
    echo "❌ Node.js not found (required for tavily-search)"
    exit 1
fi

# Check Tavily API key
if [ -z "${TAVILY_API_KEY}" ]; then
    echo "⚠️  TAVILY_API_KEY not set in environment"
    echo "   Please set it with: export TAVILY_API_KEY='your-key'"
    echo "   Get your key from: https://tavily.com"
    read -p "   Do you have a Tavily API key? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "   Enter your Tavily API key: " key
        export TAVILY_API_KEY="$key"
        echo "export TAVILY_API_KEY=\"$key\"" >> ~/.bashrc
        echo "   Key saved to ~/.bashrc"
    else
        echo "   Please sign up at https://tavily.com to get a free API key"
        exit 1
    fi
else
    echo "✅ TAVILY_API_KEY is set"
fi

# Check tavily-search skill
echo
echo "📂 Checking tavily-search skill..."
if [ -f "${SCRIPT_DIR}/../../tavily-search/scripts/search.mjs" ]; then
    echo "✅ tavily-search skill found"
else
    echo "❌ tavily-search skill not found"
    exit 1
fi

# Test search
echo
echo "🔍 Testing search functionality..."
node "${SCRIPT_DIR}/../../tavily-search/scripts/search.mjs" "A股 今日要闻" -n 2 --topic news
if [ $? -eq 0 ]; then
    echo "✅ Search test successful"
else
    echo "❌ Search test failed"
    exit 1
fi

echo
echo "🎉 All checks passed! System is ready."
echo
echo "📝 To set up automatic daily delivery at 08:00 China time:"
echo "   1. Run: crontab -e"
echo "   2. Add this line:"
echo "      0 0 * * * cd ${SCRIPT_DIR}/../../ && bash investment-daily-report/scripts/generate-report.sh"
echo "   3. Save and exit"
echo
echo "🚀 To generate a test report now, run:"
echo "   bash ${SCRIPT_DIR}/generate-report.sh"