# 论文阅读系统架构设计文档

## 项目概述
跨学科论文追踪与知识管理系统，实现从论文发现到知识内化的完整闭环。

## 核心模块

### 1. 论文收集模块 (fetch_papers.py)
- **数据源**: arXiv (35篇) + Semantic Scholar (10篇)
- **支持学科**: AI、心理学、社会科学、人类学、哲学、游戏研究
- **选入标准**: 时间40% + 引用30% + 学科匹配30%
- **存储**: papers.json (45篇论文元数据)

### 2. 注释稿生成模块 (generate_annotation.py)
- **输入**: 论文元数据
- **输出**: 逐段注释稿（原文+翻译+注释）
- **格式**: Markdown，飞书文档兼容
- **状态**: 已验证BEVLM、Fly360等论文

### 3. 知识卡片模块 (flashcards.json)
- **数量**: 12张活跃卡片
- **算法**: 艾宾浩斯遗忘曲线 (1/2/4/7/15/30天)
- **状态字段**: next_review, current_stage, mastery_level
- **问题**: 3月11日后未再推送

### 4. 定时推送模块 (spaced_repetition.py)
- **推送时段**: 08:30/12:00/16:00/20:00
- **分配策略**: 交错分配到4个时段
- **消息格式**: 批量推送，含卡片ID和复习指令
- **问题**: 只输出到stdout，未调用message工具

### 5. 定时任务配置 (setup_all_cron.sh)
- **工具**: openclaw cron add
- **参数**: 使用了--deliver --channel --to --post-to-main
- **问题**: 这些参数有bug，导致消息投递失败

## 数据流
```
论文源 → fetch_papers.py → papers.json → generate_annotation.py → 飞书文档
                                                             ↓
用户阅读完成 → create_flashcard.py → flashcards.json → spaced_repetition.py → 用户
                                                             ↑
                                                    cron定时触发(当前失效)
```

## 技术债务
1. **cron参数错误**: 使用--deliver等废弃参数
2. **消息推送缺陷**: 脚本只输出不发送
3. **飞书API限制**: update_doc模式参数失效
4. **Semantic Scholar 429**: 速率限制未处理
5. **PDF全文解析**: 仅支持摘要，未解析全文

## 期望新增功能
1. PDF全文自动解析和分段
2. 智能知识卡片自动生成（AI提取而非手动）
3. 跨学科知识图谱和关联发现
4. 修复艾宾浩斯推送机制

## 文件结构
```
paper-research/
├── papers/           # PDF存储
├── annotations/      # 注释稿
├── data/
│   ├── papers.json      # 论文元数据
│   ├── flashcards.json  # 知识卡片
│   └── review_schedule.json
└── scripts/
    ├── fetch_papers.py
    ├── generate_annotation.py
    ├── spaced_repetition.py
    └── setup_all_cron.sh
```

## 部署环境
- 运行环境: OpenClaw VM
- 用户ID: ou_bbfc027431c61a8ba421c54c7bb0f5c4
- 渠道: Feishu
- 工作目录: /root/.openclaw/workspace/paper-research
