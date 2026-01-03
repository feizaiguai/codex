---
name: 16-api-integrator-G
description: API integrator for intelligent third-party API integration. Supports multiple auth methods (OAuth2/JWT/API Key/Basic Auth), rate limiting management (Token Bucket), exponential backoff retry, auto-pagination, OpenAPI auto-parsing. Use for third-party API integration, webhook handling, API gateway development.
---

# 16-api-integrator - API集成器

**版本**: 2.0.0
**优先级**: P0 (核心功能)
**类别**: 外部集成 (External Integration)

## 描述

智能集成第三方API,自动处理认证、请求构建、响应解析、错误重试和速率限制。该Skill为开发者提供统一的API集成接口,支持多种认证方式(API Key, OAuth2, JWT, Basic Auth),自动处理分页、重试和速率限制,大幅简化外部服务集成工作。

**核心能力**:

- **API发现与配置**: OpenAPI/Swagger规范自动解析、API文档智能分析、认证方式自动检测、端点自动发现
- **请求智能管理**: 智能请求构建、参数验证与转换、指数退避重试策略、速率限制自动遵守
- **响应高级处理**: 多格式自动解析(JSON/XML/Protobuf)、错误处理与映射、数据转换规范化、分页自动处理
- **高级功能**: 批量请求优化、智能响应缓存、请求/响应日志、性能监控与告警

## Instructions

### 触发条件

此Skill应在以下场景自动触发或被调用:

```yaml
自动触发场景:
  - 用户明确请求:
      - "调用 XXX API获取数据"
      - "集成 XXX 服务"
      - "从 XXX 导入数据"
      - "使用 XXX API创建资源"
      - "调用OpenAPI规范的API"

  - 上下文检测:
      - 需要访问外部API服务
      - 检测到OpenAPI/Swagger文档
      - 需要OAuth2认证流程
      - 批量数据获取需求

  - 特定关键词:
      - 包含"API"、"接口"、"调用"等词汇
      - 包含知名服务名称 (GitHub, Google, Stripe等)
      - 包含"集成"、"对接"、"同步"
```

### 执行流程

```mermaid
graph TD
    A[接收API配置] --> B{检测认证类型}
    B -->|API Key| C[添加API Key到Header]
    B -->|OAuth2| D[执行OAuth2流程]
    B -->|JWT| E[附加JWT Token]
    B -->|Basic| F[Base64编码认证]

    C --> G[构建请求]
    D --> G
    E --> G
    F --> G

    G --> H[应用速率限制]
    H --> I[发送HTTP请求]

    I --> J{请求成功?}
    J -->|是| K[解析响应]
    J -->|否| L{可重试?}

    L -->|是| M[指数退避等待]
    L -->|否| N[返回错误]

    M --> I

    K --> O{需要分页?}
    O -->|是| P[获取下一页]
    O -->|否| Q[返回结果]

    P --> H
```

**详细执行步骤**:

1. **API配置解析** (50-100ms)
   - 解析baseUrl和endpoint
   - 识别HTTP方法(GET/POST/PUT/DELETE/PATCH)
   - 替换路径参数 (e.g., `/users/{id}`)
   - 验证必需参数

2. **认证处理** (100-500ms)
   - **API Key**: 添加到Header或Query参数
   - **OAuth2**:
     - 检查access_token有效性
     - 如过期,使用refresh_token刷新
     - 执行完整OAuth2流程(如需要)
   - **JWT**: 验证token,附加到Authorization header
   - **Basic Auth**: Base64编码username:password

3. **请求构建** (50-100ms)
   - 合并默认headers和自定义headers
   - 序列化请求body (JSON/Form/Multipart)
   - 构建query参数字符串
   - 设置timeout和其他选项

4. **速率限制检查** (10-50ms)
   - 检查当前时间窗口请求数
   - 如超过限制,等待到下一个窗口
   - 使用令牌桶算法或滑动窗口
   - 记录速率限制状态

5. **发送HTTP请求** (100-5000ms)
   - 使用axios/fetch发送请求
   - 记录请求开始时间
   - 设置超时timer
   - 处理网络错误

6. **错误处理与重试** (可变)
   - **4xx错误**: 不重试,返回错误
   - **5xx错误**: 可重试
   - **网络错误**: 可重试
   - **超时**: 可重试
   - 指数退避策略:
     - 第1次重试: 等待initialDelay
     - 第2次重试: 等待initialDelay * 2
     - 第3次重试: 等待initialDelay * 4

7. **响应解析** (50-200ms)
   - 根据Content-Type解析:
     - `application/json` → JSON.parse
     - `application/xml` → XML解析
     - `application/x-protobuf` → Protobuf解码
     - `text/*` → 纯文本
   - 提取响应headers
   - 提取速率限制信息

8. **分页处理** (可选)
   - **Offset分页**: `?offset=0&limit=100`
   - **Cursor分页**: `?cursor=xxx`
   - **Page分页**: `?page=1&per_page=100`
   - 自动获取所有页直到maxPages

9. **缓存处理** (如启用)
   - 检查缓存键是否存在
   - 命中缓存直接返回
   - 未命中则执行请求并缓存结果
   - 遵守TTL过期策略

10. **返回结果** (10-20ms)
    - 构建统一的输出格式
    - 包含请求/响应元数据
    - 记录性能指标
    - 触发监控告警(如需要)

**总耗时**: 通常300ms - 6000ms (取决于API响应时间和重试)

## Input Parameters

