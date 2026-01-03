"""08-performance-optimizer 性能诊断引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import ast
import json


@dataclass
class PerformanceIssue:
    kind: str
    severity: str
    message: str
    location: str


class LoopDepthVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.max_depth = 0
        self.current = 0

    def visit_For(self, node: ast.For) -> None:
        self.current += 1
        self.max_depth = max(self.max_depth, self.current)
        self.generic_visit(node)
        self.current -= 1

    def visit_While(self, node: ast.While) -> None:
        self.current += 1
        self.max_depth = max(self.max_depth, self.current)
        self.generic_visit(node)
        self.current -= 1


class PerformanceOptimizer:
    """对 Python 文件进行简单性能体检"""

    def analyze_file(self, path: str) -> Dict[str, Any]:
        src = Path(path)
        text = src.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(text)

        loop_visitor = LoopDepthVisitor()
        loop_visitor.visit(tree)
        max_depth = loop_visitor.max_depth

        issues: List[PerformanceIssue] = []

        if max_depth >= 2:
            issues.append(
                PerformanceIssue(
                    kind="nested_loops",
                    severity="high" if max_depth >= 3 else "medium",
                    message=f"检测到循环嵌套深度 {max_depth}，可能导致 O(n^2) 或更高复杂度",
                    location=src.name,
                )
            )

        if "for " in text and (".execute(" in text or ".query(" in text or "SELECT " in text):
            issues.append(
                PerformanceIssue(
                    kind="n_plus_one",
                    severity="medium",
                    message="检测到循环内可能的数据库调用，存在 N+1 风险",
                    location=src.name,
                )
            )

        metrics = {
            "lines": len(text.splitlines()),
            "max_loop_depth": max_depth,
            "issue_count": len(issues),
        }

        return {
            "file": str(src),
            "metrics": metrics,
            "issues": [issue.__dict__ for issue in issues],
        }

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        lines = [
            f"# 性能优化报告 - {Path(analysis['file']).name}",
            "",
            f"- 行数: {analysis['metrics']['lines']}",
            f"- 最大循环嵌套: {analysis['metrics']['max_loop_depth']}",
            f"- 发现问题数: {analysis['metrics']['issue_count']}",
            "",
            "## 问题清单",
        ]
        if not analysis["issues"]:
            lines.append("- 未检测到明显性能问题")
        else:
            for item in analysis["issues"]:
                lines.append(f"- [{item['severity']}] {item['kind']}: {item['message']}")
        return "\n".join(lines)


def analyze_file(path: str) -> Dict[str, Any]:
    return PerformanceOptimizer().analyze_file(path)


def generate_report(analysis: Dict[str, Any]) -> str:
    return PerformanceOptimizer().generate_report(analysis)


if __name__ == "__main__":
    print("08-performance-optimizer engine ready")