#!/usr/bin/env python3
"""
智能知识卡片生成器 - 从注释稿自动提取Q&A对
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
DATA_DIR = WORKSPACE / "data"
ANNOTATIONS_DIR = WORKSPACE / "annotations"
FLASHCARDS_FILE = DATA_DIR / "flashcards.json"


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


def generate_card_id():
    """生成唯一卡片ID"""
    import uuid
    return f"fc_{uuid.uuid4().hex[:8]}"


def create_flashcard(paper_id, question, answer, discipline, context=None, difficulty=3):
    """创建知识卡片"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    card = {
        "id": generate_card_id(),
        "paper_id": paper_id,
        "discipline": discipline,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "context": context,
        "tags": [],
        "difficulty": difficulty,
        "review_schedule": {
            "created": today,
            "intervals": [1, 2, 4, 7, 15, 30],  # 艾宾浩斯遗忘曲线
            "reviews": [
                {"stage": 1, "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "status": "pending", "ease": None, "completed_at": None},
                {"stage": 2, "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), "status": "pending", "ease": None, "completed_at": None},
                {"stage": 3, "date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"), "status": "pending", "ease": None, "completed_at": None},
                {"stage": 4, "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), "status": "pending", "ease": None, "completed_at": None},
                {"stage": 5, "date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"), "status": "pending", "ease": None, "completed_at": None},
                {"stage": 6, "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"), "status": "pending", "ease": None, "completed_at": None},
            ],
            "current_stage": 0,
            "next_review": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        },
        "mastery_level": 0,
        "status": "active",
        "total_reviews": 0,
        "avg_ease": 0,
        "require_read": True
    }
    
    return card


def extract_qa_from_annotation(annotation_md):
    """从注释稿中提取Q&A对（基于规则）
    
    提取策略:
    1. 提取【注释解释】中的关键概念定义
    2. 提取论文的核心问题和方法
    3. 提取重要的类比和跨学科关联
    """
    qa_pairs = []
    
    # 提取术语定义（格式：**术语**：定义）
    term_pattern = r'\*\*([^*]+?)\*\*[：:]([^\n]+)'
    terms = re.findall(term_pattern, annotation_md)
    
    for term, definition in terms[:3]:  # 最多取3个术语
        question = f"什么是{term}？"
        answer = definition.strip()
        if len(answer) > 20:  # 过滤太短的定义
            qa_pairs.append({
                "question": question,
                "answer": answer,
                "type": "term",
                "difficulty": 3
            })
    
    # 提取摘要中的核心问题（假设摘要有"问题"或"挑战"等关键词）
    # 这里简化处理，实际可以用LLM更好地提取
    
    return qa_pairs


def generate_auto_flashcards(paper_id, discipline, annotation_path=None):
    """自动生成知识卡片
    
    如果提供了注释稿路径，从中提取；否则基于论文元数据生成基础卡片
    """
    db = load_flashcards_db()
    
    # 检查是否已存在该论文的卡片
    existing = [c for c in db["cards"] if c["paper_id"] == paper_id]
    if existing:
        print(f"⚠️  论文 {paper_id} 已有 {len(existing)} 张知识卡片，跳过自动生成")
        return []
    
    new_cards = []
    
    if annotation_path and Path(annotation_path).exists():
        # 从注释稿提取
        with open(annotation_path, 'r', encoding='utf-8') as f:
            annotation_md = f.read()
        
        qa_pairs = extract_qa_from_annotation(annotation_md)
        
        for qa in qa_pairs[:5]:  # 最多生成5张
            card = create_flashcard(
                paper_id=paper_id,
                question=qa["question"],
                answer=qa["answer"],
                discipline=discipline,
                difficulty=qa.get("difficulty", 3)
            )
            new_cards.append(card)
    
    if not new_cards:
        # 如果没有提取到，创建一张基础卡片提示用户
        card = create_flashcard(
            paper_id=paper_id,
            question="这篇论文的核心贡献是什么？",
            answer="【请手动补充】阅读论文后，总结1-2句话描述核心贡献",
            discipline=discipline,
            difficulty=3
        )
        new_cards.append(card)
    
    # 添加到数据库
    db["cards"].extend(new_cards)
    db["total_count"] = len(db["cards"])
    
    # 更新学科统计
    for card in new_cards:
        disc = card["discipline"]
        if disc not in db.get("by_discipline", {}):
            db["by_discipline"][disc] = 0
        db["by_discipline"][disc] += 1
    
    save_flashcards_db(db)
    
    return new_cards


def main():
    parser = argparse.ArgumentParser(description="智能知识卡片生成器")
    parser.add_argument("--paper-id", required=True, help="论文ID")
    parser.add_argument("--discipline", default="ai", help="学科")
    parser.add_argument("--annotation", help="注释稿路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print(f"🔍 预览模式: 将为论文 {args.paper_id} 生成知识卡片")
        if args.annotation:
            print(f"   从注释稿提取: {args.annotation}")
        return
    
    cards = generate_auto_flashcards(args.paper_id, args.discipline, args.annotation)
    
    print(f"✅ 已生成 {len(cards)} 张知识卡片")
    for card in cards:
        print(f"   - {card['question'][:40]}... (ID: {card['id']})")


if __name__ == "__main__":
    from datetime import timedelta
    main()
