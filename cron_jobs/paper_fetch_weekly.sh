#!/bin/bash
# 论文收集任务 - 每周一 09:00

export PATH="/root/.nvm/versions/node/v22.22.0/bin:$PATH"
LOG_FILE="/tmp/paper-fetch.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始收集论文..." >> "$LOG_FILE"

cd /root/.openclaw/workspace/skills/paper-research-assistant
python3 scripts/fetch_papers.py --discipline all --max-results 10 >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    /root/.local/share/pnpm/openclaw message send \
        --channel feishu \
        -t 'ou_bbfc027431c61a8ba421c54c7bb0f5c4' \
        -m '📚 本周论文收集完成！已更新论文数据库' \
        >> "$LOG_FILE" 2>&1
else
    /root/.local/share/pnpm/openclaw message send \
        --channel feishu \
        -t 'ou_bbfc027431c61a8ba421c54c7bb0f5c4' \
        -m '⚠️ 论文收集任务执行失败，请检查日志' \
        >> "$LOG_FILE" 2>&1
fi
