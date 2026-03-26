# 学科分类配置

本文件定义支持的学科分类及其配置参数。

## 学科列表

| 学科ID | 中文名 | 英文名 | 状态 |
|--------|--------|--------|------|
| ai | 人工智能 | Artificial Intelligence | ✅ 已启用 |
| psychology | 心理学 | Psychology | ✅ 已启用 |
| social-science | 社会科学 | Social Science | ✅ 已启用 |
| anthropology | 人类学 | Anthropology | ✅ 已启用 |
| philosophy | 哲学 | Philosophy | ✅ 已启用 |
| game-studies | 游戏研究 | Game Studies | ✅ 已启用 |

## 学科配置详情

### 人工智能 (ai)
```yaml
arxiv_categories:
  - cs.AI
  - cs.LG
  - cs.CL
  - cs.CV
  - cs.RO
keywords:
  - "artificial intelligence"
  - "machine learning"
  - "deep learning"
  - "neural network"
  - "large language model"
  - "reinforcement learning"
semantic_scholar_fields:
  - "Computer Science"
```

### 心理学 (psychology)
```yaml
arxiv_categories:
  - q-bio.NC  # 神经科学（相关）
keywords:
  - "psychology"
  - "cognitive science"
  - "behavioral science"
  - "mental health"
  - "cognitive psychology"
  - "social psychology"
semantic_scholar_fields:
  - "Psychology"
  - "Neuroscience"
```

### 社会科学 (social-science)
```yaml
arxiv_categories:
  - cs.CY  # 计算机与社会
keywords:
  - "social science"
  - "sociology"
  - "social network"
  - "computational social science"
semantic_scholar_fields:
  - "Sociology"
  - "Political Science"
  - "Economics"
```

### 人类学 (anthropology)
```yaml
arxiv_categories: []
keywords:
  - "anthropology"
  - "cultural anthropology"
  - "ethnography"
  - "qualitative research"
semantic_scholar_fields:
  - "Anthropology"
```

### 哲学 (philosophy)
```yaml
arxiv_categories:
  - cs.CY  # 计算机与社会（科技哲学相关）
keywords:
  - "philosophy"
  - "ethics"
  - "philosophy of mind"
  - "philosophy of science"
  - "AI ethics"
semantic_scholar_fields:
  - "Philosophy"
```

### 游戏研究 (game-studies)
```yaml
arxiv_categories:
  - cs.HC  # 人机交互
  - cs.AI  # 游戏AI
keywords:
  - "game studies"
  - "game design"
  - "serious games"
  - "gamification"
  - "video games"
  - "player experience"
semantic_scholar_fields:
  - "Computer Science"
```

## 扩展指南

添加新学科时，需要提供：
1. 学科ID（小写，连字符分隔）
2. 中英文名称
3. arXiv分类代码（如有）
4. 英文关键词列表（用于Semantic Scholar搜索）
5. Semantic Scholar领域代码

## 数据源优先级

1. **arXiv**: 计算机/数学/物理相关学科首选
2. **Semantic Scholar**: 跨学科、社会科学、人文科学首选
3. **Crossref**: 补充数据源（DOI解析）
