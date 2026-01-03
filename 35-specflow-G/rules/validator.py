"""
SpecFlow 需求验证器
基于预定义规则验证需求质量,类似代码Linter
"""

import re
from typing import List, Dict, Tuple
from core.models import (
    UserStory, RequirementItem, ValidationIssue,
    Severity, ValidationStatus, TestabilityLevel
)
from .knowledge_base import TESTABILITY_RULES, TESTABILITY_THRESHOLDS, CONFLICT_RULES


class RequirementValidator:
    """需求验证器(需求Linter)"""

    def __init__(self):
        self.rules = TESTABILITY_RULES
        self.conflict_rules = CONFLICT_RULES

    def validate_requirement(self, requirement: RequirementItem) -> Tuple[float, List[ValidationIssue]]:
        """
        验证单个需求
        返回: (可测试性评分, 问题列表)
        """
        score = 100.0
        issues = []

        # 规则1: 模糊词汇检测
        fuzzy_issues, deduction = self._check_fuzzy_words(requirement.description)
        score -= deduction
        issues.extend(fuzzy_issues)

        # 规则2: 验收标准检查
        if not requirement.user_stories or len(requirement.user_stories) == 0:
            issues.append(ValidationIssue(
                rule_id="T002",
                severity=Severity.CRITICAL,
                description="需求缺少用户故事",
                location=f"需求 {requirement.id}",
                suggestion="为需求添加至少1个用户故事"
            ))
            score -= 20

        # 规则3: 不可观测行为检测
        observable_issues, deduction = self._check_observable_behavior(requirement.description)
        score -= deduction
        issues.extend(observable_issues)

        # 规则4 & 5: 外部依赖和时间依赖识别
        dependency_issues = self._check_dependencies(requirement.description)
        issues.extend(dependency_issues)

        # ========== 新增质量验证规则 ==========

        # 规则6: 需求描述完整性检查(5W1H)
        completeness_issues, comp_deduction = self._check_completeness(requirement)
        score -= comp_deduction
        issues.extend(completeness_issues)

        # 规则7: 需求可量化检查
        quantifiable_issues, quant_deduction = self._check_quantifiable(requirement.description)
        score -= quant_deduction
        issues.extend(quantifiable_issues)

        # 规则8: 优先级合理性检查
        priority_issues = self._check_priority_rationality(requirement)
        issues.extend(priority_issues)

        return max(0, score), issues

    def _check_completeness(self, requirement: RequirementItem) -> Tuple[List[ValidationIssue], float]:
        """
        检查需求描述完整性(5W1H原则)
        - Who: 谁使用
        - What: 做什么
        - Why: 为什么(业务价值)
        - When: 什么时候
        - Where: 在哪里
        - How: 怎么做
        """
        issues = []
        deduction = 0
        desc = requirement.description + " " + requirement.title

        # Who: 检查是否明确用户角色
        who_keywords = ["用户", "管理员", "客户", "访客", "操作员"]
        if not any(keyword in desc for keyword in who_keywords):
            issues.append(ValidationIssue(
                rule_id="COMP-WHO",
                severity=Severity.MEDIUM,
                description="需求未明确用户角色(缺少Who)",
                location=f"需求 {requirement.id}",
                suggestion="明确说明哪类用户使用此功能"
            ))
            deduction += 5

        # What & How: 检查是否有动作描述
        action_keywords = ["查看", "创建", "编辑", "删除", "搜索", "导出", "导入", "审核"]
        if not any(keyword in desc for keyword in action_keywords):
            issues.append(ValidationIssue(
                rule_id="COMP-WHAT",
                severity=Severity.HIGH,
                description="需求未明确具体功能(缺少What)",
                location=f"需求 {requirement.id}",
                suggestion="使用动词明确描述具体功能"
            ))
            deduction += 10

        # 检查需求长度(太短可能不完整)
        if len(desc) < 20:
            issues.append(ValidationIssue(
                rule_id="COMP-LENGTH",
                severity=Severity.MEDIUM,
                description="需求描述过于简短",
                location=f"需求 {requirement.id}",
                suggestion="补充需求详情,至少包含20个字符"
            ))
            deduction += 5

        return issues, min(deduction, 20)

    def _check_quantifiable(self, text: str) -> Tuple[List[ValidationIssue], float]:
        """
        检查需求是否可量化
        如果使用性能/质量相关词汇,必须有具体指标
        """
        issues = []
        deduction = 0

        performance_keywords = {
            "快速": "指定具体响应时间(如: <200ms)",
            "高性能": "定义性能指标(如: QPS>1000)",
            "稳定": "定义可用性指标(如: 99.9%)",
            "准确": "定义准确率(如: >95%)",
            "及时": "定义时间窗口(如: <5秒)"
        }

        for keyword, suggestion in performance_keywords.items():
            if keyword in text:
                # 检查是否有数字指标
                has_metric = any(char in text for char in ["<", ">", "%", "秒", "ms", "QPS"])
                if not has_metric:
                    issues.append(ValidationIssue(
                        rule_id="QUANT-001",
                        severity=Severity.HIGH,
                        description=f"'{keyword}' 缺少可量化指标",
                        location="需求描述",
                        suggestion=suggestion
                    ))
                    deduction += 10

        return issues, min(deduction, 30)

    def _check_priority_rationality(self, requirement: RequirementItem) -> List[ValidationIssue]:
        """
        检查优先级合理性
        - Critical需求应该有详细描述
        - Low优先级需求不应该标记为"必须"
        """
        issues = []
        desc = requirement.description + " " + requirement.title

        # Critical需求必须有充分说明
        if requirement.priority.value == "Critical" and len(desc) < 30:
            issues.append(ValidationIssue(
                rule_id="PRI-001",
                severity=Severity.MEDIUM,
                description="Critical优先级需求描述过于简单",
                location=f"需求 {requirement.id}",
                suggestion="Critical需求应包含详细的业务背景和价值说明"
            ))

        # Low优先级需求不应该使用强制性词汇
        if requirement.priority.value == "Low":
            mandatory_keywords = ["必须", "一定要", "务必", "强制"]
            if any(keyword in desc for keyword in mandatory_keywords):
                issues.append(ValidationIssue(
                    rule_id="PRI-002",
                    severity=Severity.LOW,
                    description="Low优先级需求使用了强制性词汇",
                    location=f"需求 {requirement.id}",
                    suggestion="检查优先级是否应该提升,或移除强制性表述"
                ))

        return issues

    def validate_user_stories(self, user_stories: List[UserStory]) -> Tuple[float, List[ValidationIssue]]:
        """
        验证用户故事列表
        返回: (平均可测试性评分, 问题列表)
        """
        total_score = 0
        all_issues = []

        for story in user_stories:
            score, issues = self.validate_user_story(story)
            total_score += score
            all_issues.extend(issues)

        avg_score = total_score / len(user_stories) if user_stories else 0
        return avg_score, all_issues

    def validate_user_story(self, story: UserStory) -> Tuple[float, List[ValidationIssue]]:
        """
        验证单个用户故事
        检查: As a... I want... So that... 格式 + INVEST原则
        """
        score = 100.0
        issues = []

        # 检查三段式格式
        if not story.as_a or not story.i_want or not story.so_that:
            issues.append(ValidationIssue(
                rule_id="US001",
                severity=Severity.CRITICAL,
                description="用户故事格式不完整",
                location=f"故事 {story.id}",
                suggestion="使用 'As a... I want... So that...' 格式"
            ))
            score -= 30

        # 检查验收标准
        if not story.acceptance_criteria or len(story.acceptance_criteria) < 2:
            issues.append(ValidationIssue(
                rule_id="US002",
                severity=Severity.HIGH,
                description="验收标准不足",
                location=f"故事 {story.id}",
                suggestion="至少添加2条验收标准"
            ))
            score -= 20

        # 检查模糊词汇
        combined_text = f"{story.i_want} {story.so_that}"
        fuzzy_issues, deduction = self._check_fuzzy_words(combined_text)
        score -= deduction
        issues.extend(fuzzy_issues)

        # ========== INVEST原则检查 ==========
        invest_issues, invest_deduction = self._check_invest_principles(story)
        score -= invest_deduction
        issues.extend(invest_issues)

        return max(0, score), issues

    def _check_invest_principles(self, story: UserStory) -> Tuple[List[ValidationIssue], float]:
        """
        检查INVEST原则
        - I: Independent (独立性)
        - N: Negotiable (可协商)
        - V: Valuable (有价值)
        - E: Estimable (可估算)
        - S: Small (小)
        - T: Testable (可测试)
        """
        issues = []
        deduction = 0

        # I - Independent: 检查是否有依赖关键词
        dependency_keywords = ["依赖", "必须先", "需要先", "前提是", "基于"]
        story_text = f"{story.i_want} {story.so_that}"
        if any(keyword in story_text for keyword in dependency_keywords):
            issues.append(ValidationIssue(
                rule_id="INVEST-I",
                severity=Severity.MEDIUM,
                description="故事可能存在依赖性(违反Independent原则)",
                location=f"故事 {story.id}",
                suggestion="尽量减少故事间的依赖,确保可独立开发和测试"
            ))
            deduction += 5

        # N - Negotiable: 检查是否过于具体(技术实现细节)
        tech_keywords = ["使用MySQL", "用Redis", "调用API", "写SQL", "用框架"]
        if any(keyword in story_text for keyword in tech_keywords):
            issues.append(ValidationIssue(
                rule_id="INVEST-N",
                severity=Severity.LOW,
                description="故事包含技术实现细节(违反Negotiable原则)",
                location=f"故事 {story.id}",
                suggestion="聚焦用户价值,避免限定技术实现细节"
            ))
            deduction += 3

        # V - Valuable: 检查是否明确价值
        if not story.so_that or len(story.so_that) < 5:
            issues.append(ValidationIssue(
                rule_id="INVEST-V",
                severity=Severity.HIGH,
                description="故事价值不明确(违反Valuable原则)",
                location=f"故事 {story.id}",
                suggestion="在'以便'部分明确说明业务价值或用户收益"
            ))
            deduction += 10

        # E - Estimable: 检查是否可估算(长度和复杂度)
        word_count = len(story.i_want)
        if word_count > 100:
            issues.append(ValidationIssue(
                rule_id="INVEST-E",
                severity=Severity.MEDIUM,
                description="故事描述过长,可能难以估算(违反Estimable原则)",
                location=f"故事 {story.id}",
                suggestion="简化故事描述,或拆分为多个小故事"
            ))
            deduction += 5

        # S - Small: 检查是否足够小(通过关键词)
        large_scope_keywords = ["完整的", "所有的", "全部", "整个系统", "端到端"]
        if any(keyword in story_text for keyword in large_scope_keywords):
            issues.append(ValidationIssue(
                rule_id="INVEST-S",
                severity=Severity.HIGH,
                description="故事范围过大(违反Small原则)",
                location=f"故事 {story.id}",
                suggestion="将大故事拆分为多个可在1-2天内完成的小故事"
            ))
            deduction += 10

        # T - Testable: 检查验收标准的可测试性
        testable_keywords = ["可以", "能够", "应该", "显示", "返回", "成功", "失败"]
        if story.acceptance_criteria:
            testable_count = sum(
                1 for ac in story.acceptance_criteria
                if any(keyword in ac for keyword in testable_keywords)
            )
            if testable_count < len(story.acceptance_criteria) * 0.5:
                issues.append(ValidationIssue(
                    rule_id="INVEST-T",
                    severity=Severity.HIGH,
                    description="验收标准可测试性不足(违反Testable原则)",
                    location=f"故事 {story.id}",
                    suggestion="使用Given-When-Then格式,明确可验证的预期结果"
                ))
                deduction += 10

        return issues, min(deduction, 30)  # 最多扣30分

    def check_conflicts(self, requirements: List[RequirementItem]) -> List[ValidationIssue]:
        """检测需求冲突"""
        issues = []
        all_text = " ".join([req.description for req in requirements])

        for rule in self.conflict_rules:
            # 检查是否触发规则
            has_trigger = any(keyword in all_text for keyword in rule["trigger_keywords"])
            if has_trigger:
                # 检查是否有必需的关键词
                has_required = any(keyword in all_text for keyword in rule["required_keywords"])
                if not has_required:
                    issues.append(ValidationIssue(
                        rule_id=rule["id"],
                        severity=Severity[rule["severity"]],
                        description=rule["name"],
                        location="需求集合",
                        suggestion=rule["suggestion"]
                    ))

        return issues

    def _check_fuzzy_words(self, text: str) -> Tuple[List[ValidationIssue], float]:
        """检测模糊词汇"""
        fuzzy_keywords = ["可能", "尽量", "基本上", "大概", "差不多", "应该", "大约", "优化", "改善", "提升"]
        issues = []
        deduction = 0

        for keyword in fuzzy_keywords:
            if keyword in text:
                issues.append(ValidationIssue(
                    rule_id="T001",
                    severity=Severity.HIGH,
                    description=f"发现模糊词汇: '{keyword}'",
                    location="需求描述",
                    suggestion=f"使用明确的量化指标替代 '{keyword}'"
                ))
                deduction += 10

        return issues, min(deduction, 30)  # 最多扣30分

    def _check_observable_behavior(self, text: str) -> Tuple[List[ValidationIssue], float]:
        """检测不可观测行为"""
        vague_words = ["优化", "改善", "提升", "增强"]
        issues = []
        deduction = 0

        for word in vague_words:
            if word in text and not any(metric in text for metric in ["<", ">", "%", "毫秒", "秒", "分钟"]):
                issues.append(ValidationIssue(
                    rule_id="T003",
                    severity=Severity.HIGH,
                    description=f"'{word}' 缺少可量化指标",
                    location="需求描述",
                    suggestion=f"为 '{word}' 添加具体指标(如: 响应时间<100ms)"
                ))
                deduction += 15

        return issues, min(deduction, 30)

    def _check_dependencies(self, text: str) -> List[ValidationIssue]:
        """检测外部依赖和时间依赖"""
        issues = []

        # 外部依赖
        external_keywords = ["第三方", "API", "接口", "对接", "集成"]
        if any(keyword in text for keyword in external_keywords):
            issues.append(ValidationIssue(
                rule_id="T004",
                severity=Severity.MEDIUM,
                description="检测到外部依赖",
                location="需求描述",
                suggestion="考虑使用Mock对象进行单元测试"
            ))

        # 时间依赖
        time_keywords = ["定时", "每天", "每周", "每月", "延迟", "超时"]
        if any(keyword in text for keyword in time_keywords):
            issues.append(ValidationIssue(
                rule_id="T005",
                severity=Severity.MEDIUM,
                description="检测到时间依赖",
                location="需求描述",
                suggestion="使用时间Mock确保测试稳定性"
            ))

        return issues


