---
name: 10-quality-gate-G
description: Quality gate expert for multi-dimensional quality checks. Supports test coverage checks (80% threshold), code complexity analysis (cyclomatic complexity < 10), security auditing, AI code smell detection, trend analysis (quality trend charts). Use for CI/CD pipeline integration, PR merge gates, code quality monitoring.
---

# quality-gate - 质量门控专家

**版本**: 2.0.0
**优先级**: P1
**类别**: 质量与安全

---

## 描述

quality-gate是AI驱动的质量门控专家,通过多维度智能分析确保代码满足生产环境标准。执行测试覆盖率、代码复杂度、安全性、性能等全面检查,识别代码异味和潜在问题,追踪质量指标变化趋势。支持自定义门槛配置,与CI/CD无缝集成,自动阻止不合格代码合并,保障代码质量底线。

---

## 核心能力

1. **多维度质量检查**: 测试覆盖率、代码复杂度、安全性、性能、可维护性、文档完整度
2. **AI智能分析**: 识别代码异味(过长函数、重复代码、复杂条件)和潜在问题
3. **趋势分析**: 追踪质量指标历史变化,预警质量下降
4. **自定义门槛**: 支持strict/balanced/lenient模式,根据项目灵活配置准入标准
5. **集成CI/CD**: 自动阻止不合格代码合并,生成详细修复建议

---

## Instructions

### 质量评分体系

#### 1. 测试覆盖率检查

```python
def check_test_coverage(project_path):
    """
    执行测试覆盖率检查

    标准:
    - 整体覆盖率: ≥80% (AA级), ≥90% (AAA级)
    - 关键模块: ≥90% (核心业务逻辑)
    - 新增代码: ≥85% (增量覆盖率)

    检查项:
    - 行覆盖率 (Line Coverage)
    - 分支覆盖率 (Branch Coverage)
    - 函数覆盖率 (Function Coverage)
    """
    import coverage

    cov = coverage.Coverage()
    cov.start()

    # 运行测试
    pytest.main([project_path, '--cov'])

    cov.stop()
    cov.save()

    # 生成报告
    report = cov.report()

    missing_coverage = []
    for filename, data in cov.get_data().measured_files():
        coverage_pct = data.line_coverage()
        if coverage_pct < 80:
            missing_coverage.append({
                'file': filename,
                'coverage': coverage_pct,
                'missing_lines': data.missing_lines()
            })

    return {
        'overall_coverage': report,
        'missing_coverage': missing_coverage,
        'status': 'pass' if report >= 80 else 'fail'
    }
```

#### 2. 代码复杂度分析

```python
def analyze_code_complexity(code_path):
    """
    分析代码复杂度

    标准:
    - 圈复杂度 (Cyclomatic Complexity): ≤15
    - 认知复杂度 (Cognitive Complexity): ≤10
    - 函数行数: ≤50
    - 类行数: ≤300
    """
    import radon.complexity as radon_cc
    from radon.raw import analyze

    results = []

    for file_path in glob.glob(f"{code_path}/**/*.py", recursive=True):
        with open(file_path) as f:
            code = f.read()

        # 圈复杂度
        cc_results = radon_cc.cc_visit(code)

        for item in cc_results:
            if item.complexity > 15:
                results.append({
                    'type': 'high_complexity',
                    'file': file_path,
                    'function': item.name,
                    'complexity': item.complexity,
                    'lineno': item.lineno,
                    'severity': 'critical' if item.complexity > 20 else 'warning'
                })

        # 代码行数
        metrics = analyze(code)
        if metrics.loc > 300:
            results.append({
                'type': 'large_file',
                'file': file_path,
                'lines': metrics.loc,
                'severity': 'warning'
            })

    return {
        'complexity_issues': results,
        'status': 'fail' if any(r['severity'] == 'critical' for r in results) else 'warning'
    }
```

#### 3. 安全性检查

