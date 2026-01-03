"""
核心数据模型

定义SpecExplorer使用的所有数据结构
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


# ============================================================================
# 枚举类型
# ============================================================================

class Priority(str, Enum):
    """优先级"""
    P0 = "P0"  # 必须有
    P1 = "P1"  # 重要
    P2 = "P2"  # 可选
    P3 = "P3"  # 未来

class RiskLevel(str, Enum):
    """风险等级"""
    HIGH = "🔴 高风险"
    MEDIUM = "🟡 中风险"
    LOW = "🟢 低风险"


# ============================================================================
# 第0层：澄清后的上下文
# ============================================================================

@dataclass
class RequirementContext:
    """需求上下文 - 用于需求分析的核心上下文"""
    core_problem: str  # 核心问题
    target_users: List[str] = field(default_factory=list)  # 目标用户列表
    value_proposition: str = ""  # 价值主张
    technical_challenges: List[str] = field(default_factory=list)  # 技术挑战列表
    mvp_scope: List[str] = field(default_factory=list)  # MVP范围列表


@dataclass
class ClarifiedContext:
    """交互式澄清后的需求上下文"""
    raw_input: str  # 原始输入
    core_problem: str = ""  # 核心问题
    target_users: str = ""  # 目标用户
    value_proposition: str = ""  # 价值主张
    technical_challenges: str = ""  # 技术挑战
    mvp_scope: str = ""  # MVP范围
    examples: List[str] = field(default_factory=list)  # 具体示例


# ============================================================================
# Layer 1: Impact Mapping（目标与价值）
# ============================================================================

@dataclass
class Actor:
    """角色/利益相关者"""
    name: str  # 角色名称（如"区块链开发者"）
    role: str  # 角色类型（如"主要用户"、"付费客户"）
    description: str = ""  # 角色描述


@dataclass
class Impact:
    """期望影响"""
    actor: str  # 对哪个角色
    desired_change: str  # 期望的变化
    metrics: str = ""  # 量化指标（可选）


@dataclass
class ImpactModel:
    """影响地图模型（Layer 1）"""
    goal: str  # Why: 业务目标
    actors: List[Actor] = field(default_factory=list)  # Who: 关键角色
    impacts: List[Impact] = field(default_factory=list)  # How: 期望影响
    deliverables: List[str] = field(default_factory=list)  # What: 交付物列表


# ============================================================================
# Layer 2: Flow Modeling（流程与事件）
# ============================================================================

@dataclass
class DomainEvent:
    """领域事件（Event Storming）"""
    name: str  # 事件名称（如"ContractSubmitted"）
    trigger: str  # 触发命令（如"SubmitContract"）
    description: str = ""  # 事件描述


@dataclass
class UserStory:
    """用户故事"""
    id: str  # 故事ID（如"US-001"）
    title: str  # 故事标题
    description: str  # 故事描述
    priority: Priority = Priority.P1  # 优先级
    stage: str = ""  # 所属阶段


@dataclass
class JourneyStage:
    """用户旅程阶段"""
    name: str  # 阶段名称（如"提交合约"）
    stories: List[str] = field(default_factory=list)  # 包含的故事ID列表


@dataclass
class FlowModel:
    """流程模型（Layer 2）"""
    events: List[DomainEvent] = field(default_factory=list)  # Event Storming事件
    journey_stages: List[JourneyStage] = field(default_factory=list)  # 用户旅程阶段
    user_stories: List[UserStory] = field(default_factory=list)  # 用户故事列表


# ============================================================================
# Layer 3: Domain Modeling（结构与实体）
# ============================================================================

@dataclass
class Entity:
    """实体（DDD）"""
    name: str  # 实体名称（如"SmartContract"）
    attributes: List[str] = field(default_factory=list)  # 属性列表
    behaviors: List[str] = field(default_factory=list)  # 行为列表
    description: str = ""  # 实体描述


@dataclass
class ValueObject:
    """值对象（DDD）"""
    name: str  # 值对象名称（如"Vulnerability"）
    fields: List[str] = field(default_factory=list)  # 字段列表
    description: str = ""  # 描述


@dataclass
class Aggregate:
    """聚合根（DDD）"""
    root: str  # 聚合根名称（如"AuditSession"）
    entities: List[str] = field(default_factory=list)  # 包含的实体
    invariants: List[str] = field(default_factory=list)  # 不变式
    description: str = ""  # 描述


@dataclass
class BoundedContext:
    """限界上下文（DDD）"""
    name: str  # 上下文名称（如"合约分析上下文"）
    entities: List[str] = field(default_factory=list)  # 包含的实体
    responsibilities: str = ""  # 职责描述


@dataclass
class DomainModel:
    """领域模型（Layer 3）"""
    entities: List[Entity] = field(default_factory=list)  # 实体列表
    value_objects: List[ValueObject] = field(default_factory=list)  # 值对象列表
    aggregates: List[Aggregate] = field(default_factory=list)  # 聚合根列表
    bounded_contexts: List[BoundedContext] = field(default_factory=list)  # 限界上下文列表


# ============================================================================
# BDD/ATDD场景
# ============================================================================

@dataclass
class GherkinScenario:
    """Gherkin场景（BDD）"""
    feature: str  # Feature名称
    scenario: str  # Scenario名称
    given: List[str] = field(default_factory=list)  # Given步骤
    when: List[str] = field(default_factory=list)  # When步骤
    then: List[str] = field(default_factory=list)  # Then步骤
    as_a: str = ""  # As a（角色）
    i_want: str = ""  # I want to（目标）
    so_that: str = ""  # So that（价值）


@dataclass
class AcceptanceCriteria:
    """验收标准（ATDD）"""
    story_id: str  # 关联的用户故事ID
    criteria: List[str] = field(default_factory=list)  # 验收标准列表


# ============================================================================
# 风险与假设
# ============================================================================

@dataclass
class Risk:
    """风险"""
    title: str  # 风险标题
    level: RiskLevel  # 风险等级
    description: str  # 风险描述
    mitigation: str = ""  # 缓解措施


@dataclass
class Assumption:
    """假设"""
    title: str  # 假设标题
    description: str  # 假设描述
    needs_validation: bool = True  # 是否需要验证


# ============================================================================
# 完整设计草稿
# ============================================================================

@dataclass
class DesignDraft:
    """完整的设计草稿"""
    project_name: str  # 项目名称
    generated_at: str  # 生成时间

    # 需求概览
    context: ClarifiedContext

    # 三层建模
    impact: ImpactModel  # Layer 1
    flow: FlowModel  # Layer 2
    domain: DomainModel  # Layer 3

    # BDD/ATDD场景
    scenarios: List[GherkinScenario] = field(default_factory=list)
    acceptance_criteria: List[AcceptanceCriteria] = field(default_factory=list)

    # 风险与假设
    risks: List[Risk] = field(default_factory=list)
    assumptions: List[Assumption] = field(default_factory=list)

    # 技术架构建议
    architecture_style: str = ""
    tech_stack: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """转换为Markdown格式（由generator实现）"""
        raise NotImplementedError("使用 generators/design_doc.py 实现")
