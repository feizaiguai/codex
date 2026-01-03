"""
SpecFlow 规则引擎
基于关键词匹配的需求分析引擎(诚实版本,不再假装是AI)

核心功能:
- 领域识别(关键词匹配)
- 复杂度评估(规则计算)
- 需求提取(模板填充)
- 质量评分(规则验证)
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from core.models import (
    DomainCategory, ComplexityLevel, Priority,
    UserStory, RequirementItem, RequirementType,
    QualityReport, QualityMetrics, QualityGrade,
    ValidationIssue, Severity
)

from .knowledge_base import (
    DOMAIN_KEYWORDS,
    COMPLEXITY_PATTERNS,
    REQUIREMENT_PATTERNS,
    EFFORT_BASELINE,
    BDD_TEMPLATES,
    QUALITY_WEIGHTS,
)

from .validator import RequirementValidator, calculate_testability_score


class RulesEngine:
    """
    规则引擎(替代AIRequirementsAgent)

    核心理念: 确定性,可预测,无幻觉
    """

    def __init__(self):
        self.validator = RequirementValidator()

    def analyze_description(
        self,
        description: str,
        budget: Optional[float] = None,
        timeline_months: Optional[int] = None
    ) -> QualityReport:
        """
        分析需求描述(规则驱动,非AI)

        步骤:
        1. 关键词匹配识别领域
        2. 规则计算复杂度
        3. 提取需求和生成用户故事
        4. 验证质量并评分
        """

        # 1. 领域识别(关键词匹配)
        domain = self._detect_domain(description)

        # 2. 复杂度评估(规则计算)
        complexity = self._calculate_complexity(description, budget, timeline_months)

        # 3. 工时估算
        estimated_hours = self._estimate_hours(complexity, description)

        # 4. 提取需求
        requirements = self._extract_requirements(description, domain)

        # 5. 质量验证
        validation_issues = []
        for req in requirements:
            _, issues = self.validator.validate_requirement(req)
            validation_issues.extend(issues)

        # 6. 计算质量指标
        metrics = self._calculate_quality_metrics(requirements, validation_issues)

        # 7. 生成建议
        recommendations = self._generate_recommendations(domain, complexity, validation_issues)

        return QualityReport(
            domain=domain,
            complexity=complexity,
            estimated_hours=estimated_hours,
            metrics=metrics,
            validation_issues=validation_issues,
            recommendations=recommendations,
            validated_at=datetime.now().isoformat()
        )

    def _detect_domain(self, description: str) -> DomainCategory:
        """
        领域检测(关键词匹配,非AI)

        算法: 统计每个领域的关键词出现次数,选择最多的
        """
        domain_scores = {}

        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in description)
            domain_scores[domain] = score

        # 返回得分最高的领域
        if max(domain_scores.values()) > 0:
            return max(domain_scores, key=domain_scores.get)
        else:
            return DomainCategory.OTHER

    def _calculate_complexity(
        self,
        description: str,
        budget: Optional[float],
        timeline_months: Optional[int]
    ) -> ComplexityLevel:
        """
        复杂度计算(规则驱动,非AI估算)

        评分规则:
        - 关键词匹配: 每个复杂度关键词加分
        - 长度: 描述越长,复杂度越高
        - 预算: 预算越高,项目越复杂
        - 时间: 时间越长,项目越复杂
        """
        complexity_score = 0

        # 1. 关键词评分
        for keyword, score in COMPLEXITY_PATTERNS.items():
            if keyword in description:
                complexity_score += score

        # 2. 描述长度评分(每100字+5分)
        complexity_score += len(description) // 100 * 5

        # 3. 预算评分(如果提供)
        if budget:
            if budget > 1000000:  # 100万以上
                complexity_score += 30
            elif budget > 500000:  # 50万以上
                complexity_score += 20
            elif budget > 100000:  # 10万以上
                complexity_score += 10

        # 4. 时间评分(如果提供)
        if timeline_months:
            if timeline_months > 12:
                complexity_score += 25
            elif timeline_months > 6:
                complexity_score += 15
            elif timeline_months > 3:
                complexity_score += 10

        # 5. 根据评分确定级别
        if complexity_score <= 20:
            return ComplexityLevel.SIMPLE
        elif complexity_score <= 50:
            return ComplexityLevel.MEDIUM
        elif complexity_score <= 100:
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.VERY_COMPLEX

    def _estimate_hours(self, complexity: ComplexityLevel, description: str) -> int:
        """
        工时估算(基于历史数据的经验公式,非AI预测)
        """
        # 基础工时
        base_hours = EFFORT_BASELINE.get(complexity.name, 160)

        # 根据关键组件调整
        adjustment = 0
        if "UI" in description or "界面" in description:
            adjustment += 40
        if "API" in description or "接口" in description:
            adjustment += 60
        if "数据库" in description:
            adjustment += 40
        if "集成" in description or "对接" in description:
            adjustment += 80

        return int(base_hours + adjustment)

    def _extract_requirements(
        self,
        description: str,
        domain: DomainCategory
    ) -> List[RequirementItem]:
        """
        需求提取(模板匹配,非AI生成)

        算法: 在描述中搜索预定义的需求模式关键词
        """
        requirements = []
        req_id_counter = 1

        for keyword, template in REQUIREMENT_PATTERNS.items():
            if keyword in description:
                # 生成需求项
                req = RequirementItem(
                    id=f"REQ-{req_id_counter:03d}",
                    title=f"{keyword}功能",
                    description=f"系统需要提供{keyword}功能",
                    type=RequirementType.FUNCTIONAL,
                    priority=Priority.HIGH,
                    user_stories=self._generate_user_stories_from_template(
                        template, req_id_counter
                    ),
                    estimated_hours=16,  # 默认2个工作日
                    tags=[template["category"], domain.value]
                )
                requirements.append(req)
                req_id_counter += 1

        # 如果没有匹配到任何模式,创建一个通用需求
        if not requirements:
            requirements.append(RequirementItem(
                id="REQ-001",
                title="核心功能",
                description=description[:100],  # 截取前100字作为描述
                type=RequirementType.FUNCTIONAL,
                priority=Priority.HIGH,
                user_stories=[],
                estimated_hours=40,
                tags=[domain.value]
            ))

        return requirements

    def _generate_user_stories_from_template(
        self,
        template: Dict,
        base_id: int
    ) -> List[UserStory]:
        """从模板生成用户故事"""
        stories = []

        for idx, story_desc in enumerate(template["user_stories"], 1):
            # 解析用户故事描述,提取三段式
            as_a, i_want, so_that = self._parse_story_description(story_desc)

            story = UserStory(
                id=f"US-{base_id:03d}-{idx}",
                as_a=as_a,
                i_want=i_want,
                so_that=so_that,
                acceptance_criteria=template.get("acceptance_criteria", [])[:3],  # 最多3条
                priority=Priority.MEDIUM,
                estimated_hours=8.0,
                tags=[template["category"]]
            )
            stories.append(story)

        return stories

    def _parse_story_description(self, description: str) -> Tuple[str, str, str]:
        """解析用户故事描述为三段式"""
        # 简单的启发式解析
        as_a = "用户"
        i_want = description
        so_that = "提升使用体验"

        return as_a, i_want, so_that

    def _calculate_quality_metrics(
        self,
        requirements: List[RequirementItem],
        issues: List[ValidationIssue]
    ) -> QualityMetrics:
        """
        计算质量指标(规则驱动)
        """
        # 完整性评分(基于需求数量)
        completeness = min(100, len(requirements) * 20)  # 每个需求20分,最多5个

        # 一致性评分(基于问题数量)
        consistency = 100 - min(100, len(issues) * 5)  # 每个问题扣5分

        # 原子性评分(基于用户故事的平均数量)
        total_stories = sum(len(req.user_stories) for req in requirements)
        avg_stories_per_req = total_stories / len(requirements) if requirements else 0
        atomicity = min(100, avg_stories_per_req * 30)  # 理想是每个需求3-4个故事

        # 可测试性评分(基于验证问题)
        testability, _ = calculate_testability_score(issues)

        # 计算总体等级
        metrics = QualityMetrics(
            completeness_score=round(completeness, 1),
            consistency_score=round(consistency, 1),
            atomicity_score=round(atomicity, 1),
            testability_score=round(testability, 1),
            overall_grade=QualityGrade.B  # 临时值
        )

        # 使用方法计算实际等级
        metrics.overall_grade = metrics.calculate_overall_grade()

        return metrics

    def _generate_recommendations(
        self,
        domain: DomainCategory,
        complexity: ComplexityLevel,
        issues: List[ValidationIssue]
    ) -> List[str]:
        """生成改进建议(规则驱动)"""
        recommendations = []

        # 基于领域的建议
        if domain == DomainCategory.E_COMMERCE:
            recommendations.append("建议集成第三方支付SDK(微信支付,支付宝)")
            recommendations.append("考虑使用Redis缓存商品信息提升性能")

        if domain == DomainCategory.FINTECH:
            recommendations.append("必须通过安全审计(符合金融行业标准)")
            recommendations.append("实施严格的数据加密和访问控制")

        # 基于复杂度的建议
        if complexity == ComplexityLevel.COMPLEX or complexity == ComplexityLevel.VERY_COMPLEX:
            recommendations.append("建议采用微服务架构,提高系统可扩展性")
            recommendations.append("需要完善的CI/CD流程和自动化测试")

        # 基于问题的建议
        critical_issues = [i for i in issues if i.severity == Severity.CRITICAL]
        if critical_issues:
            recommendations.append(f"发现{len(critical_issues)}个严重问题,必须修复后才能开发")

        # 通用建议
        recommendations.append("遵循RESTful API设计规范")
        recommendations.append("实施代码审查流程,确保代码质量")

        return recommendations


def create_rules_engine() -> RulesEngine:
    """创建规则引擎实例(工厂函数)"""
    return RulesEngine()
