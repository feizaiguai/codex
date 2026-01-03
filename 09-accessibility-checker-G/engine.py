"""09-accessibility-checker 引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List
import re


class WCAGLevel(str, Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


@dataclass
class AccessibilityIssue:
    severity: str
    message: str
    wcag: str


class AccessibilityChecker:
    def check_html(self, html: str) -> List[AccessibilityIssue]:
        issues: List[AccessibilityIssue] = []
        if "<html" in html and "lang=" not in html:
            issues.append(AccessibilityIssue("medium", "HTML 缺少 lang 属性", "WCAG 3.1.1"))

        # 检查 img alt
        for img in re.findall(r"<img[^>]*>", html, flags=re.I):
            if "alt=" not in img.lower():
                issues.append(AccessibilityIssue("medium", "图片缺少 alt 文本", "WCAG 1.1.1"))

        # 检查 input label
        inputs = re.findall(r"<input[^>]*>", html, flags=re.I)
        if inputs and "<label" not in html.lower():
            issues.append(AccessibilityIssue("medium", "表单缺少 label", "WCAG 1.3.1"))

        return issues

    def check_file(self, path: str) -> List[AccessibilityIssue]:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        return self.check_html(text)

    def generate_report(self, issues: List[AccessibilityIssue]) -> str:
        lines = ["# 无障碍检查报告", ""]
        if not issues:
            lines.append("未发现明显问题。")
            return "\n".join(lines)
        for i, issue in enumerate(issues, 1):
            lines.append(f"{i}. [{issue.severity}] {issue.message} ({issue.wcag})")
        return "\n".join(lines)


if __name__ == "__main__":
    print("09-accessibility-checker engine ready")