---
name: 53-newsapi-G
description: NewsAPI global tech news analyzer. Fetches top headlines and AI news from NewsAPI.org. Supports category filter, keyword search. Use when user asks for global tech news or AI news.
---

# NewsAPI - 全球科技新闻分析器

**Version**: 1.0.0
**Category**: News
**Priority**: P2
**Last Updated**: 2025-12-29

---

## Description

NewsAPI全球科技新闻分析器基于NewsAPI.org，获取全球科技新闻和AI资讯。

### Core Capabilities

- **全球覆盖**: 支持70,000+新闻源
- **实时更新**: 获取最新科技新闻
- **分类筛选**: 支持technology, business, science等类别
- **关键词搜索**: 支持自定义关键词搜索
- **免费层**: 100次/天

---

## Instructions

### When to Activate

触发此skill的场景：

1. **全球科技新闻** - 用户想了解国际科技动态
2. **AI资讯** - 关注AI行业新闻
3. **创业新闻** - 查看全球创业资讯
4. **商业资讯** - 获取商业科技新闻

**触发关键词**:
- "全球科技新闻"
- "NewsAPI"
- "国际AI新闻"

### Execution Flow

```mermaid
graph TD
    A[接收用户请求] --> B{选择模式}
    B -->|Headlines| C[获取Top Headlines]
    B -->|Everything| D[搜索特定主题]
    C --> E[解析文章]
    D --> E
    E --> F[生成Markdown报告]
    F --> G[返回结果]
```

**支持的类别**:
- `technology` - 科技（默认）
- `business` - 商业
- `science` - 科学
- `health` - 健康
- `entertainment` - 娱乐

---

## TypeScript Interfaces

```typescript
interface NewsAPIInput {
  mode?: "headlines" | "everything";  // 默认: "headlines"
  category?: string;  // 默认: "technology"
  query?: string;     // 搜索关键词
  limit?: number;     // 默认: 10
  apiKey?: string;    // API密钥
}

interface NewsArticle {
  rank: number;
  title: string;
  description: string;
  source: string;
  author: string;
  url: string;
  publishedAt: string;
  content?: string;
  urlToImage?: string;
}
```

---

## Usage Examples

### Example 1: Top Headlines

**用户请求**:
```
全球科技新闻
```

**执行**:
```bash
python handler.py --mode headlines --category technology
```

### Example 2: 搜索AI新闻

**用户请求**:
```
搜索最近的AI新闻
```

**执行**:
```bash
python handler.py --mode everything --query "artificial intelligence OR AI"
```

---

## Implementation Details

### API配置

```python
BASE_URL = "https://newsapi.org/v2"
ENDPOINTS = {
    "top_headlines": "/top-headlines",
    "everything": "/everything",
    "sources": "/sources"
}
```

### 获取API Key

1. 访问 https://newsapi.org/register
2. 免费注册账号
3. 获取API key
4. 设置环境变量：`export NEWSAPI_KEY=your_key`

### 备用API方案

**方案1: NewsAPI.ai** ⭐推荐
- API: https://newsapi.ai
- 特点: 实时新闻聚合，支持多语言
- 免费层: 有限制

**方案2: NewsCatcher API**
- API: https://newscatcherapi.com
- 特点: 干净结构化的新闻数据
- 免费试用: 有限额

**方案3: NewsData.io**
- API: https://newsdata.io
- 特点: 实时和历史新闻
- 免费层: 200次/天

**方案4: TheNewsAPI**
- API: https://www.thenewsapi.com
- 特点: 免费JSON API
- 无需注册: 部分功能

---

## Best Practices

1. **API Key管理** - 使用环境变量存储，不要硬编码
2. **Rate Limit** - 免费层100次/天，合理使用
3. **缓存策略** - 缓存结果避免重复请求
4. **错误处理** - API失败时使用备用方案

---

## Limitations

- 免费层100次/天（付费版无限制）
- 某些来源需要付费
- 历史数据有限制（免费层最多1个月）
- 不支持实时推送

---

## Related Skills

**可配合使用**:
- **51-hackernews** - Hacker News趋势
- **52-reddit-trending** - Reddit讨论
- **49-ai-news** - 国内AI资讯

---

## Performance

### 性能指标
- 单次请求: 1-3秒
- 报告大小: 约3000-6000 tokens
- 免费配额: 100次/天

---

## Version History

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持NewsAPI.org
- ✅ Top Headlines模式
- ✅ Everything搜索模式
- ✅ 4个备用API方案

---

## License

MIT License
