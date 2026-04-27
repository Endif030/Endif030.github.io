# Subagent 执行手册（西语学习专用）

目标：将西语学习任务固定由单一 subagent 承载，避免与其他任务互相影响。

## 建议会话参数
- runtime: subagent
- agentId: main（当前环境可用）
- thread: true
- mode: session
- label: spanish-learning-agent

## 触发范围
- 生成周计划
- 生成 DayX 课程
- 语音练习反馈模板化输出
- 周复盘文档更新

## 产出要求
- 输出简洁可执行
- 回写学习文档
- 不输出过程性噪音说明
