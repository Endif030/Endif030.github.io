# 变更日志 (Changelog)

## [2.1.0] - 2026-03-26

### 重大变更
- **合并节点1/2/3**: 每周一自动执行完整初始化流程
  - 新增 `scripts/weekly_init.py`: 合并收集论文+生成周文档+前3篇注释稿
  - 新增 `cron_jobs/weekly_init.sh`: 定时任务脚本
  - 更新 crontab: 用 weekly_init.sh 替换 paper_fetch_weekly.sh
  
- **知识卡片直接显示答案**: 推送消息中直接展示问题和答案，无需点击展开

### 优化
- 简化 SKILL.md 结构，突出新的合并工作流
- 更新 MAINTENANCE.md，添加 weekly_init 故障排查指南

---

## [2.0.0] - 2026-03-26

### 重构
- 基于 Superpowers 方法论重构 SKILL.md
- 引入结构化工作流（Phase 1-8）
- 每个阶段定义明确的 Definition of Done

### 新增
- `scripts/health_check.py` - 健康检查脚本
- `scripts/quality_check.py` - 质量检查脚本
- `MAINTENANCE.md` - 维护者文档
- `CHANGELOG.md` - 版本历史和变更记录

### 修复
- `cron_jobs/flashcard_push.sh` - 修复消息发送逻辑

---

## [1.2.0] - 2026-03-10

### 新增
- 添加工作流程规范章节
- 飞书文档策略更新
- 长任务分阶段汇报机制
- 知识卡片自动生成流程

---

## [1.0.0] - 2026-03-08

### 初始版本
- 论文收集（arXiv + Semantic Scholar）
- PDF 下载
- 注释稿生成
- 知识卡片系统（艾宾浩斯复习）
- 定时推送
- 周报/月报生成
