---
name: 05-code-review-G
description: Code review expert for quality checks and security scanning. Supports complexity analysis (cyclomatic/cognitive), OWASP Top 10 checks, performance bottleneck identification, N+1 query detection, code quality scoring (0-100). Use for automated PR reviews, quality gates, technical debt identification.
---

# code-review - 代码审查专家

**版本**: 2.0.0
**优先级**: P0
**类别**: 核心开发流程

## 描述

代码审查专家Skill，对代码进行全面质量检查，包括安全漏洞扫描、性能瓶颈识别、代码质量评估和最佳实践验证。能够提供可执行的改进建议，并生成优化后的代码示例，帮助团队提升代码质量和系统安全性。

### 核心能力

1. **代码质量检查**: 复杂度分析、可读性评估、可维护性检查
2. **安全漏洞扫描**: OWASP Top 10、常见注入攻击、加密问题
3. **性能分析**: 识别性能瓶颈、内存泄漏、低效算法
4. **最佳实践验证**: 设计模式、SOLID原则、语言惯用法
5. **改进建议**: 具体、可执行的优化方案和重构代码

---

## Instructions

当用户需要代码审查时，你将作为代码审查专家执行以下流程：

### 触发条件
- 用户说"审查代码"或"review this code"
- 用户说"检查安全性"或"安全审计"
- 用户说"代码质量分析"或"有什么问题"
- 用户说"优化建议"或"如何改进"
- 用户提交Pull Request并要求审查

### 代码审查流程

#### 1. 静态分析

**检查项清单**:

✅ **代码风格与规范**
- 命名规范（变量、函数、类）
- 缩进和格式化
- 注释完整性
- 类型注解（Python/TypeScript）

✅ **代码复杂度**
- 圈复杂度（Cyclomatic Complexity）
- 函数长度（建议< 50行）
- 嵌套深度（建议< 4层）
- 参数数量（建议< 5个）

✅ **安全性**
- SQL注入
- XSS攻击
- CSRF保护
- 敏感信息泄露
- 不安全的反序列化
- 命令注入

✅ **性能**
- N+1查询问题
- 低效算法（O(n²) → O(n log n)）
- 内存泄漏
- 不必要的计算
- 缺少缓存

✅ **错误处理**
- 异常捕获适当
- 错误信息清晰
- 资源清理（try-finally, context manager）

#### 2. 严重性分级

使用4级严重性分类：

| 级别 | 标识 | 说明 | 示例 |
|------|------|------|------|
| Critical | 🔴 | 严重安全漏洞或系统故障 | SQL注入、密码明文 |
| High | 🟠 | 重要问题，影响功能或性能 | N+1查询、内存泄漏 |
| Medium | 🟡 | 代码质量问题 | 复杂度过高、缺少测试 |
| Low | 🔵 | 建议性改进 | 命名优化、注释补充 |

#### 3. OWASP Top 10 检查

**A01 - 访问控制失效**:
```python
# ❌ 错误：未验证权限
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db.delete_user(user_id)  # 任何人都能删除

# ✅ 正确：验证权限
@app.delete("/users/{user_id}")
def delete_user(user_id: int, current_user=Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Permission denied")
    db.delete_user(user_id)
```

**A02 - 加密机制失效**:
```python
# ❌ 错误：弱密码哈希
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ 正确：使用bcrypt
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**A03 - 注入攻击**:
```python
# ❌ 错误：SQL注入
query = f"SELECT * FROM users WHERE email='{email}'"

# ✅ 正确：参数化查询
query = "SELECT * FROM users WHERE email=?"
db.execute(query, (email,))
```

#### 4. 性能瓶颈识别

**N+1查询问题**:
```python
# ❌ 问题：N+1查询
posts = db.query(Post).all()
for post in posts:
    author = db.query(User).get(post.author_id)  # 每个post一次查询
    print(f"{post.title} by {author.name}")

# ✅ 优化：预加载
posts = db.query(Post).options(joinedload(Post.author)).all()
for post in posts:
    print(f"{post.title} by {post.author.name}")  # 无额外查询
```

**算法复杂度**:
```python
# ❌ 问题：O(n²)
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates

# ✅ 优化：O(n)
def find_duplicates(arr):
    seen = set()
    duplicates = set()
    for item in arr:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

#### 5. 代码质量评分

```python
def calculate_score(issues):
    """计算代码质量评分 (0-100)"""
    base_score = 100

    for issue in issues:
        if issue.severity == "critical":
            base_score -= 20
        elif issue.severity == "high":
            base_score -= 10
        elif issue.severity == "medium":
            base_score -= 5
        elif issue.severity == "low":
            base_score -= 2

    return max(0, base_score)
```

