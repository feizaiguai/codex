"""
UltraThink - 复杂任务规格文档编写专家
Complex Task Specification Writing Expert

Version: 1.0.0
"""

from .models import (
    UltraThinkInput,
    UltraThinkOutput,
    Phase,
    DepthLevel,
    OutputFormat,
    QualityGrade
)

__version__ = "1.0.0"
__all__ = [
    "UltraThinkInput",
    "UltraThinkOutput",
    "Phase",
    "DepthLevel",
    "OutputFormat",
    "QualityGrade"
]
