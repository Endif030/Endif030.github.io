# 论文阅读助手 - 维护者文档

> 定时任务维护、故障排查、日常维护指南
> 
> **更新 v2.1**: 每周初始化已合并（收集论文+生成周文档+前3篇注释稿）

---

## 📋 每日检查清单（建议）

```bash
python scripts/health_check.py
python scripts/health_check.py --check-flashcards
```

---

## 🔧 定时任务配置

| 任务 | 频率 | 时间 | 脚本 |
|------|------|------|------|
| **每周初始化** ⭐ | 每周一 09:00 | 收集论文+生成周文档+前3篇注释稿 | `weekly_init.sh` |
| 知识卡片推送 | 每日 | 08:30/12:00/16:00/20:00 | `flashcard_push.sh` |
| 月报生成 | 每月1日 | 21:00 | `monthly_report.sh` |

### 查看/恢复 crontab

```bash
crontab -l | grep "论文助手"
crontab cron_jobs/crontab_config.txt  # 恢复
```

---

## 🚨 故障排查

### 周一未收到周初始化消息

```bash
# 1. 检查日志
tail -100 /tmp/weekly-init.log

# 2. 检查 crontab
crontab -l | grep weekly_init

# 3. 手动测试
bash cron_jobs/weekly_init.sh

# 4. 快速修复
crontab cron_jobs/crontab_config.txt
chmod +x cron_jobs/weekly_init.sh scripts/weekly_init.py
```

### 知识卡片未推送

```bash
tail -50 /tmp/flashcard-push.log
python scripts/health_check.py --check-flashcards
bash cron_jobs/flashcard_push.sh 08:30
```

---

## 💾 数据备份

```bash
cp -r data data_backup_$(date +%Y%m%d)
git add data/ && git commit -m "backup: $(date +%Y-%m-%d)"
```

---

*最后更新: 2026-03-26 | 版本: 2.1*