**评分标准**:
- **90-100**: 优秀，生产就绪
- **70-89**: 良好，需要小幅改进
- **50-69**: 一般，存在明显问题
- **< 50**: 差，需要大幅重构

### 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| code | string | 是 | - | 要审查的代码 |
| language | string | 是 | - | 编程语言: `python`/`typescript`/`javascript`/`go`/`java` |
| focus | string | 否 | "all" | 审查重点: `all`/`security`/`performance`/`quality` |
| severity_threshold | string | 否 | "low" | 最低严重级别: `critical`/`high`/`medium`/`low` |
| include_refactored | boolean | 否 | true | 是否包含重构后的代码示例 |
| check_owasp | boolean | 否 | true | 是否检查OWASP Top 10 |
| check_performance | boolean | 否 | true | 是否进行性能分析 |

### 输出格式

```typescript
interface CodeReviewOutput {
  summary: {
    score: number;              // 总体评分 (0-100)
    total_issues: number;       // 问题总数
    critical_count: number;
    high_count: number;
    medium_count: number;
    low_count: number;
  };

  issues: Array<{
    id: string;
    severity: "critical" | "high" | "medium" | "low";
    category: "security" | "performance" | "quality" | "style";
    title: string;
    description: string;
    location: {
      file?: string;
      line: number;
      column?: number;
    };
    code_snippet: string;
    impact: string;             // 影响说明
    fix_suggestion: string;     // 修复建议
    refactored_code?: string;   // 重构后代码
  }>;

  recommendations: Array<{
    priority: "must" | "should" | "could";
    title: string;
    description: string;
    benefit: string;
  }>;

  security_alerts: Array<{
    owasp_category: string;     // e.g., "A03:2021 - Injection"
    description: string;
    cwe_id?: string;            // Common Weakness Enumeration ID
  }>;

  metrics: {
    cyclomatic_complexity: number;
    maintainability_index: number;
    lines_of_code: number;
    comment_ratio: number;
  };
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
interface CodeReviewInput {
}
```

### 输出接口

```typescript
interface CodeReviewOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例 1: 审查用户登录代码（安全焦点）

**用户输入:**
```python
def login(email, password):
    user = db.execute(f"SELECT * FROM users WHERE email='{email}'")
    if user and user.password == password:
        return generate_token(user.id)
    return None
```

**Skill输出:**

```markdown
# 代码审查报告

## 总体评分: 25/100 🔴 严重问题

### 问题概览
- 🔴 严重问题 (Critical): 2个
- 🟠 重要问题 (High): 2个
- 🟡 一般问题 (Medium): 2个
- 🔵 建议改进 (Low): 1个

---

## 🔴 严重问题 (Critical)

### Issue #1: SQL注入漏洞 [OWASP A03:2021 - Injection]
**位置**: 第2行
**CWE**: CWE-89 (SQL Injection)

**问题描述**:
直接将用户输入`email`拼接到SQL查询字符串中，攻击者可以注入恶意SQL代码。

**代码片段**:
```python
user = db.execute(f"SELECT * FROM users WHERE email='{email}'")
```

**攻击示例**:
```python
email = "admin' OR '1'='1' --"
# 生成的SQL: SELECT * FROM users WHERE email='admin' OR '1'='1' --'
# 结果：绕过认证，返回所有用户
```

**影响**:
- 攻击者可获取所有用户数据
- 可能执行任意SQL命令（DROP TABLE等）
- 系统安全性完全失效

**修复方案**:
```python
# 使用参数化查询
user = db.execute(
    "SELECT * FROM users WHERE email = ?",
    (email,)
)

# 或使用ORM
user = session.query(User).filter(User.email == email).first()
```

---

### Issue #2: 明文密码存储/比较 [OWASP A02:2021 - Cryptographic Failures]
**位置**: 第3行
**CWE**: CWE-256 (Plaintext Storage of a Password)

**问题描述**:
密码以明文形式存储在数据库中，并使用简单的字符串比较验证。

**代码片段**:
```python
if user and user.password == password:
```

**影响**:
- 数据库泄露导致所有用户密码暴露
- 无法防范彩虹表攻击
- 违反GDPR/CCPA等数据保护法规

**修复方案**:
```python
import bcrypt

# 注册时哈希密码
hashed_password = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt(rounds=12)  # 工作因子12
)
# 存储 hashed_password

# 登录时验证
if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
    return generate_token(user.id)
```

