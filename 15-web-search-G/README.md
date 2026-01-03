# 15-WebSearchFlow v3.0

**世界级AI驱动的智能网络搜索引擎**

集成6个搜索API，提供快速/自动/深度三种模式，支持语义去重、内容增强、智能路由。

---

## ✨ 核心特性

### 🚀 6个搜索引擎集成

| 引擎 | 类型 | 速度 | 特点 |
|------|------|------|------|
| **Exa.ai** | 语义搜索 | 快 | 神经网络理解查询意图 |
| **Brave Search** | 传统搜索 | 极快 | 隐私保护、索引丰富 |
| **Perplexity** | AI答案 | 中 | 直接生成答案而非链接 |
| **Jina Reader** | 内容提取 | 中 | 将网页转为Markdown |
| **Jina Embedding** | 语义理解 | 慢 | 用于相似度去重 |
| **You.com** | 混合搜索 | 快 | AI增强的传统搜索 |

### 🎯 三种搜索模式

```python
# Fast模式 - 5-7秒极速响应
result = await search("Python tutorial", mode="fast")

# Auto模式 - 8-12秒平衡性能
result = await search("React best practices", mode="auto")

# Deep模式 - 15-20秒深度分析 + AI答案
result = await search("What is quantum computing?", mode="deep")
```

| 模式 | 引擎组合 | 速度 | 使用场景 |
|------|----------|------|----------|
| **Fast** | Brave + You.com | 5-7s | 快速查询、实时搜索 |
| **Auto** | Exa Auto + Brave | 8-12s | 日常搜索、默认模式 |
| **Deep** | Exa Deep + Perplexity + You.com | 15-20s | 研究、深度分析 |
| **Code** | Exa Deep + Brave | 10-15s | 编程问题、代码示例 |

### 🧠 智能功能

1. **语义去重** - 使用Jina Embedding识别相似结果（0.85阈值）
2. **智能路由** - 根据查询类型自动选择最佳引擎组合
3. **查询优化** - 自动添加关键词提升搜索效果
4. **内容增强** - Jina Reader提取完整网页内容为Markdown
5. **相关性排序** - 综合引擎权重、排名、权威性评分
6. **质量指标** - 实时计算相关性、覆盖度、新鲜度

---

## 📦 快速开始

### 安装依赖

```bash
pip install httpx asyncio
```

### 最简单的用法

```python
import asyncio
from main import search

async def main():
    # 一行代码搞定
    result = await search("Python async programming")

    # 显示结果
    for r in result.results[:5]:
        print(f"{r.title}\n{r.url}\n")

asyncio.run(main())
```

### 基础示例

```python
from main import WebSearchFlow
from models import WebSearchInput

async def basic_search():
    # 创建搜索参数
    params = WebSearchInput(
        query="machine learning tutorial",
        mode="auto",
        max_results=10
    )

    # 执行搜索
    flow = WebSearchFlow()
    result = await flow.execute(params)

    print(f"找到 {result.total_results} 个结果")
    print(f"搜索时间: {result.search_time}ms")
    print(f"平均相关性: {result.quality['relevance_score']}/100")
```

---

## 📖 详细用法

### 1. Fast模式 - 极速搜索

```python
# 适合快速查询、实时搜索
result = await search(
    query="React hooks tutorial",
    mode="fast",
    max_results=10
)

print(f"搜索引擎: {result.engines_used}")  # ["brave", "you"]
print(f"搜索时间: {result.search_time}ms")  # ~5000-7000ms
```

### 2. Deep模式 - 深度搜索 + AI答案

```python
# 适合研究、深度分析
result = await search(
    query="What is the future of AI?",
    mode="deep",
    max_results=20
)

# 获取Perplexity AI答案
ai_answers = [r for r in result.results if r.engine == "perplexity"]
if ai_answers:
    print(f"AI答案: {ai_answers[0].snippet}")

# 查看推荐链接
for link in result.summary['recommended_links'][:3]:
    print(f"{link['title']}")
    print(f"{link['url']}")
    print(f"推荐理由: {link['reason']}\n")
```

### 3. 代码搜索模式

```python
params = WebSearchInput(
    query="Python decorator example",
    search_type="code",  # 自动使用Exa Deep + Brave
    max_results=10
)

result = await WebSearchFlow().execute(params)

# 代码搜索优化：自动添加"code example"等关键词
```

### 4. 自定义引擎组合

```python
params = WebSearchInput(
    query="TypeScript generics",
    search_engines=["exa_deep", "perplexity", "brave"],  # 自定义
    max_results=15
)

result = await WebSearchFlow().execute(params)
```

### 5. 完整内容提取

