#!/usr/bin/env python3

"""
东方财富API数据收集脚本 - 稳定版
使用AKShare的东方财富接口获取A股数据
"""

import sys
import json
import time
from datetime import datetime

# 设置UTF-8输出
sys.stdout.reconfigure(encoding='utf-8')

try:
    import akshare as ak
    print(f"✅ AKShare 加载成功，版本: {ak.__version__}")
except ImportError:
    print("❌ AKShare未安装")
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("❌ pandas未安装")
    sys.exit(1)

def safe_get_data(func, *args, **kwargs):
    """安全获取数据，带重试机制"""
    max_retries = 3
    for i in range(max_retries):
        try:
            data = func(*args, **kwargs)
            if data is not None and not data.empty:
                return data
            print(f"⚠️  第{i+1}次尝试返回空数据")
        except Exception as e:
            print(f"⚠️  第{i+1}次尝试失败: {e}")
            if i < max_retries - 1:
                time.sleep(2)  # 等待2秒后重试
    return None

def get_index_data():
    """获取主要指数数据"""
    print("📊 正在获取指数数据...")
    
    # 主要指数代码映射
    index_map = {
        "上证指数": "sh000001",
        "深证成指": "sz399001", 
        "创业板指": "sz399006",
        "科创50": "sh000688",
        "沪深300": "sh000300",
        "中证500": "sh000905",
        "上证50": "sh000016"
    }
    
    result = {}
    
    # 使用东方财富的指数实时接口
    index_data = safe_get_data(ak.stock_zh_index_spot_em)
    
    if index_data is None:
        print("❌ 指数数据获取失败")
        return result
    
    # 过滤需要的指数
    for name, code in index_map.items():
        try:
            # 查找对应代码的指数
            idx_row = index_data[index_data['代码'] == code]
            if not idx_row.empty:
                row = idx_row.iloc[0]
                result[name] = {
                    "code": code,
                    "current": round(float(row['最新价']), 2),
                    "change": round(float(row['涨跌幅']), 2),
                    "volume": int(row['成交量']) if pd.notna(row['成交量']) else 0,
                    "amount": int(row['成交额']) if pd.notna(row['成交额']) else 0,
                    "open": round(float(row['开盘价']), 2) if pd.notna(row['开盘价']) else 0,
                    "high": round(float(row['最高价']), 2) if pd.notna(row['最高价']) else 0,
                    "low": round(float(row['最低价']), 2) if pd.notna(row['最低价']) else 0
                }
                print(f"  ✅ {name}: {result[name]['current']} ({result[name]['change']:+}%)")
            else:
                print(f"  ⚠️  {name}({code}) 未找到")
        except Exception as e:
            print(f"  ⚠️  {name} 处理失败: {e}")
    
    return result

def get_market_stats():
    """获取市场统计"""
    print("\n📈 正在获取市场统计...")
    
    stats = {
        "total_stocks": 0,
        "up_count": 0,
        "down_count": 0,
        "flat_count": 0,
        "limit_up": 0,
        "limit_down": 0,
        "total_volume": 0,
        "total_amount": 0
    }
    
    # 获取全市场股票数据
    market_data = safe_get_data(ak.stock_zh_a_spot_em)
    
    if market_data is None:
        print("❌ 市场统计数据获取失败")
        return stats
    
    try:
        # 确保需要的列存在
        required_columns = ['代码', '名称', '涨跌幅', '成交量', '成交额']
        for col in required_columns:
            if col not in market_data.columns:
                print(f"⚠️  缺少必要列: {col}")
                return stats
        
        # 统计数据
        stats["total_stocks"] = len(market_data)
        stats["up_count"] = len(market_data[market_data['涨跌幅'] > 0])
        stats["down_count"] = len(market_data[market_data['涨跌幅'] < 0])
        stats["flat_count"] = len(market_data[abs(market_data['涨跌幅']) < 0.001])
        
        # 涨跌停统计（涨跌幅超过9.9%）
        stats["limit_up"] = len(market_data[market_data['涨跌幅'] >= 9.9])
        stats["limit_down"] = len(market_data[market_data['涨跌幅'] <= -9.9])
        
        # 总成交量和成交额
        stats["total_volume"] = int(market_data['成交量'].sum())
        stats["total_amount"] = int(market_data['成交额'].sum())
        
        print(f"  ✅ 总股票: {stats['total_stocks']:,}")
        print(f"  ✅ 上涨: {stats['up_count']:,}, 下跌: {stats['down_count']:,}, 平盘: {stats['flat_count']:,}")
        print(f"  ✅ 涨停: {stats['limit_up']}, 跌停: {stats['limit_down']}")
        print(f"  ✅ 总成交额: {stats['total_amount']:,} 元")
        
    except Exception as e:
        print(f"❌ 统计数据处理失败: {e}")
    
    return stats

