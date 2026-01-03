"""10-quality-gate 引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import ast
from pathlib import Path


@dataclass
class QualityMetrics:
    coverage: float
    complexity: float
    security: float
    vulns: int


@dataclass
class QualityGateResult:
    passed: bool
    score: float
    details: Dict[str, Any]


class QualityGate:
    def evaluate(self, metrics: QualityMetrics) -> QualityGateResult:
        score = (
            metrics.coverage * 0.3
            + (100 - metrics.complexity * 10) * 0.2
            + metrics.security * 0.4
            - metrics.vulns * 5
        )
        passed = metrics.coverage >= 80 and metrics.complexity <= 10 and metrics.security >= 90 and metrics.vulns == 0
        return QualityGateResult(passed=passed, score=max(0, min(100, score)), details=metrics.__dict__)

    def analyze_file_complexity(self, path: str) -> float:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(text)
        loops = sum(isinstance(n, (ast.For, ast.While)) for n in ast.walk(tree))
        return float(max(1, loops))

    def generate_report(self, result: QualityGateResult) -> str:
        lines = [
            "# 质量门控报告",
            "",
            f"- 结果: {'通过' if result.passed else '未通过'}",
            f"- 总分: {result.score:.1f}",
            "",
            "## 指标",
            f"- 覆盖率: {result.details['coverage']}%",
            f"- 复杂度: {result.details['complexity']}",
            f"- 安全评分: {result.details['security']}%",
            f"- 严重漏洞数: {result.details['vulns']}",
        ]
        return "\n".join(lines)


if __name__ == "__main__":
    print("10-quality-gate engine ready")