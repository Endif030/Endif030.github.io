#!/bin/bash
# 每周初始化任务 - 每周一 09:00
# 合并功能：收集论文 + 生成周文档 + 下载前3篇PDF + 生成前3篇注释稿

export PATH="/root/.nvm/versions/node/v22.22.0/bin:$PATH"
LOG_FILE="/tmp/weekly-init.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始每周初始化..." >> "$LOG_FILE"

cd /root/.openclaw/workspace/skills/paper-research-assistant

# 执行每周初始化脚本
python3 scripts/weekly_init.py >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 每周初始化完成" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 每周初始化失败，退出码: $EXIT_CODE" >> "$LOG_FILE"
    
    # 发送失败通知
    /root/.local/share/pnpm/openclaw message send \
        --channel feishu \
        -t 'ou_bbfc027431c61a8ba421c54c7bb0f5c4' \
        -m '⚠️ 每周论文初始化任务执行失败，请检查 /tmp/weekly-init.log' \
        >> "$LOG_FILE" 2>&1
fi

exit $EXIT_CODE
