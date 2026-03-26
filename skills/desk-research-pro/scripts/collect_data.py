#!/usr/bin/env python3
"""
桌面研究资料收集脚本
用于收集公开资料并整理分类
"""

import requests
import json
import sys
from datetime import datetime
from typing import List, Dict, Any

# Tavily API 配置
TAVILY_API_KEY = "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"

def tavily_search(query: str, max_results: int = 8) -> Dict[str, Any]:
    """
    使用 Tavily API 搜索资料
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量
    
    Returns:
        搜索结果字典
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "max_results": max_results
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        return response.json()
    except Exception as e:
        print(f"❌ 搜索失败 '{query}': {e}", file=sys.stderr)
        return {"error": str(e)}

def collect_research_data(
    topic: str,
    dimensions: List[str] = None,
    output_file: str = None
) -> Dict[str, Any]:
    """
    收集研究资料
    
    Args:
        topic: 研究主题
        dimensions: 研究维度列表
        output_file: 输出文件路径
    
    Returns:
        整理后的资料库
    """
    
    if dimensions is None:
        dimensions = [
            "市场规模",
            "发展趋势", 
            "竞争格局",
            "用户画像",
            "商业模式",
            "政策法规"
        ]
    
    # 构建搜索查询
    queries = {
        "市场规模": [f"{topic} 市场规模 2024 行业报告", f"{topic} market size 2024"],
        "发展趋势": [f"{topic} 发展趋势 2024 前景", f"{topic} growth trend"],
        "竞争格局": [f"{topic} 竞争格局 主要企业 市场份额", f"{topic} competition"],
        "用户画像": [f"{topic} 用户画像 消费行为", f"{topic} user profile"],
        "商业模式": [f"{topic} 商业模式 盈利 营收", f"{topic} business model"],
        "政策法规": [f"{topic} 政策法规 行业标准", f"{topic} regulation policy"]
    }
    
    print(f"🔍 开始收集 '{topic}' 的研究资料...")
    print(f"📊 研究维度: {', '.join(dimensions)}")
    
    results = {
        "topic": topic,
        "collection_time": datetime.now().isoformat(),
        "total_sources": 0,
        "categories": {},
        "sources": []
    }
    
    all_sources = []
    
    for dimension in dimensions:
        if dimension not in queries:
            continue
            
        print(f"\n📁 收集维度: {dimension}")
        dimension_sources = []
        
        for query in queries[dimension]:
            print(f"  🔎 搜索: {query}")
            data = tavily_search(query)
            
            if "results" in data:
                for item in data["results"]:
                    source = {
                        "category": dimension,
                        "query": query,
                        "title": item.get("title", "N/A"),
                        "url": item.get("url", ""),
                        "content": item.get("content", "")[:500],
                        "answer": data.get("answer", "")
                    }
                    dimension_sources.append(source)
                    all_sources.append(source)
                    print(f"    ✅ {item.get('title', 'N/A')[:50]}...")
        
        results["categories"][dimension] = dimension_sources
        print(f"  📄 找到 {len(dimension_sources)} 条资料")
    
    results["sources"] = all_sources
    results["total_sources"] = len(all_sources)
    
    # 保存到文件
    if output_file is None:
        output_file = f"{topic}_资料库_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 资料收集完成!")
    print(f"📊 总计: {len(all_sources)} 条资料")
    print(f"💾 已保存至: {output_file}")
    
    return results

def generate_gap_analysis(data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    生成数据缺口分析
    
    Args:
        data: 收集的资料数据
    
    Returns:
        数据缺口清单
    """
    gaps = []
    
    # 检查每个维度的资料数量
    for category, sources in data.get("categories", {}).items():
        if len(sources) < 3:
            gaps.append({
                "dimension": category,
                "gap": f"{category}维度资料较少({len(sources)}条)",
                "severity": "中",
                "suggestion": f"补充搜索{category}相关关键词"
            })
    
    return gaps

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python collect_data.py <研究主题> [输出文件]")
        print("Example: python collect_data.py '攀岩运动市场'")
        sys.exit(1)
    
    topic = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 收集资料
    data = collect_research_data(topic, output_file=output_file)
    
    # 生成缺口分析
    gaps = generate_gap_analysis(data)
    if gaps:
        print("\n⚠️ 数据缺口提醒:")
        for gap in gaps:
            print(f"  - {gap['gap']}")
