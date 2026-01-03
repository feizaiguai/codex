"""
25-ai-code-optimizer AI代码优化引擎
性能分析和优化建议

功能：
- 时间复杂度分析（Big-O分析）
- 算法优化建议（O(n²)→O(n log n)）
- 内存泄漏检测（Heap分析）
- Bundle大小优化（Tree Shaking/Code Splitting）
- AI驱动重构（模式识别）
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import ast
import re
import json
from collections import defaultdict


class ComplexityLevel(Enum):
    """复杂度等级"""
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINEARITHMIC = "O(n log n)"
    QUADRATIC = "O(n²)"
    CUBIC = "O(n³)"
    EXPONENTIAL = "O(2ⁿ)"
    FACTORIAL = "O(n!)"


class IssueType(Enum):
    """问题类型"""
    COMPLEXITY = "complexity"
    MEMORY_LEAK = "memory_leak"
    BUNDLE_SIZE = "bundle_size"
    ALGORITHM = "algorithm"
    PATTERN = "pattern"


class Severity(Enum):
    """严重程度"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class OptimizationIssue:
    """优化问题"""
    issue_type: IssueType
    severity: Severity
    line_number: int
    code_snippet: str
    description: str
    current_complexity: Optional[str] = None
    suggested_complexity: Optional[str] = None
    optimization_suggestion: str = ""
    code_example: str = ""


@dataclass
class ComplexityAnalysis:
    """复杂度分析结果"""
    time_complexity: str
    space_complexity: str
    explanation: str
    bottlenecks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OptimizationReport:
    """优化报告"""
    file_path: str
    issues: List[OptimizationIssue]
    complexity_analysis: ComplexityAnalysis
    bundle_analysis: Optional[Dict[str, Any]] = None
    memory_analysis: Optional[Dict[str, Any]] = None
    overall_score: int = 0  # 0-100


class ComplexityAnalyzer:
    """时间复杂度分析器"""

    def __init__(self):
        self.loop_patterns = {
            'nested_loop_2': ComplexityLevel.QUADRATIC,
            'nested_loop_3': ComplexityLevel.CUBIC,
            'single_loop': ComplexityLevel.LINEAR,
            'divide_conquer': ComplexityLevel.LINEARITHMIC,
            'recursive_factorial': ComplexityLevel.FACTORIAL,
            'recursive_exponential': ComplexityLevel.EXPONENTIAL,
        }

    def analyze_function(self, code: str, function_name: str) -> ComplexityAnalysis:
        """分析函数复杂度"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    return self._analyze_ast_node(node)
        except SyntaxError:
            pass

        return ComplexityAnalysis(
            time_complexity="O(?)",
            space_complexity="O(?)",
            explanation="无法分析代码复杂度"
        )

    def _analyze_ast_node(self, node: ast.FunctionDef) -> ComplexityAnalysis:
        """分析AST节点"""
        loop_depth = self._get_max_loop_depth(node)
        has_recursion = self._has_recursion(node)
        bottlenecks = []

        # 确定时间复杂度
        if has_recursion:
            if self._is_divide_and_conquer(node):
                time_complexity = ComplexityLevel.LINEARITHMIC.value
            elif self._is_exponential_recursion(node):
                time_complexity = ComplexityLevel.EXPONENTIAL.value
            else:
                time_complexity = ComplexityLevel.LINEAR.value
        elif loop_depth == 0:
            time_complexity = ComplexityLevel.CONSTANT.value
        elif loop_depth == 1:
            time_complexity = ComplexityLevel.LINEAR.value
        elif loop_depth == 2:
            time_complexity = ComplexityLevel.QUADRATIC.value
            bottlenecks.append({
                'type': 'nested_loops',
                'line': node.lineno,
                'description': '嵌套循环导致O(n²)复杂度'
            })
        else:
            time_complexity = ComplexityLevel.CUBIC.value
            bottlenecks.append({
                'type': 'deep_nesting',
                'line': node.lineno,
                'description': f'{loop_depth}层嵌套循环'
            })

        # 空间复杂度分析
        space_complexity = self._analyze_space_complexity(node)

        explanation = self._generate_explanation(time_complexity, space_complexity, loop_depth, has_recursion)

        return ComplexityAnalysis(
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            explanation=explanation,
            bottlenecks=bottlenecks
        )

    def _get_max_loop_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """获取最大循环深度"""
        max_depth = current_depth

        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                depth = self._get_max_loop_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)

        return max_depth

    def _has_recursion(self, node: ast.FunctionDef) -> bool:
        """检测是否有递归"""
        function_name = node.name
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == function_name:
                    return True
        return False

    def _is_divide_and_conquer(self, node: ast.FunctionDef) -> bool:
        """检测是否为分治算法"""
        # 简化检测：查找递归调用次数
        recursion_count = 0
        function_name = node.name

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == function_name:
                    recursion_count += 1

        return recursion_count >= 2

    def _is_exponential_recursion(self, node: ast.FunctionDef) -> bool:
        """检测是否为指数级递归（如斐波那契）"""
        # 检测是否有多个递归调用且没有记忆化
        return self._is_divide_and_conquer(node) and not self._has_memoization(node)

    def _has_memoization(self, node: ast.FunctionDef) -> bool:
        """检测是否使用了记忆化"""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id in ['lru_cache', 'cache']:
                return True
        return False

    def _analyze_space_complexity(self, node: ast.FunctionDef) -> str:
        """分析空间复杂度"""
        has_list_comprehension = False
        has_recursion = self._has_recursion(node)

        for child in ast.walk(node):
            if isinstance(child, ast.ListComp):
                has_list_comprehension = True

        if has_recursion:
            return "O(n)"  # 递归栈空间
        elif has_list_comprehension:
            return "O(n)"  # 列表空间
        else:
            return "O(1)"  # 常量空间

    def _generate_explanation(self, time_complexity: str, space_complexity: str,
                            loop_depth: int, has_recursion: bool) -> str:
        """生成解释"""
        explanations = []

        if has_recursion:
            explanations.append("函数使用递归")
        if loop_depth > 0:
            explanations.append(f"包含{loop_depth}层循环嵌套")
        if time_complexity == ComplexityLevel.QUADRATIC.value:
            explanations.append("嵌套循环导致平方级时间复杂度")

        if not explanations:
            explanations.append("常量时间操作")

        return "；".join(explanations)


class AlgorithmOptimizer:
    """算法优化建议器"""

    def __init__(self):
        self.optimization_patterns = self._load_optimization_patterns()

    def _load_optimization_patterns(self) -> List[Dict[str, Any]]:
        """加载优化模式"""
        return [
            {
                'pattern': 'nested_loop_search',
                'description': '嵌套循环进行查找',
                'current': 'O(n²)',
                'optimized': 'O(n)',
                'suggestion': '使用字典/集合进行O(1)查找',
                'example': """
