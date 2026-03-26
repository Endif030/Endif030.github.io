#!/usr/bin/env python3
"""
复习提醒推送脚本 - 艾宾浩斯遗忘曲线知识卡片推送
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
DATA_DIR = WORKSPACE / "data"
FLASHCARDS_FILE = DATA_DIR / "flashcards.json"

# 推送时段
PUSH_SLOTS = ["08:30", "12:00", "16:00", "20:00"]


def load_flashcards_db():
    """加载知识卡片数据库"""
    if FLASHCARDS_FILE.exists():
        with open(FLASHCARDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"cards": [], "total_count": 0, "by_discipline": {}}


def get_cards_for_slot(time_slot, date=None):
    """获取指定时段应推送的卡片"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    db = load_flashcards_db()
    
    # 筛选今日待复习的活跃卡片
    due_cards = []
    for card in db["cards"]:
        if card["status"] != "active":
            continue
        
        next_review = card["review_schedule"]["next_review"]
        if next_review == date:
            due_cards.append(card)
    
    if not due_cards:
        return []
    
    # 按阶段排序（优先推送新卡片）
    due_cards.sort(key=lambda x: x["review_schedule"]["current_stage"])
    
    # 交错分配到4个时段
    slot_index = PUSH_SLOTS.index(time_slot) if time_slot in PUSH_SLOTS else 0
    cards_per_slot = max(3, len(due_cards) // 4)
    
    start_idx = slot_index * cards_per_slot
    end_idx = start_idx + cards_per_slot
    
    return due_cards[start_idx:end_idx]


def format_card_message(card, stage_info=True):
    """格式化卡片为消息格式"""
    disciplines = {
        "ai": "人工智能",
        "psychology": "心理学",
        "social-science": "社会科学",
        "anthropology": "人类学",
        "philosophy": "哲学",
        "game-studies": "游戏研究"
    }
    
    discipline_name = disciplines.get(card["discipline"], card["discipline"] or "未分类")
    stage = card["review_schedule"]["current_stage"]
    total_stages = len(card["review_schedule"]["intervals"])
    
    msg = f"""🧠 知识卡片复习 [{stage+1}/{total_stages}轮]

📄 来源：{discipline_name}

❓ 问题：
{card['question']}

💡 答案：
{card['answer']}
"""
    
    if card.get("context"):
        msg += f"\n📋 上下文：{card['context']}\n"
    
    if stage_info:
        msg += f"\n---\n📊 当前掌握度：{card['mastery_level']}%"
        msg += f"\n📝 回复格式：\n  已掌握：回复 `review {card['id']} 4` 或 `review {card['id']} 5`\n  需复习：回复 `review {card['id']} 1` 或 `review {card['id']} 2`\n"
    
    return msg


def format_batch_message(cards, time_slot):
    """格式化批量推送消息"""
    if not cards:
        return None
    
    msg = f"⏰ {time_slot} 知识卡片推送\n"
    msg += f"今日共 {len(cards)} 张卡片待复习\n"
    msg += "=" * 40 + "\n\n"
    
    for i, card in enumerate(cards, 1):
        msg += f"--- 卡片 {i}/{len(cards)} ---\n"
        msg += format_card_message(card, stage_info=False)
        msg += f"\n💾 卡片ID: `{card['id']}`\n\n"
    
    msg += "=" * 40 + "\n"
    msg += "📊 记录复习：回复 `review [卡片ID] [1-5]`\n"
    msg += "（1=几乎忘记，5=完全掌握）"
    
    return msg


def push_cards(time_slot, user_id=None, channel="feishu", dry_run=False):
    """推送指定时段的卡片"""
    cards = get_cards_for_slot(time_slot)
    
    if not cards:
        print(f"⏭️  {time_slot} 时段无待复习卡片")
        return 0
    
    message = format_batch_message(cards, time_slot)
    
    if dry_run:
        print(f"\n{'='*50}")
        print(f"📤 推送预览 ({time_slot})")
        print(f"{'='*50}")
        print(message)
        return len(cards)
    
    # 实际推送 - 通过 message 工具发送
    # 这里输出格式化后的消息，由上层调用 message 工具
    print(f"📤 准备推送 {len(cards)} 张卡片 ({time_slot})")
    print(message)
    
    return len(cards)


def get_stats():
    """获取知识卡片统计"""
    db = load_flashcards_db()
    
    stats = {
        "total": len(db["cards"]),
        "active": len([c for c in db["cards"] if c["status"] == "active"]),
        "mastered": len([c for c in db["cards"] if c["status"] == "mastered"]),
        "by_discipline": {}
    }
    
    for card in db["cards"]:
        disc = card.get("discipline", "uncategorized")
        if disc not in stats["by_discipline"]:
            stats["by_discipline"][disc] = {"total": 0, "active": 0, "mastered": 0}
        stats["by_discipline"][disc]["total"] += 1
        if card["status"] == "active":
            stats["by_discipline"][disc]["active"] += 1
        elif card["status"] == "mastered":
            stats["by_discipline"][disc]["mastered"] += 1
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="艾宾浩斯知识卡片推送")
    parser.add_argument("--slot", choices=PUSH_SLOTS, help="推送时段")
    parser.add_argument("--user-id", help="用户ID")
    parser.add_argument("--channel", default="feishu", help="推送渠道")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    
    args = parser.parse_args()
    
    if args.stats:
        stats = get_stats()
        print("\n📊 知识卡片统计\n")
        print(f"总计: {stats['total']} 张")
        print(f"  - 活跃: {stats['active']} 张")
        print(f"  - 已掌握: {stats['mastered']} 张")
        print("\n按学科分布:")
        for disc, s in stats["by_discipline"].items():
            print(f"  {disc}: {s['total']} (活跃{s['active']}, 已掌握{s['mastered']})")
        return
    
    if args.slot:
        push_cards(args.slot, args.user_id, args.channel, args.dry_run)
    else:
        # 推送所有时段
        for slot in PUSH_SLOTS:
            push_cards(slot, args.user_id, args.channel, args.dry_run)


if __name__ == "__main__":
    main()