def get_limit_up_stocks():
    """获取涨停股票"""
    print("\n🚀 正在获取涨停股票...")
    
    limit_up_list = []
    
    # 获取当日涨停数据
    today = datetime.now().strftime("%Y%m%d")
    zt_data = safe_get_data(ak.stock_zt_pool_em, date=today)
    
    if zt_data is None or zt_data.empty:
        print("⚠️  涨停数据获取失败或为空")
        return 0, limit_up_list
    
    try:
        limit_up_count = len(zt_data)
        print(f"  ✅ 涨停数量: {limit_up_count}")
        
        # 提取详细信息
        count = 0
        for _, stock in zt_data.iterrows():
            if count >= 50:  # 限制只取前50只
                break
            
            try:
                limit_up_list.append({
                    "code": str(stock.get('代码', '')).strip(),
                    "name": str(stock.get('名称', '')).strip(),
                    "change": round(float(stock.get('涨跌幅', 0)), 2),
                    "volume": int(stock.get('成交额', 0)),
                    "first_limit_time": str(stock.get('首次涨停时间', 'N/A')).strip(),
                    "last_limit_time": str(stock.get('最后涨停时间', 'N/A')).strip(),
                    "open_times": int(stock.get('开板次数', 0)),
                    "limit_type": "一字板" if str(stock.get('涨停统计', '')).count('1') == 1 else "涨停"
                })
                count += 1
            except Exception as e:
                print(f"    ⚠️  处理股票数据失败: {e}")
                continue
        
        print(f"  ✅ 成功提取 {len(limit_up_list)} 只涨停股详细信息")
        
    except Exception as e:
        print(f"❌ 涨停数据处理失败: {e}")
        return 0, limit_up_list
    
    return limit_up_count, limit_up_list

def get_top_concepts():
    """获取热门概念板块"""
    print("\n🔥 正在获取热门概念板块...")
    
    try:
        # 获取概念板块数据
        concept_data = safe_get_data(ak.stock_board_concept_name_em)
        
        if concept_data is None or concept_data.empty:
            print("⚠️  概念板块数据获取失败")
            return None
        
        # 确保涨跌幅列存在且为数值类型
        if '涨跌幅' not in concept_data.columns:
            print("⚠️  概念板块数据缺少'涨跌幅'列")
            return None
        
        concept_data['涨跌幅'] = pd.to_numeric(concept_data['涨跌幅'], errors='coerce')
        concept_data = concept_data.dropna(subset=['涨跌幅'])
        
        if concept_data.empty:
            print("⚠️  概念板块数据为空")
            return None
        
        # 排序并取前5和后5
        sorted_data = concept_data.sort_values('涨跌幅', ascending=False)
        top_5 = sorted_data.head(5)
        bottom_5 = sorted_data.tail(5)
        
        result = {
            "top_5": [],
            "bottom_5": []
        }
        
        # 处理涨幅前5
        for _, concept in top_5.iterrows():
            try:
                result["top_5"].append({
                    "name": str(concept.get('板块名称', '')).strip(),
                    "change": round(float(concept.get('涨跌幅', 0)), 2),
                    "volume": int(concept.get('成交额', 0)) if pd.notna(concept.get('成交额')) else 0
                })
            except Exception as e:
                print(f"    ⚠️  处理概念板块失败: {e}")
                continue
        
        # 处理跌幅前5
        for _, concept in bottom_5.iterrows():
            try:
                result["bottom_5"].append({
                    "name": str(concept.get('板块名称', '')).strip(),
                    "change": round(float(concept.get('涨跌幅', 0)), 2),
                    "volume": int(concept.get('成交额', 0)) if pd.notna(concept.get('成交额')) else 0
                })
            except Exception as e:
                print(f"    ⚠️  处理概念板块失败: {e}")
                continue
        
        print(f"  ✅ 概念板块: 涨幅前{len(result['top_5'])}, 跌幅前{len(result['bottom_5'])}")
        
        return result
        
    except Exception as e:
        print(f"❌ 概念板块处理失败: {e}")
        return None