```typescript
/**
 * API Integrator Input Configuration
 * API集成器输入配置
 */
interface APIIntegratorInput {
  // ============ API基础配置 ============

  /**
   * OpenAPI/Swagger规范
   * @description URL或完整的OpenAPI JSON/YAML内容
   * @example 'https://petstore3.swagger.io/api/v3/openapi.json'
   */
  apiSpec?: string;

  /**
   * API基础URL
   * @required
   * @example 'https://api.github.com'
   */
  baseUrl: string;

  /**
   * API端点路径
   * @required
   * @example '/repos/{owner}/{repo}/pulls'
   * @description 支持路径参数,使用{param}语法
   */
  endpoint: string;

  /**
   * HTTP方法
   * @required
   */
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD' | 'OPTIONS';

  // ============ 认证配置 ============

  /**
   * 认证配置
   * @required
   */
  auth: {
    /**
     * 认证类型
     */
    type: 'apiKey' | 'oauth2' | 'jwt' | 'basic' | 'bearer' | 'none';

    /**
     * 认证凭据
     */
    credentials: {
      /**
       * API Key认证
       * @description 将自动添加到Header或Query参数
       */
      apiKey?: string;

      /**
       * API Key位置
       * @default 'header'
       */
      apiKeyLocation?: 'header' | 'query';

      /**
       * API Key的Header名称
       * @default 'X-API-Key'
       */
      apiKeyHeaderName?: string;

      /**
       * OAuth2认证
       */
      oauth?: {
        clientId: string;
        clientSecret: string;
        accessToken?: string;
        refreshToken?: string;
        tokenEndpoint?: string;
        scope?: string[];
      };

      /**
       * JWT认证
       */
      jwt?: string;

      /**
       * Basic认证
       */
      basic?: {
        username: string;
        password: string;
      };

      /**
       * Bearer Token
       */
      bearer?: string;
    };
  };

  // ============ 请求配置 ============

  /**
   * 请求配置
   */
  request?: {
    /**
     * 请求Headers
     * @example { 'Content-Type': 'application/json', 'Accept': 'application/json' }
     */
    headers?: Record<string, string>;

    /**
     * URL查询参数
     * @example { state: 'open', sort: 'created', per_page: 30 }
     */
    queryParams?: Record<string, any>;

    /**
     * 路径参数
     * @example { owner: 'facebook', repo: 'react' }
     * @description 用于替换endpoint中的{param}占位符
     */
    pathParams?: Record<string, string>;

    /**
     * 请求体
     * @description 自动根据Content-Type序列化
     */
    body?: any;

    /**
     * 请求超时(毫秒)
     * @default 30000
     * @min 1000
     * @max 300000
     */
    timeout?: number;

    /**
     * Content-Type
     * @default 'application/json'
     */
    contentType?: 'application/json' | 'application/x-www-form-urlencoded' | 'multipart/form-data' | 'text/plain';
  };

  // ============ 高级选项 ============

  /**
   * 高级选项
   */
  options?: {
    /**
     * 重试配置
     */
    retry?: {
      /**
       * 最大重试次数
       * @default 3
       * @min 0
       * @max 10
       */
      maxAttempts: number;

      /**
       * 退避策略
       * @default 'exponential'
       * @description
       *   - linear: 每次等待固定时间
       *   - exponential: 指数增长等待时间
       */
      backoff: 'linear' | 'exponential';

      /**
       * 初始延迟(毫秒)
       * @default 1000
       */
      initialDelay: number;

      /**
       * 最大延迟(毫秒)
       * @default 60000
       */
      maxDelay?: number;

      /**
       * 可重试的HTTP状态码
       * @default [408, 429, 500, 502, 503, 504]
       */
      retryableStatusCodes?: number[];
    };

    /**
     * 速率限制配置
     */
    rateLimit?: {
      /**
       * 时间窗口内最大请求数
       * @example 5000
       */
      maxRequests: number;

      /**
       * 时间窗口(毫秒)
       * @example 3600000 (1小时)
       */
      perWindow: number;

      /**
       * 速率限制策略
       * @default 'sliding-window'
       */
      strategy?: 'fixed-window' | 'sliding-window' | 'token-bucket';
    };

    /**
     * 缓存配置
     */
    cache?: {
      /**
       * 启用缓存
       * @default false
       */
      enabled: boolean;

      /**
       * 缓存TTL(秒)
       * @default 300
       */
      ttl: number;

      /**
       * 缓存键生成策略
       * @default 'url-params'
       * @description
       *   - url: 仅URL
       *   - url-params: URL + 查询参数
       *   - url-params-body: URL + 查询参数 + 请求体
       */
      keyStrategy?: 'url' | 'url-params' | 'url-params-body';

      /**
       * 缓存仅GET请求
       * @default true
       */
      getOnly?: boolean;
    };

    /**
     * 分页配置
     */
    pagination?: {
      /**
       * 启用自动分页
       * @default false
       */
      enabled: boolean;

      /**
       * 分页策略
       */
      strategy: 'offset' | 'cursor' | 'page' | 'link-header';

      /**
       * 最大页数
       * @default 10
       * @description 防止无限循环
       */
      maxPages?: number;

      /**
       * 每页大小
       * @default 100
       */
      pageSize?: number;

      /**
       * Offset分页配置
       */
      offset?: {
        offsetParam: string;    // e.g., 'offset'
        limitParam: string;     // e.g., 'limit'
      };

      /**
       * Cursor分页配置
       */
      cursor?: {
        cursorParam: string;    // e.g., 'cursor'
        nextCursorPath: string; // e.g., 'pagination.next_cursor'
      };

      /**
       * Page分页配置
       */
      page?: {
        pageParam: string;      // e.g., 'page'
        perPageParam: string;   // e.g., 'per_page'
      };
    };

    /**
     * 日志配置
     */
    logging?: {
      /**
       * 启用请求/响应日志
       * @default false
       */
      enabled: boolean;

      /**
       * 日志级别
       * @default 'info'
       */
      level?: 'debug' | 'info' | 'warn' | 'error';

      /**
       * 记录请求体
       * @default false
       */
      logRequestBody?: boolean;

      /**
       * 记录响应体
       * @default false
       */
      logResponseBody?: boolean;

      /**
       * 敏感字段掩码
       * @example ['password', 'apiKey', 'token']
       */
      sensitiveFields?: string[];
    };

    /**
     * 代理配置
     */
    proxy?: {
      host: string;
      port: number;
      auth?: {
        username: string;
        password: string;
      };
      protocol?: 'http' | 'https' | 'socks4' | 'socks5';
    };
  };
}
```

## Output Format

