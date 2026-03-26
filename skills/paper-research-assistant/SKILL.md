---
name: paper-research-assistant
description: |
  跨学科论文追踪与知识管理系统。核心功能包括：
  1. 定期收集AI、心理学、社会科学、人类学、哲学、游戏研究等领域的热门论文
  2. 下载论文PDF并生成逐段中文注释稿（原文+翻译+详细解释）
  3. 从注释内容中提取知识卡片，支持艾宾浩斯遗忘曲线复习
  4. 定时推送知识卡片复习提醒（每日4次）
  5. 生成周/月度阅读报告
  使用场景：用户说"收集本周AI论文"、"帮我下载这篇论文"、"生成注释稿"、"记录这个问题"、"生成周报"等
---

# Paper Research Assistant - 论文拆解与辅助阅读

> **基于 Superpowers 方法论重构 | 版本 2.1**
> 
> 本 Skill 采用系统化工作流，确保论文阅读从收集到知识内化的完整闭环。
> > **更新日志 v2.1**:
> - 合并节点1/2/3：每周一自动收集论文+生成周文档+前3篇注释稿
> - 知识卡片直接显示问题和答案（无需点击展开）

---

## 🚀 快速开始

### 每周一自动启动

每周一 09:00 自动执行：
1. ✅ 收集7篇 AI 领域论文
2. ✅ 下载前3篇 PDF
3. ✅ 生成前3篇注释稿
4. ✅ 创建阅读周飞书文档
5. ✅ 发送飞书消息通知

**用户操作**: 查收飞书消息，点击周文档链接开始阅读

---

## 📋 完整工作流程

### Phase 1: 每周初始化（合并节点 - 自动执行）

**执行时机**: 每周一 09:00（crontab 自动）

**包含任务**:
1. 📥 收集论文（7篇）
2. 📄 下载前3篇 PDF
3. ✍️ 生成前3篇注释稿
4. 📄 创建阅读周飞书文档
5. 📬 发送飞书通知

**Definition of Done**:
- [ ] papers.json 新增 7 条论文记录
- [ ] papers/ai/ 目录下前3篇 PDF 已下载
- [ ] annotations/ai/ 目录下前3篇注释稿已生成
- [ ] 飞书文档 `📚 AI阅读周 - Week of YYYY-MM-DD` 已创建
- [ ] 用户收到飞书消息通知

**用户交互**:
- **输入**: 无需操作（全自动）
- **输出**: 飞书消息
  ```
  📚 AI阅读周已启动 - Week of 2026-03-24
  
  本周已为你准备 7 篇 AI 领域前沿论文：
  #1 BEVLM: Birds Eye View Language Model...
  #2 Fly360: Omnidirectional Obstacle Avoidance...
  #3 SUREON: Surgical Robot...
  ... 还有 4 篇论文
  
  ✅ 已完成：
  • 论文收集 (7 篇)
  • PDF 下载 (前3篇)
  • 注释稿生成 (前3篇)
  
  📄 阅读周文档：[飞书链接]
  
  💡 下一步：
  1. 查看阅读周文档了解本周计划
  2. 点击 arXiv 链接阅读 #1 论文
  3. 读完后告诉我 "已读完 #1" 生成知识卡片
  ```

---

### Phase 2: 阅读论文与查看注释稿（用户主导）

**执行时机**: 周一至周日（用户自主安排）

**Definition of Done**:
- [ ] 用户阅读了论文原文（点击 arXiv 链接）
- [ ] 用户查看了注释稿（点击飞书文档链接）

**用户交互**:
- **输入**: 点击阅读周文档中的链接
  - 📄 arXiv原文: 阅读原文
  - 📝 注释稿详解: 查看逐段注释
- **输出**: 飞书文档（注释稿）
  - 封面信息（标题、作者、arXiv ID、领域）
  - 逐段结构：【原文】+【中文翻译】+【注释解释】
  - 跨学科关联分析

---

### Phase 3: 生成剩余注释稿（按需）

**执行时机**: 用户需要时（#4-7 论文）

**用户输入**:
```
"生成 #4 注释稿"
"为 SUREON 生成注释"
```

**系统处理**:
```bash
python scripts/generate_annotation.py --paper-id 2603.06545
python scripts/quality_check.py --annotation 2603.06545
```

