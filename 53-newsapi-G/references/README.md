# References - 参考文档

## 📚 参考资料

### 官方文档
- [NewsAPI官方文档](https://newsapi.org/docs) - API文档
- [NewsAPI注册](https://newsapi.org/register) - 获取API key

### 备用API
- [NewsAPI.ai](https://newsapi.ai) - 实时新闻聚合
- [NewsCatcher API](https://newscatcherapi.com) - 结构化数据
- [NewsData.io](https://newsdata.io) - 200次/天
- [TheNewsAPI](https://www.thenewsapi.com) - 免费JSON

## 📖 API详解

### Top Headlines
```bash
curl "https://newsapi.org/v2/top-headlines?category=technology&apiKey=YOUR_KEY"
```

### Everything Search
```bash
curl "https://newsapi.org/v2/everything?q=AI&apiKey=YOUR_KEY"
```

## 💡 最佳实践

1. **环境变量** - 使用NEWSAPI_KEY存储密钥
2. **Rate Limit** - 免费层100次/天
3. **缓存** - 缓存结果避免重复请求
