#!/bin/bash
# 知识卡片推送发送脚本 - 由 crontab 调用
# 使用方法: send_flashcards.sh <time_slot>

export PATH="/root/.nvm/versions/node/v22.22.0/bin:/root/.local/bin:/root/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SKILL_DIR="/root/.openclaw/workspace/skills/paper-research-assistant"
SLOT=$1
USER_ID="ou_bbfc027431c61a8ba421c54c7bb0f5c4"
LOG_FILE="/tmp/flashcard_push.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting push for slot $SLOT" >> "$LOG_FILE"

if [ -z "$SLOT" ]; then
    echo "Error: No time slot provided" >> "$LOG_FILE"
    exit 1
fi

# 生成消息内容
MESSAGE=$(cd "$SKILL_DIR" && python3 scripts/spaced_repetition_v2.py --slot "$SLOT" --message-only 2>&1)

if [ -z "$MESSAGE" ]; then
    echo "Error: Failed to generate message" >> "$LOG_FILE"
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Message generated, sending..." >> "$LOG_FILE"

# 使用 openclaw message send 发送消息
# 注意：这里使用 system 工具的 message send 功能
openclaw message send --channel feishu --to "$USER_ID" "$MESSAGE" 2>> "$LOG_FILE"

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Message sent successfully" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Failed to send message, exit code: $RESULT" >> "$LOG_FILE"
fi

echo "---" >> "$LOG_FILE"
exit $RESULT
