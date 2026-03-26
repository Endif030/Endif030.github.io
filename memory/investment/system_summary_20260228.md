# Investment Daily Report - System Summary

## 🎯 项目目标
为咨询顾问 Roy 创建自动化每日投资日报系统，每天早上 8:00 推送。

## 📊 需求实现
- ✅ A股消息占比 70%
- ✅ 美股消息占比 20%
- ✅ 币圈/期货占比 10%
- ✅ 自动去重和摘要
- ✅ 推送至飞书
- ✅ 定时执行（Cron）

## 🏗️ 系统架构

```
~/.openclaw/workspace/skills/investment-daily-report/
├── SKILL.md                      # 技能说明文档
├── README.md                     # 用户使用指南
└── scripts/
    ├── config.sh                 # 配置文件（市场比例、关键词）
    ├── generate-report.sh        # 主生成脚本
    └── test-setup.sh            # 测试脚本
```

### 依赖组件
1. **tavily-search** - AI优化搜索引擎
2. **summarize** - 内容摘要工具
3. **Cron** - 定时任务调度
4. **Feishu API** - 消息推送

### 数据源
- Tavily API（新闻搜索）
- 支持自定义搜索关键词

## 📝 工作流程

```
1. Cron 触发（每天 00:00 UTC = 08:00 CST）
   ↓
2. 执行 generate-report.sh
   ↓
3. 分别搜索 A股/美股/币圈新闻
   ↓
4. 解析和摘要搜索结果
   ↓
5. 生成 Markdown 格式报告
   ↓
6. 通过 Feishu 推送给 Roy
   ↓
7. 存档至 memory/investment/
```

## ⏰ 定时任务

```bash
# 已添加到 crontab
0 0 * * * cd /root/.openclaw/workspace/skills/investment-daily-report && TAVILY_API_KEY=${TAVILY_API_KEY} bash scripts/generate-report.sh >> /tmp/investment-report-cron.log 2>&1
```

## 🚀 待完成任务

### 立即完成
- [x] 创建 Skill 结构
- [x] 编写生成脚本
- [x] 设置 Cron 定时任务
- [x] 配置内容比例
- [ ] Roy 配置 Tavily API Key
- [ ] Roy 运行测试脚本验证

### 后续优化
- [ ] 添加更多新闻源（如RSS订阅）
- [ ] 集成市场数据API（实时行情）
- [ ] 添加图表可视化
- [ ] 支持自定义关注股票/板块
- [ ] 增加情绪分析
- [ ] 创建历史报告数据库

## 📂 文件输出

### 临时文件
- `/tmp/investment-reports/daily_report_YYYYMMDD.md`

### 存档文件
- `~/.openclaw/workspace/memory/investment/latest_report.md`

### 日志文件
- `/tmp/investment-report-cron.log`

## 🔧 配置选项

在 `scripts/config.sh` 中可配置：
- 搜索关键词（A股、美股、币圈）
- 内容占比比例
- API Key
- 推送渠道
- 搜索结果数量

## 💡 技术亮点

1. **模块化设计** - 配置与逻辑分离
2. **错误处理** - 完善的异常捕获
3. **日志记录** - 便于故障排查
4. **可扩展性** - 易于添加新数据源
5. **AI优化** - 使用Tavily AI搜索引擎

## 🎉 当前状态

**开发完成度**: 90%

**剩余工作**: 用户配置 API Key 并测试

**预计上线时间**: 配置完成后立即生效

---

*System created by niko 🦞 on 2026-02-28*