# 52-reddit-trending - Reddit趋势分析器

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org)

基于Reddit无认证JSON API的趋势分析器，获取热门讨论和内容。

## ✨ 核心功能

- 🔴 **无需认证** - 使用JSON API，无需API key
- 📊 **热门内容** - 支持r/popular、r/technology等subreddit
- 🔍 **背景搜索** - 可选集成15-web-search
- ⚡ **快速模式** - 支持--no-analysis（2-5秒）
- 🛡️ **备用方案** - 提供官方OAuth API等备用方案

## 🚀 快速开始

### 在Claude中使用

```
Reddit热搜
```

### 命令行使用

```bash
# 快速模式（推荐）
python 52-reddit-trending/handler.py --no-analysis

# 指定subreddit
python 52-reddit-trending/handler.py --subreddit technology

# 完整模式
python 52-reddit-trending/handler.py --limit 10
```

## 📖 支持的Subreddits

- `popular` - 全站热门（默认）
- `technology` - 技术
- `programming` - 编程
- `startups` - 创业
- `all` - 全部内容

## ⚙️ 配置

### API端点

```python
# 无认证JSON API（主要）
https://www.reddit.com/r/{subreddit}/hot.json

# 官方OAuth API（备用）
https://oauth.reddit.com
```

## 🎯 触发关键词

- "Reddit热搜"
- "Reddit趋势"
- "Reddit热门"

## 📦 备用API

1. **Reddit官方OAuth API** - 需要注册应用
2. **Pushshift API** - 历史数据搜索
3. **Reddit RSS** - RSS订阅

## 📝 版本历史

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持Reddit JSON API
- ✅ 集成15-web-search
- ✅ 3个备用API方案

## 📄 许可证

MIT License
