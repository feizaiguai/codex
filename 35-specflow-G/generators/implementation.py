"""
实施计划生成器
负责生成 04-实施计划.md
"""
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, UserStory


class ImplementationGenerator(BaseGenerator):
    """实施计划生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成实施计划文档

        context 必需字段:
            - user_stories: List[UserStory]
            - estimated_hours: int
        """
        # 1. 提取数据
        user_stories: List[UserStory] = context['user_stories']
        estimated_hours: int = context.get('estimated_hours', 0)

        # 2. 按优先级分组
        critical = [us for us in user_stories if us.priority.value == "Critical"]
        high = [us for us in user_stories if us.priority.value == "High"]
        medium = [us for us in user_stories if us.priority.value == "Medium"]
        low = [us for us in user_stories if us.priority.value == "Low"]

        # 3. 准备模板数据
        template_data = {
            'estimated_hours': estimated_hours,
            'estimated_days': round(estimated_hours / 8, 1),
            'critical_count': len(critical),
            'high_count': len(high),
            'medium_count': len(medium),
            'low_count': len(low),
            'critical_stories': critical,
            'high_stories': high,
            'medium_stories': medium,
            'low_stories': low,
        }

        # 4. 尝试使用模板渲染,否则降级到内置生成
        markdown = ""
        try:
            markdown = self.render_template('implementation.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 5. 创建Document对象
        return Document(
            type=DocumentType.IMPLEMENTATION,
            title="实施计划",
            version="1.0.0",
            content=template_data,
            markdown=markdown,
            token_budget=15000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容V3)"""
        parts = []

        # 实施阶段
        parts.append(f"## 实施阶段\n\n")
        parts.append(f"**总估算工时**: {data['estimated_hours']}小时(约{data['estimated_days']}工作日)\n\n")

        # Phase 1: 核心功能
        if data['critical_count'] > 0:
            parts.append(f"### Phase 1: 核心功能({data['critical_count']}个关键故事)\n")
            parts.append("优先级:Critical\n\n")
            for us in data['critical_stories'][:5]:
                parts.append(f"- {us.id}: {us.i_want}\n")
            parts.append("\n")

        # Phase 2: 重要功能
        if data['high_count'] > 0:
            parts.append(f"### Phase 2: 重要功能({data['high_count']}个高优先级故事)\n")
            parts.append("优先级:High\n\n")
            for us in data['high_stories'][:5]:
                parts.append(f"- {us.id}: {us.i_want}\n")
            parts.append("\n")

        # Phase 3: 增强功能
        if data['medium_count'] > 0:
            parts.append(f"### Phase 3: 增强功能({data['medium_count']}个中优先级故事)\n")
            parts.append("优先级:Medium\n\n")
            for us in data['medium_stories'][:5]:
                parts.append(f"- {us.id}: {us.i_want}\n")
            parts.append("\n")

        # 时间线建议
        parts.append(f"## 时间线建议\n\n")
        parts.append(f"- **Phase 1**: {data['estimated_hours'] * 0.5:.0f}小时\n")
        parts.append(f"- **Phase 2**: {data['estimated_hours'] * 0.3:.0f}小时\n")
        parts.append(f"- **Phase 3**: {data['estimated_hours'] * 0.2:.0f}小时\n\n")
        parts.append(f"**总计**: {data['estimated_hours']}小时\n\n")

        return "".join(parts)
