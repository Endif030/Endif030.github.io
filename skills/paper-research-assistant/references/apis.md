# 论文平台API参考

## arXiv API

### 端点
```
http://export.arxiv.org/api/query
```

### 参数
| 参数 | 说明 | 示例 |
|------|------|------|
| search_query | 搜索查询 | `cat:cs.AI` |
| start | 起始位置 | `0` |
| max_results | 最大结果数 | `10` |
| sortBy | 排序方式 | `relevance`, `lastUpdatedDate`, `submittedDate` |
| sortOrder | 排序顺序 | `ascending`, `descending` |

### 分类代码（部分）
| 代码 | 名称 |
|------|------|
| cs.AI | Artificial Intelligence |
| cs.LG | Machine Learning |
| cs.CL | Computation and Language (NLP) |
| cs.CV | Computer Vision |
| cs.RO | Robotics |
| cs.HC | Human-Computer Interaction |
| cs.CY | Computers and Society |
| q-bio.NC | Neurons and Cognition |

### Python示例
```python
import requests
import xml.etree.ElementTree as ET

def fetch_arxiv_papers(category, max_results=10):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{category}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    response = requests.get(url, params=params)
    # 解析Atom XML...
```

### 速率限制
- 建议请求间隔：3秒
- 批量请求时使用间隔避免被封

## Semantic Scholar API

### 端点
```
https://api.semanticscholar.org/graph/v1
```

### 论文搜索
```
GET /paper/search
```

参数：
| 参数 | 说明 |
|------|------|
| query | 搜索关键词 |
| fields | 返回字段 |
| limit | 结果数量 |
| publicationDateOrYear | 发表年份过滤 |

### 示例请求
```python
import requests

def search_semantic_scholar(query, fields=None, limit=10):
    if fields is None:
        fields = "paperId,title,abstract,year,citationCount,authors,url"
    
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "fields": fields,
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    return response.json()
```

### 获取论文详情
```
GET /paper/{paper_id}
```

### 批量获取
```
POST /paper/batch
```

## Crossref API

### 端点
```
https://api.crossref.org/works
```

### 参数
| 参数 | 说明 |
|------|------|
| query | 搜索查询 |
| filter | 过滤器 |
| rows | 结果数量 |
| sort | 排序方式 |

### DOI解析
```python
import requests

def resolve_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    return response.json()["message"]
```

## 通用字段映射

不同API返回的字段需要统一映射：

| 统一字段 | arXiv | Semantic Scholar | Crossref |
|----------|-------|------------------|----------|
| id | id | paperId | DOI |
| title | title | title | title[0] |
| abstract | summary | abstract | abstract |
| authors | authors/author/name | authors/name | author/name |
| year | published | year | published-print/date-parts[0][0] |
| url | id | url | URL |
| pdf_url | 拼接 | openAccessPdf/url | link[0][URL] |
| citation_count | - | citationCount | is-referenced-by-count |

## 错误处理

### arXiv
- HTTP 503: 服务繁忙，稍后重试
- 解析错误：检查XML命名空间

### Semantic Scholar
- HTTP 429: 速率限制，等待后重试
- HTTP 404: 论文不存在

### Crossref
- HTTP 503: 服务繁忙
- 空结果：检查查询语法
