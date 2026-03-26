# 知识卡片数据结构规范

## 卡片结构

### 核心字段
```json
{
  "id": "fc_xxxxxxxx",           // 卡片唯一ID
  "paper_id": "arxiv_2401.xxxx", // 关联论文ID
  "discipline": "ai",            // 所属学科
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  
  "question": "什么是Transformer架构的核心机制？",
  "answer": "自注意力机制（Self-Attention），允许模型在处理序列时直接关注任意位置的token...",
  "context": "来自论文《Attention Is All You Need》第二节", // 可选上下文
  
  "tags": ["transformer", "attention", "nlp"],
  "difficulty": 3,               // 1-5难度等级
  
  "review_schedule": {
    "created": "2024-01-15",
    "intervals": [1, 2, 4, 7, 15, 30],  // 艾宾浩斯复习间隔（天）
    "reviews": [
      {"date": "2024-01-16", "status": "completed", "ease": 4},
      {"date": "2024-01-17", "status": "pending"}
    ],
    "next_review": "2024-01-17",
    "stage": 1                     // 当前复习阶段
  },
  
  "mastery_level": 0,            // 掌握程度 0-100
  "status": "active"             // active, mastered, archived
}
```

## 艾宾浩斯遗忘曲线

### 复习间隔
| 阶段 | 间隔天数 | 记忆保留率 |
|------|----------|------------|
| 初次学习 | 0 | 100% |
| 第1次复习 | 1 | ~60% |
| 第2次复习 | 2 | ~70% |
| 第3次复习 | 4 | ~80% |
| 第4次复习 | 7 | ~85% |
| 第5次复习 | 15 | ~90% |
| 第6次复习 | 30 | ~95% |

### 动态调整
根据用户对卡片的掌握程度（ease rating 1-5）调整间隔：
- ease ≥ 4: 间隔增加20%
- ease = 3: 保持默认间隔
- ease ≤ 2: 间隔减少20%，必要时增加额外复习

## 存储格式

### 文件组织
```
flashcards/
├── active/
│   ├── 2024-01/
│   │   ├── fc_001.json
│   │   └── fc_002.json
│   └── 2024-02/
├── archived/
│   └── fc_old.json
└── index.json  // 卡片索引，用于快速查询
```

### 索引文件
```json
{
  "total_cards": 150,
  "active_cards": 120,
  "mastered_cards": 30,
  "by_discipline": {
    "ai": 50,
    "psychology": 30,
    "social-science": 20,
    "anthropology": 15,
    "philosophy": 20,
    "game-studies": 15
  },
  "cards": {
    "fc_001": {
      "status": "active",
      "next_review": "2024-01-17",
      "discipline": "ai"
    }
  }
}
```

## 每日推送策略

### 推送时段
| 时段 | 时间 | 推送数量策略 |
|------|------|--------------|
| 晨间 | 08:30 | 3-5张（新卡片优先）|
| 午间 | 12:00 | 3-5张（待复习卡片）|
| 下午 | 16:00 | 3-5张（困难卡片加强）|
| 晚间 | 20:00 | 3-5张（综合复习）|

### 推送内容格式
```markdown
🧠 知识卡片复习 [第1/6轮]

📄 来源：人工智能 - Attention Is All You Need

❓ 问题：
什么是Transformer架构的核心机制？

💡 答案：
自注意力机制（Self-Attention），允许模型在处理序列时直接关注任意位置的token，计算query、key、value三个向量的交互。

---
回复"已掌握"或"需复习"来记录你的掌握程度
```

## 掌握度评估

### 自评等级
| 等级 | 描述 | 后续动作 |
|------|------|----------|
| 5 | 完全掌握，可以教授他人 | 延长间隔，向归档过渡 |
| 4 | 掌握良好 | 正常进入下一阶段 |
| 3 | 基本掌握，略有迟疑 | 正常进入下一阶段 |
| 2 | 部分掌握，需要加强 | 缩短间隔，增加复习 |
| 1 | 几乎忘记 | 重置复习进度 |

### 自动化掌握度计算
```
mastery_level = (completed_reviews / total_reviews) * avg_ease * 20
```

当 mastery_level ≥ 80 且完成所有6轮复习时，卡片状态变为 mastered。
