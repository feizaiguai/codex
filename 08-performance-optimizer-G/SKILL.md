---
name: 08-performance-optimizer-G
description: Performance optimization expert that identifies bottlenecks and provides optimization solutions. Supports algorithm complexity optimization (O(n²)→O(n log n)), database optimization (N+1 queries/indexes), caching strategy design (Redis/Memcached), frontend resource optimization (Bundle/CDN/lazy loading), concurrency optimization (connection pools/thread pools). Use for performance diagnostics, system optimization, high-concurrency scenarios.
---

# performance-optimizer - 性能优化专家

**版本**: 2.0.0
**优先级**: P0 (最高优先级)
**类别**: 质量与安全

---

## 描述

performance-optimizer是一个专业的性能优化专家，通过深度分析识别代码中的性能瓶颈（CPU、内存、I/O、数据库），提供具体的优化方案并预估改进效果。支持多维度性能分析：时间复杂度优化（O(n²)→O(n log n)）、数据库查询优化（N+1问题、索引建议）、前端资源优化（懒加载、代码分割）、缓存策略设计（多层缓存、失效策略）、并发优化（异步处理、连接池）。通过profiling数据分析、代码静态分析和最佳实践匹配，为每个瓶颈提供before/after对比代码、性能指标预估和验证方法，帮助开发团队显著提升应用响应速度、吞吐量和资源利用率。

---

## 核心能力

1. **性能瓶颈识别**: CPU热点、内存泄漏、I/O阻塞、数据库慢查询深度分析
2. **算法优化**: 时间/空间复杂度分析，提供更高效算法实现
3. **数据库优化**: N+1查询解决、索引建议、查询重写、连接优化
4. **前端性能优化**: 资源加载优化、渲染性能提升、代码分割、懒加载
5. **缓存策略**: 多层缓存设计（Redis、CDN、浏览器缓存）、失效策略
6. **并发优化**: 异步I/O、连接池、批处理、并行计算优化

---

## Instructions

### 工作流程

#### 1. 性能分析与瓶颈识别

**分析维度**:

**A. CPU性能分析**
```python
# 识别热点函数（CPU时间占用高）
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20热点

    return result

# 分析结果示例
"""
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    5.234    5.234 api.py:45(get_users)
     1000    2.345    0.002    4.567    0.005 serializer.py:12(serialize)
     1000    1.234    0.001    1.234    0.001 {method 'fetchall'}
"""
# 识别：serialize函数占用46%时间 → 优化目标
```

**B. 内存分析**
```python
import tracemalloc

def analyze_memory():
    tracemalloc.start()

    # 执行代码
    data = load_large_dataset()

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    for stat in top_stats[:10]:
        print(f"{stat.size / 1024 / 1024:.1f} MB - {stat}")

# 检测内存泄漏
def detect_memory_leak():
    import gc
    gc.collect()

    snapshot1 = tracemalloc.take_snapshot()
    # ... 执行操作 ...
    snapshot2 = tracemalloc.take_snapshot()

    diff = snapshot2.compare_to(snapshot1, 'lineno')
    for stat in diff[:10]:
        if stat.size_diff > 1024 * 1024:  # 增长超过1MB
            print(f"⚠️ Memory leak: {stat}")
```

**C. 数据库性能分析**
```python
# Django ORM查询分析
from django.db import connection

def analyze_queries():
    from django.test.utils import override_settings

    with override_settings(DEBUG=True):
        # 执行操作
        users = User.objects.all()
        for user in users:
            posts = user.posts.all()  # N+1问题

        # 分析查询
        queries = connection.queries
        print(f"Total queries: {len(queries)}")

        for q in queries:
            if float(q['time']) > 0.1:  # 慢查询
                print(f"⚠️ Slow query ({q['time']}s): {q['sql']}")
```

**D. I/O性能分析**
```python
import time

def measure_io_time(func):
    start = time.perf_counter()
    result = func()
    end = time.perf_counter()

    io_time = end - start
    if io_time > 1.0:
        print(f"⚠️ Slow I/O operation: {io_time:.2f}s")

    return result
```

#### 2. 算法复杂度优化

**常见优化模式**:

**A. O(n²) → O(n) 优化**
```python
# ❌ O(n²) - 嵌套循环
def find_duplicates_slow(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates

# 性能: 10,000元素 → 45秒

# ✅ O(n) - 哈希表
def find_duplicates_fast(arr):
    seen = set()
    duplicates = set()

    for item in arr:
        if item in seen:
            duplicates.add(item)
        seen.add(item)

    return list(duplicates)

# 性能: 10,000元素 → 0.002秒
# 提升: 22,500倍
```

**B. O(n log n) 排序优化**
```python
# ❌ O(n²) - 冒泡排序
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# ✅ O(n log n) - 内置排序（Tim Sort）
def optimized_sort(arr):
    return sorted(arr)

# 性能对比（100,000元素）:
# 冒泡排序: 124秒
# Tim Sort: 0.08秒
# 提升: 1,550倍
```

**C. 空间换时间优化**
```python
# ❌ 每次计算斐波那契数（指数时间）
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n-1) + fib_slow(n-2)

# fib_slow(40) → 102秒

# ✅ 记忆化（O(n)时间，O(n)空间）
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_fast(n):
    if n <= 1:
        return n
    return fib_fast(n-1) + fib_fast(n-2)

# fib_fast(40) → 0.00001秒
# 提升: 10,000,000倍
```

#### 3. 数据库查询优化

**A. 解决N+1查询问题**
```python
# ❌ N+1问题
def get_users_with_posts():
    users = User.objects.all()  # 1次查询

    result = []
    for user in users:
        posts = user.posts.all()  # N次查询（每个用户1次）
        result.append({
            'user': user,
            'posts': posts
        })

    return result

# 100用户 → 101次查询 → 3.5秒

# ✅ 使用select_related/prefetch_related
def get_users_with_posts_optimized():
    users = User.objects.prefetch_related('posts').all()  # 2次查询

    result = []
    for user in users:
        result.append({
            'user': user,
            'posts': user.posts.all()  # 已预加载，无额外查询
        })

    return result

# 100用户 → 2次查询 → 0.15秒
# 提升: 23倍
```

**B. 索引优化**
```python
# 识别缺少索引的查询
"""
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';

# 结果显示全表扫描
Seq Scan on users  (cost=0.00..1693.00 rows=1 width=100) (actual time=45.234..45.234 rows=1 loops=1)
  Filter: (email = 'test@example.com')
Planning time: 0.123 ms
Execution time: 45.357 ms  ← 慢！
"""

# ✅ 添加索引
# migrations/0005_add_email_index.py
from django.db import migrations, models

class Migration(migrations.Migration):
    operations = [
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='user_email_idx')
        ),
    ]

"""
# 添加索引后
Index Scan using user_email_idx on users  (cost=0.42..8.44 rows=1 width=100) (actual time=0.023..0.024 rows=1 loops=1)
  Index Cond: (email = 'test@example.com')
Execution time: 0.047 ms  ← 快965倍！
"""
```

**C. 查询重写优化**
```python
# ❌ 低效：多次单条查询
def get_user_stats(user_ids):
    stats = []
    for user_id in user_ids:
        post_count = Post.objects.filter(user_id=user_id).count()
        comment_count = Comment.objects.filter(user_id=user_id).count()
        stats.append({
            'user_id': user_id,
            'post_count': post_count,
            'comment_count': comment_count
        })
    return stats

# 1000用户 → 2000次查询 → 15秒

# ✅ 高效：聚合查询
from django.db.models import Count

def get_user_stats_optimized(user_ids):
    stats = User.objects.filter(id__in=user_ids).annotate(
        post_count=Count('posts'),
        comment_count=Count('comments')
    ).values('id', 'post_count', 'comment_count')

    return list(stats)

# 1000用户 → 1次查询 → 0.3秒
# 提升: 50倍
```

**D. 分页优化**
```python
# ❌ OFFSET性能问题（大偏移量慢）
def get_posts_page(page, per_page=20):
    offset = (page - 1) * per_page
    posts = Post.objects.order_by('-created_at')[offset:offset+per_page]
    return posts

# page=1000 → offset=19,980 → 数据库需扫描20,000行 → 2.5秒

# ✅ 游标分页（Cursor Pagination）
def get_posts_cursor(last_id=None, limit=20):
    query = Post.objects.order_by('-id')

    if last_id:
        query = query.filter(id__lt=last_id)

    posts = query[:limit]
    return posts

# 任意页码 → 只扫描20行 → 0.02秒
# 提升: 125倍
```

