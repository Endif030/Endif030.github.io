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

> **基于 Superpowers 方法论重构 | 版本 2.0**
> 
> 本 Skill 采用系统化工作流，确保论文阅读从收集到知识内化的完整闭环。

---

## 🚀 快速开始

### 启动本周阅读工作流

```bash
# Step 1: 前置检查
python scripts/health_check.py

# Step 2: 收集论文
python scripts/fetch_papers.py --discipline ai --max-results 7

# Step 3: 下载PDF
python scripts/download_paper.py --discipline ai

# Step 4: 生成阅读周文档（飞书）
# [自动生成并发送链接]
```

---

## 📋 完整工作流程

### Phase 1: 前置检查 (Pre-flight Check)

**执行时机**: 每周工作流启动前、遇到问题时

- [ ] **检查数据源连通性**
  ```bash
  python scripts/health_check.py --check-sources
  ```
  ✅ 期望: arXiv API 返回 200, Semantic Scholar API 返回 200

- [ ] **检查飞书文档权限**
  ```bash
  python scripts/health_check.py --check-feishu
  ```
  ✅ 期望: 可创建测试文档

- [ ] **检查定时任务配置**
  ```bash
  crontab -l | grep "论文助手"
  ```
  ✅ 期望: 显示 4 个任务（收集 + 3个推送时段）

- [ ] **验证环境依赖**
  ```bash
  python scripts/health_check.py --check-deps
  ```
  ✅ 期望: Python 3.x, requests, beautifulsoup4 已安装

---

### Phase 2: 论文收集 (Paper Collection)

**目标**: 每周收集 7-10 篇高质量论文

**执行频率**: 每周一 09:00（通过 crontab 自动）

**Definition of Done**:
- [ ] papers.json 新增 ≥7 条记录
- [ ] 每篇论文包含: title, arxiv_id, authors, abstract, url
- [ ] 学科分布符合配置（默认 AI 为主）

**执行任务**:

- [ ] **Step 1: 按学科收集**
  ```bash
  cd ~/.openclaw/workspace/skills/paper-research-assistant
  python scripts/fetch_papers.py --discipline ai --max-results 7
  ```
  Expected: 输出新增论文数量

- [ ] **Step 2: 验证收集结果**
  ```bash
  python -c "
  import json
  with open('data/papers.json', 'r') as f:
      data = json.load(f)
  new_papers = [p for p in data['papers'] if p.get('collection_date') == '$(date +%Y-%m-%d)']
  print(f'本周新增: {len(new_papers)} 篇')
  assert len(new_papers) >= 7, '论文数量不足'
  "
  ```

- [ ] **Step 3: 创建阅读周文档**
  - 自动生成飞书文档：`📚 AI阅读周 - Week of YYYY-MM-DD`
  - 包含：7篇论文摘要、arXiv 链接、阅读进度追踪

---

### Phase 3: PDF 下载 (Paper Download)

**目标**: 确保所有论文 PDF 本地可访问

**Definition of Done**:
- [ ] papers/ 目录下每个学科有对应 PDF 文件
- [ ] PDF 文件可正常解析（非损坏）
- [ ] 文件大小 > 100KB（排除空文件）

**执行任务**:

- [ ] **Step 1: 批量下载**
  ```bash
  python scripts/download_paper.py --discipline ai
  ```

- [ ] **Step 2: 验证下载完整性**
  ```bash
  python scripts/health_check.py --check-pdfs
  ```
  Expected: 输出 "✅ 所有 PDF 文件正常"

---

### Phase 4: 注释稿生成 (Annotation Generation) ⭐ 核心

**目标**: 为每篇论文生成逐段中文注释稿

**Definition of Done** (每篇论文):
- [ ] 封面信息完整（标题、作者、arXiv ID、领域、项目主页）
- [ ] 包含所有章节（摘要、引言、方法、实验、结论）
- [ ] 每段结构：`【原文】` + `【中文翻译】` + `【注释解释】`
- [ ] 术语解释 ≥ 3 个关键概念
- [ ] 包含跨学科关联分析
- [ ] 飞书文档链接可用
- [ ] 格式规范（【标注】用粗体，非标题；段落间有 `---` 分割线）

**执行任务**（每篇论文）:

