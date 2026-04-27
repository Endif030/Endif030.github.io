---
name: paper-research-assistant
description: |
  跨学科论文追踪与知识管理系统 v3.0
  核心功能包括：
  1. 定期收集AI、心理学、社会科学、人类学、哲学、游戏研究等领域的热门论文
  2. 生成逐段中文注释稿（原文+翻译+详细术语解释+类比）
  3. 用户触发式生成知识卡片（读完论文后），支持艾宾浩斯遗忘曲线复习
  4. 深度讨论Q&A文档（可选）
  5. 定时推送知识卡片复习提醒（每日4次）
  使用场景：用户说"收集本周AI论文"、"已读完#1"、"生成#4注释稿"、"保存#1讨论"等
---

# Paper Research Assistant v3.0 - 论文阅读与知识管理

> **版本 3.0** | 基于用户实际工作流重构
> 
> **核心变更**:
> - 用户阅读**注释稿**（逐段解析版），而非论文原文
> - 知识卡片改为**用户触发**（读完论文后生成）
> - 注释稿包含：【原文】+【中文翻译】+【详细注释】+【术语解释】+【生活类比】+【跨学科关联】+【批判性思考】
> - 周文档格式：总览表+单篇论文区块结构

---

## 🚀 快速开始

### 每周工作流程

| 时间 | 动作 | 触发方式 | 说明 |
|------|------|----------|------|
| **周五 18:00** | 📬 主题询问 | 自动 | 询问下周想读什么主题 |
| **周日 23:59** | ⏰ 选择截止 | 自动 | 回复主题，不回复则沿用当前主题 |
| **周一 09:00** | 🚀 周初始化 | 自动 | 收集7篇论文+生成周文档+生成前3篇逐段注释稿 |
| **任意时间** | 📖 阅读注释稿 | 用户自主 | 阅读「注释稿详解」链接（**不需要读原文**） |
| **用户说"已读完#X"** | 📝 生成知识卡片 | 用户触发 | 生成5张卡片+启动复习计划 |
| **用户说"生成#X注释稿"** | ✍️ 生成注释稿 | 用户触发 | 生成指定论文逐段注释稿 |
| **有讨论后** | 💬 生成深度Q&A | 用户触发 | 整理讨论内容生成Q&A文档 |
| **每日 08:30/12:00/16:00/20:00** | ⏰ 卡片复习 | 自动 | 推送当日待复习知识卡片 |

### 支持的学科主题

1. 🤖 **人工智能** (`ai`) - AI、机器学习、深度学习
2. 🧠 **心理学** (`psychology`) - 认知科学、行为科学、心理健康
3. 👥 **社会科学** (`social-science`) - 社会学、计算社会科学
4. 🏛️ **人类学** (`anthropology`) - 文化人类学、民族志
5. 📖 **哲学** (`philosophy`) - 心智哲学、科学哲学、伦理学
6. 🎮 **游戏研究** (`game-studies`) - 游戏设计、玩家体验、游戏化

---

## 📋 完整工作流程

### Phase 1: 每周初始化（周一 09:00 自动执行）

**包含任务**:
1. 📥 收集该主题7篇论文
2. 📄 下载前3篇PDF
3. ✍️ 生成前3篇**逐段注释稿**（详细版，包含术语解释+类比+跨学科关联+批判性思考）
4. 📄 创建阅读周飞书文档（总览表+单篇论文区块）
5. 📬 发送飞书通知

**生成文档格式**:

**周文档** (`📚 [学科]阅读周 - Week of YYYY-MM-DD`):
```markdown
# 📚 AI阅读周 - Week of 2026-03-24
*原始时间: 2026-03-24*
*更新时间: 2026-03-30*
*状态: ⏳ 进行中*

## 📋 阅读完成情况总览
| 序号 | 论文 | 阅读状态 | 知识卡片 | 注释稿 |
|------|------|----------|----------|--------|
| #1 | BEVLM | ⏳ 待阅读 | - | ✅ 完整注释 |
| #2 | Fly360 | ⏳ 待阅读 | - | ✅ 完整注释 |
...

## ⏳ #1 BEVLM - 待阅读

**标题**: BEVLM: Distilling Semantic Knowledge from LLMs into Bird's-Eye View Representations

**arXiv ID**: 2603.06576

**领域**: 自动驾驶 + 大语言模型

**核心洞察**: ...
**核心要点**:
- 要点1
- 要点2
...

**链接**:
- 📄 arXiv原文: https://arxiv.org/abs/2603.06576
- 📥 PDF下载: https://arxiv.org/pdf/2603.06576.pdf
- 📝 **注释稿详解**: [飞书文档链接] ✅
- 💬 深度讨论Q&A: （待讨论后生成）

> 💡 **阅读建议**: 直接点击「注释稿详解」阅读（不需要读原文）
```

