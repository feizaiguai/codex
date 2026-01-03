"""
SpecFlow - 统一核心数据模型
基于规则引擎的需求工程专家系统

版本: 3.0.0(重构版)
日期: 2025-12-17

核心理念:
- 去除所有AI相关虚假概念
- 统一数据模型定义
- 基于规则的确定性输出
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


# ============================================================================
# 基础枚举类型(核心业务枚举,从13个精简到8个)
# ============================================================================

class Priority(str, Enum):
    """优先级"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Severity(str, Enum):
    """严重程度"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ComponentCategory(str, Enum):
    """组件类别"""
    FEATURE = "Feature"
    TECHNICAL = "Technical"
    INFRASTRUCTURE = "Infrastructure"


class DomainCategory(str, Enum):
    """领域分类(用于加载特定领域的规则模板)"""
    E_COMMERCE = "电商平台"
    SOCIAL = "社交网络"
    ENTERPRISE = "企业应用"
    FINTECH = "金融科技"
    EDUCATION = "教育平台"
    HEALTHCARE = "医疗健康"
    ENTERTAINMENT = "娱乐媒体"
    IOT = "物联网"
    OTHER = "其他"


class ComplexityLevel(str, Enum):
    """复杂度级别(基于规则计算,非AI估算)"""
    SIMPLE = "简单"      # < 5个用户故事
    MEDIUM = "中等"      # 5-20个用户故事
    COMPLEX = "复杂"     # 21-50个用户故事
    VERY_COMPLEX = "非常复杂"  # > 50个用户故事


class TestabilityLevel(str, Enum):
    """可测试性级别"""
    EXCELLENT = "优秀"   # 85-100分
    GOOD = "良好"        # 70-84分
    FAIR = "一般"        # 50-69分
    POOR = "较差"        # < 50分


class ValidationStatus(str, Enum):
    """验证状态"""
    PASSED = "通过"
    WARNING = "警告"
    FAILED = "失败"
    SKIPPED = "跳过"


class TestType(str, Enum):
    """测试类型(测试金字塔)"""
    UNIT = "单元测试"
    INTEGRATION = "集成测试"
    E2E = "端到端测试"
    PERFORMANCE = "性能测试"
    SECURITY = "安全测试"


class RequirementType(str, Enum):
    """需求类型"""
    FUNCTIONAL = "功能性需求"
    NON_FUNCTIONAL = "非功能性需求"
    CONSTRAINT = "约束条件"


class DocumentType(str, Enum):
    """文档类型"""
    OVERVIEW = "00-项目概览"
    REQUIREMENTS = "01-需求规格"
    DOMAIN_MODEL = "02-领域模型"
    ARCHITECTURE = "03-架构设计"
    IMPLEMENTATION = "04-实施计划"
    TEST_STRATEGY = "05-测试策略"
    RISK_ASSESSMENT = "06-风险评估"
    QUALITY_REPORT = "07-质量报告"


class DocumentStatus(str, Enum):
    """文档状态"""
    DRAFT = "Draft"
    IN_REVIEW = "In Review"
    APPROVED = "Approved"
    FINAL = "Final"


class DepthLevel(str, Enum):
    """深度级别"""
    SIMPLE = "simple"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class QualityGrade(str, Enum):
    """质量等级"""
    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


# ============================================================================
# 核心原子模型(统一定义,消除重复)
# ============================================================================

@dataclass
class UserStory:
    """
    用户故事(统一定义)
    格式: As a [role], I want [action], So that [value]
    """
    id: str
    as_a: str                           # 角色:作为一个...
    i_want: str                         # 功能:我想要...
    so_that: str                        # 价值:以便...
    acceptance_criteria: List[str]      # 验收标准
    priority: Priority                  # 优先级
    estimated_hours: float = 0.0        # 估算工时(人小时)
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他故事ID


@dataclass
class Feature:
    """特性"""
    id: str
    name: str
    description: str
    user_stories: List[UserStory]
    priority: Priority
    category: ComponentCategory


@dataclass
class AtomicComponent:
    """原子组件"""
    id: str
    name: str
    description: str
    category: ComponentCategory
    dependencies: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)


# ============================================================================
# 需求模型(简化,去除AI属性)
# ============================================================================

@dataclass
class RequirementItem:
    """
    需求项(替代DecomposedRequirement)
    去除: confidence, source, context_signals等AI属性
    """
    id: str
    title: str
    description: str
    type: RequirementType               # 功能/非功能/约束
    priority: Priority
    user_stories: List[UserStory]
    estimated_hours: float = 0.0
    tags: List[str] = field(default_factory=list)


# ============================================================================
# 测试模型(Shift-Left Testing保留)
# ============================================================================

@dataclass
class TestCase:
    """测试用例"""
    id: str
    title: str
    type: TestType
    description: str
    given: str                          # 前置条件
    when: str                           # 操作
    then: str                           # 预期结果
    priority: Priority = Priority.MEDIUM


@dataclass
class ValidationIssue:
    """验证问题"""
    rule_id: str                        # 规则ID: R001, R002...
    severity: Severity
    description: str
    location: str                       # 位置
    suggestion: str                     # 改进建议


@dataclass
class TestPyramid:
    """测试金字塔"""
    unit_tests: int
    integration_tests: int
    e2e_tests: int
    total_tests: int
    coverage_target: float              # 覆盖率目标(%)


@dataclass
class TestStrategy:
    """测试策略"""
    approach: str                       # TDD / BDD / ATDD
    frameworks: List[str]               # Jest, Pytest, Selenium
    pyramid: TestPyramid
    ci_cd_integration: str
    performance_testing: Optional[str] = None
    security_testing: Optional[str] = None


# ============================================================================
# DDD 领域模型
# ============================================================================

@dataclass
class BoundedContext:
    """限界上下文(DDD)"""
    name: str
    description: str
    aggregates: List[str]
    entities: List[str]
    value_objects: List[str]
    domain_events: List[str]
    ubiquitous_language: Dict[str, str]
    dependencies: List[str] = field(default_factory=list)


@dataclass
class Aggregate:
    """聚合根(DDD)"""
    name: str
    description: str
    root_entity: str
    entities: List[str]
    value_objects: List[str]
    invariants: List[str]               # 不变量(业务规则)
    domain_events: List[str]


# ============================================================================
# 架构设计模型
# ============================================================================

@dataclass
class ArchitectureDecisionRecord:
    """架构决策记录(ADR)"""
    id: str                             # ADR-001
    title: str
    date: str
    status: str                         # Proposed / Accepted / Deprecated
    context: str
    decision: str
    consequences: List[str]
    alternatives: List[str] = field(default_factory=list)


@dataclass
class TechStack:
    """技术栈"""
    category: str                       # Frontend / Backend / Database / Infrastructure
    technology: str                     # React / Node.js / PostgreSQL / AWS
    version: str
    justification: str
    alternatives_considered: List[str] = field(default_factory=list)


# ============================================================================
# 风险评估模型
# ============================================================================

@dataclass
class Risk:
    """风险项"""
    id: str                             # RISK-001
    title: str
    category: str                       # Technical / Schedule / Resource / Business
    description: str
    probability: str                    # High / Medium / Low
    impact: str                         # Critical / High / Medium / Low
    severity: Severity
    mitigation: str
    contingency: str
    owner: Optional[str] = None


# ============================================================================
# 实施计划模型
# ============================================================================

@dataclass
class Milestone:
    """里程碑"""
    id: str                             # M1
    name: str
    description: str
    deliverables: List[str]
    estimated_date: str
    dependencies: List[str] = field(default_factory=list)


@dataclass
class WorkBreakdownStructure:
    """工作分解结构(WBS)"""
    phase: str
    features: List[Feature]
    user_stories: List[UserStory]
    components: List[AtomicComponent]
    estimated_hours: float
    milestones: List[Milestone]


# ============================================================================
# 质量评估模型(替代AIAnalysisResult)
# ============================================================================

@dataclass
class QualityMetrics:
    """质量指标(V5: 内容质量驱动)"""
    completeness_score: float           # 完整性评分(0-100)- V5: 结构完整性
    consistency_score: float            # 一致性评分(0-100)- V5: 逻辑一致性
    atomicity_score: float              # 原子性评分(0-100)- V5: 内容实质度
    testability_score: float            # 可测试性评分(0-100)- V5: 验证覆盖度
    overall_grade: QualityGrade         # V5: 总体等级
    overall_score: float = 0.0          # V5: 总体得分(0-100)

    def calculate_overall_grade(self) -> QualityGrade:
        """计算总体等级"""
        avg = (self.completeness_score + self.consistency_score +
               self.atomicity_score + self.testability_score) / 4

        if avg >= 95 and self.consistency_score == 100 and self.atomicity_score >= 90:
            return QualityGrade.A_PLUS
        elif avg >= 90 and self.consistency_score >= 95 and self.atomicity_score >= 85:
            return QualityGrade.A
        elif avg >= 80 and self.consistency_score >= 90 and self.atomicity_score >= 75:
            return QualityGrade.B
        elif avg >= 70:
            return QualityGrade.C
        elif avg >= 60:
            return QualityGrade.D
        else:
            return QualityGrade.F


@dataclass
class QualityReport:
    """
    质量报告(替代AIAnalysisResult)
    去除: confidence, requirement_seeds, context_signals等AI概念
    """
    domain: DomainCategory
    complexity: ComplexityLevel
    estimated_hours: int
    metrics: QualityMetrics
    validation_issues: List[ValidationIssue]
    recommendations: List[str]
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================================
# 文档模型
# ============================================================================

@dataclass
class Document:
    """单个文档"""
    type: DocumentType
    title: str
    version: str
    content: Dict[str, Any]
    markdown: str = ""
    status: DocumentStatus = DocumentStatus.DRAFT
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    token_count: int = 0
    token_budget: int = 15000
    token_usage_percentage: float = 0.0

    def update_token_stats(self, token_count: int):
        """更新token统计"""
        self.token_count = token_count
        self.token_usage_percentage = (token_count / self.token_budget) * 100
        self.updated_at = datetime.now().isoformat()

    def is_within_budget(self) -> bool:
        """检查是否在预算内"""
        return self.token_count <= self.token_budget

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type.value,
            "title": self.title,
            "version": self.version,
            "status": self.status.value,
            "token_count": self.token_count,
            "token_budget": self.token_budget,
            "token_usage": f"{self.token_usage_percentage:.1f}%",
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


# ============================================================================
# 顶层规格文档模型(统一V2和V3)
# ============================================================================

@dataclass
class SpecificationDocument:
    """
    SpecFlow 完整规格文档集
    统一V2.0和V3.0的最佳实践,去除AI虚假概念
    """
    # 项目信息
    project_name: str
    project_version: str
    depth_level: DepthLevel
    spec_version: str = "3.0.0"

    # 8个核心文档
    documents: Dict[DocumentType, Document] = field(default_factory=dict)

    # 原子级组件集合
    components: List[AtomicComponent] = field(default_factory=list)
    user_stories: List[UserStory] = field(default_factory=list)
    features: List[Feature] = field(default_factory=list)
    requirements: List[RequirementItem] = field(default_factory=list)

    # DDD 模型
    bounded_contexts: List[BoundedContext] = field(default_factory=list)
    aggregates: List[Aggregate] = field(default_factory=list)

    # 架构决策
    architecture_decisions: List[ArchitectureDecisionRecord] = field(default_factory=list)
    tech_stack: List[TechStack] = field(default_factory=list)

    # 测试与风险
    test_strategy: Optional[TestStrategy] = None
    test_cases: List[TestCase] = field(default_factory=list)
    risks: List[Risk] = field(default_factory=list)

    # 实施计划
    wbs: List[WorkBreakdownStructure] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)

    # 质量(去除AI相关字段)
    quality_report: Optional[QualityReport] = None

    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_document(self, doc: Document):
        """添加文档"""
        self.documents[doc.type] = doc
        self.updated_at = datetime.now().isoformat()

    def get_document(self, doc_type: DocumentType) -> Optional[Document]:
        """获取文档"""
        return self.documents.get(doc_type)

    def get_total_tokens(self) -> int:
        """获取总token数"""
        return sum(doc.token_count for doc in self.documents.values())

    def get_token_budget(self) -> int:
        """获取总token预算"""
        return sum(doc.token_budget for doc in self.documents.values())

    def get_token_usage_percentage(self) -> float:
        """获取总token使用率"""
        total = self.get_total_tokens()
        budget = self.get_token_budget()
        return (total / budget * 100) if budget > 0 else 0

    def is_within_budget(self) -> bool:
        """检查是否所有文档都在预算内"""
        return all(doc.is_within_budget() for doc in self.documents.values())

    def get_summary(self) -> Dict[str, Any]:
        """获取摘要"""
        return {
            "project_name": self.project_name,
            "project_version": self.project_version,
            "spec_version": self.spec_version,
            "depth_level": self.depth_level.value,
            "documents_count": len(self.documents),
            "components_count": len(self.components),
            "user_stories_count": len(self.user_stories),
            "features_count": len(self.features),
            "total_tokens": self.get_total_tokens(),
            "token_budget": self.get_token_budget(),
            "token_usage": f"{self.get_token_usage_percentage():.1f}%",
            "within_budget": self.is_within_budget(),
            "quality_grade": self.quality_report.metrics.overall_grade.value if self.quality_report else "N/A",
            "validation_issues_count": len(self.quality_report.validation_issues) if self.quality_report else 0,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