```python
def security_audit(code_path):
    """
    安全性审计

    检查项:
    - SQL注入风险
    - XSS漏洞
    - 硬编码密钥
    - 不安全的依赖
    - OWASP Top 10
    """
    import bandit
    import safety

    # Bandit静态分析
    bandit_results = bandit.run_bandit(code_path)

    # Safety依赖检查
    safety_results = safety.check()

    critical_issues = []
    high_issues = []

    for issue in bandit_results:
        if issue.severity == 'HIGH':
            high_issues.append({
                'type': 'security',
                'severity': 'high',
                'file': issue.fname,
                'line': issue.lineno,
                'issue': issue.text,
                'cwe': issue.cwe
            })
        elif issue.severity == 'CRITICAL':
            critical_issues.append({
                'type': 'security',
                'severity': 'critical',
                'file': issue.fname,
                'line': issue.lineno,
                'issue': issue.text,
                'cwe': issue.cwe
            })

    for vuln in safety_results:
        critical_issues.append({
            'type': 'dependency_vulnerability',
            'severity': 'critical' if vuln.cvss >= 7.0 else 'high',
            'package': vuln.package,
            'version': vuln.version,
            'vulnerability': vuln.vulnerability,
            'fixed_in': vuln.fixed_in
        })

    return {
        'critical_issues': critical_issues,
        'high_issues': high_issues,
        'status': 'fail' if critical_issues else 'pass'
    }
```

#### 4. AI代码异味检测

```python
def detect_code_smells(code):
    """
    AI驱动的代码异味检测

    检测模式:
    1. 过长函数 (Long Method)
    2. 重复代码 (Duplicated Code)
    3. 复杂条件 (Complex Conditional)
    4. 数据泥团 (Data Clumps)
    5. 大类 (Large Class)
    """
    smells = []

    # 1. 过长函数检测
    functions = extract_functions(code)
    for func in functions:
        if func.line_count > 50:
            smells.append({
                'type': 'long_method',
                'name': func.name,
                'lines': func.line_count,
                'recommendation': 'Split into smaller functions with single responsibility',
                'refactoring': generate_refactoring_suggestion(func)
            })

    # 2. 重复代码检测
    duplicates = find_duplicate_code_blocks(code, threshold=0.85)
    for dup in duplicates:
        smells.append({
            'type': 'duplicated_code',
            'locations': dup.locations,
            'similarity': dup.similarity,
            'recommendation': 'Extract common logic into a shared function',
            'refactoring': generate_extract_function_suggestion(dup)
        })

    # 3. 复杂条件检测
    conditionals = extract_conditionals(code)
    for cond in conditionals:
        if cond.nesting_level > 3:
            smells.append({
                'type': 'complex_conditional',
                'location': cond.location,
                'nesting_level': cond.nesting_level,
                'recommendation': 'Use early returns or strategy pattern',
                'refactoring': generate_simplification_suggestion(cond)
            })

    return smells
```

#### 5. 性能影响评估

```python
def assess_performance_impact(code_changes):
    """
    评估代码变更的性能影响

    检查项:
    - 算法复杂度变化
    - 数据库查询数量
    - 网络请求数量
    - 内存分配模式
    """
    performance_score = 100
    issues = []

    # 检测N+1查询问题
    db_queries = detect_database_queries(code_changes)
    for query in db_queries:
        if query.in_loop:
            performance_score -= 10
            issues.append({
                'type': 'n_plus_1_query',
                'location': query.location,
                'impact': 'High database load under scale',
                'fix': 'Use joinedload() or prefetch_related()'
            })

    # 检测算法复杂度
    algorithms = analyze_algorithms(code_changes)
    for algo in algorithms:
        if algo.complexity == 'O(n^2)' or algo.complexity == 'O(n^3)':
            performance_score -= 15
            issues.append({
                'type': 'inefficient_algorithm',
                'location': algo.location,
                'current_complexity': algo.complexity,
                'impact': 'Performance degrades with data size',
                'suggestion': 'Optimize to O(n log n) or O(n)'
            })

    # 检测同步阻塞操作
    sync_ops = detect_sync_blocking_operations(code_changes)
    for op in sync_ops:
        if op.type in ['http_request', 'file_io', 'external_api']:
            performance_score -= 5
            issues.append({
                'type': 'sync_blocking_operation',
                'location': op.location,
                'operation': op.type,
                'suggestion': 'Use async/await or background tasks'
            })

    return {
        'performance_score': max(0, performance_score),
        'issues': issues,
        'status': 'pass' if performance_score >= 90 else 'warning'
    }
```