**⚠️ 周文档格式要求（重要）**:
1. **标题、arXiv ID、领域之间必须使用空行分隔**（确保每行一个字段）
2. 正确的格式：
   ```markdown
   **标题**: BEVLM: ...
   
   **arXiv ID**: 2603.06576
   
   **领域**: 自动驾驶 + 大语言模型
   ```
3. 错误的格式（会导致挤在一起）：
   ```markdown
   **标题**: BEVLM: ...  
   **arXiv ID**: 2603.06576  
   **领域**: ...
   ```

**注释稿** (`📝 注释稿: [论文标题]_YYYY-MM-DD`):

**⚠️ 注释稿排版规范（2026-04-27 新增，强制执行）**
1. 每个段落必须使用三段分离式结构，严禁写成同一行：
   - `**【原文】**`（独占一行）
   - 原文正文（下一行开始）
   - `**【中文翻译】**`（独占一行）
   - 中文翻译正文（下一行开始）
   - `**【注释解析】**`（独占一行）
   - 注释条目（下一行开始）
2. 段内术语映射编号统一使用圈号：`① ② ③ ④ ⑤`。
3. 同一段中，原文/中文翻译/注释解析三处必须使用**相同圈号**对应同一概念。
4. 不再在文档开头维护“统一概念索引表”，改为段内就地标注。
5. 避免错误加粗：`**【原文】**` 后必须空行，再写正文。
6. 默认**不插入论文配图**（Figure 1/2/...）。仅当用户明确要求“补图/图解”时才执行配图流程，避免无效 token 消耗与版面噪音。
7. 文档内不保留“本版说明/更新说明/下一轮计划”等过程性文字，只保留读者需要的正文内容。

```markdown
# 📝 注释稿: BEVLM_2026-03-30

## 📄 封面信息
| 项目 | 内容 |
|------|------|
| **标题** | ... |
| **arXiv ID** | 2603.06576 |
| **作者** | ... |
| **领域** | ... |

## 摘要
**【原文】** ...
**【中文翻译】** ...
**【注释解释】**
- **术语解释**: [详细定义+背景+例子]
- **背景知识**: [相关背景]
- **类比**: [生活化类比]

## 第1节 引言
...

## 内容拆解
### 研究背景
...
### 核心贡献
...
### 实验结果
...
### 跨学科关联
...
### 一句话总结
> ...

## 批判性思考 / 局限性
...

📚 返回阅读周文档: [链接]
```

---

### Phase 2: 阅读注释稿（用户自主）

**用户操作**:
1. 打开周文档
2. 点击「📝 注释稿详解」链接
3. 阅读逐段解析版本（包含原文、翻译、详细注释、术语解释、类比）

**注释稿内容结构**:
- **封面信息**: 标题、arXiv ID、作者、领域、时间
- **逐段解析**: 
  - 【原文】完整英文段落
  - 【中文翻译】逐句翻译
  - 【注释解释】术语解释（详细版：定义+背景+例子）、背景知识、生活类比
- **内容拆解**: 研究背景、核心贡献、实验结果、跨学科关联、一句话总结
- **批判性思考/局限性**: 方法局限、实验局限、伦理考量、未来方向

---

### Phase 3: 生成剩余注释稿（#4-7，用户触发）

**触发方式**: 用户说"生成 #4 注释稿" 或 "为 Fly360 生成注释"

**执行流程**:
1. 下载对应论文PDF
2. 生成逐段注释稿（与Phase 1相同格式）
3. 创建飞书文档
4. 更新周文档中的「注释稿」状态列

---

### Phase 4: 标记阅读完成 & 生成知识卡片（用户触发）

**触发方式**: 用户说"已读完 #1" 或 "完成 BEVLM"

**执行流程**:
1. 在 papers.json 中标记 `read: true`
2. 更新周文档中的「阅读状态」列
3. 从注释稿内容中提取5个核心问题
4. 生成5张知识卡片（问题+详细答案）
5. 启动艾宾浩斯复习计划（6轮复习：1天后、2天后、4天后、7天后、15天后、30天后）
6. 更新周文档中的「知识卡片」列

