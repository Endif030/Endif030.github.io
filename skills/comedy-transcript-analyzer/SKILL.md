# Comedy Transcript Analyzer

脱口秀逐字稿拆解分析工具 - 将脱口秀逐字稿拆解为笑点模块，生成带关系标注的PPT分析报告。

## 功能

- 📊 **笑点拆解**：将逐字稿拆解为独立笑点模块
- 🏷️ **主题分类**：自动/手动分类到不同主题
- 🔗 **关系标注**：标注笑点之间的承接、callback关系
- 📑 **PPT生成**：生成带颜色区分的可视化PPT报告

## 使用方法

### 1. 导入模块

```python
from analyzer import ComedyTranscriptAnalyzer

analyzer = ComedyTranscriptAnalyzer(output_dir="./output")
```

### 2. 准备数据

```python
jokes_data = [
    {
        "id": "1.1",
        "title": "开场钩子",
        "text": "笑点完整中文译文（英文原文）",
        "relation": "→ 承接1.X / → 【callback X.X】",
        "theme": "原生家庭"
    },
    # ... 更多笑点
]
```

### 3. 生成PPT

```python
output_path = analyzer.create_ppt(
    title="【主题名】笑点分析",
    jokes_data=jokes_data,
    filename="分析结果.pptx"
)
```

## 数据结构

### 笑点字典字段

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | str | 笑点编号，如 "1.1" |
| title | str | 笑点标题 |
| text | str | 完整译文（含英文原文括号标注） |
| relation | str | 关系说明，如 "承接1.1" 或 "【callback 1.5】" |
| theme | str | 主题分类，决定模块颜色 |

### 支持的主题

- `原生家庭` - 青绿色
- `恋爱关系` - 蓝色
- `表演生涯` - 薄荷绿
- `性身体` - 金黄色
- `生死心理` - 珊瑚色
- `社会观察` - 浅蓝色
- `默认` - 灰色

## 分析流程

1. **读取逐字稿**：获取脱口秀完整文本
2. **识别笑点**：按段落/逻辑切分独立笑点
3. **主题归类**：为每个笑点分配主题颜色
4. **关系标注**：标注承接、callback等关系
5. **生成PPT**：导出可视化分析报告

## 示例

见 `analyzer.py` 底部示例代码。