#### 4. 前端性能优化

**A. 代码分割与懒加载**
```javascript
// ❌ 一次性加载所有组件（打包文件3MB）
import Dashboard from './Dashboard';
import AdminPanel from './AdminPanel';
import Reports from './Reports';
import Analytics from './Analytics';

function App() {
  return (
    <Routes>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/admin" element={<AdminPanel />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/analytics" element={<Analytics />} />
    </Routes>
  );
}

// 首次加载: 3MB → 4.2秒 (3G网络)

// ✅ 动态导入 + 代码分割
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const AdminPanel = lazy(() => import('./AdminPanel'));
const Reports = lazy(() => import('./Reports'));
const Analytics = lazy(() => import('./Analytics'));

function App() {
  return (
    <Routes>
      <Route
        path="/dashboard"
        element={
          <Suspense fallback={<Loading />}>
            <Dashboard />
          </Suspense>
        }
      />
      {/* 其他路由... */}
    </Routes>
  );
}

// 首次加载: 400KB → 0.5秒 (3G网络)
// 提升: 8.4倍
// 后续页面: 按需加载（200-500KB）
```

**B. 图片优化**
```javascript
// ❌ 加载原始大图
<img src="/images/hero-original.jpg" alt="Hero" />
// 文件大小: 2.5MB, 加载时间: 3.5秒

// ✅ 响应式图片 + 现代格式
<picture>
  <source
    srcSet="/images/hero-small.webp 480w,
            /images/hero-medium.webp 768w,
            /images/hero-large.webp 1200w"
    type="image/webp"
  />
  <source
    srcSet="/images/hero-small.jpg 480w,
            /images/hero-medium.jpg 768w,
            /images/hero-large.jpg 1200w"
    type="image/jpeg"
  />
  <img
    src="/images/hero-medium.jpg"
    alt="Hero"
    loading="lazy"  // 懒加载
  />
</picture>

// 文件大小: 120KB (WebP), 加载时间: 0.4秒
// 提升: 8.75倍
```

**C. 虚拟滚动（长列表优化）**
```javascript
// ❌ 渲染10,000个列表项（DOM节点过多）
function UserList({ users }) {
  return (
    <div className="list">
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

// 10,000项 → 渲染时间: 8.5秒, 内存: 450MB

// ✅ 虚拟滚动（仅渲染可见区域）
import { FixedSizeList } from 'react-window';

function UserListVirtualized({ users }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={users.length}
      itemSize={80}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          <UserCard user={users[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}

// 10,000项 → 渲染时间: 0.2秒, 内存: 35MB
// 渲染提升: 42倍
// 内存节省: 92%
```

#### 5. 缓存策略设计

**多层缓存架构**:
```
┌─────────────────────────────────────────┐
│  Layer 1: 浏览器缓存 (Cache-Control)    │ ← 最快
├─────────────────────────────────────────┤
│  Layer 2: CDN缓存 (CloudFlare/AWS)      │
├─────────────────────────────────────────┤
│  Layer 3: 应用内存缓存 (LRU Cache)      │
├─────────────────────────────────────────┤
│  Layer 4: Redis缓存 (分布式)            │
├─────────────────────────────────────────┤
│  Layer 5: 数据库查询缓存                │
├─────────────────────────────────────────┤
│  Layer 6: 数据库 (PostgreSQL)           │ ← 最慢
└─────────────────────────────────────────┘
```

**实现示例**:
```python
from functools import lru_cache
import redis
from django.core.cache import cache

# Layer 3: 应用内存缓存（单进程）
@lru_cache(maxsize=1000)
def get_user_profile_memory(user_id):
    return User.objects.get(id=user_id)

# Layer 4: Redis缓存（分布式）
def get_user_profile_redis(user_id):
    cache_key = f'user_profile:{user_id}'

    # 尝试从缓存获取
    cached = cache.get(cache_key)
    if cached:
        return cached

    # 缓存未命中，从数据库加载
    user = User.objects.get(id=user_id)

    # 存入缓存（TTL: 5分钟）
    cache.set(cache_key, user, timeout=300)

    return user

# 缓存失效策略
def update_user_profile(user_id, data):
    # 更新数据库
    user = User.objects.get(id=user_id)
    for key, value in data.items():
        setattr(user, key, value)
    user.save()

    # 主动失效缓存
    cache_key = f'user_profile:{user_id}'
    cache.delete(cache_key)

    return user
```

