# 30-wechat-trending - 微信热搜分析器

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org)

自动抓取微信实时热搜榜单，并为每个热搜话题搜索详细的新闻背景和上下文信息。

## ✨ 核心功能

- 💬 **实时热搜抓取** - 通过天行API获取微信实时热搜榜单
- 🔍 **智能话题分析** - 使用WebSearch为每个话题搜索背景信息
- 📝 **深度解读** - 自动生成话题摘要、关键信息和事件时间线
- 🎯 **自定义筛选** - 支持按排名、关键词筛选

## 🚀 快速开始

### 在Claude中使用

直接对Claude说：
```
今天微信热搜都有什么？
```

Claude会自动调用此skill并返回前10名热搜的详细分析。

### 命令行使用

```bash
# 安装依赖
pip install requests

# 获取默认前10名热搜
python 30-wechat-trending/handler.py

# 获取前5名
python 30-wechat-trending/handler.py --limit 5

# 搜索关键词
python 30-wechat-trending/handler.py --keyword "科技"

# 只要基本信息（不包含详细分析）
python 30-wechat-trending/handler.py --no-analysis
```

## 📖 使用示例

### 示例1: 获取默认热搜

**输入**:
```
微信现在有什么热点？
```

**输出**:
```markdown
# 💬 微信热搜榜

更新时间: 2025-12-29 14:30

## 🔥 Top 10 热搜话题

### 1. 【话题标题】

话题概述: [话题详细信息...]
背景信息: [背景...]
关键要点:
- 要点1
- 要点2

🔗 微信搜索: [话题标题](...)
---
```

### 示例2: 关键词搜索

**输入**:
```
微信热搜里有关于"经济"的话题吗？
```

**输出**:
返回所有包含"经济"关键词的热搜话题。

## 📁 目录结构

```
30-wechat-trending/
├── SKILL.md              # Skill主文档
├── README.md             # 本文件
├── handler.py            # 核心处理逻辑
├── scripts/              # 可执行脚本
│   ├── README.md
│   └── wechat_trending.py
├── references/           # 参考文档
│   └── README.md
└── core/                 # 核心模块（预留）
```

## ⚙️ 配置

### API密钥

默认使用内置API密钥。如需使用自己的密钥：

```python
from handler import WeChatTrendingConfig, WeChatTrendingAnalyzer

config = WeChatTrendingConfig(
    api_key="YOUR_API_KEY",
    limit=10,
    include_analysis=True
)

analyzer = WeChatTrendingAnalyzer(config)
report = analyzer.analyze()
print(report)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 内置 | 天行API密钥 |
| `limit` | int | 10 | 返回热搜数量 |
| `keyword` | str | None | 关键词筛选 |
| `include_analysis` | bool | True | 是否包含详细分析 |
| `timeout` | int | 10 | API请求超时（秒） |
| `max_retries` | int | 3 | 最大重试次数 |

## 🔧 依赖

**必需依赖**:
- Python 3.8+
- requests库
- **15-web-search skill**（必需，用于话题背景搜索）

**可选依赖**:
- 36-deep-research skill（用于深度话题研究）

## 📊 数据来源

### 主要数据源
- **API提供商**: 天行数据 (tianapi.com)
- **API接口**: https://apis.tianapi.com/wxhottopic/index
- **数据源**: 微信热搜榜
- **更新频率**: 实时更新
- **数据时效**: 实时

### 备用数据源

#### 选项1: 聚合数据
- **API提供商**: 聚合数据 (juhe.cn)
- **官方文档**: https://www.juhe.cn/docs/api/id/414
- **注册地址**: https://www.juhe.cn
- **特点**: 稳定可靠，完善售后支持
- **状态**: ⚠️ 需要注册获取API密钥

#### 选项2: 综合热榜API
- **功能**: 聚合多平台热搜（包括微信）
- **平台覆盖**: 微信热搜、微信搞笑榜、财经榜、八卦榜等
- **参考**: [免费综合热榜查询API](https://zhuanlan.zhihu.com/p/586514283)
- **状态**: ⚠️ 需要查看官方文档获取接口地址

#### 选项3: AA1.cn
- **API文档**: https://api.aa1.cn/doc/weibo-rs.html
- **响应格式**: JSON
- **状态**: ⚠️ 需要查看官方文档

#### 选项4: 天行API - 微信文章精选 ⭐推荐
- **API接口**: https://apis.tianapi.com/wxnew/index
- **功能**: 获取微信精选文章（非热搜榜单）
- **数据**: 完整文章信息（标题、描述、链接、作者等）
- **特点**: 天行API官方接口，稳定可靠
- **状态**: ✅ 已测试可用

**使用说明**:
- 主API（wxhottopic）：热搜榜单 - 当前使用
- 备用API（wxnew）：精选文章 - 内容补充
- 其他备用API：商业级稳定方案

## 🎯 触发关键词

在Claude中，以下关键词会自动触发此skill：

- "微信热搜"、"微信热点"
- "wechat trending"
- "现在微信上什么最火"
- "今天微信有什么热点"
- "帮我看看微信热搜榜"

## ⚠️ 限制

- 依赖天行API，受其更新频率和配额限制
- WebSearch结果质量取决于网络可访问性
- 主要支持中文热搜
- API有调用次数限制
- 不提供热度指数（仅排名）

## 🔗 相关Skill

- **15-web-search** - 网络搜索引擎（**必需依赖**，用于话题背景搜索）
- **14-weibo-trending** - 微博热搜分析器（类似功能，不同平台）
- **21-baidu-trending** - 百度热搜分析器（类似功能，不同平台）
- **28-douyin-trending** - 抖音热搜分析器（类似功能，不同平台）
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
python 30-wechat-trending/handler.py --limit 3 --no-analysis

# 测试完整功能（包含15-web-search）
python 30-wechat-trending/handler.py --limit 2
```

## 📝 版本历史

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持天行API热搜抓取
- ✅ 集成WebSearch话题分析
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
