# Paper Research Assistant - 使用指南

## 项目概述

Paper Research Assistant 是一个跨学科论文追踪与知识管理系统，核心特色是**逐段注释稿**生成，将英文学术论文转化为易读的中文注释版本。

## 已完成工作

### ✅ 已实现功能

1. **论文收集系统**
   - 6个学科分类（AI、心理学、社会科学、人类学、哲学、游戏研究）
   - 45篇论文已入库
   - 双数据源：arXiv + Semantic Scholar

2. **PDF下载管理**
   - 7篇AI论文PDF已下载
   - 自动分类存储

3. **注释稿生成** ⭐核心功能
   - **BEVLM论文全文注释稿已完成**
   - 逐段格式：原文 + 中文翻译 + 详细注释
   - 包含术语解释、背景知识、类比说明

4. **知识卡片系统**
   - 艾宾浩斯遗忘曲线复习计划
   - 掌握度跟踪

5. **报告生成**
   - 周报/月报自动生成

### 📄 注释稿样例

**BEVLM论文完整注释稿**已生成并上传到飞书云文档：
- 链接：https://feishu.cn/docx/IRoZdF36HoIbbFxQQPocNNfynWb
- 内容：标题页 + 摘要 + 引言 + 相关工作 + BEV研究 + 方法 + 实验 + 结论

## AI阅读周使用指南

### 什么是AI阅读周？

**AI阅读周**是一种集中式的论文阅读模式：
- **周期**: 1周（7天）
- **数量**: 7篇论文（每天1-2篇）
- **主题**: 聚焦同一领域（如AI多领域应用）
- **输出**: 阅读周文档 + 逐篇注释稿 + 知识卡片

### 阅读周文档格式

每篇论文在阅读周文档中的标准格式：

```markdown
## #编号 论文简称 - 主题

**标题**: 完整英文标题

**arXiv ID**: xxx

**领域**: 学科分类

**核心内容**:
- **问题**: 研究要解决的核心问题
- **方法**: 采用的技术方法
- **创新**: 核心创新点
- **价值**: 应用价值/意义
- **跨学科关联**: 与其他学科的连接

📄 arXiv原文: https://arxiv.org/abs/xxx
📥 PDF下载: https://arxiv.org/pdf/xxx.pdf
📝 注释稿详解: [链接]（状态）
```

### 如何使用阅读周文档

**第一步**: 打开阅读周文档
- 查看本周7篇论文列表
- 了解每篇论文的主题和核心内容

**第二步**: 点击arXiv原文阅读
- 直接跳转到arXiv阅读论文
- 或下载PDF本地阅读

**第三步**: 读完标记
- 告诉AI"已读完#编号"
- 知识卡片自动加入复习库

**第四步**: 查看注释稿深入理解
- 点击"注释稿详解"链接
- 阅读逐段原文+翻译+注释

### 阅读周工作流程

```
周一: 收集7篇论文 → 生成阅读周文档 → 开始阅读#1
周二: 完成#1注释稿 → 更新文档链接 → 阅读#2
周三: 完成#2注释稿 → 更新链接 → 阅读#3
...
周日: 完成全部7篇 → 生成周报 → 创建知识卡片
```

### 当前阅读周案例

**AI阅读周（2026-03-09启动）**
- **文档链接**: https://feishu.cn/docx/LRgJdpjd4omLZkxoMpBc6cnynge
- **7篇AI论文**:
  1. ✅ BEVLM - 自动驾驶+大语言模型（注释稿已完成）
  2. 📖 Fly360 - 无人机全景避障
  3. 📖 SUREON - 手术AI推理
  4. 📖 Boosting RL - 强化学习
  5. 📖 LiveSense - WiFi感知
  6. 📖 RAMoEA-QA - 呼吸诊断
  7. 📖 Fetal AI - 产前诊断

### 生成新的阅读周

```bash
# 1. 收集论文
cd ~/.openclaw/workspace/skills/paper-research-assistant
python scripts/fetch_papers.py --discipline ai --max-results 10

# 2. 创建阅读周文档（手动）
# - 创建飞书云文档
# - 按标准格式添加7篇论文信息
# - 添加arXiv链接和PDF下载链接

# 3. 逐篇生成注释稿并更新链接
# - 读完一篇，生成注释稿
# - 上传到飞书，获取链接
# - 更新阅读周文档中的"注释稿详解"链接

# 4. 设置定时任务
bash scripts/setup_all_cron.sh
```

