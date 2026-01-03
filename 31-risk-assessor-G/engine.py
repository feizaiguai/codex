"""31-risk-assessor 引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    SECURITY = "security"
    DEPENDENCY = "dependency"
    COMPLEXITY = "complexity"
    COMPLIANCE = "compliance"


@dataclass
class Risk:
    category: RiskCategory
    level: RiskLevel
    description: str
    score: int


@dataclass
class RiskAssessment:
    project_name: str
    overall_risk_score: int
    summary: str
    risks: List[Risk]


class RiskAssessor:
    def assess(self, project_name: str, metrics: Dict[str, Any], deps: List[str], compliance: List[str]) -> RiskAssessment:
        risks: List[Risk] = []
        score = 0

        complexity = float(metrics.get("complexity", 0)) if metrics else 0.0
        if complexity >= 15:
            risks.append(Risk(RiskCategory.COMPLEXITY, RiskLevel.HIGH, "复杂度偏高", 20))
            score += 20
        elif complexity >= 10:
            risks.append(Risk(RiskCategory.COMPLEXITY, RiskLevel.MEDIUM, "复杂度偏高", 10))
            score += 10

        vuln_count = int(metrics.get("vulns", 0)) if metrics else 0
        if vuln_count > 0:
            risks.append(Risk(RiskCategory.SECURITY, RiskLevel.HIGH, f"检测到 {vuln_count} 个漏洞", 25))
            score += 25

        for dep in deps:
            if "alpha" in dep or "beta" in dep:
                risks.append(Risk(RiskCategory.DEPENDENCY, RiskLevel.MEDIUM, f"依赖版本不稳定: {dep}", 8))
                score += 8

        if compliance:
            missing = [c for c in compliance if c not in ["GDPR", "SOC2", "HIPAA"]]
            if missing:
                risks.append(Risk(RiskCategory.COMPLIANCE, RiskLevel.MEDIUM, f"未知合规标准: {', '.join(missing)}", 5))
                score += 5

        overall = min(100, score)
        summary = "无显著风险" if not risks else f"发现 {len(risks)} 个风险项"
        return RiskAssessment(project_name=project_name, overall_risk_score=overall, summary=summary, risks=risks)

    def generate_report(self, assessment: RiskAssessment) -> str:
        lines = [
            f"# 风险评估报告 - {assessment.project_name}",
            "",
            f"总体风险评分: {assessment.overall_risk_score}",
            f"摘要: {assessment.summary}",
            "",
            "## 风险项",
        ]
        if not assessment.risks:
            lines.append("- 未发现高风险项")
        else:
            for r in assessment.risks:
                lines.append(f"- [{r.level}] {r.category}: {r.description} (score {r.score})")
        return "\n".join(lines)


if __name__ == "__main__":
    print("31-risk-assessor engine ready")
