"""
领域模型生成器
负责生成 02-领域模型.md
"""
from typing import Dict, Any, List, Set
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, DomainCategory, RequirementItem


class DomainModelGenerator(BaseGenerator):
    """领域模型生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成领域模型文档

        context 必需字段:
            - domain: DomainCategory
            - requirements: List[RequirementItem]
        """
        # 1. 提取数据
        domain: DomainCategory = context['domain']
        requirements: List[RequirementItem] = context['requirements']

        # 2. 从需求中提取实体
        entities = self._extract_entities_from_requirements(requirements)

        # 3. 准备模板数据
        template_data = {
            'domain': domain.value,
            'entity_count': len(entities),
            'entities': entities,
        }

        # 4. 尝试使用模板渲染,否则降级到内置生成
        markdown = ""
        try:
            markdown = self.render_template('domain_model.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 5. 创建Document对象
        return Document(
            type=DocumentType.DOMAIN_MODEL,
            title="领域模型",
            version="1.0.0",
            content=template_data,
            markdown=markdown,
            token_budget=18000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容V3)"""
        parts = []

        # 领域概览
        parts.append(f"## 领域概览\n\n")
        parts.append(f"**领域**: {data['domain']}\n\n")
        parts.append(f"本文档描述{data['domain']}领域的核心概念,实体和关系.\n\n")

        # 核心实体
        parts.append(f"## 核心实体\n\n")
        parts.append(f"识别出{data['entity_count']}个核心实体:\n\n")

        for entity in data['entities']:
            parts.append(f"### {entity}\n\n")
            parts.append(f"- **职责**: 管理{entity}相关的业务逻辑\n")
            parts.append(f"- **关键属性**: ID, 名称, 状态, 创建时间, 更新时间\n\n")

        # 限界上下文
        parts.append(f"## 限界上下文\n\n")
        parts.append("建议根据业务边界划分为独立的限界上下文,每个上下文负责特定的业务职能.\n\n")

        return "".join(parts)

    def _extract_entities_from_requirements(self, requirements: List[RequirementItem]) -> List[str]:
        """从需求中提取核心实体(基于关键词规则)"""
        entity_keywords = [
            "用户", "订单", "商品", "支付", "库存", "客户", "产品", "服务",
            "账户", "交易", "文档", "文件", "评论", "消息", "通知", "配置",
            "权限", "角色", "组织", "部门", "项目", "任务", "工单", "报表",
            "日志", "审计", "流程", "规则", "标签", "分类", "模板", "字典"
        ]

        entities: Set[str] = set()

        for req in requirements:
            text = req.title + " " + req.description
            for keyword in entity_keywords:
                if keyword in text:
                    entities.add(keyword)

        return list(entities) if entities else ["业务实体", "数据实体", "服务实体"]
