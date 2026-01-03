# Gemini Skill - 全能型AI助手 (Google Gemini驱动)

**版本**: 2.0.0
**类型**: 全能型智能助手
**驱动**: Google Gemini 3 Pro
**质量等级**: A+

## 📋 功能概述

Gemini是Google Gemini 3 Pro驱动的全能型AI助手,不受限于特定任务类型。无论任务多复杂,Gemini都会想尽一切办法完成,自动选择最佳策略,遇到障碍时切换方案,持续尝试直到成功。

### 核心能力

1. **智能任务分析** - 自动识别任务类型和难度、分解复杂任务为可执行步骤
2. **多策略执行** - 直接解决/分步解决/多工具组合/迭代优化4种策略
3. **工具全覆盖** - 代码生成、审查、调试、数据分析、架构设计、自动化
4. **自适应能力** - 遇错自动重试、工具不可用时切换备选、从失败中学习优化
5. **永不放弃精神** - 持续尝试不同方法直到任务完成

## 🚀 使用方法

### 自动触发
当提示词中包含"gemini"(不区分大小写)时自动调用。

### Slash Command
```bash
/gemini [任务描述]
```

### 自然语言调用
```
用gemini帮我完成这个任务
让GEMINI解决这个问题
gemini能处理这个吗
```

## 📖 使用示例

### 示例:问题诊断与修复

**输入**:
```
gemini帮我找出为什么API响应时间从100ms增长到2秒
```

**执行过程**:
```markdown
# Gemini诊断报告

## 任务分析
**类型**: 性能问题诊断(复杂任务)
**症状**: API响应时间 100ms → 2000ms (20倍下降)
**影响**: 用户体验严重下降,可能导致超时

## 策略选择
选择**策略D: 迭代优化**
- 需要多次测试和假设验证
- 不确定根本原因,需要逐步排查

---

## 诊断步骤

### Step 1: 收集基础信息 ✓

**检查项**:
- [x] 何时开始变慢? → 3天前开始
- [x] 影响范围? → 仅GET /api/products端点
- [x] 其他端点正常? → 是,其他端点响应时间正常
- [x] 最近有代码变更? → 是,3天前添加了商品评分功能

**初步结论**: 问题与GET /api/products端点和最近的商品评分功能相关

---

### Step 2: 性能分析 (第1次尝试) ✓

**方法**: 添加性能跟踪代码

```typescript
// 在 ProductController.ts 中添加
import { performance } from 'perf_hooks';

async getProducts(req, res) {
  const t0 = performance.now();

  const products = await Product.findAll();
  console.log(`[1] Query products: ${performance.now() - t0}ms`);

  const t1 = performance.now();
  // 新增: 获取每个商品的平均评分
  for (const product of products) {
    product.avgRating = await Rating.aggregate([
      { $match: { productId: product.id } },
      { $group: { _id: null, avg: { $avg: '$score' } } }
    ]);
  }
  console.log(`[2] Calculate ratings: ${performance.now() - t1}ms`);

  res.json(products);
}
```

**运行结果**:
```
[1] Query products: 15ms
[2] Calculate ratings: 1950ms  ← 瓶颈!!!
```

**发现问题**: N+1查询问题!
- 100个商品 → 100次数据库查询
- 每次查询~20ms → 总计2000ms

---

### Step 3: 修复方案设计 (第2次尝试) ✓

**方案A: 使用JOIN查询**
```typescript
// 不适用 - Product在PostgreSQL,Rating在MongoDB,无法跨库JOIN
```

**方案B: 批量查询**
```typescript
async getProducts(req, res) {
  const products = await Product.findAll();

  // ✓ 批量获取所有商品的评分
  const productIds = products.map(p => p.id);
  const ratings = await Rating.aggregate([
    { $match: { productId: { $in: productIds } } },
    {
      $group: {
        _id: '$productId',
        avgRating: { $avg: '$score' },
        count: { $sum: 1 }
      }
    }
  ]);

  // 构建评分Map
  const ratingMap = new Map(
    ratings.map(r => [r._id, { avgRating: r.avgRating, count: r.count }])
  );

  // 关联评分数据
  products.forEach(p => {
    const rating = ratingMap.get(p.id) || { avgRating: 0, count: 0 };
    p.avgRating = rating.avgRating;
    p.reviewCount = rating.count;
  });

  res.json(products);
}
```

**测试结果**:
```
[1] Query products: 15ms
[2] Calculate ratings: 35ms  ← 从1950ms → 35ms (50倍提升!)
Total: 50ms ✓
```

---

### Step 4: 进一步优化 (第3次尝试) ✓

**方案C: 添加Redis缓存**

问题: 商品评分变化不频繁,不需要实时计算

```typescript
import Redis from 'ioredis';
const redis = new Redis();

