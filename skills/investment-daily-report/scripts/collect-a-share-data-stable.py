#!/usr/bin/env python3

"""
简化版A股数据收集 - 使用稳定数据源
专注于可可靠获取的数据：涨停数据、市场统计
"""

import sys
import json
from datetime import datetime

# 设置UTF-8输出
sys.stdout.reconfigure(encoding='utf-8')

try:
    import akshare as ak
    print(f"✅ AKShare 加载成功，版本: {ak.__version__}")
except ImportError:
    print("❌ AKShare未安装，请先安装: pip install akshare", file=sys.stderr)
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("❌ pandas未安装，请先安装: pip install pandas", file=sys.stderr)
    sys.exit(1)

def get_limit_up_stocks():
    """获取涨停股票列表"""
    print("📊 正在获取涨停股票数据...")
    
    try:
        today = datetime.now().strftime("%Y%m%d")
        zt_data = ak.stock_zt_pool_em(date=today)
        
        if zt_data is not None and not zt_data.empty:
            print(f"✅ 涨停数量: {len(zt_data)}")
            
            # 转换为列表
            limit_up_list = []
            for _, stock in zt_data.head(20).iterrows():  # 只取前20只
                limit_up_list.append({
                    "code": str(stock['代码']),
                    "name": str(stock['名称']),
                    "change": round(float(stock['涨跌幅']), 2),
                    "volume": int(stock.get('成交额', 0)),
                    "first_limit_time": str(stock.get('首次涨停时间', 'N/A')),
                    "last_limit_time": str(stock.get('最后涨停时间', 'N/A')),
                    "open_times": int(stock.get('开板次数', 0)),
                    "limit_type": "一字板" if str(stock.get('涨停统计', '')).count('1') == 1 else "涨停"
                })
            
            return len(zt_data), limit_up_list
        else:
            print("⚠️  涨停数据为空")
            return 0, []
    except Exception as e:
        print(f"❌ 涨停数据获取失败: {e}")
        return 0, []

def get_limit_down_stocks():
    """获取跌停股票列表"""
    print("📊 正在获取跌停股票数据...")
    
    try:
        today = datetime.now().strftime("%Y%m%d")
        dt_data = ak.stock_zt_pool_dtgc_em(date=today)
        
        if dt_data is not None and not dt_data.empty:
            print(f"✅ 跌停数量: {len(dt_data)}")
            
            # 只取基本信息
            limit_down_list = []
            for _, stock in dt_data.head(10).iterrows():
                limit_down_list.append({
                    "code": str(stock['代码']),
                    "name": str(stock['名称']),
                    "change": round(float(stock['涨跌幅']), 2)
                })
            
            return len(dt_data), limit_down_list
        else:
            print("⚠️  无跌停股票")
            return 0, []
    except Exception as e:
        print(f"❌ 跌停数据获取失败: {e}")
        return 0, []

def get_market_overview():
    """获取市场整体概况"""
    print("📈 正在获取市场概况...")
    
    market_data = {
        "total_stocks": 0,
        "up_count": 0,
        "down_count": 0,
        "flat_count": 0,
        "up_limit": 0,
        "down_limit": 0
    }
    
    try:
        # 获取所有A股数据
        all_stocks = ak.stock_zh_a_spot_em()
        
        if all_stocks is not None and not all_stocks.empty:
            market_data["total_stocks"] = len(all_stocks)
            
            # 计算涨跌平
            market_data["up_count"] = len(all_stocks[all_stocks['涨跌幅'] > 0])
            market_data["down_count"] = len(all_stocks[all_stocks['涨跌幅'] < 0])
            market_data["flat_count"] = len(all_stocks[abs(all_stocks['涨跌幅']) < 0.001])
            
            # 计算涨跌停（通常涨跌幅超过9.9%算涨停）
            market_data["up_limit"] = len(all_stocks[all_stocks['涨跌幅'] >= 9.9])
            market_data["down_limit"] = len(all_stocks[all_stocks['涨跌幅'] <= -9.9])
            
            print(f"✅ 市场概况: 总数{market_data['total_stocks']}, 上涨{market_data['up_count']}, 下跌{market_data['down_count']}")
        else:
            print("⚠️  市场概况数据为空")
    except Exception as e:
        print(f"❌ 市场概况获取失败: {e}")
    
    return market_data

def get_concept_boards():
    """获取概念板块涨跌情况"""
    print("🔥 正在获取概念板块数据...")
    
    try:
        # 获取概念板块
        concept_data = ak.stock_board_concept_name_em()
        
        if concept_data is not None and not concept_data.empty:
            # 排序
            concept_data['涨跌幅'] = pd.to_numeric(concept_data['涨跌幅'], errors='coerce')
            sorted_data = concept_data.dropna(subset=['涨跌幅']).sort_values('涨跌幅', ascending=False)
            
            # 取前5和后5
            top_5 = sorted_data.head(5)
            bottom_5 = sorted_data.tail(5)
            
            result = {
                "top_5": [],
                "bottom_5": []
            }
            
            # 处理涨幅前5
            for _, concept in top_5.iterrows():
                result["top_5"].append({
                    "name": str(concept['板块名称']),
                    "change": round(float(concept['涨跌幅']), 2)
                })
            
            # 处理跌幅前5
            for _, concept in bottom_5.iterrows():
                result["bottom_5"].append({
                    "name": str(concept['板块名称']),
                    "change": round(float(concept['涨跌幅']), 2)
                })
            
            print(f"✅ 概念板块: 涨幅前{len(result['top_5'])}, 跌幅前{len(result['bottom_5'])}")
            return result
        else:
            print("⚠️  概念板块数据为空")
            return None
    except Exception as e:
        print(f"❌ 概念板块获取失败: {e}")
        return None