**HTTP缓存头配置**:
```python
# Django视图
from django.views.decorators.cache import cache_page
from django.utils.cache import patch_cache_control

# 静态资源：长期缓存
@cache_page(60 * 60 * 24 * 365)  # 1年
def serve_static_asset(request):
    response = HttpResponse(content, content_type='image/jpeg')
    patch_cache_control(
        response,
        public=True,
        max_age=31536000,  # 1年
        immutable=True
    )
    return response

# 动态内容：短期缓存
@cache_page(60 * 5)  # 5分钟
def get_trending_posts(request):
    posts = Post.objects.filter(trending=True)[:10]
    return JsonResponse({'posts': list(posts)})

# 用户特定内容：私有缓存
def get_user_feed(request):
    user = request.user
    feed = generate_feed(user)

    response = JsonResponse({'feed': feed})
    patch_cache_control(
        response,
        private=True,
        max_age=300  # 5分钟
    )
    return response
```

#### 6. 并发与异步优化

**A. 异步I/O（FastAPI示例）**
```python
import asyncio
import httpx

# ❌ 同步调用（串行）
def fetch_user_data_sync(user_ids):
    results = []
    for user_id in user_ids:
        response = requests.get(f'https://api.example.com/users/{user_id}')
        results.append(response.json())
    return results

# 100用户 → 100次HTTP请求 → 25秒 (每次250ms)

# ✅ 异步调用（并行）
async def fetch_user_data_async(user_ids):
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f'https://api.example.com/users/{user_id}')
            for user_id in user_ids
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# 100用户 → 100次并行请求 → 0.5秒
# 提升: 50倍
```

**B. 数据库连接池**
```python
# ❌ 每次请求创建新连接
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # 耗时100ms
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# ✅ 使用连接池
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=5,
    maxconn=20,
    host='localhost',
    database='mydb'
)

def get_user_pooled(user_id):
    conn = connection_pool.getconn()  # 复用连接，耗时<1ms
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    connection_pool.putconn(conn)
    return user

# 连接开销: 100ms → 1ms
# 提升: 100倍
```

**C. 批处理优化**
```python
# ❌ 逐条插入（N次数据库往返）
def insert_users_slow(users):
    for user in users:
        db.session.add(User(**user))
        db.session.commit()

# 1000用户 → 1000次提交 → 45秒

# ✅ 批量插入（1次数据库往返）
def insert_users_fast(users):
    user_objects = [User(**user) for user in users]
    db.session.bulk_save_objects(user_objects)
    db.session.commit()

# 1000用户 → 1次提交 → 0.8秒
# 提升: 56倍
```

---

## 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| code_or_profile | string/object | 是 | - | 代码路径或性能分析数据 |
| optimization_target | string | 否 | balanced | 优化目标: speed/memory/throughput/balanced |
| current_metrics | object | 否 | - | 当前性能指标（响应时间、QPS、内存等） |
| target_metrics | object | 否 | - | 目标性能指标 |
| constraints | object | 否 | {} | 约束条件（如不能增加硬件成本） |
| profiling_data | object | 否 | - | Profiling工具输出数据 |

---

## 输出格式

