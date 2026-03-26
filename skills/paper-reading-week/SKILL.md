# 论文阅读周文档管理流程

## 概述

本 SKILL 定义了 AI 论文阅读周文档的标准化生成和管理流程，确保文档格式统一、更新便捷、历史可追溯。

---

## 文档生命周期

```
周一早 9:00 → 自动收集本周论文 → 生成新周文档（基于模板）
                ↓
周一至周五 → 阅读论文 + 生成知识卡片 + 生成注释稿
                ↓
周末 → 完成当周阅读 → 归档文档 → 准备下周
```

---

## 模板结构

模板文件位置：`~/.openclaw/workspace/skills/paper-reading-week/template.md`

### 模板内容规范

```markdown
# 📚 AI阅读周 ({{DATE}}) - {{WEEK_NUMBER}}周 - {{THEME}}

*生成时间: {{DATE}}*  
*状态: ⏳ 进行中*

---

## 本周论文概览

| 序号 | 论文 | 阅读状态 | 知识卡片 | 注释稿 |
|------|------|----------|----------|--------|
| #1 | {{PAPER_1_TITLE}} | ⏳ 待阅读 | ⏳ 待生成 | ⏳ 待生成 |
| #2 | {{PAPER_2_TITLE}} | ⏳ 待阅读 | ⏳ 待生成 | ⏳ 待生成 |
| #3 | {{PAPER_3_TITLE}} | ⏳ 待阅读 | ⏳ 待生成 | ⏳ 待生成 |
| #4 | {{PAPER_4_TITLE}} | ⏳ 待阅读 | ⏳ 待生成 | ⏳ 待生成 |
| #5 | {{PAPER_5_TITLE}} | ⏳ 待阅读 | ⏳ 待生成 | ⏳ 待生成 |
| #6 | {{PAPER_6_TITLE}} | ⏳ 待阅读 | ⏳ 待生成 | ⏳ 待生成 |
| #7 | {{PAPER_7_TITLE}} | ⏳ 待阅读 | ⏳ 待生成 | ⏳ 待生成 |

**总计**: 7篇论文待阅读

---

## ✅ #1 {{PAPER_1_TITLE}} - 待阅读

**标题**: {{PAPER_1_FULL_TITLE}}  
**arXiv ID**: {{PAPER_1_ARXIV}}  
**领域**: {{PAPER_1_FIELD}}

**核心洞察**: [待填写]

**核心内容**:
- **问题**: [待填写]
- **方法**: [待填写]
- **创新**: [待填写]
- **价值**: [待填写]
- **跨学科关联**: [待填写]

**知识卡片** (5张):
1. [待生成]
2. [待生成]
3. [待生成]
4. [待生成]
5. [待生成]

- 📄 arXiv原文: https://arxiv.org/abs/{{PAPER_1_ARXIV}}
- 📥 PDF下载: https://arxiv.org/pdf/{{PAPER_1_ARXIV}}.pdf
- 📝 注释稿详解: ⏳ 待生成
- 💬 深度讨论Q&A: ⏳ 待生成

> 💡 **推荐阅读顺序**: 先看arXiv原文 → 再看注释稿 → 最后看深度讨论Q&A

---

## ✅ #2 {{PAPER_2_TITLE}} - 待阅读

[结构同上，复制 #1 格式]

---

## ✅ #3 {{PAPER_3_TITLE}} - 待阅读

[结构同上，复制 #1 格式]

---

## ✅ #4 {{PAPER_4_TITLE}} - 待阅读

[结构同上，复制 #1 格式]

---

## ✅ #5 {{PAPER_5_TITLE}} - 待阅读

[结构同上，复制 #1 格式]

---

## ✅ #6 {{PAPER_6_TITLE}} - 待阅读

[结构同上，复制 #1 格式]

---

## ✅ #7 {{PAPER_7_TITLE}} - 待阅读

[结构同上，复制 #1 格式]

---

**使用说明**: 点击arXiv原文链接 → 读完告诉我"已读完#编号" → 查看注释稿深入理解 → 阅读深度Q&A（如有）进行跨学科思考

*AI阅读周计划进行中 🚀*

---

## 📋 更新日志

**{{DATE}} 初始化**:
- ⏳ 创建本周阅读文档
- ⏳ 7篇论文待阅读和生成注释稿

*最后更新: {{DATE}}*
```

---

