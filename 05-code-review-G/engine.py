"""
05-code-review 代码审查引擎
代码质量检查和安全扫描

支持：
- 复杂度分析（圈复杂度/认知复杂度）
- OWASP Top 10 安全检查
- 性能瓶颈识别
- N+1 查询检测
- 代码质量评分（0-100）
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import ast
import re


class Severity(Enum):
    """问题严重程度"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class Issue:
    """代码问题"""
    file: str
    line: int
    severity: Severity
    category: str
    message: str
    suggestion: str


@dataclass
class ComplexityMetrics:
    """复杂度指标"""
    cyclomatic_complexity: int  # 圈复杂度
    cognitive_complexity: int  # 认知复杂度
    lines_of_code: int
    max_nesting_depth: int


class ComplexityAnalyzer:
    """复杂度分析器"""

    def analyze_python_file(self, filepath: str) -> Dict[str, ComplexityMetrics]:
        """分析 Python 文件复杂度"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='gbk') as f:
                tree = ast.parse(f.read())

        metrics = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics[node.name] = self._calculate_metrics(node)

        return metrics

    def _calculate_metrics(self, node: ast.FunctionDef) -> ComplexityMetrics:
        """计算函数复杂度"""
        cyclomatic = self._calculate_cyclomatic(node)
        cognitive = self._calculate_cognitive(node)
        loc = self._count_lines(node)
        nesting = self._max_nesting_depth(node)

        return ComplexityMetrics(
            cyclomatic_complexity=cyclomatic,
            cognitive_complexity=cognitive,
            lines_of_code=loc,
            max_nesting_depth=nesting
        )

    def _calculate_cyclomatic(self, node: ast.AST) -> int:
        """计算圈复杂度"""
        complexity = 1  # 基础复杂度

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _calculate_cognitive(self, node: ast.AST) -> int:
        """计算认知复杂度"""
        cognitive = 0
        nesting_level = 0

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                cognitive += 1 + nesting_level
                nesting_level += 1
            elif isinstance(child, ast.BoolOp):
                cognitive += len(child.values) - 1

        return cognitive

    def _count_lines(self, node: ast.AST) -> int:
        """计算代码行数"""
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            return node.end_lineno - node.lineno + 1
        return 0

    def _max_nesting_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """计算最大嵌套深度"""
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                child_depth = self._max_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._max_nesting_depth(child, current_depth)
                max_depth = max(max_depth, child_depth)

        return max_depth


class SecurityScanner:
    """安全扫描器（OWASP Top 10）"""

    def scan_file(self, filepath: str) -> List[Issue]:
        """扫描文件安全问题"""
        issues = []

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # 检查 SQL 注入
        issues.extend(self._check_sql_injection(lines, filepath))

        # 检查硬编码密码
        issues.extend(self._check_hardcoded_secrets(lines, filepath))

        # 检查不安全的反序列化
        issues.extend(self._check_unsafe_deserialization(lines, filepath))

        # 检查 eval 使用
        issues.extend(self._check_eval_usage(lines, filepath))

        return issues

    def _check_sql_injection(self, lines: List[str], filepath: str) -> List[Issue]:
        """检查 SQL 注入风险"""
        issues = []
        sql_patterns = [
            r'execute\([^?]*\+',  # 字符串拼接
            r'\.format\(',  # 使用 format
            r'f["\'].*SELECT.*{',  # f-string
        ]

        for i, line in enumerate(lines, 1):
            for pattern in sql_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(Issue(
                        file=filepath,
                        line=i,
                        severity=Severity.CRITICAL,
                        category='SQL Injection',
                        message='潜在的 SQL 注入风险',
                        suggestion='使用参数化查询'
                    ))

        return issues

    def _check_hardcoded_secrets(self, lines: List[str], filepath: str) -> List[Issue]:
        """检查硬编码密码"""
        issues = []
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]

        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(Issue(
                        file=filepath,
                        line=i,
                        severity=Severity.HIGH,
                        category='Hardcoded Secret',
                        message='检测到硬编码的敏感信息',
                        suggestion='使用环境变量或密钥管理系统'
                    ))

        return issues

    def _check_unsafe_deserialization(self, lines: List[str], filepath: str) -> List[Issue]:
        """检查不安全的反序列化"""
        issues = []

        for i, line in enumerate(lines, 1):
            if 'pickle.loads' in line or 'yaml.load(' in line:
                issues.append(Issue(
                    file=filepath,
                    line=i,
                    severity=Severity.HIGH,
                    category='Unsafe Deserialization',
                    message='不安全的反序列化操作',
                    suggestion='使用 yaml.safe_load() 或避免使用 pickle'
                ))

        return issues

    def _check_eval_usage(self, lines: List[str], filepath: str) -> List[Issue]:
        """检查 eval 使用"""
        issues = []

        for i, line in enumerate(lines, 1):
            if re.search(r'\beval\s*\(', line):
                issues.append(Issue(
                    file=filepath,
                    line=i,
                    severity=Severity.CRITICAL,
                    category='Code Injection',
                    message='使用 eval() 可能导致代码注入',
                    suggestion='避免使用 eval()，使用更安全的替代方案'
                ))

        return issues


class PerformanceScanner:
    """性能扫描器"""

    def scan_file(self, filepath: str) -> List[Issue]:
        """扫描性能问题"""
        issues = []

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # 检查 N+1 查询
        issues.extend(self._check_n_plus_one(lines, filepath))

        # 检查循环中的数据库查询
        issues.extend(self._check_db_in_loop(lines, filepath))

        # 检查大量字符串拼接
        issues.extend(self._check_string_concat(lines, filepath))

        return issues

    def _check_n_plus_one(self, lines: List[str], filepath: str) -> List[Issue]:
        """检查 N+1 查询问题"""
        issues = []

        in_loop = False
        loop_start = 0

        for i, line in enumerate(lines, 1):
            if re.search(r'for .+ in ', line):
                in_loop = True
                loop_start = i

            if in_loop and re.search(r'\.(get|filter|query)\(', line):
                issues.append(Issue(
                    file=filepath,
                    line=i,
                    severity=Severity.MEDIUM,
                    category='N+1 Query',
                    message=f'循环中的数据库查询（行 {loop_start}）',
                    suggestion='使用 select_related() 或 prefetch_related()'
                ))

            # 简化：假设缩进减少表示循环结束
            if in_loop and line and not line.startswith(' '):
                in_loop = False

        return issues

    def _check_db_in_loop(self, lines: List[str], filepath: str) -> List[Issue]:
        """检查循环中的数据库操作"""
        issues = []
        # 实现类似 N+1 的检查
        return issues

    def _check_string_concat(self, lines: List[str], filepath: str) -> List[Issue]:
        """检查字符串拼接"""
        issues = []

        for i, line in enumerate(lines, 1):
            # 循环中的 + 拼接
            if 'for' in line and '+=' in line and ('str' in line or '"' in line):
                issues.append(Issue(
                    file=filepath,
                    line=i,
                    severity=Severity.LOW,
                    category='Performance',
                    message='循环中使用字符串拼接效率低',
                    suggestion='使用 join() 或 StringIO'
                ))

        return issues


class CodeQualityScorer:
    """代码质量评分器"""

    def score_file(
        self,
        filepath: str,
        complexity: Dict[str, ComplexityMetrics],
        issues: List[Issue]
    ) -> Dict[str, Any]:
        """评分代码质量（0-100）"""
        score = 100.0

        # 复杂度扣分
        for func_name, metrics in complexity.items():
            if metrics.cyclomatic_complexity > 10:
                score -= (metrics.cyclomatic_complexity - 10) * 2

            if metrics.cognitive_complexity > 15:
                score -= (metrics.cognitive_complexity - 15) * 1.5

            if metrics.max_nesting_depth > 4:
                score -= (metrics.max_nesting_depth - 4) * 3

        # 问题扣分
        severity_weights = {
            Severity.CRITICAL: 15,
            Severity.HIGH: 10,
            Severity.MEDIUM: 5,
            Severity.LOW: 2,
            Severity.INFO: 1
        }

        for issue in issues:
            score -= severity_weights.get(issue.severity, 0)

        # 确保分数在 0-100 范围内
        score = max(0, min(100, score))

        # 评级
        if score >= 90:
            grade = 'A (优秀)'
        elif score >= 80:
            grade = 'B (良好)'
        elif score >= 70:
            grade = 'C (中等)'
        elif score >= 60:
            grade = 'D (较差)'
        else:
            grade = 'F (不合格)'

        return {
            'file': filepath,
            'score': round(score, 1),
            'grade': grade,
            'total_issues': len(issues),
            'critical_issues': len([i for i in issues if i.severity == Severity.CRITICAL]),
            'high_issues': len([i for i in issues if i.severity == Severity.HIGH]),
        }


class CodeReviewer:
    """代码审查主类"""

    def __init__(self):
        self.complexity_analyzer = ComplexityAnalyzer()
        self.security_scanner = SecurityScanner()
        self.performance_scanner = PerformanceScanner()
        self.scorer = CodeQualityScorer()

    def review_file(self, filepath: str) -> Dict[str, Any]:
        """审查文件"""
        print(f"[代码审查] 正在审查 {filepath}...")

        # 复杂度分析
        complexity = self.complexity_analyzer.analyze_python_file(filepath)

        # 安全扫描
        security_issues = self.security_scanner.scan_file(filepath)

        # 性能扫描
        performance_issues = self.performance_scanner.scan_file(filepath)

        all_issues = security_issues + performance_issues

        # 评分
        quality_score = self.scorer.score_file(filepath, complexity, all_issues)

        return {
            'complexity': complexity,
            'issues': all_issues,
            'quality_score': quality_score
        }

    def generate_report(self, review_result: Dict[str, Any]) -> str:
        """生成审查报告"""
        report = f"""# 代码审查报告