### 质量门控配置

#### Strict Mode (严格模式)

```yaml
quality_gates:
  test_coverage:
    threshold: 90%
    blocking: true      # 不达标则阻塞合并

  code_complexity:
    max_complexity: 10
    threshold_score: 90
    blocking: true

  security_issues:
    critical: 0         # 不允许任何Critical问题
    high: 0            # 不允许任何High问题
    blocking: true

  performance_regression:
    threshold: -5%      # 不允许性能下降超过5%
    blocking: true

  documentation:
    threshold: 80%
    blocking: true

  duplication:
    max_percentage: 3%
    blocking: true

  code_smells:
    max_count: 5
    blocking: false     # 警告但不阻塞
```

#### Balanced Mode (平衡模式 - 默认)

```yaml
quality_gates:
  test_coverage:
    threshold: 80%
    blocking: false     # 警告但不阻塞

  code_complexity:
    max_complexity: 15
    threshold_score: 80
    blocking: false

  security_issues:
    critical: 0         # Critical必须修复
    high: 2            # 最多2个High问题
    blocking: true      # Critical阻塞,High警告

  performance_regression:
    threshold: -10%
    blocking: true

  documentation:
    threshold: 70%
    blocking: false

  duplication:
    max_percentage: 5%
    blocking: false
```

#### Lenient Mode (宽松模式)

```yaml
quality_gates:
  test_coverage:
    threshold: 60%
    blocking: false

  code_complexity:
    max_complexity: 20
    threshold_score: 70
    blocking: false

  security_issues:
    critical: 1         # 允许1个Critical
    high: 5
    blocking: false

  performance_regression:
    threshold: -15%
    blocking: false

  documentation:
    threshold: 50%
    blocking: false

  duplication:
    max_percentage: 10%
    blocking: false
```

---

## 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| code_changes | object | 是 | - | 代码变更内容(diff, files) |
| quality_profile | string | 否 | balanced | 质量档案: strict/balanced/lenient |
| custom_thresholds | object | 否 | {} | 自定义阈值配置 |
| baseline_metrics | object | 否 | null | 基线指标用于对比 |
| blocking_mode | boolean | 否 | true | 是否在质量不达标时阻塞 |

---

## 输出格式

```typescript
interface QualityGateOutput {
  gate_status: 'pass' | 'fail' | 'warning';
  overall_score: number;                  // 0-100综合评分

  metrics: {
    test_coverage: MetricResult;
    code_complexity: MetricResult;
    security: MetricResult;
    performance: MetricResult;
    maintainability: MetricResult;
    documentation: MetricResult;
  };

  blocking_issues: Issue[];               // 阻塞性问题
  warnings: Issue[];                      // 警告
  code_smells: CodeSmell[];              // 代码异味

  trend_analysis: {
    previous_score: number;
    score_change: number;
    degraded_metrics: string[];
  };

  recommendations: Recommendation[];
  fix_priority: FixPriority[];
}

interface MetricResult {
  score: number;
  status: 'pass' | 'fail' | 'warning';
  threshold: number;
  actual: number;
  details: any;
}

interface Issue {
  severity: 'critical' | 'high' | 'medium' | 'low';
  type: string;
  location: string;
  description: string;
  fix_suggestion: string;
  estimated_time: string;
}

interface CodeSmell {
  type: 'long_method' | 'duplicated_code' | 'complex_conditional' | 'large_class';
  location: string;
  severity: 'minor' | 'major';
  recommendation: string;
  refactoring_example: string;
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
interface QualityGateInput {
}
```

### 输出接口

