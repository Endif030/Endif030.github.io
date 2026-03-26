#!/usr/bin/env python3
"""
健康检查脚本 - 论文阅读助手
检查数据源连通性、文件完整性、定时任务配置等

用法:
    python scripts/health_check.py                    # 完整检查
    python scripts/health_check.py --check-sources    # 仅检查数据源
    python scripts/health_check.py --check-pdfs       # 检查PDF完整性
    python scripts/health_check.py --check-flashcards # 检查知识卡片
    python scripts/health_check.py --check-feishu     # 检查飞书权限
    python scripts/health_check.py --weekly-check     # 周收尾检查
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 配置
DATA_DIR = Path(__file__).parent.parent / "data"
PAPERS_DIR = Path(__file__).parent.parent / "papers"
LOG_DIR = Path("/tmp")

COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "reset": "\033[0m"
}

def print_status(message, status, details=""):
    """打印状态消息"""
    color = COLORS["green"] if status == "OK" else COLORS["red"] if status == "FAIL" else COLORS["yellow"]
    status_str = f"{color}[{status}]{COLORS['reset']}"
    print(f"{status_str} {message}")
    if details:
        print(f"    {details}")

def check_sources():
    """检查数据源连通性"""
    print("\n" + "="*50)
    print("📡 检查数据源连通性")
    print("="*50)
    
    import urllib.request
    
    checks = [
        ("arXiv API", "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=1"),
        ("Semantic Scholar API", "https://api.semanticscholar.org/graph/v1/paper/search?query=AI&fields=title&limit=1")
    ]
    
    all_ok = True
    for name, url in checks:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    print_status(f"{name}", "OK")
                else:
                    print_status(f"{name}", "FAIL", f"状态码: {response.status}")
                    all_ok = False
        except Exception as e:
            print_status(f"{name}", "FAIL", str(e))
            all_ok = False
    
    return all_ok

def check_files():
    """检查关键文件存在性"""
    print("\n" + "="*50)
    print("📁 检查关键文件")
    print("="*50)
    
    files = [
        ("论文数据库", DATA_DIR / "papers.json"),
        ("知识卡片", DATA_DIR / "flashcards.json"),
        ("学科配置", Path(__file__).parent.parent / "references" / "disciplines.md"),
    ]
    
    all_ok = True
    for name, filepath in files:
        if filepath.exists():
            size = filepath.stat().st_size
            print_status(f"{name}", "OK", f"{filepath} ({size} bytes)")
        else:
            print_status(f"{name}", "FAIL", f"找不到: {filepath}")
            all_ok = False
    
    return all_ok

def check_pdfs():
    """检查PDF文件完整性"""
    print("\n" + "="*50)
    print("📄 检查 PDF 完整性")
    print("="*50)
    
    if not PAPERS_DIR.exists():
        print_status("PDF 目录", "FAIL", f"找不到: {PAPERS_DIR}")
        return False
    
    disciplines = ["ai", "psychology", "social-science", "anthropology", "philosophy", "game-studies"]
    all_ok = True
    
    for discipline in disciplines:
        discipline_dir = PAPERS_DIR / discipline
        if not discipline_dir.exists():
            continue
        
        pdfs = list(discipline_dir.glob("*.pdf"))
        if pdfs:
            # 检查文件大小
            small_files = [p for p in pdfs if p.stat().st_size < 10000]  # < 10KB 可能损坏
            if small_files:
                print_status(f"{discipline}", "WARN", f"{len(pdfs)} 个PDF, {len(small_files)} 个可能损坏")
                all_ok = False
            else:
                print_status(f"{discipline}", "OK", f"{len(pdfs)} 个PDF文件正常")
        else:
            print_status(f"{discipline}", "OK", "无PDF文件")
    
    return all_ok

def check_flashcards():
    """检查知识卡片状态"""
    print("\n" + "="*50)
    print("🎴 检查知识卡片")
    print("="*50)
    
    flashcards_file = DATA_DIR / "flashcards.json"
    if not flashcards_file.exists():
        print_status("知识卡片文件", "FAIL", "找不到 flashcards.json")
        return False
    
    try:
        with open(flashcards_file, 'r') as f:
            data = json.load(f)
        
        cards = data.get('cards', [])
        active_cards = [c for c in cards if c.get('status') == 'active']
        
        today = datetime.now().strftime('%Y-%m-%d')
        due_today = [c for c in active_cards 
                     if c.get('review_schedule', {}).get('next_review') == today]
        
        print_status("卡片总数", "OK", f"{len(cards)} 张")
        print_status("活跃卡片", "OK", f"{len(active_cards)} 张")
        print_status("今日待复习", "OK", f"{len(due_today)} 张")
        
        return True
    except Exception as e:
        print_status("知识卡片解析", "FAIL", str(e))
        return False

def check_cron_jobs():
    """检查定时任务配置"""
    print("\n" + "="*50)
    print("⏰ 检查定时任务")
    print("="*50)
    
    import subprocess
    
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode != 0:
            print_status("crontab 读取", "FAIL", result.stderr)
            return False
        
        cron_content = result.stdout
        
        # 检查关键任务
        expected_jobs = [
            ("论文收集", "paper_fetch_weekly.sh"),
            ("知识卡片推送", "flashcard_push.sh"),
            ("月报生成", "monthly_report.sh")
        ]
        
        all_ok = True
        for name, script in expected_jobs:
            if script in cron_content:
                count = cron_content.count(script)
                print_status(name, "OK", f"{count} 个任务配置")
            else:
                print_status(name, "WARN", f"未找到 {script}")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print_status("定时任务检查", "FAIL", str(e))
        return False

def check_logs():
    """检查日志文件状态"""
    print("\n" + "="*50)
    print("📋 检查日志文件")
    print("="*50)
    
    log_files = [
        ("推送日志", LOG_DIR / "flashcard-push.log"),
        ("论文收集日志", LOG_DIR / "paper-fetch.log"),
    ]
    
    for name, log_file in log_files:
        if log_file.exists():
            # 检查最后修改时间
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            age_hours = (datetime.now() - mtime).total_seconds() / 3600
            
            if age_hours < 24:
                print_status(name, "OK", f"最近更新: {age_hours:.1f} 小时前")
            else:
                print_status(name, "WARN", f"未更新: {age_hours:.1f} 小时前")
        else:
            print_status(name, "WARN", f"日志文件不存在: {log_file}")

def check_feishu():
    """检查飞书权限（简化版，实际需要调用 feishu 工具）"""
    print("\n" + "="*50)
    print("✈️  检查飞书配置")
    print("="*50)
    
    print("⚠️  请手动验证：")
    print("   1. 能否使用 feishu_create_doc 工具创建文档")
    print("   2. 飞书 OAuth 授权是否有效")
    print("   3. 文档创建后能否正常访问")
    
    return True

def weekly_check():
    """周收尾完整检查"""
    print("\n" + "="*50)
    print("🔍 周收尾完整检查")
    print("="*50)
    
    checks = [
        check_sources(),
        check_files(),
        check_pdfs(),
        check_flashcards(),
        check_cron_jobs(),
    ]
    
    if all(checks):
        print("\n" + COLORS["green"] + "✅ 所有检查通过！本周工作流正常。" + COLORS["reset"])
        return True
    else:
        print("\n" + COLORS["yellow"] + "⚠️ 部分检查未通过，请查看详情。" + COLORS["reset"])
        return False

def main():
    parser = argparse.ArgumentParser(description='论文阅读助手健康检查')
    parser.add_argument('--check-sources', action='store_true', help='检查数据源连通性')
    parser.add_argument('--check-files', action='store_true', help='检查关键文件')
    parser.add_argument('--check-pdfs', action='store_true', help='检查PDF完整性')
    parser.add_argument('--check-flashcards', action='store_true', help='检查知识卡片')
    parser.add_argument('--check-cron', action='store_true', help='检查定时任务')
    parser.add_argument('--check-logs', action='store_true', help='检查日志文件')
    parser.add_argument('--check-feishu', action='store_true', help='检查飞书权限')
    parser.add_argument('--weekly-check', action='store_true', help='周收尾完整检查')
    
    args = parser.parse_args()
    
    # 如果没有参数，执行默认检查
    if not any(vars(args).values()):
        check_sources()
        check_files()
        check_pdfs()
        check_flashcards()
        check_cron_jobs()
        check_logs()
        print("\n" + "="*50)
        print("💡 使用 --weekly-check 进行完整周检查")
        print("💡 使用 --check-feishu 验证飞书权限")
        return
    
    # 执行指定检查
    if args.check_sources:
        check_sources()
    if args.check_files:
        check_files()
    if args.check_pdfs:
        check_pdfs()
    if args.check_flashcards:
        check_flashcards()
    if args.check_cron:
        check_cron_jobs()
    if args.check_logs:
        check_logs()
    if args.check_feishu:
        check_feishu()
    if args.weekly_check:
        weekly_check()

if __name__ == "__main__":
    main()
