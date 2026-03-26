#!/bin/bash
# 每日美股&币圈交易行情简报 - 自动任务脚本
# 执行时间: 每天早上 8:00 (北京时间)

# 设置时区为北京时间
export TZ='Asia/Shanghai'

# 飞书配置
export FEISHU_APP_ID="cli_a92826c79ce4dbb6"
export FEISHU_APP_SECRET="FNtwhE9aGa9C4QPclmupPbU4sforEjtS"

# 日志文件
LOG_FILE="/tmp/daily_briefing_$(date +%Y%m%d).log"
BRIEFING_FILE="/tmp/daily_briefing_$(date +%Y%m%d).md"

echo "========================================" >> $LOG_FILE
echo "每日简报生成任务 - $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

cd ~/.openclaw/workspace/skills/investment-daily-report

# 执行Python数据收集脚本
python3 << 'PYEOF'
import requests
import json
from datetime import datetime
import sys

TAVILY_API_KEY = "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"

def tavily_search(query, max_results=6):
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
        return {"error": str(e)}

print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始数据收集...")

# 1. 美股大盘
data = {"timestamp": datetime.now().isoformat(), "sections": {}}
print("[1/5] 美股大盘...")
data["sections"]["us_market"] = tavily_search("US stock market today Dow Jones S&P 500 Nasdaq performance")

# 2. 中概股/中国指数
print("[2/5] 中概股...")
data["sections"]["china_stocks"] = tavily_search("YINN YANG ETF Chinese stocks today Alibaba Baidu performance")

# 3. 币圈
print("[3/5] 币圈...")
data["sections"]["crypto"] = tavily_search("Bitcoin BTC Ethereum ETH price today crypto market news")

# 4. 重点个股
print("[4/5] 重点个股...")
data["sections"]["stocks"] = tavily_search("Tesla TSLA Nvidia NVDA stock today latest news")

# 5. 社交媒体
print("[5/5] 社交媒体...")
data["sections"]["social"] = tavily_search("Elon Musk Donald Trump tweets today market impact")

# 保存数据
output_file = f"/tmp/daily_briefing_data_{datetime.now().strftime('%Y%m%d')}.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[{datetime.now().strftime('%H:%M:%S')}] 数据收集完成: {output_file}")

# 生成简报
briefing = f"""# 📊 每日美股&币圈交易行情简报

*生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}*  
*数据日期: {datetime.now().strftime('%Y-%m-%d')}*  
*数据来源: Tavily AI搜索*

---

## 📈 一、美股市场动态

### 1.1 大盘指数

**市场摘要**:
{data['sections']['us_market'].get('answer', '数据采集中')}

"""

# 添加美股详情
if data['sections']['us_market'].get('results'):
    for i, item in enumerate(data['sections']['us_market']['results'][:3], 1):
        briefing += f"{i}. **{item.get('title', 'N/A')}**\\n"
        content = item.get('content', '')[:100]
        briefing += f"   {content}...\\n\\n"

# 中概股
briefing += """---

### 1.2 中概股及中国指数

**市场摘要**:
"""
briefing += data['sections']['china_stocks'].get('answer', '数据采集中')
briefing += "\\n\\n"

if data['sections']['china_stocks'].get('results'):
    for i, item in enumerate(data['sections']['china_stocks']['results'][:3], 1):
        briefing += f"{i}. **{item.get('title', 'N/A')}**\\n"
        content = item.get('content', '')[:100]
        briefing += f"   {content}...\\n\\n"

# 重点个股
briefing += """---

### 1.3 重点个股

"""
if data['sections']['stocks'].get('results'):
    for i, item in enumerate(data['sections']['stocks']['results'][:3], 1):
        briefing += f"{i}. **{item.get('title', 'N/A')}**\\n"
        content = item.get('content', '')[:100]
        briefing += f"   {content}...\\n\\n"

# 币圈
briefing += """---

## ₿ 二、币圈市场动态

**市场摘要**:
"""
briefing += data['sections']['crypto'].get('answer', '数据采集中')
briefing += "\\n\\n"

if data['sections']['crypto'].get('results'):
    for i, item in enumerate(data['sections']['crypto']['results'][:3], 1):
        briefing += f"{i}. **{item.get('title', 'N/A')}**\\n"
        content = item.get('content', '')[:120]
        briefing += f"   {content}...\\n\\n"

# 社交媒体
briefing += """---

## 🐦 三、社交媒体监控

**市场影响**:
"""
briefing += data['sections']['social'].get('answer', '数据采集中')
briefing += "\\n\\n"

if data['sections']['social'].get('results'):
    for i, item in enumerate(data['sections']['social']['results'][:3], 1):
        briefing += f"{i}. **{item.get('title', 'N/A')}**\\n"
        content = item.get('content', '')[:100]
        briefing += f"   {content}...\\n\\n"

# 结尾
briefing += f"""---

## ⚠️ 风险提示

- 本简报数据来源于AI搜索，仅供参考
- 杠杆ETF风险极高，不适合长期持有
- 社交媒体信息需谨慎验证
- 市场波动剧烈，投资需谨慎

---

*简报生成: niko 🦞*  
*自动任务时间: 每日 08:00 (北京时间)*
"""

# 保存简报
briefing_file = f"/tmp/每日美股币圈简报_{datetime.now().strftime('%Y%m%d')}.md"
with open(briefing_file, "w", encoding="utf-8") as f:
    f.write(briefing)

print(f"[{datetime.now().strftime('%H:%M:%S')}] 简报生成完成: {briefing_file}")
PYEOF

# 记录完成
echo "任务完成: $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG_FILE
echo "简报文件: $BRIEFING_FILE" >> $LOG_FILE

# 推送到飞书
echo "正在推送至飞书..." >> $LOG_FILE
python3 ~/.openclaw/workspace/skills/investment-daily-report/scripts/send_briefing_to_feishu.py $BRIEFING_FILE >> $LOG_FILE 2>&1

echo "========================================" >> $LOG_FILE

