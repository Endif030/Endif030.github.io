# Research Pack 协议（写作侧）

## 命名规则
- 研究包：`R-公司代码-YYYYMMDD-vN`
- 文章包：`W-公司代码-基于R版本-vN`

## 最小文件集合
- `meta.yaml`：公司、范围、时间、作者、版本
- `evidence-ledger.csv`：证据台账（来源、下载时间、核验状态）
- `tables/financials.csv`
- `tables/profitability.csv`
- `tables/leverage.csv`
- `tables/business_mix.csv`
- `tables/timeline.csv`
- `notes/key-findings.md`

## 写作规则
1. 每个关键判断需映射到底表字段或证据台账。
2. 若 evidence-ledger 中某项 `verified=N`，正文中必须标注“待核验”。
3. 不得新增未在研究包中出现的具体数据。
4. 输出末尾附“数据口径与来源摘要”。

## 输出质量门槛
- 图文一致
- 口径一致
- 结论可追溯