```typescript
/**
 * API Integrator Output Result
 * API集成器输出结果
 */
interface APIIntegratorOutput {
  // ============ 请求信息 ============

  /**
   * 请求信息
   */
  request: {
    /**
     * 完整请求URL
     * @example 'https://api.github.com/repos/facebook/react/pulls?state=open&per_page=30'
     */
    url: string;

    /**
     * HTTP方法
     */
    method: string;

    /**
     * 请求时间戳 (ISO 8601)
     */
    timestamp: string;

    /**
     * 请求Headers
     * @description 敏感信息(如API Key)已脱敏
     */
    headers: Record<string, string>;

    /**
     * 请求体 (如果有)
     * @description 仅在logging.logRequestBody=true时存在
     */
    body?: any;
  };

  // ============ 响应数据 ============

  /**
   * 响应数据
   */
  response: {
    /**
     * HTTP状态码
     * @example 200, 404, 500
     */
    status: number;

    /**
     * 状态文本
     * @example 'OK', 'Not Found', 'Internal Server Error'
     */
    statusText: string;

    /**
     * 响应Headers
     */
    headers: Record<string, string>;

    /**
     * 解析后的响应数据
     * @description 根据Content-Type自动解析
     */
    data: any;

    /**
     * 原始响应数据
     * @description 仅在logging.logResponseBody=true时存在
     */
    rawData?: string;

    /**
     * Content-Type
     */
    contentType?: string;
  };

  // ============ 执行元数据 ============

  /**
   * 执行元数据
   */
  metadata: {
    /**
     * 请求总耗时(毫秒)
     * @description 包括重试和等待时间
     */
    duration: number;

    /**
     * 实际HTTP请求耗时(毫秒)
     * @description 不包括重试等待
     */
    networkDuration?: number;

    /**
     * 重试次数
     * @min 0
     */
    retryCount: number;

    /**
     * 是否命中缓存
     */
    cacheHit: boolean;

    /**
     * 缓存键 (如果使用缓存)
     */
    cacheKey?: string;

    /**
     * 速率限制信息
     */
    rateLimit?: {
      /**
       * 剩余请求配额
       */
      remaining: number;

      /**
       * 总配额
       */
      limit: number;

      /**
       * 配额重置时间 (Unix timestamp)
       */
      reset: number;

      /**
       * 当前窗口使用率 (%)
       */
      usage: number;
    };

    /**
     * 分页信息 (如果使用分页)
     */
    pagination?: {
      /**
       * 当前页码
       */
      currentPage: number;

      /**
       * 总页数 (如果可知)
       */
      totalPages?: number;

      /**
       * 总记录数 (如果可知)
       */
      totalRecords?: number;

      /**
       * 是否有下一页
       */
      hasNext: boolean;

      /**
       * 下一页cursor/offset
       */
      nextCursor?: string;
    };

    /**
     * 性能指标
     */
    performance?: {
      /**
       * DNS查询时间 (ms)
       */
      dnsLookup?: number;

      /**
       * TCP连接时间 (ms)
       */
      tcpConnection?: number;

      /**
       * TLS握手时间 (ms)
       */
      tlsHandshake?: number;

      /**
       * 首字节时间 (ms)
       */
      timeToFirstByte?: number;

      /**
       * 内容下载时间 (ms)
       */
      contentDownload?: number;
    };
  };

  // ============ 错误信息 ============

  /**
   * 错误信息 (仅在请求失败时存在)
   */
  error?: {
    /**
     * 错误代码
     * @example 'NETWORK_ERROR', 'TIMEOUT', 'AUTH_FAILED', 'RATE_LIMIT_EXCEEDED'
     */
    code: string;

    /**
     * 错误消息
     */
    message: string;

    /**
     * HTTP状态码 (如果是HTTP错误)
     */
    statusCode?: number;

    /**
     * 详细错误信息
     */
    details?: any;

    /**
     * 重试历史
     */
    retryHistory?: Array<{
      attempt: number;
      timestamp: string;
      error: string;
      waitTime: number;
    }>;

    /**
     * 是否可恢复
     * @description true表示可以通过重试解决
     */
    recoverable: boolean;

    /**
     * 建议操作
     */
    suggestedAction?: string;
  };

  // ============ 警告信息 ============

  /**
   * 警告信息
   * @description 非致命问题,但可能影响使用
   */
  warnings?: Array<{
    code: string;
    message: string;
    severity: 'low' | 'medium' | 'high';
  }>;
}
```


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
interface APIIntegratorInput {

  quotaMonitoring?: {
    enabled: boolean;
    dailyLimit?: number;
    warningThreshold?: number;
    resetTime?: string;
    fallbackStrategy?: 'cache' | 'queue' | 'fail';
    provider?: string;
  };
}
```

### 输出接口

```typescript
interface APIIntegratorOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段

  quotaUsage?: {
    used: number;
    limit: number;
    remaining: number;
    percentUsed: number;
    resetAt: string;
    willExceed: boolean;
    costEstimate?: number;
  };
}
```

---

## Examples

### Example 1: GitHub API集成 - 获取仓库Pull Requests

**场景**: 开发者需要获取React仓库的开放PR列表并分析

```typescript
import { apiIntegrator } from '@claude-skills/api-integrator';

// 配置GitHub API集成
const githubAPIConfig: APIIntegratorInput = {
  baseUrl: 'https://api.github.com',
  endpoint: '/repos/{owner}/{repo}/pulls',
  method: 'GET',

  // GitHub使用Personal Access Token作为Bearer认证
  auth: {
    type: 'bearer',
    credentials: {
      bearer: process.env.GITHUB_TOKEN!
    }
  },

  // 请求配置
  request: {
    headers: {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'MyApp/1.0'
    },
    pathParams: {
      owner: 'facebook',
      repo: 'react'
    },
    queryParams: {
      state: 'open',
      sort: 'created',
      direction: 'desc',
      per_page: 30
    },
    timeout: 10000
  },

  // 高级选项
  options: {
    // 重试配置
    retry: {
      maxAttempts: 3,
      backoff: 'exponential',
      initialDelay: 1000,
      maxDelay: 10000
    },

    // 速率限制 (GitHub: 5000 req/hour for authenticated users)
    rateLimit: {
      maxRequests: 5000,
      perWindow: 3600000,  // 1 hour
      strategy: 'sliding-window'
    },

    // 缓存配置
    cache: {
      enabled: true,
      ttl: 300,  // 5 minutes
      keyStrategy: 'url-params',
      getOnly: true
    },

    // 启用日志
    logging: {
      enabled: true,
      level: 'info',
      logRequestBody: false,
      logResponseBody: true,
      sensitiveFields: ['token', 'apiKey', 'password']
    }
  }
};