```typescript
interface PerformanceOptimizationOutput {
  current_metrics: PerformanceMetrics;
  bottlenecks: Bottleneck[];
  optimizations: Optimization[];
  estimated_improvement: ImprovementEstimate;
  implementation_priority: PriorityTask[];
  verification_methods: VerificationMethod[];
}

interface PerformanceMetrics {
  response_time_ms: number;
  throughput_qps?: number;
  cpu_usage_percent?: number;
  memory_usage_mb?: number;
  database_queries_count?: number;
  cache_hit_rate?: number;
}

interface Bottleneck {
  id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  category: 'algorithm' | 'database' | 'network' | 'memory' | 'frontend';
  location: string;                    // 文件:行号
  description: string;
  current_performance: string;         // "2.5秒响应时间"
  impact: string;                      // 对整体性能的影响
  root_cause: string;
}

interface Optimization {
  id: string;
  bottleneck_id: string;               // 关联的瓶颈ID
  title: string;
  description: string;
  code_before: string;                 // 优化前代码
  code_after: string;                  // 优化后代码
  complexity_before: string;           // "O(n²)"
  complexity_after: string;            // "O(n log n)"
  estimated_improvement: {
    response_time_reduction: string;   // "70%"
    memory_reduction?: string;
    query_reduction?: string;
  };
  difficulty: 'easy' | 'medium' | 'hard';
  breaking_changes: boolean;
  dependencies: string[];              // 需要的库或工具
}

interface ImprovementEstimate {
  overall_improvement: string;         // "65%响应时间减少"
  before_metrics: PerformanceMetrics;
  after_metrics: PerformanceMetrics;
  roi_analysis: string;                // 投入产出分析
}

interface PriorityTask {
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  optimization_ids: string[];
  estimated_effort: string;            // "2小时", "1天"
  expected_impact: string;             // "50%性能提升"
}

interface VerificationMethod {
  optimization_id: string;
  method: string;                      // 如何验证优化效果
  benchmark_code?: string;
  expected_result: string;
}
```

---


---

## TypeScript接口

### 基础输出接口

所有Skill的输出都继承自`BaseOutput`统一接口：

```typescript
interface BaseOutput {
  success: boolean;
  error?: {
    code: string;
    message: string;
    suggestedFix?: string;
  };
  metadata?: {
    requestId: string;
    timestamp: string;
    version: string;
  };
  warnings?: Array<{
    code: string;
    message: string;
    severity: 'low' | 'medium' | 'high';
  }>;
}
```

### 输入接口

```typescript
interface PerformanceOptimizerInput {{
  // ... 其他字段
}}
```

### 输出接口

```typescript
interface PerformanceOptimizerOutput extends BaseOutput {{
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}}
```

---

## Examples

### 示例1: API响应时间优化（2847ms → 385ms）

**用户请求**:
> "这个用户仪表盘API响应时间2.8秒，目标优化到500ms以内"

**当前代码** (app/api/dashboard.py):
```python
from flask import Blueprint, jsonify
from app.models import User, Post, Comment, Like
from app.database import db

bp = Blueprint('dashboard', __name__)

@bp.route('/api/dashboard/<int:user_id>')
def get_user_dashboard(user_id):
    # Query 1: 获取用户信息
    user = db.session.query(User).filter(User.id == user_id).first()

    # Query 2: 获取用户帖子
    posts = db.session.query(Post).filter(Post.user_id == user_id).all()

    # Query 3: 获取用户评论
    comments = db.session.query(Comment).filter(Comment.user_id == user_id).all()

    # Query 4: 获取用户点赞数
    likes = db.session.query(Like).filter(Like.user_id == user_id).all()

    # 序列化（CPU密集）
    serialized_posts = [serialize_post(p) for p in posts]
    serialized_comments = [serialize_comment(c) for c in comments]

    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar_url,
            'bio': user.bio,
            'created_at': user.created_at.isoformat()
        },
        'stats': {
            'posts_count': len(posts),
            'comments_count': len(comments),
            'likes_count': len(likes)
        },
        'recent_posts': serialized_posts[:10],
        'recent_comments': serialized_comments[:10]
    })

def serialize_post(post):
    """序列化帖子（每次查询数据库获取作者）"""
    author = db.session.query(User).filter(User.id == post.author_id).first()
    return {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': {'id': author.id, 'username': author.username},
        'created_at': post.created_at.isoformat()
    }

def serialize_comment(comment):
    """序列化评论"""
    return {
        'id': comment.id,
        'content': comment.content,
        'created_at': comment.created_at.isoformat()
    }
```

**性能分析结果**:
```
总响应时间: 2847ms

时间分布:
- 数据库查询: 2613ms (91.8%)
  ├─ Query 1 (user): 45ms
  ├─ Query 2 (posts): 320ms
  ├─ Query 3 (comments): 280ms
  ├─ Query 4 (likes): 150ms
  └─ N+1查询 (serialize_post): 1818ms (10次 × 181ms)

- CPU处理 (序列化): 234ms (8.2%)

瓶颈识别:
🔴 Critical: N+1查询问题 (serialize_post中重复查询User)
🟠 High: 执行4个独立查询（可合并）
🟡 Medium: 序列化逻辑可优化
```

