import logging

"""
02-architecture 架构设计专家
V3.0 Final - Gemini S级验收通过

输入：DESIGN_DRAFT.md（来自01-spec-explorer）
输出：ARCHITECTURE.md（输出给35-specflow）
"""

__version__ = "3.0.0"
__author__ = "Claude Code"
__status__ = "Production"

from .core.models import (
    ScaleType,
    ArchitecturePattern,
    TechCategory,
    DesignDraft,
    ScaleAssessment,
    TechStackRecommendation,
    PatternSelection,
    ADRDocument,
    ArchitectureDesign
)

from .architecture_designer import ArchitectureDesigner

__all__ = [
    'ArchitectureDesigner',
    'ScaleType',
    'ArchitecturePattern',
    'TechCategory',
    'DesignDraft',
    'ScaleAssessment',
    'TechStackRecommendation',
    'PatternSelection',
    'ADRDocument',
    'ArchitectureDesign'
]