**系统输出**:
- 分阶段进度通知
- 最终输出飞书文档链接

---

### Phase 4: 标记阅读完成（用户触发）

**执行时机**: 用户读完一篇论文后

**触发条件**: 用户告知"已读完 #编号"

**Definition of Done**:
- [ ] papers.json 中标记该论文 `read: true`
- [ ] 自动生成 5-7 张知识卡片
- [ ] 卡片状态为 `active`，启动艾宾浩斯复习计划

**用户输入**:
```
"已读完 #1"
"完成第二篇"
```

**系统输出**:
```
✅ 已记录 BEVLM 阅读完成
📝 正在生成知识卡片...

📚 BEVLM 知识卡片已生成（5张）:
1. BEVLM的核心问题是什么？
2. BEV表示学习是什么？
...

⏰ 复习计划已启动：
- 第1次复习：明天 08:30
- 第2次复习：后天
```

---

### Phase 5: 知识卡片复习（自动推送）

**执行时机**: 每日 08:30/12:00/16:00/20:00（crontab 自动）

**用户输入**: 无需操作

**系统处理**:
```bash
bash cron_jobs/flashcard_push.sh 08:30
```

**系统输出**（直接显示问题和答案）:
```
⏰ 08:30 知识卡片推送
今日共 3 张卡片待复习
========================================

--- 卡片 1/3 ---
🧠 知识卡片复习 [2/6轮]

📄 来源：人工智能

❓ 问题：
什么是BEV表示学习？

💡 答案：
BEV（Bird's Eye View）表示学习是将...

📋 上下文：自动驾驶场景中的3D感知

💾 卡片ID: fc_2603_abc123

========================================
📊 记录复习：回复 review 卡片ID 评分
（1=几乎忘记，5=完全掌握）
```

---

### Phase 6: 周/月报告生成（自动触发）

**周报 - 每周日 21:00**
**月报 - 每月1日 21:00**

---

## 📁 目录结构

```
paper-research-assistant/
├── SKILL.md                    # 本文件
├── MAINTENANCE.md              # 维护者文档
├── CHANGELOG.md                # 变更日志
├── data/
│   ├── papers.json             # 论文数据库
│   ├── flashcards.json         # 知识卡片
│   └── review_schedule.json    # 复习计划
├── papers/                     # PDF 存储
├── annotations/                # 注释稿
├── scripts/
│   ├── fetch_papers.py         # 论文收集
│   ├── download_paper.py       # PDF下载
│   ├── generate_annotation.py  # 注释稿生成
│   ├── create_flashcard.py     # 知识卡片
│   ├── spaced_repetition_v2.py # 复习推送
│   ├── weekly_init.py          # 每周初始化 ⭐
│   ├── quality_check.py        # 质量检查
│   └── health_check.py         # 健康检查
├── cron_jobs/
│   ├── weekly_init.sh          # 每周初始化 ⭐
│   ├── flashcard_push.sh       # 知识卡片推送
│   └── monthly_report.sh       # 月报生成
└── references/
    └── disciplines.md          # 学科配置
```

---

## 📝 注释稿格式规范

```markdown
## 封面信息

**标题**: [论文标题]
**arXiv ID**: [ID]
**领域**: [学科]

---

## 摘要

**【原文】**
英文段落...

**【中文翻译】**
中文翻译...

**【注释解释】**
- **术语解释**: [定义]
- **背景知识**: [补充]
```

---

## 🔧 故障排查

### 周一未收到周初始化消息
```bash
tail -50 /tmp/weekly-init.log
crontab -l | grep weekly_init
bash cron_jobs/weekly_init.sh
```

### 知识卡片未推送
```bash
tail -50 /tmp/flashcard-push.log
python scripts/health_check.py --check-flashcards
bash cron_jobs/flashcard_push.sh 08:30
```

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1 | 2026-03-26 | 合并节点1/2/3；知识卡片直接显示答案 |
| 2.0 | 2026-03-26 | 基于 Superpowers 方法论重构 |
| 1.2 | 2026-03-10 | 添加工作流程规范 |
| 1.0 | 2026-03-09 | 初始版本 |

---

*最后更新: 2026-03-26 | 版本: 2.1*
