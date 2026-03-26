#!/usr/bin/env python3
"""
定时任务设置脚本 - 配置OpenClaw Cron任务
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# 配置
SKILL_DIR = Path("/root/.openclaw/workspace/skills/paper-research-assistant")
CRON_CONFIG_FILE = Path("/root/.openclaw/workspace/paper-research/.cron_config.json")


def get_cron_commands(user_id, channel="feishu"):
    """获取所有定时任务命令"""
    
    commands = []
    
    # 1. 每周一 09:00 收集论文
    for discipline in ["ai", "psychology", "social-science", "anthropology", "philosophy", "game-studies"]:
        cmd = f'''openclaw cron add \\
  --name "paper-fetch-{discipline}" \\
  --at "0 9 * * 1" \\
  --session isolated \\
  --deliver \\
  --channel {channel} \\
  --to "{user_id}" \\
  --post-to-main none \\
  --message "请使用 message 工具发送：📚 正在收集本周 {discipline} 领域论文..." && \\
  cd {SKILL_DIR} && python scripts/fetch_papers.py --discipline {discipline} --max-results 10'''
        commands.append((f"paper-fetch-{discipline}", cmd))
    
    # 2. 知识卡片推送 - 每日4次
    for slot in ["08:30", "12:00", "16:00", "20:00"]:
        hour, minute = slot.split(":")
        cron_time = f"{minute} {hour} * * *"
        
        cmd = f'''openclaw cron add \\
  --name "flashcard-push-{slot.replace(':', '')}" \\
  --at "{cron_time}" \\
  --session isolated \\
  --deliver \\
  --channel {channel} \\
  --to "{user_id}" \\
  --post-to-main none \\
  --message "cd {SKILL_DIR} && python scripts/spaced_repetition.py --slot {slot} --user-id {user_id}"'''
        commands.append((f"flashcard-push-{slot.replace(':', '')}", cmd))
    
    # 3. 周报生成 - 每周日 21:00
    cmd = f'''openclaw cron add \\
  --name "weekly-report" \\
  --at "0 21 * * 0" \\
  --session isolated \\
  --deliver \\
  --channel {channel} \\
  --to "{user_id}" \\
  --post-to-main none \\
  --message "cd {SKILL_DIR} && python scripts/generate_report.py --type weekly --save && \\
  请使用 message 工具发送：📊 本周阅读报告已生成，正在发送到飞书云文档和邮箱..."'''
    commands.append(("weekly-report", cmd))
    
    # 4. 月报生成 - 每月最后一日 21:00
    cmd = f'''openclaw cron add \\
  --name "monthly-report" \\
  --at "0 21 28-31 * *" \\
  --session isolated \\
  --deliver \\
  --channel {channel} \\
  --to "{user_id}" \\
  --post-to-main none \\
  --message "cd {SKILL_DIR} && python scripts/generate_report.py --type monthly --save && \\
  请使用 message 工具发送：📊 本月阅读报告已生成，正在发送到飞书云文档和邮箱..."'''
    commands.append(("monthly-report", cmd))
    
    return commands


def setup_cron(user_id, channel="feishu", dry_run=False):
    """设置所有定时任务"""
    
    print(f"\n🕐 正在设置定时任务...")
    print(f"   用户ID: {user_id}")
    print(f"   渠道: {channel}\n")
    
    commands = get_cron_commands(user_id, channel)
    
    if dry_run:
        print("📋 预览模式（不实际创建任务）：\n")
        for name, cmd in commands:
            print(f"--- {name} ---")
            print(cmd)
            print()
        return
    
    # 保存配置
    config = {
        "user_id": user_id,
        "channel": channel,
        "tasks": [name for name, _ in commands]
    }
    
    CRON_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CRON_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ 配置已保存: {CRON_CONFIG_FILE}\n")
    
    # 输出手动设置指南
    print("=" * 60)
    print("请手动执行以下命令设置定时任务：")
    print("=" * 60)
    print()
    
    for name, cmd in commands:
        print(f"# {name}")
        print(cmd)
        print()
    
    print("=" * 60)
    print("💡 提示：也可以使用 `openclaw cron` 命令管理任务")
    print("   查看任务: openclaw cron list")
    print("   删除任务: openclaw cron remove <name>")


def generate_cron_script(user_id, channel="feishu"):
    """生成可执行的cron设置脚本"""
    
    script_path = SKILL_DIR / "scripts" / "setup_cron_auto.sh"
    
    script_content = f'''#!/bin/bash
# 自动生成的定时任务设置脚本
# 生成时间: {__import__('datetime').datetime.now().isoformat()}

USER_ID="{user_id}"
CHANNEL="{channel}"
SKILL_DIR="{SKILL_DIR}"

echo "🕐 正在设置 Paper Research Assistant 定时任务..."

# 收集论文任务
openclaw cron add \\
  --name "paper-fetch-all" \\
  --at "0 9 * * 1" \\
  --session isolated \\
  --deliver \\
  --channel $CHANNEL \\
  --to "$USER_ID" \\
  --post-to-main none \\
  --message "请执行: cd $SKILL_DIR && python scripts/fetch_papers.py --discipline all --max-results 10"

# 知识卡片推送
for slot in "08:30" "12:00" "16:00" "20:00"; do
    cron_time=$(echo $slot | sed 's/\\(\\d\\+\\):\\(\\d\\+\\)/\\2 \\1/')
    name="flashcard-push-$(echo $slot | tr -d ':')"
    
    openclaw cron add \\
        --name "$name" \\
        --at "$cron_time * * *" \\
        --session isolated \\
        --deliver \\
        --channel $CHANNEL \\
        --to "$USER_ID" \\
        --post-to-main none \\
        --message "cd $SKILL_DIR && python scripts/spaced_repetition.py --slot $slot"
done

# 周报
cd $SKILL_DIR && python scripts/generate_report.py --type weekly --save
openclaw cron add \\
  --name "weekly-report" \\
  --at "0 21 * * 0" \\
  --session isolated \\
  --deliver \\
  --channel $CHANNEL \\
  --to "$USER_ID" \\
  --post-to-main none \\
  --message "cd $SKILL_DIR && python scripts/generate_report.py --type weekly --save && 请使用 message 工具发送周报"

# 月报
openclaw cron add \\
  --name "monthly-report" \\
  --at "0 21 28-31 * *" \\
  --session isolated \\
  --deliver \\
  --channel $CHANNEL \\
  --to "$USER_ID" \\
  --post-to-main none \\
  --message "cd $SKILL_DIR && python scripts/generate_report.py --type monthly --save && 请使用 message 工具发送月报"

echo "✅ 定时任务设置完成！"
echo "查看任务: openclaw cron list"
'''
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    script_path.chmod(0o755)
    
    print(f"✅ 已生成脚本: {script_path}")
    print(f"执行命令: bash {script_path}")
    
    return script_path


def main():
    parser = argparse.ArgumentParser(description="设置定时任务")
    parser.add_argument("--user-id", required=True, help="用户ID (飞书用户ID)")
    parser.add_argument("--channel", default="feishu", help="消息渠道")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("--generate-script", action="store_true", help="生成可执行脚本")
    
    args = parser.parse_args()
    
    if args.generate_script:
        generate_cron_script(args.user_id, args.channel)
    else:
        setup_cron(args.user_id, args.channel, args.dry_run)


if __name__ == "__main__":
    main()