```typescript
interface QualityGateOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例1: PR合并前质量检查

**输入**:
```json
{
  "code_changes": {
    "added_lines": 450,
    "modified_lines": 120,
    "deleted_lines": 30,
    "files": [
      "src/services/user_service.py",
      "src/services/payment_processor.py",
      "tests/test_user_service.py"
    ]
  },
  "quality_profile": "balanced"
}
```

**输出**:
```markdown
# 质量门控报告

## 门控决策: ⚠️ 条件通过 (需要修复2个问题)

### 📊 质量评分: 82/100

| 维度 | 评分 | 状态 | 阈值 |
|------|------|------|------|
| 测试覆盖率 | 76% | ⚠️ 警告 | ≥80% |
| 代码复杂度 | 92/100 | ✅ 通过 | ≥80 |
| 安全性 | 88/100 | ✅ 通过 | ≥85 |
| 可维护性 | 78/100 | ⚠️ 警告 | ≥80 |
| 性能影响 | 95/100 | ✅ 通过 | ≥90 |
| 文档完整度 | 65% | ❌ 不合格 | ≥70% |

### 🚫 阻塞性问题 (0个)

✅ 没有阻塞性问题

### ⚠️ 警告 (2个)

#### 1. 测试覆盖率不足
- **当前**: 76%
- **要求**: ≥80%
- **缺失覆盖**:
  - `user_service.py` Line 45-58: 错误处理分支未测试
  - `payment_processor.py` Line 89-102: 退款逻辑未测试

**修复建议**:
```python
# tests/test_user_service.py
def test_create_user_database_error():
    """测试数据库错误处理"""
    with mock.patch('db.session.add', side_effect=SQLAlchemyError):
        with pytest.raises(DatabaseError):
            user_service.create_user(...)

# tests/test_payment.py
def test_refund_success():
    """测试退款成功场景"""
    result = payment_processor.refund(order_id="123")
    assert result.status == "refunded"
```

**估计时间**: 30分钟

#### 2. 文档不完整
- **当前**: 65%
- **要求**: ≥70%
- **缺失**:
  - 3个公共函数缺少docstring
  - README未更新新的API端点
  - CHANGELOG未更新

**修复建议**:
```python
def process_payment(order_id: str, amount: Decimal) -> PaymentResult:
    """处理支付请求

    Args:
        order_id: 订单ID
        amount: 支付金额（必须>0）

    Returns:
        PaymentResult对象，包含支付状态和交易ID

    Raises:
        ValueError: 如果金额无效
        PaymentError: 如果支付网关返回错误

    Example:
        >>> result = process_payment("ORD-123", Decimal("99.99"))
        >>> print(result.status)
        'success'
    """
    ...
```

**估计时间**: 15分钟

### 🔍 代码异味检测 (3个)

#### 1. 过长函数 (Code Smell)
- **文件**: `user_service.py:create_user_account()`
- **行数**: 95行
- **建议**: 分解为更小的函数

**重构方案**:
```python
def create_user_account(data):
    # 重构后: 拆分为多个职责单一的函数
    user = _validate_and_create_user(data)
    _send_verification_email(user)
    _create_default_preferences(user)
    _log_user_creation(user)
    return user
```

#### 2. 重复代码 (Duplication)
- **位置**: `payment_processor.py` Line 23-45 和 Line 89-111
- **重复度**: 85%相似
- **建议**: 提取公共函数

**重构方案**:
```python
def _validate_payment_params(order_id, amount, payment_method):
    """提取的公共验证逻辑"""
    if not order_id:
        raise ValueError("Order ID required")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if payment_method not in SUPPORTED_METHODS:
        raise ValueError(f"Unsupported method: {payment_method}")
```

### 📈 质量趋势分析

```
测试覆盖率趋势:
v1.0.0: 72% ━━━━━━━━━━━━━━━━━━
v1.1.0: 78% ━━━━━━━━━━━━━━━━━━━━━
v1.2.0: 76% ━━━━━━━━━━━━━━━━━━━ ⚠️ 下降

代码复杂度趋势:
v1.0.0: 88  ━━━━━━━━━━━━━━━━━━━━━━
v1.1.0: 90  ━━━━━━━━━━━━━━━━━━━━━━━
v1.2.0: 92  ━━━━━━━━━━━━━━━━━━━━━━━━━ ✅ 改进
```

