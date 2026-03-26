#!/usr/bin/env python3
"""
注释稿生成脚本 - 生成结构化中文注释稿
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
DATA_DIR = WORKSPACE / "data"
PAPERS_FILE = DATA_DIR / "papers.json"
ANNOTATIONS_DIR = WORKSPACE / "annotations"


def load_papers_db():
    """加载论文数据库"""
    if PAPERS_FILE.exists():
        with open(PAPERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"papers": [], "last_updated": None}


def generate_annotation(paper, template_path=None):
    """生成论文注释稿"""
    
    # 模板路径
    if template_path is None:
        template_path = Path(__file__).parent.parent / "assets" / "annotation_template.md"
    
    # 读取模板
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        template = get_default_template()
    
    # 学科映射
    disciplines = {
        "ai": "人工智能",
        "psychology": "心理学",
        "social-science": "社会科学",
        "anthropology": "人类学",
        "philosophy": "哲学",
        "game-studies": "游戏研究"
    }
    
    # 填充模板
    annotation = template.format(
        title=paper.get("title", "未命名"),
        discipline=disciplines.get(paper.get("discipline", ""), "未分类"),
        authors=", ".join(paper.get("authors", ["未知"])),
        year=paper.get("year", paper.get("published", "")[:4] if paper.get("published") else "未知"),
        source=paper.get("source", "未知"),
        abstract=paper.get("summary", "无摘要"),
        url=paper.get("url", paper.get("id", "")),
        pdf_path=paper.get("local_pdf", "未下载"),
        doi=paper.get("doi", "无"),
        citation_count=paper.get("citation_count", "未知"),
        fetched_at=paper.get("fetched_at", datetime.now().isoformat()),
        paper_id=paper.get("id", "").replace(":", "_").replace("/", "_")
    )
    
    return annotation


def get_default_template():
    """获取默认模板"""
    return """# 📄 {title}

## 基础信息

| 项目 | 内容 |
|------|------|
| **学科** | {discipline} |
| **作者** | {authors} |
| **年份** | {year} |
| **来源** | {source} |
| **引用数** | {citation_count} |
| **DOI** | {doi} |
| **原文链接** | {url} |
| **本地PDF** | {pdf_path} |

---

## 📝 摘要（原文）

{abstract}

---

## 🌐 摘要（中文翻译）

【待翻译】

---

## 🔍 研究背景

【在此记录研究的背景和动机】

- 
- 
- 

---

## 🧪 研究方法

【在此记录研究方法和实验设计】

- 方法：
- 数据：
- 实验设置：

---

## 💡 核心发现

【在此记录主要研究结论】

1. 
2. 
3. 

---

## 🎯 创新点

【在此记录论文的创新之处】

- 
- 

---

## 🤔 个人批注与思考

### 疑问点
【记录阅读过程中的疑问】

- 
- 

### Insight / 启发
【记录阅读后的思考和启发】

- 
- 

### 可关联的知识
【与其他学科或论文的关联】

- 
- 

---

## 🏷️ 标签

#论文 #{discipline} #{year} #待读 #待翻译

---

## 📚 知识卡片（从问题生成）

【在阅读过程中，将关键问题-答案对记录为知识卡片】

### 卡片 1
- **问题**：
- **答案**：
- **掌握度**：□ 生疏 □ 熟悉 □ 精通

---

*生成时间：{fetched_at}*
*论文ID：{paper_id}*
"""


def save_annotation(paper, overwrite=False):
    """保存注释稿"""
    discipline = paper.get("discipline", "uncategorized")
    annot_dir = ANNOTATIONS_DIR / discipline
    annot_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    safe_title = re.sub(r'[\\/:*?"<>|]', '', paper.get("title", "unknown"))[:50]
    if "arxiv_id" in paper:
        filename = f"arxiv_{paper['arxiv_id']}.md"
    else:
        filename = f"{safe_title}.md"
    
    annot_path = annot_dir / filename
    
    # 检查是否已存在
    if annot_path.exists() and not overwrite:
        print(f"   ⏭️  注释稿已存在: {annot_path.name}")
        return str(annot_path)
    
    # 生成并保存
    annotation = generate_annotation(paper)
    
    with open(annot_path, 'w', encoding='utf-8') as f:
        f.write(annotation)
    
    print(f"   ✅ 已生成注释稿: {annot_path.name}")
    
    # 更新数据库
    paper["annotation_path"] = str(annot_path)
    
    return str(annot_path)


def main():
    parser = argparse.ArgumentParser(description="生成论文注释稿")
    parser.add_argument("--paper-id", help="论文ID")
    parser.add_argument("--discipline", help="学科ID，生成该学科所有注释稿")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已存在的文件")
    parser.add_argument("--all", action="store_true", help="生成所有未生成的注释稿")
    
    args = parser.parse_args()
    
    ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)
    db = load_papers_db()
    
    if args.paper_id:
        paper = next((p for p in db["papers"] if p["id"] == args.paper_id), None)
        if paper:
            save_annotation(paper, args.overwrite)
            save_papers_db(db)
        else:
            print(f"❌ 未找到论文: {args.paper_id}")
    
    elif args.discipline:
        papers = [p for p in db["papers"] if p.get("discipline") == args.discipline]
        print(f"📝 生成 {len(papers)} 篇 {args.discipline} 注释稿...")
        for paper in papers:
            save_annotation(paper, args.overwrite)
        save_papers_db(db)
    
    elif args.all:
        print(f"📝 生成所有注释稿...")
        for paper in db["papers"]:
            save_annotation(paper, args.overwrite)
        save_papers_db(db)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
