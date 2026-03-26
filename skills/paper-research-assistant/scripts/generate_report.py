#!/usr/bin/env python3
"""
报告生成脚本 - 生成周/月度阅读报告
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
DATA_DIR = WORKSPACE / "data"
REPORTS_DIR = WORKSPACE / "reports"
PAPERS_FILE = DATA_DIR / "papers.json"
FLASHCARDS_FILE = DATA_DIR / "flashcards.json"


def load_papers_db():
    """加载论文数据库"""
    if PAPERS_FILE.exists():
        with open(PAPERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"papers": [], "last_updated": None}


def load_flashcards_db():
    """加载知识卡片数据库"""
    if FLASHCARDS_FILE.exists():
        with open(FLASHCARDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"cards": [], "total_count": 0}


def generate_weekly_report(week_start=None):
    """生成周报"""
    if week_start is None:
        # 默认上周
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday() + 7)
    
    week_end = week_start + timedelta(days=6)
    week_start_str = week_start.strftime("%Y-%m-%d")
    week_end_str = week_end.strftime("%Y-%m-%d")
    
    papers_db = load_papers_db()
    flashcards_db = load_flashcards_db()
    
    # 筛选本周数据
    week_papers = []
    for p in papers_db["papers"]:
        fetched = p.get("fetched_at", "")
        if fetched and week_start_str <= fetched[:10] <= week_end_str:
            week_papers.append(p)
    
    week_cards = []
    for c in flashcards_db["cards"]:
        created = c.get("created_at", "")
        if created and week_start_str <= created[:10] <= week_end_str:
            week_cards.append(c)
    
    # 统计
    by_discipline = defaultdict(int)
    for p in week_papers:
        by_discipline[p.get("discipline", "unknown")] += 1
    
    # 生成报告
    report = f"""# 📊 论文阅读周报

**报告周期**: {week_start_str} ~ {week_end_str}
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📚 本周概览

| 指标 | 数量 |
|------|------|
| 新增论文 | {len(week_papers)} 篇 |
| 新增知识卡片 | {len(week_cards)} 张 |
| 活跃知识卡片 | {len([c for c in flashcards_db['cards'] if c['status'] == 'active'])} 张 |
| 已掌握知识 | {len([c for c in flashcards_db['cards'] if c['status'] == 'mastered'])} 张 |

---

## 📖 学科分布

| 学科 | 新增论文 | 占比 |
|------|----------|------|
"""
    
    disciplines = {
        "ai": "人工智能",
        "psychology": "心理学",
        "social-science": "社会科学",
        "anthropology": "人类学",
        "philosophy": "哲学",
        "game-studies": "游戏研究"
    }
    
    for disc, count in sorted(by_discipline.items(), key=lambda x: -x[1]):
        pct = count / len(week_papers) * 100 if week_papers else 0
        name = disciplines.get(disc, disc)
        report += f"| {name} | {count} | {pct:.1f}% |\n"
    
    report += f"""
---

## 📝 本周新增论文

"""
    
    for i, p in enumerate(week_papers[:10], 1):  # 最多显示10篇
        disc_name = disciplines.get(p.get("discipline"), "未分类")
        report += f"""### {i}. {p['title'][:60]}{'...' if len(p['title']) > 60 else ''}
- **学科**: {disc_name}
- **作者**: {', '.join(p.get('authors', ['未知'])[:3])}{'等' if len(p.get('authors', [])) > 3 else ''}
- **来源**: {p.get('source', '未知')}

"""
    
    report += f"""
---

## 🧠 本周知识卡片

共创建 {len(week_cards)} 张新卡片：

"""
    
    for i, c in enumerate(week_cards[:5], 1):
        q = c['question'][:50] + "..." if len(c['question']) > 50 else c['question']
        report += f"{i}. [{c['discipline'] or '未分类'}] {q}\n"
    
    report += f"""

---

## 💡 本周 Insight

【在此记录本周的主要收获和思考】

- 
- 
- 

---

## 📅 下周计划

- [ ] 阅读论文：___篇
- [ ] 创建知识卡片：___张
- [ ] 重点学科：___

---

*报告由 Paper Research Assistant 自动生成*
"""
    
    return report, week_start_str, week_end_str


def generate_monthly_report(year=None, month=None):
    """生成月报"""
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    
    month_start = datetime(year, month, 1)
    if month == 12:
        month_end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = datetime(year, month + 1, 1) - timedelta(days=1)
    
    month_start_str = month_start.strftime("%Y-%m-%d")
    month_end_str = month_end.strftime("%Y-%m-%d")
    
    papers_db = load_papers_db()
    flashcards_db = load_flashcards_db()
    
    # 筛选本月数据
    month_papers = []
    for p in papers_db["papers"]:
        fetched = p.get("fetched_at", "")
        if fetched and month_start_str <= fetched[:10] <= month_end_str:
            month_papers.append(p)
    
    month_cards = []
    for c in flashcards_db["cards"]:
        created = c.get("created_at", "")
        if created and month_start_str <= created[:10] <= month_end_str:
            month_cards.append(c)
    
    # 统计
    by_discipline = defaultdict(lambda: {"papers": 0, "cards": 0})
    for p in month_papers:
        by_discipline[p.get("discipline", "unknown")]["papers"] += 1
    for c in month_cards:
        by_discipline[c.get("discipline", "unknown")]["cards"] += 1
    
    # 总积累
    total_papers = len(papers_db["papers"])
    total_cards = len(flashcards_db["cards"])
    total_mastered = len([c for c in flashcards_db["cards"] if c["status"] == "mastered"])
    
    disciplines = {
        "ai": "人工智能",
        "psychology": "心理学",
        "social-science": "社会科学",
        "anthropology": "人类学",
        "philosophy": "哲学",
        "game-studies": "游戏研究"
    }
    
    report = f"""# 📊 论文阅读月报

