#!/bin/bash
# 论文阅读月报 - 每月1日 21:00

export PATH="/root/.nvm/versions/node/v22.22.0/bin:$PATH"
LOG_FILE="/tmp/monthly-report.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始生成月报..." >> "$LOG_FILE"

cd /root/.openclaw/workspace/skills/paper-research-assistant
python3 scripts/generate_report.py --type monthly --save >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    /root/.local/share/pnpm/openclaw message send \
        --channel feishu \
        -t 'ou_bbfc027431c61a8ba421c54c7bb0f5c4' \
        -m '📊 本月论文阅读报告已生成！' \
        >> "$LOG_FILE" 2>&1
else
    /root/.local/share/pnpm/openclaw message send \
        --channel feishu \
        -t 'ou_bbfc027431c61a8ba421c54c7bb0f5c4' \
        -m '⚠️ 月报生成失败，请检查日志' \
        >> "$LOG_FILE" 2>&1
fi