## 占位符说明

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{DATE}}` | 当前日期 | 2026-03-24 |
| `{{WEEK_NUMBER}}` | 第几周 | 第3周 |
| `{{THEME}}` | 本周主题 | 医疗AI专题 |
| `{{PAPER_N_TITLE}}` | 论文简称 | BEVLM |
| `{{PAPER_N_FULL_TITLE}}` | 论文完整标题 | BEVLM: Distilling Semantic Knowledge... |
| `{{PAPER_N_ARXIV}}` | arXiv ID | 2603.06576 |
| `{{PAPER_N_FIELD}}` | 领域 | 自动驾驶 / 大语言模型 |

---

## 执行流程

### 1. 每周一 9:00 - 初始化新周文档

**触发条件**: 定时任务 `cron 0 9 * * 1` (每周一早9点)

**执行步骤**:
1. 读取本地模板 `template.md`
2. 从论文源（arXiv/其他）收集本周7篇论文信息
3. 填充模板占位符
4. 生成本地 Markdown 文件：`AI阅读周_{{DATE}}.md`
5. 使用 `feishu_create_doc` 上传到飞书云文档
6. 记录文档链接到 `weeks_index.md`

**脚本示例**:
```javascript
// 伪代码
const template = readFile('template.md');
const papers = await fetchWeeklyPapers();
const filled = fillTemplate(template, papers);
const localPath = saveLocal(filled, `AI阅读周_${date}.md`);
const doc = await feishuCreateDoc({
  title: `📚 AI阅读周 (${date}) - ${weekNum}周`,
  markdown: filled
});
recordToIndex(date, weekNum, doc.url);
```

### 2. 阅读期 - 更新内容

**阶段 1: 阅读论文**（用户完成）
- 用户点击 arXiv 链接阅读
- 告诉 AI "已读完 #N"
- AI 更新文档状态：⏳ → ✅

**阶段 2: 生成知识卡片**（用户或 AI）
- 基于论文内容生成 5 张知识卡片
- 替换 `[待生成]` 为具体问题

**阶段 3: 生成注释稿**（AI 执行）
```javascript
// 自动流程
1. 读取本地论文 PDF 或 arXiv 页面
2. 生成逐段中文注释稿
3. 保存到本地：`/paper-research/annotations/ai/{{PAPER}}_注释稿.md`
4. 上传到飞书云文档创建注释稿文档
5. 获取注释稿文档链接
6. 更新周文档中的链接：⏳ 待生成 → [链接] ✅
```

**阶段 4: 生成深度 Q&A**（可选）
- 基于注释稿内容生成跨学科问答
- 创建 Q&A 文档并更新链接

### 3. 周末 - 归档

**检查清单**:
- [ ] 所有 7 篇论文状态为 ✅ 已完成
- [ ] 所有知识卡片已生成（非 [待生成]）
- [ ] 所有注释稿链接已更新（非 ⏳）
- [ ] 更新文档状态：*状态: ⏳ 进行中* → *状态: ✅ 已完成*

**归档操作**:
1. 将完成文档添加到知识库索引
2. 触发知识卡片复习计划（艾宾浩斯）
3. 准备下周模板

---

## 历史文档管理

### 索引文件

位置：`~/.openclaw/workspace/skills/paper-reading-week/weeks_index.md`

```markdown
# AI阅读周历史文档索引

| 周次 | 日期 | 主题 | 飞书文档链接 | 状态 | 备注 |
|------|------|------|-------------|------|------|
| 第1周 | 2026-03-09 | AI多领域应用 | [链接] | ✅ 已完成 | 7篇全部完成 |
| 第2周 | 2026-03-17 | 医疗AI专题 | [链接] | ✅ 已完成 | 7篇全部完成 |
| 第3周 | 2026-03-24 | [主题] | [链接] | ⏳ 进行中 | 进行中 |
```

### 本地文件结构

```
~/.openclaw/workspace/skills/paper-reading-week/
├── template.md              # 主模板
├── weeks_index.md           # 历史索引
├── SKILL.md                 # 本文件
├── weeks/                   # 历史周文档
│   ├── AI阅读周_2026-03-09.md
│   ├── AI阅读周_2026-03-17.md
│   └── AI阅读周_2026-03-24.md
└── annotations/             # 注释稿本地备份
    ├── BEVLM_注释稿.md
    ├── Fly360_注释稿.md
    └── ...
```

---

## 更新规范

### 允许更新的内容

✅ **可以更新**:
- `[待填写]` → 具体文本内容
- `[待生成]` → 知识卡片问题
- `⏳ 待生成` → 文档链接 ✅
- `⏳ 进行中` → `✅ 已完成`
- 更新日志追加新条目

❌ **禁止更新**（除非用户明确要求）:
- 文档标题格式
- 论文条目结构（标题/arXiv ID/领域行）
- 四链接格式（arXiv/PDF/注释稿/Q&A）
- 推荐阅读顺序提示框
- 分隔符 `---`

### 更新操作示例

**更新知识卡片**:
```javascript
feishu_update_doc({
  doc_id: 'xxx',
  mode: 'replace_range',
  selection_with_ellipsis: '1. [待生成]...5. [待生成]',
  markdown: '1. 什么是知识蒸馏？\n2. 为什么传统BEV训练方式无法实现语义理解？\n3. ...'
});
```

**更新注释稿链接**:
```javascript
feishu_update_doc({
  doc_id: 'xxx',
  mode: 'replace_range',
  selection_with_ellipsis: '📝 注释稿详解: ⏳ 待生成',
  markdown: '📝 注释稿详解: https://www.feishu.cn/docx/xxx ✅'
});
```

---

## 故障处理

### 格式错乱恢复

如果更新导致格式错乱：
1. 立即停止修改
2. 从本地备份 `weeks/AI阅读周_{{DATE}}.md` 重新上传
3. 或使用模板重新生成，复制已有内容

### 注释稿链接失效

如果注释稿文档被误删：
1. 从本地备份 `annotations/{{PAPER}}_注释稿.md` 重新上传
2. 获取新链接并更新周文档

---

## 附录：定时任务配置

```bash
# 每周一上午 9:00 生成新周文档
openclaw cron add \
  --name "论文阅读周初始化" \
  --at "0 9 * * 1" \
  --session isolated \
  --message "请执行：读取模板 → 收集本周论文 → 生成新周文档 → 上传飞书"
```

---

**创建时间**: 2026-03-24  
**版本**: v1.0  
**适用**: AI论文阅读周文档管理
