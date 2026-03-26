#!/usr/bin/env python3
"""
AI阅读周 - 半自动化流程脚本
每周一执行：收集论文 → 生成周文档 → 上传飞书 → 更新索引

使用方式:
  1. 手动执行: python weekly_reading_init.py
  2. 每步需要用户确认后再继续
  3. 输出结果供用户检查

作者: AI Assistant
日期: 2026-03-25
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

# 配置路径
SKILL_DIR = Path("/root/.openclaw/workspace/skills/paper-reading-week")
TEMPLATE_PATH = SKILL_DIR / "template.md"
WEEKS_DIR = SKILL_DIR / "weeks"
INDEX_PATH = SKILL_DIR / "weeks_index.md"
PAPER_RESEARCH_DIR = Path("/root/.openclaw/workspace/paper-research")

def get_current_date():
    """获取当前日期"""
    return datetime.now().strftime("%Y-%m-%d")

def get_week_number():
    """获取当前是第几周"""
    # 基于2026-03-09为第1周计算
    start_date = datetime(2026, 3, 9)
    today = datetime.now()
    days_diff = (today - start_date).days
    week_num = (days_diff // 7) + 1
    return week_num

def load_template():
    """加载模板文件"""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def collect_papers_mock():
    """
    模拟论文收集过程
    实际使用时，这里应该调用 fetch_papers.py 获取真实论文
    """
    print("\n" + "="*60)
    print("📚 步骤1: 收集本周论文")
    print("="*60)
    print("\n【模拟数据 - 实际需要调用 fetch_papers.py 获取真实论文】\n")
    
    # 模拟7篇论文数据
    mock_papers = [
        {
            "short_title": "Paper1",
            "full_title": "Example Paper Title 1: A New Approach to AI",
            "arxiv_id": "2603.10001",
            "field": "大语言模型"
        },
        {
            "short_title": "Paper2",
            "full_title": "Example Paper Title 2: Robotics Vision",
            "arxiv_id": "2603.10002",
            "field": "机器人"
        },
        {
            "short_title": "Paper3",
            "full_title": "Example Paper Title 3: Medical AI System",
            "arxiv_id": "2603.10003",
            "field": "医疗AI"
        },
        {
            "short_title": "Paper4",
            "full_title": "Example Paper Title 4: Reinforcement Learning",
            "arxiv_id": "2603.10004",
            "field": "强化学习"
        },
        {
            "short_title": "Paper5",
            "full_title": "Example Paper Title 5: Computer Vision",
            "arxiv_id": "2603.10005",
            "field": "计算机视觉"
        },
        {
            "short_title": "Paper6",
            "full_title": "Example Paper Title 6: Natural Language Processing",
            "arxiv_id": "2603.10006",
            "field": "NLP"
        },
        {
            "short_title": "Paper7",
            "full_title": "Example Paper Title 7: Multimodal Learning",
            "arxiv_id": "2603.10007",
            "field": "多模态学习"
        }
    ]
    
    print("拟收集论文列表:")
    for i, paper in enumerate(mock_papers, 1):
        print(f"  #{i}: {paper['short_title']} ({paper['arxiv_id']}) - {paper['field']}")
    
    print("\n⚠️  注意: 以上为模拟数据")
    print("实际执行时需要:")
    print("  python /root/.openclaw/workspace/skills/paper-research-assistant/scripts/fetch_papers.py --discipline ai --max-results 7")
    
    return mock_papers

def fill_template(template, papers, date, week_num):
    """填充模板占位符"""
    content = template
    
    # 替换基本信息
    content = content.replace("{{DATE}}", date)
    content = content.replace("{{WEEK_NUMBER}}", f"第{week_num}")
    content = content.replace("{{THEME}}", "待确定")
    
    # 替换论文信息
    for i, paper in enumerate(papers, 1):
        content = content.replace(f"{{PAPER_{i}_TITLE}}", paper['short_title'])
        content = content.replace(f"{{PAPER_{i}_FULL_TITLE}}", paper['full_title'])
        content = content.replace(f"{{PAPER_{i}_ARXIV}}", paper['arxiv_id'])
        content = content.replace(f"{{PAPER_{i}_FIELD}}", paper['field'])
    
    return content

def generate_week_document(papers):
    """生成周文档"""
    print("\n" + "="*60)
    print("📝 步骤2: 生成周文档")
    print("="*60)
    
    date = get_current_date()
    week_num = get_week_number()
    
    print(f"\n日期: {date}")
    print(f"周次: 第{week_num}周")
    
    # 加载并填充模板
    template = load_template()
    content = fill_template(template, papers, date, week_num)
    
    # 保存到本地
    filename = f"AI阅读周_{date}.md"
    filepath = WEEKS_DIR / filename
    
    print(f"\n生成本地文件: {filepath}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 文件已保存")
    
    # 返回文件路径和内容
    return filepath, content

def print_upload_instruction(filepath, date, week_num):
    """打印上传飞书的操作指引"""
    print("\n" + "="*60)
    print("☁️  步骤3: 上传飞书")
    print("="*60)
    
    print(f"\n请执行以下操作:")
    print(f"\n1. 读取本地文件: {filepath}")
    print(f"2. 使用 feishu_create_doc 创建文档")
    print(f"3. 文档标题: 📚 AI阅读周 ({date}) - 第{week_num}周")
    print(f"\n命令示例:")
    print(f"  feishu_create_doc(")
    print(f"    title='📚 AI阅读周 ({date}) - 第{week_num}周',")
    print(f"    markdown=...文件内容...")
    print(f"  )")
    print(f"\n4. 记录返回的文档链接")

def print_update_index_instruction(date, week_num):
    """打印更新索引的操作指引"""
    print("\n" + "="*60)
    print("📋 步骤4: 更新索引")
    print("="*60)
    
    print(f"\n请更新文件: {INDEX_PATH}")
    print(f"\n添加以下行到表格:")
    print(f"  | 第{week_num}周 | {date} | [主题] | [飞书链接] | ⏳ 进行中 | 7篇待阅读 |")
    print(f"\n同时更新本地备份表格")

def main():
    """主流程"""
    print("="*60)
    print("🚀 AI阅读周 - 半自动化初始化流程")
    print("="*60)
    print(f"\n当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"本周是: 第{get_week_number()}周")
    
    # 步骤1: 收集论文
    papers = collect_papers_mock()
    
    print("\n" + "-"*60)
    response = input("\n是否继续生成周文档? (yes/no): ")
    if response.lower() != 'yes':
        print("\n⏹️  流程已暂停")
        return
    
    # 步骤2: 生成周文档
    filepath, content = generate_week_document(papers)
    
    print("\n" + "-"*60)
    response = input("\n是否继续上传飞书? (yes/no): ")
    if response.lower() != 'yes':
        print("\n⏹️  流程已暂停")
        print(f"本地文件已保存: {filepath}")
        return
    
    # 步骤3: 打印上传指引
    date = get_current_date()
    week_num = get_week_number()
    print_upload_instruction(filepath, date, week_num)
    
    print("\n" + "-"*60)
    response = input("\n飞书文档已创建后，是否继续更新索引? (yes/no): ")
    if response.lower() != 'yes':
        print("\n⏹️  流程已暂停")
        return
    
    # 步骤4: 打印更新索引指引
    print_update_index_instruction(date, week_num)
    
    print("\n" + "="*60)
    print("✅ 半自动化流程完成")
    print("="*60)
    print("\n后续步骤:")
    print("  1. 手动上传文档到飞书")
    print("  2. 更新 weeks_index.md 索引")
    print("  3. 开始阅读论文并生成注释稿")

if __name__ == "__main__":
    main()
