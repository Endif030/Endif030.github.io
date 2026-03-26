# 飞书文档更新方案

## 背景
由于当前会话中 `feishu_update_doc` 工具调用格式存在问题（参数验证失败），需要通过 Node.js 脚本间接调用。

## 可用的 Node.js 脚本

### 脚本位置
```
/tmp/update_doc_direct.js
```

### 使用方法

#### 1. 基本调用格式
```bash
node /tmp/update_doc_direct.js "<doc_id>" "<markdown内容>" "<mode>"
```

#### 2. 参数说明
- `doc_id`: 飞书文档 ID（如 `FdB1dqW8ooYhWsxYB8Nclcyjnud`）
- `markdown`: 要追加/替换的 Markdown 内容（支持换行符 `\n`）
- `mode`: 更新模式，可选 `append`（追加）、`replace_range`（替换）、`overwrite`（覆盖）

#### 3. 使用示例

**追加内容到文档末尾：**
```bash
node /tmp/update_doc_direct.js "文档ID" "## 新章节\n\n内容" "append"
```

**替换文档中的特定内容：**
```bash
node /tmp/update_doc_direct.js "文档ID" "## 新标题\n\n新内容" "replace_range"
# 注意：replace_range 模式需要配合 selection 参数
```

#### 4. 通过 AI 执行
在当前会话中，我可以使用 `exec` 工具调用该脚本：
```javascript
exec({
  command: `node /tmp/update_doc_direct.js "${docId}" "${markdown}" "${mode}"`
})
```

## 飞书周文档标准格式模板

### 论文条目结构
```markdown
## #N 论文标题

**标题**: 英文标题  
**arXiv ID**: xxx  
**领域**: 领域1 / 领域2  

**核心内容**:
- **问题**: xxx
- **方法**: xxx
- **创新**: xxx
- **价值**: xxx
- **跨学科关联**: xxx

📄 arXiv原文: https://arxiv.org/abs/xxx  
📥 PDF下载: https://arxiv.org/pdf/xxx.pdf  
📝 注释稿详解: https://my.feishu.cn/docx/xxx ✅  
💬 深度讨论Q&A: https://www.feishu.cn/docx/xxx ⭐ 新增

> 💡 **推荐阅读顺序**: 先看arXiv原文 → 再看注释稿 → 最后看深度讨论Q&A
```

### 关键格式要素
1. **四个链接**（每行独立，带 emoji 前缀）：
   - 📄 arXiv原文: URL
   - 📥 PDF下载: URL
   - 📝 注释稿详解: URL ✅
   - 💬 深度讨论Q&A: URL ⭐ 新增

2. **推荐阅读顺序**（引用块格式）：
   ```markdown
   > 💡 **推荐阅读顺序**: 先看arXiv原文 → 再看注释稿 → 最后看深度讨论Q&A
   ```

3. **文档末尾**：更新日志（时间戳 + 更新内容列表）

## 临时解决方案
在新会话启动或工具调用格式修复之前，使用 Node.js 脚本作为替代方案完成文档更新。

## 创建时间
2026-03-24
