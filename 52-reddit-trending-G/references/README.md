# References - 参考文档

本目录包含52-reddit-trending skill的参考文档和资源。

## 📚 参考资料

### 官方文档
- [Reddit API官方文档](https://www.reddit.com/dev/api) - 官方API文档
- [Reddit JSON API](https://github.com/reddit-archive/reddit/wiki/JSON) - JSON API说明

### 备用API文档
- [Pushshift API](https://pushshift.io) - 历史数据搜索
- [PRAW - Python Reddit API Wrapper](https://praw.readthedocs.io) - Python SDK

## 🔧 Progressive Disclosure

**Layer 1 (Metadata)**: SKILL.md的YAML frontmatter (~100 tokens)
**Layer 2 (Core Instructions)**: SKILL.md的主要内容 (<3000 tokens)
**Layer 3 (References)**: 本目录的详细参考文档（按需加载）

## 📖 API详解

### Reddit JSON API

#### 获取热门帖子
```bash
curl "https://www.reddit.com/r/popular/hot.json?limit=10"
```

#### 参数说明
- `limit`: 返回数量（最大100）
- `after`: 分页标识
- `t`: 时间范围（hour, day, week, month, year, all）

## 💡 最佳实践

1. **User-Agent设置** - 必须设置合理的User-Agent
2. **Rate Limit** - 无认证约60次/分钟
3. **缓存策略** - 建议缓存结果避免频繁请求
