# 论文阅读助手 - 维护者文档

> 定时任务维护、故障排查、日常维护指南

---

## 📋 每日检查清单（建议）

每天早上检查一次，确保系统正常运行：

```bash
# 快速健康检查
python scripts/health_check.py

# 检查今日待复习卡片
python scripts/health_check.py --check-flashcards
```

**期望输出**:
- ✅ 所有数据源正常
- ✅ 今日待复习: N 张（N > 0 表示有卡片需要推送）

---

## 🔧 定时任务管理

### 当前定时任务配置

所有定时任务使用 **系统 crontab** 实现（稳定可靠）：

| 任务 | 频率 | 时间 | 脚本 |
|------|------|------|------|
| 论文收集 | 每周一 | 09:00 | `cron_jobs/paper_fetch_weekly.sh` |
| 知识卡片推送 | 每日 | 08:30 | `cron_jobs/flashcard_push.sh 08:30` |
| 知识卡片推送 | 每日 | 12:00 | `cron_jobs/flashcard_push.sh 12:00` |
| 知识卡片推送 | 每日 | 16:00 | `cron_jobs/flashcard_push.sh 16:00` |
| 知识卡片推送 | 每日 | 20:00 | `cron_jobs/flashcard_push.sh 20:00` |
| 月报生成 | 每月1日 | 21:00 | `cron_jobs/monthly_report.sh` |

### 查看当前 crontab

```bash
crontab -l | grep "论文助手"
```

### 备份 crontab

```bash
# 备份到文件
crontab -l > cron_jobs/crontab_backup_$(date +%Y%m%d).txt

# 或查看现有备份
ls -la cron_jobs/crontab_*
```

### 恢复 crontab

```bash
# 从配置文件恢复
crontab cron_jobs/crontab_config.txt

# 验证
 crontab -l | grep "论文助手"
```

### 编辑 crontab

```bash
# 编辑当前用户的 crontab
crontab -e

# 或修改配置文件后重新加载
vim cron_jobs/crontab_config.txt
crontab cron_jobs/crontab_config.txt
```

---

## 🚨 故障排查指南

### 问题1: 到点未收到知识卡片推送

**症状**: 08:30/12:00/16:00/20:00 没有收到推送消息

**排查步骤**:

1. **检查日志**
   ```bash
   tail -50 /tmp/flashcard-push.log
   ```
   
   期望看到:
   ```
   [时间] 开始推送知识卡片 [08:30]...
   [时间] 消息内容生成成功
   [时间] 消息发送成功 [08:30]
   ```

2. **检查 crontab 配置**
   ```bash
   crontab -l | grep flashcard
   ```
   
   期望输出包含:
   ```
   30 8 * * * export PATH="..." && .../flashcard_push.sh 08:30
   ```

3. **手动测试推送**
   ```bash
   bash cron_jobs/flashcard_push.sh 08:30
   ```
   
   观察输出是否成功

4. **检查 PATH 配置**
   ```bash
   which openclaw
   which python3
   ```
   
   确保 `openclaw` 和 `python3` 在 PATH 中

**常见原因及修复**:

| 原因 | 症状 | 修复 |
|------|------|------|
| crontab PATH 未设置 | 日志显示 "command not found" | 确保 crontab 中有 `export PATH=...` |
| openclaw 不在 PATH | 日志显示 "openclaw: not found" | 使用绝对路径或正确设置 PATH |
| 无待复习卡片 | 日志显示 "消息生成失败或为空" | 检查 flashcards.json 是否有今日应复习卡片 |
| 授权失效 | 日志显示发送失败 | 重新授权飞书 OAuth |

**快速修复命令**:
```bash
# 1. 检查今日应复习卡片
python scripts/health_check.py --check-flashcards

# 2. 手动执行一次推送
bash cron_jobs/flashcard_push.sh 08:30

# 3. 如果失败，检查 openclaw
which openclaw
ls -la /root/.local/share/pnpm/openclaw

# 4. 重新导入 crontab
crontab cron_jobs/crontab_config.txt
```

---

### 问题2: 论文收集任务失败

**症状**: 周一 09:00 未收到"本周论文收集完成"消息

**排查步骤**:

1. **检查日志**
   ```bash
   tail -50 /tmp/paper-fetch.log
   ```

2. **手动执行收集**
   ```bash
   python scripts/fetch_papers.py --discipline all --max-results 10
   ```

3. **检查数据源连通性**
   ```bash
   python scripts/health_check.py --check-sources
   ```

