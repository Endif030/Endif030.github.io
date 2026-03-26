#!/usr/bin/env python3
"""
知识卡片创建脚本 - 创建艾宾浩斯遗忘曲线知识卡片
更新：添加"已读"状态检查，只有用户明确读完论文后才加入复习库
"""

import argparse
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
DATA_DIR = WORKSPACE / "data"
FLASHCARDS_FILE = DATA_DIR / "flashcards.json"
SCHEDULE_FILE = DATA_DIR / "review_schedule.json"
READING_STATUS_FILE = DATA_DIR / "reading_status.json"  # 新增：阅读状态跟踪

# 艾宾浩斯复习间隔（天）
REVIEW_INTERVALS = [1, 2, 4, 7, 15, 30]


def ensure_dirs():
    """确保目录结构存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_reading_status():
    """加载阅读状态"""
    if READING_STATUS_FILE.exists():
        with open(READING_STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"papers": {}}  # {paper_id: {"status": "unread|reading|completed", "completed_at": timestamp}}


def save_reading_status(status):
    """保存阅读状态"""
    with open(READING_STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def mark_paper_completed(paper_id):
    """标记论文为已读完"""
    status = load_reading_status()
    status["papers"][paper_id] = {
        "status": "completed",
        "completed_at": datetime.now().isoformat()
    }
    save_reading_status(status)
    print(f"✅ 已标记论文为已读完: {paper_id}")
    print("📚 该论文的知识卡片已加入每日复习库！")


def load_flashcards_db():
    """加载知识卡片数据库"""
    if FLASHCARDS_FILE.exists():
        with open(FLASHCARDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"cards": [], "total_count": 0, "by_discipline": {}}


def save_flashcards_db(db):
    """保存知识卡片数据库"""
    with open(FLASHCARDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def create_flashcard(paper_id, question, answer, discipline="", context="", tags=None, difficulty=3, require_read=True):
    """创建新的知识卡片
    
    Args:
        require_read: 是否要求论文已读完才加入复习库（默认True）
    """
    # 检查论文是否已读完
    if require_read:
        status = load_reading_status()
        paper_status = status["papers"].get(paper_id, {})
        if paper_status.get("status") != "completed":
            print(f"⚠️  论文 {paper_id} 尚未标记为已读完！")
            print("💡 请先阅读论文，然后告诉我'已读完'，知识卡片才会加入复习库。")
            print("📝 卡片已保存为草稿状态，读完后自动激活。")
            is_active = False
        else:
            is_active = True
    else:
        is_active = True
    
    card_id = f"fc_{uuid.uuid4().hex[:8]}"
    now = datetime.now()
    
    # 生成复习计划（只有激活的卡片才有复习计划）
    if is_active:
        reviews = []
        for i, interval in enumerate(REVIEW_INTERVALS):
            review_date = (now + timedelta(days=interval)).strftime("%Y-%m-%d")
            reviews.append({
                "stage": i + 1,
                "date": review_date,
                "status": "pending" if i > 0 else "created",
                "ease": None,
                "completed_at": None
            })
        next_review = reviews[0]["date"]
    else:
        reviews = []
        next_review = None
    
    card = {
        "id": card_id,
        "paper_id": paper_id,
        "discipline": discipline,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        
        "question": question,
        "answer": answer,
        "context": context,
        
        "tags": tags or [],
        "difficulty": difficulty,
        
        "review_schedule": {
            "created": now.strftime("%Y-%m-%d"),
            "intervals": REVIEW_INTERVALS,
            "reviews": reviews,
            "current_stage": 0,
            "next_review": next_review
        },
        
        "mastery_level": 0,
        "status": "active" if is_active else "draft",  # draft = 草稿，未激活
        "total_reviews": 0,
        "avg_ease": 0,
        "require_read": require_read
    }
    
    return card


def add_flashcard(paper_id, question, answer, discipline="", context="", tags=None, difficulty=3, require_read=True):
    """添加知识卡片到数据库"""
    ensure_dirs()
    
    db = load_flashcards_db()
    
    card = create_flashcard(paper_id, question, answer, discipline, context, tags, difficulty, require_read)
    db["cards"].append(card)
    db["total_count"] = len(db["cards"])
    
    # 更新学科统计
    if discipline:
        if discipline not in db["by_discipline"]:
            db["by_discipline"][discipline] = 0
        db["by_discipline"][discipline] += 1
    
    save_flashcards_db(db)
    
    if card["status"] == "active":
        print(f"✅ 已创建卡片: {card['id']}")
        print(f"   下次复习: {card['review_schedule']['next_review']}")
    else:
        print(f"✅ 已创建卡片草稿: {card['id']}")
        print(f"   状态: 待激活（读完论文后自动加入复习库）")
    
    return card


def get_due_cards(date=None, include_draft=False):
    """获取指定日期到期的卡片"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    db = load_flashcards_db()
    due = []
    
    for card in db["cards"]:
        if card["status"] == "draft" and not include_draft:
            continue
        
        next_review = card["review_schedule"]["next_review"]
        if next_review and next_review <= date:
            due.append(card)
    
    return due


