# 50-china-social-media - 国内社媒资讯聚合器

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org)

自动依次调用5个平台的资讯分析器，一键生成国内社媒全景式资讯报告。

## ✨ 核心功能

- 🌐 **五平台联动** - 自动执行微博、百度、抖音、微信、AI资讯5个分析器
- ⚡ **一键聚合** - 只需说"国内社媒资讯"即可触发完整分析
- 📊 **综合报告** - 生成包含所有平台的Markdown格式报告
- 🛡️ **容错机制** - 单个平台失败不影响其他平台执行

## 🚀 快速开始

### 在Claude中使用

直接对Claude说：
```
国内社媒资讯
```

Claude会自动依次调用5个平台的分析器，并返回综合报告。

### 命令行使用

```bash
# 安装依赖
pip install requests

# 执行聚合分析（默认每个平台10条）
python 50-china-social-media/handler.py

# 自定义每个平台返回5条
python 50-china-social-media/handler.py --limit 5

# 指定输出文件
python 50-china-social-media/handler.py --output report.md
```

## 📖 使用示例

### 示例1: 默认用法

**输入**:
```
国内社媒资讯
```

**输出**:
```markdown
# 🌐 国内社媒资讯聚合报告

**生成时间**: 2025-12-29 15:30:00
**平台数量**: 5 个

## 📊 执行摘要
- **成功**: 5/5 个平台
- **失败**: 0/5 个平台

---

## 🔥 微博热搜
### 1. [热搜话题1]
...

## 🔍 百度热搜
### 1. [热搜话题1]
...

## 🎵 抖音热搜
### 1. [热搜话题1]
...

## 💬 微信热搜
### 1. [热搜话题1]
...

## 🤖 AI资讯
### 1. [AI资讯1]
...
```

### 示例2: 自定义数量

**输入**:
```
给我国内社媒资讯，每个平台5条就够了
```

**执行**:
```bash
python handler.py --limit 5
```

## 📁 目录结构

```
50-china-social-media/
├── SKILL.md              # Skill主文档
├── README.md             # 本文件
├── handler.py            # 核心聚合逻辑
├── scripts/              # 可执行脚本
│   ├── README.md
│   └── aggregate.py
└── references/           # 参考文档
    └── README.md
```

## ⚙️ 配置

### 依赖的5个Skills

必须确保以下5个skills已安装：

```bash
# 检查依赖
ls C:/Users/bigbao/.claude/skills/14-weibo-trending
ls C:/Users/bigbao/.claude/skills/21-baidu-trending
ls C:/Users/bigbao/.claude/skills/28-douyin-trending
ls C:/Users/bigbao/.claude/skills/30-wechat-trending
ls C:/Users/bigbao/.claude/skills/49-ai-news
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--limit` | int | 10 | 每个平台返回的资讯数量 |
| `--output` | str | 自动生成 | 输出文件路径 |

## 🔧 技术特点

### 执行模式

**快速模式**（默认）:
- 每个平台使用`--no-analysis`参数
- 只获取核心资讯，不进行深度搜索
- 单平台耗时：2-5秒
- 总耗时：15-30秒

**优点**:
- ⚡ 速度快
- 📊 覆盖全面
- 💡 满足大多数需求

### 执行流程

```
1. 🔥 微博热搜 (14-weibo-trending)
   ↓
2. 🔍 百度热搜 (21-baidu-trending)
   ↓
3. 🎵 抖音热搜 (28-douyin-trending)
   ↓
4. 💬 微信热搜 (30-wechat-trending)
   ↓
5. 🤖 AI资讯 (49-ai-news)
   ↓
6. 📄 生成综合报告
```

### 容错机制

- ✅ 单个平台失败不影响其他平台
- ✅ 60秒超时自动终止并继续下一个
- ✅ 完整的错误日志记录
- ✅ 最终报告标注成功/失败状态

## 🔧 依赖

**必需依赖**（全部5个）:
- Python 3.8+
- requests库
- **14-weibo-trending** - 微博热搜分析器
- **21-baidu-trending** - 百度热搜分析器
- **28-douyin-trending** - 抖音热搜分析器
- **30-wechat-trending** - 微信热搜分析器
- **49-ai-news** - AI资讯分析器

## 📊 性能指标

### 快速模式（推荐）
- 单平台耗时: 2-5秒
- 总耗时: 15-30秒
- 报告大小: 约5000-8000 tokens

### 数据覆盖
- 5个主要平台
- 默认50条资讯（每平台10条）
- 全面覆盖国内社交媒体热点

## 🎯 触发关键词

在Claude中，以下关键词会自动触发此skill：

- **"国内社媒资讯"** ⭐唯一触发词

## ⚠️ 限制

- 串行执行（避免API并发冲突）
- 依赖5个平台skills，缺一不可
- 快速模式不包含深度分析
- 总耗时为各平台耗时之和

## 🔗 相关Skill

**核心依赖**:
- **14-weibo-trending** - 微博热搜分析器
- **21-baidu-trending** - 百度热搜分析器
- **28-douyin-trending** - 抖音热搜分析器
- **30-wechat-trending** - 微信热搜分析器
- **49-ai-news** - AI资讯分析器

**可配合使用**:
- **36-deep-research** - 深度研究助手（深挖特定话题）
- **15-web-search** - 网络搜索引擎（补充信息）

## 📦 安装说明

### 1. 确保5个平台Skills已安装

```bash
# 检查所有依赖
cd C:/Users/bigbao/.claude/skills

# 应该包含以下5个目录
14-weibo-trending/
21-baidu-trending/
28-douyin-trending/
30-wechat-trending/
49-ai-news/
```

### 2. 安装Python依赖

```bash
pip install requests
```

### 3. 测试聚合器

```bash
# 快速测试（每个平台3条，不含详细分析）
python 50-china-social-media/handler.py --limit 3
```

## 📝 版本历史

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持5个平台自动聚合
- ✅ 快速模式实现
- ✅ 综合报告生成
- ✅ 容错机制

## 📄 许可证

MIT License - 详见LICENSE文件

## 👥 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

- 项目: Claude Code Skills
- 作者: Claude Code Skills Team
- 版本: 1.0.0

---

## 🌟 特别说明

这是一个**协调器skill**，本身不进行数据抓取，而是协调调用5个独立的平台分析器。

**设计理念**:
- 单一职责：每个平台skill专注自己的数据源
- 松耦合：各平台独立运行，互不影响
- 易扩展：未来可轻松添加新平台
- 容错性：部分失败不影响整体

**术语映射**（已添加到CLAUDE.md）:
```
"国内社媒资讯" = 五平台联动资讯聚合
```
