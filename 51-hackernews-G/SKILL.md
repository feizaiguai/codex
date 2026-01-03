---
name: 51-hackernews-G
description: Hacker News trending analyzer. Fetches top stories from official Hacker News API, optionally searches background info. Use when user asks for HN trends, tech discussions, or startup news.
---

# Hacker News - Hacker News趋势分析器

**Version**: 1.0.0
**Category**: Social Media
**Priority**: P2
**Last Updated**: 2025-12-29

---

## Description

Hacker News趋势分析器基于官方HN API，自动获取技术社区最热门的讨论和新闻。

### Core Capabilities

- **官方API**: 使用完全免费的Hacker News官方API
- **热门故事**: 获取首页top stories（默认10条）
- **详细信息**: 包含分数、作者、评论数、发布时间
- **背景搜索**: 可选使用15-web-search搜索背景信息
- **快速模式**: 支持--no-analysis跳过背景搜索

---

## Instructions

### When to Activate

触发此skill的场景：

1. **技术趋势** - 用户想了解最新技术讨论
2. **创业资讯** - 关注startup和产品发布
3. **技术社区** - 查看HN社区关注的话题
4. **开发者资讯** - 获取开发者关心的新闻

**触发关键词**:
- "HackerNews热搜"
- "HN趋势"
- "Hacker News热门"

### Execution Flow

```mermaid
graph TD
    A[接收用户请求] --> B[获取Top Story IDs]
    B --> C[逐个获取故事详情]
    C --> D{是否需要背景信息?}
    D -->|是| E[15-web-search搜索]
    D -->|否| F[跳过搜索]
    E --> G[生成Markdown报告]
    F --> G
    G --> H[返回结果]
```

**执行特点**:
- **快速模式**: 使用`--no-analysis`只获取基本信息（2-5秒）
- **完整模式**: 包含背景搜索（30-60秒）
- **官方数据**: 直接从HN Firebase API获取

---

## TypeScript Interfaces

```typescript
/**
 * HN故事配置
 */
interface HNInput {
  /**
   * 返回的故事数量 (默认: 10)
   */
  limit?: number;

  /**
   * 是否跳过背景搜索 (默认: false)
   */
  noAnalysis?: boolean;
}

/**
 * HN故事数据
 */
interface HNStoryItem {
  /**
   * 排名
   */
  rank: number;

  /**
   * 标题
   */
  title: string;

  /**
   * 原文链接
   */
  url: string;

  /**
   * 分数
   */
  score: number;

  /**
   * 作者
   */
  by: string;

  /**
   * 发布时间
   */
  time: string;

  /**
   * 评论数
   */
  comments: number;

  /**
   * HN讨论链接
   */
  hnUrl: string;

  /**
   * 背景信息（可选）
   */
  details?: {
    background?: string;
  };
}

/**
 * 输出结果
 */
interface HNOutput {
  /**
   * 故事列表
   */
  stories: HNStoryItem[];

  /**
   * Markdown报告
   */
  report: string;
}
```

---

## Usage Examples

### Example 1: 快速模式

**用户请求**:
```
HackerNews热搜
```

**Skill执行**:
```bash
python handler.py --limit 10 --no-analysis
```

**输出示例**:
```markdown
# 🟠 Hacker News热门故事

**生成时间**: 2025-12-29 15:30:00
**故事数量**: 10 个

---

## 1. Show HN: I built a tool to visualize Git branches

- **分数**: 523 分
- **作者**: johndoe
- **时间**: 2025-12-29 12:00:00 UTC
- **评论数**: 127
- **链接**: https://gitvisualizer.com
- **HN讨论**: https://news.ycombinator.com/item?id=123456

---
```

---

### Example 2: 完整模式

**用户请求**:
```
给我HackerNews热门故事，需要背景信息
```

**Skill执行**:
```bash
python handler.py --limit 10
```

包含每个故事的背景搜索结果。

