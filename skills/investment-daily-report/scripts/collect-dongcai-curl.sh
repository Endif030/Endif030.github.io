#!/bin/bash

# 东方财富数据收集 - 使用curl
# 使用命令行curl绕过Python请求限制

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="/tmp/dongcai_data"
mkdir -p "$OUTPUT_DIR"

# 设置请求头
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# 指数列表
INDICES=(
    "sh000001|上证指数"
    "sz399001|深证成指"
    "sz399006|创业板指"
    "sh000688|科创50"
    "sh000300|沪深300"
)

echo "📊 开始收集东方财富数据..."
echo "===================================="

# 1. 获取指数数据
echo "📈 获取指数数据..."
curl -s "https://push2.eastmoney.com/api/qt/stock/get?ut=bd1d9ddb04089700cf99c526de20d9f4&fltt=2&invt=2&dect=1&secids=1.sh000001,0.sz399001,0.sz399006,1.sh000688,1.sh000300" \
    -H "User-Agent: $USER_AGENT" \
    -o "$OUTPUT_DIR/indices.json"

if [ -f "$OUTPUT_DIR/indices.json" ]; then
    echo "✅ 指数数据获取成功"
else
    echo "❌ 指数数据获取失败"
fi

# 2. 获取涨停数据
echo "🚀 获取涨停数据..."
curl -s "https://push2ex.eastmoney.com/getTopicZTPool?cb=&ut=7eea3edcaed734bea9cb4482714ae2&dpt=wz.ztzt&Pageindex=0&Pagesize=100&sort=changepercent&order=desc&date=$(date +%Y%m%d)&_=$(date +%s)000" \
    -H "User-Agent: $USER_AGENT" \
    -o "$OUTPUT_DIR/limit_up.json"

if [ -f "$OUTPUT_DIR/limit_up.json" ]; then
    echo "✅ 涨停数据获取成功"
else
    echo "❌ 涨停数据获取失败"
fi

# 3. 获取概念板块
echo "🔥 获取概念板块..."
curl -s "https://93.push2.eastmoney.com/api/qt/clist/get?cb=&pn=1&pz=200&po=1&np=1&ut=bd1d9ddb04089700cf99c526de20d9f4&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f1,f2,f3,f4,f5,f6,f12,f13,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222&_=$(date +%s)000" \
    -H "User-Agent: $USER_AGENT" \
    -o "$OUTPUT_DIR/concepts.json"

if [ -f "$OUTPUT_DIR/concepts.json" ]; then
    echo "✅ 概念板块数据获取成功"
else
    echo "❌ 概念板块数据获取失败"
fi

# 4. 使用Python解析JSON数据
echo "📝 解析数据并生成报告..."
python3 << 'PYEOF'
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

output_dir = "/tmp/dongcai_data"

# 解析指数数据
try:
    with open(f"{output_dir}/indices.json", 'r', encoding='utf-8') as f:
        indices_raw = f.read()
        # 清理可能的回调函数
        if indices_raw.startswith('(') and indices_raw.endswith(')'):
            indices_raw = indices_raw[1:-1]
        indices_data = json.loads(indices_raw)
    
    print("📈 指数数据解析成功")
    print(f"  数据状态: {indices_data.get('rc')}, 消息: {indices_data.get('msg')}")
    
    if 'data' in indices_data and indices_data['data']:
        print("  指数列表:")
        for item in indices_data['data']:
            name = item.get('n', 'N/A')
            code = item.get('c', 'N/A')
            change = item.get('p', 0)
            print(f"    {name}({code}): {change:+.2f}%")
    
except Exception as e:
    print(f"❌ 指数数据解析失败: {e}")

# 解析涨停数据
try:
    with open(f"{output_dir}/limit_up.json", 'r', encoding='utf-8') as f:
        limit_raw = f.read()
        limit_data = json.loads(limit_raw)
    
    print("\n🚀 涨停数据解析成功")
    print(f"  数据状态: {limit_data.get('rc')}, 消息: {limit_data.get('msg')}")
    
    if 'data' in limit_data and limit_data['data']:
        pool = limit_data['data'].get('pool', [])
        print(f"  涨停数量: {len(pool)}")
        if pool:
            print("  前10只涨停股:")
            for i, stock in enumerate(pool[:10]):
                name = stock.get('n', 'N/A')
                code = stock.get('c', 'N/A')
                change = stock.get('zdp', 0)
                print(f"    {i+1}. {name}({code}): {change:+.2f}%")
    
except Exception as e:
    print(f"❌ 涨停数据解析失败: {e}")

print(f"\n✅ 数据收集完成！时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
PYEOF

echo ""
echo "===================================="
echo "✅ 东方财富数据收集完成！"
echo "数据目录: $OUTPUT_DIR"
echo "===================================="