console.log('🔄 调用GitHub API获取React仓库的Pull Requests...\n');

// 执行API调用
const result = await apiIntegrator.execute(githubAPIConfig);

// 错误处理
if (result.error) {
  console.error(`❌ API调用失败: ${result.error.message}`);
  console.error(`   错误代码: ${result.error.code}`);

  if (result.error.retryHistory) {
    console.error(`   重试历史:`);
    result.error.retryHistory.forEach(retry => {
      console.error(`      尝试 ${retry.attempt}: ${retry.error} (等待${retry.waitTime}ms)`);
    });
  }

  if (result.error.suggestedAction) {
    console.error(`   建议操作: ${result.error.suggestedAction}`);
  }

  return;
}

// 成功响应
console.log('✅ API调用成功!');
console.log(`📊 状态码: ${result.response.status} ${result.response.statusText}`);
console.log(`⏱️  请求耗时: ${result.metadata.duration}ms`);
console.log(`🔄 重试次数: ${result.metadata.retryCount}`);
console.log(`💾 缓存命中: ${result.metadata.cacheHit ? '是' : '否'}\n`);

// 速率限制信息
if (result.metadata.rateLimit) {
  const rateLimit = result.metadata.rateLimit;
  console.log('⚡ 速率限制状态:');
  console.log(`   剩余配额: ${rateLimit.remaining} / ${rateLimit.limit}`);
  console.log(`   使用率: ${rateLimit.usage.toFixed(1)}%`);
  console.log(`   重置时间: ${new Date(rateLimit.reset * 1000).toLocaleString()}\n`);

  // 告警: 配额使用超过80%
  if (rateLimit.usage > 80) {
    console.warn(`⚠️  警告: API配额使用率已超过${rateLimit.usage.toFixed(0)}%`);
  }
}

// 处理响应数据
const pullRequests = result.response.data;

console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`找到 ${pullRequests.length} 个开放的Pull Requests`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

// 显示PR列表
pullRequests.forEach((pr: any, index: number) => {
  console.log(`[${index + 1}] #${pr.number}: ${pr.title}`);
  console.log(`    👤 作者: ${pr.user.login}`);
  console.log(`    📅 创建: ${new Date(pr.created_at).toLocaleDateString()}`);
  console.log(`    📝 描述: ${pr.body ? pr.body.substring(0, 100) + '...' : '无'}`);
  console.log(`    🔗 URL: ${pr.html_url}`);
  console.log(`    💬 评论: ${pr.comments} | ✅ 审核: ${pr.requested_reviewers?.length || 0}`);
  console.log(`    🏷️  标签: ${pr.labels.map((l: any) => l.name).join(', ') || '无'}\n`);
});

// 统计分析
const stats = {
  totalPRs: pullRequests.length,
  averageComments: pullRequests.reduce((sum: number, pr: any) => sum + pr.comments, 0) / pullRequests.length,
  withLabels: pullRequests.filter((pr: any) => pr.labels.length > 0).length,
  withReviewers: pullRequests.filter((pr: any) => pr.requested_reviewers && pr.requested_reviewers.length > 0).length
};

console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`📊 统计分析`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`总PR数: ${stats.totalPRs}`);
console.log(`平均评论数: ${stats.averageComments.toFixed(1)}`);
console.log(`带标签PR: ${stats.withLabels} (${(stats.withLabels / stats.totalPRs * 100).toFixed(0)}%)`);
console.log(`待审核PR: ${stats.withReviewers} (${(stats.withReviewers / stats.totalPRs * 100).toFixed(0)}%)`);

// 性能指标
if (result.metadata.performance) {
  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`⚡ 性能指标`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  const perf = result.metadata.performance;
  console.log(`DNS查询: ${perf.dnsLookup}ms`);
  console.log(`TCP连接: ${perf.tcpConnection}ms`);
  console.log(`TLS握手: ${perf.tlsHandshake}ms`);
  console.log(`首字节: ${perf.timeToFirstByte}ms`);
  console.log(`内容下载: ${perf.contentDownload}ms`);
}
```

**预期输出示例**:

```
🔄 调用GitHub API获取React仓库的Pull Requests...

✅ API调用成功!
📊 状态码: 200 OK
⏱️  请求耗时: 342ms
🔄 重试次数: 0
💾 缓存命中: 否

⚡ 速率限制状态:
   剩余配额: 4987 / 5000
   使用率: 0.3%
   重置时间: 2024/12/10 15:30:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
找到 30 个开放的Pull Requests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] #28456: Fix: useEffect cleanup in StrictMode
    👤 作者: gaearon
    📅 创建: 2024/01/10
    📝 描述: This PR fixes an issue where useEffect cleanup functions were being called twice in Strict Mode...
    🔗 URL: https://github.com/facebook/react/pull/28456
    💬 评论: 12 | ✅ 审核: 3
    🏷️  标签: bug, react-hooks

[2] #28455: Add React.use() hook for Suspense
    👤 作者: acdlite
    📅 创建: 2024/01/09
    📝 描述: Implements the new React.use() hook that allows reading promises and context values in render...
    🔗 URL: https://github.com/facebook/react/pull/28455
    💬 评论: 45 | ✅ 审核: 5
    🏷️  标签: enhancement, react-suspense, breaking-change

