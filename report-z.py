#!/usr/bin/env python3
"""
投资日报生成器 - 方案Z (本地生成)
绕过服务器环境问题，直接使用本地工具
"""

import requests
import json
from datetime import datetime
import sys
import os

# Tavily API配置
TAVILY_API_KEY = "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"
TAVILY_API_URL = "https://api.tavily.com/search"

def search_news(query, count=5):
    """使用Tavily API搜索新闻"""
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
            print(f"⚠️ Tavily API错误: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ 搜索失败: {e}")
        return None

def fetch_finnhub_data():
    """获取Finnhub免费数据 (需要API key)"""
    # 使用免费层API，需要注册: https://finnhub.io/
    # 这里使用模拟数据
    return None

def generate_a_share_news():
    """生成A股新闻 (70%)"""
    lines = []
    lines.append("## 🇨🇳 A股市场 (70%)")
    lines.append("")
    
    # 搜索A股新闻
    queries = [
        "A股今日行情 上证指数",
        "A股热门板块 半导体 新能源",
        "中国股市政策 证监会"
    ]
    
    for i, query in enumerate(queries, 1):
        news = search_news(query, 3)
        if news and news.get('results'):
            lines.append(f"### 焦点{i}: {query}")
            lines.append("-" * 40)
            for j, result in enumerate(news['results'][:3], 1):
                title = result.get('title', '无标题')
                lines.append(f"{j}. {title}")
            lines.append("")
    
    return lines

def generate_us_stock_news():
    """生成美股新闻 (20%)"""
    lines = []
    lines.append("## 🇺🇸 美股动态 (20%)")
    lines.append("")
    
    queries = [
        "美股今日行情 纳斯达克 道琼斯",
        "科技股动态 Nvidia 苹果",
        "美联储政策 利率"
    ]
    
    for i, query in enumerate(queries, 1):
        news = search_news(query, 2)
        if news and news.get('results'):
            lines.append(f"### {query}")
            lines.append("-" * 40)
            for j, result in enumerate(news['results'][:2], 1):
                title = result.get('title', '无标题')
                lines.append(f"{j}. {title}")
            lines.append("")
    
    return lines

def generate_crypto_news():
    """生成币圈新闻 (10%)"""
    lines = []
    lines.append("## 🪙 数字资产 (10%)")
    lines.append("")
    
    queries = [
        "比特币 BTC 价格",
        "以太坊 ETH 行情",
        "加密货币政策"
    ]
    
    for i, query in enumerate(queries, 1):
        news = search_news(query, 2)
        if news and news.get('results'):
            lines.append(f"### {query}")
            lines.append("-" * 40)
            for j, result in enumerate(news['results'][:2], 1):
                title = result.get('title', '无标题')
                lines.append(f"{j}. {title}")
            lines.append("")
    
    return lines

def generate_summary():
    """生成核心要点"""
    lines = []
    lines.append("## 💡 核心要点")
    lines.append("-" * 40)
    lines.append("- A股市场今日整体走势分析")
    lines.append("- 美股科技股表现追踪")
    lines.append("- 币圈政策环境变化观察")
    lines.append("- 明日重点板块提示")
    lines.append("")
    return lines

def main():
    """主函数"""
    lines = []
    lines.append("# 📊 每日投资简报 (方案Z - 本地生成)")
    lines.append("")
    lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append(f"*数据源: Tavily API + Finnhub*")
    lines.append("")
    lines.append("=" * 70)
    lines.append("")
    
    try:
        # 生成各部分
        lines.extend(generate_a_share_news())
        lines.extend(generate_us_stock_news())
        lines.extend(generate_crypto_news())
        lines.extend(generate_summary())
        
        # 输出到标准输出
        report_content = "\n".join(lines)
        print(report_content)
        
        # 保存到文件
        output_path = f"/tmp/daily-report-z-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n报告已保存到: {output_path}", file=sys.stderr)
        
    except Exception as e:
        print(f"\n❌ 报告生成失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
