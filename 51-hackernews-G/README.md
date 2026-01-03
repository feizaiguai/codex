# 51-hackernews - Hacker News趋势分析器

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org)

基于Hacker News官方API的趋势分析器，获取技术社区最热门的讨论和新闻。

## ✨ 核心功能

- 🟠 **官方API** - 使用完全免费的HN Firebase API
- 📊 **热门故事** - 获取首页top stories（默认10条）
- 🔍 **背景搜索** - 可选集成15-web-search搜索背景信息
- ⚡ **快速模式** - 支持--no-analysis跳过背景搜索（2-5秒）
- 🛡️ **备用方案** - 提供3个备用API

## 🚀 快速开始

### 在Claude中使用

直接对Claude说：
```
HackerNews热搜
```

### 命令行使用

```bash
# 安装依赖
pip install requests

# 快速模式（推荐）
python 51-hackernews/handler.py --no-analysis

# 完整模式（含背景搜索）
python 51-hackernews/handler.py --limit 10

# 指定输出文件
python 51-hackernews/handler.py --output hn_report.md
```

## 📖 使用示例

### 示例1: 快速模式

**输入**:
```
HackerNews热搜
```

**输出**:
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

## 📁 目录结构

```
51-hackernews/
├── SKILL.md              # Skill主文档
├── README.md             # 本文件
├── handler.py            # 核心分析逻辑
├── scripts/              # 可执行脚本
│   ├── README.md
│   └── fetch.py
└── references/           # 参考文档
    └── README.md
```

## ⚙️ 配置

### API端点

```python
# 官方API（主要）
BASE_URL = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES = "/topstories.json"
ITEM_DETAILS = "/item/{id}.json"

# 备用API
ALGOLIA_API = "https://hn.algolia.com/api/v1/search"
OFFICIAL_RSS = "https://news.ycombinator.com/rss"
UNOFFICIAL_API = "https://api.hnpwa.com/v0/news/1.json"
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--limit` | int | 10 | 返回的故事数量 |
| `--no-analysis` | flag | false | 跳过背景搜索（快速模式） |
| `--output` | str | 无 | 输出文件路径 |

## 🔧 技术特点

### 数据获取流程

```
1. 获取Top Story IDs
   ↓
2. 逐个获取故事详情
   ↓
3. [可选] 15-web-search背景搜索
   ↓
4. 生成Markdown报告
```

### 数据结构

```json
{
  "by": "username",
  "descendants": 127,
  "id": 123456,
  "score": 523,
  "time": 1735478400,
  "title": "Show HN: I built...",
  "type": "story",
  "url": "https://example.com"
}
```

## 🔧 依赖

**必需依赖**:
- Python 3.8+
- requests库

**可选依赖**:
- **15-web-search** - 背景信息搜索（推荐）

## 📊 性能指标

### 快速模式（推荐）
- 获取10个故事: 2-5秒
- 报告大小: 约2000-3000 tokens
- 无外部搜索调用

### 完整模式
- 获取10个故事（含背景搜索）: 30-60秒
- 报告大小: 约4000-6000 tokens
- 每个故事调用1次15-web-search

## 🎯 触发关键词

在Claude中，以下关键词会自动触发此skill：

- **"HackerNews热搜"** ⭐主要触发词
- "HN趋势"
- "Hacker News热门"

## ⚠️ 限制

- 官方API无明确rate limit，但建议合理使用
- 当前只获取评论数，不获取评论内容
- 不支持历史故事搜索和自定义排序

## 🔗 相关Skill

**可选依赖**:
- **15-web-search** - 网络搜索（用于背景信息）

**可配合使用**:
- **36-deep-research** - 深度研究助手（深挖特定话题）
- **53-newsapi** - 全球科技新闻（补充资讯）

## 📦 备用API

### 1. Algolia HN Search API ⭐推荐

```bash
curl "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10"
```

**优点**:
- 免费，无需认证
- 提供搜索、排序、筛选
- 响应快速

### 2. HN Official RSS

```bash
curl "https://news.ycombinator.com/rss"
```

**优点**:
- 官方支持
- 简单可靠

### 3. HN Unofficial API

```bash
curl "https://api.hnpwa.com/v0/news/1.json"
```

**优点**:
- RESTful接口
- 数据结构清晰

## 📝 版本历史

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持HN官方API
- ✅ 集成15-web-search（可选）
- ✅ 快速模式支持
- ✅ 3个备用API方案

## 📄 许可证

MIT License - 详见LICENSE文件

## 👥 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

- 项目: Claude Code Skills
- 作者: Claude Code Skills Team
- 版本: 1.0.0

---

## 🌟 为什么选择Hacker News？

- **技术社区标杆** - 最活跃的技术讨论社区
- **高质量内容** - 严格的内容质量控制
- **创业生态** - Y Combinator官方社区
- **免费API** - 完全免费，无限制使用