[3] #28454: Optimize fiber reconciliation performance
    👤 作者: sebmarkbage
    📅 创建: 2024/01/09
    📝 描述: Improves fiber reconciliation algorithm by implementing a new diffing strategy that reduces...
    🔗 URL: https://github.com/facebook/react/pull/28454
    💬 评论: 23 | ✅ 审核: 4
    🏷️  标签: performance, react-reconciler

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 统计分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总PR数: 30
平均评论数: 18.7
带标签PR: 28 (93%)
待审核PR: 25 (83%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ 性能指标
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNS查询: 12ms
TCP连接: 45ms
TLS握手: 67ms
首字节: 156ms
内容下载: 62ms
```

---

### Example 2: OAuth2完整认证流程 - Google Drive集成

**场景**: 应用需要访问用户的Google Drive文件

```typescript
import { apiIntegrator } from '@claude-skills/api-integrator';
import express from 'express';

const app = express();
const PORT = 3000;

// OAuth2配置
const oauth2Config = {
  clientId: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  redirectUri: `http://localhost:${PORT}/callback`,
  scopes: [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/userinfo.profile'
  ]
};

// Step 1: 生成授权URL,重定向用户
app.get('/auth', (req, res) => {
  const authUrlConfig: APIIntegratorInput = {
    baseUrl: 'https://accounts.google.com',
    endpoint: '/o/oauth2/v2/auth',
    method: 'GET',

    auth: {
      type: 'none',
      credentials: {}
    },

    request: {
      queryParams: {
        client_id: oauth2Config.clientId,
        redirect_uri: oauth2Config.redirectUri,
        response_type: 'code',
        scope: oauth2Config.scopes.join(' '),
        access_type: 'offline',  // 获取refresh token
        prompt: 'consent'        // 强制显示授权页面
      }
    }
  };

  // 构建授权URL
  const authUrl = apiIntegrator.buildUrl(authUrlConfig);
  console.log(`🔐 重定向到授权页面: ${authUrl}`);

  res.redirect(authUrl);
});

// Step 2: 处理OAuth回调,交换access token
app.get('/callback', async (req, res) => {
  const authCode = req.query.code as string;

  if (!authCode) {
    return res.status(400).send('Missing authorization code');
  }

  console.log(`\n✅ 收到授权码: ${authCode.substring(0, 20)}...\n`);

  // 使用授权码换取访问令牌
  const tokenConfig: APIIntegratorInput = {
    baseUrl: 'https://oauth2.googleapis.com',
    endpoint: '/token',
    method: 'POST',

    auth: {
      type: 'none',
      credentials: {}
    },

    request: {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: {
        code: authCode,
        client_id: oauth2Config.clientId,
        client_secret: oauth2Config.clientSecret,
        redirect_uri: oauth2Config.redirectUri,
        grant_type: 'authorization_code'
      }
    }
  };

  console.log('🔄 交换访问令牌...');
  const tokenResult = await apiIntegrator.execute(tokenConfig);

  if (tokenResult.error) {
    console.error(`❌ 令牌交换失败: ${tokenResult.error.message}`);
    return res.status(500).send('Token exchange failed');
  }

  const tokens = tokenResult.response.data;
  console.log('✅ 成功获取令牌!');
  console.log(`   Access Token: ${tokens.access_token.substring(0, 30)}...`);
  console.log(`   Refresh Token: ${tokens.refresh_token?.substring(0, 30)}...`);
  console.log(`   Expires In: ${tokens.expires_in} seconds\n`);

  // 保存令牌(实际应用应该加密存储到数据库)
  global.googleTokens = tokens;

  // Step 3: 使用访问令牌调用Google Drive API
  await listDriveFiles(tokens.access_token);

  res.send('Authorization successful! Check console for Drive files.');
});

// 获取Drive文件列表
async function listDriveFiles(accessToken: string) {
  const driveConfig: APIIntegratorInput = {
    baseUrl: 'https://www.googleapis.com',
    endpoint: '/drive/v3/files',
    method: 'GET',

    auth: {
      type: 'bearer',
      credentials: {
        bearer: accessToken
      }
    },

    request: {
      queryParams: {
        pageSize: 20,
        fields: 'nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, owners)',
        orderBy: 'modifiedTime desc',
        q: "trashed = false"  // 仅显示未删除的文件
      }
    },

    options: {
      retry: {
        maxAttempts: 3,
        backoff: 'exponential',
        initialDelay: 1000
      },

      // 自动分页
      pagination: {
        enabled: true,
        strategy: 'cursor',
        maxPages: 5,
        cursor: {
          cursorParam: 'pageToken',
          nextCursorPath: 'nextPageToken'
        }
      }
    }
  };

  console.log('🔄 获取Google Drive文件...\n');
  const driveResult = await apiIntegrator.execute(driveConfig);

  if (driveResult.error) {
    console.error(`❌ 获取文件失败: ${driveResult.error.message}`);
    return;
  }

  const files = driveResult.response.data.files;

  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`📁 Google Drive文件 (共${files.length}个)`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

  files.forEach((file: any, index: number) => {
    const sizeKB = file.size ? (parseInt(file.size) / 1024).toFixed(1) : 'N/A';
    const owner = file.owners?.[0]?.displayName || 'Unknown';

    console.log(`[${index + 1}] ${file.name}`);
    console.log(`    📄 类型: ${file.mimeType}`);
    console.log(`    💾 大小: ${sizeKB} KB`);
    console.log(`    👤 所有者: ${owner}`);
    console.log(`    📅 创建: ${new Date(file.createdTime).toLocaleDateString()}`);
    console.log(`    🔄 修改: ${new Date(file.modifiedTime).toLocaleDateString()}`);
    console.log(`    🔗 ID: ${file.id}\n`);
  });

  // 分页信息
  if (driveResult.metadata.pagination) {
    const paging = driveResult.metadata.pagination;
    console.log(`📄 分页信息:`);
    console.log(`   当前页: ${paging.currentPage}`);
    console.log(`   总页数: ${paging.totalPages || '未知'}`);
    console.log(`   是否有下一页: ${paging.hasNext ? '是' : '否'}`);
  }
}

// 启动服务器
app.listen(PORT, () => {
  console.log(`🚀 OAuth2 Server running at http://localhost:${PORT}`);
  console.log(`\n请访问: http://localhost:${PORT}/auth 开始授权流程\n`);
});
```

**OAuth2流程输出示例**:

```
🚀 OAuth2 Server running at http://localhost:3000

请访问: http://localhost:3000/auth 开始授权流程

🔐 重定向到授权页面: https://accounts.google.com/o/oauth2/v2/auth?client_id=...&scope=...

[用户在浏览器中完成授权]

✅ 收到授权码: 4/0AX4XfWhE5jKZ...

🔄 交换访问令牌...
✅ 成功获取令牌!
   Access Token: ya29.a0AfH6SMBx3K9...
   Refresh Token: 1//0gHPyC5fT9K...
   Expires In: 3600 seconds

🔄 获取Google Drive文件...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Google Drive文件 (共20个)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] 2024项目计划.docx
    📄 类型: application/vnd.openxmlformats-officedocument.wordprocessingml.document
    💾 大小: 245.3 KB
    👤 所有者: John Doe
    📅 创建: 2024/01/05
    🔄 修改: 2024/01/10
    🔗 ID: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs

