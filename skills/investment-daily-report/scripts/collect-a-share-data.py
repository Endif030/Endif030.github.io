#!/usr/bin/env python3

"""
A股数据收集与报告生成 - 阶段1：核心数据模块
集成AKShare数据源，生成A股投资简报
"""

import sys
import json
from datetime import datetime, timedelta

# 设置UTF-8输出
sys.stdout.reconfigure(encoding='utf-8')

try:
    import akshare as ak
    print(f"✅ AKShare 加载成功，版本: {ak.__version__}")
except ImportError:
    print("❌ AKShare未安装，请先安装: pip install akshare", file=sys.stderr)
    sys.exit(1)

def safe_get_data(func, *args, **kwargs):
    """安全获取数据，失败返回空DataFrame"""
    try:
        data = func(*args, **kwargs)
        if data is not None and not data.empty:
            return data
        return None
    except Exception as e:
        print(f"⚠️  数据获取失败: {e}", file=sys.stderr)
        return None

def get_index_data():
    """获取主要指数数据"""
    print("📊 正在获取指数数据...")
    
    indices = {
        "上证": "sh000001",
        "深证成指": "sz399001",
        "创业板": "sz399006",
        "科创50": "sh000688",
        "沪深300": "sh000300"
    }
    
    result = {}
    for name, code in indices.items():
        data = safe_get_data(ak.stock_zh_index_daily_em, symbol=code)
        if data is not None and not data.empty:
            latest = data.iloc[-1]
            prev = data.iloc[-2] if len(data) > 1 else latest
            
            change = ((latest['close'] - prev['close']) / prev['close'] * 100) if prev['close'] != 0 else 0
            
            result[name] = {
                "code": code,
                "current": round(latest['close'], 2),
                "change": round(change, 2),
                "volume": int(latest.get('volume', 0)),
                "amount": int(latest.get('amount', 0))
            }
        else:
            print(f"⚠️  {name}({code}) 数据获取失败")
            result[name] = None
    
    return result

def get_market_stats():
    """获取市场整体统计"""
    print("📈 正在获取市场统计...")
    
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_stocks": 0,
        "up_count": 0,
        "down_count": 0,
        "limit_up": 0,
        "limit_down": 0
    }
    
    # 获取涨停数据
    today = datetime.now().strftime("%Y%m%d")
    zt_data = safe_get_data(ak.stock_zt_pool_em, date=today)
    
    if zt_data is not None:
        stats["limit_up"] = len(zt_data)
        print(f"✅ 涨停数量: {stats['limit_up']}")
    
    # 跌停数据
    dt_data = safe_get_data(ak.stock_zt_pool_dtgc_em, date=today)
    if dt_data is not None:
        stats["limit_down"] = len(dt_data)
        print(f"✅ 跌停数量: {stats['limit_down']}")
    
    # A股总体数据
    all_stocks = safe_get_data(ak.stock_zh_a_spot_em)
    if all_stocks is not None:
        stats["total_stocks"] = len(all_stocks)
        stats["up_count"] = len(all_stocks[all_stocks['涨跌幅'] > 0])
        stats["down_count"] = len(all_stocks[all_stocks['涨跌幅'] < 0])
        print(f"✅ 总股票数: {stats['total_stocks']}, 上涨: {stats['up_count']}, 下跌: {stats['down_count']}")
    
    return stats

def get_top_concepts():
    """获取热门概念板块"""
    print("🔥 正在获取热门概念...")
    
    try:
        # 获取概念板块数据
        concept_data = safe_get_data(ak.stock_board_concept_name_em)
        
        if concept_data is None or concept_data.empty:
            print("⚠️  概念板块数据获取失败")
            return None
        
        # 按涨跌幅排序，取前5和后5
        concept_data['涨跌幅'] = pd.to_numeric(concept_data['涨跌幅'], errors='coerce')
        sorted_data = concept_data.dropna(subset=['涨跌幅']).sort_values('涨跌幅', ascending=False)
        
        top_5 = sorted_data.head(5)
        bottom_5 = sorted_data.tail(5)
        
        result = {
            "top_5": [],
            "bottom_5": []
        }
        
        # 获取每个概念板块的热门个股
        for _, concept in top_5.iterrows():
            concept_name = concept['板块名称']
            change = concept['涨跌幅']
            
            # 获取该概念的个股
            try:
                stocks = safe_get_data(ak.stock_board_concept_cons_em, symbol=concept_name)
                hot_stocks = []
                if stocks is not None and not stocks.empty:
                    hot_stocks = stocks.head(3)['名称'].tolist()
                
                result["top_5"].append({
                    "name": concept_name,
                    "change": round(change, 2),
                    "hot_stocks": hot_stocks
                })
            except:
                result["top_5"].append({
                    "name": concept_name,
                    "change": round(change, 2),
                    "hot_stocks": []
                })
        
        for _, concept in bottom_5.iterrows():
            concept_name = concept['板块名称']
            change = concept['涨跌幅']
            
            result["bottom_5"].append({
                "name": concept_name,
                "change": round(change, 2),
                "hot_stocks": []
            })
        
        print(f"✅ 概念板块数据获取成功，Top5: {len(result['top_5'])}, Bottom5: {len(result['bottom_5'])}")
        return result
        
    except Exception as e:
        print(f"⚠️  获取概念板块失败: {e}")
        return None