- [ ] **Step 1: 解析 PDF 结构**
  ```bash
  python scripts/parse_pdf_structure.py --paper-id <arxiv_id>
  ```
  Output: 章节结构 JSON

- [ ] **Step 2: 生成逐段注释**
  ```bash
  python scripts/generate_annotation.py --paper-id <arxiv_id>
  ```
  Output: `annotations/<discipline>/<arxiv_id>_annotation.md`

- [ ] **Step 3: 质量自检**
  ```bash
  python scripts/quality_check.py --annotation <arxiv_id>
  ```
  Expected: 输出 "✅ 通过 6/6 项检查"

- [ ] **Step 4: 创建飞书文档**
  - 标题格式：`📄 论文标题 (vYYYYMMDD)`
  - 分批上传（每批 ≤2000 字符）

- [ ] **Step 5: 更新阅读周文档链接**
  - 在阅读周文档中标记状态：`📝 注释稿详解: [链接] ✅`

- [ ] **Step 6: 提交本地文件**
  ```bash
  git add annotations/
  git commit -m "annotation: add <paper_title> ($(date +%Y-%m-%d))"
  ```

---

### Phase 5: 知识卡片生成 (Flashcard Creation)

**目标**: 从已读论文提取知识卡片，启动艾宾浩斯复习

**触发条件**: 用户告知"已读完 #编号"

**Definition of Done**:
- [ ] 每篇论文生成 5-7 张卡片
- [ ] 卡片覆盖：核心问题、方法细节、创新点、实验结果、跨学科关联
- [ ] 复习日期按艾宾浩斯曲线设置（1/2/4/7/15/30 天）
- [ ] 卡片状态为 `active`

**执行任务**:

- [ ] **Step 1: 解析注释稿提取关键概念**

- [ ] **Step 2: 生成知识卡片**
  ```bash
  python scripts/create_flashcard.py auto --paper-id <arxiv_id>
  ```

- [ ] **Step 3: 验证卡片状态**
  ```bash
  python scripts/health_check.py --check-flashcards
  ```
  Expected: 输出今日应复习卡片数

---

### Phase 6: 定时复习推送 (Spaced Repetition)

**目标**: 每日 4 次推送知识卡片（08:30/12:00/16:00/20:00）

**实施方案**: 系统 crontab（稳定可靠）

**定时任务配置**:
```bash
# 查看当前配置
crontab -l | grep "论文助手"

# 配置位于
cron_jobs/crontab_config.txt
```

**Definition of Done**:
- [ ] 每日 4 个时段按时推送
- [ ] 每次推送 2-3 张卡片
- [ ] 推送消息格式正确（问题 + 可折叠答案）
- [ ] 无重复推送

**执行任务**:

- [ ] **Step 1: 手动测试推送**
  ```bash
  bash cron_jobs/flashcard_push.sh 08:30
  ```

- [ ] **Step 2: 检查日志**
  ```bash
  tail -20 /tmp/flashcard-push.log
  ```
  Expected: 显示 "消息发送成功"

---

### Phase 7: 周/月报告生成 (Reports)

**周报 - 每周日 21:00**:
- 本周阅读论文数
- 学科分布
- 新增知识卡片数
- 复习完成率
- 下周阅读建议

**月报 - 每月1日 21:00**:
- 月度趋势分析
- 知识图谱可视化
- 研究热点识别

**执行任务**:

- [ ] **生成周报**
  ```bash
  python scripts/generate_report.py --type weekly --save
  ```

- [ ] **生成月报**
  ```bash
  python scripts/generate_report.py --type monthly --save
  ```

---

### Phase 8: 工作流收尾 (Wrap-up)

**执行时机**: 每周日 21:00 后

**Definition of Done**:
- [ ] 本周 7 篇论文注释稿全部完成
- [ ] 所有已读论文知识卡片已生成
- [ ] 定时推送任务正常运行
- [ ] 周报已生成并发送
- [ ] 数据已归档
- [ ] 变更已提交 git

**执行任务**:

- [ ] **Step 1: 验证完成状态**
  ```bash
  python scripts/health_check.py --weekly-check
  ```

- [ ] **Step 2: 归档数据**
  ```bash
  cp data/papers.json data/archive/papers_$(date +%Y%m%d).json
  ```

