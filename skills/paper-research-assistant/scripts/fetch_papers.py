#!/usr/bin/env python3
"""
论文抓取脚本 - 从arXiv和Semantic Scholar获取热门论文
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

import requests
import yaml

# 配置
WORKSPACE = Path("/root/.openclaw/workspace/paper-research")
DATA_DIR = WORKSPACE / "data"
PAPERS_FILE = DATA_DIR / "papers.json"

# 学科配置
DISCIPLINES = {
    "ai": {
        "name": "人工智能",
        "arxiv_cats": ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.RO"],
        "keywords": ["artificial intelligence", "machine learning", "deep learning", "large language model"],
        "fields": ["Computer Science"]
    },
    "psychology": {
        "name": "心理学",
        "arxiv_cats": ["q-bio.NC"],
        "keywords": ["psychology", "cognitive science", "behavioral science", "mental health"],
        "fields": ["Psychology", "Neuroscience"]
    },
    "social-science": {
        "name": "社会科学",
        "arxiv_cats": ["cs.CY"],
        "keywords": ["social science", "sociology", "computational social science"],
        "fields": ["Sociology", "Political Science", "Economics"]
    },
    "anthropology": {
        "name": "人类学",
        "arxiv_cats": [],
        "keywords": ["anthropology", "cultural anthropology", "ethnography"],
        "fields": ["Anthropology"]
    },
    "philosophy": {
        "name": "哲学",
        "arxiv_cats": ["cs.CY"],
        "keywords": ["philosophy", "ethics", "philosophy of mind", "AI ethics"],
        "fields": ["Philosophy"]
    },
    "game-studies": {
        "name": "游戏研究",
        "arxiv_cats": ["cs.HC", "cs.AI"],
        "keywords": ["game studies", "game design", "gamification", "video games"],
        "fields": ["Computer Science"]
    }
}


def ensure_dirs():
    """确保目录结构存在"""
    for discipline in DISCIPLINES.keys():
        (WORKSPACE / "papers" / discipline).mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


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


def fetch_arxiv_papers(category, max_results=10):
    """从arXiv获取论文"""
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{category}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # 解析Atom XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        
        # 命名空间
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            paper = {
                "id": entry.find('atom:id', ns).text if entry.find('atom:id', ns) is not None else "",
                "title": entry.find('atom:title', ns).text.strip() if entry.find('atom:title', ns) is not None else "",
                "summary": entry.find('atom:summary', ns).text.strip() if entry.find('atom:summary', ns) is not None else "",
                "published": entry.find('atom:published', ns).text if entry.find('atom:published', ns) is not None else "",
                "updated": entry.find('atom:updated', ns).text if entry.find('atom:updated', ns) is not None else "",
                "authors": [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
                "categories": [cat.get('term') for cat in entry.findall('atom:category', ns)],
                "source": "arxiv",
                "pdf_url": "",
                "doi": ""
            }
            
            # 提取arXiv ID并构建PDF链接
            arxiv_id_match = re.search(r'arXiv:(\d+\.\d+)', paper["id"])
            if arxiv_id_match:
                arxiv_id = arxiv_id_match.group(1)
                paper["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                paper["arxiv_id"] = arxiv_id
            
            # 提取DOI
            doi_elem = entry.find('arxiv:doi', ns)
            if doi_elem is not None:
                paper["doi"] = doi_elem.text
            
            papers.append(paper)
        
        return papers
    except Exception as e:
        print(f"Error fetching arXiv papers for {category}: {e}")
        return []


def fetch_semantic_scholar_papers(keyword, fields=None, limit=10):
    """从Semantic Scholar获取论文"""
    if fields is None:
        fields = "paperId,title,abstract,year,citationCount,authors,url,openAccessPdf"
    
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": keyword,
        "fields": fields,
        "limit": limit,
        "sort": "citationCount:desc"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        papers = []
        for item in data.get("data", []):
            paper = {
                "id": f"s2_{item.get('paperId', '')}",
                "title": item.get("title", ""),
                "summary": item.get("abstract", ""),
                "published": f"{item.get('year', '2024')}-01-01",
                "year": item.get("year", 2024),
                "authors": [a.get("name", "") for a in item.get("authors", [])],
                "citation_count": item.get("citationCount", 0),
                "source": "semantic_scholar",
                "url": item.get("url", ""),
                "pdf_url": item.get("openAccessPdf", {}).get("url", "") if item.get("openAccessPdf") else "",
                "doi": "",
                "categories": []
            }
            papers.append(paper)
        
        return papers
    except Exception as e:
        print(f"Error fetching Semantic Scholar papers for {keyword}: {e}")
        return []


def fetch_discipline_papers(discipline_id, max_per_source=10):
    """获取指定学科的热门论文"""
    config = DISCIPLINES.get(discipline_id)
    if not config:
        print(f"Unknown discipline: {discipline_id}")
        return []
    
    all_papers = []
    
    # 从arXiv获取
    for cat in config["arxiv_cats"]:
        papers = fetch_arxiv_papers(cat, max_per_source)
        for p in papers:
            p["discipline"] = discipline_id
        all_papers.extend(papers)
        time.sleep(3)  # 避免速率限制
    
    # 从Semantic Scholar获取
    for keyword in config["keywords"][:2]:  # 取前2个关键词
        papers = fetch_semantic_scholar_papers(keyword, limit=max_per_source)
        for p in papers:
            p["discipline"] = discipline_id
        all_papers.extend(papers)
        time.sleep(1)
    
    # 去重（基于标题相似度）
    seen_titles = set()
    unique_papers = []
    for p in all_papers:
        title_key = p["title"].lower().strip()
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_papers.append(p)
    
    # 按引用数和时间排序，取Top N
    unique_papers.sort(key=lambda x: (x.get("year", 2024), x.get("citation_count", 0)), reverse=True)
    
    return unique_papers[:max_per_source]


def main():
    parser = argparse.ArgumentParser(description="获取学科热门论文")
    parser.add_argument("--discipline", choices=list(DISCIPLINES.keys()) + ["all"], 
                        default="all", help="学科ID")
    parser.add_argument("--max-results", type=int, default=10, help="每学科最大结果数")
    parser.add_argument("--output", help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    disciplines_to_fetch = list(DISCIPLINES.keys()) if args.discipline == "all" else [args.discipline]
    
    all_results = {}
    db = load_papers_db()
    
    for disc_id in disciplines_to_fetch:
        print(f"\n📚 正在获取: {DISCIPLINES[disc_id]['name']}")
        papers = fetch_discipline_papers(disc_id, args.max_results)
        all_results[disc_id] = papers
        
        # 更新数据库
        for p in papers:
            # 检查是否已存在
            existing = next((x for x in db["papers"] if x["id"] == p["id"]), None)
            if existing:
                existing.update(p)
            else:
                p["fetched_at"] = datetime.now().isoformat()
                db["papers"].append(p)
        
        print(f"   获取 {len(papers)} 篇论文")
        time.sleep(5)  # 学科间间隔
    
    db["last_updated"] = datetime.now().isoformat()
    save_papers_db(db)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完成！总计获取 {sum(len(v) for v in all_results.values())} 篇论文")
    
    # 输出摘要
    for disc_id, papers in all_results.items():
        print(f"\n{DISCIPLINES[disc_id]['name']}:")
        for i, p in enumerate(papers[:5], 1):
            print(f"  {i}. {p['title'][:60]}...")


if __name__ == "__main__":
    main()