**优化方案**:

**Skill执行**:
```python
result = performance_optimizer_skill.execute({
    "code_or_profile": "./app/api/dashboard.py",
    "optimization_target": "speed",
    "current_metrics": {
        "response_time_ms": 2847,
        "database_queries_count": 14
    },
    "target_metrics": {
        "response_time_ms": 500
    }
})
```

**生成的优化报告**:

```markdown
# 性能优化报告 - 用户仪表盘API

**当前性能**: 2847ms (平均)
**目标性能**: < 500ms
**预估优化后**: 385ms
**预计提升**: 86.5% ⚡

---

## 瓶颈分析

### 🔴 严重瓶颈 #1: N+1查询问题

**位置**: `app/api/dashboard.py:serialize_post:29`

**问题描述**:
`serialize_post`函数在循环中为每个帖子单独查询作者信息，导致N+1查询问题。当有10个帖子时，执行11次数据库查询（1次获取帖子 + 10次获取作者）。

**性能影响**:
- 额外查询次数: 10次
- 每次查询耗时: ~180ms
- 总影响: 1818ms (占总响应时间64%)

**SQL查询示例**:
```sql
-- Query 1
SELECT * FROM posts WHERE user_id = 123;  -- 返回10行

-- Query 2-11 (N+1问题)
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id = 1;  -- 重复查询同一作者
SELECT * FROM users WHERE id = 2;
... (共10次)
```

### 🟠 高危瓶颈 #2: 多次独立查询

**位置**: `app/api/dashboard.py:get_user_dashboard:8-14`

**问题描述**:
执行4个独立的SELECT查询获取用户、帖子、评论、点赞，可以通过JOIN或预加载优化。

**性能影响**:
- 数据库往返次数: 4次
- 网络延迟开销: ~60ms × 4 = 240ms

---

## 优化方案

### 优化 #1: 使用预加载解决N+1问题 (预计提升64%)

**优化前**:
```python
def serialize_post(post):
    # ❌ 每次查询数据库
    author = db.session.query(User).filter(User.id == post.author_id).first()
    return {
        'id': post.id,
        'title': post.title,
        'author': {'id': author.id, 'username': author.username},
    }

# 循环调用
serialized_posts = [serialize_post(p) for p in posts]
```

**优化后**:
```python
from sqlalchemy.orm import joinedload

@bp.route('/api/dashboard/<int:user_id>')
def get_user_dashboard_v2(user_id):
    # ✅ 使用joinedload预加载关联数据
    posts = db.session.query(Post)\
        .options(joinedload(Post.author))\  # 预加载作者
        .filter(Post.user_id == user_id)\
        .limit(10)\
        .all()

    # 序列化时不需要额外查询
    serialized_posts = [
        {
            'id': p.id,
            'title': p.title,
            'author': {
                'id': p.author.id,  # 已预加载，无额外查询
                'username': p.author.username
            }
        }
        for p in posts
    ]
```

**性能对比**:
- 查询次数: 11次 → 1次
- 响应时间: 2100ms → 350ms
- **提升**: 83%

**SQL查询**:
```sql
-- 优化后仅1次JOIN查询
SELECT posts.*, users.id, users.username
FROM posts
LEFT JOIN users ON posts.author_id = users.id
WHERE posts.user_id = 123
LIMIT 10;
```

---

### 优化 #2: 聚合查询减少数据库往返 (预计提升15%)

**优化前**:
```python
# ❌ 4次独立查询
user = db.session.query(User).filter(User.id == user_id).first()
posts = db.session.query(Post).filter(Post.user_id == user_id).all()
comments = db.session.query(Comment).filter(Post.user_id == user_id).all()
likes = db.session.query(Like).filter(Like.user_id == user_id).all()
```

**优化后**:
```python
from sqlalchemy import func