async getProducts(req, res) {
  const products = await Product.findAll();
  const productIds = products.map(p => p.id);

  // 尝试从缓存批量获取
  const cacheKeys = productIds.map(id => `rating:${id}`);
  const cachedRatings = await redis.mget(cacheKeys);

  // 识别缓存缺失的商品ID
  const missingIds = productIds.filter((id, i) => !cachedRatings[i]);

  let ratingsMap = new Map();

  // 从缓存恢复已有的评分
  productIds.forEach((id, i) => {
    if (cachedRatings[i]) {
      ratingsMap.set(id, JSON.parse(cachedRatings[i]));
    }
  });

  // 查询缺失的评分
  if (missingIds.length > 0) {
    const ratings = await Rating.aggregate([
      { $match: { productId: { $in: missingIds } } },
      { $group: { _id: '$productId', avgRating: { $avg: '$score' }, count: { $sum: 1 } } }
    ]);

    // 写入缓存 (TTL: 1小时)
    const pipeline = redis.pipeline();
    ratings.forEach(r => {
      const data = { avgRating: r.avgRating, count: r.count };
      ratingsMap.set(r._id, data);
      pipeline.setex(`rating:${r._id}`, 3600, JSON.stringify(data));
    });
    await pipeline.exec();
  }

  // 关联数据
  products.forEach(p => {
    const rating = ratingsMap.get(p.id) || { avgRating: 0, count: 0 };
    p.avgRating = rating.avgRating;
    p.reviewCount = rating.count;
  });

  res.json(products);
}
```

**测试结果**:
```
首次请求 (缓存未命中): 50ms
后续请求 (缓存命中): 18ms ✓
```

---

### Step 5: 缓存失效策略 ✓

**问题**: 新增评分时,缓存不会更新

**解决**: 在Rating创建/更新时清除缓存

```typescript
// RatingService.ts
async createRating(productId: string, userId: string, score: number) {
  const rating = await Rating.create({ productId, userId, score });

  // 清除该商品的评分缓存
  await redis.del(`rating:${productId}`);

  return rating;
}
```

---

## 诊断总结

### 根本原因
**N+1查询问题**: 为每个商品单独查询评分,导致100个商品 = 100次数据库查询

### 优化方案
1. **批量查询**: 1次查询获取所有评分 (1950ms → 35ms, 50倍提升)
2. **Redis缓存**: 缓存评分数据,减少数据库查询 (35ms → 18ms, 额外2倍提升)
3. **缓存失效**: 评分变更时清除缓存,保证数据一致性

### 最终效果
| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 响应时间 | 2000ms | 18ms | 111倍 ✓ |
| 数据库查询 | 101次 | 1次 | 99% 减少 ✓ |
| 缓存命中率 | N/A | 95%+ | 新增 ✓ |

### 代码变更
- 修改文件: 2个 (ProductController.ts, RatingService.ts)
- 新增依赖: Redis
- 代码行数: +45行

**状态**: ✅ 问题完全解决
```

### 示例:数据处理与报表生成

**输入**:
```
gemini处理这个sales.csv文件,生成月度销售报表
包含:
- 按月统计销售额
- 按产品类别排名
- 同比增长率
- 可视化图表
```

**执行过程**:
```markdown
# Gemini数据处理报告

## 任务分析
**类型**: 数据分析与报表生成(中等任务)
**数据源**: sales.csv (预估 10K-100K行)
**输出**: 月度销售报表 + 图表

## 策略选择
选择**策略B: 分步解决**
- Step 1: 数据加载和验证
- Step 2: 数据清洗和转换
- Step 3: 统计分析
- Step 4: 图表生成
- Step 5: 报表输出

---

## 执行步骤

### Step 1: 数据探索 ✓

```python
import pandas as pd
import numpy as np
from datetime import datetime

# 加载数据
df = pd.read_csv('sales.csv')

# 基本信息
print(f"数据行数: {len(df)}")
print(f"字段: {df.columns.tolist()}")
print(f"\n数据预览:")
print(df.head())
```

**输出**:
```
数据行数: 45,328
字段: ['date', 'product_id', 'category', 'amount', 'quantity', 'region']

数据预览:
        date  product_id  category  amount  quantity region
0 2024-01-05         123  电子产品   1299.00         1   华东
1 2024-01-06         456  服装鞋帽    299.99         2   华北
2 2024-01-07         789  食品饮料     89.90         5   华南
```

### Step 2: 数据清洗 ✓

```python
# 转换日期格式
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['year_month'] = df['date'].dt.to_period('M')

# 处理缺失值
print(f"缺失值: {df.isnull().sum()}")
# amount: 0, quantity: 2 → 填充为0

df['quantity'].fillna(0, inplace=True)

# 异常值检测
print(f"异常值:")
print(f"  负金额: {(df['amount'] < 0).sum()}")  # 3条 → 删除
print(f"  异常高金额: {(df['amount'] > 50000).sum()}")  # 1条 → 保留(可能是企业订单)

df = df[df['amount'] >= 0]
```

### Step 3: 月度销售统计 ✓

```python
# 按月统计
monthly_sales = df.groupby('year_month').agg({
    'amount': 'sum',
    'quantity': 'sum',
    'product_id': 'count'  # 订单数
}).rename(columns={'product_id': 'orders'})

