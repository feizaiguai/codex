# References - 参考文档

本目录包含51-hackernews skill的参考文档和资源。

## 📚 参考资料

### 官方文档
- [Hacker News官方API](https://github.com/HackerNews/API) - 官方API文档
- [Hacker News](https://news.ycombinator.com) - HN官网

### 备用API文档
- [Algolia HN Search API](https://hn.algolia.com/api) - Algolia搜索API
- [HN Unofficial API](https://github.com/cheeaun/node-hnapi) - 非官方RESTful API
- [HN RSS源](https://news.ycombinator.com/rss) - 官方RSS订阅

## 🔧 Progressive Disclosure

本skill遵循Progressive Disclosure设计原则：

**Layer 1 (Metadata)**: SKILL.md的YAML frontmatter (~100 tokens)
**Layer 2 (Core Instructions)**: SKILL.md的主要内容 (<3000 tokens)
**Layer 3 (References)**: 本目录的详细参考文档（按需加载）

Claude会根据任务需求自动加载相关参考文档，避免不必要的Token消耗。

## 📖 API详解

### HN官方API结构

#### 1. Top Stories
```
GET https://hacker-news.firebaseio.com/v0/topstories.json

返回: [123456, 123457, 123458, ...]
```

#### 2. Item详情
```
GET https://hacker-news.firebaseio.com/v0/item/123456.json

返回: {
  "by": "username",
  "descendants": 评论数,
  "id": 123456,
  "kids": [评论ID数组],
  "score": 分数,
  "time": Unix时间戳,
  "title": "标题",
  "type": "story",
  "url": "链接"
}
```

#### 3. Item类型
- `story` - 故事
- `comment` - 评论
- `job` - 招聘
- `poll` - 投票
- `pollopt` - 投票选项

### Algolia API详解

#### 搜索首页故事
```bash
curl "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10"
```

#### 参数说明
- `tags`: 标签筛选（front_page, story, comment等）
- `hitsPerPage`: 每页结果数
- `page`: 页码（从0开始）
- `query`: 搜索关键词

## 🛡️ 错误处理

### 常见错误

#### 1. 网络超时
```python
# 增加timeout参数
requests.get(url, timeout=15)
```

#### 2. Story详情为空
```python
# 某些story可能已被删除或没有url
if story_data and story_data.get('title'):
    # 处理story
```

#### 3. Unicode编码问题
```python
# 使用UTF-8编码
with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
```

## 💡 最佳实践

### 使用建议

1. **快速模式优先** - 日常使用建议使用`--no-analysis`
2. **数量控制** - 默认10条足够，避免过多
3. **定时任务** - 配置cron定时获取
4. **错误重试** - API失败时使用备用API

### 优化建议

1. **缓存Story IDs** - 避免频繁请求topstories.json
2. **并发获取** - 可使用线程池并发获取story详情
3. **增量更新** - 只获取新增的stories
4. **过滤低分** - 可过滤score < 100的stories

## 🔄 更新日志

### 2025-12-29
- 初始版本发布
- 支持HN官方API
- 集成15-web-search
- 提供3个备用API方案