**知识卡片格式**:
```json
{
  "id": "fc_xxx",
  "paper_id": "2603.06576",
  "question": "什么是知识蒸馏？",
  "answer": "详细解释...",
  "context": "BEVLM应用场景",
  "difficulty": 3,
  "review_schedule": [...]
}
```

---

### Phase 5: 深度讨论 Q&A（可选，用户触发）

**触发方式**: 讨论结束后用户说"保存 #1 讨论" 或 "生成 #1 深度 Q&A"

**执行流程**:
1. 整理用户与我的对话历史
2. 按问题分类组织讨论内容
3. 生成深度 Q&A 文档
4. 更新周文档中的「深度讨论 Q&A」链接

**Q&A 文档格式**:
```markdown
# 💬 深度讨论Q&A: BEVLM
**论文**: BEVLM
**讨论时间**: 2026-03-24

## 问题1: [问题标题]
**用户问**: ...
**我的回答**: ...
**延伸思考**: ...

📚 返回阅读周文档: [链接]
```

---

### Phase 6: 知识卡片复习（自动推送）

**执行时机**: 每日 08:30 / 12:00 / 16:00 / 20:00

**推送规则**:
- ✅ **有卡片时**: 正常推送待复习的知识卡片
- ✅ **无卡片时**: **取消推送，不发任何消息**（避免重复打扰）

**推送内容示例**:
```
⏰ 08:30 知识卡片复习
今日共 3 张卡片待复习
========================================

--- 卡片 1/3 ---
🧠 知识卡片复习 [2/6轮]

📄 来源：BEVLM（人工智能）

❓ 问题：什么是知识蒸馏？

💡 答案：知识蒸馏是一种将大模型（教师）的知识迁移到小模型（学生）的技术...

📋 上下文：自动驾驶场景中的语义学习
💾 卡片ID: fc_xxx

========================================
📊 记录复习：回复 "review 卡片ID 评分"
（1=几乎忘记，5=完全掌握）
```

---

## 💬 用户命令体系

| 用户输入 | 系统动作 | 产出 |
|----------|----------|------|
| "收集本周论文" | 手动触发周初始化 | 周文档 + 前3篇注释稿 |
| "已读完 #1" / "完成 BEVLM" | 标记阅读完成 + 生成知识卡片 | 5张卡片 + 复习计划 |
| "生成 #4 注释稿" | 生成指定论文逐段注释稿 | 注释稿文档 |
| "保存 #1 讨论" / "生成 #1 深度 Q&A" | 生成深度讨论文档 | Q&A 文档 |
| "显示本周进度" | 读取周文档状态 | 进度摘要 |
| "复习" | 显示今日待复习卡片 | 卡片列表 |

---

## 📁 目录结构

```
paper-research-assistant/
├── SKILL.md                          # 本文件（v3.0）
├── MAINTENANCE.md                    # 维护者文档
├── CHANGELOG.md                      # 变更日志
├── data/
│   ├── papers.json                   # 论文数据库（更新字段）
│   ├── week_docs.json               # 新增：周文档索引
│   ├── flashcards.json              # 知识卡片数据库
│   ├── review_schedule.json         # 复习计划
│   └── theme_config.json            # 主题配置
├── papers/                           # PDF 存储
├── annotations/                      # 本地注释稿备份
├── scripts/
│   ├── fetch_papers.py              # 论文收集
│   ├── download_paper.py            # PDF下载
│   ├── generate_annotation.py       # 🔥 逐段注释稿生成（核心）
│   ├── create_flashcard.py          # 知识卡片生成（用户触发）
│   ├── create_deep_qa.py            # 新增：深度Q&A生成
│   ├── update_week_doc.py           # 新增：周文档更新
│   ├── weekly_init.py               # 周初始化
│   ├── spaced_repetition_v2.py      # 复习推送
│   └── quality_check.py             # 质量检查
├── cron_jobs/
│   ├── weekly_init.sh               # 每周初始化
│   ├── flashcard_push.sh            # 知识卡片推送
│   └── monthly_report.sh            # 月报生成
└── references/
    └── disciplines.md               # 学科配置
```

---

## 📝 数据结构

