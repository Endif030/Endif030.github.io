# AI阅读周历史文档索引

| 周次 | 日期 | 主题 | 飞书文档链接 | 状态 | 备注 |
|------|------|------|-------------|------|------|
| 第1周 | 2026-03-09 | AI多领域应用 | https://my.feishu.cn/docx/CAOvdTeZ3oyScyxvDIvcDKQWnl0 | ✅ 已完成 | 7篇全部完成，已删除，由v2替代 |
| 第1周(v2) | 2026-03-24 | AI多领域应用 | https://my.feishu.cn/docx/CJU1dsyP0odefLxg6e5ckSlOnpg | ✅ 已完成 | 格式优化版，完整7篇+注释稿 |

---

## 本地备份

| 周次 | 本地文件 | 备份日期 |
|------|----------|----------|
| 第1周 | `weeks/AI阅读周_2026-03-09.md` | 2026-03-09 |
| 第1周(v2) | `weeks/AI阅读周_2026-03-24.md` | 2026-03-24 |

---

## 半自动化流程说明

### 每周执行步骤（周一上午）

**步骤1: 收集论文** (需要确认)
- 执行论文收集脚本
- 从arXiv等源获取7篇本周论文
- 输出: 论文列表（标题、arXiv ID、领域）

**步骤2: 生成周文档** (需要确认)
- 读取模板 `template.md`
- 填充论文信息到占位符
- 生成本地 Markdown 文件
- 输出: `weeks/AI阅读周_YYYY-MM-DD.md`

**步骤3: 上传飞书** (需要确认)
- 创建飞书云文档
- 输出: 飞书文档链接

**步骤4: 更新索引** (自动)
- 记录到 `weeks_index.md`

---

## 脚本工具

| 脚本 | 用途 | 位置 |
|------|------|------|
| weekly_reading_init.py | 半自动化周文档初始化 | `scripts/weekly_reading_init.py` |

**使用方式**:
```bash
python /root/.openclaw/workspace/skills/paper-reading-week/scripts/weekly_reading_init.py
```

---

## 定时任务

| 任务名 | 时间 | 说明 |
|--------|------|------|
| weekly-reading-init | 每周一 09:00 | 提醒执行周文档初始化流程 |

---

*最后更新: 2026-03-25*