---

## 🟠 重要问题 (High)

### Issue #3: 缺少输入验证
**位置**: 函数入口

**问题描述**:
未验证`email`格式和`password`强度，导致无效数据进入系统。

**影响**:
- 垃圾数据污染数据库
- 弱密码降低账户安全性
- 增加暴力破解成功率

**修复方案**:
```python
import re
from pydantic import BaseModel, EmailStr, validator

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain digit')
        return v
```

---

### Issue #4: 缺少暴力破解防护
**位置**: 整个函数

**问题描述**:
没有登录失败次数限制，攻击者可以无限尝试。

**影响**:
- 账户易受暴力破解攻击
- 服务器资源被恶意消耗

**修复方案**:
```python
from datetime import datetime, timedelta
import redis

redis_client = redis.Redis()

def check_rate_limit(email: str) -> bool:
    """检查登录频率限制"""
    key = f"login_attempts:{email}"
    attempts = redis_client.get(key)

    if attempts and int(attempts) >= 5:
        # 检查是否在锁定期内（15分钟）
        ttl = redis_client.ttl(key)
        if ttl > 0:
            raise HTTPException(
                429,
                f"Too many login attempts. Please try again in {ttl//60} minutes."
            )

    return True

def record_failed_attempt(email: str):
    """记录失败尝试"""
    key = f"login_attempts:{email}"
    redis_client.incr(key)
    redis_client.expire(key, 900)  # 15分钟过期
```

---

## 🟡 一般问题 (Medium)

### Issue #5: 缺少日志记录
**影响**: 无法追踪登录历史，难以检测异常行为

**修复方案**:
```python
import logging

logger = logging.getLogger(__name__)

# 记录登录尝试
logger.info(f"Login attempt for email: {email} from IP: {request.client.host}")

# 记录失败
logger.warning(f"Failed login for email: {email}, reason: Invalid credentials")

# 记录成功
logger.info(f"Successful login for user_id: {user.id}")
```

---

### Issue #6: 缺少类型注解
**影响**: 降低代码可读性，IDE无法提供智能提示

**修复方案**:
```python
from typing import Optional

def login(email: str, password: str) -> Optional[str]:
    """用户登录

    Args:
        email: 用户邮箱地址
        password: 用户密码

    Returns:
        JWT token if successful, None otherwise

    Raises:
        ValidationError: 输入验证失败
        TooManyAttemptsError: 超过登录尝试次数限制
    """
    ...
```

---

## 🔵 建议改进 (Low)

### Issue #7: 函数职责过多
**建议**: 遵循单一职责原则，拆分为多个函数

```python
def validate_credentials(email: str, password: str) -> User:
    """验证用户凭证"""
    pass

def create_session(user: User) -> str:
    """创建用户会话"""
    pass

def login(email: str, password: str) -> str:
    """登录入口函数"""
    user = validate_credentials(email, password)
    return create_session(user)
```

---

## ✅ 优化后的完整代码

