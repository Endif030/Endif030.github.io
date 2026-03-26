# 📄 BEVLM: Distilling Semantic Knowledge from LLMs into Bird's-Eye View Representations

## 基础信息

| 项目 | 内容 |
|------|------|
| **学科** | 人工智能 |
| **作者** | Thomas Monninger, Shaoyuan Xie, Qi Alfred Chen, Sihao Ding |
| **年份** | 2026 |
| **来源** | arxiv |
| **引用数** | 未知 |
| **DOI** |  |
| **原文链接** | http://arxiv.org/abs/2603.06576v1 |
| **本地PDF** | /root/.openclaw/workspace/paper-research/papers/ai/arxiv_2603.06576.pdf |

---

## 📝 摘要（原文）

The integration of Large Language Models (LLMs) into autonomous driving has attracted growing interest for their strong reasoning and semantic understanding abilities, which are essential for handling complex decision-making and long-tail scenarios. However, existing methods typically feed LLMs with tokens from multi-view and multi-frame images independently, leading to redundant computation and limited spatial consistency. This separation in visual processing hinders accurate 3D spatial reasoning and fails to maintain geometric coherence across views. On the other hand, Bird's-Eye View (BEV) representations learned from geometrically annotated tasks (e.g., object detection) provide spatial structure but lack the semantic richness of foundation vision encoders. To bridge this gap, we propose BEVLM, a framework that connects a spatially consistent and semantically distilled BEV representation with LLMs. Through extensive experiments, we show that BEVLM enables LLMs to reason more effectively in cross-view driving scenes, improving accuracy by 46%, by leveraging BEV features as unified inputs. Furthermore, by distilling semantic knowledge from LLMs into BEV representations, BEVLM significantly improves closed-loop end-to-end driving performance by 29% in safety-critical scenarios.

---

## 🌐 摘要（中文翻译）

【待翻译】

---

## 🔍 研究背景

【在此记录研究的背景和动机】

- 
- 
- 

---

## 🧪 研究方法

【在此记录研究方法和实验设计】

- 方法：
- 数据：
- 实验设置：

---

## 💡 核心发现

【在此记录主要研究结论】

1. 
2. 
3. 

---

## 🎯 创新点

【在此记录论文的创新之处】

- 
- 

---

## 🤔 个人批注与思考

### 疑问点
【记录阅读过程中的疑问】

- 
- 

### Insight / 启发
【记录阅读后的思考和启发】

- 
- 

### 可关联的知识
【与其他学科或论文的关联】

- 
- 

---

## 🏷️ 标签

#论文 #人工智能 #2026 #待读 #待翻译

---

## 📚 知识卡片（从问题生成）

【在阅读过程中，将关键问题-答案对记录为知识卡片】

使用命令创建：
```bash
python scripts/create_flashcard.py create \\
  --paper-id "http___arxiv.org_abs_2603.06576v1" \\
  --question "你的问题" \\
  --answer "答案内容" \\
  --discipline "人工智能" \\
  --context "来自论文的上下文"
```

### 卡片示例
- **问题**：
- **答案**：
- **掌握度**：□ 生疏 □ 熟悉 □ 精通

---

*生成时间：2026-03-09T19:23:49.566478*
*论文ID：http___arxiv.org_abs_2603.06576v1*
