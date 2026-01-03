---
name: 52-reddit-trending-G
description: Reddit trending analyzer. Fetches hot posts from r/popular, r/technology and other subreddits using Reddit JSON API. Use when user asks for Reddit trends or tech discussions.
---

# Reddit Trending - Reddit趋势分析器

**Version**: 1.0.0
**Category**: Social Media
**Priority**: P2
**Last Updated**: 2025-12-29

---

## Description

Reddit趋势分析器基于Reddit无认证JSON API，获取热门讨论和内容。

### Core Capabilities

- **无需认证**: 使用Reddit JSON API，无需API key
- **热门内容**: 支持r/popular、r/technology等subreddit
- **详细信息**: 包含分数、评论数、作者、发布时间
- **背景搜索**: 可选使用15-web-search搜索背景信息
- **快速模式**: 支持--no-analysis跳过背景搜索

---

## Instructions

### When to Activate

触发此skill的场景：

1. **技术讨论** - 用户想了解Reddit技术社区讨论
2. **热门话题** - 查看Reddit全站热门内容
3. **社区动态** - 关注特定subreddit的动态
4. **舆情分析** - 了解英文社交媒体讨论

**触发关键词**:
- "Reddit热搜"
- "Reddit趋势"
- "Reddit热门"

### Execution Flow

```mermaid
graph TD
    A[接收用户请求] --> B[获取r/popular热门帖子]
    B --> C[解析帖子详情]
    C --> D{是否需要背景信息?}
    D -->|是| E[15-web-search搜索]
    D -->|否| F[跳过搜索]
    E --> G[生成Markdown报告]
    F --> G
    G --> H[返回结果]
```

**支持的Subreddits**:
- `popular` - 全站热门（默认）
- `technology` - 技术
- `programming` - 编程
- `startups` - 创业
- `all` - 全部内容

---

## TypeScript Interfaces

```typescript
interface RedditInput {
  subreddit?: string;  // 默认: "popular"
  limit?: number;      // 默认: 10
  noAnalysis?: boolean; // 默认: false
}

interface RedditPost {
  rank: number;
  title: string;
  subreddit: string;
  author: string;
  score: number;
  numComments: number;
  url: string;
  permalink: string;
  createdUtc: string;
  selftext?: string;
  details?: {
    background?: string;
  };
}
```

---

## Usage Examples

### Example 1: 默认用法

**用户请求**:
```
Reddit热搜
```

**执行**:
```bash
python handler.py --no-analysis
```

### Example 2: 指定Subreddit

**用户请求**:
```
给我Reddit的技术板块热门讨论
```

**执行**:
```bash
python handler.py --subreddit technology --limit 10
```

---

## Implementation Details

### API端点

```python
# 无认证JSON API（主要）
BASE_URL = "https://www.reddit.com"
HOT_POSTS = "/r/{subreddit}/hot.json"

# 官方OAuth API（备用）
OAUTH_BASE = "https://oauth.reddit.com"
```

### 备用API方案

**方案1: Reddit官方OAuth API**
- 需要注册应用获取client_id和secret
- 更稳定，有更高的rate limit
- API文档: https://www.reddit.com/dev/api

**方案2: Pushshift API**
- 历史数据搜索
- API: https://api.pushshift.io/reddit/search/submission/

**方案3: Reddit RSS**
- RSS订阅: https://www.reddit.com/r/{subreddit}/.rss
- 简单但功能有限

---

## Best Practices

1. **快速模式优先** - 日常使用建议使用`--no-analysis`
2. **Subreddit选择** - 根据需求选择合适的subreddit
3. **Rate Limit** - 无认证API有限制，避免频繁请求
4. **User-Agent** - 必须设置合理的User-Agent

---

## Limitations

- 无认证API有rate limit（约60次/分钟）
- 部分私有subreddit无法访问
- 不支持实时推送
- 评论内容需单独获取

---

## Related Skills

**可选依赖**:
- **15-web-search** - 网络搜索（用于背景信息）

**可配合使用**:
- **51-hackernews** - Hacker News趋势
- **53-newsapi** - 全球科技新闻

---

## Version History

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持Reddit JSON API
- ✅ 集成15-web-search
- ✅ 3个备用API方案

---

## License

MIT License
