"""Core模块 - 数据模型"""
from .models import (
    # 枚举
    ScaleType,
    ArchitecturePattern,
    TechCategory,
    # 输入模型
    DesignDraft,
    create_empty_design_draft,
    # 分析结果模型
    ScaleAssessment,
    TechStackItem,
    TechStackRecommendation,
    PatternSelection,
    # ADR
    ADRDocument,
    # 输出模型
    ArchitectureDesign
)

__all__ = [
    # 枚举
    'ScaleType',
    'ArchitecturePattern',
    'TechCategory',
    # 输入模型
    'DesignDraft',
    'create_empty_design_draft',
    # 分析结果模型
    'ScaleAssessment',
    'TechStackItem',
    'TechStackRecommendation',
    'PatternSelection',
    # ADR
    'ADRDocument',
    # 输出模型
    'ArchitectureDesign'
]