def validate_user_story_format(story_text: str) -> bool:
    """
    快速验证用户故事格式
    返回: True表示格式正确
    """
    # 检查是否包含 "作为","我想","以便" 等关键词
    patterns = [
        r"作为.*我想.*以便",
        r"As a.*I want.*So that",
    ]

    for pattern in patterns:
        if re.search(pattern, story_text, re.IGNORECASE):
            return True

    return False


def calculate_testability_score(issues: List[ValidationIssue]) -> Tuple[float, TestabilityLevel]:
    """
    计算可测试性评分和级别
    """
    # 基础分100分
    score = 100.0

    # 根据问题严重程度扣分
    for issue in issues:
        if issue.severity == Severity.CRITICAL:
            score -= 20
        elif issue.severity == Severity.HIGH:
            score -= 10
        elif issue.severity == Severity.MEDIUM:
            score -= 5
        else:
            score -= 2

    score = max(0, score)

    # 确定级别
    level = TestabilityLevel.POOR
    for test_level, (min_score, max_score) in TESTABILITY_THRESHOLDS.items():
        if min_score <= score <= max_score:
            level = test_level
            break

    return score, level


def generate_validation_report(requirements: List[RequirementItem]) -> Dict[str, any]:
    """生成完整的验证报告"""
    validator = RequirementValidator()

    total_score = 0
    all_issues = []

    for req in requirements:
        score, issues = validator.validate_requirement(req)
        total_score += score
        all_issues.extend(issues)

    avg_score = total_score / len(requirements) if requirements else 0
    _, level = calculate_testability_score(all_issues)

    # 检测冲突
    conflict_issues = validator.check_conflicts(requirements)
    all_issues.extend(conflict_issues)

    # 统计问题
    critical_count = sum(1 for issue in all_issues if issue.severity == Severity.CRITICAL)
    high_count = sum(1 for issue in all_issues if issue.severity == Severity.HIGH)
    medium_count = sum(1 for issue in all_issues if issue.severity == Severity.MEDIUM)
    low_count = sum(1 for issue in all_issues if issue.severity == Severity.LOW)

    status = ValidationStatus.PASSED
    if critical_count > 0:
        status = ValidationStatus.FAILED
    elif high_count > 3:
        status = ValidationStatus.WARNING

    return {
        "status": status,
        "testability_score": avg_score,
        "testability_level": level,
        "total_issues": len(all_issues),
        "issues_by_severity": {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count
        },
        "issues": all_issues,
        "summary": f"可测试性评分: {avg_score:.1f}/100 ({level.value})"
    }
