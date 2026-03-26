---
name: investment-daily-report
description: Automatic daily investment news report generator for A-shares, US stocks, and crypto markets.
homepage: 
metadata: 
  clawdbot:
    emoji: "📈"
    requires:
      bins: ["node", "bash"]
      env: ["TAVILY_API_KEY"]
      skills: ["tavily-search", "summarize"]
---

# Investment Daily Report

Generate daily investment news briefings with customizable market coverage ratios.

## Features

- **A-shares (A股)**: 70% coverage
- **US stocks (美股)**: 20% coverage  
- **Crypto/Commodities (币圈/期货)**: 10% coverage
- Automatic deduplication and summarization
- Scheduled delivery via cron

## Setup

1. Get Tavily API key from https://tavily.com
2. Set environment variable: `export TAVILY_API_KEY="your-key"`
3. Configure cron job for daily execution

## Usage

### Generate report manually
```bash
bash {baseDir}/scripts/generate-report.sh
```

### Configure cron job (daily at 08:00 China time)
```bash
# Add to crontab
crontab -e

# Add this line (China timezone is UTC+8, so 00:00 UTC = 08:00 CST)
0 0 * * * cd /root/.openclaw/workspace/skills/investment-daily-report && bash scripts/generate-report.sh
```

## Report Format

Report is automatically sent via configured message channel (Feishu/Telegram/etc).

Sections:
1. 📊 **Market Overview** - Key indices performance
2. 🇨🇳 **A-Share Focus** (70%) - Chinese market news, policy updates, sector movements
3. 🇺🇸 **US Market Pulse** (20%) - US stocks, economic data, earnings
4. 🪙 **Crypto & Commodities** (10%) - Digital assets, futures, commodities
5. 💡 **Key Takeaways** - Summarized actionable insights

## Configuration

Edit `scripts/config.sh` to customize:
- Search keywords for each market
- Source preferences
- Summary length
- Output format