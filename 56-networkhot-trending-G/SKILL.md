---
name: 56-networkhot-trending-G
description: Network hot search analyzer. Fetches real-time trending topics from across major platforms (Weibo, Zhihu, Baidu, Douyin, Bilibili, etc.) via TianAPI, enriches each topic with detailed background, news coverage, and analysis using 15-web-search skill. Returns top 10 trending topics by default with comprehensive insights. Use for social media trends monitoring, public opinion tracking, hot topic analysis, content marketing research.
---

# Network Hot Search - 全网热搜分析器

**Version**: 1.0.0
**Category**: Social Media Analytics
**Priority**: P2
**Last Updated**: 2025-12-29

---

## Description

全网热搜分析器自动抓取全平台（微博、知乎、百度、抖音、B站等）实时热搜榜单，并为每个热搜话题搜索详细的背景信息、新闻报道和深度分析。默认返回前10个热搜话题的全方位解读，支持自定义数量和筛选条件。

### Core Capabilities

- **全平台热搜聚合**: 通过天行API获取微博、知乎、百度、抖音、B站等多平台热搜
- **智能背景搜索**: 使用15-web-search skill为每个热搜话题搜索背景信息、新闻报道和事件脉络
- **深度话题分析**: 自动生成话题摘要、关键要点、公众情绪和传播路径
- **实时更新**: 跟踪热搜榜单实时变化，捕捉突发热点
- **自定义筛选**: 支持按数量、关键词、平台等条件筛选热搜

---

## Instructions

### When to Activate

触发此skill的场景：

1. **社会热点追踪** - 用户想了解当前社会关注的热点话题和事件
2. **舆情监测** - 需要监控公众舆论方向和网络热点
3. **内容创作** - 寻找热门话题作为自媒体创作素材
4. **市场营销** - 借势热点进行营销策划和内容推广
5. **新闻线索** - 记者、编辑寻找新闻线索和选题方向
6. **趋势分析** - 分析社会关注点的变化趋势和公众情绪

**触发关键词（自动识别）**:
- "全网热搜"、"网络热搜"、"热搜榜"
- "现在什么最火"、"今天有什么热点"
- "全平台热搜"、"综合热搜"

---

## Usage Examples

### Example 1: 获取最新全网热搜TOP 10

**Input**:
```
今天全网热搜有哪些？
```

**Expected Output**:
- 自动调用handler.py获取全网热搜TOP 10
- 为每个热搜话题使用15-web-search搜索详细背景
- 生成包含话题摘要、新闻报道、公众情绪、关键要点的完整报告
- 输出Markdown格式的热搜分析报告

---

### Example 2: 自定义数量和关键词筛选

**Input**:
```
查看全网热搜前20个，重点关注"科技"相关话题
```

**Expected Output**:
- 获取前20个全网热搜
- 筛选出科技相关话题
- 提供每个话题的深度分析

---

### Example 3: 特定平台热搜分析

**Input**:
```
全网热搜中有哪些娱乐类话题？
```

**Expected Output**:
- 从全网热搜中筛选娱乐类话题
- 分析话题热度、传播路径和公众反应

---

## Implementation Details

### Core Process

1. **API数据获取**:
   - 调用天行API全网热搜接口：`https://apis.tianapi.com/networkhot/index`
   - 解析返回的热搜列表（包含标题、热度、来源平台等）

2. **背景信息搜索**:
   - 对每个热搜话题调用15-web-search skill
   - 搜索相关新闻报道、事件背景、专家评论
   - 整合多源信息形成完整话题画像

3. **深度分析生成**:
   - 提取话题核心要点
   - 分析公众情绪倾向
   - 总结事件发展脉络
   - 预测话题走向

4. **报告输出**:
   - 生成结构化的Markdown报告
   - 包含话题排名、热度指数、详细分析

### Handler Script

主要执行文件: `handler.py`

**核心功能模块**:
- `NetworkHotAnalyzer`: 全网热搜分析器主类
- `fetch_hot_topics()`: 从API获取热搜数据
- `enrich_with_search()`: 使用15-web-search丰富话题信息
- `analyze_topic()`: 分析单个话题的深度信息
- `generate_report()`: 生成Markdown格式报告

**调用示例**:
```bash
python handler.py --limit 10 --keyword "科技"
```

---

## Configuration

### Environment Variables

无需额外环境变量（API密钥已内置）

### Parameters

- `limit`: 返回热搜数量（默认: 10，最大: 50）
- `keyword`: 关键词筛选（可选）
- `include_analysis`: 是否包含深度分析（默认: true）
- `platforms`: 筛选特定平台（可选，如 "weibo,zhihu"）

---

## Dependencies

### Required Skills
- **15-web-search**: 必需，用于搜索每个热搜话题的背景信息和新闻报道

### Required Libraries
- `requests`: HTTP请求
- `json`: JSON数据处理
- `datetime`: 时间处理

### API Dependencies
- **天行数据API**: https://apis.tianapi.com/networkhot/index
  - 免费额度: 100次/天
  - API密钥: 已内置
  - 备用API: 无

---

## Output Format

### Markdown Report Structure

```markdown
# 全网热搜榜单

**更新时间**: 2025-12-29 14:30:00
**热搜数量**: 10个

---

## 🔥 TOP 1: [话题标题]

- **热度指数**: 1,234,567
- **来源平台**: 微博、知乎、百度
- **话题标签**: #科技 #人工智能

### 📰 事件背景
[通过15-web-search搜索到的背景信息]

### 🔍 新闻报道
[相关新闻汇总]

### 💬 公众情绪
[情绪分析：正面/中性/负面]

### 🎯 关键要点
- 要点1
- 要点2
- 要点3

---

## 🔥 TOP 2: [话题标题]
...
```

---

## Error Handling

### Common Issues

1. **API调用失败**
   - 错误: "API请求超时"
   - 解决: 自动重试3次，使用指数退避策略

2. **网络热搜为空**
   - 错误: "未获取到热搜数据"
   - 解决: 检查API密钥和网络连接

3. **15-web-search调用失败**
   - 错误: "背景信息搜索失败"
   - 解决: 降级为仅返回基础热搜列表

---

## Performance

- **执行时间**:
  - 基础版（无分析）: 2-5秒
  - 完整版（含深度分析）: 30-60秒（取决于热搜数量）
- **Token消耗**: 2000-4000 tokens
- **API调用**: 1次天行API + N次15-web-search（N=热搜数量）

---

## Version History

- **v1.0.0** (2025-12-29): 初始版本
  - 支持全网热搜数据获取
  - 集成15-web-search进行话题深度分析
  - 生成Markdown格式报告

---

## See Also

- **14-weibo-trending**: 微博热搜专项分析
- **21-baidu-trending**: 百度热搜专项分析
- **50-china-social-media**: 国内社媒资讯聚合器
- **15-web-search**: 网络搜索引擎
