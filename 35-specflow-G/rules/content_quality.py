"""
内容质量检查模块 - Quality V5.0
检测占位符,泛化描述,空验收标准等内容质量问题

设计: Claude + Gemini 联合设计
版本: V5.0
日期: 2025-12-21
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """验证结果"""
    passed: bool
    score: float  # 0-100
    message: str
    severity: str  # INFO, WARNING, CRITICAL
    details: List[str] = None

    def __post_init__(self):
        if self.details is None:
            self.details = []


class PlaceholderValidator:
    """占位符和垃圾词检测器(P0 - 一级熔断)"""

    # 黑名单词库(中英文)
    # Gemini优化:移除高频中性词(相关,有关,某个)以降低误判率
    BLOCKLIST = [
        # 中文占位符
        "待定", "待明确", "待定义", "待识别", "待补充", "待完善",
        # 英文占位符
        "TBD", "TODO", "FIXME", "XXX", "placeholder",
        # 通用占位符
        "XX", "占位符", "填写这里", "填写", "示例", "模板",
        # 泛化描述
        "Generic", "默认", "系统就绪", "默认操作",
        "达成业务目标", "完成操作", "提升效率", "优化体验",
        "提高性能", "增强功能", "改进", "完善",
        # 空洞词汇(已移除"相关","有关","某个")
        "一些", "相应",
    ]

    # 占位符模式(正则表达式)
    PLACEHOLDER_PATTERNS = [
        r'\[.*?\]',  # [填写内容]
        r'<.*?>',    # <待补充>
        r'\{.*?\}',  # {placeholder}
        r'___+',     # ______
        r'\.\.\.+',  # ...
    ]

    def __init__(self, junk_threshold: float = 0.2):
        """
        初始化占位符验证器

        Args:
            junk_threshold: 垃圾词密度阈值(默认20%)
        """
        self.junk_threshold = junk_threshold
        self.compiled_patterns = [re.compile(p) for p in self.PLACEHOLDER_PATTERNS]

    def validate(self, spec_model: Dict) -> ValidationResult:
        """
        验证文档的占位符密度

        Args:
            spec_model: 规格模型(包含用户故事,BDD场景等)

        Returns:
            ValidationResult: 验证结果
        """
        # 提取所有文本内容
        all_text = self._extract_all_text(spec_model)

        if len(all_text) < 50:
            return ValidationResult(
                passed=False,
                score=0,
                message="严重质量问题:文档内容过少(< 50字符)",
                severity="CRITICAL",
                details=["文档总字符数: {}".format(len(all_text))]
            )

        # 计算垃圾词密度
        junk_density, junk_details = self._calculate_junk_density(all_text)

        # 一级熔断:垃圾词密度过高
        if junk_density > self.junk_threshold:
            return ValidationResult(
                passed=False,
                score=0,
                message=f"严重质量问题:文档包含大量占位符或未完成内容(垃圾词密度{junk_density:.1%})",
                severity="CRITICAL",
                details=junk_details
            )

        # 计算得分(线性扣分)
        # 垃圾词密度0% → 100分,20% → 0分
        score = max(0, 100 - (junk_density / self.junk_threshold * 100))

        severity = "INFO"
        if junk_density > 0.1:
            severity = "WARNING"

        return ValidationResult(
            passed=True,
            score=score,
            message=f"信息实质度: {score:.1f}/100(垃圾词密度{junk_density:.1%})",
            severity=severity,
            details=junk_details if junk_density > 0 else []
        )

    def _extract_all_text(self, spec_model: Dict) -> str:
        """提取规格模型中的所有文本"""
        texts = []

        # 提取项目基本信息
        if 'meta' in spec_model:
            meta = spec_model['meta']
            texts.append(meta.get('project_name', ''))
            texts.append(meta.get('description', ''))

        # 提取用户故事
        if 'spec_model' in spec_model:
            spec = spec_model['spec_model']

            # 用户故事
            if 'flow_modeling' in spec and 'user_stories' in spec['flow_modeling']:
                for story in spec['flow_modeling']['user_stories']:
                    texts.append(story.get('role', ''))
                    texts.append(story.get('action', ''))
                    texts.append(story.get('goal', ''))
                    texts.append(story.get('acceptance_criteria', ''))

            # BDD场景
            if 'bdd_scenarios' in spec:
                for scenario in spec['bdd_scenarios']:
                    texts.append(scenario.get('feature', ''))
                    texts.append(scenario.get('scenario', ''))
                    texts.extend(scenario.get('given', []))
                    texts.extend(scenario.get('when', []))
                    texts.extend(scenario.get('then', []))

        return ' '.join(filter(None, texts))

    def _calculate_junk_density(self, text: str) -> Tuple[float, List[str]]:
        """
        计算垃圾词密度

        Args:
            text: 文本内容

        Returns:
            (密度, 详情列表)
        """
        total_length = len(text)
        if total_length == 0:
            return 1.0, ["文档为空"]

        junk_count = 0
        details = []

        # 1. 检查黑名单词
        for word in self.BLOCKLIST:
            count = text.count(word)
            if count > 0:
                junk_count += count * len(word) * 5  # 赋予5倍权重
                details.append(f"检测到'{word}': {count}次")

        # 2. 检查占位符模式
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text)
            if matches:
                junk_count += sum(len(m) for m in matches) * 3  # 赋予3倍权重
                details.append(f"检测到占位符模式: {len(matches)}个")

        # 计算密度
        junk_density = junk_count / total_length

        return junk_density, details


class GenericStepDetector:
    """泛化描述检测器(P1)- 检测BDD场景的泛化程度"""

    # 泛化模式(中英文)
    GENERIC_PATTERNS = [
        # Given模式
        r"Given\s+系统.*正常",
        r"Given\s+.*就绪",
        r"Given\s+.*准备好",
        r"Given\s+system\s+is\s+ready",
        r"Given\s+.*is\s+available",
        # When模式
        r"When\s+用户.*操作",
        r"When\s+.*提交.*请求",
        r"When\s+.*执行",
        r"When\s+user\s+does\s+something",
        r"When\s+.*performs\s+action",
        # Then模式
        r"Then\s+.*成功",
        r"Then\s+系统.*完成",
        r"Then\s+.*正确",
        r"Then\s+success",
        r"Then\s+system\s+completes",
    ]

    # 最小步骤长度
    MIN_STEP_LENGTH = 10

    def __init__(self, generic_threshold: float = 0.3):
        """
        初始化泛化检测器

        Args:
            generic_threshold: 泛化步骤占比阈值(默认30%)
        """
        self.generic_threshold = generic_threshold
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.GENERIC_PATTERNS]

    def detect(self, bdd_scenarios: List[Dict]) -> ValidationResult:
        """
        检测BDD场景的泛化程度

        Args:
            bdd_scenarios: BDD场景列表

        Returns:
            ValidationResult: 检测结果
        """
        if not bdd_scenarios:
            return ValidationResult(
                passed=False,
                score=0,
                message="缺少BDD场景",
                severity="CRITICAL"
            )

        total_steps = 0
        generic_steps = 0
        details = []

        for scenario in bdd_scenarios:
            # 合并所有步骤
            all_steps = []
            all_steps.extend(scenario.get('given', []))
            all_steps.extend(scenario.get('when', []))
            all_steps.extend(scenario.get('then', []))

            for step in all_steps:
                total_steps += 1

                # 检查1: 步骤长度过短
                if len(step) < self.MIN_STEP_LENGTH:
                    generic_steps += 1
                    details.append(f"步骤过短: '{step}' (长度{len(step)})")
                    continue

                # 检查2: 命中泛化模式
                for pattern in self.compiled_patterns:
                    if pattern.search(step):
                        generic_steps += 1
                        details.append(f"泛化步骤: '{step}'")
                        break

        # 计算泛化比例
        generic_ratio = generic_steps / total_steps if total_steps > 0 else 1.0

        # 计算得分
        if generic_ratio > self.generic_threshold:
            score = max(0, 100 - (generic_ratio / self.generic_threshold * 100))
            passed = False
            severity = "CRITICAL"
            message = f"BDD场景过于泛化({generic_ratio:.1%}的步骤为模板化描述)"
        else:
            score = 100 - (generic_ratio * 200)  # 线性扣分
            passed = True
            severity = "WARNING" if generic_ratio > 0.1 else "INFO"
            message = f"规格具体性: {score:.1f}/100(泛化步骤{generic_ratio:.1%})"

        return ValidationResult(
            passed=passed,
            score=score,
            message=message,
            severity=severity,
            details=details[:10]  # 只显示前10个示例
        )


class EmptyACValidator:
    """空验收标准检测器(P1)- 检测验收标准的完整性"""

    # 空值标记
    EMPTY_MARKERS = ["无", "略", "同上", "待补充", "N/A", "None", ""]

    def __init__(self, empty_threshold: float = 0.2):
        """
        初始化验收标准检测器

        Args:
            empty_threshold: 空验收标准占比阈值(默认20%)
        """
        self.empty_threshold = empty_threshold

    def validate(self, user_stories: List[Dict]) -> ValidationResult:
        """
        验证用户故事的验收标准完整性

        Args:
            user_stories: 用户故事列表

        Returns:
            ValidationResult: 验证结果
        """
        if not user_stories:
            return ValidationResult(
                passed=False,
                score=0,
                message="缺少用户故事",
                severity="CRITICAL"
            )

        total_stories = len(user_stories)
        empty_count = 0
        incomplete_count = 0
        details = []

        for i, story in enumerate(user_stories, 1):
            ac = story.get('acceptance_criteria', '')

            # 检查1: 验收标准为空
            if not ac or ac.strip() in self.EMPTY_MARKERS:
                empty_count += 1
                story_id = story.get('id', f'US-{i:03d}')
                details.append(f"{story_id}: 验收标准为空")
                continue

            # 检查2: 验收标准包含占位符
            if any(marker in ac for marker in ["待定", "TBD", "TODO"]):
                incomplete_count += 1
                story_id = story.get('id', f'US-{i:03d}')
                details.append(f"{story_id}: 验收标准不完整(包含占位符)")

        # 计算空验收标准比例
        empty_ratio = empty_count / total_stories
        total_issue_ratio = (empty_count + incomplete_count) / total_stories

        # 一级熔断:全部为空
        if empty_ratio == 1.0:
            return ValidationResult(
                passed=False,
                score=0,
                message=f"严重质量问题:验收标准缺失({total_stories}个用户故事全部缺少验收标准)",
                severity="CRITICAL",
                details=details
            )

        # 二级熔断:超过阈值
        if total_issue_ratio > self.empty_threshold:
            score = max(0, 100 - (total_issue_ratio / self.empty_threshold * 100))
            return ValidationResult(
                passed=False,
                score=score,
                message=f"验证覆盖度不足: {empty_count}个用户故事缺少验收标准,{incomplete_count}个不完整",
                severity="CRITICAL",
                details=details
            )

        # 计算得分
        score = 100 - (total_issue_ratio * 300)  # 线性扣分,有问题扣分更重

        return ValidationResult(
            passed=True,
            score=max(0, score),
            message=f"验证覆盖度: {score:.1f}/100({empty_count}个空AC,{incomplete_count}个不完整)",
            severity="WARNING" if total_issue_ratio > 0 else "INFO",
            details=details if details else []
        )


class ContentQualityInspector:
    """内容质量综合检查器 - 整合所有检测器"""

    def __init__(self):
        self.placeholder_validator = PlaceholderValidator()
        self.generic_detector = GenericStepDetector()
        self.ac_validator = EmptyACValidator()

    def inspect(self, spec_model: Dict) -> Dict[str, ValidationResult]:
        """
        全面检查规格文档的内容质量

        Args:
            spec_model: 规格模型

        Returns:
            各检测器的结果字典
        """
        results = {}

        # 1. 占位符检测(P0 - 熔断检查)
        results['placeholder'] = self.placeholder_validator.validate(spec_model)

        # 2. BDD泛化检测(P1)
        bdd_scenarios = []
        if 'spec_model' in spec_model and 'bdd_scenarios' in spec_model['spec_model']:
            bdd_scenarios = spec_model['spec_model']['bdd_scenarios']
        results['generic_bdd'] = self.generic_detector.detect(bdd_scenarios)

        # 3. 验收标准检测(P1)
        user_stories = []
        if 'spec_model' in spec_model and 'flow_modeling' in spec_model['spec_model']:
            flow = spec_model['spec_model']['flow_modeling']
            user_stories = flow.get('user_stories', [])
        results['acceptance_criteria'] = self.ac_validator.validate(user_stories)

        return results

    def calculate_total_score(self, results: Dict[str, ValidationResult]) -> Tuple[float, str, List[str]]:
        """
        计算总体质量得分(仅计算内容质量的80%)

        Args:
            results: 各检测器结果

        Returns:
            (总分0-100, 等级, 问题列表)
        """
        # 权重配置(归一化,总和1.0)
        # 这里只计算内容质量部分(占总分80%),结构和一致性由json_loader.py处理
        weights = {
            'placeholder': 0.4375,      # 35/80 归一化
            'generic_bdd': 0.3125,      # 25/80 归一化
            'acceptance_criteria': 0.25,  # 20/80 归一化
        }

        # 检查一级熔断
        if not results['placeholder'].passed:
            return (
                min(40, results['placeholder'].score),
                'F',
                [results['placeholder'].message] + results['placeholder'].details
            )

        # 检查二级熔断(验收标准全空)
        if results['acceptance_criteria'].score == 0:
            return (
                40.0,
                'F',
                [results['acceptance_criteria'].message] + results['acceptance_criteria'].details
            )

        # 加权计算总分
        total_score = 0
        issues = []

        for key, weight in weights.items():
            result = results[key]
            total_score += result.score * weight

            if result.severity in ['CRITICAL', 'WARNING']:
                issues.append(result.message)
                issues.extend(result.details[:3])  # 每项最多3个详情

        # 映射等级
        grade = self._map_score_to_grade(total_score)

        return total_score, grade, issues

    def _map_score_to_grade(self, score: float) -> str:
        """映射分数到等级"""
        if score >= 97:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