```python
# 使用Jina Reader提取完整网页内容
result = await search(
    query="OpenAI GPT-4",
    mode="fast",
    max_results=3,
    fetch_full_content=True  # 启用内容提取
)

for r in result.results:
    if r.full_content:
        print(f"完整内容: {len(r.full_content)} 字符")

        # 提取的代码块
        for snippet in r.code_snippets:
            print(f"代码块 ({snippet['language']}): {snippet['code']}")
```

### 6. 高级过滤

```python
params = WebSearchInput(
    query="machine learning",
    language="en",                           # 仅英文
    time_range="month",                      # 最近一个月
    site_filter=["github.com", "arxiv.org"], # 指定网站
    exclude_sites=["medium.com"],            # 排除网站
    deduplication=True,                      # 启用去重
    max_results=20
)

result = await WebSearchFlow().execute(params)
```

### 7. 查看质量指标

```python
result = await search("climate change", mode="deep")

quality = result.quality
print(f"相关性分数: {quality['relevance_score']}/100")
print(f"平均权威性: {quality['average_source_authority']}/100")
print(f"新鲜度分数: {quality['freshness_score']}/100")
print(f"覆盖度分数: {quality['coverage_score']}/100")
```

### 8. 导出结果

```python
import json

result = await search("Docker tutorial")

# 转换为字典
result_dict = result.to_dict()

# 保存为JSON
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(result_dict, f, ensure_ascii=False, indent=2)
```

---

## 🏗️ 架构设计

### 核心流程

```
用户查询
    ↓
1. 查询优化 (添加关键词、语言检测)
    ↓
2. 智能路由 (选择最佳引擎组合)
    ↓
3. 并行搜索 (多引擎异步调用)
    ↓
4. 去重处理 (URL去重 + 语义去重)
    ↓
5. 相关性排序 (多因子评分)
    ↓
6. 内容增强 (Jina Reader提取完整内容)
    ↓
7. 生成摘要 (高频域名、主题、推荐链接)
    ↓
8. 质量评估 (相关性、权威性、新鲜度、覆盖度)
    ↓
返回结果
```

### 智能路由规则

```python
# 查询类型 → 引擎选择
{
    "general": ["exa_auto", "brave"],           # 通用查询
    "code": ["exa_deep", "brave"],              # 编程问题
    "documentation": ["brave", "you"],          # 文档查询
    "stackoverflow": ["brave"],                 # Stack Overflow专用
    "research": ["exa_deep", "perplexity"]      # 研究分析
}

# 搜索模式 → 引擎选择
{
    "fast": ["brave", "you"],                   # 快速模式
    "auto": ["exa_auto", "brave"],              # 自动模式
    "deep": ["exa_deep", "perplexity", "you"]   # 深度模式
}
```

### 相关性排序算法

```python
final_score = (
    base_score * engine_weight +       # 基础分数 × 引擎权重
    rank_penalty +                      # 排名惩罚(越靠后越低)
    authority_bonus +                   # 权威性加成
    https_bonus                         # HTTPS加成
)

# 引擎权重
engine_weights = {
    "exa": 1.0,        # 语义搜索最高
    "perplexity": 0.95,
    "brave": 0.9,
    "you": 0.85
}
```

### 语义去重

```python
# 1. URL标准化去重
- 移除协议 (https:// → )
- 移除www前缀
- 移除尾随斜杠
- 移除查询参数
- 转小写

# 2. 语义相似度去重 (Jina Embedding v3)
- 提取标题 + 摘要
- 生成512维向量
- 计算余弦相似度
- 阈值0.85（超过则视为重复）
```

---

## 🔧 配置说明

### API配置 (config.py)

所有API密钥已预配置在 `config.py` 中：

```python
EXA_CONFIG = APIConfig(
    name="Exa.ai",
    endpoint="https://api.exa.ai/search",
    auth_type="header",
    auth_key="${EXA_API_KEY}",
    enabled=True,
    timeout=30
)

# ... 其他5个API配置
```

### 搜索模式配置

```python
SEARCH_MODES = {
    "fast": {
        "engines": ["brave", "you"],
        "max_results": 10,
        "fetch_full_content": False,
        "timeout": 10
    },
    "deep": {
        "engines": ["exa_deep", "perplexity", "you"],
        "max_results": 25,
        "fetch_full_content": True,
        "timeout": 30
    }
    # ... 其他模式
}
```

### 去重配置

```python
DEDUP_CONFIG = {
    "similarity_threshold": 0.85,  # 相似度阈值
    "url_normalization": True,     # URL标准化
    "content_dedup": True,          # 内容去重
    "use_embedding": True           # 使用语义嵌入
}
```

---

## 📊 数据模型