[2] Q4财务报表.xlsx
    📄 类型: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
    💾 大小: 487.2 KB
    👤 所有者: Jane Smith
    📅 创建: 2024/01/03
    🔄 修改: 2024/01/09
    🔗 ID: 1ZdR3L3qP_D9C1YfHePLNs4zRQKmPcHXv

📄 分页信息:
   当前页: 1
   总页数: 3
   是否有下一页: 是
```

---

### Example 3: 批量请求与速率限制自动处理

**场景**: 需要批量获取100个用户的详细信息,遵守API速率限制

```typescript
import { apiIntegrator } from '@claude-skills/api-integrator';

// 生成100个用户ID
const userIds = Array.from({ length: 100 }, (_, i) => i + 1);

console.log(`🔄 开始批量获取 ${userIds.length} 个用户信息...\n`);
console.log(`⚙️  速率限制配置: 10 请求/秒\n`);

// 配置API请求模板
const batchConfigTemplate: APIIntegratorInput = {
  baseUrl: 'https://jsonplaceholder.typicode.com',
  endpoint: '/users/{id}',
  method: 'GET',

  auth: {
    type: 'apiKey',
    credentials: {
      apiKey: process.env.API_KEY!,
      apiKeyLocation: 'header',
      apiKeyHeaderName: 'X-API-Key'
    }
  },

  options: {
    // 速率限制: 每秒最多10个请求
    rateLimit: {
      maxRequests: 10,
      perWindow: 1000,  // 1 second
      strategy: 'token-bucket'
    },

    // 重试配置
    retry: {
      maxAttempts: 3,
      backoff: 'exponential',
      initialDelay: 500,
      maxDelay: 5000,
      retryableStatusCodes: [408, 429, 500, 502, 503, 504]
    },

    // 启用详细日志
    logging: {
      enabled: true,
      level: 'info'
    }
  }
};

const startTime = Date.now();

// 生成所有请求配置
const batchConfigs = userIds.map(id => ({
  ...batchConfigTemplate,
  endpoint: batchConfigTemplate.endpoint.replace('{id}', id.toString()),
  request: {
    ...batchConfigTemplate.request,
    pathParams: { id: id.toString() }
  }
}));

// 执行批量请求 (API Integrator内部自动处理速率限制)
console.log(`⏳ 执行批量请求...\n`);
const results = await apiIntegrator.executeBatch(batchConfigs);

const duration = Date.now() - startTime;

// 统计结果
const successful = results.filter(r => !r.error);
const failed = results.filter(r => r.error);
const totalRetries = results.reduce((sum, r) => sum + r.metadata.retryCount, 0);
const avgDuration = results
  .filter(r => !r.error)
  .reduce((sum, r) => sum + r.metadata.duration, 0) / successful.length;

console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`📊 批量请求完成统计`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

console.log(`✅ 成功: ${successful.length} / ${userIds.length} (${(successful.length / userIds.length * 100).toFixed(1)}%)`);
console.log(`❌ 失败: ${failed.length}`);
console.log(`🔄 总重试次数: ${totalRetries}`);
console.log(`⏱️  总耗时: ${(duration / 1000).toFixed(2)}秒`);
console.log(`📈 平均耗时: ${avgDuration.toFixed(0)}ms/请求`);
console.log(`⚡ 实际速率: ${((userIds.length / duration) * 1000).toFixed(1)} 请求/秒`);
console.log(`🎯 速率限制遵守: ${((userIds.length / duration) * 1000) <= 10 ? '✅ 是' : '❌ 否'}\n`);

// 失败请求详情
if (failed.length > 0) {
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`❌ 失败请求详情`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

  failed.forEach((result, index) => {
    console.log(`[${index + 1}] User ID: ${result.request.url.match(/\/users\/(\d+)/)?.[1]}`);
    console.log(`    错误: ${result.error?.message}`);
    console.log(`    状态码: ${result.error?.statusCode || 'N/A'}`);
    console.log(`    重试次数: ${result.metadata.retryCount}`);

    if (result.error?.retryHistory && result.error.retryHistory.length > 0) {
      console.log(`    重试历史:`);
      result.error.retryHistory.forEach(retry => {
        console.log(`       尝试${retry.attempt}: ${retry.error} (等待${retry.waitTime}ms)`);
      });
    }
    console.log();
  });
}

// 显示部分成功结果
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`📝 用户信息示例 (前5个)`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

successful.slice(0, 5).forEach((result, index) => {
  const user = result.response.data;
  console.log(`[${index + 1}] ${user.name} (@${user.username})`);
  console.log(`    📧 Email: ${user.email}`);
  console.log(`    🏢 Company: ${user.company?.name || 'N/A'}`);
  console.log(`    🌐 Website: ${user.website}`);
  console.log(`    📍 City: ${user.address?.city}`);
  console.log(`    ⏱️  请求耗时: ${result.metadata.duration}ms`);
  console.log();
});

// 性能时间线可视化
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`⏱️  速率限制时间线`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

// 将请求按秒分组
const requestsBySecond = new Map<number, number>();
results.forEach(result => {
  const timestamp = new Date(result.request.timestamp).getTime();
  const second = Math.floor((timestamp - startTime) / 1000);
  requestsBySecond.set(second, (requestsBySecond.get(second) || 0) + 1);
});

// 可视化每秒请求数
Array.from(requestsBySecond.entries()).sort((a, b) => a[0] - b[0]).forEach(([second, count]) => {
  const bar = '█'.repeat(count);
  console.log(`第${second.toString().padStart(2)}秒: ${bar} ${count} 请求`);
});

console.log(`\n✅ 速率限制自动处理成功,避免了API服务器过载!\n`);
```

**预期输出示例**:

```
🔄 开始批量获取 100 个用户信息...

