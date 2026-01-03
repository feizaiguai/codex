# 49-ai-news - AI资讯分析器

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org)

自动抓取AI领域实时资讯，并为每条资讯搜索详细的新闻背景和深度解读。

## ✨ 核心功能

- 🤖 **实时资讯抓取** - 通过天行API获取AI领域最新资讯
- 🔍 **智能内容分析** - 使用WebSearch为每条资讯搜索背景信息
- 📝 **深度解读** - 自动生成资讯摘要、关键要点和技术分析
- 🎯 **自定义筛选** - 支持按数量、关键词筛选

## 🚀 快速开始

### 在Claude中使用

直接对Claude说：
```
今天AI领域有什么新闻？
```

Claude会自动调用此skill并返回前10条AI资讯的详细分析。

### 命令行使用

```bash
# 安装依赖
pip install requests

# 获取默认前10条AI资讯
python 49-ai-news/handler.py

# 获取前5条
python 49-ai-news/handler.py --limit 5

# 搜索关键词
python 49-ai-news/handler.py --keyword "谷歌"

# 只要基本信息（不包含详细分析）
python 49-ai-news/handler.py --no-analysis
```

## 📖 使用示例

### 示例1: 获取默认AI资讯

**输入**:
```
最新的AI动态有什么？
```

**输出**:
```markdown
# 🤖 AI资讯速递

更新时间: 2025-12-29 14:30

## 📰 Top 10 AI资讯

### 1. 【资讯标题】

📅 发布时间: 2025-12-29 00:00
📌 来源: IT家人工智能

📝 内容概述: [资讯描述...]
💡 深度解读: [背景信息...]
🔑 关键要点:
- 要点1
- 要点2

🔗 原文链接: [链接]
---
```

### 示例2: 关键词搜索

**输入**:
```
AI资讯里有关于"Meta"的吗？
```

**输出**:
返回所有包含"Meta"关键词的AI资讯。

## 📁 目录结构

```
49-ai-news/
├── SKILL.md              # Skill主文档
├── README.md             # 本文件
├── handler.py            # 核心处理逻辑
├── scripts/              # 可执行脚本
│   ├── README.md
│   └── ai_news.py
└── references/           # 参考文档
    └── README.md
```

## ⚙️ 配置

### API密钥

默认使用内置API密钥。如需使用自己的密钥：

```python
from handler import AINewsConfig, AINewsAnalyzer

config = AINewsConfig(
    api_key="YOUR_API_KEY",
    limit=10,
    include_analysis=True
)

analyzer = AINewsAnalyzer(config)
report = analyzer.analyze()
print(report)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 内置 | 天行API密钥 |
| `limit` | int | 10 | 返回资讯数量 |
| `keyword` | str | None | 关键词筛选 |
| `include_analysis` | bool | True | 是否包含详细分析 |
| `timeout` | int | 10 | API请求超时（秒） |
| `max_retries` | int | 3 | 最大重试次数 |

## 🔧 依赖

**必需依赖**:
- Python 3.8+
- requests库
- **15-web-search skill**（必需，用于资讯背景搜索）

**可选依赖**:
- 36-deep-research skill（用于深度话题研究）

## 📊 数据来源

### 主要数据源
- **API提供商**: 天行数据 (tianapi.com)
- **API接口**: https://apis.tianapi.com/ai/index
- **数据源**: AI行业资讯
- **更新频率**: 实时更新
- **数据时效**: 实时

### 备用数据源

#### 选项1: 聚合数据
- **API提供商**: 聚合数据 (juhe.cn)
- **官方网站**: https://www.juhe.cn
- **特点**: 稳定可靠，完善售后支持
- **状态**: ⚠️ 需要注册获取API密钥

#### 选项2: NewsAPI
- **功能**: 全球新闻聚合（支持AI关键词筛选）
- **官方网站**: https://newsapi.org
- **特点**: 全球主流媒体覆盖，免费版每日100次调用
- **状态**: ⚠️ 需要注册获取API密钥

#### 选项3: 36氪API
- **功能**: 中国科技创投新闻
- **覆盖**: AI创业公司、融资信息、技术趋势
- **特点**: 聚焦中国科技创投领域，内容深度高
- **状态**: ⚠️ 需要查看官方文档

#### 选项4: AI新闻聚合RSS源 ⭐推荐
- **推荐源**: MIT Technology Review, VentureBeat AI, 量子位, 机器之心
- **特点**: 免费使用，内容权威，可通过RSS解析
- **状态**: ✅ 可用

**使用说明**:
- 主API（ai接口）：AI行业综合资讯 - 当前使用
- 备用API选项：提供更高可用性和多样化数据源
- RSS源：免费备选方案，适合长期稳定使用

## 🎯 触发关键词

在Claude中，以下关键词会自动触发此skill：

- "AI资讯"、"AI新闻"
- "ai news"
- "最新的AI动态"
- "今天AI领域有什么新闻"
- "帮我看看AI行业热点"

## ⚠️ 限制

- 依赖天行API，受其更新频率和配额限制
- WebSearch结果质量取决于网络可访问性
- 主要支持中文AI资讯
- API有调用次数限制
- 内容深度基于API提供的摘要

## 🔗 相关Skill

- **15-web-search** - 网络搜索引擎（**必需依赖**，用于资讯背景搜索）
- **14-weibo-trending** - 微博热搜分析器（社交媒体热点）
- **21-baidu-trending** - 百度热搜分析器（搜索引擎热点）
- **28-douyin-trending** - 抖音热搜分析器（短视频平台热点）
- **30-wechat-trending** - 微信热搜分析器（微信生态热点）
- **36-deep-research** - 深度研究助手（可选，用于深度挖掘）

## 📦 安装说明

### 1. 确保15-web-search skill已安装

```bash
# 检查15-web-search是否存在
ls C:/Users/bigbao/.claude/skills/15-web-search/

# 如果不存在，需要先安装15-web-search skill
```

### 2. 安装Python依赖

```bash
pip install requests
```

### 3. 测试skill

```bash
# 测试基本功能（不含详细分析）
python 49-ai-news/handler.py --limit 3 --no-analysis

# 测试完整功能（包含15-web-search）
python 49-ai-news/handler.py --limit 2
```

## 📝 版本历史

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持天行API资讯抓取
- ✅ 集成WebSearch资讯分析
- ✅ 默认Top 10展示
- ✅ 支持自定义筛选

## 📄 许可证

MIT License - 详见LICENSE文件

## 👥 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

- 项目: Claude Code Skills
- 作者: Claude Code Skills Team
- 版本: 1.0.0