### papers.json（更新后）
```json
{
  "papers": [
    {
      "id": "http://arxiv.org/abs/2603.06576v1",
      "title": "BEVLM: ...",
      "arxiv_id": "2603.06576",
      "discipline": "ai",
      "fetched_at": "2026-03-24T09:00:00",
      
      "week_order": 1,
      "week_doc_url": "https://www.feishu.cn/docx/xxx",
      "annotation_doc_url": "https://www.feishu.cn/docx/yyy",
      "deep_qa_doc_url": null,
      
      "read": false,
      "read_at": null,
      "flashcards": [],
      
      "local_pdf": "/path/to/pdf"
    }
  ],
  "last_updated": "2026-03-24T09:00:00"
}
```

### week_docs.json（新增）
```json
{
  "week_docs": [
    {
      "week_start": "2026-03-24",
      "discipline": "ai",
      "discipline_emoji": "🤖",
      "status": "in_progress",
      "doc_url": "https://www.feishu.cn/docx/xxx",
      "paper_count": 7,
      "papers": ["2603.06576", "2603.06573", ...],
      "annotations_generated": [1, 2, 3],
      "created_at": "2026-03-24T09:00:00",
      "updated_at": "2026-03-24T09:00:00"
    }
  ]
}
```

---

## ⚙️ 自动化配置（Crontab）

**重要规则**: 知识卡片推送脚本在没有待复习卡片时会返回**空输出**，调用者需要检查输出并决定是否发送消息。

### 配置示例

```bash
# 周五 18:00 - 主题询问
0 18 * * 5 cd /root/.openclaw/workspace/skills/paper-research-assistant && python3 scripts/ask_weekly_theme.py

# 周一 09:00 - 周初始化（生成周文档+前3篇逐段注释稿）
0 9 * * 1 cd /root/.openclaw/workspace/skills/paper-research-assistant && python3 scripts/weekly_init.py

# 每日 08:30/12:00/16:00/20:00 - 知识卡片复习推送
# 注意：脚本返回空时取消推送，避免打扰
30 8 * * * cd /root/.openclaw/workspace/skills/paper-research-assistant && python3 scripts/spaced_repetition_v2.py --slot 08:30 --message-only | xargs -I {} sh -c '[ -n "{}" ] && openclaw message send --channel feishu "{}"'
0 12 * * * cd /root/.openclaw/workspace/skills/paper-research-assistant && python3 scripts/spaced_repetition_v2.py --slot 12:00 --message-only | xargs -I {} sh -c '[ -n "{}" ] && openclaw message send --channel feishu "{}"'
0 16 * * * cd /root/.openclaw/workspace/skills/paper-research-assistant && python3 scripts/spaced_repetition_v2.py --slot 16:00 --message-only | xargs -I {} sh -c '[ -n "{}" ] && openclaw message send --channel feishu "{}"'
0 20 * * * cd /root/.openclaw/workspace/skills/paper-research-assistant && python3 scripts/spaced_repetition_v2.py --slot 20:00 --message-only | xargs -I {} sh -c '[ -n "{}" ] && openclaw message send --channel feishu "{}"'
```

### 使用 OpenClaw Cron（推荐）

```bash
# 10分钟后测试
openclaw cron add \
  --name "知识卡片推送 08:30" \
  --at "30 8 * * *" \
  --session isolated \
  --message "请执行：cd /root/.openclaw/workspace/skills/paper-research-assistant && python3 scripts/spaced_repetition_v2.py --slot 08:30 --message-only，如果输出非空则使用 message 工具发送"
```

**子代理执行逻辑**:
```python
import subprocess
result = subprocess.run(
    ["python3", "scripts/spaced_repetition_v2.py", "--slot", "08:30", "--message-only"],
    capture_output=True, text=True, cwd="/root/.openclaw/workspace/skills/paper-research-assistant"
)
message = result.stdout.strip()
if message:  # 只有在有内容时才发送
    # 使用 message 工具发送
    send_message(message)
# 否则静默跳过，不打扰用户
```

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **3.0** | 2026-03-30 | 重构工作流：用户读注释稿而非原文；知识卡片用户触发；注释稿包含逐段解析+详细术语+类比+跨学科+批判性思考 |
| 2.1 | 2026-03-26 | 合并节点；知识卡片直接显示答案 |
| 2.0 | 2026-03-26 | 基于 Superpowers 方法论重构 |
| 1.0 | 2026-03-09 | 初始版本 |

---

*最后更新: 2026-03-30 | 版本: 3.0*
