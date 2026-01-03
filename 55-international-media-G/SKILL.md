---
name: 55-international-media-G
description: International social media aggregator. Automatically executes 3 platform analyzers in sequence (Hacker News, Reddit, NewsAPI) and generates a comprehensive report. Use when user says "国外社媒资讯" or asks for international tech/social media trends overview.
---

# International Media - 国外社媒资讯聚合器

**Version**: 1.0.0
**Category**: Social Media Aggregation
**Priority**: P1
**Last Updated**: 2025-12-29

---

## Description

国外社媒资讯聚合器是一个协调器skill，自动依次调用3个国外平台的资讯分析器（Hacker News、Reddit、NewsAPI），生成综合的国外社媒资讯报告。

### Core Capabilities

- **三平台联动**: 自动依次执行51-hackernews、52-reddit-trending、53-newsapi
- **一键聚合**: 用户只需说"国外社媒资讯"即可触发完整分析流程
- **综合报告**: 生成包含所有平台资讯的Markdown格式综合报告
- **错误容忍**: 单个平台失败不影响其他平台的执行

---

## Instructions

### When to Activate

触发此skill的场景：

1. **全球资讯需求** - 用户想一次性了解国外主要平台的热点
2. **趋势对比分析** - 需要对比不同平台的热点差异
3. **国际舆情监控** - 需要全面掌握国外社交媒体动态
4. **技术资讯** - 寻找国外技术社区的热门话题

**触发关键词**:
- **"国外社媒资讯"** ⭐唯一触发词

### Execution Flow

```mermaid
graph TD
    A[接收用户请求: 国外社媒资讯] --> B[初始化聚合器]
    B --> C[依次执行3个平台]

    C --> D1[51-hackernews]
    D1 --> D2[52-reddit-trending]
    D2 --> D3[53-newsapi]

    D3 --> E[收集所有结果]
    E --> F[生成综合报告]
    F --> G[返回Markdown格式]
```

**执行特点**:
- **串行执行**: 依次执行，确保不会并发冲突
- **快速模式**: 默认使用`--no-analysis`参数，只获取基本资讯
- **容错机制**: 单个平台失败不影响其他平台

---

## TypeScript Interfaces

```typescript
/**
 * 聚合器输入配置
 */
interface AggregatorInput {
  /**
   * 每个平台返回的资讯数量 (默认: 10)
   */
  limit?: number;

  /**
   * NewsAPI密钥（可选）
   */
  newsapiKey?: string;
}

/**
 * 平台执行结果
 */
interface PlatformResult {
  platformName: string;
  displayName: string;
  success: boolean;
  content: string;
  emoji: string;
}

/**
 * 综合报告输出
 */
interface AggregatedOutput {
  generatedAt: string;
  platformResults: PlatformResult[];
  successCount: number;
  failureCount: number;
  report: string;
}
```

---

## Usage Examples

### Example 1: 基本用法

**用户请求**:
```
国外社媒资讯
```

**Skill执行**:
1. 自动依次调用3个平台分析器
2. 每个平台获取10条资讯（默认）
3. 生成综合报告

**输出示例**:
```markdown
# 🌐 国外社媒资讯聚合报告

**生成时间**: 2025-12-29 15:30:00
**平台数量**: 3 个

## 📊 执行摘要
- **成功**: 3/3 个平台
- **失败**: 0/3 个平台

---

## 🟠 Hacker News
[Hacker News内容...]

---

## 🔴 Reddit
[Reddit内容...]

---

## 📰 NewsAPI
[NewsAPI内容...]

---
```

---

## Implementation Details

### 平台执行配置

```python
platforms = [
    {
        "name": "hackernews",
        "display_name": "Hacker News",
        "skill_path": "51-hackernews",
        "emoji": "🟠"
    },
    {
        "name": "reddit",
        "display_name": "Reddit",
        "skill_path": "52-reddit-trending",
        "emoji": "🔴"
    },
    {
        "name": "newsapi",
        "display_name": "NewsAPI",
        "skill_path": "53-newsapi",
        "emoji": "📰"
    }
]
```

### 执行策略

**快速模式**:
```bash
# 每个平台都使用--no-analysis参数
python handler.py --limit 10
```

**优点**:
- 速度快（每个平台2-5秒）
- 总耗时约10-20秒完成所有3个平台
- 获取核心资讯，满足大多数需求

**注意事项**:
- NewsAPI需要API密钥（免费注册）
- 可设置NEWSAPI_KEY环境变量或使用--newsapi-key参数

---

## Error Handling

### 容错机制

1. **单平台失败**
   - 错误码: `PLATFORM_ERROR`
   - 处理: 记录错误，继续执行下一个平台

2. **平台超时**
   - 错误码: `TIMEOUT_ERROR`
   - 处理: 60秒超时后终止该平台，继续下一个

3. **Skill未安装**
   - 错误码: `SKILL_NOT_FOUND`
   - 处理: 提示用户安装缺失的skill

4. **NewsAPI密钥缺失**
   - 错误码: `API_KEY_MISSING`
   - 处理: 提示用户设置密钥，继续其他平台

---

## Best Practices

### 使用建议

1. **NewsAPI配置**: 提前设置NEWSAPI_KEY环境变量
2. **快速模式**: 使用默认设置即可，速度快
3. **数量控制**: 默认10条足够，避免报告过长
4. **定时执行**: 可配置为每日定时任务

---

## Limitations

### 当前限制

1. **串行执行**: 平台依次执行，总耗时为各平台耗时之和
2. **依赖3个skills**: 所有3个平台skills必须已安装
3. **NewsAPI限制**: 免费层100次/天
4. **无缓存机制**: 每次都重新抓取数据

### 不支持的功能

- ❌ 并行执行（避免API并发冲突）
- ❌ 跨平台话题关联分析
- ❌ 热点趋势预测
- ❌ 自定义平台选择（固定3个平台）

---

## Related Skills

**依赖的3个平台Skills**:
- **51-hackernews**: Hacker News趋势分析器（必需）
- **52-reddit-trending**: Reddit热门讨论分析器（必需）
- **53-newsapi**: NewsAPI全球科技新闻分析器（必需）

**可配合使用**:
- **50-china-social-media**: 国内社媒资讯聚合器（对比国内外）
- **36-deep-research**: 深度研究助手（深挖特定话题）
- **15-web-search**: 网络搜索引擎（补充信息）

---

## Skill Dependencies

**必需依赖**（全部3个）:
- ✅ **51-hackernews** - Hacker News
- ✅ **52-reddit-trending** - Reddit
- ✅ **53-newsapi** - NewsAPI

**安装检查**:
```bash
# 检查所有依赖是否已安装
ls C:/Users/bigbao/.claude/skills/51-hackernews
ls C:/Users/bigbao/.claude/skills/52-reddit-trending
ls C:/Users/bigbao/.claude/skills/53-newsapi
```

---

## Performance

### 性能指标

**快速模式**（推荐）:
- 单平台耗时: 2-5秒
- 总耗时: 10-20秒
- 报告大小: 约6000-10000 tokens

---

## Version History

### v1.0.0 (2025-12-29)
- ✅ 初始版本发布
- ✅ 支持3个平台自动聚合
- ✅ 快速模式（--no-analysis）
- ✅ 综合报告生成
- ✅ 错误容忍机制

---

## License

MIT License - 详见项目根目录LICENSE文件
