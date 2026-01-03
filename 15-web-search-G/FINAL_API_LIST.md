# 15-WebSearchFlow - 最终API清单
# Final API List for Implementation

**更新时间**: 2025-12-12
**状态**: ✅ 已确认，准备实施

---

## ✅ 将要实现的6个API

### 1. Exa.ai - 语义搜索引擎
```python
endpoint = "https://api.exa.ai/search"
auth_header = "x-api-key"
api_key = "${EXA_API_KEY}"
```

**功能**:
- Fast search (<350ms)
- Auto mode (默认)
- Deep search (3.5s)
- Neural search

**用途**: 主要搜索引擎，语义搜索

---

### 2. Brave Search - 隐私搜索引擎
```python
endpoint = "https://api.search.brave.com/res/v1/web/search"
auth_header = "X-Subscription-Token"
api_key = "${BRAVE_API_KEY}"
```

**功能**:
- Web search
- News search
- Image search
- Privacy-focused

**用途**: 通用网页搜索，隐私友好

---

### 3. Perplexity - AI搜索引擎
```python
endpoint = "https://api.perplexity.ai/chat/completions"
auth_header = "Authorization: Bearer"
api_key = "${PERPLEXITY_API_KEY}"
model = "sonar"  # 重要: 使用简短模型名
```

**功能**:
- AI-powered search
- Direct answers
- Citation support

**用途**: AI增强搜索，直接答案生成

---

### 4. Jina Reader - 网页内容提取
```python
endpoint = "https://r.jina.ai/{target_url}"
auth = None  # 免费，无需API key
```

**功能**:
- Clean markdown output
- Free service
- URL prefix

**用途**: 提取网页完整内容为Markdown

---

### 5. Jina Embedding - 语义嵌入
```python
endpoint = "https://api.jina.ai/v1/embeddings"
auth_header = "Authorization: Bearer"
api_key = "${JINA_API_KEY}"
model = "jina-embeddings-v3"
```

**功能**:
- Semantic similarity
- MTEB #1 ranking
- 256-8192 dimensions
- Late chunking

**用途**: 语义去重，相似度计算

---

### 6. You.com - 搜索引擎
```python
endpoint = "https://api.you.com/v1/search"  # 注意: 不是ydc-index.io
auth_header = "X-API-Key"
api_key = "${YOU_API_KEY}"
```

**功能**:
- Web Search
- News API
- RAG API
- Deep Search
- Image Search

**用途**: 结构化搜索结果，多种搜索模式

---

## ❌ 已删除的API

### Gemini - Google AI (已删除)
**删除原因**: 两个API密钥均验证失败(404 Not Found)

**原API密钥** (已失效):
- `${YOUTUBE_API_KEY}`
- `${YOUTUBE_API_KEY}`

**替代方案**: 使用Perplexity作为AI搜索的替代

---

## 实现架构

### 三层搜索设计

```
┌─────────────────────────────────────────┐
│         快速搜索层 (Primary)             │
│   Brave + Exa.ai Fast + You.com         │
│   响应时间: 5-7秒                        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         深度搜索层 (Deep)                │
│   Exa.ai Deep + Perplexity + You.com    │
│   响应时间: 8-12秒                       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         内容增强层 (Enhancement)         │
│   Jina Reader + Jina Embedding          │
│   响应时间: 15-20秒                      │
└─────────────────────────────────────────┘
```

---

## 成本估算 (月度)

| API | 免费额度 | 超出价格 | 月预估 |
|-----|---------|---------|--------|
| Exa.ai | 1000次 | $0.005/次 | $10-30 |
| Brave Search | 2000次 | $0.0035/次 | $5-15 |
| Perplexity | N/A | $0.005/次 | $10-30 |
| Jina Reader | ∞ | FREE | $0 |
| Jina Embedding | 1M tokens | $0.02/1M | $5-10 |
| You.com | 试用配额 | 待确认 | $0-10 |

**总计**: $30-95/月

---

## 下一步

1. ✅ API验证完成
2. ✅ Gemini已删除
3. ⏭️ 实现main.py (WebSearchFlow核心逻辑)
4. ⏭️ 实现6个API客户端
5. ⏭️ 实现智能路由和去重
6. ⏭️ 编写测试和文档

---

**确认**: 以上6个API均已验证可用，准备开始实现。