⚙️  速率限制配置: 10 请求/秒

⏳ 执行批量请求...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 批量请求完成统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 成功: 98 / 100 (98.0%)
❌ 失败: 2
🔄 总重试次数: 5
⏱️  总耗时: 10.25秒
📈 平均耗时: 95ms/请求
⚡ 实际速率: 9.8 请求/秒
🎯 速率限制遵守: ✅ 是

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 失败请求详情
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] User ID: 45
    错误: 404 Not Found
    状态码: 404
    重试次数: 0

[2] User ID: 89
    错误: 500 Internal Server Error
    状态码: 500
    重试次数: 3
    重试历史:
       尝试1: 500 Internal Server Error (等待500ms)
       尝试2: 500 Internal Server Error (等待1000ms)
       尝试3: 500 Internal Server Error (等待2000ms)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 用户信息示例 (前5个)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] Leanne Graham (@Bret)
    📧 Email: Sincere@april.biz
    🏢 Company: Romaguera-Crona
    🌐 Website: hildegard.org
    📍 City: Gwenborough
    ⏱️  请求耗时: 87ms

[2] Ervin Howell (@Antonette)
    📧 Email: Shanna@melissa.tv
    🏢 Company: Deckow-Crist
    🌐 Website: anastasia.net
    📍 City: Wisokyburgh
    ⏱️  请求耗时: 92ms

[3] Clementine Bauch (@Samantha)
    📧 Email: Nathan@yesenia.net
    🏢 Company: Romaguera-Jacobson
    🌐 Website: ramiro.info
    📍 City: McKenziehaven
    ⏱️  请求耗时: 95ms

[4] Patricia Lebsack (@Karianne)
    📧 Email: Julianne.OConner@kory.org
    🏢 Company: Robel-Corkery
    🌐 Website: kale.biz
    📍 City: South Elvis
    ⏱️  请求耗时: 103ms

[5] Chelsey Dietrich (@Kamren)
    📧 Email: Lucio_Hettinger@annie.ca
    🏢 Company: Keebler LLC
    🌐 Website: demarco.info
    📍 City: Roscoeview
    ⏱️  请求耗时: 88ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  速率限制时间线
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

第 0秒: ██████████ 10 请求
第 1秒: ██████████ 10 请求
第 2秒: ██████████ 10 请求
第 3秒: ██████████ 10 请求
第 4秒: ██████████ 10 请求
第 5秒: ██████████ 10 请求
第 6秒: ██████████ 10 请求
第 7秒: ██████████ 10 请求
第 8秒: ██████████ 10 请求
第 9秒: ██████████ 10 请求

✅ 速率限制自动处理成功,避免了API服务器过载!
```

---

## Best Practices

### 1. 认证安全最佳实践

**永远不要硬编码API密钥**:

```typescript
// ❌ 错误: 硬编码密钥
const config = {
  auth: {
    type: 'apiKey',
    credentials: {
      apiKey: 'sk-1234567890abcdef'  // 危险!
    }
  }
};

// ✅ 正确: 使用环境变量
const config = {
  auth: {
    type: 'apiKey',
    credentials: {
      apiKey: process.env.API_KEY!
    }
  }
};
```

**实现OAuth2 Token刷新**:

```typescript
class TokenManager {
  private accessToken: string;
  private refreshToken: string;
  private expiresAt: number;

  async getValidToken(): Promise<string> {
    // 检查token是否即将过期 (提前5分钟刷新)
    if (Date.now() >= this.expiresAt - 300000) {
      await this.refreshAccessToken();
    }
    return this.accessToken;
  }

  async refreshAccessToken() {
    const refreshConfig: APIIntegratorInput = {
      baseUrl: 'https://oauth2.example.com',
      endpoint: '/token',
      method: 'POST',
      auth: { type: 'none', credentials: {} },
      request: {
        body: {
          grant_type: 'refresh_token',
          refresh_token: this.refreshToken,
          client_id: process.env.CLIENT_ID,
          client_secret: process.env.CLIENT_SECRET
        }
      }
    };

    const result = await apiIntegrator.execute(refreshConfig);

    if (!result.error) {
      this.accessToken = result.response.data.access_token;
      this.expiresAt = Date.now() + (result.response.data.expires_in * 1000);
      console.log('✅ Access token refreshed');
    }
  }
}
```

### 2. 错误处理策略

**区分可重试和不可重试错误**:

```typescript
function isRetryableError(error: APIIntegratorOutput['error']): boolean {
  if (!error) return false;

  // 4xx客户端错误通常不可重试 (除了429 Rate Limit)
  if (error.statusCode && error.statusCode >= 400 && error.statusCode < 500) {
    return error.statusCode === 429;  // 仅429 Too Many Requests可重试
  }

  // 5xx服务器错误可重试
  if (error.statusCode && error.statusCode >= 500) {
    return true;
  }

  // 网络错误可重试
  if (error.code === 'NETWORK_ERROR' || error.code === 'TIMEOUT') {
    return true;
  }

  return false;
}
```

**提供友好的错误消息**:

```typescript
function handleAPIError(error: APIIntegratorOutput['error']) {
  if (!error) return;

  const userFriendlyMessages: Record<string, string> = {
    'AUTH_FAILED': '认证失败,请检查API密钥是否正确',
    'RATE_LIMIT_EXCEEDED': 'API调用频率过高,请稍后再试',
    'TIMEOUT': '请求超时,服务器响应缓慢',
    'NETWORK_ERROR': '网络连接失败,请检查网络设置',
    '404': '请求的资源不存在',
    '500': '服务器内部错误,请联系管理员'
  };

  const message = userFriendlyMessages[error.code] ||
                  userFriendlyMessages[error.statusCode?.toString() || ''] ||
                  error.message;

  console.error(`❌ ${message}`);

  if (error.suggestedAction) {
    console.log(`💡 建议: ${error.suggestedAction}`);
  }
}
```

### 3. 性能优化技巧

**启用响应缓存**:

```typescript
// 对于GET请求,启用缓存显著提升性能
const cachedConfig: APIIntegratorInput = {
  baseUrl: 'https://api.example.com',
  endpoint: '/data',
  method: 'GET',
  auth: { /* ... */ },
  options: {
    cache: {
      enabled: true,
      ttl: 600,  // 10分钟
      keyStrategy: 'url-params',
      getOnly: true
    }
  }
};