# 计算同比增长率
monthly_sales['yoy_growth'] = monthly_sales['amount'].pct_change(12) * 100

print(monthly_sales.tail(6))
```

**输出**:
```
year_month     amount  quantity  orders  yoy_growth
2024-07     2,458,900    12,345     876       15.2%
2024-08     2,789,500    13,890   1,023       18.7%
2024-09     2,345,600    11,234     789       12.5%
2024-10     3,123,400    15,678   1,234       25.3%
2024-11     3,567,800    17,890   1,456       22.8%
2024-12     4,234,500    21,234   1,789       28.6%
```

### Step 4: 产品类别排名 ✓

```python
# 按类别统计
category_sales = df.groupby('category').agg({
    'amount': 'sum',
    'quantity': 'sum'
}).sort_values('amount', ascending=False)

category_sales['share'] = (category_sales['amount'] / category_sales['amount'].sum() * 100).round(2)

print(category_sales)
```

**输出**:
```
category     amount  quantity  share
电子产品   15,234,500    45,678  42.5%
服装鞋帽    8,456,200    67,890  23.6%
食品饮料    5,678,900    89,012  15.8%
家居用品    4,234,100    34,567  11.8%
图书音像    2,234,800    23,456   6.2%
```

### Step 5: 可视化图表 ✓

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 月度销售额趋势
axes[0, 0].plot(monthly_sales.index.astype(str), monthly_sales['amount'], marker='o')
axes[0, 0].set_title('月度销售额趋势', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('月份')
axes[0, 0].set_ylabel('销售额 (元)')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. 同比增长率
axes[0, 1].bar(monthly_sales.index.astype(str)[-12:], monthly_sales['yoy_growth'][-12:], color='green')
axes[0, 1].set_title('同比增长率 (近12月)', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('月份')
axes[0, 1].set_ylabel('增长率 (%)')
axes[0, 1].axhline(0, color='black', linewidth=0.8)
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. 产品类别占比
axes[1, 0].pie(category_sales['amount'], labels=category_sales.index, autopct='%1.1f%%', startangle=90)
axes[1, 0].set_title('产品类别销售额占比', fontsize=14, fontweight='bold')

# 4. 地区分布
region_sales = df.groupby('region')['amount'].sum().sort_values(ascending=False)
axes[1, 1].barh(region_sales.index, region_sales.values, color='skyblue')
axes[1, 1].set_title('地区销售额分布', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('销售额 (元)')

plt.tight_layout()
plt.savefig('sales_report.png', dpi=300, bbox_inches='tight')
print("图表已保存: sales_report.png")
```

### Step 6: 生成Excel报表 ✓

```python
with pd.ExcelWriter('sales_report_2024.xlsx', engine='openpyxl') as writer:
    # Sheet 1: 月度统计
    monthly_sales.to_excel(writer, sheet_name='月度统计')

    # Sheet 2: 类别排名
    category_sales.to_excel(writer, sheet_name='类别排名')

    # Sheet 3: 明细数据
    df.to_excel(writer, sheet_name='销售明细', index=False)

print("Excel报表已生成: sales_report_2024.xlsx")
```

---

## 完成总结

✅ **任务完成度**: 100%
✅ **数据行数**: 45,328行
✅ **输出文件**: 2个 (PNG图表 + Excel报表)
✅ **关键洞察**:
- 2024年总销售额: 3,584万元
- 同比增长: 平均20.3%
- 最佳月份: 12月 (423万元)
- 主要品类: 电子产品 (42.5%份额)

**耗时**: < 3分钟 (Gemini全自动)
**质量评分**: A+
```

## 🎯 核心特性

### 1. 多领域能力
- ✅ 代码开发 (全栈)
- ✅ 问题诊断 (性能/Bug/安全)
- ✅ 数据处理 (分析/可视化/报表)
- ✅ 架构设计 (微服务/分布式)
- ✅ 自动化 (CI/CD/脚本/工具)
- ✅ 文档编写 (API/架构/技术)

### 2. 智能容错
```
遇到错误 → 分析原因 → 切换方法 → 重新尝试
```

### 3. 从失败中学习
```
失败记录 → 模式识别 → 策略优化 → 提升成功率
```

## 🛠️ 最佳实践

1. **明确目标**: 清晰描述任务和期望结果
2. **提供上下文**: 说明项目技术栈和约束条件
3. **信任Gemini**: 让它自主选择最佳策略
4. **反馈迭代**: 如果结果不理想,提供反馈让Gemini优化
5. **验证结果**: Gemini会生成解决方案,但建议人工验证关键逻辑

## 🔗 与其他 Skills 配合

- `performance-optimizer`: Gemini诊断性能问题,optimizer提供深度优化建议
- `debugger`: Gemini快速定位问题,debugger提供详细调试步骤
- `project-planner`: Gemini实施任务,planner管理整体项目进度

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
