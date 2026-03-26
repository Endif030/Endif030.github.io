#!/usr/bin/env python3
"""
A股专属简报生成器 (2026-02-28)
"""

import requests
import json
from datetime import datetime
import sys

TAVILY_API_KEY = "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"
TAVILY_API_URL = "https://api.tavily.com/search"

def search_news(query, count=5):
    """搜索新闻"""
    if not TAVILY_API_KEY:
        return None
    
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_images": False,
        "include_answer": False,
        "max_results": count,
        "include_raw_content": False
    }
    
    try:
        response = requests.post(TAVILY_API_URL, headers=headers, data=json.dumps(data), timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"搜索失败: {e}", file=sys.stderr)
        return None

def main():
    lines = []
    lines.append(f"# 📊 A股投资简报 (2026-02-28)")
    lines.append("")
    lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append(f"*数据源: Tavily API 历史数据*")
    lines.append("")
    lines.append("=" * 70)
    lines.append("")
    
    # A股市场焦点 - 针对2026-02-28
    lines.append("## 🇨🇳 A股市场 (100%)")
    lines.append("")
    
    # 指数行情
    lines.append("### 📈 主要指数行情")
    lines.append("-" * 40)
    news = search_news("2026年2月28日 上证指数 A股收盘", 4)
    if news and news.get('results'):
        for i, result in enumerate(news['results'][:4], 1):
            title = result.get('title', '无标题')
            source = result.get('url', '')
            lines.append(f"{i}. {title}")
            if source:
                lines.append(f"   📎 {source}")
    else:
        lines.append("⚠️ 历史数据获取有限")
    lines.append("")
    
    # 行业板块
    lines.append("### 🔥 热门板块")
    lines.append("-" * 40)
    news = search_news("2026年2月28日 A股半导体 新能源 医药", 3)
    if news and news.get('results'):
        for i, result in enumerate(news['results'][:3], 1):
            title = result.get('title', '无标题')
            lines.append(f"{i}. {title}")
    lines.append("")
    
    # 政策消息
    lines.append("### 📢 政策与监管")
    lines.append("-" * 40)
    news = search_news("2026年2月28日 证监会 A股政策", 3)
    if news and news.get('results'):
        for i, result in enumerate(news['results'][:3], 1):
            title = result.get('title', '无标题')
            lines.append(f"{i}. {title}")
    lines.append("")
    
    # 北向资金
    lines.append("### 💰 北向资金动向")
    lines.append("-" * 40)
    news = search_news("2026年2月28日 北向资金 外资流入", 2)
    if news and news.get('results'):
        for i, result in enumerate(news['results'][:2], 1):
            title = result.get('title', '无标题')
            lines.append(f"{i}. {title}")
    lines.append("")
    
    # 个股动态
    lines.append("### 🏢 个股动态")
    lines.append("-" * 40)
    news = search_news("2026年2月28日 A股涨停 跌停 个股", 3)
    if news and news.get('results'):
        for i, result in enumerate(news['results'][:3], 1):
            title = result.get('title', '无标题')
            lines.append(f"{i}. {title}")
    lines.append("")
    
    # 打印报告
    print("\n".join(lines))
    
    # 保存到文件
    output_path = "/tmp/a-share-briefing-20260228.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"\n✅ 报告已保存到: {output_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
