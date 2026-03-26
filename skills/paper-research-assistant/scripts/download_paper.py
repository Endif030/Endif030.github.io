#!/usr/bin/env python3
"""
论文下载脚本 - 下载论文PDF并保存到学科目录
"""

import argparse
import json
import os
import re
from pathlib import Path

import requests

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
DATA_DIR = WORKSPACE / "data"
PAPERS_FILE = DATA_DIR / "papers.json"


def sanitize_filename(filename):
    """清理文件名，移除非法字符"""
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename[:100]  # 限制长度


def load_papers_db():
    """加载论文数据库"""
    if PAPERS_FILE.exists():
        with open(PAPERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"papers": [], "last_updated": None}


def save_papers_db(db):
    """保存论文数据库"""
    with open(PAPERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def download_paper(paper, overwrite=False):
    """下载单篇论文"""
    discipline = paper.get("discipline", "uncategorized")
    paper_dir = WORKSPACE / "papers" / discipline
    paper_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    if "arxiv_id" in paper:
        filename_base = f"arxiv_{paper['arxiv_id']}"
    else:
        safe_title = sanitize_filename(paper.get("title", "unknown"))
        filename_base = safe_title
    
    pdf_path = paper_dir / f"{filename_base}.pdf"
    
    # 检查是否已存在
    if pdf_path.exists() and not overwrite:
        print(f"   ⏭️  已存在: {pdf_path.name}")
        return str(pdf_path)
    
    # 获取PDF URL
    pdf_url = paper.get("pdf_url", "")
    if not pdf_url and "arxiv_id" in paper:
        pdf_url = f"https://arxiv.org/pdf/{paper['arxiv_id']}.pdf"
    
    if not pdf_url:
        print(f"   ❌ 无PDF链接: {paper.get('title', 'Unknown')}")
        return None
    
    # 下载PDF
    try:
        print(f"   ⬇️  下载: {pdf_url[:60]}...")
        response = requests.get(pdf_url, timeout=60, stream=True)
        response.raise_for_status()
        
        with open(pdf_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"   ✅ 已保存: {pdf_path.name}")
        
        # 更新数据库中的本地路径
        paper["local_pdf"] = str(pdf_path)
        
        return str(pdf_path)
    
    except Exception as e:
        print(f"   ❌ 下载失败: {e}")
        return None


def download_by_id(paper_id, overwrite=False):
    """通过ID下载论文"""
    db = load_papers_db()
    
    paper = next((p for p in db["papers"] if p["id"] == paper_id or p.get("arxiv_id") == paper_id), None)
    
    if not paper:
        print(f"❌ 未找到论文: {paper_id}")
        return None
    
    result = download_paper(paper, overwrite)
    
    if result:
        save_papers_db(db)
    
    return result


def download_by_discipline(discipline, max_papers=10, overwrite=False):
    """下载指定学科的所有论文"""
    db = load_papers_db()
    
    papers = [p for p in db["papers"] if p.get("discipline") == discipline]
    papers = papers[:max_papers]
    
    print(f"📚 下载 {len(papers)} 篇 {discipline} 论文...")
    
    downloaded = 0
    for paper in papers:
        result = download_paper(paper, overwrite)
        if result:
            downloaded += 1
    
    save_papers_db(db)
    
    print(f"✅ 成功下载 {downloaded}/{len(papers)} 篇论文")
    return downloaded


def main():
    parser = argparse.ArgumentParser(description="下载论文PDF")
    parser.add_argument("--paper-id", help="论文ID或arXiv ID")
    parser.add_argument("--discipline", help="学科ID，下载该学科所有论文")
    parser.add_argument("--max-papers", type=int, default=10, help="最大下载数量")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已存在的文件")
    parser.add_argument("--all", action="store_true", help="下载所有未下载的论文")
    
    args = parser.parse_args()
    
    if args.paper_id:
        result = download_by_id(args.paper_id, args.overwrite)
        if result:
            print(f"\n✅ 下载完成: {result}")
    
    elif args.discipline:
        download_by_discipline(args.discipline, args.max_papers, args.overwrite)
    
    elif args.all:
        db = load_papers_db()
        disciplines = set(p.get("discipline") for p in db["papers"] if p.get("discipline"))
        
        for disc in disciplines:
            download_by_discipline(disc, args.max_papers, args.overwrite)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