def generate_report(data):
    """生成Markdown报告"""
    
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    report = f"# 📊 A股市场日报\n\n"
    report += f"*生成时间: {now} | 中国标准时间*\n\n"
    report += f"---\n\n"
    
    # 市场概况
    market = data.get('market_overview', {})
    report += f"## 📈 市场概况\n\n"
    report += f"- **总股票数**: {market.get('total_stocks', 0):,}\n"
    report += f"- **上涨**: {market.get('up_count', 0):,}\n"
    report += f"- **下跌**: {market.get('down_count', 0):,}\n"
    report += f"- **平盘**: {market.get('flat_count', 0):,}\n"
    report += f"- **涨停**: {market.get('up_limit', 0)}\n"
    report += f"- **跌停**: {market.get('down_limit', 0)}\n\n"
    
    report += f"---\n\n"
    
    # 涨停统计
    report += f"## 🚀 涨停统计\n\n"
    report += f"- **今日涨停**: {data.get('limit_up_count', 0)} 只\n\n"
    
    if data.get('limit_up_stocks'):
        report += f"| 代码 | 名称 | 涨幅 | 开板次数 | 涨停时间 |\n"
        report += f"|------|------|------|----------|----------|\n"
        
        for stock in data['limit_up_stocks'][:15]:  # 只显示前15只
            report += f"| {stock['code']} | {stock['name']} | {stock['change']:+.2f}% | {stock['open_times']} | {stock['first_limit_time']} |\n"
        
        if data.get('limit_up_count', 0) > 15:
            report += f"| ... | 还有 {data['limit_up_count'] - 15} 只 | | | |\n"
    
    report += f"\n"
    report += f"---\n\n"
    
    # 概念板块
    concepts = data.get('concepts')
    if concepts:
        report += f"## 🔥 概念板块\n\n"
        
        # 涨幅前5
        report += f"### 📈 涨幅前5\n\n"
        report += f"| 板块名称 | 涨跌幅 |\n"
        report += f"|----------|--------|\n"
        
        for concept in concepts.get('top_5', []):
            report += f"| {concept['name']} | {concept['change']:+.2f}% |\n"
        
        report += f"\n### 📉 跌幅前5\n\n"
        report += f"| 板块名称 | 涨跌幅 |\n"
        report += f"|----------|--------|\n"
        
        for concept in concepts.get('bottom_5', []):
            report += f"| {concept['name']} | {concept['change']:+.2f}% |\n"
        
        report += f"\n"
    
    report += f"---\n\n"
    
    # 跌停情况
    if data.get('limit_down_count', 0) > 0:
        report += f"## 💥 跌停情况\n\n"
        report += f"- **今日跌停**: {data.get('limit_down_count', 0)} 只\n\n"
        
        if data.get('limit_down_stocks'):
            report += f"| 代码 | 名称 | 跌幅 |\n"
            report += f"|------|------|------|\n"
            
            for stock in data['limit_down_stocks']:
                report += f"| {stock['code']} | {stock['name']} | {stock['change']:+.2f}% |\n"
        
        report += f"\n"
    
    report += f"---\n\n"
    report += f"*数据来源: AKShare | 更新时间: {now}*\n"
    
    return report

def main():
    """主函数"""
    
    print("=" * 80)
    print("📊 A股市场日报 - 稳定版")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # 收集数据
    data = {
        "timestamp": datetime.now().isoformat(),
        "limit_up_count": 0,
        "limit_up_stocks": [],
        "limit_down_count": 0,
        "limit_down_stocks": [],
        "market_overview": get_market_overview(),
        "concepts": get_concept_boards()
    }
    
    # 获取涨停数据
    up_count, up_stocks = get_limit_up_stocks()
    data["limit_up_count"] = up_count
    data["limit_up_stocks"] = up_stocks
    
    # 获取跌停数据
    down_count, down_stocks = get_limit_down_stocks()
    data["limit_down_count"] = down_count
    data["limit_down_stocks"] = down_stocks
    
    # 生成报告
    print()
    print("📝 正在生成报告...")
    report = generate_report(data)
    
    # 保存报告
    output_file = "/tmp/a-share-daily-report.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print()
    print("=" * 80)
    print(f"✅ 报告生成完成！")
    print(f"📄 报告文件: {output_file}")
    print("=" * 80)
    
    # 同时保存JSON数据
    json_file = "/tmp/a-share-data.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 JSON数据: {json_file}")

if __name__ == "__main__":
    main()