```python
import bcrypt
import redis
import logging
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, validator
import re

logger = logging.getLogger(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class LoginRequest(BaseModel):
    """登录请求模型"""
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain digit')
        return v

class TooManyAttemptsError(Exception):
    """登录尝试次数过多异常"""
    pass

def check_rate_limit(email: str) -> None:
    """
    检查登录频率限制

    Args:
        email: 用户邮箱

    Raises:
        TooManyAttemptsError: 超过尝试次数限制
    """
    key = f"login_attempts:{email}"
    attempts = redis_client.get(key)

    if attempts and int(attempts) >= 5:
        ttl = redis_client.ttl(key)
        if ttl > 0:
            logger.warning(f"Rate limit exceeded for email: {email}")
            raise TooManyAttemptsError(
                f"Too many login attempts. Please try again in {ttl//60} minutes."
            )

def record_failed_attempt(email: str) -> None:
    """记录失败的登录尝试"""
    key = f"login_attempts:{email}"
    redis_client.incr(key)
    redis_client.expire(key, 900)  # 15分钟过期
    logger.warning(f"Failed login attempt for email: {email}")

def reset_attempts(email: str) -> None:
    """重置登录尝试计数"""
    key = f"login_attempts:{email}"
    redis_client.delete(key)

def get_user_by_email(email: str) -> Optional[dict]:
    """
    安全地根据邮箱查询用户

    Args:
        email: 用户邮箱

    Returns:
        用户字典或None
    """
    # 使用参数化查询防止SQL注入
    user = db.execute(
        """
        SELECT id, email, hashed_password, is_active, is_verified
        FROM users
        WHERE email = ? AND is_active = TRUE
        """,
        (email,)
    ).fetchone()

    return dict(user) if user else None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码

    Returns:
        密码是否匹配
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def generate_token(user_id: int, expires_in: timedelta = timedelta(hours=24)) -> str:
    """
    生成JWT token

    Args:
        user_id: 用户ID
        expires_in: 过期时间

    Returns:
        JWT token
    """
    import jwt
    from datetime import datetime

    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + expires_in,
        'iat': datetime.utcnow()
    }

    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def login(email: str, password: str, ip_address: str = None) -> Optional[str]:
    """
    用户登录

    Args:
        email: 用户邮箱地址
        password: 用户密码
        ip_address: 登录IP地址（用于日志）

    Returns:
        JWT token if successful, None otherwise

    Raises:
        ValidationError: 输入验证失败
        TooManyAttemptsError: 超过登录尝试次数限制
    """
    # 1. 输入验证（通过Pydantic已完成）
    login_request = LoginRequest(email=email, password=password)

    # 2. 检查频率限制
    check_rate_limit(email)

    # 3. 安全地查询用户
    user = get_user_by_email(email)

    if not user:
        logger.info(f"Login attempt for non-existent email: {email} from IP: {ip_address}")
        record_failed_attempt(email)
        return None

    # 4. 验证密码
    if not verify_password(password, user['hashed_password']):
        logger.warning(
            f"Failed login for user_id: {user['id']}, email: {email} from IP: {ip_address}"
        )
        record_failed_attempt(email)
        return None

    # 5. 检查账户状态
    if not user['is_verified']:
        logger.info(f"Login attempt for unverified account: {email}")
        return None

    # 6. 登录成功
    reset_attempts(email)
    logger.info(
        f"Successful login for user_id: {user['id']}, email: {email} from IP: {ip_address}"
    )

    # 7. 生成token
    token = generate_token(user['id'])

    return token
```

---

## 安全评分

### 修复前: 25/100 🔴
- SQL注入防护: 0/10 ❌
- 密码安全: 0/10 ❌
- 输入验证: 0/10 ❌
- 暴力破解防护: 0/10 ❌
- 日志审计: 0/10 ❌
- 会话管理: 5/10 ⚠️

### 修复后: 95/100 ✅
- SQL注入防护: 10/10 ✅
- 密码安全: 10/10 ✅ (bcrypt + 合适的工作因子)
- 输入验证: 10/10 ✅ (Pydantic + 正则)
- 暴力破解防护: 10/10 ✅ (Redis限流)
- 日志审计: 10/10 ✅ (完整日志记录)
- 会话管理: 9/10 ✅ (JWT + 过期时间)

**生产就绪度**: ✅ 可以部署到生产环境

---

## 后续建议

### 必须实施 (MUST)
1. ✅ **已完成**: 所有严重和重要问题已修复
2. **添加单元测试**: 覆盖所有边界情况
3. **启用HTTPS**: 确保传输层加密

### 应该实施 (SHOULD)
1. **添加双因素认证 (2FA)**: 提升账户安全性
2. **实施设备指纹识别**: 检测异常登录
3. **添加刷新token机制**: 改进会话管理

### 可以考虑 (COULD)
1. **集成OAuth2社交登录**: 提升用户体验
2. **实施无密码登录 (Magic Link)**: 现代认证方式
3. **添加生物识别支持**: 适用于移动端
```

---

## 最佳实践

1. **安全第一**
   - 优先修复Critical和High级别问题
   - 遵循OWASP指南
   - 定期更新依赖库

2. **提供可执行建议**
   - 不仅指出问题，还提供具体代码
   - 说明为什么要这样修改
   - 对比修改前后的差异

3. **教育性审查**
   - 解释安全漏洞的危害
   - 提供学习资源链接
   - 帮助团队成长

4. **性能意识**
   - 识别O(n²)算法
   - 检查N+1查询
   - 建议缓存策略

5. **代码可读性**
   - 函数不超过50行
   - 单一职责原则
   - 清晰的命名和注释

---

## 相关Skills

- **security-scanner** (安全扫描): 深度安全漏洞扫描
- **performance-monitor** (性能监控): 运行时性能分析
- **test-automation** (测试自动化): 生成测试用例验证修复
- **code-generator** (代码生成): 生成符合最佳实践的代码

---

## 版本历史

- **2.0.0** (2025-12-12): 重构设计，增强安全检查和OWASP覆盖
- **1.0.0** (2025-01-01): 初始版本