def list_cards(status=None, discipline=None, limit=20):
    """列出知识卡片"""
    db = load_flashcards_db()
    cards = db["cards"]
    
    if status:
        cards = [c for c in cards if c["status"] == status]
    if discipline:
        cards = [c for c in cards if c["discipline"] == discipline]
    
    cards = cards[:limit]
    
    print(f"\n📚 知识卡片列表 (共{len(cards)}张)\n")
    print(f"{'ID':<12} {'状态':<8} {'学科':<10} {'阶段':<6} {'掌握度':<8} {'问题':<40}")
    print("-" * 90)
    
    for card in cards:
        q = card["question"][:37] + "..." if len(card["question"]) > 40 else card["question"]
        status_zh = "✅活跃" if card["status"] == "active" else "📝草稿"
        print(f"{card['id']:<12} {status_zh:<8} {card['discipline']:<10} {card['review_schedule']['current_stage']:<6} {card['mastery_level']:<8} {q:<40}")
    
    return cards


def main():
    parser = argparse.ArgumentParser(description="知识卡片管理")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 创建卡片
    create_parser = subparsers.add_parser("create", help="创建新卡片")
    create_parser.add_argument("--paper-id", required=True, help="关联论文ID")
    create_parser.add_argument("--question", required=True, help="问题")
    create_parser.add_argument("--answer", required=True, help="答案")
    create_parser.add_argument("--discipline", help="学科")
    create_parser.add_argument("--context", help="上下文")
    create_parser.add_argument("--tags", help="标签，逗号分隔")
    create_parser.add_argument("--difficulty", type=int, default=3, help="难度1-5")
    create_parser.add_argument("--no-require-read", action="store_true", help="不要求论文已读完")
    
    # 标记已读完
    complete_parser = subparsers.add_parser("complete", help="标记论文已读完")
    complete_parser.add_argument("--paper-id", required=True, help="论文ID")
    
    # 列出卡片
    list_parser = subparsers.add_parser("list", help="列出卡片")
    list_parser.add_argument("--status", choices=["active", "draft", "mastered", "archived"])
    list_parser.add_argument("--discipline", help="学科过滤")
    list_parser.add_argument("--limit", type=int, default=20)
    
    # 查看阅读状态
    status_parser = subparsers.add_parser("status", help="查看阅读状态")
    status_parser.add_argument("--paper-id", help="指定论文ID")
    
    args = parser.parse_args()
    
    if args.command == "create":
        tags = args.tags.split(",") if args.tags else []
        require_read = not args.no_require_read
        card = add_flashcard(
            paper_id=args.paper_id,
            question=args.question,
            answer=args.answer,
            discipline=args.discipline,
            context=args.context,
            tags=tags,
            difficulty=args.difficulty,
            require_read=require_read
        )
    
    elif args.command == "complete":
        mark_paper_completed(args.paper_id)
    
    elif args.command == "list":
        list_cards(args.status, args.discipline, args.limit)
    
    elif args.command == "status":
        status = load_reading_status()
        if args.paper_id:
            paper_status = status["papers"].get(args.paper_id)
            if paper_status:
                print(f"\n📄 论文 {args.paper_id}:")
                print(f"   状态: {paper_status['status']}")
                print(f"   完成时间: {paper_status.get('completed_at', 'N/A')}")
            else:
                print(f"\n📄 论文 {args.paper_id}: 未开始阅读")
        else:
            print("\n📚 阅读状态总览:")
            for pid, info in status["papers"].items():
                icon = "✅" if info["status"] == "completed" else "📖"
                print(f"   {icon} {pid}: {info['status']}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