- [ ] **Step 3: 提交变更**
  ```bash
  git add .
  git commit -m "weekly: complete week of $(date +%Y-%m-%d)"
  ```

---

## 📁 目录结构

```
paper-research-assistant/
├── SKILL.md                    # 本文件
├── MAINTENANCE.md              # 维护者文档
├── data/
│   ├── papers.json             # 论文数据库
│   ├── flashcards.json         # 知识卡片
│   ├── review_schedule.json    # 复习计划
│   └── archive/                # 历史备份
├── papers/                     # PDF 存储
│   ├── ai/
│   ├── psychology/
│   ├── social-science/
│   ├── anthropology/
│   ├── philosophy/
│   └── game-studies/
├── annotations/                # 注释稿
├── reports/                    # 周报/月报
├── scripts/
│   ├── fetch_papers.py         # 论文收集
│   ├── download_paper.py       # PDF下载
│   ├── generate_annotation.py  # 注释稿生成
│   ├── create_flashcard.py     # 知识卡片
│   ├── spaced_repetition_v2.py # 复习推送
│   ├── generate_report.py      # 报告生成
│   ├── quality_check.py        # 质量检查 ⭐ 新增
│   └── health_check.py         # 健康检查 ⭐ 新增
├── cron_jobs/                  # 定时任务脚本
│   ├── crontab_config.txt      # crontab 配置模板
│   ├── flashcard_push.sh       # 知识卡片推送
│   ├── paper_fetch_weekly.sh   # 论文收集
│   └── monthly_report.sh       # 月报生成
└── references/
    └── disciplines.md          # 学科配置
```

---

## 📝 注释稿格式规范

### 正确格式

```markdown
## 封面信息

**标题**: [论文标题]

**arXiv ID**: [ID]

**领域**: [学科]

**项目主页**: [URL]

---

## 摘要

**【原文】**
英文段落...

**【中文翻译】**
中文翻译...

**【注释解释】**
- **术语解释**: [定义]
- **背景知识**: [补充]
- **类比说明**: [类比]
- **技术意义**: [重要性]

---

## 第1节 引言

### 1.1 xxx

**【原文】**
...
```

### ⚠️ 格式禁忌

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| `## 【原文】` (用标题) | `**【原文】**` (用粗体) |
| 段落间无分割线 | 每段后加 `---` |
| 封面信息不换行 | 每项单独一行 |

---

## 🔧 故障排查

### 问题1: 定时任务未推送消息

**症状**: 到点未收到知识卡片推送

**排查步骤**:
1. 检查日志: `tail -20 /tmp/flashcard-push.log`
2. 检查 crontab: `crontab -l | grep flashcard`
3. 手动测试: `bash cron_jobs/flashcard_push.sh 08:30`
4. 检查 PATH: `which openclaw` 应返回路径

**常见原因**:
- crontab 中 PATH 未正确设置
- `openclaw` 命令不在 PATH 中
- Python 依赖缺失

### 问题2: 注释稿生成失败

**症状**: 执行后无输出或报错

**排查步骤**:
1. 检查 PDF 是否存在: `ls papers/ai/<arxiv_id>.pdf`
2. 检查 PDF 可解析性: `python scripts/parse_pdf_structure.py --paper-id <id>`
3. 检查日志输出中的具体错误

### 问题3: 飞书文档创建失败

**症状**: 无法创建或更新文档

**排查步骤**:
1. 检查飞书授权: `python scripts/health_check.py --check-feishu`
2. 检查内容长度: 单次内容 ≤2000 字符
3. 使用分批上传策略

---

## 📚 学科配置

详见 `references/disciplines.md`

当前支持:
- ai (人工智能)
- psychology (心理学)
- social-science (社会科学)
- anthropology (人类学)
- philosophy (哲学)
- game-studies (游戏研究)

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0 | 2026-03-26 | 基于 Superpowers 方法论重构，添加质量检查、健康检查、维护者文档 |
| 1.2 | 2026-03-10 | 添加工作流程规范、飞书文档策略更新 |
| 1.0 | 2026-03-09 | 初始版本 |

---

*最后更新: 2026-03-26 | 版本: 2.0*
