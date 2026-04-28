---
name: listed-company-writing
description: 上市公司文章撰写技能。基于已完成的 Research Pack（研究包）进行结构化成文与图表说明生成。仅负责写作与表达，不负责原始资料收集。
---

# Listed Company Writing

## 适用场景
当用户要求：
- 根据已有研究资料输出完整文章
- 按固定文风与结构生成上市公司拆解稿
- 仅做写作，不做资料采集

## 职责边界
- ✅ 负责：成文、结构化叙述、图表解读、风险提示
- ❌ 不负责：抓取原始资料、公告下载、证据核验

## 输入要求（强制）
必须指定或读取一个 Research Pack，包含：
1. `meta.yaml`
2. `evidence-ledger.csv`
3. `tables/*.csv`
4. `notes/*.md`

无 Research Pack 时，需明确提示先走 `desk-research-pro`。

## 输出结构（默认）
1. 公司基础画像
2. 核心业务逻辑
3. 产业链位置与议价权
4. 行业景气与竞争格局
5. 财务质量分析
6. 公司履历（时间轴）
7. 总结与风险提示
8. 引用来源摘要

## 版本规则
- 文章版本：`W-公司代码-基于R版本-vN`
- 示例：`W-301382-R20260429v1-v1`

## 变更标签
- `narrative-update`：仅文字表达调整
- `data-update`：数据更新触发重写
- `validation-update`：证据核验导致修订

详见 references/pack-protocol.md
