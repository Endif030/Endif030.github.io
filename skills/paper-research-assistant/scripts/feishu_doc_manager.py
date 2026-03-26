#!/usr/bin/env python3
"""
飞书文档管理工具 - 解决 update_doc 失效问题
策略: 每次创建新文档，使用版本化命名
"""

import argparse
import re
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
ANNOTATIONS_DIR = WORKSPACE / "annotations"


def generate_doc_title(paper_title, paper_id=None):
    """生成规范的飞书文档标题
    
    格式: 📄 论文注释 - {简称} (v{YYYYMMDD})
    """
    # 提取论文简称（取前30个字符）
    short_title = paper_title[:30] + "..." if len(paper_title) > 30 else paper_title
    
    # 清理特殊字符
    short_title = re.sub(r'[\\/*?"<>|]', '', short_title)
    
    # 添加版本日期
    today = datetime.now().strftime("%Y%m%d")
    
    return f"📄 {short_title} (v{today})"


def generate_reading_week_title(week_num, date=None):
    """生成阅读周导航文档标题
    
    格式: 📚 AI阅读周 - Week {N} (v{YYYYMMDD})
    """
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    return f"📚 AI阅读周 - Week {week_num} (v{date})"


def generate_annotation_content(paper, annotation_md):
    """生成完整的飞书文档内容"""
    
    # 封面信息
    content = f"""# {paper.get('title', '未命名')}

## 封面信息

**论文标题**: {paper.get('title', '未命名')}

**arXiv ID**: {paper.get('arxiv_id', 'N/A')}

**领域**: {paper.get('discipline', '未分类')}

**作者**: {', '.join(paper.get('authors', ['未知']))}

**发布时间**: {paper.get('published', '未知')}

**原文链接**: {paper.get('url', paper.get('pdf_url', 'N/A'))}

---

"""
    
    # 添加注释稿内容
    content += annotation_md
    
    # 添加页脚
    content += f"""

---

*文档生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

*论文阅读系统 v2.0*
"""
    
    return content


def generate_reading_week_content(papers, week_num):
    """生成阅读周导航文档内容"""
    
    content = f"""# 📚 AI阅读周 - Week {week_num}

*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## 本周阅读清单

"""
    
    for i, paper in enumerate(papers, 1):
        arxiv_id = paper.get('arxiv_id', 'N/A')
        has_annotation = paper.get('annotation_path') is not None
        
        content += f"""### #{i} {paper.get('title', '未命名')[:50]}

**arXiv ID**: {arxiv_id}

**领域**: {paper.get('discipline', 'AI')}

**核心内容**:
- 问题: {paper.get('summary', '无摘要')[:100]}...

📄 [arXiv原文](https://arxiv.org/abs/{arxiv_id})
📥 [PDF下载](https://arxiv.org/pdf/{arxiv_id}.pdf)
📝 注释稿: {'✅ 已完成' if has_annotation else '⏳ 待生成'}

---

"""
    
    content += """## 阅读进度追踪

| 序号 | 论文 | 阅读状态 | 知识卡片 |
|------|------|----------|----------|
"""
    
    for i, paper in enumerate(papers, 1):
        content += f"| #{i} | {paper.get('title', '未命名')[:20]}... | ⏳ 待读 | ⏳ 待创建 |\n"
    
    content += """
---

💡 **使用说明**:
1. 点击 arXiv原文 阅读论文
2. 阅读完成后告诉我"已读完#编号"
3. 我会自动生成知识卡片并更新状态
"""
    
    return content


def main():
    parser = argparse.ArgumentParser(description="飞书文档标题和内容生成器")
    parser.add_argument("--paper-title", help="论文标题")
    parser.add_argument("--paper-id", help="论文ID")
    parser.add_argument("--week-num", type=int, help="阅读周编号")
    parser.add_argument("--mode", choices=["annotation", "reading-week"], help="文档类型")
    
    args = parser.parse_args()
    
    if args.mode == "annotation" and args.paper_title:
        title = generate_doc_title(args.paper_title, args.paper_id)
        print(f"TITLE:{title}")
    elif args.mode == "reading-week" and args.week_num:
        title = generate_reading_week_title(args.week_num)
        print(f"TITLE:{title}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
