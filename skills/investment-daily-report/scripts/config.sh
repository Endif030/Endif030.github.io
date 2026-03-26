#!/bin/bash

# Investment Daily Report - Configuration
# 投资日报配置

# API Keys (will use environment variables if available)
TAVILY_API_KEY=${TAVILY_API_KEY:-"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"}

# Message channel configuration (for sending report)
CHANNEL="feishu"  # Options: feishu, telegram, discord, etc.
TARGET_USER="ou_bbfc027431c61a8ba421c54c7bb0f5c4"

# Search configuration
SEARCH_RESULTS_PER_MARKET=8
DEEP_SEARCH=false

# Content ratios (in percentages, must sum to 100)
A_SHARE_RATIO=70
US_STOCK_RATIO=20
CRYPTO_RATIO=10

# A-Share search keywords (70%)
A_SHARE_KEYWORDS=(
    "A股 今日要闻"
    "中国股市 政策"
    "沪深300 行情"
    "北上资金 流向"
    "A股 板块分析"
    "证监会 最新消息"
)

# US Stock search keywords (20%)
US_STOCK_KEYWORDS=(
    "US stock market today"
    "S&P500 Dow Jones Nasdaq"
    "Fed interest rates"
    "US stocks earnings"
    "Wall Street news"
)

# Crypto/Commodities search keywords (10%)
CRYPTO_KEYWORDS=(
    "Bitcoin Ethereum crypto news"
    "crypto market today"
    "futures commodities oil gold"
)

# Generated report paths
REPORT_DIR="/tmp/investment-reports"
REPORT_FILE="${REPORT_DIR}/daily_report_$(date +%Y%m%d).md"
MARKET_DATA_DIR="/root/.openclaw/workspace/memory/investment"