## 质量评分
- **分数**: {review_result['quality_score']['score']}/100
- **评级**: {review_result['quality_score']['grade']}
- **总问题数**: {review_result['quality_score']['total_issues']}
  - 严重: {review_result['quality_score']['critical_issues']}
  - 高危: {review_result['quality_score']['high_issues']}

## 复杂度分析
"""

        for func_name, metrics in review_result['complexity'].items():
            report += f"""
### 函数: {func_name}
- 圈复杂度: {metrics.cyclomatic_complexity} {'⚠️ 过高' if metrics.cyclomatic_complexity > 10 else '✓'}
- 认知复杂度: {metrics.cognitive_complexity} {'⚠️ 过高' if metrics.cognitive_complexity > 15 else '✓'}
- 代码行数: {metrics.lines_of_code}
- 最大嵌套深度: {metrics.max_nesting_depth} {'⚠️ 过深' if metrics.max_nesting_depth > 4 else '✓'}
"""

        report += "\n## 问题列表\n"

        # 按严重程度分组
        issues_by_severity = {}
        for issue in review_result['issues']:
            severity = issue.severity.value
            if severity not in issues_by_severity:
                issues_by_severity[severity] = []
            issues_by_severity[severity].append(issue)

        for severity in ['critical', 'high', 'medium', 'low']:
            if severity in issues_by_severity:
                report += f"\n### {severity.upper()}\n"
                for issue in issues_by_severity[severity]:
                    report += f"""
- **{issue.category}** (行 {issue.line})
  - 问题: {issue.message}
  - 建议: {issue.suggestion}
"""

        return report
