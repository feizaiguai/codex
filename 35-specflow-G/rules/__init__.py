"""
SpecFlow 规则引擎
基于关键词匹配和预定义规则的需求分析系统
"""

from .knowledge_base import (
    DOMAIN_KEYWORDS,
    COMPLEXITY_PATTERNS,
    REQUIREMENT_PATTERNS,
    TESTABILITY_RULES,
    get_domain_rules,
)

from .validator import (
    RequirementValidator,
    validate_user_story_format,
    calculate_testability_score,
)

from .engine import (
    RulesEngine,
    create_rules_engine,
)

__all__ = [
    # 知识库
    'DOMAIN_KEYWORDS',
    'COMPLEXITY_PATTERNS',
    'REQUIREMENT_PATTERNS',
    'TESTABILITY_RULES',
    'get_domain_rules',

    # 验证器
    'RequirementValidator',
    'validate_user_story_format',
    'calculate_testability_score',

    # 引擎
    'RulesEngine',
    'create_rules_engine',
]