# ✅ 单次查询获取所有统计
user_stats = db.session.query(
    User.id,
    User.username,
    User.avatar_url,
    func.count(Post.id).label('posts_count'),
    func.count(Comment.id).label('comments_count'),
    func.count(Like.id).label('likes_count')
)\
.outerjoin(Post, Post.user_id == User.id)\
.outerjoin(Comment, Comment.user_id == User.id)\
.outerjoin(Like, Like.user_id == User.id)\
.filter(User.id == user_id)\
.group_by(User.id, User.username, User.avatar_url)\
.first()
```

**性能对比**:
- 查询次数: 4次 → 1次
- 响应时间: 795ms → 120ms
- **提升**: 85%

---

### 优化 #3: 仅查询需要的字段 (预计提升5%)

**优化前**:
```python
# ❌ 查询完整对象（包含不需要的大字段）
posts = db.session.query(Post).filter(Post.user_id == user_id).all()
```

**优化后**:
```python
# ✅ 仅查询需要的字段
posts = db.session.query(
    Post.id,
    Post.title,
    Post.created_at
).filter(Post.user_id == user_id)\
 .limit(10)\
 .all()
```

**性能对比**:
- 数据传输量: 120KB → 12KB
- 响应时间: 350ms → 315ms
- **提升**: 10%

---

### 优化 #4: 添加Redis缓存 (预计额外提升60%)

对于不经常变化的数据，添加缓存层：

```python
from django.core.cache import cache
import hashlib

@bp.route('/api/dashboard/<int:user_id>')
def get_user_dashboard_cached(user_id):
    # 生成缓存键
    cache_key = f'dashboard:user:{user_id}'

    # 尝试从缓存获取
    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data)

    # 缓存未命中，执行优化后的查询
    data = get_user_dashboard_optimized(user_id)

    # 存入缓存（5分钟TTL）
    cache.set(cache_key, data, timeout=300)

    return jsonify(data)

# 缓存失效：用户更新时主动删除
def update_user_profile(user_id, new_data):
    # 更新数据库...

    # 失效缓存
    cache_key = f'dashboard:user:{user_id}'
    cache.delete(cache_key)
```

**性能对比**:
- 缓存命中: 385ms → 15ms
- **提升**: 96% (缓存命中时)

---

## 完整优化代码

```python
from flask import Blueprint, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from django.core.cache import cache

bp = Blueprint('dashboard', __name__)

@bp.route('/api/dashboard/<int:user_id>')
def get_user_dashboard(user_id):
    # 尝试缓存
    cache_key = f'dashboard:user:{user_id}'
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)

    # 优化后的查询
    data = get_dashboard_data(user_id)

    # 缓存5分钟
    cache.set(cache_key, data, timeout=300)

    return jsonify(data)

def get_dashboard_data(user_id):
    # 查询1: 用户基本信息 + 统计（聚合查询）
    user_stats = db.session.query(
        User.id,
        User.username,
        User.avatar_url,
        User.bio,
        func.count(Post.id).label('posts_count'),
        func.count(Comment.id).label('comments_count'),
        func.count(Like.id).label('likes_count')
    )\
    .outerjoin(Post, Post.user_id == User.id)\
    .outerjoin(Comment, Comment.user_id == User.id)\
    .outerjoin(Like, Like.user_id == User.id)\
    .filter(User.id == user_id)\
    .group_by(User.id)\
    .first()

    # 查询2: 最近10篇帖子（预加载作者）
    recent_posts = db.session.query(
        Post.id,
        Post.title,
        Post.created_at,
        User.id.label('author_id'),
        User.username.label('author_username')
    )\
    .join(User, Post.author_id == User.id)\
    .filter(Post.user_id == user_id)\
    .order_by(Post.created_at.desc())\
    .limit(10)\
    .all()

    # 查询3: 最近10条评论
    recent_comments = db.session.query(
        Comment.id,
        Comment.content,
        Comment.created_at
    )\
    .filter(Comment.user_id == user_id)\
    .order_by(Comment.created_at.desc())\
    .limit(10)\
    .all()

    return {
        'user': {
            'id': user_stats.id,
            'username': user_stats.username,
            'avatar': user_stats.avatar_url,
            'bio': user_stats.bio
        },
        'stats': {
            'posts_count': user_stats.posts_count,
            'comments_count': user_stats.comments_count,
            'likes_count': user_stats.likes_count
        },
        'recent_posts': [
            {
                'id': p.id,
                'title': p.title,
                'author': {
                    'id': p.author_id,
                    'username': p.author_username
                },
                'created_at': p.created_at.isoformat()
            }
            for p in recent_posts
        ],
        'recent_comments': [
            {
                'id': c.id,
                'content': c.content,
                'created_at': c.created_at.isoformat()
            }
            for c in recent_comments
        ]
    }
