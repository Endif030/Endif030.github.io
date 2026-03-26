#!/usr/bin/env python3

"""
Tushare数据源测试
验证是否能稳定获取A股指数和市场数据
"""

import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

try:
    import tushare as ts
    print(f"✅ Tushare 加载成功")
except ImportError:
    print("❌ Tushare未安装")
    sys.exit(1)

# 需要设置Token（免费注册用户可获得）
# 这里先测试不需要Token的接口
test_mode = "no_token"

def test_index_data():
    """测试指数数据获取"""
    print("📊 测试1：获取上证指数日线数据")
    
    try:
        # Tushare的指数接口
        import tushare as ts
        df = ts.get_k_data(code='sh', start='2026-02-20', end='2026-02-28', ktype='D', index=True)
        if df is not None and not df.empty:
            print(f"✅ 上证指数数据获取成功，共{len(df)}条记录")
            print(df.tail(3))
        else:
            print("⚠️  上证指数数据为空")
    except Exception as e:
        print(f"❌ 上证指数获取失败: {e}")
        
        # 尝试备用方法
        print("🔍 尝试备用方法获取指数数据...")
        try:
            # 使用新浪财经接口（tushare内置）
            df = ts.get_k_data('000001', index=True, start='2026-02-20', end='2026-02-28')
            if df is not None and not df.empty:
                print(f"✅ 备用方法成功，共{len(df)}条记录")
                print(df.tail(3))
            else:
                print("⚠️  备用方法也失败")
        except Exception as e2:
            print(f"❌ 备用方法失败: {e2}")
    
    print()

def test_gem_data():
    """测试创业板数据"""
    print("📊 测试2：获取创业板指数据")
    
    try:
        import tushare as ts
        df = ts.get_k_data(code='cyb', start='2026-02-20', end='2026-02-28', ktype='D', index=True)
        if df is not None and not df.empty:
            print(f"✅ 创业板指数据获取成功")
            print(f"最新数据：{df.iloc[-1]['close']:.2f}")
        else:
            print("⚠️  创业板指数据为空")
    except Exception as e:
        print(f"❌ 创业板指获取失败: {e}")
    
    print()

def test_realtime_quotes():
    """测试实时行情"""
    print("📊 测试3：获取实时行情")
    
    try:
        import tushare as ts
        quotes = ts.get_realtime_quotes(['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb'])
        
        if quotes is not None and not quotes.empty:
            print(f"✅ 实时行情获取成功，共{len(quotes)}个指数")
            for _, quote in quotes.iterrows():
                change = float(quote['change'])
                change_pct = float(quote['change_percent'])
                print(f"  {quote['name']}: {quote['price']} ({change:+.2f}, {change_pct:+.2f}%)")
        else:
            print("⚠️  实时行情数据为空")
    except Exception as e:
        print(f"❌ 实时行情获取失败: {e}")
    
    print()

def test_today_all():
    """测试当日全市场数据"""
    print("📊 测试4：获取当日全市场数据")
    
    try:
        import tushare as ts
        df = ts.get_today_all()
        
        if df is not None and not df.empty:
            print(f"✅ 当日全市场数据获取成功，共{len(df)}只股票")
            
            # 统计涨跌停
            up_limit = len(df[df['changepercent'] >= 9.9])
            down_limit = len(df[df['changepercent'] <= -9.9])
            
            print(f"  涨停: {up_limit}只，跌停: {down_limit}只")
            print(f"  上涨: {len(df[df['changepercent'] > 0])}只")
            print(f"  下跌: {len(df[df['changepercent'] < 0])}只")
        else:
            print("⚠️  当日市场数据为空")
    except Exception as e:
        print(f"❌ 当日市场数据获取失败: {e}")
    
    print()

def main():
    print("=" * 60)
    print("Tushare数据源测试")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    if test_mode == "no_token":
        print("⚠️  当前测试不需要Token的接口")
        print("   如果需要更完整功能，请在tushare.pro注册获取Token")
        print()
    
    try:
        # 测试各个数据源
        test_index_data()
        test_gem_data()
        test_realtime_quotes()
        test_today_all()
        
        print("=" * 60)
        print("✅ Tushare测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()