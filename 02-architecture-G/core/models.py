"""
02-architecture 核心数据模型
遵循零依赖原则，仅使用Python标准库
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


# ===================== 枚举类型 =====================

class ScaleType(str, Enum):
    """系统规模类型"""
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class ArchitecturePattern(str, Enum):
    """架构模式"""
    MONOLITHIC = "Monolithic"
    MICROSERVICES = "Microservices"
    HEXAGONAL = "Hexagonal"
    CQRS = "CQRS"
    EVENT_DRIVEN = "Event-Driven"
    SERVERLESS = "Serverless"
    LAYERED = "Layered"
    CLEAN = "Clean Architecture"


class TechCategory(str, Enum):
    """技术栈类别"""
    BACKEND_LANGUAGE = "Backend Language"
    DATABASE = "Database"
    CACHE = "Cache"
    MESSAGE_QUEUE = "Message Queue"
    API_STYLE = "API Style"
    FRONTEND = "Frontend"


# ===================== 输入数据模型 (来自01-spec-explorer) =====================

@dataclass
class DesignDraft:
    """设计草稿 - 从DESIGN_DRAFT.md解析的数据"""

    # 第一章：需求概述
    project_name: str
    core_value: str
    target_users: str
    user_scale: str  # e.g., "100-1000用户"

    # 第二章：功能设计
    features: List[Dict[str, str]]  # [{"name": "用户管理", "priority": "P0", ...}]

    # 第三章：领域模型
    entities: List[Dict[str, any]]  # [{"name": "User", "attributes": [...], ...}]
    value_objects: List[str]
    aggregates: List[Dict[str, any]]

    # 第四章：上下文映射
    contexts: List[Dict[str, any]]  # [{"name": "用户上下文", "entities": [...], ...}]

    # 第五章：交互设计
    user_stories: List[Dict[str, str]]
    workflows: List[Dict[str, any]]

    # 元数据
    performance_requirements: Optional[Dict[str, str]] = None
    security_requirements: Optional[List[str]] = None

    def __post_init__(self):
        """数据验证"""
        if not self.project_name:
            raise ValueError("项目名称不能为空")
        if not self.target_users:
            raise ValueError("目标用户不能为空")


# ===================== 分析结果数据模型 =====================

@dataclass
class ScaleAssessment:
    """规模评估结果"""
    scale: ScaleType  # Small/Medium/Large
    score: float  # 0-50分
    details: Dict[str, any]  # 每条规则的详细得分
    reasoning: str  # 评估理由

    # 量化指标
    estimated_users: int
    estimated_entities: int
    estimated_contexts: int
    complexity_level: str  # Low/Medium/High

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "scale": self.scale.value,
            "score": self.score,
            "details": self.details,
            "reasoning": self.reasoning,
            "estimated_users": self.estimated_users,
            "estimated_entities": self.estimated_entities,
            "estimated_contexts": self.estimated_contexts,
            "complexity_level": self.complexity_level
        }


@dataclass
class TechStackItem:
    """单项技术栈推荐"""
    category: TechCategory
    recommendation: str  # 推荐的技术
    alternatives: List[str]  # 备选技术
    score: float  # 评分
    reasoning: str  # 选择理由

    def to_dict(self) -> Dict:
        return {
            "category": self.category.value,
            "recommendation": self.recommendation,
            "alternatives": self.alternatives,
            "score": self.score,
            "reasoning": self.reasoning
        }


@dataclass
class TechStackRecommendation:
    """完整技术栈推荐"""
    backend_language: TechStackItem
    database: TechStackItem
    cache: TechStackItem
    message_queue: TechStackItem
    api_style: TechStackItem
    frontend: Optional[TechStackItem] = None

    # 综合评估
    overall_reasoning: str = ""
    total_score: float = 0.0

    def to_dict(self) -> Dict:
        result = {
            "backend_language": self.backend_language.to_dict(),
            "database": self.database.to_dict(),
            "cache": self.cache.to_dict(),
            "message_queue": self.message_queue.to_dict(),
            "api_style": self.api_style.to_dict(),
            "overall_reasoning": self.overall_reasoning,
            "total_score": self.total_score
        }
        if self.frontend:
            result["frontend"] = self.frontend.to_dict()
        return result


@dataclass
class PatternSelection:
    """架构模式选择结果"""
    primary_pattern: ArchitecturePattern
    supporting_patterns: List[ArchitecturePattern]
    reasoning: str

    # 模式特性
    scalability: str  # Low/Medium/High
    complexity: str  # Low/Medium/High
    flexibility: str  # Low/Medium/High

    # 适用场景
    suitable_for: List[str]
    not_suitable_for: List[str]

    def to_dict(self) -> Dict:
        return {
            "primary_pattern": self.primary_pattern.value,
            "supporting_patterns": [p.value for p in self.supporting_patterns],
            "reasoning": self.reasoning,
            "scalability": self.scalability,
            "complexity": self.complexity,
            "flexibility": self.flexibility,
            "suitable_for": self.suitable_for,
            "not_suitable_for": self.not_suitable_for
        }


# ===================== ADR (架构决策记录) =====================

@dataclass
class ADRDocument:
    """单个架构决策记录"""
    adr_id: str  # e.g., "ADR-001"
    title: str
    date: str
    status: str  # Proposed/Accepted/Superseded

    # ADR核心内容
    context: str  # 决策背景
    decision: str  # 决策内容
    consequences: str  # 决策后果

    # 可选字段
    alternatives: Optional[List[str]] = None
    related_adrs: Optional[List[str]] = None

    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        md = f"# {self.adr_id}: {self.title}\n\n"
        md += f"**状态**: {self.status}\n"
        md += f"**日期**: {self.date}\n\n"
        md += f"## 背景\n\n{self.context}\n\n"
        md += f"## 决策\n\n{self.decision}\n\n"
        md += f"## 后果\n\n{self.consequences}\n\n"

        if self.alternatives:
            md += f"## 备选方案\n\n"
            for alt in self.alternatives:
                md += f"- {alt}\n"
            md += "\n"

        if self.related_adrs:
            md += f"## 相关ADR\n\n"
            for adr in self.related_adrs:
                md += f"- {adr}\n"
            md += "\n"

        return md


# ===================== 输出数据模型 (输出给35-specflow) =====================

@dataclass
class ArchitectureDesign:
    """完整架构设计 - 输出到ARCHITECTURE.md"""

    # 元数据（必需字段）
    project_name: str
    scale_assessment: ScaleAssessment
    tech_stack: TechStackRecommendation
    pattern_selection: PatternSelection

    # 元数据（可选字段）
    version: str = "1.0.0"
    date: str = ""

    # 架构决策记录
    adrs: List[ADRDocument] = field(default_factory=list)

    # 架构图表（可选）
    diagrams: Dict[str, str] = field(default_factory=dict)

    # 实施建议
    implementation_phases: List[Dict[str, any]] = field(default_factory=list)
    evolution_path: str = ""

    def to_dict(self) -> Dict:
        """转换为字典（用于JSON序列化）"""
        return {
            "project_name": self.project_name,
            "version": self.version,
            "date": self.date,
            "scale_assessment": self.scale_assessment.to_dict(),
            "tech_stack": self.tech_stack.to_dict(),
            "pattern_selection": self.pattern_selection.to_dict(),
            "adrs": [adr.to_markdown() for adr in self.adrs],
            "implementation_phases": self.implementation_phases,
            "evolution_path": self.evolution_path
        }

    def validate(self) -> bool:
        """验证数据完整性"""
        if not self.project_name:
            raise ValueError("项目名称不能为空")
        if not self.scale_assessment:
            raise ValueError("缺少规模评估结果")
        if not self.tech_stack:
            raise ValueError("缺少技术栈推荐")
        if not self.pattern_selection:
            raise ValueError("缺少架构模式选择")
        return True


# ===================== 辅助函数 =====================

def create_empty_design_draft() -> DesignDraft:
    """创建空的设计草稿（用于测试）"""
    return DesignDraft(
        project_name="",
        core_value="",
        target_users="",
        user_scale="",
        features=[],
        entities=[],
        value_objects=[],
        aggregates=[],
        contexts=[],
        user_stories=[],
        workflows=[]
    )