```

---

## 性能对比总结

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 响应时间 | 2847ms | 385ms | **86.5%** ⚡ |
| 数据库查询 | 14次 | 3次 | **78.6%** |
| 缓存命中时 | N/A | 15ms | **99.5%** 🚀 |
| CPU使用 | 234ms | 35ms | **85%** |
| 内存占用 | 45MB | 12MB | **73%** |

---

## 验证方法

### 1. 基准测试

```python
import time
import requests

def benchmark_api(url, iterations=100):
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        response = requests.get(url)
        end = time.perf_counter()

        times.append(end - start)

    print(f"平均响应时间: {sum(times)/len(times)*1000:.2f}ms")
    print(f"P50: {sorted(times)[50]*1000:.2f}ms")
    print(f"P95: {sorted(times)[95]*1000:.2f}ms")
    print(f"P99: {sorted(times)[99]*1000:.2f}ms")

# 优化前
benchmark_api('http://localhost:5000/api/dashboard/123')
# 平均: 2847ms, P95: 3200ms

# 优化后
benchmark_api('http://localhost:5000/api/dashboard/123')
# 平均: 385ms, P95: 420ms
```

### 2. SQL查询日志

```python
# settings.py
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}

# 检查日志确认查询次数减少
# 优化前: 14 queries
# 优化后: 3 queries
```

### 3. 负载测试

```bash
# 使用Apache Bench
ab -n 1000 -c 10 http://localhost:5000/api/dashboard/123

# 优化前:
# Requests per second: 35.2 [#/sec]

# 优化后:
# Requests per second: 259.7 [#/sec]
# 提升: 7.4倍
```

---

## 实施优先级

### P0 - 立即实施 (今天)
- ✅ 优化 #1: 解决N+1查询问题（2小时工作量，64%提升）
- ✅ 优化 #2: 聚合查询（1小时工作量，15%提升）

### P1 - 本周完成
- ✅ 优化 #3: 字段优化（30分钟工作量，5%提升）
- ✅ 优化 #4: 添加Redis缓存（3小时工作量，额外60%提升）

### P2 - 后续优化
- 添加数据库索引（如果查询仍慢）
- 实施CDN缓存静态资源
- 考虑读写分离

---

**生成时间**: 2025-12-12T14:00:00Z
**优化工具**: Claude Code performance-optimizer v2.0.0
```

---

## Best Practices

### 1. 性能优化金字塔

```
┌────────────────────────────┐
│  算法优化 (最大ROI)        │  ← 优先级最高
├────────────────────────────┤
│  数据库查询优化            │
├────────────────────────────┤
│  缓存策略                  │
├────────────────────────────┤
│  并发与异步                │
├────────────────────────────┤
│  前端资源优化              │
├────────────────────────────┤
│  硬件升级 (最小ROI)        │  ← 最后考虑
└────────────────────────────┘
```

### 2. 80/20法则

专注于优化占用80%时间的20%代码。

### 3. 始终测量

"过早优化是万恶之源" - Donald Knuth

先profiling，再优化，最后验证。

### 4. 权衡取舍

性能优化常涉及权衡：
- 时间 vs 空间
- 复杂度 vs 可维护性
- 缓存 vs 数据一致性

### 5. 持续监控

生产环境性能监控工具：
- New Relic
- Datadog
- Sentry Performance
- Application Insights

---

## Related Skills

- `code-review`: 代码审查应包含性能检查
- `test-automation`: 编写性能测试用例
- `debugger`: 性能问题调试
- `security-audit`: 某些性能优化可能影响安全

---

## Version History

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 2.0.0 | 2025-12-12 | 重大升级：算法分析、前端优化、多层缓存 |
| 1.5.0 | 2025-10-01 | 添加异步优化、连接池 |
| 1.0.0 | 2025-06-01 | 初始版本：基础数据库优化 |

---

**生成时间**: 2025-12-12T14:30:00Z
**Skill版本**: performance-optimizer v2.0.0
**文档字数**: 8,200+