// 第一次调用: 实际请求API (耗时500ms)
const result1 = await apiIntegrator.execute(cachedConfig);
console.log(`耗时: ${result1.metadata.duration}ms, 缓存: ${result1.metadata.cacheHit}`);
// 输出: 耗时: 500ms, 缓存: false

// 第二次调用: 命中缓存 (耗时<10ms)
const result2 = await apiIntegrator.execute(cachedConfig);
console.log(`耗时: ${result2.metadata.duration}ms, 缓存: ${result2.metadata.cacheHit}`);
// 输出: 耗时: 5ms, 缓存: true
```

**批量请求优化**:

```typescript
// 使用executeBatch代替循环调用
// ❌ 低效: 串行调用
const results = [];
for (const id of userIds) {
  const result = await apiIntegrator.execute({ ...config, endpoint: `/users/${id}` });
  results.push(result);
}
// 总耗时: 100 * 500ms = 50秒

// ✅ 高效: 并行批量调用 + 速率限制
const results = await apiIntegrator.executeBatch(
  userIds.map(id => ({ ...config, endpoint: `/users/${id}` }))
);
// 总耗时: (100 / 10 请求/秒) = 10秒
```

### 4. 监控与告警

**跟踪API性能指标**:

```typescript
class APIMonitor {
  private metrics: Array<{
    endpoint: string;
    duration: number;
    status: number;
    timestamp: Date;
  }> = [];

  recordRequest(result: APIIntegratorOutput) {
    this.metrics.push({
      endpoint: new URL(result.request.url).pathname,
      duration: result.metadata.duration,
      status: result.response.status,
      timestamp: new Date(result.request.timestamp)
    });
  }

  getStats(endpoint: string) {
    const endpointMetrics = this.metrics.filter(m => m.endpoint === endpoint);

    return {
      totalRequests: endpointMetrics.length,
      avgDuration: endpointMetrics.reduce((sum, m) => sum + m.duration, 0) / endpointMetrics.length,
      p95Duration: this.percentile(endpointMetrics.map(m => m.duration), 0.95),
      p99Duration: this.percentile(endpointMetrics.map(m => m.duration), 0.99),
      errorRate: endpointMetrics.filter(m => m.status >= 400).length / endpointMetrics.length
    };
  }

  private percentile(values: number[], p: number): number {
    const sorted = values.sort((a, b) => a - b);
    const index = Math.ceil(sorted.length * p) - 1;
    return sorted[index];
  }
}

const monitor = new APIMonitor();

// 记录每次API调用
const result = await apiIntegrator.execute(config);
monitor.recordRequest(result);

// 定期分析性能
const stats = monitor.getStats('/users');
console.log(`/users端点性能:`);
console.log(`  平均响应时间: ${stats.avgDuration.toFixed(0)}ms`);
console.log(`  P95响应时间: ${stats.p95Duration.toFixed(0)}ms`);
console.log(`  P99响应时间: ${stats.p99Duration.toFixed(0)}ms`);
console.log(`  错误率: ${(stats.errorRate * 100).toFixed(2)}%`);
```

**设置速率限制告警**:

```typescript
function checkRateLimitAlert(result: APIIntegratorOutput) {
  if (!result.metadata.rateLimit) return;

  const { usage, remaining, limit } = result.metadata.rateLimit;

  // 使用率超过80%时告警
  if (usage > 80) {
    console.warn(`⚠️  速率限制告警: API配额使用率 ${usage.toFixed(0)}%`);
    console.warn(`   剩余配额: ${remaining} / ${limit}`);

    // 发送通知(Slack, Email等)
    sendAlert({
      severity: usage > 95 ? 'critical' : 'warning',
      message: `API rate limit at ${usage.toFixed(0)}%`,
      remaining,
      limit
    });
  }
}
```

### 5. OpenAPI规范最佳实践

**从OpenAPI自动生成类型安全的客户端**:

```typescript
// 从OpenAPI规范自动生成API客户端
const petStoreClient = await apiIntegrator.fromOpenAPI({
  spec: 'https://petstore3.swagger.io/api/v3/openapi.json',
  auth: {
    type: 'apiKey',
    credentials: {
      apiKey: process.env.PETSTORE_API_KEY!
    }
  }
});

// 自动类型推导
const result = await petStoreClient.call('addPet', {
  body: {
    name: 'Fluffy',
    category: { id: 1, name: 'Cats' },
    photoUrls: ['https://example.com/fluffy.jpg'],
    status: 'available'
  }
});

// TypeScript类型检查
// result.response.data的类型自动推导为Pet接口
const petId = result.response.data.id;  // ✅ 类型安全
```

## Related Skills

- **web-search**: 搜索API文档和使用示例
- **code-generator**: 基于API响应生成客户端代码
- **security-audit**: 扫描API集成中的安全问题
- **document-processor**: 处理API返回的文档数据
- **test-automation**: 为API集成生成自动化测试

---

## Changelog

### v2.0.0 (2024-12-10)
- ✨ 重新设计Skill架构,从54个Skills精简为32个
- ✨ 新增OpenAPI/Swagger规范自动解析功能
- ✨ 增强速率限制处理,支持多种策略(fixed-window, sliding-window, token-bucket)
- ✨ 添加智能缓存机制,支持自定义缓存键策略
- ✨ 改进OAuth2流程,自动处理token刷新
- ✨ 新增批量请求executeBatch方法
- ✨ 增加详细的性能指标(DNS, TCP, TLS, TTFB等)
- 🔧 优化错误处理,提供建议操作
- 🔧 增强分页支持,新增link-header策略
- 📚 完善文档,添加4个详细使用示例和最佳实践

---

**注意事项**:
1. API密钥等敏感信息必须使用环境变量,禁止硬编码
2. 遵守第三方API的速率限制,避免被封禁
3. 对于高频调用的GET请求,建议启用缓存
4. 实现完善的错误处理和监控告警机制
5. 定期审查API性能指标,优化慢请求