def generate_markdown_report(data):
    """生成Markdown报告"""
    
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    report = f"# 📊 A股市场日报\n\n"
    report += f"*生成时间: {now} | 中国标准时间*\n\n"
    report += f"---\n\n"
    
    # 市场指数
    if data.get('indices'):
        report += f"## 📈 主要指数\n\n"
        report += f"| 指数名称 | 当前点位 | 涨跌幅 | 成交额(亿) | 最高 | 最低 |\n"
        report += f"|----------|----------|--------|------------|------|------|\n"
        
        for name, idx_data in data['indices'].items():
            amount_yi = idx_data['amount'] / 100000000 if idx_data['amount'] > 0 else 0
            report += f"| {name} | {idx_data['current']} | {idx_data['change']:+}% | {amount_yi:.2f} | {idx_data['high']} | {idx_data['low']} |\n"
        
        report += f"\n"
    
    # 市场统计
    stats = data.get('stats', {})
    report += f"## 📊 市场统计\n\n"
    report += f"- **总股票数**: {stats.get('total_stocks', 0):,}\n"
    report += f"- **上涨**: {stats.get('up_count', 0):,}\n"
    report += f"- **下跌**: {stats.get('down_count', 0):,}\n"
    report += f"- **平盘**: {stats.get('flat_count', 0):,}\n"
    report += f"- **涨停**: {stats.get('limit_up', 0)}\n"
    report += f"- **跌停**: {stats.get('limit_down', 0)}\n"
    report += f"- **总成交额**: {stats.get('total_amount', 0):,} 元\n\n"
    
    report += f"---\n\n"
    
    # 涨停统计
    limit_up_stocks = data.get('limit_up_stocks', [])
    if limit_up_stocks:
        report += f"## 🚀 涨停统计\n\n"
        report += f"**今日涨停**: {data.get('limit_up_count', 0)} 只\n\n"
        report += f"| 代码 | 名称 | 涨幅 | 开板次数 | 涨停时间 |\n"
        report += f"|------|------|------|----------|----------|\n"
        
        for stock in limit_up_stocks[:20]:  # 只显示前20只
            report += f"| {stock['code']} | {stock['name']} | {stock['change']:+}% | {stock['open_times']} | {stock['first_limit_time']} |\n"
        
        if data.get('limit_up_count', 0) > 20:
            report += f"| ... | 还有 {data['limit_up_count'] - 20} 只 | - | - | - |\n"
        
        report += f"\n"
    
    report += f"---\n\n"
    
    # 概念板块
    concepts = data.get('concepts')
    if concepts:
        report += f"## 🔥 概念板块\n\n"
        
        # 涨幅前5
        report += f"### 📈 涨幅前5\n\n"
        report += f"| 板块名称 | 涨跌幅 | 成交额(亿) |\n"
        report += f"|----------|--------|------------|\n"
        
        for concept in concepts.get('top_5', []):
            volume_yi = concept['volume'] / 100000000 if concept['volume'] > 0 else 0
            report += f"| {concept['name']} | {concept['change']:+}% | {volume_yi:.2f} |\n"
        
        report += f"\n### 📉 跌幅前5\n\n"
        report += f"| 板块名称 | 涨跌幅 | 成交额(亿) |\n"
        report += f"|----------|--------|------------|\n"
        
        for concept in concepts.get('bottom_5', []):
            volume_yi = concept['volume'] / 100000000 if concept['volume'] > 0 else 0
            report += f"| {concept['name']} | {concept['change']:+}% | {volume_yi:.2f} |\n"
        
        report += f"\n"
    
    report += f"---\n\n"
    report += f"*数据来源: 东方财富(通过AKShare) | 更新时间: {now}*\n"
    
    return report

def main():
    """主函数"""
    
    print("=" * 80)
    print("📈 A股市场日报数据收集系统 - 东方财富API版")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    try:
        # 收集数据
        data = {
            "timestamp": datetime.now().isoformat(),
            "indices": get_index_data(),
            "stats": get_market_stats(),
        }
        
        # 获取涨停数据
        limit_up_count, limit_up_stocks = get_limit_up_stocks()
        data["limit_up_count"] = limit_up_count
        data["limit_up_stocks"] = limit_up_stocks
        
        # 获取概念板块
        data["concepts"] = get_top_concepts()
        
        # 生成报告
        print("\n📝 正在生成Markdown报告...")
        report = generate_markdown_report(data)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"/tmp/a_share_report_{timestamp}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存JSON数据
        json_file = f"/tmp/a_share_data_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 80)
        print(f"✅ 报告生成完成！")
        print(f"📄 Markdown报告: {output_file}")
        print(f"💾 JSON数据: {json_file}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 系统执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()