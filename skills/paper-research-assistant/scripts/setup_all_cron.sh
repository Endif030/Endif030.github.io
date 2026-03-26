#!/bin/bash
# Paper Research Assistant - 定时任务自动设置脚本
# 生成时间: 2026-03-09

USER_ID="ou_bbfc027431c61a8ba421c54c7bb0f5c4"
CHANNEL="feishu"
WORKSPACE="/root/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/paper-research-assistant"

echo "🕐 正在设置 Paper Research Assistant 定时任务..."
echo "   用户ID: $USER_ID"
echo ""

# ============================================================
# 1. 论文收集任务 - 每周一 09:00
echo "📚 设置论文收集任务..."

openclaw cron add \
  --name "paper-fetch-all" \
  --at "0 9 * * 1" \
  --session isolated \
  --deliver \
  --channel $CHANNEL \
  --to "$USER_ID" \
  --post-to-main none \
  --message "请使用 message 工具发送：📚 正在收集本周各学科热门论文..."

echo "   ✅ paper-fetch-all (每周一 09:00)"

# ============================================================
# 2. 知识卡片推送 - 每日4次
echo ""
echo "🧠 设置知识卡片推送任务..."

# 08:30 晨间推送
openclaw cron add \
  --name "flashcard-push-0830" \
  --at "30 8 * * *" \
  --session isolated \
  --deliver \
  --channel $CHANNEL \
  --to "$USER_ID" \
  --post-to-main none \
  --message "cd $SKILL_DIR && python3 scripts/spaced_repetition.py --slot 08:30 --user-id $USER_ID"

echo "   ✅ flashcard-push-0830 (每天 08:30)"

# 12:00 午间推送
openclaw cron add \
  --name "flashcard-push-1200" \
  --at "0 12 * * *" \
  --session isolated \
  --deliver \
  --channel $CHANNEL \
  --to "$USER_ID" \
  --post-to-main none \
  --message "cd $SKILL_DIR && python3 scripts/spaced_repetition.py --slot 12:00 --user-id $USER_ID"

echo "   ✅ flashcard-push-1200 (每天 12:00)"

# 16:00 下午推送
openclaw cron add \
  --name "flashcard-push-1600" \
  --at "0 16 * * *" \
  --session isolated \
  --deliver \
  --channel $CHANNEL \
  --to "$USER_ID" \
  --post-to-main none \
  --message "cd $SKILL_DIR && python3 scripts/spaced_repetition.py --slot 16:00 --user-id $USER_ID"

echo "   ✅ flashcard-push-1600 (每天 16:00)"

# 20:00 晚间推送
openclaw cron add \
  --name "flashcard-push-2000" \
  --at "0 20 * * *" \
  --session isolated \
  --deliver \
  --channel $CHANNEL \
  --to "$USER_ID" \
  --post-to-main none \
  --message "cd $SKILL_DIR && python3 scripts/spaced_repetition.py --slot 20:00 --user-id $USER_ID"

echo "   ✅ flashcard-push-2000 (每天 20:00)"

# ============================================================
# 3. 周报生成 - 每周日 21:00
echo ""
echo "📊 设置周报任务..."

openclaw cron add \
  --name "weekly-report" \
  --at "0 21 * * 0" \
  --session isolated \
  --deliver \
  --channel $CHANNEL \
  --to "$USER_ID" \
  --post-to-main none \
  --message "cd $SKILL_DIR && python3 scripts/generate_report.py --type weekly --save && 请使用 message 工具发送：📊 本周阅读报告已生成"

echo "   ✅ weekly-report (每周日 21:00)"

# ============================================================
# 4. 月报生成 - 每月1日 21:00
echo ""
echo "📊 设置月报任务..."

openclaw cron add \
  --name "monthly-report" \
  --at "0 21 1 * *" \
  --session isolated \
  --deliver \
  --channel $CHANNEL \
  --to "$USER_ID" \
  --post-to-main none \
  --message "cd $SKILL_DIR && python3 scripts/generate_report.py --type monthly --save && 请使用 message 工具发送：📊 本月阅读报告已生成"

echo "   ✅ monthly-report (每月1日 21:00)"

# ============================================================
echo ""
echo "=========================================="
echo "✅ 所有定时任务设置完成！"
echo "=========================================="
echo ""
echo "📋 任务列表："
echo "   1. paper-fetch-all      - 每周一 09:00  收集论文"
echo "   2. flashcard-push-0830  - 每天 08:30   知识卡片推送"
echo "   3. flashcard-push-1200  - 每天 12:00   知识卡片推送"
echo "   4. flashcard-push-1600  - 每天 16:00   知识卡片推送"
echo "   5. flashcard-push-2000  - 每天 20:00   知识卡片推送"
echo "   6. weekly-report        - 每周日 21:00  周报"
echo "   7. monthly-report       - 每月1日 21:00 月报"
echo ""
echo "💡 管理命令："
echo "   查看任务: openclaw cron list"
echo "   删除任务: openclaw cron remove <name>"
echo "   暂停任务: openclaw cron pause <name>"
echo "   恢复任务: openclaw cron resume <name>"