### 🎯 修复建议优先级

**高优先级 (推荐修复后再合并)**:
1. 添加测试覆盖缺失的错误处理分支 (30分钟)
2. 为公共函数添加docstring (15分钟)
3. 更新README和CHANGELOG (10分钟)

**中优先级 (可以合并后修复)**:
4. 重构`create_user_account`函数 (1小时)
5. 消除`payment_processor.py`中的重复代码 (45分钟)

### ✅ 批准建议

**决策**: ⚠️ 条件批准

**理由**:
- 没有阻塞性问题（安全性、性能符合要求）
- 测试覆盖率76%接近80%阈值
- 文档不完整但不影响功能
- 代码异味已识别，可在后续迭代修复

**批准条件**:
1. 创建Issue跟踪文档补充任务
2. 在下一个PR中将测试覆盖率提升至80%+
3. 在2周内重构标识的3个代码异味
```

### 示例2: CI/CD集成配置

**GitHub Actions工作流**:
```yaml
name: Quality Gate

on:
  pull_request:
    branches: [main, develop]

jobs:
  quality-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # 获取完整历史用于趋势分析

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov radon bandit safety

      - name: Run Quality Gate
        id: quality_gate
        run: |
          python -m quality_gate \
            --profile balanced \
            --output-format github \
            --baseline main

      - name: Comment PR
        uses: actions/github-script@v6
        if: always()
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('quality_gate_report.md', 'utf8');

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });

      - name: Check Gate Status
        run: |
          if [ "${{ steps.quality_gate.outputs.status }}" == "fail" ]; then
            echo "❌ Quality gate failed"
            exit 1
          else
            echo "✅ Quality gate passed"
          fi
```

---

## Best Practices

### 1. 渐进式质量提升

```python
# 不要一次性要求100%完美
# 采用渐进式策略

# Week 1: Lenient模式 (建立基线)
quality_profile = 'lenient'
# 覆盖率: 60%, 复杂度: 20, 文档: 50%

# Week 2-4: Balanced模式 (稳步提升)
quality_profile = 'balanced'
# 覆盖率: 80%, 复杂度: 15, 文档: 70%

# Week 5+: Strict模式 (追求卓越)
quality_profile = 'strict'
# 覆盖率: 90%, 复杂度: 10, 文档: 80%
```

### 2. 区分关键路径和非关键路径

```python
# 为不同模块设置不同标准
custom_thresholds = {
    'critical_modules': {
        'paths': ['src/auth/*', 'src/payment/*'],
        'test_coverage': 95,
        'max_complexity': 10,
        'security_issues': 0
    },
    'standard_modules': {
        'paths': ['src/api/*', 'src/services/*'],
        'test_coverage': 85,
        'max_complexity': 15
    },
    'low_risk_modules': {
        'paths': ['src/utils/*', 'src/helpers/*'],
        'test_coverage': 70,
        'max_complexity': 20
    }
}
```

### 3. 自动化修复建议

```python
# 集成自动修复工具
auto_fix_config = {
    'code_formatting': 'black',      # 自动格式化
    'import_sorting': 'isort',       # 导入排序
    'type_hints': 'pyupgrade',       # 类型提示升级
    'security': 'safety',            # 依赖升级
    'complexity': 'radon'            # 复杂度报告
}
```

### 4. 质量趋势看板

```python
# 在Grafana中展示质量趋势
metrics_to_track = [
    'test_coverage_percentage',
    'code_complexity_score',
    'security_vulnerabilities_count',
    'code_smells_count',
    'documentation_completeness',
    'overall_quality_score'
]
```

---

## Related Skills

- `code-review`: 深度代码审查
- `test-automation`: 生成缺失测试
- `security-audit`: 安全漏洞详细分析
- `performance-optimizer`: 性能优化建议

---

## Version History

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 2.0.0 | 2025-12-12 | AI驱动质量分析、趋势追踪、自定义门槛 |
| 1.0.0 | 2025-06-01 | 初始版本 |