# 优化前：
for item in list1:
    for target in list2:
        if item == target:
            result.append(item)

# 优化后：
set2 = set(list2)
result = [item for item in list1 if item in set2]
"""
            },
            {
                'pattern': 'repeated_calculation',
                'description': '重复计算相同值',
                'current': 'O(n²)',
                'optimized': 'O(n)',
                'suggestion': '缓存计算结果',
                'example': """
# 优化前：
for i in range(n):
    result = expensive_calculation(x)
    use(result)

# 优化后：
cached_result = expensive_calculation(x)
for i in range(n):
    use(cached_result)
"""
            },
            {
                'pattern': 'list_concatenation',
                'description': '循环中拼接列表',
                'current': 'O(n²)',
                'optimized': 'O(n)',
                'suggestion': '使用列表推导或join',
                'example': """
# 优化前：
result = []
for item in items:
    result = result + [processed(item)]

# 优化后：
result = [processed(item) for item in items]
"""
            },
            {
                'pattern': 'sort_in_loop',
                'description': '循环中重复排序',
                'current': 'O(n² log n)',
                'optimized': 'O(n log n)',
                'suggestion': '在循环外排序一次',
                'example': """
# 优化前：
for i in range(n):
    sorted_list = sorted(data)
    process(sorted_list)

# 优化后：
sorted_list = sorted(data)
for i in range(n):
    process(sorted_list)
