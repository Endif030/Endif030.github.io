#!/usr/bin/env python3
"""
完整投资日报生成器 (方案C - Python路径)
数据源: AKShare + Tavily API + Tushare
"""

import akshare as ak
import requests
import json
from datetime import datetime
import sys
import os

# API配置
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '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')
TAVILY_API_URL = "https://api.tavily.com/search"

def search_news(query, count=5):
    """使用Tavily API搜索新闻"""
    if not TAVILY_API_KEY or TAVILY_API_KEY == "":
        print(f"⚠️ Tavily API Key未配置，跳过搜索: {query}")
        return None
    
    headers = {
        "Content-Type": "application/json"
    }
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
        response = requests.post(TAVILY_API_URL, headers=headers, data=json.dumps(data), timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Tavily API返回状态码 {response.status_code}: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"⚠️ 搜索 '{query}' 失败: {e}")
        return None

def generate_a_share_report():
    """生成A股部分 (70%)"""
    lines = []
    lines.append("## 🇨🇳 A股市场 (70%)")
    lines.append("")
    
    # 获取主要指数
    lines.append("### 📊 主要指数")
    lines.append("-" * 40)
    try:
        index_df = ak.stock_zh_index_spot()
        if not index_df.empty:
            main_indices = ['sh000001', 'sz399001', 'sz399006']  # 上证、深证、创业板
            index_names = ['上证指数', '深证成指', '创业板指']
            
            for i, (code, name) in enumerate(zip(main_indices, index_names)):
                if i < len(index_df):
                    row = index_df.iloc[i]
                    lines.append(f"- **{name}**: {row.get('最新价', 'N/A')} (涨跌: {row.get('涨跌幅', 'N/A')}%)")
    except Exception as e:
        lines.append(f"⚠️ 指数数据获取失败: {e}")
    
    lines.append("")
    
    # 获取A股热点新闻（通过搜索）
    lines.append("### 🔥 A股要闻")
    lines.append("-" * 40)
    
    # 尝试使用Tavily搜索
    try:
        a_share_news = search_news("A股市场热点 今日财经新闻", 4)
        if a_share_news and 'results' in a_share_news and a_share_news['results']:
            for i, result in enumerate(a_share_news['results'][:4], 1):
                title = result.get('title', '无标题')
                lines.append(f"{i}. {title}")
        else:
            lines.append("暂无Tavily新闻数据")
    except Exception as e:
        lines.append(f"⚠️ 新闻获取失败: {e}")
    
    lines.append("")
    return lines

def generate_us_stock_report():
    """生成美股部分 (20%)"""
    lines = []
    lines.append("## 🇺🇸 美股动态 (20%)")
    lines.append("")
    
    lines.append("### 📈 市场焦点")
    lines.append("-" * 40)
    
    try:
        us_news = search_news("美股今日行情 纳斯达克指数 科技股动态", 3)
        if us_news and 'results' in us_news and us_news['results']:
            for i, result in enumerate(us_news['results'][:3], 1):
                title = result.get('title', '无标题')
                lines.append(f"{i}. {title}")
        else:
            lines.append("暂无美股新闻数据")
    except Exception as e:
        lines.append(f"⚠️ 美股数据获取失败: {e}")
    
    lines.append("")
    return lines

def generate_crypto_report():
    """生成币圈部分 (10%)"""
    lines = []
    lines.append("## 🪙 数字资产 (10%)")
    lines.append("")
    
    lines.append("### 🔥 最新资讯")
    lines.append("-" * 40)
    
    try:
        crypto_news = search_news("比特币 以太坊 加密货币市场行情", 2)
        if crypto_news and 'results' in crypto_news and crypto_news['results']:
            for i, result in enumerate(crypto_news['results'][:2], 1):
                title = result.get('title', '无标题')
                lines.append(f"{i}. {title}")
        else:
            lines.append("暂无币圈新闻数据")
    except Exception as e:
        lines.append(f"⚠️ 币圈数据获取失败: {e}")
    
    lines.append("")
    return lines

def generate_summary():
    """生成摘要"""
    lines = []
    lines.append("## 💡 核心要点")
    lines.append("-" * 40)
    lines.append("- A股市场今日表现分析")
    lines.append("- 美股科技股动态追踪")
    lines.append("- 币圈政策环境变化观察")
    lines.append("- 明日重点关注板块提示")
    lines.append("")
    return lines

def main():
    """主函数"""
    lines = []
    lines.append("# 📊 每日投资简报 (方案C)")
    lines.append("")
    lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append(f"*数据源: AKShare + Tavily API*")
    lines.append("")
    lines.append("=" * 70)
    lines.append("")
    
    try:
        # 生成各部分
        lines.extend(generate_a_share_report())
        lines.extend(generate_us_stock_report())
        lines.extend(generate_crypto_report())
        lines.extend(generate_summary())
        
        # 输出到标准输出
        print("\n".join(lines))
        
        # 同时保存到文件
        output_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/daily-report-c-" + datetime.now().strftime('%Y%m%d') + ".md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        
        print(f"\n✅ 报告已保存到: {output_path}", file=sys.stderr)
        
    except Exception as e:
        print(f"\n❌ 报告生成失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
