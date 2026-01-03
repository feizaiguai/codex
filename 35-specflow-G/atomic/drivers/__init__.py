"""
多驱动模式

五种驱动模式协同工作:
1. 截图驱动(Screenshot-driven)- UI组件
2. 测试驱动(Test-driven)- BDD场景
3. 领域驱动(Domain-driven)- DDD建模
4. 契约驱动(Contract-driven)- API设计
5. 数据驱动(Data-driven)- 数据模型
"""

from .screenshot_driven import ScreenshotDrivenDriver
from .test_driven import TestDrivenDriver
from .domain_driven import DomainDrivenDriver
from .contract_driven import ContractDrivenDriver
from .data_driven import DataDrivenDriver

__all__ = [
    'ScreenshotDrivenDriver',
    'TestDrivenDriver',
    'DomainDrivenDriver',
    'ContractDrivenDriver',
    'DataDrivenDriver',
]
