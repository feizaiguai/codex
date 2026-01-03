# 53-newsapi - NewsAPI全球科技新闻分析器

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org)

基于NewsAPI.org的全球科技新闻分析器。

## ✨ 核心功能

- 📰 **全球覆盖** - 70,000+新闻源
- 🔍 **分类筛选** - technology, business, science等
- ⚡ **实时更新** - 最新科技新闻
- 🔑 **免费层** - 100次/天
- 🛡️ **备用API** - 4个备用方案

## 🚀 快速开始

### 获取API Key

1. 访问 https://newsapi.org/register
2. 免费注册
3. 获取API key
4. 设置环境变量：`export NEWSAPI_KEY=your_key`

### 使用

```bash
# Headlines模式
python 53-newsapi/handler.py --api-key YOUR_KEY

# 搜索AI新闻
python 53-newsapi/handler.py --mode everything --query "AI" --api-key YOUR_KEY
```

## 🎯 触发关键词

- "全球科技新闻"
- "NewsAPI"
- "国际AI新闻"

## 📦 备用API

1. **NewsAPI.ai** - 实时新闻聚合
2. **NewsCatcher API** - 结构化数据
3. **NewsData.io** - 200次/天
4. **TheNewsAPI** - 免费JSON API

## 📝 版本历史

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布

## 📄 许可证

MIT License