---

## 快速开始

### 1. 收集论文

```bash
cd ~/.openclaw/workspace/skills/paper-research-assistant

# 收集AI领域论文
python scripts/fetch_papers.py --discipline ai --max-results 10

# 收集所有学科
python scripts/fetch_papers.py --discipline all
```

### 2. 下载PDF

```bash
# 下载某学科所有论文
python scripts/download_paper.py --discipline ai --max-papers 10

# 下载所有未下载的论文
python scripts/download_paper.py --all
```

### 3. 生成注释稿

```bash
# 为指定论文生成注释稿
python scripts/generate_annotation.py --paper-id <arxiv_id>
```

**注意**: 当前脚本生成基础注释稿模板。全文逐段注释需要手动基于PDF内容生成（参考BEVLM样例）。

### 4. 创建知识卡片

```bash
python scripts/create_flashcard.py create \
  --paper-id <arxiv_id> \
  --question "什么是BEV表示？" \
  --answer "鸟瞰图表示，将多摄像头图像转换为统一俯视图..." \
  --discipline ai \
  --tags "bev,autonomous-driving"
```

### 5. 设置定时任务

```bash
# 设置所有定时任务（论文收集、知识卡片推送、报告生成）
bash scripts/setup_all_cron.sh
```

这将创建7个定时任务：
- 每周一 09:00 收集论文
- 每天 08:30/12:00/16:00/20:00 推送知识卡片
- 每周日 21:00 生成周报
- 每月1日 21:00 生成月报

### 6. 生成报告

```bash
# 生成周报
python scripts/generate_report.py --type weekly --save

# 生成月报
python scripts/generate_report.py --type monthly --save
```

## 注释稿格式规范

### 标准格式

```markdown
【原文】
论文原始英文段落

【中文翻译】
准确的中文译文

【注释解释】
- **术语解释**：专业术语的含义
- **背景知识**：相关技术背景  
- **类比说明**：帮助理解的比喻
- **技术意义**：为什么重要
```

### 示例

**【原文】**
> The integration of Large Language Models (LLMs) into autonomous driving has attracted growing interest for their strong reasoning and semantic understanding abilities...

**【中文翻译】**
> 将大语言模型(LLM)集成到自动驾驶领域已引起越来越多的关注...

**【注释解释】**
- **长尾场景**: 99%常见情况 + 1%罕见但关键的情况
- **语义理解**: 不只是识别物体，而是理解场景含义

## 目录结构

```
paper-research/
├── papers/                    # PDF存储（7篇AI论文）
├── annotations/               # 注释稿
│   └── ai/
│       └── BEVLM_完整注释稿.md  ✅ 样例
├── reports/                   # 报告
└── data/                      # 数据库
    ├── papers.json            # 45篇论文元数据
    ├── flashcards.json        # 知识卡片
    └── review_schedule.json   # 复习计划
```

## 数据现状

| 学科 | 论文数 | PDF下载 | 注释稿 |
|------|--------|---------|--------|
| 人工智能 | 10篇 | 7篇 | 1篇完整 |
| 心理学 | 10篇 | - | - |
| 社会科学 | 10篇 | - | - |
| 人类学 | 10篇 | - | - |
| 游戏研究 | 10篇 | - | - |
| **总计** | **45篇** | **7篇** | **1篇** |

## 术语定义

| 术语 | 定义 |
|------|------|
| **注释稿 (Annotation)** | 逐段原文+翻译+解释的文档，便于边读边理解 |
| **内容拆解 (Analysis)** | 结构化总结，用于全局把握 |
| **知识卡片 (Flashcard)** | Q&A对，用于艾宾浩斯复习 |

## 后续优化方向

### 短期（1-2周）
- [ ] 设置定时任务自动化
- [ ] 为剩余6篇AI论文生成注释稿
- [ ] 接入翻译API优化翻译质量

### 中期（1个月）
- [ ] 增加PubMed数据源
- [ ] 完善其他学科论文下载
- [ ] 构建论文引用网络

### 长期（3个月）
- [ ] 接入JSTOR等人文社科数据源
- [ ] 实现主题聚类分析
- [ ] 构建跨学科知识图谱

## 问题反馈

如有问题或建议，请直接修改 skill 目录下的文档和脚本。

---

*最后更新: 2026-03-09*  
*版本: v1.1*  
*新增: AI阅读周使用指南*  
*论文总数: 45篇*