---

## Implementation Details

### API配置

```python
@dataclass
class HNConfig:
    api_base: str = "https://hacker-news.firebaseio.com/v0"
    top_stories_endpoint: str = "/topstories.json"
    item_endpoint: str = "/item/{id}.json"
    timeout: int = 10
```

### API调用流程

1. **获取Story IDs**:
   ```
   GET /v0/topstories.json
   返回: [123456, 123457, ...]
   ```

2. **获取Story详情**:
   ```
   GET /v0/item/123456.json
   返回: {
     "by": "username",
     "descendants": 评论数,
     "id": 123456,
     "score": 分数,
     "time": Unix时间戳,
     "title": "标题",
     "url": "链接"
   }
   ```

### 备用API方案

**方案1: Algolia HN Search API**
```python
# API: https://hn.algolia.com/api
# 获取top stories
GET https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10
```

**方案2: HN RSS源**
```python
# RSS: https://news.ycombinator.com/rss
# 解析XML获取故事
```

**方案3: HN Unofficial API**
```python
# GitHub: cheeaun/node-hnapi
# API: https://api.hnpwa.com/v0/news/1.json
```

---

## Error Handling

### 容错机制

1. **API失败**
   - 错误码: `API_ERROR`
   - 处理: 返回错误信息，建议使用备用API

2. **故事详情获取失败**
   - 错误码: `STORY_FETCH_ERROR`
   - 处理: 跳过该故事，继续获取下一个

3. **背景搜索超时**
   - 错误码: `SEARCH_TIMEOUT`
   - 处理: 记录错误，继续处理其他故事

4. **网络问题**
   - 错误码: `NETWORK_ERROR`
   - 处理: 使用备用API或稍后重试

---

## Best Practices

### 使用建议

1. **快速模式优先**: 日常使用建议使用`--no-analysis`
2. **数量控制**: 默认10条足够，避免过多
3. **定时任务**: 可配置为每日定时获取
4. **备用方案**: API失败时切换到Algolia或RSS

---

## Limitations

### 当前限制

1. **官方API限制**: 无明确rate limit，但建议合理使用
2. **无缓存机制**: 每次都重新抓取
3. **评论内容**: 当前只获取评论数，不获取评论内容
4. **Ask HN/Show HN**: 混合在top stories中，未单独分类

### 不支持的功能

- ❌ 评论内容抓取
- ❌ 用户信息详情
- ❌ 历史故事搜索
- ❌ 自定义排序（只支持top stories）

---

## Related Skills

**可选依赖**:
- **15-web-search**: 网络搜索（用于背景信息）

**可配合使用**:
- **36-deep-research**: 深度研究（深挖特定话题）
- **53-newsapi**: 全球科技新闻（补充资讯）

---

## Performance

### 性能指标

**快速模式**（推荐）:
- 获取10个故事: 2-5秒
- 报告大小: 约2000-3000 tokens

**完整模式**:
- 获取10个故事（含背景搜索）: 30-60秒
- 报告大小: 约4000-6000 tokens

---

## Backup APIs

### 1. Algolia HN Search API ⭐推荐

**优点**:
- 免费，无需认证
- 提供搜索、排序、筛选功能
- 响应快速

**API文档**: https://hn.algolia.com/api

**示例**:
```bash
# 获取首页故事
curl "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10"
```

### 2. HN Official RSS

**优点**:
- 官方支持
- 简单可靠

**RSS源**: https://news.ycombinator.com/rss

### 3. HN Unofficial API

**优点**:
- RESTful接口
- 数据结构清晰

**GitHub**: https://github.com/cheeaun/node-hnapi
**API**: https://api.hnpwa.com/v0/news/1.json

---

## Version History

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持HN官方API
- ✅ 集成15-web-search（可选）
- ✅ 快速模式支持
- ✅ 3个备用API方案

---

## License

MIT License - 详见项目根目录LICENSE文件