### SearchResult - 单条搜索结果

```python
@dataclass
class SearchResult:
    title: str                      # 标题
    url: str                        # URL
    snippet: str                    # 摘要
    source: str                     # 来源域名
    relevance_score: float          # 相关性分数 (0-100)

    # 可选字段
    publish_date: Optional[str]     # 发布日期
    full_content: Optional[str]     # 完整内容 (Jina Reader)
    code_snippets: List[Dict]       # 代码块
    images: List[Dict]              # 图片

    # 元数据
    engine: str                     # 搜索引擎
    original_rank: int              # 原始排名
    language: Optional[str]         # 语言
    authority_score: float          # 权威性分数
    is_secure: bool                 # 是否HTTPS
    response_time: float            # 响应时间(ms)
```

### WebSearchInput - 搜索输入

```python
@dataclass
class WebSearchInput:
    # 核心参数
    query: str                      # 搜索查询
    search_engines: Optional[List[str]]  # 指定引擎
    max_results: int = 10           # 最大结果数

    # 过滤器
    language: Optional[str]         # 语言过滤
    region: Optional[str]           # 地区过滤
    time_range: str = "all"         # 时间范围
    site_filter: Optional[List[str]]     # 网站白名单
    exclude_sites: Optional[List[str]]   # 网站黑名单

    # 结果控制
    fetch_full_content: bool = False     # 是否提取完整内容
    deduplication: bool = True           # 是否去重

    # 高级选项
    search_type: str = "general"    # 搜索类型
    mode: str = "auto"              # 搜索模式
```

### WebSearchOutput - 搜索输出

```python
@dataclass
class WebSearchOutput:
    # 元数据
    query: str                      # 实际查询（可能经过优化）
    total_results: int              # 结果总数
    search_time: float              # 搜索耗时(ms)
    engines_used: List[str]         # 使用的引擎

    # 搜索结果
    results: List[SearchResult]     # 结果列表

    # 聚合分析
    summary: Dict[str, Any]         # 摘要分析
        # - top_domains: 高频域名
        # - common_themes: 共同主题
        # - recommended_links: AI推荐链接

    # 质量指标
    quality: Dict[str, Any]         # 质量指标
        # - relevance_score: 相关性
        # - average_source_authority: 平均权威性
        # - freshness_score: 新鲜度
        # - coverage_score: 覆盖度

    # 错误与警告
    warnings: List[Dict]            # 警告信息
    partial_failures: List[Dict]    # 部分失败的引擎

    # 查询优化记录
    query_optimization: Dict        # 查询优化详情
```

---

## 🧪 测试

### 运行综合测试

```bash
python test_search.py
```

测试内容：
1. ✅ Fast模式测试
2. ✅ Auto模式测试
3. ✅ Deep模式测试
4. ✅ 代码搜索测试
5. ✅ 去重功能测试
6. ✅ 内容增强测试

### 运行使用示例

```bash
python example_usage.py
```

包含10个示例：
1. 快速搜索
2. Fast模式
3. Deep模式
4. 代码搜索
5. 自定义引擎
6. 完整内容提取
7. 高级过滤
8. 质量指标
9. 错误处理
10. 导出结果

---

## ⚡ 性能指标

### 搜索速度

| 模式 | 引擎数量 | 平均耗时 | 结果数量 |
|------|----------|----------|----------|
| Fast | 2 | 5-7秒 | 10-15个 |
| Auto | 2 | 8-12秒 | 15-20个 |
| Deep | 3 | 15-20秒 | 20-30个 |
| Code | 2 | 10-15秒 | 10-20个 |

### API响应时间 (单次调用)

| API | 平均耗时 | 结果质量 | 成本 |
|-----|----------|----------|------|
| Exa.ai | 7355ms | ⭐⭐⭐⭐⭐ | 付费 |
| Brave | 6333ms | ⭐⭐⭐⭐ | 付费 |
| Perplexity | 8000ms | ⭐⭐⭐⭐⭐ | 付费 |
| Jina Reader | 4723ms | ⭐⭐⭐⭐ | 免费 |
| Jina Embedding | 14975ms | ⭐⭐⭐⭐⭐ | 付费 |
| You.com | 5000ms | ⭐⭐⭐⭐ | 付费 |

---

## 🔒 错误处理

### 部分失败容错

```python
result = await search("query")

# 检查部分失败
if result.partial_failures:
    print(f"警告: {len(result.partial_failures)}个引擎失败")
    for failure in result.partial_failures:
        print(f"{failure['engine']}: {failure['error']}")

# 仍然返回可用结果
print(f"获得 {result.total_results} 个有效结果")
```

