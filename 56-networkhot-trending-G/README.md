# 56-networkhot-trending - 全网热搜分析器

## 📋 概述

全网热搜分析器自动抓取微博、知乎、百度、抖音、B站等多平台实时热搜榜单，并为每个热搜话题搜索详细的背景信息、新闻报道和深度分析。

## 🎯 核心功能

- ✅ 全平台热搜聚合（微博、知乎、百度、抖音、B站等）
- ✅ 智能背景搜索（使用15-web-search skill）
- ✅ 深度话题分析（摘要、要点、情绪、传播路径）
- ✅ 实时更新（跟踪热搜榜单变化）
- ✅ 自定义筛选（数量、关键词、平台）

## 🚀 快速开始

### 基础用法

```bash
# 获取最新全网热搜TOP 10
python handler.py

# 获取前20个热搜
python handler.py --limit 20

# 筛选特定关键词
python handler.py --keyword "科技"

# 快速模式（不含深度分析）
python handler.py --no-analysis

# 保存到文件
python handler.py --output networkhot_report.md
```

### 在Claude Code中使用

触发关键词：
- "全网热搜"、"网络热搜"、"热搜榜"
- "现在什么最火"、"今天有什么热点"
- "全平台热搜"、"综合热搜"

示例对话：
```
用户: 今天全网热搜有哪些？
Claude: [自动调用56-networkhot-trending，返回TOP 10热搜及详细分析]

用户: 查看全网热搜前20个，重点关注"娱乐"相关话题
Claude: [调用handler.py --limit 20 --keyword "娱乐"]
```

## 📊 输出示例

```markdown
# 全网热搜榜单

**更新时间**: 2025-12-29 14:30:00
**热搜数量**: 10 个

---

## 🔥 TOP 1: 某重大新闻事件

- **热度指数**: 1,234,567
- **话题链接**: https://...
- **话题标签**: 社会

### 📝 话题摘要
[事件简要描述]

### 🔍 背景信息与深度分析
[通过15-web-search搜索到的详细背景、新闻报道、专家评论]

---

## 🔥 TOP 2: ...
```

## 🔧 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--limit` | int | 10 | 返回热搜数量 |
| `--keyword` | str | None | 关键词筛选 |
| `--no-analysis` | flag | False | 不包含深度分析 |
| `--output` | str | None | 输出文件路径 |

## 📦 依赖

### 必需Skills
- **15-web-search**: 用于搜索每个热搜的背景信息

### Python库
- `requests`: HTTP请求
- `json`: JSON处理
- `datetime`: 时间处理

### API
- **天行数据API**: https://apis.tianapi.com/networkhot/index
  - 免费额度: 100次/天
  - API密钥: 已内置

## 🎭 使用场景

1. **社会热点追踪** - 了解当前社会关注焦点
2. **舆情监测** - 监控公众舆论和网络热点
3. **内容创作** - 寻找热门话题作为创作素材
4. **市场营销** - 借势热点进行营销策划
5. **新闻线索** - 发现新闻线索和选题方向
6. **趋势分析** - 分析社会关注点变化趋势

## 📈 性能指标

- **执行时间**:
  - 基础版（无分析）: 2-5秒
  - 完整版（含深度分析）: 30-60秒
- **Token消耗**: 2000-4000 tokens
- **API调用**: 1次天行API + N次15-web-search

## 🔗 相关Skills

- **14-weibo-trending**: 微博热搜专项分析
- **21-baidu-trending**: 百度热搜专项分析
- **28-douyin-trending**: 抖音热搜专项分析
- **30-wechat-trending**: 微信热搜专项分析
- **50-china-social-media**: 国内社媒资讯聚合器

## 📝 版本历史

- **v1.0.0** (2025-12-29): 初始版本
  - 支持全网热搜数据获取
  - 集成15-web-search进行深度分析
  - 生成Markdown格式报告

## 📄 License

MIT License