**报告月份**: {year}年{month}月
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📈 本月概览

### 新增数据
| 指标 | 本月新增 | 累计总量 |
|------|----------|----------|
| 论文 | {len(month_papers)} 篇 | {total_papers} 篇 |
| 知识卡片 | {len(month_cards)} 张 | {total_cards} 张 |

### 知识掌握
| 指标 | 数量 |
|------|------|
| 已掌握知识 | {total_mastered} 张 |
| 掌握率 | {total_mastered/total_cards*100:.1f}% |\n
---

## 📊 学科分析

| 学科 | 本月论文 | 本月卡片 | 论文累计 | 卡片累计 |
|------|----------|----------|----------|----------|
"""
    
    for disc in disciplines.keys():
        month_p = by_discipline[disc]["papers"]
        month_c = by_discipline[disc]["cards"]
        total_p = len([p for p in papers_db["papers"] if p.get("discipline") == disc])
        total_c = len([c for c in flashcards_db["cards"] if c.get("discipline") == disc])
        report += f"| {disciplines[disc]} | {month_p} | {month_c} | {total_p} | {total_c} |\n"
    
    report += f"""
---

## 📚 本月重点论文

【在此列出本月最值得关注的论文】

"""
    
    # 按引用数排序取Top
    top_papers = sorted(month_papers, key=lambda x: x.get("citation_count", 0) or 0, reverse=True)[:5]
    for i, p in enumerate(top_papers, 1):
        disc_name = disciplines.get(p.get("discipline"), "未分类")
        citations = p.get("citation_count", "未知")
        report += f"""### {i}. {p['title'][:70]}{'...' if len(p['title']) > 70 else ''}
- **学科**: {disc_name}
- **引用数**: {citations}
- **作者**: {', '.join(p.get('authors', ['未知'])[:3])}{'等' if len(p.get('authors', [])) > 3 else ''}

"""
    
    report += f"""
---

## 🧠 知识增长

### 本月新增知识卡片分布
"""
    
    for disc, counts in sorted(by_discipline.items(), key=lambda x: -x[1]["cards"]):
        if counts["cards"] > 0:
            name = disciplines.get(disc, disc)
            report += f"- {name}: {counts['cards']} 张\n"
    
    report += f"""
### 掌握度趋势
【记录本月知识掌握度的变化趋势】

---

## 💡 本月 Insight 汇总

### 跨学科思考
【在此记录本月产生的跨学科洞见】

### 研究趋势观察
【观察本月各学科的研究热点和趋势】

---

## 🎯 下月目标

- [ ] 论文阅读目标：___篇
- [ ] 知识卡片目标：___张
- [ ] 重点掌握领域：___

---

*报告由 Paper Research Assistant 自动生成*
"""
    
    return report, year, month


def save_report(report_content, report_type, filename):
    """保存报告"""
    if report_type == "weekly":
        report_dir = REPORTS_DIR / "weekly"
    else:
        report_dir = REPORTS_DIR / "monthly"
    
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"{filename}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_path


def main():
    parser = argparse.ArgumentParser(description="生成阅读报告")
    parser.add_argument("--type", choices=["weekly", "monthly"], required=True, help="报告类型")
    parser.add_argument("--week-start", help="周报起始日期 (YYYY-MM-DD)")
    parser.add_argument("--year", type=int, help="月报年份")
    parser.add_argument("--month", type=int, help="月报月份")
    parser.add_argument("--save", action="store_true", help="保存到文件")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    if args.type == "weekly":
        week_start = None
        if args.week_start:
            week_start = datetime.strptime(args.week_start, "%Y-%m-%d")
        
        report, start, end = generate_weekly_report(week_start)
        
        if args.save:
            filename = f"weekly_{start}_{end}"
            path = save_report(report, "weekly", filename)
            print(f"✅ 周报已保存: {path}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
        
        print(report)
    
    elif args.type == "monthly":
        report, year, month = generate_monthly_report(args.year, args.month)
        
        if args.save:
            filename = f"monthly_{year}_{month:02d}"
            path = save_report(report, "monthly", filename)
            print(f"✅ 月报已保存: {path}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
        
        print(report)


if __name__ == "__main__":
    main()