### 常见错误码

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| HTTP 401 | API密钥无效 | 检查config.py中的auth_key |
| HTTP 429 | 请求过于频繁 | 增加请求间隔或升级套餐 |
| HTTP 500 | 服务器错误 | 稍后重试或切换引擎 |
| Timeout | 请求超时 | 增加timeout设置 |

---

## 📈 最佳实践

### 1. 根据场景选择模式

```python
# 快速查询、实时搜索 → Fast
result = await search("weather today", mode="fast")

# 日常搜索、综合查询 → Auto (默认)
result = await search("Python tutorial")

# 研究、深度分析 → Deep
result = await search("quantum computing theory", mode="deep")

# 编程问题 → Code
params = WebSearchInput(query="React hooks", search_type="code")
```

### 2. 利用缓存减少调用

```python
# WebSearchFlow内部有简单缓存机制
flow = WebSearchFlow()

# 相同查询会命中缓存（默认1小时TTL）
result1 = await flow.execute(params)
result2 = await flow.execute(params)  # 命中缓存
```

### 3. 批量搜索使用异步

```python
queries = ["query1", "query2", "query3"]

# 并行执行多个搜索
tasks = [search(q) for q in queries]
results = await asyncio.gather(*tasks)
```

### 4. 控制API开销

```python
# 对于不重要的查询，使用Fast模式减少API调用
result = await search("simple query", mode="fast")

# 只在需要时启用内容提取（Jina Reader消耗额外调用）
result = await search("query", fetch_full_content=False)

# 限制结果数量
result = await search("query", max_results=5)
```

---

## 🚀 升级日志

### v3.0.0 (当前版本)

**新增功能**:
- ✅ 6个搜索API集成 (Exa, Brave, Perplexity, Jina Reader, Jina Embedding, You.com)
- ✅ 三种搜索模式 (Fast/Auto/Deep)
- ✅ 智能路由系统
- ✅ 语义去重 (Jina Embedding v3)
- ✅ 内容增强 (Jina Reader)
- ✅ 相关性排序算法
- ✅ 质量指标评估
- ✅ 查询优化
- ✅ 部分失败容错
- ✅ 完整的类型注解

**已删除**:
- ❌ Gemini API (API密钥失效，已移除)

**已修复**:
- 🐛 Perplexity模型名称错误 (改为"sonar")
- 🐛 You.com错误的端点 (改为api.you.com)

---

## 📞 API参考

### 快捷函数

```python
async def search(
    query: str,
    mode: str = "auto",
    max_results: int = 10,
    fetch_full_content: bool = False
) -> WebSearchOutput
```

### 核心类

```python
class WebSearchFlow:
    async def execute(self, input_params: WebSearchInput) -> WebSearchOutput
```

### 配置类

```python
class WebSearchConfig:
    EXA_CONFIG: APIConfig
    BRAVE_CONFIG: APIConfig
    PERPLEXITY_CONFIG: APIConfig
    JINA_READER_CONFIG: APIConfig
    JINA_EMBEDDING_CONFIG: APIConfig
    YOU_CONFIG: APIConfig

    SEARCH_MODES: Dict[str, Dict]
    DEDUP_CONFIG: Dict[str, Any]
    QUALITY_CONFIG: Dict[str, Any]
```

---

## 🎯 常见问题

**Q: 为什么Deep模式这么慢？**
A: Deep模式使用3个引擎（Exa Deep + Perplexity + You.com）并提取完整内容，需要15-20秒。如果需要快速响应，使用Fast或Auto模式。

**Q: 如何提高搜索准确性？**
A:
1. 使用更具体的查询词
2. 选择Deep模式
3. 设置search_type（如"code"、"documentation"）
4. 启用内容提取（fetch_full_content=True）

**Q: 语义去重是如何工作的？**
A: 使用Jina Embedding v3生成512维向量，计算余弦相似度，超过0.85阈值的结果被视为重复。

**Q: 可以自定义引擎组合吗？**
A: 可以！使用search_engines参数指定：
```python
params = WebSearchInput(
    query="...",
    search_engines=["exa_deep", "brave", "perplexity"]
)
```

**Q: 如何处理API配额用完？**
A:
1. 检查partial_failures字段查看哪个引擎失败
2. 使用其他引擎继续搜索
3. 升级API套餐或更换API密钥

---

## 📝 许可证

内部项目，仅供学习和研究使用。

---

## 🙏 致谢

感谢以下API提供商：
- Exa.ai - 语义搜索引擎
- Brave Search - 隐私保护搜索
- Perplexity AI - AI答案生成
- Jina AI - Reader & Embedding服务
- You.com - AI增强搜索

---

**WebSearchFlow v3.0** - 构建于2025年 🚀