def get_top_performers():
    """获取涨幅榜个股"""
    print("📈 正在获取涨幅榜...")
    
    all_stocks = safe_get_data(ak.stock_zh_a_spot_em)
    
    if all_stocks is None or all_stocks.empty:
        print("⚠️  无法获取股票数据")
        return None
    
    # 按涨跌幅排序，取前10
    top_10 = all_stocks.nlargest(10, '涨跌幅')
    
    result = []
    for _, stock in top_10.iterrows():
        result.append({
            "code": stock['代码'],
            "name": stock['名称'],
            "change": round(stock['涨跌幅'], 2),
            "volume": int(stock.get('成交额', 0)),
            "concepts": []  # 需要额外API获取所属概念
        })
    
    print(f"✅ 涨幅榜获取成功，共{len(result)}只股票")
    return result

def generate_markdown_report(data):
    """生成Markdown格式报告"""
    
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    report = f"# 📊 A股市场日报\n\n"
    report += f"*Generated on {now} China Standard Time*\n\n"
    report += f"---\n\n"
    
    # 市场指数
    report += f"## 📈 市场指数\n\n"
    report += f"| 指数 | 当前点位 | 涨跌幅 | 成交量 | 成交额 |\n"
    report += f"|------|----------|--------|--------|--------|\n"
    
    for name, idx_data in data.get('indices', {}).items():
        if idx_data:
            report += f"| {name} | {idx_data['current']} | {idx_data['change']:+}% | {idx_data['volume']:,} | {idx_data['amount']:,} |\n"
    
    report += f"\n"
    
    # 市场统计
    stats = data.get('stats', {})
    report += f"## 📊 市场统计\n\n"
    report += f"- **总股票数**: {stats.get('total_stocks', 0)}\n"
    report += f"- **上涨股票**: {stats.get('up_count', 0)}\n"
    report += f"- **下跌股票**: {stats.get('down_count', 0)}\n"
    report += f"- **涨停数量**: {stats.get('limit_up', 0)}\n"
    report += f"- **跌停数量**: {stats.get('limit_down', 0)}\n\n"
    
    report += f"---\n\n"
    
    # 热门概念
    concepts = data.get('concepts')
    if concepts:
        report += f"## 🔥 热门概念板块\n\n"
        
        report += f"### 涨幅前5\n\n"
        report += f"| 概念板块 | 涨跌幅 | 热门个股 |\n"
        report += f"|----------|--------|----------|\n"
        
        for concept in concepts.get('top_5', []):
            hot_stocks = ', '.join(concept['hot_stocks'][:3]) if concept['hot_stocks'] else 'N/A'
            report += f"| {concept['name']} | {concept['change']:+}% | {hot_stocks} |\n"
        
        report += f"\n### 跌幅前5\n\n"
        report += f"| 概念板块 | 涨跌幅 |\n"
        report += f"|----------|--------|\n"
        
        for concept in concepts.get('bottom_5', []):
            report += f"| {concept['name']} | {concept['change']:+}% |\n"
        
        report += f"\n"
    
    report += f"---\n\n"
    
    # 涨幅榜
    top_performers = data.get('top_performers')
    if top_performers:
        report += f"## 📈 涨幅榜（前10）\n\n"
        report += f"| 排名 | 代码 | 名称 | 涨跌幅 | 成交额(万) |\n"
        report += f"|------|------|------|--------|------------|\n"
        
        for i, stock in enumerate(top_performers, 1):
            volume_wan = stock['volume'] / 10000 if stock['volume'] else 0
            report += f"| {i} | {stock['code']} | {stock['name']} | {stock['change']:+}% | {volume_wan:.0f} |\n"
        
        report += f"\n"
    
    report += f"---\n\n"
    report += f"*数据由 AKShare 提供 | 仅供参考，不构成投资建议*\n"
    
    return report

def main():
    """主函数"""
    
    print("=" * 80)
    print("📈 A股市场日报数据收集系统 v1.0")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # 收集数据（分步进行，避免超时）
    print("📊 第1步：获取市场统计（涨跌停等）...")
    stats = get_market_stats()
    
    print("📊 第2步：获取指数数据...")
    indices = get_index_data()
    
    print("📊 第3步：获取热门概念（此步骤可能需要较长时间）...")
    concepts = get_top_concepts()
    
    print("📊 第4步：获取涨幅榜...")
    top_performers = get_top_performers()
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "indices": indices,
        "stats": stats,
        "concepts": concepts,
        "top_performers": top_performers
    }
    
    # 生成报告
    print()
    print("📝 正在生成报告...")
    report = generate_markdown_report(data)
    
    # 保存报告
    output_file = "/tmp/a-share-daily-report.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print()
    print("=" * 80)
    print(f"✅ 报告生成完成！")
    print(f"📄 报告文件: {output_file}")
    print("=" * 80)
    
    # 同时输出JSON数据
    json_file = "/tmp/a-share-data.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 JSON数据: {json_file}")

if __name__ == "__main__":
    try:
        import pandas as pd
        main()
    except ImportError:
        print("❌ pandas未安装，请安装: pip install pandas", file=sys.stderr)
        sys.exit(1)