"""
原子级规格生成模块

支持多驱动模式协同生成原子级组件规格
"""

from .schema import (
    AtomicProp,
    AtomicUISpec,
    AtomicInteraction,
    AtomicComponent,
    AtomicAction,
    AtomicTask,
    AtomicSpecification
)

from .coordinator import AtomicSpecCoordinator

__all__ = [
    'AtomicProp',
    'AtomicUISpec',
    'AtomicInteraction',
    'AtomicComponent',
    'AtomicAction',
    'AtomicTask',
    'AtomicSpecification',
    'AtomicSpecCoordinator',
]
