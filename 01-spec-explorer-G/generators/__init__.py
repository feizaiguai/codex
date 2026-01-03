"""
文档生成器集合

包含：
- gherkin.py: BDD/ATDD场景生成器
- design_doc.py: 设计草稿生成器
"""

from . import gherkin
from . import design_doc

__all__ = ['gherkin', 'design_doc']
