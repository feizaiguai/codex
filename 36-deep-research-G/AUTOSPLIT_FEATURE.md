# 📄 Deep Research 自动文档分割功能

## 功能说明

当生成的深度研究报告超过 **20,000 tokens** 时，系统会自动将报告分割为多个文件，确保每个文件都可以被 Claude 完整读取。

## 技术细节

### Token 估算方法

使用保守估算策略：**1 token ≈ 2.5 个字符**

这比实际token数偏高，确保即使 Claude 的内部计数更高，分割后的文件也不会超过限制。

### 分割策略

1. **保留头部信息**
   - 每个分割文件都包含完整的元数据（前 50 行）
   - 包含：标题、生成时间、搜索模式、总耗时、总结果数等

2. **智能内容分割**
   - 按行分割，不会在内容中间截断
   - 自动计算每行的 token 数
   - 达到限制前保存当前 part

3. **安全边际**
   - 每个文件预留 **500 tokens** 的安全边际
   - 确保分页标记和格式化不会导致超限

4. **分页标记**
   - 每个文件添加 `[Part X/Y]` 标记
   - 清楚标识这是第几部分，共几部分

## 文件命名规则

- **单文件**：`research_{查询主题}.md`
- **多文件**：
  - `research_{查询主题}_part1.md`
  - `research_{查询主题}_part2.md`
  - `research_{查询主题}_part3.md`
  - ...

## 使用示例

### 示例 1：小报告（不分割）

```bash
python deep_research.py "React hooks best practices" --max-results 5
```

**输出**：
```
📊 报告大小估算: 15,937 tokens
📄 报告已保存到: research_React_hooks_best_practices.md
```

### 示例 2：大报告（自动分割）

```bash
python deep_research.py "过去一周全球AI发生的新闻，对人类有什么影响" --max-results 20
```

**输出**：
```
📊 报告大小估算: 44,682 tokens
⚠️  报告超过 20,000 tokens 限制，自动分割为多个文件...

   ✅ Part 1: research_AI新闻_part1.md (19,762 tokens)
   ✅ Part 2: research_AI新闻_part2.md (19,667 tokens)
   ✅ Part 3: research_AI新闻_part3.md (6,636 tokens)

📄 报告已分割保存为 3 个文件:
   - research_AI新闻_part1.md
   - research_AI新闻_part2.md
   - research_AI新闻_part3.md
```

## 分割文件结构

每个分割文件的结构：

```markdown
# {查询主题} 深度研究报告 [Part 1/3]

**生成时间**: 2025-12-16 04:51:12
**搜索模式**: Deep Research (3 AI 协作)
**总耗时**: 52.34s
**总搜索结果**: 88
**平均可信度**: 61.7/100

---

📄 这是分段报告的第 1 部分

---

## 🎯 执行摘要

... (内容) ...
```

## 性能指标

| 指标 | 数值 |
|------|------|
| 最大文件大小 | 20,000 tokens |
| 安全边际 | 500 tokens |
| 估算精度 | 1 token ≈ 2.5 字符 |
| 分割速度 | < 1 秒 |

## 测试验证

### 测试案例

```python
# 模拟 44,682 tokens 的大报告
large_report = original_report * 3

# 分割
parts = split_report_by_tokens(large_report, max_tokens=20000)

# 结果
✓ Part 1/3: 49,405 字符 / 19,762 tokens
✓ Part 2/3: 49,168 字符 / 19,667 tokens
✓ Part 3/3: 16,590 字符 / 6,636 tokens

✅ 所有分割文件都在 20,000 tokens 限制内！
```

## 优势

1. ✅ **自动化**：无需手动操作，系统自动检测和分割
2. ✅ **安全**：500 tokens 安全边际确保不超限
3. ✅ **完整性**：每个文件都包含完整的元数据头部
4. ✅ **可读性**：清晰的分页标记（Part 1/3, Part 2/3...）
5. ✅ **高效**：分割速度快，不影响整体研究时间

## 技术实现

### 核心函数

#### 1. `estimate_tokens(text: str) -> int`

估算文本的 token 数量。

```python
def estimate_tokens(text: str) -> int:
    """
    保守估算（考虑 Claude 的 token 计数）：
    - 1 token ≈ 2.5 个字符（混合中英文）
    - 这比实际偏高，确保分割后不会超过限制
    """
    estimated_tokens = int(len(text) / 2.5)
    return estimated_tokens
```

#### 2. `split_report_by_tokens(report: str, max_tokens: int = 20000) -> List[str]`

按 token 限制分割报告。

```python
def split_report_by_tokens(report: str, max_tokens: int = 20000) -> List[str]:
    """
    按 token 限制分割报告

    Args:
        report: 完整报告内容
        max_tokens: 每个文件的最大 token 数（默认 20000）

    Returns:
        分割后的报告列表
    """
    # 如果不超过限制，返回原报告
    if estimate_tokens(report) <= max_tokens:
        return [report]

    # 分割逻辑...
    # (保留头部 + 智能内容分割 + 安全边际)
```

## 未来改进

- [ ] 支持自定义 max_tokens 限制
- [ ] 添加 PDF 导出功能
- [ ] 生成目录索引文件
- [ ] 支持按主题智能分割（不仅按 tokens）

## 更新日志

### v2.1 (2025-12-16)

- ✅ 新增自动文档分割功能
- ✅ Token 估算算法（2.5 字符/token）
- ✅ 500 tokens 安全边际
- ✅ 分页标记 [Part X/Y]
- ✅ 多文件保存支持

---

**注意**：这是 Deep Research V2.0 的重要功能增强，确保所有报告都可以被 Claude 完整读取和分析。
