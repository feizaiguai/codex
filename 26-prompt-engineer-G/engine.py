"""26-prompt-engineer 引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
import re


class SafetyLevel(str, Enum):
    SAFE = "safe"
    WARNING = "warning"
    DANGEROUS = "dangerous"


@dataclass
class SafetyResult:
    level: SafetyLevel
    issues: List[str]
    suggestions: List[str]


@dataclass
class PromptOptimization:
    original: str
    optimized: str
    improvements: List[str]
    expected_impact: str


@dataclass
class Example:
    input: str
    output: str


@dataclass
class ABTestResult:
    winner: str
    confidence: float
    metrics: Dict[str, float]


class ABTester:
    def compare_prompts(self, a: str, b: str, examples: List[Example]) -> ABTestResult:
        score_a = len(a) + (20 if "步骤" in a else 0)
        score_b = len(b) + (20 if "步骤" in b else 0)
        winner = "A" if score_a >= score_b else "B"
        confidence = abs(score_a - score_b) / max(score_a, score_b, 1)
        return ABTestResult(winner=winner, confidence=confidence, metrics={"score_a": score_a, "score_b": score_b})


class FewShotOptimizer:
    def generate_few_shot_prompt(self, task: str, examples: List[Example], query: str) -> str:
        lines = [f"任务: {task}", "", "示例:"]
        for i, ex in enumerate(examples, 1):
            lines.append(f"{i}. 输入: {ex.input}")
            lines.append(f"   输出: {ex.output}")
        lines.extend(["", "现在轮到你:", f"输入: {query}", "输出:"])
        return "\n".join(lines)


class PromptEngineer:
    def __init__(self) -> None:
        self.ab_tester = ABTester()
        self.few_shot_optimizer = FewShotOptimizer()

    def optimize_prompt(self, prompt: str, task_type: str = "general") -> PromptOptimization:
        improvements = ["补充目标与约束", "明确输出格式", "加入步骤要求"]
        optimized = (
            f"请完成以下任务（类型: {task_type}）。\n"
            f"要求: 1) 分步骤 2) 给出结论 3) 必要时给出示例。\n"
            f"任务: {prompt}"
        )
        return PromptOptimization(
            original=prompt,
            optimized=optimized,
            improvements=improvements,
            expected_impact="提高可读性与可执行性",
        )


def check_prompt_safety(prompt: str) -> SafetyResult:
    issues = []
    lowered = prompt.lower()
    if "ignore previous" in lowered or "忽略之前" in prompt:
        issues.append("存在提示注入迹象")
    if re.search(r"\bpassword\b|密钥|token", prompt, re.I):
        issues.append("包含可能的敏感信息")
    level = SafetyLevel.SAFE if not issues else SafetyLevel.WARNING
    suggestions = ["避免提示注入", "不要包含敏感信息"] if issues else ["内容安全"]
    return SafetyResult(level=level, issues=issues, suggestions=suggestions)


if __name__ == "__main__":
    print("26-prompt-engineer engine ready")