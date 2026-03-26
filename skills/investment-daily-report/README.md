# Investment Daily Report - Setup Guide

## 📋 系统概述

这是一个自动化的投资日报生成系统，每天早上8点（中国时间）为你推送定制的投资资讯简报。

### 内容占比
- 🇨🇳 **A股消息**: 70%
- 🇺🇸 **美股消息**: 20%
- 🪙 **币圈/期货等其他市场**: 10%

## 🛠️ 安装步骤

### 1. 获取 Tavily API Key

Tavily 是一个AI优化的搜索引擎，用于收集投资资讯。

**步骤：**
- 访问 https://tavily.com
- 注册账户（提供免费额度）
- 在 Dashboard 复制你的 API Key

### 2. 配置环境变量

在你的 shell 配置文件中添加（通常是 `~/.bashrc` 或 `~/.profile`）：

```bash
export TAVILY_API_KEY="your_api_key_here"
```

然后刷新配置：
```bash
source ~/.bashrc
```

### 3. 测试系统

运行测试脚本来检查所有组件：

```bash
cd /root/.openclaw/workspace/skills/investment-daily-report
bash scripts/test-setup.sh
```

这会检查：
- Node.js 是否安装
- Tavily API Key 是否配置
- tavily-search skill 是否可用
- 搜索功能是否正常

## ⏰ 设置定时任务（Cron）

### 手动设置

1. 编辑 crontab：
```bash
crontab -e
```

2. 添加以下行（在中国时区，08:00 = UTC 00:00）：
```bash
0 0 * * * cd /root/.openclaw/workspace/skills/investment-daily-report && bash scripts/generate-report.sh
```

3. 保存并退出

### 验证 Cron 任务

查看已添加的任务：
```bash
crontab -l
```

## 📝 使用方式

### 手动生成报告

随时运行以下命令手动生成投资日报：

```bash
cd /root/.openclaw/workspace/skills/investment-daily-report
bash scripts/generate-report.sh
```

报告将：
- 保存到 `/tmp/investment-reports/`
- 同时推送到你的飞书（Feishu）
- 存档到 `~/.openclaw/workspace/memory/investment/`

### 自定义配置

编辑 `scripts/config.sh` 可调整：
- 搜索关键词
- 结果数量
- 消息推送方式
- 各市场占比（如果需求变化）

## 📊 报告格式

每天推送的简报名括：

1. **📊 市场概览** - 主要指数表现
2. **🇨🇳 A股要闻** (70%) - 政策、资金流向、板块分析
3. **🇺🇸 美股动态** (20%) - 美股走势、经济数据、企业财报
4. **🪙 数字资产与商品** (10%) - 加密货币、商品期货
5. **💡 核心要点** - 可执行的投资洞察摘要

## 🔧 故障排查

### 问题：没有收到日报

**检查项：**
1. Cron 服务是否运行：`systemctl status cron`
2. Tavily API Key 是否有效：运行测试脚本
3. 查看日志：`grep CRON /var/log/syslog`

### 问题：搜索结果太少

**解决方案：**
- 在 `config.sh` 中增加 `SEARCH_RESULTS_PER_MARKET`
- 添加更多相关的搜索关键词
- 检查 Tavily API 的配额使用情况

### 问题：推送失败

**检查项：**
1. 飞书权限是否完整（需要 `contact:contact.base:readonly`）
2. 用户ID是否正确配置
3. 查看错误日志输出

## 📈 高级配置

### 添加更多数据源

在 `config.sh` 的 `*_KEYWORDS` 数组中添加更多搜索关键词，例如：

```bash
A_SHARE_KEYWORDS=(
    "A股 今日要闻"
    "中国股市 政策"
    "沪深300 行情"
    "北上资金 流向"
    "A股 板块分析"
    "证监会 最新消息"
    "科创板 动态"  # 添加更多...
)
```

### 调整内容比例

修改配置中的比例变量（必须总和为100）：

```bash
A_SHARE_RATIO=70
US_STOCK_RATIO=20
CRYPTO_RATIO=10
```

### 修改推送时间

中国的08:00对应UTC时间的00:00。如果要修改推送时间，调整cron表达式：

```bash
# 格式：分 时 日 月 星期
# 例如：每天早上9点（UTC 01:00）
0 1 * * * cd /root/.openclaw/workspace/skills/investment-daily-report && bash scripts/generate-report.sh
```

## 🤝 支持与反馈

如有问题或建议，请联系系统管理员或查看日志文件。

---

*本系统由 niko 🦞 为你定制开发