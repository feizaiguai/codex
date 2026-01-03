# API Integrator Skill - API集成器

**版本**: 2.0.0
**类型**: 外部集成
**质量等级**: A+

## 📋 功能概述

智能处理第三方API集成,自动处理认证、重试和速率限制。

### 核心能力

1. **多认证方式** - 支持OAuth2/JWT/API Key/Basic Auth四种认证
2. **速率限制管理** - Token Bucket算法自动遵守API限制
3. **指数退避重试** - 智能重试策略,自动处理临时失败
4. **自动分页处理** - 支持Offset/Cursor/Page三种分页方式
5. **OpenAPI解析** - 自动解析Swagger/OpenAPI规范

## 🚀 使用方法

### Slash Command
```bash
/api-integrate [API配置]
```

### 自然语言调用
```
调用GitHub API获取仓库信息
集成Stripe支付API
从Notion导入数据
```

## 📖 使用示例

### 示例:调用GitHub API
**输入**:
```
/api-integrate --base-url=https://api.github.com --endpoint=/repos/facebook/react --auth=bearer
```

**输出**:
- ✅ 请求成功 (200 OK)
- ✅ 响应时间: 234ms
- ✅ 速率限制: 4998/5000 (剩余)
- ✅ 数据解析: JSON (15KB)
- 📊 仓库信息:
  - Stars: 228,123
  - Forks: 46,789
  - Issues: 1,234

## 🔐 支持的认证方式

### 1. API Key认证
```yaml
auth:
  type: apiKey
  location: header  # 或 query
  key: X-API-Key
  value: your-api-key
```

### 2. OAuth2认证
```yaml
auth:
  type: oauth2
  accessToken: your-access-token
  refreshToken: your-refresh-token
  tokenUrl: https://api.example.com/oauth/token
```

### 3. JWT认证
```yaml
auth:
  type: jwt
  token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Basic认证
```yaml
auth:
  type: basic
  username: user
  password: pass
```

## 🔄 重试策略

### 指数退避算法
```
初始延迟: 1秒
第1次重试: 等待 1秒
第2次重试: 等待 2秒 (1 * 2)
第3次重试: 等待 4秒 (2 * 2)
第4次重试: 等待 8秒 (4 * 2)
最大重试: 5次
```

### 可重试的错误
- ✅ 5xx服务器错误
- ✅ 网络超时
- ✅ 连接错误
- ✅ DNS解析失败
- ❌ 4xx客户端错误 (不重试)

## 📄 分页处理

### Offset分页
```
GET /api/users?offset=0&limit=100
GET /api/users?offset=100&limit=100
```

### Cursor分页
```
GET /api/users?cursor=abc123
GET /api/users?cursor=def456
```

### Page分页
```
GET /api/users?page=1&per_page=100
GET /api/users?page=2&per_page=100
```

## ⚡ 速率限制管理

### Token Bucket算法
```typescript
// 每分钟100请求
rateLimit: {
  maxRequests: 100,
  perSeconds: 60,
  strategy: 'token-bucket'
}

// 自动等待示例:
请求1-100: 立即发送
请求101: 等待至下一分钟
```

### 速率限制响应
```json
{
  "rateLimit": {
    "limit": 5000,
    "remaining": 4998,
    "reset": 1640995200,
    "resetDate": "2025-01-01T00:00:00Z"
  }
}
```

## 🌐 OpenAPI集成

### 自动发现端点
```yaml
# 提供OpenAPI规范URL
apiSpec: https://petstore3.swagger.io/api/v3/openapi.json

# 自动提取:
- 所有可用端点
- 参数类型和验证
- 认证方式
- 响应格式
```

## 📊 实际案例

### 案例1: GitHub API集成
```typescript
// 获取仓库PR列表
{
  baseUrl: 'https://api.github.com',
  endpoint: '/repos/{owner}/{repo}/pulls',
  pathParams: { owner: 'facebook', repo: 'react' },
  auth: { type: 'bearer', token: 'ghp_xxxx' },
  pagination: { type: 'page', maxPages: 5 }
}

// 结果: 自动获取5页PR,合并为单个数组
```

### 案例2: Stripe支付API
```typescript
// 创建支付意图
{
  baseUrl: 'https://api.stripe.com',
  endpoint: '/v1/payment_intents',
  method: 'POST',
  auth: { type: 'bearer', token: 'sk_test_xxxx' },
  body: {
    amount: 2000,
    currency: 'usd',
    payment_method_types: ['card']
  },
  retry: { maxRetries: 3, strategy: 'exponential' }
}
```

### 案例3: 批量数据同步
```typescript
// 从Notion导出数据
{
  baseUrl: 'https://api.notion.com',
  endpoint: '/v1/databases/{database_id}/query',
  auth: {
    type: 'bearer',
    token: 'secret_xxxx'
  },
  pagination: {
    type: 'cursor',
    maxPages: 'all' // 获取所有页
  },
  cache: {
    enabled: true,
    ttl: 300 // 缓存5分钟
  }
}
```

## 🛠️ 最佳实践

1. **使用环境变量**: 不要硬编码API密钥
2. **启用重试**: 处理临时网络问题
3. **配置超时**: 防止请求hang住
4. **监控速率限制**: 避免被API封禁
5. **缓存响应**: 减少API调用次数

## 🔗 与其他 Skills 配合

- `log-analyzer`: 分析API调用日志
- `performance-optimizer`: 优化API调用性能
- `security-audit`: 检查API密钥泄露

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