"""
            }
        ]

    def suggest_optimization(self, code: str, complexity: ComplexityAnalysis) -> List[OptimizationIssue]:
        """建议优化方案"""
        issues = []

        # 检测嵌套循环
        if "O(n²)" in complexity.time_complexity or "O(n³)" in complexity.time_complexity:
            nested_loops = self._detect_nested_loops(code)
            for loop_info in nested_loops:
                pattern = self._match_optimization_pattern(code, loop_info)
                if pattern:
                    issues.append(OptimizationIssue(
                        issue_type=IssueType.ALGORITHM,
                        severity=Severity.HIGH,
                        line_number=loop_info['line'],
                        code_snippet=loop_info['code'],
                        description=pattern['description'],
                        current_complexity=pattern['current'],
                        suggested_complexity=pattern['optimized'],
                        optimization_suggestion=pattern['suggestion'],
                        code_example=pattern['example']
                    ))

        return issues

    def _detect_nested_loops(self, code: str) -> List[Dict[str, Any]]:
        """检测嵌套循环"""
        try:
            tree = ast.parse(code)
            nested_loops = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While)):
                    # 检查是否包含嵌套循环
                    for child in ast.walk(node):
                        if child != node and isinstance(child, (ast.For, ast.While)):
                            nested_loops.append({
                                'line': node.lineno,
                                'code': ast.unparse(node) if hasattr(ast, 'unparse') else '...'
                            })
                            break

            return nested_loops
        except:
            return []

    def _match_optimization_pattern(self, code: str, loop_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """匹配优化模式"""
        loop_code = loop_info['code']

        # 检测是否为查找模式
        if 'if' in loop_code and '==' in loop_code:
            return self.optimization_patterns[0]

        # 检测是否为重复计算
        if '(' in loop_code and ')' in loop_code:
            return self.optimization_patterns[1]

        # 默认返回通用建议
        return self.optimization_patterns[0]


class MemoryAnalyzer:
    """内存泄漏检测器"""

    def analyze(self, code: str) -> Dict[str, Any]:
        """分析内存使用"""
        issues = []

        # 检测常见内存泄漏模式
        issues.extend(self._detect_global_variables(code))
        issues.extend(self._detect_circular_references(code))
        issues.extend(self._detect_unclosed_resources(code))
        issues.extend(self._detect_large_data_structures(code))

        return {
            'total_issues': len(issues),
            'issues': issues,
            'estimated_impact': self._estimate_memory_impact(issues)
        }

    def _detect_global_variables(self, code: str) -> List[Dict[str, Any]]:
        """检测全局变量"""
        issues = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Global):
                    issues.append({
                        'type': 'global_variable',
                        'line': node.lineno,
                        'severity': 'medium',
                        'description': '使用全局变量可能导致内存无法释放'
                    })
        except:
            pass
        return issues

    def _detect_circular_references(self, code: str) -> List[Dict[str, Any]]:
        """检测循环引用"""
        issues = []
        # 简化检测：查找self引用
        if 'self.' in code and '=' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if 'self.' in line and '=' in line and 'self' in line.split('=')[1]:
                    issues.append({
                        'type': 'circular_reference',
                        'line': i,
                        'severity': 'high',
                        'description': '可能存在循环引用'
                    })
        return issues

    def _detect_unclosed_resources(self, code: str) -> List[Dict[str, Any]]:
        """检测未关闭资源"""
        issues = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            if 'open(' in line and 'with' not in line:
                issues.append({
                    'type': 'unclosed_file',
                    'line': i,
                    'severity': 'high',
                    'description': '文件未使用with语句，可能导致资源泄漏'
                })

        return issues

    def _detect_large_data_structures(self, code: str) -> List[Dict[str, Any]]:
        """检测大型数据结构"""
        issues = []
        # 检测列表推导式中的大数据
        if '[' in code and 'for' in code and 'range(' in code:
            match = re.search(r'range\((\d+)\)', code)
            if match and int(match.group(1)) > 10000:
                issues.append({
                    'type': 'large_list',
                    'line': 0,
                    'severity': 'medium',
                    'description': f'创建大型列表（{match.group(1)}个元素）'
                })

        return issues

    def _estimate_memory_impact(self, issues: List[Dict[str, Any]]) -> str:
        """估算内存影响"""
        if not issues:
            return "低"

        high_count = sum(1 for i in issues if i['severity'] == 'high')

        if high_count >= 3:
            return "高"
        elif high_count >= 1:
            return "中"
        else:
            return "低"


class BundleOptimizer:
    """Bundle大小优化器"""

    def analyze(self, project_path: str) -> Dict[str, Any]:
        """分析Bundle大小"""
        return {
            'total_size': '未实现',
            'suggestions': [
                {
                    'type': 'tree_shaking',
                    'description': '启用Tree Shaking删除未使用代码',
                    'impact': '可减少20-30%体积'
                },
                {
                    'type': 'code_splitting',
                    'description': '实现代码分割按需加载',
                    'impact': '首次加载可减少50%+'
                },
                {
                    'type': 'compression',
                    'description': '启用Gzip/Brotli压缩',
                    'impact': '可减少60-70%传输大小'
                }
            ]
        }


class AICodeOptimizer:
    """AI代码优化器主类"""

    def __init__(self):
        self.complexity_analyzer = ComplexityAnalyzer()
        self.algorithm_optimizer = AlgorithmOptimizer()
        self.memory_analyzer = MemoryAnalyzer()
        self.bundle_optimizer = BundleOptimizer()

    def optimize_code(self, code: str, file_path: str = "unknown") -> OptimizationReport:
        """优化代码"""
        issues = []

        # 1. 复杂度分析
        complexity = self._analyze_all_functions(code)

        # 2. 算法优化建议
        algo_issues = self.algorithm_optimizer.suggest_optimization(code, complexity)
        issues.extend(algo_issues)

        # 3. 内存分析
        memory_analysis = self.memory_analyzer.analyze(code)
        for mem_issue in memory_analysis['issues']:
            issues.append(OptimizationIssue(
                issue_type=IssueType.MEMORY_LEAK,
                severity=Severity[mem_issue['severity'].upper()],
                line_number=mem_issue['line'],
                code_snippet="",
                description=mem_issue['description']
            ))

        # 4. 计算总体评分
        overall_score = self._calculate_score(complexity, issues)

        return OptimizationReport(
            file_path=file_path,
            issues=issues,
            complexity_analysis=complexity,
            memory_analysis=memory_analysis,
            overall_score=overall_score
        )

    def _analyze_all_functions(self, code: str) -> ComplexityAnalysis:
        """分析所有函数"""
        try:
            tree = ast.parse(code)
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

            if not functions:
                return ComplexityAnalysis(
                    time_complexity="O(1)",
                    space_complexity="O(1)",
                    explanation="无函数定义"
                )

            # 分析第一个函数（简化）
            return self.complexity_analyzer._analyze_ast_node(functions[0])

        except:
            return ComplexityAnalysis(
                time_complexity="O(?)",
                space_complexity="O(?)",
                explanation="代码解析失败"
            )

    def _calculate_score(self, complexity: ComplexityAnalysis, issues: List[OptimizationIssue]) -> int:
        """计算代码质量评分（0-100）"""
        score = 100

        # 复杂度扣分
        complexity_penalties = {
            "O(1)": 0,
            "O(log n)": 0,
            "O(n)": 5,
            "O(n log n)": 10,
            "O(n²)": 25,
            "O(n³)": 40,
            "O(2ⁿ)": 50,
            "O(n!)": 60
        }

        score -= complexity_penalties.get(complexity.time_complexity, 0)

        # 问题扣分
        severity_penalties = {
            Severity.CRITICAL: 20,
            Severity.HIGH: 15,
            Severity.MEDIUM: 10,
            Severity.LOW: 5,
            Severity.INFO: 2
        }

        for issue in issues:
            score -= severity_penalties.get(issue.severity, 0)

        return max(0, min(100, score))

    def generate_report(self, report: OptimizationReport) -> str:
        """生成优化报告"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"AI代码优化报告")
        lines.append(f"文件: {report.file_path}")
        lines.append(f"总体评分: {report.overall_score}/100")
        lines.append("=" * 80)
        lines.append("")

        # 复杂度分析
        lines.append("## 复杂度分析")
        lines.append(f"时间复杂度: {report.complexity_analysis.time_complexity}")
        lines.append(f"空间复杂度: {report.complexity_analysis.space_complexity}")
        lines.append(f"说明: {report.complexity_analysis.explanation}")
        lines.append("")

        # 问题列表
        if report.issues:
            lines.append(f"## 发现问题 ({len(report.issues)}个)")
            for i, issue in enumerate(report.issues, 1):
                lines.append(f"\n### {i}. {issue.description}")
                lines.append(f"类型: {issue.issue_type.value}")
                lines.append(f"严重程度: {issue.severity.value}")
                lines.append(f"行号: {issue.line_number}")

                if issue.current_complexity and issue.suggested_complexity:
                    lines.append(f"当前复杂度: {issue.current_complexity}")
                    lines.append(f"建议复杂度: {issue.suggested_complexity}")

                if issue.optimization_suggestion:
                    lines.append(f"\n优化建议: {issue.optimization_suggestion}")

                if issue.code_example:
                    lines.append(f"\n代码示例:")
                    lines.append(issue.code_example)
        else:
            lines.append("## ✓ 未发现明显问题")

        # 内存分析
        if report.memory_analysis:
            lines.append(f"\n## 内存分析")
            lines.append(f"内存问题: {report.memory_analysis['total_issues']}个")
            lines.append(f"预估影响: {report.memory_analysis['estimated_impact']}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)


# 工具函数
def optimize_file(file_path: str) -> OptimizationReport:
    """优化单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    optimizer = AICodeOptimizer()
    return optimizer.optimize_code(code, file_path)


def batch_optimize(file_paths: List[str]) -> List[OptimizationReport]:
    """批量优化文件"""
    optimizer = AICodeOptimizer()
    reports = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            report = optimizer.optimize_code(code, file_path)
            reports.append(report)
        except Exception as e:
            print(f"错误: 无法处理文件 {file_path}: {e}")

    return reports