**常见原因**:
- arXiv API 临时不可用
- Semantic Scholar 速率限制（429 错误）
- 网络连接问题

---

### 问题3: 注释稿生成失败

**症状**: 执行生成脚本后无输出或报错

**排查步骤**:

1. **检查 PDF 是否存在**
   ```bash
   ls papers/ai/<arxiv_id>.pdf
   ```

2. **检查 PDF 可解析性**
   ```bash
   file papers/ai/<arxiv_id>.pdf
   ```

3. **手动执行生成**
   ```bash
   python scripts/generate_annotation.py --paper-id <arxiv_id> 2>&1
   ```

---

### 问题4: 飞书文档创建失败

**症状**: 无法创建或更新飞书文档

**排查步骤**:

1. **检查授权状态**
   ```bash
   # 尝试创建一个测试文档
   # 使用 feishu_create_doc 工具
   ```

2. **检查内容长度**
   - 单次内容 ≤2000 字符
   - 超长内容需分批上传

3. **使用分批策略**
   ```python
   # 先生成本地文件
   # 再分批 append 到飞书文档
   ```

---

## 🔍 日志文件位置

| 日志文件 | 路径 | 说明 |
|---------|------|------|
| 知识卡片推送 | `/tmp/flashcard-push.log` | 每次推送的详细日志 |
| 论文收集 | `/tmp/paper-fetch.log` | 论文收集任务日志 |
| 月报生成 | `/tmp/monthly-report.log` | 月报生成日志 |
| Cron 错误 | `/var/log/cron` (root) | 系统 cron 错误 |

**查看日志技巧**:
```bash
# 实时查看推送日志
tail -f /tmp/flashcard-push.log

# 查看最近 100 行
tail -100 /tmp/flashcard-push.log

# 搜索错误
grep "FAIL\|错误\|Error" /tmp/flashcard-push.log
```

---

## 💾 数据备份

### 自动备份

数据文件已纳入 git 版本控制，提交即备份：
```bash
git add data/
git commit -m "backup: $(date +%Y-%m-%d)"
```

### 手动备份

```bash
# 备份数据目录
cp -r data data_backup_$(date +%Y%m%d)

# 备份特定文件
cp data/papers.json data/archive/papers_$(date +%Y%m%d).json
cp data/flashcards.json data/archive/flashcards_$(date +%Y%m%d).json
```

### 恢复备份

```bash
# 从 git 恢复
git checkout data/papers.json

# 从备份文件恢复
cp data/archive/papers_20260326.json data/papers.json
```

---

## 🔄 周维护流程（每周日执行）

```bash
# 1. 完整健康检查
python scripts/health_check.py --weekly-check

# 2. 归档本周数据
cp data/papers.json data/archive/papers_$(date +%Y%m%d).json

# 3. 提交所有变更
git add .
git commit -m "weekly: complete week of $(date +%Y-%m-%d)"

# 4. 检查下周定时任务
crontab -l | grep "论文助手"
```

---

## 📝 重要文件说明

| 文件 | 作用 | 修改建议 |
|------|------|---------|
| `SKILL.md` | 使用文档 | 随功能更新同步修改 |
| `MAINTENANCE.md` | 本文档 | 记录新的故障和解决方案 |
| `scripts/health_check.py` | 健康检查 | 根据需要添加新检查项 |
| `scripts/quality_check.py` | 质量检查 | 根据格式规范调整检查规则 |
| `cron_jobs/crontab_config.txt` | 定时任务配置 | 修改后需重新导入 crontab |

---

## 🆘 紧急恢复

如果系统完全失效，按以下步骤恢复：

1. **恢复数据**
   ```bash
   # 从最近的备份恢复
   cp data/archive/papers_YYYYMMDD.json data/papers.json
   ```

2. **恢复定时任务**
   ```bash
   crontab cron_jobs/crontab_config.txt
   ```

3. **验证环境**
   ```bash
   python scripts/health_check.py
   ```

4. **手动执行一次完整流程**
   ```bash
   python scripts/fetch_papers.py --discipline ai --max-results 3
   bash cron_jobs/flashcard_push.sh 08:30
   ```

---

## 📞 获取帮助

如果以上步骤无法解决问题：

1. 收集以下信息：
   - 相关日志文件（`/tmp/flashcard-push.log` 等）
   - 执行的命令和输出
   - 错误提示截图

2. 检查 SKILL.md 的"故障排查"章节

3. 查看 git 历史是否有最近变更导致问题

---

*最后更新: 2026-03-26*
