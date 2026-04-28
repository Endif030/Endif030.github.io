---
name: spanish-learning-production
description: 西语学习系统生产化技能。统一使用专用 subagent 执行西语课程更新、练习系统迭代、发布与验收。
---

# Spanish Learning Production

## 触发条件
当用户提到以下任一意图时使用：
- 执行西语 skill
- 开始今天的西语学习
- 继续西语课程
- 更新西语学习页面 / 题库 / 复习规则

## 强制规则
1. **统一走专用 subagent** 处理西语相关任务，不混用其他执行流。
2. 学习系统采用双模块：
   - Learn（课程学习页）
   - Practice（批量练习页）
3. 复习系统采用艾宾浩斯节奏：1/2/4/7/15/30 天。
4. 学习压力阈值：
   - 常规模式：软15 / 硬20
   - 错题巩固模式：软25 / 硬35
5. 当新题覆盖复习知识点时，必须合并去重。

## 固定工作流
1. 读取当日课程数据（day-N）
2. 生成练习集（常规/巩固）
3. 执行阈值裁剪与顺延队列
4. 发布到 GitHub Pages
5. 回传验收链接与变更摘要

## 目录约定
- 运行项目：`projects/spanish-learning-studio/`
- 课程数据：`projects/spanish-learning-studio/js/curriculum.js`
- 复习引擎：`projects/spanish-learning-studio/js/reviewEngine.js`

## 发布约定
- 目标仓库：`Endif030/Endif030.github.io`
- 路径：`/spanish-learning-studio/`

详见 references 下的规则文件。
