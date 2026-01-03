"""
生成器工厂
负责创建和管理所有生成器实例(插件机制)
"""
from typing import Dict, Type
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from generators.overview import OverviewGenerator
from generators.requirements import RequirementsGenerator
from generators.domain_model import DomainModelGenerator
from generators.architecture import ArchitectureGenerator
from generators.implementation import ImplementationGenerator
from generators.test_strategy import TestStrategyGenerator
from generators.risk_assessment import RiskAssessmentGenerator
from generators.quality_report import QualityReportGenerator


class GeneratorFactory:
    """生成器工厂(支持插件注册)"""

    # 生成器注册表(全部8个生成器)
    _generators: Dict[str, Type[BaseGenerator]] = {
        'overview': OverviewGenerator,
        'requirements': RequirementsGenerator,
        'domain_model': DomainModelGenerator,
        'architecture': ArchitectureGenerator,
        'implementation': ImplementationGenerator,
        'test_strategy': TestStrategyGenerator,
        'risk_assessment': RiskAssessmentGenerator,
        'quality_report': QualityReportGenerator,
    }

    @classmethod
    def create(cls, generator_type: str, **kwargs) -> BaseGenerator:
        """
        创建生成器实例

        参数:
            generator_type: 生成器类型
            **kwargs: 传递给生成器构造函数的参数

        返回:
            BaseGenerator: 生成器实例

        异常:
            ValueError: 未知的生成器类型
        """
        generator_class = cls._generators.get(generator_type)
        if not generator_class:
            raise ValueError(
                f"未知的生成器类型: {generator_type}\n"
                f"可用类型: {', '.join(cls._generators.keys())}"
            )

        return generator_class(**kwargs)

    @classmethod
    def register(cls, name: str, generator_class: Type[BaseGenerator]):
        """
        注册新的生成器类型(插件机制)

        参数:
            name: 生成器名称
            generator_class: 生成器类
        """
        cls._generators[name] = generator_class
        print(f"✓ 注册生成器: {name} -> {generator_class.__name__}")

    @classmethod
    def get_all_generators(cls, **kwargs) -> Dict[str, BaseGenerator]:
        """
        获取所有生成器实例

        参数:
            **kwargs: 传递给所有生成器的参数

        返回:
            Dict[str, BaseGenerator]: 生成器字典
        """
        return {
            name: cls.create(name, **kwargs)
            for name in cls._generators.keys()
        }

    @classmethod
    def list_available(cls) -> list:
        """列出所有可用的生成器"""
        return list(cls._generators.keys())
