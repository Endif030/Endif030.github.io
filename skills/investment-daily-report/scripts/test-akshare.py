#!/usr/bin/env python3

"""
A股数据获取测试 - AKShare数据源
验证是否能获取精确的A股市场数据
"""

import sys
import json
from datetime import datetime, timedelta

print("🔍 测试AKShare数据源...")
print("=" * 60)

try:
    import akshare as ak
    print("✅ AKShare 安装成功，版本:", ak.__version__)
    print()
    
    # 测试1：获取上证指数实时数据
    print("📊 测试1：获取上证指数实时数据")
    try:
        sh_index = ak.stock_zh_index_spot_em(symbol="sh000001")
        if not sh_index.empty:
            print("✅ 上证指数数据获取成功")
            print(sh_index.head(2))
        else:
            print("⚠️  上证指数数据为空")
    except Exception as e:
        print(f"❌ 上证指数获取失败: {e}")
    
    print()
    
    # 测试2：获取创业板指
    print("📊 测试2：获取创业板指实时数据")
    try:
        cyb_index = ak.stock_zh_index_spot_em(symbol="sz399006")
        if not cyb_index.empty:
            print("✅ 创业板指数据获取成功")
            print(cyb_index.head(2))
        else:
            print("⚠️  创业板指数据为空")
    except Exception as e:
        print(f"❌ 创业板指获取失败: {e}")
    
    print()
    
    # 测试3：获取科创板50
    print("📊 测试3：获取科创板50指数")
    try:
        kcb_index = ak.stock_zh_index_spot_em(symbol="sh000688")
        if not kcb_index.empty:
            print("✅ 科创板50数据获取成功")
            print(kcb_index.head(2))
        else:
            print("⚠️  科创板50数据为空")
    except Exception as e:
        print(f"❌ 科创板50获取失败: {e}")
    
    print()
    
    # 测试4：获取A股市场整体成交量
    print("📊 测试4：获取A股整体成交量")
    try:
        # 获取所有A股数据，然后汇总成交量
        all_stocks = ak.stock_zh_a_spot_em()
        if not all_stocks.empty:
            total_volume = all_stocks['成交额'].sum()
            print(f"✅ A股总成交额获取成功: {total_volume:,.0f} 元")
            print("前5只股票数据:")
            print(all_stocks[['代码', '名称', '成交额', '涨跌幅']].head(5))
        else:
            print("⚠️  A股数据为空")
    except Exception as e:
        print(f"❌ A股数据获取失败: {e}")
    
    print()
    
    # 测试5：获取历史数据（日线）
    print("📊 测试5：获取上证指数历史数据（最近5天）")
    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
        
        sh_hist = ak.stock_zh_index_hist_em(symbol="sh000001", period="daily", start_date=start_date, end_date=end_date)
        
        if not sh_hist.empty:
            print("✅ 上证指数历史数据获取成功")
            print("最近5个交易日:")
            print(sh_hist[['日期', '收盘', '涨跌幅', '成交额']].tail(5))
        else:
            print("⚠️  历史数据为空")
    except Exception as e:
        print(f"❌ 历史数据获取失败: {e}")
    
    print()
    
    # 测试6：获取涨停股票列表
    print("📊 测试6：获取涨停股票列表")
    try:
        from datetime import datetime
        current_time = datetime.now().strftime("%Y%m%d")
        
        # 使用stock_zt_pool_em获取涨停股票
        zt_list = ak.stock_zt_pool_em(date=current_time)
        
        if not zt_list.empty:
            print(f"✅ 涨停股票数据获取成功，共{len(zt_list)}只涨停股")
            print("前10只涨停股票:")
            print(zt_list[['代码', '名称', '涨跌幅', '成交额']].head(10))
        else:
            print("⚠️  涨停股票数据为空（可能当前非交易时段）")
    except Exception as e:
        print(f"❌ 涨停数据获取失败: {e}")
    
    print()
    print("=" * 60)
    print("✅ AKShare数据源测试完成！")
    
except ImportError:
    print("❌ AKShare未安装，请先安装:")
    print("   pip install akshare")
    sys.exit(1)
except Exception as e:
    print(f"❌ 测试失败: {e}")
    sys.exit(1)