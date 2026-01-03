"""
11-debugger 高级Debug引擎
假设验证和运行时数据驱动决策

工作流程：
1. 提出假设（Hypothesis）
2. 运行时埋点（Instrumentation）
3. Bug复现（Reproduction）
4. 根因分析（Root Cause Analysis）
5. 自动修复建议（Fix Suggestion）
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import ast
import re


class BugType(Enum):
    """Bug类型"""
    LOGIC_ERROR = "logic_error"
    NULL_REFERENCE = "null_reference"
    INDEX_OUT_OF_BOUNDS = "index_out_of_bounds"
    TYPE_ERROR = "type_error"
    RACE_CONDITION = "race_condition"
    MEMORY_LEAK = "memory_leak"


@dataclass
class Hypothesis:
    """调试假设"""
    id: str
    description: str
    location: str
    line: int
    evidence: List[str]
    confidence: float  # 0-100


@dataclass
class Breakpoint:
    """断点"""
    file: str
    line: int
    condition: Optional[str]
    log_expression: Optional[str]


@dataclass
class DebugReport:
    """调试报告"""
    bug_type: BugType
    root_cause: str
    hypotheses: List[Hypothesis]
    fix_suggestions: List[str]
    reproduction_steps: List[str]


class HypothesisGenerator:
    """假设生成器"""

    def generate_from_error(self, error_msg: str, stack_trace: str) -> List[Hypothesis]:
        """从错误信息生成假设"""
        hypotheses = []

        # 分析错误类型
        if 'NoneType' in error_msg or 'null' in error_msg.lower():
            hypotheses.append(Hypothesis(
                id='H1',
                description='可能存在空引用（NoneType/null）',
                location='',
                line=0,
                evidence=[error_msg],
                confidence=90.0
            ))

        if 'IndexError' in error_msg or 'out of range' in error_msg:
            hypotheses.append(Hypothesis(
                id='H2',
                description='数组索引越界',
                location='',
                line=0,
                evidence=[error_msg],
                confidence=95.0
            ))

        if 'TypeError' in error_msg:
            hypotheses.append(Hypothesis(
                id='H3',
                description='类型不匹配',
                location='',
                line=0,
                evidence=[error_msg],
                confidence=85.0
            ))

        # 从堆栈跟踪提取位置
        file_line_pattern = r'File "([^"]+)", line (\d+)'
        matches = re.findall(file_line_pattern, stack_trace)
        if matches:
            file, line = matches[-1]
            for h in hypotheses:
                h.location = file
                h.line = int(line)

        return hypotheses


class InstrumentationEngine:
    """埋点引擎"""

    def insert_logging(self, code: str, variables: List[str]) -> str:
        """插入日志语句"""
        lines = code.split('\n')
        instrumented = []

        for line in lines:
            instrumented.append(line)

            # 在关键位置插入日志
            for var in variables:
                if var in line and '=' in line:
                    indent = len(line) - len(line.lstrip())
                    log_stmt = ' ' * indent + f'print(f"[DEBUG] {var} = {{{var}}}")'
                    instrumented.append(log_stmt)

        return '\n'.join(instrumented)

    def generate_breakpoints(self, file: str, suspicious_lines: List[int]) -> List[Breakpoint]:
        """生成断点"""
        breakpoints = []

        for line in suspicious_lines:
            breakpoints.append(Breakpoint(
                file=file,
                line=line,
                condition=None,
                log_expression=f'locals()'
            ))

        return breakpoints


class RootCauseAnalyzer:
    """根因分析器"""

    def analyze(
        self,
        error_msg: str,
        stack_trace: str,
        code: str,
        runtime_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """根因分析"""
        root_cause = {
            'type': BugType.LOGIC_ERROR,
            'description': '',
            'affected_variables': [],
            'timeline': []
        }

        # 分析错误类型
        if 'NoneType' in error_msg:
            root_cause['type'] = BugType.NULL_REFERENCE
            root_cause['description'] = '对象为 None 时调用了方法或属性'

            # 查找可能为 None 的变量
            none_vars = self._find_none_assignments(code)
            root_cause['affected_variables'] = none_vars

        elif 'IndexError' in error_msg:
            root_cause['type'] = BugType.INDEX_OUT_OF_BOUNDS
            root_cause['description'] = '访问数组时索引超出范围'

        elif 'TypeError' in error_msg:
            root_cause['type'] = BugType.TYPE_ERROR
            root_cause['description'] = '类型不匹配'

        # 运行时数据分析
        if runtime_data:
            root_cause['timeline'] = self._reconstruct_timeline(runtime_data)

        return root_cause

    def _find_none_assignments(self, code: str) -> List[str]:
        """查找可能为 None 的变量"""
        none_vars = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if isinstance(node.value, ast.Constant) and node.value.value is None:
                                none_vars.append(target.id)

        except:
            pass

        return none_vars

    def _reconstruct_timeline(self, runtime_data: Dict[str, Any]) -> List[str]:
        """重建执行时间线"""
        timeline = []

        # 模拟时间线重建
        for key, value in runtime_data.items():
            timeline.append(f"{key} = {value}")

        return timeline


class FixSuggestionEngine:
    """修复建议引擎"""

    def generate_suggestions(self, bug_type: BugType, root_cause: Dict[str, Any]) -> List[str]:
        """生成修复建议"""
        suggestions = []

        if bug_type == BugType.NULL_REFERENCE:
            suggestions.append("添加空值检查:")
            suggestions.append("```python")
            suggestions.append("if obj is not None:")
            suggestions.append("    obj.method()")
            suggestions.append("```")

            suggestions.append("或使用可选链:")
            suggestions.append("```python")
            suggestions.append("result = obj.method() if obj else default_value")
            suggestions.append("```")

        elif bug_type == BugType.INDEX_OUT_OF_BOUNDS:
            suggestions.append("添加边界检查:")
            suggestions.append("```python")
            suggestions.append("if 0 <= index < len(array):")
            suggestions.append("    value = array[index]")
            suggestions.append("```")

            suggestions.append("或使用 get() 方法（字典）:")
            suggestions.append("```python")
            suggestions.append("value = dict.get(key, default_value)")
            suggestions.append("```")

        elif bug_type == BugType.TYPE_ERROR:
            suggestions.append("添加类型检查:")
            suggestions.append("```python")
            suggestions.append("if isinstance(value, expected_type):")
            suggestions.append("    # 处理")
            suggestions.append("```")

            suggestions.append("或使用类型转换:")
            suggestions.append("```python")
            suggestions.append("value = int(value) if value.isdigit() else 0")
            suggestions.append("```")

        return suggestions


class BugReproducer:
    """Bug复现器"""

    def generate_reproduction_steps(
        self,
        error_msg: str,
        input_data: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """生成复现步骤"""
        steps = [
            "# Bug 复现步骤",
            "",
            "1. 准备测试数据:"
        ]

        if input_data:
            steps.append("```python")
            for key, value in input_data.items():
                steps.append(f"{key} = {repr(value)}")
            steps.append("```")

        steps.extend([
            "",
            "2. 执行触发 Bug 的操作",
            "",
            "3. 观察错误:",
            f"   {error_msg}",
            "",
            "4. 验证修复后的行为"
        ])

        return steps


class Debugger:
    """高级调试器主类"""

    def __init__(self):
        self.hypothesis_gen = HypothesisGenerator()
        self.instrumentation = InstrumentationEngine()
        self.root_cause_analyzer = RootCauseAnalyzer()
        self.fix_suggester = FixSuggestionEngine()
        self.reproducer = BugReproducer()

    def debug(
        self,
        error_msg: str,
        stack_trace: str,
        code: str,
        runtime_data: Optional[Dict[str, Any]] = None
    ) -> DebugReport:
        """执行调试"""
        print("[DEBUG] 开始调试流程...")

        # 步骤1: 生成假设
        print("\n[1/4] 生成调试假设...")
        hypotheses = self.hypothesis_gen.generate_from_error(error_msg, stack_trace)
        for h in hypotheses:
            print(f"  {h.id}: {h.description} (置信度: {h.confidence}%)")

        # 步骤2: 根因分析
        print("\n[2/4] 根因分析...")
        root_cause = self.root_cause_analyzer.analyze(
            error_msg, stack_trace, code, runtime_data
        )
        print(f"  根因类型: {root_cause['type'].value}")
        print(f"  描述: {root_cause['description']}")

        # 步骤3: 生成修复建议
        print("\n[3/4] 生成修复建议...")
        suggestions = self.fix_suggester.generate_suggestions(
            root_cause['type'], root_cause
        )

        # 步骤4: 生成复现步骤
        print("\n[4/4] 生成复现步骤...")
        reproduction = self.reproducer.generate_reproduction_steps(error_msg)

        return DebugReport(
            bug_type=root_cause['type'],
            root_cause=root_cause['description'],
            hypotheses=hypotheses,
            fix_suggestions=suggestions,
            reproduction_steps=reproduction
        )

    def generate_report(self, debug_report: DebugReport) -> str:
        """生成调试报告"""
        report = f"""# 调试报告

## Bug 类型
**{debug_report.bug_type.value}**

## 根因
{debug_report.root_cause}

## 调试假设
"""

        for h in debug_report.hypotheses:
            report += f"""
### {h.id}: {h.description}
- **位置**: {h.location}:{h.line}
- **置信度**: {h.confidence}%
- **证据**: {', '.join(h.evidence)}
"""

        report += "\n## 修复建议\n"
        for suggestion in debug_report.fix_suggestions:
            report += f"{suggestion}\n"

        report += "\n## Bug 复现步骤\n"
        for step in debug_report.reproduction_steps:
            report += f"{step}\n"

        return report
