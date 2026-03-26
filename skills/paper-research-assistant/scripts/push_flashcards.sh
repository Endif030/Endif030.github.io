#!/bin/bash
# 知识卡片推送包装脚本 - 调用 message 工具发送

SKILL_DIR="/root/.openclaw/workspace/skills/paper-research-assistant"
SLOT=$1

if [ -z "$SLOT" ]; then
    echo "Usage: $0 <time_slot>"
    echo "Example: $0 08:30"
    exit 1
fi

# 生成消息内容
MESSAGE=$(cd "$SKILL_DIR" && python3 scripts/spaced_repetition_v2.py --slot "$SLOT" --message-only 2>/dev/null)

# 如果生成失败，使用默认消息
if [ -z "$MESSAGE" ]; then
    MESSAGE="⏰ ${SLOT} 知识卡片推送\n\n⚠️ 消息生成失败，请检查系统状态"
fi

# 输出指令（供子代理执行）
echo "请使用 message 工具发送以下内容："
echo ""
echo "$MESSAGE"
